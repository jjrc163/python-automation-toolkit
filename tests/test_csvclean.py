from autotoolkit.csvclean import clean_csv, clean_rows


def test_clean_rows_strips_whitespace():
    rows = [{"name": "  Ana  ", "city": " Caracas "}]
    cleaned, duplicates = clean_rows(rows)
    assert cleaned == [{"name": "Ana", "city": "Caracas"}]
    assert duplicates == 0


def test_clean_rows_drops_empty_rows():
    rows = [{"name": "Ana"}, {"name": ""}, {"name": "Luis"}]
    cleaned, _ = clean_rows(rows)
    assert [r["name"] for r in cleaned] == ["Ana", "Luis"]


def test_clean_rows_deduplicates_on_key():
    rows = [
        {"email": "a@x.com", "name": "Ana"},
        {"email": "a@x.com", "name": "Ana Duplicate"},
        {"email": "b@x.com", "name": "Luis"},
    ]
    cleaned, duplicates = clean_rows(rows, key_columns=["email"])
    assert len(cleaned) == 2
    assert duplicates == 1


def test_clean_csv_end_to_end(tmp_path):
    source = tmp_path / "in.csv"
    source.write_text("name,city\nAna, Caracas \nAna, Caracas\nLuis, Merida\n", encoding="utf-8")

    report = clean_csv(source, output_path=tmp_path / "out.csv")

    assert report["rows_in"] == 3
    assert report["rows_out"] == 2
    assert report["duplicates_removed"] == 1
    assert (tmp_path / "out.csv").exists()