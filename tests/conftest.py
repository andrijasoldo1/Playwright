import pytest
import os
from dotenv import load_dotenv
from test_applicationv3 import add_adult

load_dotenv()
NUM_ADULTS = int(os.getenv("NUM_ADULTS", 1))

@pytest.fixture
def add_adults_fixture():
    def _add(page):
        for _ in range(NUM_ADULTS):
            add_adult(page)
    return _add
