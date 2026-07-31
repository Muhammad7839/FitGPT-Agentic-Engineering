# Image Storage Backends

Reference for the backend's server-side image storage adapters, defined in
[`backend/app/storage.py`](../../backend/app/storage.py) and configured via
[`backend/app/config.py`](../../backend/app/config.py).

> **Context**: as noted in `docs/features/architecture.md`, wardrobe images
> uploaded through the web app are currently thumbnailed and stored
> client-side as base64 data URLs. The adapters described here are the
> backend's own image storage layer (used for any bytes uploaded through the
> backend), and are the mechanism the codebase provides for moving image
> storage off the local filesystem and onto S3-compatible object storage.

## Overview

`backend/app/storage.py` exposes a single `ImageStorage` protocol with one
method:

```python
def save(self, filename: str, data: bytes, content_type: str) -> str:
    """Save image bytes and return the URL clients should store."""
```

Two concrete implementations exist:

- `LocalStorage` — writes files to disk under `backend/uploads/`.
- `S3Storage` — uploads bytes to an S3-compatible bucket via `boto3`
  (`boto3>=1.34` is listed in `backend/requirements.txt`).

A module-level singleton, `get_storage()`, picks the implementation based on
the `STORAGE_BACKEND` environment variable and caches the instance for the
life of the process (`_storage` global in `storage.py`).

## Configuration variables

All variables are read in `backend/app/config.py` via `get_env(name, default)`,
which falls back to the given default when the variable is unset or empty.
None of these appear in `backend/.env.example` today, so they must be added
to a local `.env` (or the deployment environment) manually if the S3/R2
backend is needed.

| Variable | Default | Purpose |
|---|---|---|
| `STORAGE_BACKEND` | `local` | Selects the adapter. Accepted values: `local`, `s3`, `r2`. Any other value raises `RuntimeError` from `get_storage()`. |
| `S3_BUCKET` | `""` | Target bucket name for `S3Storage`. |
| `S3_ENDPOINT_URL` | `""` | Custom S3-compatible endpoint. Passed to `boto3.client("s3", endpoint_url=...)`; empty string is converted to `None`, letting `boto3` use AWS's default endpoint resolution. |
| `S3_ACCESS_KEY_ID` | `""` | Access key passed to `boto3.client(...)`. |
| `S3_SECRET_ACCESS_KEY` | `""` | Secret key passed to `boto3.client(...)`. |
| `S3_PUBLIC_BASE_URL` | `""` | Base URL prefixed onto stored object keys when building the URL returned to callers. |

`STORAGE_BACKEND` is lower-cased and stripped in `config.py`
(`STORAGE_BACKEND = get_env("STORAGE_BACKEND", "local").strip().lower()`), so
`S3`, `s3`, and ` s3 ` are all treated the same.

The `config.py` source also carries this operational note as a comment:

> In production on Render, set `STORAGE_BACKEND=local` (default). Images are
> now stored client-side as base64. If upgrading to S3/R2, set
> `STORAGE_BACKEND=s3` and all `S3_*` vars.

## `local` backend

`LocalStorage.__init__` creates `backend/uploads/` (`LOCAL_UPLOAD_DIR`,
resolved from `BACKEND_ROOT / "uploads"`) if it doesn't already exist.

`save(filename, data, content_type)`:
1. Writes `data` to `backend/uploads/<filename>` (`content_type` is accepted
   for interface parity with `S3Storage` but not otherwise used by
   `LocalStorage`).
2. Returns `/uploads/<filename>` — a relative path, not an absolute URL.

`backend/app/main.py` only mounts this directory as static files when
`STORAGE_BACKEND == "local"`:

```python
if STORAGE_BACKEND == "local":
    LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=LOCAL_UPLOAD_DIR), name="uploads")
```

This means the `/uploads/<filename>` path returned by `LocalStorage.save()`
is only reachable through the running backend process — it is not a
standalone or CDN-backed URL, and callers must resolve it against the
backend's own base URL.

## `s3` / `r2` backend

Both `STORAGE_BACKEND=s3` and `STORAGE_BACKEND=r2` route to the same
`S3Storage` class in `get_storage()`. The repository does not implement
separate behavior for `r2`; `S3_ENDPOINT_URL` can supply a custom
S3-compatible endpoint for either setting.

`S3Storage.__init__`:
1. Validates that `S3_BUCKET`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`,
   and `S3_PUBLIC_BASE_URL` are all non-empty. If any are missing, it raises
   `RuntimeError("Missing S3 storage configuration: <missing names>")` —
   this happens at first use (when `get_storage()` first constructs the
   singleton), not at process startup.
2. Imports `boto3` lazily (inside `__init__`, not at module scope), so the
   `local` backend never requires `boto3` to be installed.
3. Stores `S3_PUBLIC_BASE_URL` with any trailing `/` stripped
   (`.rstrip("/")`).
4. Constructs a `boto3` S3 client with `endpoint_url=S3_ENDPOINT_URL or None`,
   `aws_access_key_id=S3_ACCESS_KEY_ID`, `aws_secret_access_key=S3_SECRET_ACCESS_KEY`.

`save(filename, data, content_type)`:
1. Calls `put_object(Bucket=self.bucket, Key=filename, Body=data, ContentType=content_type)`.
2. Returns `f"{self.public_base_url}/{filename}"`.

Notes on this behavior:
- The object key is exactly `filename` as passed in — there's no prefixing,
  namespacing, or extension normalization performed by `storage.py` itself.
- Bucket/object ACLs are not set by this code; whether the returned URL is
  publicly fetchable depends entirely on the bucket's own configuration
  (such as a public bucket policy or CDN configuration)
  matching what `S3_PUBLIC_BASE_URL` points to.
- No retry, error handling, or logging wraps `put_object` — a `boto3`
  exception (e.g. `ClientError` for bad credentials or a missing bucket)
  propagates directly out of `save()`.

## Returned URL behavior summary

| Backend | Return value shape | Directly fetchable without the backend running? |
|---|---|---|
| `local` | `/uploads/<filename>` (relative path) | No — served only via the backend's own `/uploads` static mount. |
| `s3` / `r2` | A string formed as `<S3_PUBLIC_BASE_URL>/<filename>` | Whether it is an absolute and publicly usable URL depends on the configured `S3_PUBLIC_BASE_URL` and the object-storage or CDN configuration. |

Callers that persist these values (e.g. as a wardrobe item's `image_url`)
should be aware that switching `STORAGE_BACKEND` after images already exist
does not migrate or rewrite previously stored URLs.

## Secret-handling guidance

- `S3_ACCESS_KEY_ID` and `S3_SECRET_ACCESS_KEY` are credentials, not
  configuration flags. Never commit them to `.env.example`, documentation,
  code, or version control. `backend/.env.example` currently contains no
  `S3_*` entries — if you add real placeholders there, use clearly fake
  values (e.g. `your_s3_access_key_id_here`) following the existing
  convention used for `SECRET_KEY`, `GROQ_API_KEY`, etc.
- Set real values only in an untracked `backend/.env` file or in your
  deployment platform's secret/environment configuration (e.g. Render
  environment variables). `backend/.env` is expected to be excluded from
  version control per the project's existing `.env` handling described in
  `README.md`.
- Scope the credentials to the minimum S3 permissions needed
  (`PutObject` on the target bucket/prefix) — `S3Storage.save()` only ever
  calls `put_object`, so the app does not need broader bucket permissions
  such as delete or list.
- If a key is ever exposed (committed, logged, or pasted into a shared
  channel), rotate it in the provider console immediately; `storage.py` does
  not cache or persist credentials beyond the `boto3` client instance held in
  the process, so restarting the backend with rotated values is sufficient
  to pick up new credentials.
- `S3_PUBLIC_BASE_URL` and `S3_ENDPOINT_URL` are commonly non-secret service
  URLs, but treat them as sensitive when they contain embedded credentials,
  signed query parameters, private hostnames, account identifiers, or other
  restricted information. Confirm the bucket behind `S3_PUBLIC_BASE_URL` is
  intended to be public before relying on it for user-facing image URLs,
  since `storage.py` performs no access-control checks of its own.

## Troubleshooting

- **`RuntimeError: Unsupported STORAGE_BACKEND '<value>'`** — `STORAGE_BACKEND`
  is set to something other than `local`, `s3`, or `r2`. Check for typos or
  stray whitespace/casing in the environment variable (the value is
  lower-cased and stripped, so this indicates a genuinely different string).
- **`RuntimeError: Missing S3 storage configuration: ...`** — one or more of
  `S3_BUCKET`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_PUBLIC_BASE_URL`
  is empty or unset while `STORAGE_BACKEND` is `s3` or `r2`. The error message
  lists exactly which names are missing. `S3_ENDPOINT_URL` is intentionally
  excluded from this check since it's optional for AWS S3.
- **Uploads succeed locally but images 404 in the browser (`local` backend)** —
  confirm `STORAGE_BACKEND` is actually `local` at startup, since the
  `/uploads` static mount in `main.py` is only registered when
  `STORAGE_BACKEND == "local"` at import time. Changing the environment
  variable requires restarting the backend process for the mount to
  (dis)appear.
- **Images upload but the returned URL isn't publicly reachable (`s3`/`r2`
  backend)** — this is a bucket/CDN configuration issue, not something
  `storage.py` controls. Verify the object-storage or CDN public-access
  configuration matches the host in `S3_PUBLIC_BASE_URL`, and that
  `S3_PUBLIC_BASE_URL` actually points at that public host (not the
  authenticated API endpoint).
- **`boto3` `ClientError` / `NoCredentialsError` on save** — credentials or
  bucket name are wrong, or `S3_ENDPOINT_URL` is missing/incorrect for a
  custom S3-compatible service, causing `boto3` to use a different endpoint
  than intended. `S3Storage` does not catch or wrap these errors, so the raw
  `boto3` exception and message are the best diagnostic signal.
- **`ModuleNotFoundError: boto3`** — only occurs when `STORAGE_BACKEND` is
  `s3`/`r2` (the `local` backend never imports `boto3`). Confirm
  `backend/requirements.txt` (`boto3>=1.34`) is installed in the active
  environment.
- **Switching backends doesn't update old image URLs** — expected; `save()`
  only affects new uploads. Existing stored `image_url` values keep whatever
  string form (`/uploads/...` or `<S3_PUBLIC_BASE_URL>/...`) they had when
  they were originally saved.
