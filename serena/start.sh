#!/bin/bash
set -e

# Activate python virtual environment
source .venv/bin/activate

# Add Go to PATH
export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"

# Install Go if not present
if ! command -v go &> /dev/null; then
    echo "Installing Go 1.21.0..."
    curl -LO https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
    rm go1.21.0.linux-amd64.tar.gz
else
    echo "Go is already installed."
fi

# Install gopls if not present
if ! command -v gopls &> /dev/null; then
    echo "Installing gopls..."
    go install golang.org/x/tools/gopls@latest
else
    echo "gopls is already installed."
fi

# Install Erlang if not present
if ! dpkg -s erlang-nox &> /dev/null; then
    echo "Installing erlang-nox..."
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y erlang-nox
else
    echo "erlang-nox is already installed."
fi

# Install Erlang LS if not present
if ! command -v erlang_ls &> /dev/null; then
    echo "Installing erlang_ls..."
    curl -LO https://github.com/erlang-ls/erlang_ls/releases/download/1.1.0/erlang_ls-linux-27.tar.gz
    tar -C /usr/local/bin -xzf erlang_ls-linux-27.tar.gz
    rm erlang_ls-linux-27.tar.gz
    chmod +x /usr/local/bin/erlang_ls
else
    echo "erlang_ls is already installed."
fi

echo "Starting serena-mcp-server..."
exec uv run --directory . serena-mcp-server --transport sse --port 9121 --host 0.0.0.0 --context claude-code
