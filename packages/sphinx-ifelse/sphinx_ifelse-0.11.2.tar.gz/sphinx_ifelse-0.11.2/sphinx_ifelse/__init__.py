"""Sphinx extension for alternating content based on configuration values."""

__version__ = "0.11.2"


def setup(app):  # type: ignore[no-untyped-def]
    from sphinx_ifelse.ifelse import setup as ifelse_setup

    return ifelse_setup(app)
