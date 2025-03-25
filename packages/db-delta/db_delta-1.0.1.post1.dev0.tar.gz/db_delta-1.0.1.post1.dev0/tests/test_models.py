from src.db_delta.models import ChangeSet, UpdatedItem, PutItem, DeletedItem


def test_update_item_validation():
    pass


def test_update_item_validation_failed():
    pass


def test_change_set_from_json():

    changeset = ChangeSet.from_json("tests/data/sample_changeset.json")
    assert len(changeset.changes) == 3
    assert [type(change) for change in changeset.changes] == [
        PutItem,
        UpdatedItem,
        DeletedItem,
    ]
