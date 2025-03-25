"""
The `interactive` module will run an interactive duckdb session between the various
data resources.

Note that just importing this module, if in an IPython environment, will register the
magic `%%sql` command to your session.

SQL queries runnable in [duckdb](https://duckdb.org/docs/sql/introduction) which is
designed to closely follow the structure of Postgres Queries.

The interactive SQL session will be kept in memory at run-time *not ran on a SQL database*.
It's worthwhile therefore, to only bring in the data you need before querying it, in order
to avoid overloading your memory.

For example:

```python
from flex_dtk import interactive

interactive.register_warehouse_query(
    "big_table",
    "SELECT * FROM a_big.table",
    server,
    database,
)

df = interactive.flexsql("SELECT * FROM big_table LIMIT 10")
```

Will load *everything* from `a_big.table` into memory before filtering it, in comparison to
the below which will only load 10 items into memory to start with:

```python
from flex_dtk import interactive

interactive.register_warehouse_query(
    "small_table",
    "SELECT TOP 10 * FROM a_big.table",
    server,
    database,
)

df = interactive.flexsql("SELECT * FROM small_table")
```
"""

from datetime import datetime

try:
    import duckdb
    import pandas as pd
    from IPython.core.magic import register_cell_magic
except ImportError as exception:
    raise ImportError(
        "You may be missing required dependencies for flex_dtk's interactive module\n"
        "Hint: try installing 'flex_dtk[interactive]' rather than simply 'flex_dtk'"
    ) from exception

from flex_dtk import datalake, warehouse, trading_db

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

connection = duckdb.connect()


def flexsql(query: str) -> pd.DataFrame:
    """
    Execute a SQL query in the current session, and return the results as a
    pandas dataframe.
    """
    return connection.execute(query).fetchdf()


def register_flexsql(table: str, query: str) -> None:
    """
    Execute a SQL query in the current session, and register the result to a
    virtual table.
    """
    connection.register(table, flexsql(query))
    print(f"Result registered to {table}")


try:

    @register_cell_magic
    def sql(line, cell):  # pragma: no cover
        """
        Jupyter notebook magic implementation of lakesql function.

        Will  execute contents of cell as SQL query, if line is given,
        they'll also be registered to that line as a virtual table.
        """
        dataframe = flexsql(cell)
        if line:
            connection.register(line, dataframe)
            print(f"result registered to {line}")
        return flexsql(cell)
except NameError:
    pass


def _ensure_datetime(target: str | datetime) -> datetime:
    """
    Internal function, if target is string, will convert
    to a datetime under format "%Y-%m-%d" (or raise error)
    otherwise, will pass back target.
    """
    if isinstance(target, str):
        return datetime.strptime(target, "%Y-%m-%d")
    return target


def _registerable_name_from_path(path: str) -> str:
    """
    Internal function, decide name to register table against from path.
    """
    return path.split("/", maxsplit=2)[-1].replace("/", "_")


def register_datalake_date_range(
    path: str,
    from_date: str | datetime,
    to_date: str | datetime,
    **kwargs,
) -> None:
    """
    Read date range of datalake partitions, and register them as a
    virtual table.
    """
    from_date = _ensure_datetime(from_date)
    to_date = _ensure_datetime(to_date)
    connection.register(
        (register_name := _registerable_name_from_path(path)),
        datalake.between_dates(
            path,
            from_date=from_date,
            to_date=to_date,
            **kwargs,
        ),
    )
    print(f"Table registered to {register_name}")


def register_datalake_latest(
    path: str,
    as_of: str | datetime | None = None,
    **kwargs,
) -> None:
    """
    Read latest datalake partition, and register as a
    virtual table.
    """
    as_of = as_of if as_of is None else _ensure_datetime(as_of)
    connection.register(
        (register_name := _registerable_name_from_path(path)),
        datalake.latest(
            path,
            as_of=as_of,
            **kwargs,
        ),
    )
    print(f"Table registered to {register_name}")


def register_datalake_for_date(
    path: str,
    for_date: str | datetime,
    **kwargs,
) -> None:
    """
    Read a single datalake partition, and register as a
    virtual table.
    """
    for_date = _ensure_datetime(for_date)
    connection.register(
        (register_name := _registerable_name_from_path(path)),
        datalake.for_date(
            path=path,
            for_date=for_date,
            **kwargs,
        ),
    )
    print(f"Table registered to {register_name}")


def register_warehouse_query(
    register_name: str,
    query: str,
    server: str,
    database: str,
    **kwargs,
) -> None:
    """
    Query the warehouse and register results as an in-session virtual table.
    """
    connection.register(
        register_name,
        warehouse.query(
            query,
            server=server,
            database=database,
            **kwargs,
        ),
    )
    print(f"Table registered to {register_name}")


def register_trading_db_query(
    register_name: str,
    query: str,
    server: str,
    database: str,
    username: str,
    password: str,
    **kwargs,
) -> None:
    """
    Query the trading database and register results as an in-session virtual table
    """
    connection.register(
        register_name,
        trading_db.query(
            query,
            server=server,
            database=database,
            username=username,
            password=password,
            **kwargs,
        ),
    )
    print(f"Table registered to {register_name}")
