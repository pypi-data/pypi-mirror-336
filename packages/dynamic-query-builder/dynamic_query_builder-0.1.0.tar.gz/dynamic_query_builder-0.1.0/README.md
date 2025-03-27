# Dynamic Query Builder

A dynamic query builder for SQLAlchemy models with support for pagination, filtering, and sorting.

## Installation

```bash
pip install dynamic-query-builder
```

```
from dynamic_query_builder import QueryBuilder
from models import User  # Example model

# Initialize the QueryBuilder
query_builder = QueryBuilder(
    model=User,
    session=db_session,
    filters={"username": "john"},
    search_fields=["username"],
    page=1,
    page_size=10,
)

# Execute the query
results = await query_builder.execute()
```
