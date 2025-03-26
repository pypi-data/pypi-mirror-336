import os
import json
import pandas as pd
import pandas.testing as pdt
from unittest.mock import patch
from notion2pandas import Notion2PandasClient


def load_mock_data_simplest_read_table():
    with open("tests/mock_data/NOTION_SIMPLEST_READ_TABLE.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_mock_data_empty_db_columns():
    with open("tests/mock_data/NOTION_EMPTY_DB_COLUMNS.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_mock_data_empty_read_table():
    return []


@patch.object(Notion2PandasClient, "_notion_executor")
def test_from_notion_db_to_dataframe_simplest_table(mock_executor):
    n2p = Notion2PandasClient(auth="fake_token")

    mock_executor.return_value = load_mock_data_simplest_read_table()

    df_mock = n2p.from_notion_DB_to_dataframe(
        database_id=os.environ["NOTION_SIMPLEST_READ_TABLE"]
    )

    df_pkl = pd.read_pickle("tests/mock_data/NOTION_SIMPLEST_READ_TABLE.pkl")

    pdt.assert_frame_equal(df_mock, df_pkl)


@patch.object(Notion2PandasClient, "_Notion2PandasClient__get_database_columns_and_types")
@patch.object(Notion2PandasClient, "_notion_executor")
def test_from_notion_db_to_dataframe_empty_table(mock_executor, mock_columns_and_types):
    expected_columns = {'Test table 1', 'Checkbox', 'Text', 'Last edited time', 'Tags',
                        'Files & media', '👾 Digital Memories', 'Created time', 'Test table',
                        'Rollup Date Range', 'Rollup', 'ID', 'Number', 'Person', 'Last edited by',
                        'Multi-select', 'Formula', 'Rollup Counter', 'Created by', 'URL', 'Status',
                        'Date With End', 'Date', 'Name', 'PageID', 'Row_Hash'}
    n2p = Notion2PandasClient(auth="fake_token")

    mock_executor.return_value = load_mock_data_empty_read_table()
    mock_columns_and_types.return_value = load_mock_data_empty_db_columns()

    df_empty_mock_db = n2p.from_notion_DB_to_dataframe(os.environ['NOTION_EMPTY_DB_ID'])
    columns_empty_db = set(df_empty_mock_db.columns)
    assert columns_empty_db == expected_columns
    assert df_empty_mock_db.empty