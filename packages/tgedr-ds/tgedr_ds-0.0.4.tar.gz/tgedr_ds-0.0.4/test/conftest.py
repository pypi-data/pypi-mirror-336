import os
import sys
import tempfile
from typing import List

import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
)  # isort:skip


def assert_frames_are_equal(
    actual: DataFrame,
    expected: DataFrame,
    sort_columns: List[str],
    abs_tol: float = None,
):
    results_sorted = actual.sort_values(by=sort_columns).reset_index(drop=True)
    expected_sorted = expected.sort_values(by=sort_columns).reset_index(drop=True)
    if abs_tol is not None:
        assert_frame_equal(
            results_sorted,
            expected_sorted,
            check_dtype=False,
            check_exact=False,
            check_like=True,
            atol=abs_tol,
        )
    else:
        assert_frame_equal(
            results_sorted,
            expected_sorted,
            check_dtype=False,
            check_exact=False,
            check_like=True,
        )


@pytest.fixture(scope="session")
def resources_folder() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))


@pytest.fixture(scope="session")
def temporary_folder() -> str:
    _folder = tempfile.TemporaryDirectory("+wb").name
    if not os.path.exists(_folder):
        os.makedirs(_folder)
    return _folder
