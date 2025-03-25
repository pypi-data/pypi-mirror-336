"""
fbi_wanted_library

This package provides an interface to the FBI Wanted API, allowing users to search for wanted persons
with various filters. The main class is FBIWanted, which includes methods for searching and retrieving
results from the API.
"""

from .fbi_wanted import FBIWanted

__all__ = ['FBIWanted']
