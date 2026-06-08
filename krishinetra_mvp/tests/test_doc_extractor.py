from modules.doc_extractor import (
    _fallback_extract, pdf_to_bytes, DOC_FIELDS
)


class FakeUploadedFile:
    def read(self) -> bytes:
        return b"fake pdf content"


def test_fallback_extract_land_record():
    result = _fallback_extract("sample_land_record.pdf")
    assert result["owner_name"] == "Rajesh Vitthal Patil"
    assert result["survey_number"] == "123/45"
    assert result["area_hectares"] == 3.25
    assert result["crop_type"] == "Sugarcane"


def test_fallback_extract_unknown():
    result = _fallback_extract("random.pdf")
    assert result["owner_name"] == "Sample Farmer"
    assert result["crop_type"] == "Cotton"


def test_fallback_extract_none():
    result = _fallback_extract(None)
    assert result["owner_name"] == "Sample Farmer"


def test_fallback_extract_all_keys_present():
    result = _fallback_extract("test.pdf")
    for field in DOC_FIELDS:
        assert field in result


def test_pdf_to_bytes():
    f = FakeUploadedFile()
    assert pdf_to_bytes(f) == b"fake pdf content"


def test_doc_fields_list():
    assert isinstance(DOC_FIELDS, list)
    assert len(DOC_FIELDS) >= 8
