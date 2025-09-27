"""
Input Helpers - centralizes input handling for interactive and scripted modes.
"""

import os
import builtins

# Module-level scripted input support: reads lines from CONTACT_MANAGER_INPUT_SCRIPT if set
_SCRIPT_LINES = None
_SCRIPT_ITER = None
_PROVIDER = None


class InputProvider:
    """Interface for input providers."""
    def get(self, prompt: str = "") -> str:  # pragma: no cover - interface
        return builtins.input(prompt)


class ScriptInputProvider(InputProvider):
    def __init__(self, lines):
        self._iter = iter(lines or [])
    def get(self, prompt: str = "") -> str:
        try:
            return next(self._iter)
        except StopIteration:
            print("\n[Script completed]")
            raise SystemExit(0)


def set_input_provider(provider: InputProvider) -> None:
    global _PROVIDER
    _PROVIDER = provider

def _init_script_if_needed():
    global _SCRIPT_LINES, _SCRIPT_ITER
    if _SCRIPT_LINES is not None:
        return
    script_path = os.environ.get("CONTACT_MANAGER_INPUT_SCRIPT")
    if not script_path:
        _SCRIPT_LINES = []
        _SCRIPT_ITER = iter(_SCRIPT_LINES)
        return
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            _SCRIPT_LINES = [line.rstrip('\n') for line in f]
        _SCRIPT_ITER = iter(_SCRIPT_LINES)
        print(f"[InputHelpers] Script mode enabled with {_SCRIPT_LINES.__len__()} lines from {script_path}")
    except Exception as e:
        _SCRIPT_LINES = []
        _SCRIPT_ITER = iter(_SCRIPT_LINES)
        print(f"[InputHelpers] Failed to load script '{script_path}': {e}")


def safe_get_input(prompt: str = "") -> str:
    """Get input from either a script (if configured) or interactively.

    Raises SystemExit when input stream/script is exhausted to avoid infinite loops.
    """
    if _PROVIDER is not None:
        return _PROVIDER.get(prompt)
    _init_script_if_needed()
    if _SCRIPT_LINES:
        try:
            return next(_SCRIPT_ITER)
        except StopIteration:
            print("\n[Script completed]")
            raise SystemExit(0)
    try:
        return builtins.input(prompt)
    except EOFError:
        print("\n[No more input available – exiting]")
        raise SystemExit(0)


