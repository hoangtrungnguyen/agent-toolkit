# Serena Local Development Environment

This repository provides a `docker-compose.yaml` configuration to seamlessly run the Serena MCP (Model Context Protocol) server over SSE locally, fully loaded with necessary Go compilation tools.

## Features Built-in
- **Pre-installed Go environment**: Downloads Go 1.21.0 automatically. 
- **`gopls` language support**: Compiles and runs the official Go language server extension on boot.
- **Auto-mounted Codebase Workspaces**: Maps real local paths (like `/Vikki/digital-platform`) straight into the `/workspace/` folders inside the container for direct project analysis. 

---

## 🚀 1. Starting the Serena Server

To spin up the Serena container and allow it to initialize its toolkit, run the following in your terminal:

```bash
docker compose up -d
```
> *Note: On the first launch, Serena might take a minute or two before it is fully ready because it downloads and compiles Go dependencies and `gopls` dynamically.*

To view the live compilation progress and logs, use:
```bash
docker compose logs -f
```

---

## 🖥 2. Using Serena via the Terminal

There are two primary ways to interact with the running container via the terminal, depending on what you are trying to achieve:

### A. Dropping into an Interactive Bash Shell
If you need to enter the container manually to inspect files, execute manual `bash` commands, test Go compilation, or explore the mounted `/workspace` directories as Serena sees them:

```bash
docker exec -it serena-container bash
```
Once inside, you will have access to the mounted projects in your `/workspace/` folder.

### B. Connecting an Assistant to the Serena Server (Claude Code / Cursor)
The Serena server runs natively over the Model Context Protocol (MCP) using a Server-Sent Events (SSE) transport. Our configuration explicitly exposes port **`9121`** with the `--context claude-code` flag.

If you are using **Claude Code** (the terminal assistant from Anthropic), you can easily add this Serena node by adding the SSE server to your MCP config or connecting it dynamically:
```bash
claude mcp add serena http://localhost:9121/sse
```
*Depending on the precise client requirements, replacing `/sse` with the root or direct messaging paths might be necessary. Once added, your CLI agent will possess all symbolic workspace abilities provided by Serena.*

---

## 🛑 3. Stopping the Container

To shut down the container cleanly and preserve your environment for next time:
```bash
docker compose down
```


---
# CLI configuration

## Per-project configuration

```bash
claude mcp add -t sse serena http://localhost:9121/sse
```

## Global user-level configuration

```bash
claude mcp add --scope user -t sse serena http://localhost:9121/sse
```


---

## 🔌 4. Activating Projects for AI Assistants

Because your AI assistant (e.g., Claude Code, Cursor) runs on your host machine but Serena runs inside Docker, the assistant might incorrectly try to use your host paths (like `/Users/.../grava`) when calling Serena's tools like `activate_project`. This will result in an error:
`ProjectNotFoundError - Project '/Users/.../grava' not found`

**How to resolve:**
When asking your AI assistant to query or analyze a project, simply specify the **container-internal** path. For example:
> "Please activate the project using the container-internal path: `/workspace/grava`"

This guarantees the assistant uses the correct path that Serena recognizes.

---

## 📇 5. Indexing & Re-indexing Projects

### First-time indexing
To index a project so Serena can provide symbolic analysis (functions, classes, dependencies), use the interactive helper:

```bash
sh index.sh
```

Select the project you want to index from the menu. This will scan all source files and build the symbol database.

### Check index status
To see which projects have been indexed:

```bash
sh check.sh
```

### Re-indexing after code changes
Serena picks up most file changes automatically while the server is running. However, a full re-index is needed when:
- **New files or directories** are added that weren't present during the initial index
- A **new language** is added to the project
- The index becomes **stale or corrupted**

To re-index, simply run `sh index.sh` again and select the project, or run directly:

```bash
docker exec -it serena-container bash -c "export PATH=/usr/local/go/bin:/root/go/bin:\$PATH; source .venv/bin/activate && serena project index /workspace/<project-name>"
```

### Adding a new project
1. Add a volume mount in `docker-compose.yaml`:
   ```yaml
   volumes:
     - ../../my-new-project:/workspace/my-new-project
   ```
2. Restart the container:
   ```bash
   docker compose up -d --force-recreate
   ```
3. Index the new project:
   ```bash
   sh index.sh
   ```