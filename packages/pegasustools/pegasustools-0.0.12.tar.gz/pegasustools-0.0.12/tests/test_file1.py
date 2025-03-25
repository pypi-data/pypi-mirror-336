"""Test the contents of the file_2 module."""

import pegasustools as pt


def test_times_2() -> None:
    """Verify that pt.times_2 is correct."""
    test_var: int = 4
    assert pt.times_2(test_var) == 2 * test_var
