"""CMake dependency graph visualization tool."""

from .cli import (
    build_dependency_graph,
    filter_graph_by_target,
    exclude_external_dependencies,
    visualize_graph,
)

__version__ = "0.1.1"
__all__ = [
    "build_dependency_graph",
    "filter_graph_by_target",
    "exclude_external_dependencies",
    "visualize_graph",
]
