import pytest

from galeriafora import AiMetadata


class TestAiMetadata:
    def test_can_be_created_with_valid_data(self):
        ai_metadata = AiMetadata(
            is_ai_generated=True,
        )

        assert ai_metadata.is_ai_generated is True

    def test_can_be_created_for_non_ai_content(self):
        ai_metadata = AiMetadata.create_non_ai_generated()
        assert ai_metadata.is_ai_generated is False

    def test_can_be_created_for_ai_generated_content(self):
        ai_metadata = AiMetadata.create_ai_generated()
        assert ai_metadata.is_ai_generated is True

    def test_str_representation(self):
        ai_metadata = AiMetadata(is_ai_generated=True)
        assert str(ai_metadata) == "AiMetadata(is_ai_generated=True)"

    def test_repr_representation(self):
        ai_metadata = AiMetadata(is_ai_generated=False)
        assert repr(ai_metadata) == "AiMetadata(is_ai_generated=False)"

    def test_equality(self):
        ai_metadata1 = AiMetadata(is_ai_generated=True)
        ai_metadata2 = AiMetadata(is_ai_generated=True)
        ai_metadata3 = AiMetadata(is_ai_generated=False)

        assert ai_metadata1 == ai_metadata2
        assert ai_metadata1 != ai_metadata3

    def test_immutability(self):
        ai_metadata = AiMetadata(is_ai_generated=True)

        with pytest.raises(AttributeError):
            ai_metadata.is_ai_generated = False

    def test_serialization(self):
        ai_metadata = AiMetadata(is_ai_generated=True)
        serialized = ai_metadata.to_dict()
        assert serialized == {"is_ai_generated": True}

    def test_deserialization(self):
        data = {"is_ai_generated": False}
        ai_metadata = AiMetadata.from_dict(data)
        assert ai_metadata.is_ai_generated is False
