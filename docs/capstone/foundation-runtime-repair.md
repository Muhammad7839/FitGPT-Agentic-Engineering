# Foundation Runtime Repair

## Initial state

- Repository branch: `capstone/aura-forge`
- Historical Module 4 starting commit: `31af8c300dbdcac6ddb16fdf97d015cc04d83f28`
- Trusted sandbox: root `Dockerfile`, verified from local Git history as the FitGPT Agentic Engineering sandbox.

## Failure 1

The trusted sandbox built, but the governed MCP modules failed to import because the sandbox did not include the MCP runtime expected by the existing server code:

```text
ModuleNotFoundError: No module named 'mcp.server'
```

## Repair attempt 1

The first repair attempt added a broad v1 constraint:

```text
mcp>=1.2,<2
```

That resolved to `mcp 1.29.0`. The `FastMCP` import succeeded, but real server registration failed under the sandbox's existing Pydantic behavior. This was preserved diagnostic evidence, not a successful configuration.

## Repair investigation

Package metadata established the compatibility boundary:

- `mcp 1.12.0` supports `pydantic>=2.8.0,<3.0.0`
- `mcp 1.13.0` raises the minimum to `pydantic>=2.11.0,<3.0.0`

The reproducible dependency decision is:

```text
mcp==1.12.0
pydantic==2.9.2
```

## Failure 2

With dependencies installed cleanly, both real governed server modules still failed during FastMCP tool registration:

```text
TypeError: issubclass() arg 1 must be a class
```

## Root-cause investigation

Both governed MCP servers used postponed annotations:

```python
from __future__ import annotations
```

FastMCP 1.12.0 reads raw parameter annotations during Context detection and calls `issubclass(param.annotation, Context)`. With postponed annotations enabled, parameters such as `entry_id: str`, `limit: int`, and `query: str` are raw strings, causing `issubclass('str', Context)` to fail.

The mechanism was proven with full tracebacks, installed SDK inspection, tool-by-tool registration tests, a minimal reproduction, and temporary copies of both real servers. Temporary copies imported successfully when only the future-annotations import was removed.

## Final fix

- Added the exact runtime pin: `mcp==1.12.0`
- Removed `from __future__ import annotations` from:
  - `mcp-servers/storage/server.py`
  - `mcp-servers/retrieval/server.py`
- Added focused regression coverage in `eval/test_mcp_runtime.py`

No governance behavior, tool authorization, allow-list, classification ceiling, storage behavior, retrieval behavior, or production code was intentionally changed.

## Final evidence

- Rebuilt image: `sha256:94a926df6f47d17b45ec2f8094f34a48503930e99f7732440d6db15b8384e511`
- MCP version: `1.12.0`
- Pydantic version: `2.9.2`
- `python -m pip check`: `No broken requirements found.`
- FastMCP import: PASS
- Storage MCP import: PASS
- Retrieval MCP import: PASS
- Targeted regression: `1 passed`
- Read-only workspace denial: write to `/workspace/.milestone0f-ro-write-probe-DO-NOT-CREATE` failed with `Read-only file system`
- Module 4 policy tests: `16 passed`
- Locked holdout SHA-256: `e3aa9cdcec7b643507b7dd6f03ea15d92cfb6ed5fcacc4f56f5b2a8631631f32`

All verification was local, deterministic, no-secret, and non-production. No Claude authentication was mounted, no model call was invoked, and no production FitGPT, Render, Vercel, or database endpoint was contacted.
