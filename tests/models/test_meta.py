from cipher.models import Meta


def test_meta():
    meta = Meta()

    meta.a = 1
    meta["b"] = 2

    assert meta.to_dict() == {"a": 1, "b": 2}
    assert meta["a"] == 1
    assert meta.b == 2
