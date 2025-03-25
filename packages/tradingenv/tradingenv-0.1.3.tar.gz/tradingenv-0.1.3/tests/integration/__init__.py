import pytest
from tradingenv.contracts import AbstractContract


@pytest.fixture(autouse=True)
def set_global():
    now_before = AbstractContract.now
    AbstractContract.now = now_before
    yield  # allows us to have cleanup after the test
    AbstractContract.now = now_before  # once test is done, revert value for next test
