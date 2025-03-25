import pandas as pd
import pytest

from flex_dtk import warehouse


def test_query_returns_results_of_read_sql(monkeypatch) -> None:
    def some_dataframe(*args, **kwargs) -> pd.DataFrame:
        return pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})

    monkeypatch.setattr(warehouse.pd, "read_sql", some_dataframe)
    monkeypatch.setattr(warehouse, "azure_connection", lambda x, y: None)
    actual = warehouse.query("SELECT * FROM table", "server.net", "DB")
    assert set(actual.columns) == {"a", "b"}
    assert len(actual) == 3

def test_query_fails_no_variables(monkeypatch) -> None:
    def some_dataframe(*args, **kwargs) -> pd.DataFrame:
        return pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})

    monkeypatch.setattr(warehouse.pd, "read_sql", some_dataframe)
    monkeypatch.setattr(warehouse, "azure_connection", lambda x, y: None)

    with pytest.raises(ValueError):
        warehouse.query("SELECT * FROM table")