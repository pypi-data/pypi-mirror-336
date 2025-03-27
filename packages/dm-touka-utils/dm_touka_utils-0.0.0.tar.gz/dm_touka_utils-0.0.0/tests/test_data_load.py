from pathlib import Path

import pandas as pd
import pytest

from dm_utils.data_load import read_csv_flexible, read_txt_flexible


@pytest.fixture
def utf8_csv(tmp_path):
    file = tmp_path / "utf8.csv"
    file.write_text("col1,col2\nあ,い\nう,え", encoding="utf-8")
    return file


@pytest.fixture
def shift_jis_csv(tmp_path):
    file = tmp_path / "shiftjis.csv"
    file.write_text("col1,col2\nあ,い\nう,え", encoding="shift_jis")
    return file


@pytest.fixture
def utf8_txt(tmp_path):
    file = tmp_path / "utf8.txt"
    file.write_text("これはUTF-8のテキストです。", encoding="utf-8")
    return file


@pytest.fixture
def shift_jis_txt(tmp_path):
    file = tmp_path / "shiftjis.txt"
    file.write_text("これはShift_JISのテキストです。", encoding="shift_jis")
    return file


def test_read_csv_flexible_utf8(utf8_csv):
    df = read_csv_flexible(utf8_csv)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert df.iloc[0, 0] == "あ"


def test_read_csv_flexible_shiftjis(shift_jis_csv):
    df = read_csv_flexible(shift_jis_csv)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert df.iloc[0, 1] == "い"


def test_read_txt_flexible_utf8(utf8_txt):
    txt = read_txt_flexible(utf8_txt)
    assert "UTF-8のテキスト" in txt


def test_read_txt_flexible_shiftjis(shift_jis_txt):
    txt = read_txt_flexible(shift_jis_txt)
    assert "Shift_JISのテキスト" in txt
