from pathlib import Path
import pytest
from cjio.cityjson import reader

@pytest.fixture(scope='function')
def data_dir():
    tests_dir = Path(__file__).resolve().parent
    yield tests_dir / "data"


@pytest.fixture(scope='function')
def tmp_dir(data_dir):
    yield data_dir / "tmp"


@pytest.fixture(scope="function")
def input_model_5910_path(data_dir):
    """3D BAG tile 5910 subset"""
    yield data_dir / "3dbag_v210908_fd2cee53_5910_subset.json"

@pytest.fixture(scope="function")
def input_model_5910(data_dir):
    """3D BAG tile 5910 subset"""
    with (data_dir / "3dbag_v210908_fd2cee53_5910_subset.json").open("r") as fo:
        return reader(file=fo)
