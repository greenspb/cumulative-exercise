"""These are unit tests for main.py"""

import main


def test_root():
    assert main.root() == {"message": "Hello World"}


def test_convert():
    assert main.convert("PA", "Pittsburgh") == {"lat": "40.4416941", "long": "-79.9900861"}
