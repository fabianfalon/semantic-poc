import pytest

from src.domain.content_text_spliter import ContentTextSplitter


class BadSplitter(ContentTextSplitter):
    pass


def test_content_text_splitter_must_implement_split():
    with pytest.raises(TypeError):
        BadSplitter() 