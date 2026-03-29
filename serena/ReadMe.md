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
claude mcp add serena --url http://localhost:9121/sse  
  
## Global user-level configuration    
claude mcp add --scope user serena --url http://localhost:9121/sse