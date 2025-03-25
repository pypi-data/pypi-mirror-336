from datetime import datetime

import pandas as pd

from flex_dtk import datalake


class DummyFileSystem:
    def __init__(*args, **kwargs) -> None: ...

    def clear_instance_cache(*args, **kwargs) -> None: ...

    def ls(*args, **kwargs) -> list[str]:
        return ["file/2024", "file/2022"]

    def glob(self, *args, **kwargs) -> list[str]:
        return self.ls()


def return_args(*args, **kwargs) -> dict:
    return {
        "args": args,
        "kwargs": kwargs,
    }


def test_data_functions_call_dataframe_from_files_with_expected_arguments(
    monkeypatch,
) -> None:
    monkeypatch.setattr(datalake.fsspec, "filesystem", DummyFileSystem)
    monkeypatch.setattr(
        datalake, "_latest_partition_folder", lambda x, y: "cool/folder"
    )
    monkeypatch.setattr(datalake, "_dataframe_from_files", return_args)
    actual = datalake.latest("some/file/somewhere/or/other")
    for to_call, kwargs in [
        (datalake.latest, {"path": "some/file/somewhere/or/other"}),
        (
            datalake.between_dates,
            {
                "path": "some/file/somewhere/or/other",
                "from_date": datetime(2023, 2, 2),
                "to_date": datetime(2023, 4, 5),
            },
        ),
        (
            datalake.for_dates,
            {
                "path": "some/file/somewhere/or/other",
                "dates": [datetime(2023, 4, 1), datetime(2024, 2, 3)],
            },
        ),
        (
            datalake.for_date,
            {
                "path": "some/file/somewhere/or/other",
                "target_date": datetime(2024, 2, 3),
            },
        ),
    ]:
        actual = to_call(**kwargs)
        assert actual["kwargs"]["storage_options"] == {
            "account_name": "some",
            "anon": False,
            "use_listings_cache": False,
        }
        assert set(actual["args"][0]) == {
            "file/2024",
            "file/2022",
        }


def test_latest_partition_folder_returns_expected(monkeypatch) -> None:
    monkeypatch.setattr(datalake.fsspec, "filesystem", DummyFileSystem)
    actual = datalake._latest_partition_folder(
        "some/really/cool/path/2023", datetime(2024, 3, 1)
    )
    assert actual == "file/2024"


def test_all_files_in_path_returns_expected(monkeypatch) -> None:
    actual = datalake._all_files_in_path(
        "cool/path",
        DummyFileSystem(),
    )
    assert set(actual) == {"file/2024", "file/2022"}


def test_dataframe_from_files_concatenates_job_results(monkeypatch) -> None:
    def dummy_file(*args, **kwargs) -> pd.DataFrame:
        return pd.DataFrame({"a": [1, 2], "b": [1, 2]})

    actual = datalake._dataframe_from_files(
        ["one", "two", "three"], {}, input_operation=dummy_file
    )
    assert set(actual.columns) == {"a", "b"}
    assert len(actual) == 6
