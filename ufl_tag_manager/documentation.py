#!/usr/bin/env python3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
PDF  = BASE / "assets/Tagging website Documentation.pdf"

try:
    data = PDF.read_bytes()
    print("Content-Type: application/pdf")
    print('Content-Disposition: inline; filename="Tagging website Documentation.pdf"')
    print(f"Content-Length: {len(data)}")
    print()
    sys.stdout.buffer.write(data)
except Exception as e:
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(f"Cannot read PDF: {e}\nTried: {PDF}\nExists? {PDF.exists()}")
