#!/bin/bash
set -e

echo "🔑 Generating secure keys for AVIK Sandbox Shield..."

# Create key directory
mkdir -p /etc/avik/keys 2>/dev/null || mkdir -p ~/.avik/keys

KEY_DIR=${KEY_DIR:-/etc/avik/keys}
FALLBACK_DIR=~/.avik/keys

# Master key
if [ ! -f "$KEY_DIR/master.key" ]; then
    openssl rand -hex 32 > "$KEY_DIR/master.key" 2>/dev/null || \
    openssl rand -hex 32 > "$FALLBACK_DIR/master.key"
    chmod 600 "$KEY_DIR/master.key" 2>/dev/null || chmod 600 "$FALLBACK_DIR/master.key"
    echo "✓ Master key created"
fi

# Killswitch key
if [ ! -f "$KEY_DIR/killswitch.key" ]; then
    openssl rand -hex 32 > "$KEY_DIR/killswitch.key" 2>/dev/null || \
    openssl rand -hex 32 > "$FALLBACK_DIR/killswitch.key"
    chmod 600 "$KEY_DIR/killswitch.key" 2>/dev/null || chmod 600 "$FALLBACK_DIR/killswitch.key"
    echo "✓ Killswitch key created"
fi

echo "✅ All keys generated successfully."