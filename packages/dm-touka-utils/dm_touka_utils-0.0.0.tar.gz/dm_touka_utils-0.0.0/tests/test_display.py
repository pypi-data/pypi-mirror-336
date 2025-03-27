from dm_utils.display import display_string_by_rich


def test_display_string_by_rich():
    # 実行時エラーがないか確認するだけのテスト
    try:
        display_string_by_rich("テスト表示", title="テスト", style="green")
    except Exception as e:
        assert False, f"display_string_by_richがエラーを起こしました: {e}"
