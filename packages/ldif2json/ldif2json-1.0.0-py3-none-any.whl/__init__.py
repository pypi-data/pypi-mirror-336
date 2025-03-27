"""LDIF to JSON converter package."""
from .cli import parse_ldif, nest_entries

__version__ = "1.0.0"
__all__ = ['parse_ldif', 'nest_entries']
