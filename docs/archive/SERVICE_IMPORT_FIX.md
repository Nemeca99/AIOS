# Blackwall Service Import Fix: Final State

## Only One Copy in core/

- All service modules (`llm_service.py`, `error_handler.py`, etc.) now exist only in `/core/`.
- All code and tests should import from `core` only.
- There are no symlinks, wrappers, or file copies in `/lexicon/`.

## How to Import

- `from core.llm_service import LLMService`
- `from core.error_handler import error_handler`

## Why?
- **Simplicity**: No confusion, no sync issues, no import errors.
- **Maintainability**: Only one file to update.
- **Pythonic**: This is the standard, recommended approach.

## Migration Notes
- Update any old code that imports from `lexicon.llm_service` or `lexicon.error_handler` to import from `core` instead.
- Remove any old symlink/copy setup scripts—they are no longer needed.

## This is now the official and supported structure for Blackwall.
