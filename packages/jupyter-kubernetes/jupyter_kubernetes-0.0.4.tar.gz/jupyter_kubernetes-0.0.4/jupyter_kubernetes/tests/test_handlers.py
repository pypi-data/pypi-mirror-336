import json

from ..__version__ import __version__


async def test_config(jp_fetch):
    # When
    response = await jp_fetch("jupyter_kubernetes", "config")
    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "extension": "jupyter_kubernetes",
        "version": __version__
    }
