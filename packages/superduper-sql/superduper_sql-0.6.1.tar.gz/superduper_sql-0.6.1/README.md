<!-- Auto-generated content start -->
# superduper_sql

superduper-sql is a plugin for SQL databackends that allows you to use these backends with superduper.


Superduper supports SQL databases via the ibis project. With superduper, queries may be built which conform to the ibis API, with additional support for complex data-types and vector-searches.


## Installation

```bash
pip install superduper_sql
```

## API


- [Code](https://github.com/superduper-io/superduper/tree/main/plugins/ibis)
- [API-docs](/docs/api/plugins/superduper_ibis)

| Class | Description |
|---|---|
| `superduper_sql.data_backend.SQLDataBackend` | sql data backend for the database. |


<!-- Auto-generated content end -->

<!-- Add your additional content below -->

## Connection examples

### MySQL

```python
from superduper import superduper

db = superduper('mysql://<mysql-uri>')
```

### Postgres

```python
from superduper import superduper

db = superduper('postgres://<postgres-uri>')
```

### Other databases

```python

from superduper import superduper

db = superduper('<database-uri>')
```

## Query examples

### Inserting data

Table data must correspond to the `Schema` for that table.
Either [create a `Schema` and `Table`](../execute_api/data_encodings_and_schemas.md#create-a-table-with-a-schema)
or use [an auto-detected `Schema`](../execute_api/auto_data_types.md). Once you've 
got a `Schema`, all data inserted must conform to that `Schema`:

```python
import pandas

pandas.DataFrame([
    PIL.Image.open('image.jpg'), 'some text', 4,
    PIL.Image.open('other_image.jpg'), 'some other text', 3,
])

t.insert(dataframe.to_dict(orient='records'))
```

### Selecting data

`superduper` supports selecting data via the `ibis` query API.
For example:

```python
db['my_table'].filter(t.rating > 3).limit(5).select(t.image).execute()
```

### Vector-search

Vector-searches are supported via the `like` operator:

```python
(
    db['my_table']
    .like({'text': 'something like this'}, vector_index='my-index')
    .filter(t.rating > 3)
    .limit(5)
    .select(t.image, t.id)
).execute()
```

Vector-searches are either first or last in a chain of operations:

```python
(
    db['my_table']
    t.filter(t.rating > 3)
    .limit(5)
    .select(t.image, t.id)
    .like({'text': 'something like this'}, vector_index='my-index')
).execute()
```

### Updating data

Updates are not covered for `superduper` SQL integrations.

### Deleting data

```python
db.databackend.drop_table('my-table')
```
