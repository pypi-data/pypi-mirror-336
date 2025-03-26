"""
Test bookkeeping router as a normal router
"""

import pytest

pytestmark = pytest.mark.enabled_dependencies(
    [
        "AuthSettings",
        "BookkeepingDB",
        "BookkeepingAccessPolicy",
        "DevelopmentSettings",
    ]
)


@pytest.fixture
def normal_user_client(client_factory):
    with client_factory.normal_user() as client:
        yield client


def test_bookkeeping(normal_user_client):
    r = normal_user_client.get("/api/bookkeeping")

    assert r.status_code == 200
    assert r.json() == 0
