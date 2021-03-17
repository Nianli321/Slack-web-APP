import pytest
from backend import utils


def test_generate_luid():
    # generate valid luid
    assert isinstance(utils.generate_luid(), int)

    # generate an invalid luid
    with pytest.raises(ValueError):
        utils.generate_luid(800)
