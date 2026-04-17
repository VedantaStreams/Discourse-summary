#!/bin/bash

# ─────────────────────────────────────────────────────────
#   🕉️  Suma AI Hub — Local Runner (Mac)
#   YouTube automation works locally — no cloud restrictions
# ─────────────────────────────────────────────────────────

set -e

echo ""
echo "🕉️  Suma AI Hub — Local Version"
echo "─────────────────────────────────────────────────────"

# ── Check Python ──────────────────────────────────────────
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install from https://python.org"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# ── Check ffmpeg ──────────────────────────────────────────
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install ffmpeg
fi
echo "✅ ffmpeg ready"

# ── Check yt-dlp ──────────────────────────────────────────
if ! command -v yt-dlp &> /dev/null; then
    echo "⚠️  yt-dlp not found. Installing..."
    pip3 install yt-dlp --quiet
fi
echo "✅ yt-dlp ready"

# ── Install Python packages ───────────────────────────────
echo ""
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt --quiet
echo "✅ All packages installed"

# ── Launch app ────────────────────────────────────────────
echo ""
echo "─────────────────────────────────────────────────────"
echo "🚀 Launching Suma AI Hub locally..."
echo "   Opening at: http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo "─────────────────────────────────────────────────────"
echo ""

streamlit run app.py
