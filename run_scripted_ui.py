#!/usr/bin/env python3
"""
Scripted UI Runner: feeds inputs from a file to the interactive CLI.
Usage:
  CONTACT_MANAGER_INPUT_SCRIPT=path/to/script.txt python run_scripted_ui.py
or pass the path as the first argument.
"""

import os
import sys
import builtins
from input_helpers import set_input_provider, ScriptInputProvider

def enable_scripted_input(script_path: str) -> None:
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    iterator = iter(lines)
    def scripted_input(prompt: str = "") -> str:
        try:
            return next(iterator)
        except StopIteration:
            print("\n[Script completed]")
            raise SystemExit(0)
    builtins.input = scripted_input
    print(f"[Script runner] Feeding {len(lines)} lines from {script_path}")

def main():
    script_path = os.environ.get("CONTACT_MANAGER_INPUT_SCRIPT") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not script_path:
        print("❌ No input script provided. Set CONTACT_MANAGER_INPUT_SCRIPT or pass path as arg.")
        sys.exit(1)
    # Use centralized input provider so all modules read from the same script
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    set_input_provider(ScriptInputProvider(lines))
    print(f"[Script runner] Feeding {len(lines)} lines from {script_path}")
    # Also override builtins.input to catch any stray calls not using safe_get_input
    def _scripted_input(prompt: str = "") -> str:
        try:
            return lines.pop(0)
        except IndexError:
            print("\n[Script completed]")
            raise SystemExit(0)
    builtins.input = _scripted_input
    # Ensure UI isn't disabled
    os.environ.pop("CONTACT_MANAGER_DISABLE_UI", None)
    import main as app
    app.main()

if __name__ == "__main__":
    main()


