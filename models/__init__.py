#!/usr/bin/python3
"""Initializes the models package."""
from models.engine.file_storage import FileStorage

# Create a FileStorage instance to interface with the filesystem.
storage = FileStorage()
# Load existing objects from the storage file, if any.
storage.reload()
