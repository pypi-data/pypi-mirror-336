from decimal import Decimal

import pytest

from src.db_delta.validate import (
    validate_dynamodb_changeset,
    get_key_fields_from_table,
    hash_key,
)
from src.db_delta.models import ChangeSet


def test_validate_dynamodb_changeset_put_item(mock_dynamo_table):

    changeset = ChangeSet(
        changes=[
            {
                "action": "put_item",
                "key": {
                    "PK": "ITEM_ID#6",
                    "SK": "ITEM#6",
                },
                "item": {
                    "PK": "ITEM_ID#6",
                    "SK": "ITEM#6",
                    "id": Decimal(4),
                    "name": "Test 4",
                    "description": "Description 4",
                },
            },
        ],
    )

    with validate_dynamodb_changeset(mock_dynamo_table, changeset):
        mock_dynamo_table.put_item(
            Item={
                "PK": "ITEM_ID#6",
                "SK": "ITEM#6",
                "id": 4,
                "name": "Test 4",
                "description": "Description 4",
            }
        )


def test_validate_dynamodb_changeset_put_item_failed(mock_dynamo_table):

    changeset = ChangeSet(
        changes=[
            {
                "action": "put_item",
                "key": {
                    "PK": "ITEM_ID#6",
                    "SK": "ITEM#6",
                },
                "item": {
                    "PK": "ITEM_ID#6",
                    "SK": "ITEM#6",
                    "id": Decimal(4),
                    "name": "Test 4",
                    "description": "Description 4",
                },
            },
        ],
    )

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.put_item(
                Item={
                    "PK": "ITEM_ID#7",
                    "SK": "ITEM#7",
                    "id": 4,
                    "name": "Test 4",
                    "description": "Description 4",
                }
            )

    expected_error = """New item {'PK': 'ITEM_ID#7', 'SK': 'ITEM#7'} found in updated
 table, but not in expected changeset."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_validate_dynamodb_changeset_updated_item(mock_dynamo_table):

    changeset = ChangeSet(
        changes=[
            {
                "action": "update_item",
                "key": {
                    "PK": "ITEM_ID#1",
                    "SK": "ITEM#1",
                },
                "updated_fields": [
                    {
                        "field": "name",
                        "update_type": "updated",
                        "old_value": "Item 1",
                        "new_value": "Item 1 Updated",
                    },
                    {
                        "field": "description",
                        "update_type": "removed",
                    },
                ],
            },
        ],
    )

    with validate_dynamodb_changeset(mock_dynamo_table, changeset):
        mock_dynamo_table.update_item(
            Key={
                "PK": "ITEM_ID#1",
                "SK": "ITEM#1",
            },
            UpdateExpression="SET #name = :name, REMOVE description",
            ExpressionAttributeNames={"#name": "name"},
            ExpressionAttributeValues={":name": "Item 1 Updated"},
        )


def test_validate_dynamodb_changeset_updated_item_failed(mock_dynamo_table):

    changeset = ChangeSet(
        changes=[
            {
                "action": "update_item",
                "key": {
                    "PK": "ITEM_ID#1",
                    "SK": "ITEM#1",
                },
                "updated_fields": [
                    {
                        "field": "name",
                        "update_type": "updated",
                        "old_value": "Item 1",
                        "new_value": "Item 1 Updated",
                    },
                    {
                        "field": "description",
                        "update_type": "removed",
                    },
                ],
            },
        ],
    )

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.update_item(
                Key={
                    "PK": "ITEM_ID#2",
                    "SK": "ITEM#2",
                },
                UpdateExpression="SET #name = :name, REMOVE description",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":name": "Item 1 Updated"},
            )

    expected_error = """Item {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2'} found in updated table,
 but has been modified. Expected: {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2', 'name': 'Item 2',
 'description': 'Description of item 2', 'price': Decimal('200')}, Actual: {'PK':
 'ITEM_ID#2', 'SK': 'ITEM#2', 'name': 'Item 1 Updated', 'price': Decimal('200')}."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_validate_dynamodb_changeset_deleted_item(mock_dynamo_table):

    changeset = ChangeSet(
        changes=[
            {
                "action": "delete_item",
                "key": {
                    "PK": "ITEM_ID#1",
                    "SK": "ITEM#1",
                },
            },
        ],
    )

    with validate_dynamodb_changeset(mock_dynamo_table, changeset):
        mock_dynamo_table.delete_item(
            Key={
                "PK": "ITEM_ID#1",
                "SK": "ITEM#1",
            },
        )


def test_validate_dynamodb_changeset_deleted_item_failed(mock_dynamo_table):

    changeset = ChangeSet(
        changes=[
            {
                "action": "delete_item",
                "key": {
                    "PK": "ITEM_ID#1",
                    "SK": "ITEM#1",
                },
            },
        ],
    )

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.delete_item(
                Key={
                    "PK": "ITEM_ID#2",
                    "SK": "ITEM#2",
                },
            )

    expected_error = """Expected key {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2'} not found in
 updated table."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_validate_changeset(mock_dynamo_table):

    changeset = ChangeSet.from_json("tests/data/sample_changeset.json")

    with validate_dynamodb_changeset(mock_dynamo_table, changeset):
        mock_dynamo_table.put_item(
            Item={
                "PK": "ITEM_ID#6",
                "SK": "ITEM#6",
                "id": 4,
                "name": "Test 4",
                "description": "Description 4",
            }
        )

        mock_dynamo_table.update_item(
            Key={
                "PK": "ITEM_ID#2",
                "SK": "ITEM#2",
            },
            UpdateExpression="SET #name = :name, REMOVE description",
            ExpressionAttributeNames={"#name": "name"},
            ExpressionAttributeValues={":name": "Test 2 Updated"},
        )

        mock_dynamo_table.delete_item(
            Key={
                "PK": "ITEM_ID#3",
                "SK": "ITEM#3",
            },
        )


def test_validate_changeset_failed_put(mock_dynamo_table):

    changeset = ChangeSet.from_json("tests/data/sample_changeset.json")

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):

            mock_dynamo_table.update_item(
                Key={
                    "PK": "ITEM_ID#2",
                    "SK": "ITEM#2",
                },
                UpdateExpression="SET #name = :name, REMOVE description",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":name": "Test 2 Updated"},
            )

            mock_dynamo_table.delete_item(
                Key={
                    "PK": "ITEM_ID#3",
                    "SK": "ITEM#3",
                },
            )

    expected_error = """NewItem validation: Key {'PK': 'ITEM_ID#6', 'SK': 'ITEM#6'} not
 found in updated table."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_validate_changeset_failed_update(mock_dynamo_table):

    changeset = ChangeSet.from_json("tests/data/sample_changeset.json")

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.put_item(
                Item={
                    "PK": "ITEM_ID#6",
                    "SK": "ITEM#6",
                    "id": 4,
                    "name": "Test 4",
                    "description": "Description 4",
                }
            )

            mock_dynamo_table.delete_item(
                Key={
                    "PK": "ITEM_ID#3",
                    "SK": "ITEM#3",
                },
            )

    expected_error = """UpdateItem validation: Field 'name' for key {'PK': 'ITEM_ID#2',
 'SK': 'ITEM#2'} has been updated, but does not match expected value. Expected 'Test 2
 Updated', got 'Item 2'."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_validate_changeset_failed_delete(mock_dynamo_table):

    changeset = ChangeSet.from_json("tests/data/sample_changeset.json")

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.put_item(
                Item={
                    "PK": "ITEM_ID#6",
                    "SK": "ITEM#6",
                    "id": 4,
                    "name": "Test 4",
                    "description": "Description 4",
                }
            )

            mock_dynamo_table.update_item(
                Key={
                    "PK": "ITEM_ID#2",
                    "SK": "ITEM#2",
                },
                UpdateExpression="SET #name = :name, REMOVE description",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":name": "Test 2 Updated"},
            )

    expected_error = """DeletedItem validation: Key {'PK': 'ITEM_ID#3', 'SK': 'ITEM#3'}
 found in updated table."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_empty_changeset_inserted(mock_dynamo_table):

    changeset = ChangeSet(changes=[])

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.put_item(
                Item={
                    "PK": "ITEM_ID#7",
                    "SK": "ITEM#7",
                    "id": 7,
                    "name": "Item 7",
                    "description": "Description of item 7",
                    "price": Decimal(200),
                }
            )

    expected_error = """New item {'PK': 'ITEM_ID#7', 'SK': 'ITEM#7'} found in updated
 table, but not in expected changeset."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_empty_changeset_updated(mock_dynamo_table):

    changeset = ChangeSet(changes=[])

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.update_item(
                Key={
                    "PK": "ITEM_ID#2",
                    "SK": "ITEM#2",
                },
                UpdateExpression="SET #name = :name",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":name": "Test 2 Updated"},
            )

    expected_error = """Item {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2'} found in updated
 table, but has been modified. Expected: {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2', 'name':
 'Item 2', 'description': 'Description of item 2', 'price': Decimal('200')}, Actual:
 {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2', 'name': 'Test 2 Updated', 'description':
 'Description of item 2', 'price': Decimal('200')}."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_empty_changeset_deleted(mock_dynamo_table):

    changeset = ChangeSet(changes=[])

    with pytest.raises(AssertionError) as exc:
        with validate_dynamodb_changeset(mock_dynamo_table, changeset):
            mock_dynamo_table.delete_item(
                Key={
                    "PK": "ITEM_ID#2",
                    "SK": "ITEM#2",
                },
            )

    expected_error = """Expected key {'PK': 'ITEM_ID#2', 'SK': 'ITEM#2'} not found in
 updated table."""

    assert str(exc.value) == expected_error.replace("\n", "")


def test_hash_key():

    key = {
        "PK": "ITEM_ID#1",
        "SK": "ITEM#1",
    }
    assert hash_key(key) == "f5dcbd5ee3a947823383b36d60e80ed5"


def test_get_key_fields_from_table(mock_dynamo_table):

    pk, sk = get_key_fields_from_table(mock_dynamo_table)
    assert pk == "PK"
    assert sk == "SK"
