from pathlib import Path

from autotoolkit.organize import category_for, organize


def test_category_for_known_extensions():
    assert category_for(Path("photo.JPG")) == "images"
    assert category_for(Path("report.pdf")) == "documents"
    assert category_for(Path("data.csv")) == "spreadsheets"
    assert category_for(Path("script.py")) == "code"
    assert category_for(Path("song.mp3")) == "audio"


def test_category_for_unknown_extension():
    assert category_for(Path("mystery.xyz")) == "other"


def test_organize_by_type_moves_files(tmp_path):
    (tmp_path / "a.png").write_text("x")
    (tmp_path / "b.pdf").write_text("x")
    (tmp_path / "c.py").write_text("x")

    moves = organize(tmp_path, by="type")

    assert len(moves) == 3
    assert (tmp_path / "images" / "a.png").exists()
    assert (tmp_path / "documents" / "b.pdf").exists()
    assert (tmp_path / "code" / "c.py").exists()


def test_organize_dry_run_does_not_move(tmp_path):
    (tmp_path / "a.png").write_text("x")

    moves = organize(tmp_path, by="type", dry_run=True)

    assert len(moves) == 1
    assert (tmp_path / "a.png").exists()
    assert not (tmp_path / "images").exists()


def test_organize_avoids_overwriting_duplicates(tmp_path):
    (tmp_path / "a.png").write_text("first")
    (tmp_path / "images").mkdir()
    (tmp_path / "images" / "a.png").write_text("existing")

    organize(tmp_path, by="type")

    assert (tmp_path / "images" / "a.png").read_text() == "existing"
    assert (tmp_path / "images" / "a_1.png").read_text() == "first"