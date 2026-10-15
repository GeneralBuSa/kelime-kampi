#!/bin/sh
# macOS / Linux: ./baslat.sh  ->  http://localhost:8765
cd "$(dirname "$0")" || exit 1
URL=http://localhost:8765
echo "Kelime Kampı başlatılıyor: $URL (kapatmak için Ctrl+C)"
( sleep 1; if command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"; else open "$URL"; fi ) >/dev/null 2>&1 &
python3 -m http.server 8765 --bind 127.0.0.1
