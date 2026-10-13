"""Launch the feature-complete Elysia desktop pet application."""

from __future__ import annotations

import sys

from pet.app import main as pet_main


if __name__ == "__main__":
    raise SystemExit(pet_main(sys.argv))
