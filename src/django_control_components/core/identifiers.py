"""DOM id sanitising.

Templates interpolate component ids into Alpine *expression* contexts
(``x-data="dccChart('{{ payload_id }}')"``), where HTML escaping does not
protect: the parser decodes ``&#x27;`` back to ``'`` before Alpine reads the
attribute. Escaping is a string-context defence, so an id reaching an
expression context has to be safe pre-escape.
"""

from __future__ import annotations

import re

_UNSAFE_ID_CHARS = re.compile(r"[^A-Za-z0-9_-]+")


def slug_id(value: object, fallback: str) -> str:
    """Coerce a caller- or spec-supplied DOM id to ``[A-Za-z0-9_-]+``.

    Returns ``fallback`` when nothing survives the strip, so a purely
    punctuation id still yields a usable element id.
    """
    cleaned = _UNSAFE_ID_CHARS.sub("", str(value)) if value else ""
    return cleaned or fallback
