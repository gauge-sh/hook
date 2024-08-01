# core.py
from __future__ import annotations


class PublicAPI:
    def get(self) -> str:
        return "public"


class _PrivateAPI:
    def get(self) -> str:
        return "shhh"


__all__ = ["PublicAPI"]
