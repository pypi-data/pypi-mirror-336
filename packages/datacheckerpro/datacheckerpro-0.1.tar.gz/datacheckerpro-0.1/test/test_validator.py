import pytest
import sys
import os

# Adding the parent directory of the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datavalidatorpro.validator import DATAVALIDATOR
# Testing emails
def test_validate_email():
    validator = DATAVALIDATOR("okoliogechi74gmailcom")  # Testing invalid email
    assert validator.validate_email() == False

def test_validate_email():
    validator = DATAVALIDATOR("okoliogechi74@gmail.com")  # Testing valid email
    assert validator.validate_email() == True

# Testing phone numbers
def test_validate_phone():
    validator = DATAVALIDATOR("+2349075042986")  # Testing valid phone number
    assert validator.validate_phone() == True

def test_validate_phone():
    validator = DATAVALIDATOR("234907504286")  # Testing invalid phone number
    assert validator.validate_phone() == False

# Testing dates
def test_validate_date():
    validator = DATAVALIDATOR("2025-03-112")  # Testing invalid date
    assert validator.validate_date() == False

def test_validate_date():
    validator = DATAVALIDATOR("2025-03-12")  # Testing valid date
    assert validator.validate_date() == True

# Testing URLs
def test_validate_url():
    validator = DATAVALIDATOR("http://www.google.com")  # Testing valid URL
    assert validator.validate_url() == True

def test_validate_url():
    validator = DATAVALIDATOR("http:google.com")  # Testing invalid URL
    assert validator.validate_url() == False