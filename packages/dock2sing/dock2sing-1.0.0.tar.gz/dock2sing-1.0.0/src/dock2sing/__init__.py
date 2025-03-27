"""
Dock2Sing - A tool for converting Docker Compose to Singularity Compose format.
"""

from .docker_to_singularity import convert_docker_to_singularity
from .singularity_compose_validator import validate_singularity_compose

__version__ = "0.1.0"
__all__ = ["convert_docker_to_singularity", "validate_singularity_compose"]
