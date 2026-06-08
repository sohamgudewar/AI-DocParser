from modules.security import (
    validate_pdf_upload, sanitize_filename,
    validate_coordinates, geojson_complexity_safe,
    PDF_MAGIC, MAX_FILE_SIZE_BYTES,
)


def test_validate_pdf_upload_valid():
    content = b"%PDF-1.4 some pdf content"
    err = validate_pdf_upload(content, "doc.pdf")
    assert err is None


def test_validate_pdf_upload_no_magic():
    content = b"not a pdf"
    err = validate_pdf_upload(content, "doc.pdf")
    assert err is not None
    assert "PDF" in err


def test_validate_pdf_upload_too_large():
    content = b"x" * (MAX_FILE_SIZE_BYTES + 1)
    err = validate_pdf_upload(content, "doc.pdf")
    assert err is not None
    assert "too large" in err.lower()


def test_validate_pdf_upload_bad_filename():
    content = b"%PDF-1.4 good content"
    err = validate_pdf_upload(content, "../../etc/passwd")
    assert err is not None


def test_sanitize_filename():
    assert sanitize_filename("hello.pdf") == "hello.pdf"
    assert "../" not in sanitize_filename("../bad.pdf")
    assert sanitize_filename("a" * 300) == "a" * 255


def test_validate_coordinates_valid():
    assert validate_coordinates(19.0, 76.0) is None


def test_validate_coordinates_out_of_bounds():
    assert validate_coordinates(99.0, 76.0) is not None
    assert validate_coordinates(19.0, 200.0) is not None
    assert validate_coordinates(10.0, 76.0) is not None


def test_geojson_complexity_safe():
    assert geojson_complexity_safe('{"type": "Point", "coordinates": [0, 0]}') is None


def test_geojson_complexity_safe_too_complex():
    big = "[" * 60000
    assert geojson_complexity_safe(big) is not None
