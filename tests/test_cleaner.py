import pytest
from scraper.cleaner import (
    clean_price, clean_rating, clean_availability, 
    clean_title, clean_book, clean_books
)

# --- Tests for clean_price ---
def test_clean_price_valid():
    assert clean_price("£12.99") == 12.99
    assert clean_price("$50") == 50.0

def test_clean_price_invalid():
    assert clean_price("not a price") == 0.0
    assert clean_price(None) == 0.0

# --- Tests for clean_rating ---
def test_clean_rating_valid():
    assert clean_rating("Three") == 3
    assert clean_rating("One") == 1

def test_clean_rating_invalid():
    assert clean_rating("Six") == 0
    assert clean_rating(None) == 0

# --- Tests for clean_availability ---
def test_clean_availability_valid():
    assert clean_availability("In stock") is True
    assert clean_availability("  Only 2 left (In Stock) ") is True

def test_clean_availability_invalid():
    assert clean_availability("Out of stock") is False
    assert clean_availability(None) is False

# --- Tests for clean_title ---
def test_clean_title():
    assert clean_title("  The Great Gatsby  ") == "The Great Gatsby"
    assert clean_title(None) == ""

# --- Tests for clean_book ---
def test_clean_book():
    raw_data = {
        "title": " Dune ",
        "price": "£10.50",
        "rating": "Five",
        "availability": "In Stock"
    }
    expected = {
        "title": "Dune",
        "price": 10.5,
        "rating": 5,
        "available": True
    }
    assert clean_book(raw_data) == expected

# --- Tests for clean_books ---
def test_clean_books():
    raw_list = [
        {"title": "Book 1", "price": "10", "rating": "One", "availability": "In Stock"},
        {"title": "Book 2", "price": "20", "rating": "Two", "availability": "Out"}
    ]
    result = clean_books(raw_list)
    assert len(result) == 2
    assert result[0]["price"] == 10.0
    assert result[1]["available"] is False