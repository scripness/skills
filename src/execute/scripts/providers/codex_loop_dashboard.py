#!/usr/bin/env python3
"""Terminal dashboard wrapper for the local Codex loop helper.

This file is presentation only. It sits above `codex_loop.py`, consumes the
generic loop's JSON event stream, and renders a live terminal view. It does
not own loop control, plan writes, or verdict logic.

When the dashboard is unsuitable, such as non-TTY output, `--plain`, or help
requests, this script falls back to the raw `codex_loop.py` output surface.
"""

from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path


REFRESH_INTERVAL_SECONDS = 0.1
MAX_EVENT_LINES = 8
MAX_DIAG_LINES = 6


def codex_loop_path() -> Path:
    return Path(__file__).resolve().with_name("codex_loop.py")


def build_command(argv: list[str]) -> list[str]:
    return [sys.executable, str(codex_loop_path()), *argv]


def should_passthrough(argv: list[str]) -> bool:
    if "--plain" in argv:
        return True
    if "--help" in argv or "-h" in argv:
        return True
    if not sys.stdout.isatty():
        return True
    return os.environ.get("TERM", "").lower() in {"", "dumb"}


def strip_dashboard_args(argv: list[str]) -> list[str]:
    return [arg for arg in argv if arg != "--plain"]


def format_duration(seconds: float) -> str:
    total = max(0, int(seconds))
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def truncate(text: str, width: int) -> str:
    if width <= 0:
        return ""
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return f"{text[:width - 3]}..."


def progress_bar(completed: int, total: int, width: int) -> str:
    if total <= 0:
        return "-" * max(1, width)
    filled = int(round((completed / total) * width))
    filled = max(0, min(width, filled))
    return f"{'#' * filled}{'-' * (width - filled)}"


def bool_label(value: bool) -> str:
    return "yes" if value else "no"


def summarize_event(event: dict[str, object]) -> str:
    event_name = str(event.get("event", "unknown"))
    if event_name == "start":
        state = event.get("initial_state", {}) or {}
        return (
            "start: "
            f"remaining={state.get('remaining_milestones', '?')} "
            f"continue_after_fail={event.get('continue_after_fail', False)}"
        )
    if event_name == "phase":
        return (
            f"phase {event.get('phase', '?')} {event.get('status', '?')}: "
            f"iteration={event.get('iteration', '?')}"
        )
    if event_name == "iteration":
        return (
            f"iteration {event.get('iteration', '?')}: "
            f"status={event.get('status', '?')} "
            f"verdict={event.get('verification_verdict', '-')}"
        )
    if event_name == "final_review":
        return (
            f"final review: status={event.get('status', '?')} "
            f"verdict={event.get('verification_verdict', '-')}"
        )
    if event_name == "stop":
        return (
            f"stop: outcome={event.get('final_outcome', '?')} "
            f"reason={event.get('reason', '?')}"
        )
    return json.dumps(event, sort_keys=True)


@dataclass
class DashboardState:
    command: list[str]
    started_at: float
    start_event: dict[str, object] | None = None
    stop_event: dict[str, object] | None = None
    current_event: dict[str, object] | None = None
    current_state: dict[str, object] | None = None
    current_phase: str | None = None
    current_iteration: int | None = None
    latest_status: str | None = None
    latest_verdict: str | None = None
    latest_outcome: str | None = None
    log_root: str | None = None
    latest_logs: dict[str, str] = field(default_factory=dict)
    event_lines: deque[str] = field(
        default_factory=lambda: deque(maxlen=MAX_EVENT_LINES)
    )
    diag_lines: deque[str] = field(
        default_factory=lambda: deque(maxlen=MAX_DIAG_LINES)
    )
    raw_stdout_lines: deque[str] = field(
        default_factory=lambda: deque(maxlen=MAX_EVENT_LINES)
    )
    child_returncode: int | None = None

    def update_from_event(self, event: dict[str, object]) -> None:
        event_name = str(event.get("event", "unknown"))
        self.current_event = event
        self.event_lines.append(summarize_event(event))

        if event_name == "start":
            self.start_event = event
            self.current_state = event.get("initial_state") or None
            self.log_root = event.get("log_root") if isinstance(event.get("log_root"), str) else None
            self.latest_status = "running"
            return

        if event_name == "phase":
            self.current_phase = str(event.get("phase", "unknown"))
            self.current_iteration = (
                int(event["iteration"]) if isinstance(event.get("iteration"), int) else self.current_iteration
            )
            if event.get("status") == "start":
                self.latest_status = f"{self.current_phase} running"
                self.current_state = event.get("state_before") or self.current_state
            else:
                self.latest_status = f"{self.current_phase} finished"
                self.current_state = event.get("state_after") or self.current_state
                result = event.get("result")
                if isinstance(result, dict):
                    self.latest_logs.update(
                        {
                            "stdout_log": str(result.get("stdout_log", "")),
                            "stderr_log": str(result.get("stderr_log", "")),
                            "label": str(result.get("label", "")),
                        }
                    )
                verdict = event.get("verification_verdict")
                if isinstance(verdict, str):
                    self.latest_verdict = verdict
            return

        if event_name == "iteration":
            self.current_iteration = (
                int(event["iteration"]) if isinstance(event.get("iteration"), int) else self.current_iteration
            )
            self.latest_status = str(event.get("status", "running"))
            verdict = event.get("verification_verdict")
            if isinstance(verdict, str):
                self.latest_verdict = verdict
            self.current_state = event.get("state_after_verify") or self.current_state
            verify = event.get("verify")
            if isinstance(verify, dict):
                self.latest_logs.update(
                    {
                        "verify_stdout_log": str(verify.get("stdout_log", "")),
                        "verify_stderr_log": str(verify.get("stderr_log", "")),
                    }
                )
            execute = event.get("execute")
            if isinstance(execute, dict):
                self.latest_logs.update(
                    {
                        "execute_stdout_log": str(execute.get("stdout_log", "")),
                        "execute_stderr_log": str(execute.get("stderr_log", "")),
                    }
                )
            return

        if event_name == "final_review":
            self.current_phase = "final_verify"
            self.current_iteration = (
                int(event["iteration"]) if isinstance(event.get("iteration"), int) else self.current_iteration
            )
            self.latest_status = str(event.get("status", "running"))
            verdict = event.get("verification_verdict")
            if isinstance(verdict, str):
                self.latest_verdict = verdict
            self.current_state = event.get("state_after") or self.current_state
            verify = event.get("verify")
            if isinstance(verify, dict):
                self.latest_logs.update(
                    {
                        "final_verify_stdout_log": str(verify.get("stdout_log", "")),
                        "final_verify_stderr_log": str(verify.get("stderr_log", "")),
                    }
                )
            return

        if event_name == "stop":
            self.stop_event = event
            self.latest_outcome = str(event.get("final_outcome", "unknown"))
            self.latest_status = str(event.get("reason", "stopped"))
            self.current_state = event.get("state") or self.current_state


def read_stream(
    name: str,
    stream: subprocess.PIPE,
    output_queue: queue.Queue[tuple[str, str | None]],
) -> None:
    try:
        assert stream is not None
        for line in stream:
            output_queue.put((name, line.rstrip("\n")))
    finally:
        output_queue.put((name, None))


def section(title: str, lines: list[str], width: int) -> list[str]:
    header = f"{title}:"
    rendered = [header]
    for line in lines:
        rendered.append(f"  {truncate(line, max(1, width - 2))}")
    if not lines:
        rendered.append("  -")
    return rendered


def render_dashboard(state: DashboardState) -> None:
    width = max(80, shutil.get_terminal_size(fallback=(100, 32)).columns)
    separator = "=" * width
    current_state = state.current_state or {}
    completed = int(current_state.get("completed_milestones", 0) or 0)
    total = int(current_state.get("total_milestones", 0) or 0)
    remaining = int(current_state.get("remaining_milestones", 0) or 0)
    next_milestone = str(current_state.get("next_milestone") or "None")
    blockers = current_state.get("blockers") if isinstance(current_state.get("blockers"), list) else []
    blocker_lines = [str(item) for item in blockers] if blockers else ["None currently."]
    outcome = state.latest_outcome or "running"
    phase = state.current_phase or "idle"
    iteration = state.current_iteration if state.current_iteration is not None else "-"
    verdict = state.latest_verdict or "-"
    elapsed = format_duration(time.time() - state.started_at)
    log_root = state.log_root or "-"
    plan = "-"
    continue_after_fail = "-"
    allow_pass_with_risks = "-"
    provider_command = "-"
    if state.start_event is not None:
        plan = str(state.start_event.get("plan", "-"))
        continue_after_fail = bool_label(bool(state.start_event.get("continue_after_fail", False)))
        allow_pass_with_risks = bool_label(bool(state.start_event.get("allow_pass_with_risks", False)))
        provider_command = " ".join(str(part) for part in state.start_event.get("provider_command", []))

    summary_lines = [
        truncate(
            f"status={state.latest_status or 'starting'} outcome={outcome} phase={phase} iteration={iteration} elapsed={elapsed}",
            width,
        ),
        truncate(
            f"plan={plan}",
            width,
        ),
        truncate(
            f"provider={provider_command}",
            width,
        ),
        truncate(
            f"continue_after_fail={continue_after_fail} allow_pass_with_risks={allow_pass_with_risks} verdict={verdict}",
            width,
        ),
        truncate(
            f"progress=[{progress_bar(completed, total, 24)}] {completed}/{total} complete, remaining={remaining}, next={next_milestone}",
            width,
        ),
        truncate(f"log_root={log_root}", width),
    ]

    log_lines = [
        f"{key}={value}"
        for key, value in state.latest_logs.items()
        if value and key.endswith("_log")
    ]

    lines: list[str] = [
        separator,
        truncate("Codex Loop Dashboard", width),
        separator,
        *section("Summary", summary_lines, width),
        "-" * width,
        *section("Recent events", list(state.event_lines), width),
        "-" * width,
        *section("Diagnostics", list(state.diag_lines), width),
        "-" * width,
        *section("Latest logs", log_lines, width),
        "-" * width,
        *section("Blockers", blocker_lines, width),
    ]
    if state.raw_stdout_lines:
        lines.extend(["-" * width, *section("Raw stdout", list(state.raw_stdout_lines), width)])
    lines.append(separator)

    output = "\x1b[H\x1b[2J" + "\n".join(lines)
    sys.stdout.write(output)
    sys.stdout.flush()


def passthrough(command: list[str]) -> int:
    completed = subprocess.run(command)
    return completed.returncode


def dashboard_main(argv: list[str]) -> int:
    forwarded_args = strip_dashboard_args(argv)
    command = build_command(forwarded_args)
    state = DashboardState(command=command, started_at=time.time())

    try:
        child = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
    except OSError as exc:
        print(f"failed to start Codex loop wrapper: {exc}", file=sys.stderr)
        return 3

    output_queue: queue.Queue[tuple[str, str | None]] = queue.Queue()
    threads = [
        threading.Thread(
            target=read_stream, args=("stdout", child.stdout, output_queue), daemon=True
        ),
        threading.Thread(
            target=read_stream, args=("stderr", child.stderr, output_queue), daemon=True
        ),
    ]
    for thread in threads:
        thread.start()

    done_streams = 0
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()
    try:
        while done_streams < len(threads) or child.poll() is None:
            try:
                stream_name, payload = output_queue.get(timeout=REFRESH_INTERVAL_SECONDS)
            except queue.Empty:
                render_dashboard(state)
                continue

            if payload is None:
                done_streams += 1
                render_dashboard(state)
                continue

            if stream_name == "stderr":
                if payload:
                    state.diag_lines.append(payload)
            else:
                if not payload:
                    continue
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    state.raw_stdout_lines.append(payload)
                else:
                    if isinstance(event, dict):
                        state.update_from_event(event)
                    else:
                        state.raw_stdout_lines.append(payload)
            render_dashboard(state)

        state.child_returncode = child.wait()
        render_dashboard(state)
        return state.child_returncode
    finally:
        sys.stdout.write("\x1b[?25h\n")
        sys.stdout.flush()


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if should_passthrough(argv):
        return passthrough(build_command(strip_dashboard_args(argv)))
    return dashboard_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
