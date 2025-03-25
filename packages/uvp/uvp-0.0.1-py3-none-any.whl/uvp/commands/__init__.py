# Package initialization to make commands a proper package
# Explicitly import all modules with commands to ensure they're registered
from . import base

# This ensures that all commands in these modules are registered with the app
__all__ = ["base"]
