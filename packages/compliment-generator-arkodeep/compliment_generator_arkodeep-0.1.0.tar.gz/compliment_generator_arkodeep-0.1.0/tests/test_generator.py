import pytest
from compliment_generator import ComplimentGenerator

def test_get_compliment():
    cg = ComplimentGenerator()
    assert isinstance(cg.get_compliment(), str)

def test_get_compliment_by_category():
    cg = ComplimentGenerator()
    assert cg.get_compliment_by_category("funny") in cg.compliments["funny"]

def test_add_custom_compliment():
    cg = ComplimentGenerator()
    cg.add_custom_compliment("You are fantastic!", "custom")
    assert "You are fantastic!" in cg.compliments["custom"]

def test_list_categories():
    cg = ComplimentGenerator()
    assert "general" in cg.list_categories()
