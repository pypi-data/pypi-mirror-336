# DB Delta

`db-delta` is a Python testing utility package designed to be used alongside `moto` that evaluates and validates database changesets in test that executes AWS DynamoDB operations to ensure that only the changes that you defined are executed against your database, no more and no less.

Usage is simple.

#### Step 1: Define a changeset in JSON format:

```json
[
    {
        "action": "update_item",
        "key":{
            "PK": "FOO",
            "SK": "BAR"
        },
        "updated_fields": [
            {
                "field": "bar",
                "update_type": "updated",
                "new_value": "bar-foo"
            },
            {
                "field": "foo",
                "update_type": "removed",
            }
        ]
    }
]
```

#### Step 2: Execute test function with `validate_dynamodb_changeset`

```python

from db_delta import ChangeSet, validate_dynamodb_changeset

def test_function_foo(table):

    expected_changeset = ChangeSet.from_json("path_to_changeset.json")

    with validate_dynamodb_changeset(table, expected_changeset):
        # call your function that modifies the contents of your database.
        # db_delta will ensure that only the changes specified are executed.
        execute_function(table, "foo", "bar")
```

`db_delta` will scan your DynamoDB table before and after the execution of your code. It will then verify that only the changes defined in the changeset have been executed. If any of the specified changes are not found, or if any changes have been made that are not defined in the changeset, an `AssertionException` is raised.

### Why use `db_delta`?

Writing exhaustive unittests to test database operations is, well, exhausting. Unittests end up being either incomplete, or extremely verbose and repetitive. `db_delta` not ony makes tests far more readable, it also makes them far more robust. If any change is made to any item in your database that has not been defined in the changeset, your tests will fail. No exceptions and no surprises.

Consider the following example code.

```python

def example_function(table, new_name: str):
    table.update_item(
        Key={
            "PK": "FOO",
            "SK": "BAR",
        },
        UpdateExpression="SET #name = :name",
        ExpressionAttributeNames={
            "#name": "name",
        },
        ExpressionAttributeValues={
            ":name": new_name,
        },
    )
```

A typical unittest would look like the following.

```python

def test_example_function(table):

    item = table.get_item(
        Key={
            "PK": "FOO",
            "SK": "BAR",
        },
    )["Item"]
    assert item["name"] == "name"

    example_function(table, "name V2")

    item = table.get_item(
        Key={
            "PK": "FOO",
            "SK": "BAR",
        },
    )["Item"]
    assert item["name"] == "name V2"
```

There are two issues with the above.

1. Tests like the above quickly become extremely repetitive, with a great deal of duplicated code to read from your database and compare values.
2. The test only checks if one field in one item has been updated as expected. Every other item from the database could have been deleted and the test would still pass.

The second point is critical and can lead to serious issues in your data. While the above example is trivial, real life codebases generally have more complex functions that execute multiple database operations in multiple places, and it quickly becomes difficult to test everything without writing long unittests that check for every possible outcome.

This is where `db_delta` comes in. Because it scans your table before and after the function you are testing is executed, it generates a complete picture of the changes made to your database as the result of running the code you are testing. It can then compare the initial and final state of your table to make sure that only the changes you expect have actually been executed.

It also neatens up the code. With `db_delta`, the above test now becomes

```python

def test_example_function(table):

    expected_changeset = ChangeSet(
        changes=[
            {
                "action": "update_item",
                "key": {
                    "PK": "FOO",
                    "SK": "BAR",
                },
                "updated_fields": [
                    {
                        "field": "name",
                        "update_type": "updated",
                        "new_value": "name V2"
                    }
                ]
            }
        ]
    )

    with validate_dynamodb_changeset(table, expected_changeset):
        example_function(table, "name V2")

```

The test no longer contains any logic to retrieve and validate changes from your database. Additionally, if any other changes are made other than the specified update, `validate_dynamodb_changeset` will raise an exception and the test will fail.


### Installation

`db_delta` is available on `PyPi` and can be installed using

```bash
$ pip install db-delta
```

Alternatively, you can clone the repo and install the package manually with

```bash
$ pip install .
```

### Usage

The only two components required to use `db_delta` is the `ChangeSet` object and the `validate_dynamodb_changeset` function.

#### `ChangeSet` Object

The `ChangeSet` object is a `pydantic` data model that contains the database changes that you expect your function to produce. There are three types of changes that you can provide in a changeset.

* `PutItem` - represents a new item created using `dynamodb:PutItem`.
* `UpdatedItem` - represents an update to an existing item using `dynamodb:UpdateItem`.
* `DeletedItem`- represents an item deleted using `dynamodb:DeleteItem`.

Expected updates are provided as an array of objects collectively referred to as a changeset. Each update type has its own format, and the structure of each is documented below.

<details>
<summary>

##### `PutItem`
</summary>

`PutItem` represents a new item in your database. When a changeset contains a `PutItem` update, `db_delta` will check that the item did not exist in the initial table state, but does exist in the final state, and that the created item matches the expected structure. The JSON structure for a `PutItem` update is given below.

```json
{
    "action": "put_item",
    "key": {
        "foo": "bar",
        "bar": "foo"
    },
    "item": {
        "foo": "bar",
        "bar": "foo",
        "id": 1,
        "description": "An example"
    }
}
```
</details>

<details>
<summary>

##### `UpdatedItem`
</summary>


`UpdatedItem` represents an item in your database that has been updated. When a changeset contains a `UpdatedItem` update, `db_delta` will check that the item exists in both the initial table state and in the final state, and that the changes made to the item match the changes defined in the changeset. The JSON structure for an `UpdatedItem` update is given below.

```json
{
    "action": "updated_item",
    "key": {
        "foo": "bar",
        "bar": "foo"
    },
    "updated_fields": [
        {
            "field": "newField",
            "update_type": "added",
            "new_value": "bar-foo"
        },
        {
            "field": "updatedField",
            "update_type": "updated",
            "new_value": "bar-foo"
        },
        {
            "field": "removedField",
            "update_type": "removed",
        }
    ]
}
```

All expected updates to the item must be defined in the `updated_fields` column, where each update has the following structure

```json
{
    "field": "String",
    "update_type": "added|updated|removed",
    "new_value": "String | Integer | Float | Object"
}
```

The `field` parameter specifies the field of the item that is being updated, while the `update_type` parameter indicates what type of change is expected.
</details>
<details>
<summary>

##### `DeletedItem`
</summary>

`DeletedItem` represents an item that has been deleted from your database. When a changeset contains a `DeletedItem` update, `db_delta` will check that the item exists in the initial table state, but does not exist in the final state.

```json
{
    "action": "deleted_item",
    "key": {
        "foo": "bar",
        "bar": "foo"
    },
}
```
</details>


##### Generating `ChangeSet` instance

A `ChangeSet` instance can be generated one of two ways. Either define your changeset in code

```python
expected_changeset = ChangeSet(
    changes=[
        {
            "action": "update_item",
            "key": {
                "PK": "FOO",
                "SK": "BAR",
            },
            "updated_fields": [
                {
                    "field": "name",
                    "update_type": "updated",
                    "new_value": "name V2"
                }
            ]
        }
    ]
)
```

or define your changeset in a JSON file and use the `from_json` class method

```python
expected_changeset = ChangeSet.from_json("path_to_changeset.json")
```

#### `validate_dynamodb_changeset` Function

Once you have a `ChangeSet` instance constructed with your expected changes, simply execute your function in the `validate_dynamodb_changeset` context manager.

```python
from db_delta import ChangeSet, validate_dynamodb_changeset


def test_function_foo(table):

    expected_changeset = ChangeSet.from_json("path_to_changeset.json")

    with validate_dynamodb_changeset(table, expected_changeset):
        # call your function that modifies the contents of your database.
        # db_delta will ensure that only the changes specified are executed.
        execute_function(table, "foo", "bar")
```

If `execute_function` results in any changes that are not defined in the changeset, `validate_dynamodb_changeset` will raise an `AssertionException`.

Note that the `validate_dynamodb_changeset` requires both a configured DynamoDB table resource as well as the expected changeset. The table resource should be created using `boto3`.

```python
table = boto3.resource("dynamodb").Table("example-table")
```

### Test Setup

In order to get the most out of `db_delta` its critical that you set up your unittests correctly. `db_delta` is designed to be used alongside `moto` and `pytest`. We strongly recommend that you get familiar with both before integration `db_delta` into your unittests. For a complete example, see the `examples/basic` folder in this repository, which shows you how to configure a basic testing environment with the required tools.


### Advanced Usage

`validate_dynamodb_changeset` accepts an optional formatting function is called on all items before making comparisons. This is especially useful if your code adds certain metadata fields such as created and update timestamps that you want to exclude from any comparisons. For example:

```python

def strip_metadata(row: Dict) -> Dict:
    for key in ["createdTs", "updatedTs"]:
        row.pop(key)
    return row


def test_function_foo(table):

    expected_changeset = ChangeSet.from_json("path_to_changeset.json")

    with validate_dynamodb_changeset(table, expected_changeset, formatter=strip_metadata):
        # call your function that modifies the contents of your database.
        # db_delta will ensure that only the changes specified are executed.
        execute_function(table, "foo", "bar")
```

The `strip_metadata` function is called on all items before any comparisons are made. In this case, both the `createdTs` and `updatedTs` timestamps are removed from any items, ensuring that your changesets do not need to include the updated values for mocked timestamps. This can help to keep the changesets compact.
