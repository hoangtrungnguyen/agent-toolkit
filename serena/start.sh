#!/bin/bash
set -e

# Check if running outside of Docker (optional warning)
if [ -z "$SERENA_DOCKER" ] && [[ "$OSTYPE" == "darwin"* ]]; then
    echo "⚠️  Warning: This script is intended to run inside the Serena Docker container."
    echo "Please use 'docker compose up -d' to start the server first."
    echo "=========================================="
    echo "🚀 Step 0: Open interactive Docker terminal?"
    echo "=========================================="
    read -p "Do you want to enter the container bash now? (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        if docker ps | grep -q serena-container; then
            docker exec -it serena-container bash
        else
            echo "❌ Error: Container 'serena-container' is not running."
            echo "Run 'docker compose up -d' first."
        fi
    fi
    exit 0
fi

# Activate python virtual environment if it exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

# Add Go to PATH
export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"
if ! grep -q "/usr/local/go/bin" /etc/profile; then
    echo 'export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"' >> /etc/profile
fi

# Install Go if not present or wrong version/arch
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
    CURRENT_GO_ARCH=$(go version | awk '{print $4}' | cut -d'/' -f2)
    if [[ "$CURRENT_GO_VERSION" != "go1.25.0" ]] || [[ "$CURRENT_GO_ARCH" != "$GOARCH" ]]; then
        echo "Found Go $CURRENT_GO_VERSION ($CURRENT_GO_ARCH), but need go1.25.0 ($GOARCH). Reinstalling..."
        REINSTALL_GO=true
    fi
fi

if [ "$REINSTALL_GO" = true ]; then
    echo "Installing Go 1.25.0 for $GOARCH..."
    rm -rf /usr/local/go
    curl -LO "https://go.dev/dl/go1.25.0.linux-$GOARCH.tar.gz"
    tar -C /usr/local -xzf "go1.25.0.linux-$GOARCH.tar.gz"
    rm "go1.25.0.linux-$GOARCH.tar.gz"
else
    echo "Go 1.25.0 ($GOARCH) is already installed."
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
