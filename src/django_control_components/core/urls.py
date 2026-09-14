"""Browser-navigation URL validation shared by links and clickable rows."""

from __future__ import annotations

from urllib.parse import urlsplit

_NAVIGATION_SCHEMES = {"http", "https", "mailto", "tel"}


def safe_navigation_url(value: object) -> str:
    """Return a browser-safe navigation URL, or ``""`` for an unsafe scheme.

    Relative paths, anchors, and query strings stay valid. Control characters
    are rejected before parsing so a browser cannot normalize an obfuscated
    script scheme after server-side validation.
    """
    url = str(value or "").strip()
    if any(ord(char) < 32 or ord(char) == 127 for char in url):
        return ""
    try:
        scheme = urlsplit(url).scheme.lower()
    except ValueError:
        return ""
    if scheme and scheme not in _NAVIGATION_SCHEMES:
        return ""
    return url
