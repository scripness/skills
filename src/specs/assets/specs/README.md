# [Project Name] Specifications

[One sentence describing what this spec set covers.]

## How To Use These Specs

- Read the relevant spec before implementing in that area.
- Treat specs as intent and code as implemented reality.
- Keep specs focused on one topic of concern per file.
- Use specs for durable topic truth, not execution planning or task checklists.
- Map each spec to the owning app, package, service, or shared subsystem the
  repo actually uses rather than assuming one default layout.
- Reference owning code paths only; ignore generated, vendor, cache, and
  copied-artifact trees unless a spec explicitly owns them.
- Update this index when specs are added, removed, renamed, or materially
  repurposed.

## Product And Domain

| Spec | Owning paths | Purpose |
|------|--------------|---------|
| [`[domain].md`](./[domain].md) | `[path, package, app, or service]` | [what it defines] |

## Architecture And Shared Systems

| Spec | Owning paths | Purpose |
|------|--------------|---------|
| [`[architecture].md`](./[architecture].md) | `[path, package, app, or service]` | [what it defines] |

## Quality And Operations

| Spec | Owning paths | Purpose |
|------|--------------|---------|
| [`[testing-strategy].md`](./[testing-strategy].md) | `[path, package, app, or service]` | [what it defines] |
