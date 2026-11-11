"""hashDataRetrieve must find the right revision entry for every DSA name."""
import pytest

import Main


@pytest.mark.parametrize("name", Main.DSAs_array)
def test_hash_retrieve_returns_entry_for_name(name):
    entry = Main.hashDataRetrieve(name)
    assert entry["name"] == name
    for field in ("id", "categories", "types", "description", "content", "file"):
        assert field in entry, f"{name} entry is missing {field!r}"


def test_every_name_in_database_is_a_known_dsa():
    import ast

    names = [
        ast.literal_eval(line.rstrip("\n"))["name"]
        for line in Main.database_list
        if line.strip()
    ]
    assert sorted(names) == sorted(Main.DSAs_array)
