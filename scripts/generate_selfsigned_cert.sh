#!/usr/bin/env bash
set -euo pipefail

# Generate a self-signed certificate for branchloans.com and place in nginx/ssl
OUT_DIR="$(dirname "$0")/../nginx/ssl"
mkdir -p "$OUT_DIR"

KEY_FILE="$OUT_DIR/branchloans.com.key"
CRT_FILE="$OUT_DIR/branchloans.com.crt"

# Backup existing files if present
timestamp() { date +%Y%m%d%H%M%S; }
if [[ -f "$KEY_FILE" || -f "$CRT_FILE" ]]; then
  b="backup-$(timestamp)"
  echo "Backing up existing cert files to ${OUT_DIR}/${b}-*"
  [[ -f "$KEY_FILE" ]] && mv "$KEY_FILE" "${OUT_DIR}/${b}-branchloans.com.key"
  [[ -f "$CRT_FILE" ]] && mv "$CRT_FILE" "${OUT_DIR}/${b}-branchloans.com.crt"
fi

# Generate self-signed cert (non-interactive)
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout "$KEY_FILE" \
  -out "$CRT_FILE" \
  -subj "/CN=branchloans.com"

chmod 600 "$KEY_FILE" || true
chmod 644 "$CRT_FILE" || true

echo "Generated self-signed cert: $CRT_FILE"
echo "Generated key: $KEY_FILE"

echo "You can now start nginx via docker compose. Run:"
echo "  docker compose up -d nginx"

echo "To test locally, add an /etc/hosts entry (run as sudo):"
echo "  echo '127.0.0.1 branchloans.com' | sudo tee -a /etc/hosts"
