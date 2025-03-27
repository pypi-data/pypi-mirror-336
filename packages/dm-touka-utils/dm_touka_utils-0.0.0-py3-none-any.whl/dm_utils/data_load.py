import pandas as pd


def read_csv_flexible(filename, first_encoding="utf-8"):
    """
    CSVファイルをutf-8で読み込み、エラーの場合はshift_jisで読み込む。
    """
    try:
        df = pd.read_csv(filename, encoding=first_encoding)
    except UnicodeDecodeError:
        df = pd.read_csv(filename, encoding="shift_jis")
    return df


def read_txt_flexible(filename, first_encoding="utf-8"):
    """
    テキストファイルをまずutf-8で読み込み、UnicodeDecodeErrorの場合はshift_jisで読み込み、文字列として返す。
    """
    try:
        with open(filename, encoding=first_encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filename, encoding="shift_jis") as f:
            return f.read()
