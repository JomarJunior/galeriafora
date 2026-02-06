import pytest

from galeriafora import MatureRating


class TestRating:
    def test_mature_rating_enum(self):
        assert MatureRating.PG.value == "pg"
        assert MatureRating.PG_13.value == "pg-13"
        assert MatureRating.R.value == "r"
        assert MatureRating.X.value == "x"
        assert MatureRating.XXX.value == "xxx"

    def test_str_representation(self):
        for rating in MatureRating.__members__.values():
            assert str(rating) == rating.value

    def test_equality(self):
        assert MatureRating.PG == MatureRating.PG
        assert MatureRating.PG != MatureRating.PG_13
        assert MatureRating.R == MatureRating.R
        assert MatureRating.R != MatureRating.X
        assert MatureRating.X == MatureRating.X
        assert MatureRating.X != MatureRating.XXX
        assert MatureRating.XXX == MatureRating.XXX
        assert MatureRating.XXX != MatureRating.PG

    def test_can_be_created_from_string(self):
        assert MatureRating("pg") == MatureRating.PG
        assert MatureRating("pg-13") == MatureRating.PG_13
        assert MatureRating("r") == MatureRating.R
        assert MatureRating("x") == MatureRating.X
        assert MatureRating("xxx") == MatureRating.XXX

    def test_string_equality(self):
        assert MatureRating.PG == "pg"
        assert MatureRating.PG_13 == "pg-13"
        assert MatureRating.R == "r"
        assert MatureRating.X == "x"
        assert MatureRating.XXX == "xxx"

    def test_can_be_assimilated_from_string(self):
        class CustomClass:
            def __init__(self, mature_rating: MatureRating):
                self.mature_rating = mature_rating

        custom_instance = CustomClass(mature_rating="pg")
        assert custom_instance.mature_rating == MatureRating.PG
