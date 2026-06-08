import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def _make_test_png(r: int, g: int, b: int, alpha: int = 180) -> str:
    arr = np.zeros((100, 100, 4), dtype=np.uint8)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b
    arr[:, :, 3] = alpha
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img = Image.fromarray(arr, "RGBA")
    img.save(tmp.name)
    img.close()
    return tmp.name


@pytest.fixture(scope="function")
def test_ndvi_png() -> str:
    path = _make_test_png(50, 200, 80)
    yield path
    os.unlink(path)


@pytest.fixture(scope="function")
def test_stressed_ndvi_png() -> str:
    path = _make_test_png(220, 60, 60)
    yield path
    os.unlink(path)


@pytest.fixture(scope="function")
def test_empty_ndvi_png() -> str:
    path = _make_test_png(0, 0, 0, alpha=0)
    yield path
    os.unlink(path)
