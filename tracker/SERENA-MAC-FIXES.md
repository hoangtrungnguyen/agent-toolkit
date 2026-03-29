---
issue: SERENA-MAC-FIXES
status: done
Description: Fixed ARM64/Mac architecture mismatch preventing Go/gopls installation in Docker, replaced bash-specific `mapfile` with POSIX-compatible loops, persisted Go PATH for docker exec, and updated ReadMe with CLI config and indexing docs.
---

**Timestamp:** 2026-03-29 18:07:00
**Affected Modules:**
  - serena/start.sh
  - serena/check.sh
  - serena/index.sh
  - serena/docker-compose.yaml
  - serena/ReadMe.md

---

## Session Details

### Problems Fixed
1. **`gcc: error: unrecognized command-line option '-m64'`** — `start.sh` hardcoded `go1.21.0.linux-amd64.tar.gz`. On Apple Silicon (arm64), Docker runs an arm64 container whose gcc doesn't support `-m64`. Fixed by detecting `uname -m` and selecting the correct Go archive.
2. **`gopls requires go >= 1.25`** — Upgraded Go from 1.21.0 to 1.25.0.
3. **`mapfile: command not found`** — macOS default `sh` doesn't support `mapfile`. Replaced with `while IFS= read -r` loops in `check.sh` and `index.sh`.
4. **`gopls is not installed` during indexing** — `gopls` was installed to `/root/go/bin` but that wasn't in the PATH for `docker exec` sessions. Added `/root/go/bin` to the PATH in `index.sh` and persisted the Go PATH to `/etc/profile` in `start.sh`.
5. **Documentation gaps** — Updated ReadMe with correct `claude mcp add -t sse` command and added a full section on indexing/re-indexing projects.

### Commits
- `fix(serena): architectural awareness for Go and macOS shell compatibility`
- `docs(serena): add indexing/re-indexing guide and session tracker`

### Current State
- Serena container boots successfully on Apple Silicon
- Go 1.25.0 (arm64) and gopls install correctly
- `grava` project indexed successfully (556 files: 423 python, 117 go, 16 bash)
- `takumi-ide` volume mount added to docker-compose.yaml (not yet indexed)
