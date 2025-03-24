from importlib import metadata

from .field_factory import FieldFactory
from .model_factory import ModelFactory

__version__ = metadata.version("pydantricks")

__all__ = ["FieldFactory", "ModelFactory"]
