#!/bin/bash
set -e

# Activate python virtual environment
source .venv/bin/activate

# Add Go to PATH
export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"

# Install Go if not present or wrong version
ARCH=$(uname -m)
case "$ARCH" in
    x86_64) GOARCH="amd64" ;;
    aarch64|arm64) GOARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

REINSTALL_GO=false
if ! command -v go &> /dev/null; then
    REINSTALL_GO=true
else
    CURRENT_GO_VERSION=$(go version | awk '{print $3}')
    if [[ "$CURRENT_GO_VERSION" != "go1.25.8" ]]; then
        echo "Found Go $CURRENT_GO_VERSION, but need go1.25.8. Reinstalling..."
        REINSTALL_GO=true
    fi
fi

if [ "$REINSTALL_GO" = true ]; then
    echo "Installing Go 1.25.8 for $GOARCH..."
    rm -rf /usr/local/go
    curl -LO "https://go.dev/dl/go1.25.8.linux-$GOARCH.tar.gz"
    tar -C /usr/local -xzf "go1.25.8.linux-$GOARCH.tar.gz"
    rm "go1.25.8.linux-$GOARCH.tar.gz"
else
    echo "Go 1.25.8 is already installed."
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
