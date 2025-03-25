from __future__ import annotations

import asyncio

import pytest


class CustomSelectorLoop(asyncio.SelectorEventLoop):
    """A subclass with no overrides, just to test for presence."""


@pytest.fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = CustomSelectorLoop()
    yield loop
    loop.close()
