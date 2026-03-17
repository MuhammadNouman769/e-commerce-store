from __future__ import annotations

from typing import Any, Callable

from django.http import HttpRequest


def _empty_context(_: HttpRequest) -> dict[str, Any]:
    return {}


def __getattr__(name: str) -> Callable[[HttpRequest], dict[str, Any]]:
    """
    Safety net for misconfigured/renamed context processors.

    If settings reference `apps.products.context_processors.<something>`, we return
    an empty context processor instead of raising ImportError.
    """
    return _empty_context

