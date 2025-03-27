import pytest
import networkx as nx

from cmake2graph.cli import (
    parse_cmake_file,
    build_dependency_graph,
    filter_graph_by_target,
    exclude_external_dependencies
)


@pytest.fixture
def sample_cmake_content(tmp_path):
    cmake_content = """
    add_library(core src/core.cpp)
    add_library(math src/math.cpp)
    add_executable(app src/main.cpp)

    target_link_libraries(math
        PUBLIC core
    )

    target_link_libraries(app
        PRIVATE
            core
            math
    )
    """

    cmake_file = tmp_path / "CMakeLists.txt"
    cmake_file.write_text(cmake_content)
    return str(cmake_file)


def test_parse_cmake_file(sample_cmake_content):
    targets, dependencies = parse_cmake_file(sample_cmake_content)

    assert targets == {"core", "math", "app"}
    assert dependencies == {
        "math": ["core"],
        "app": ["core", "math"]
    }


def test_build_dependency_graph(tmp_path):
    # Create a mock CMake project structure
    (tmp_path / "src").mkdir()
    (tmp_path / "src/CMakeLists.txt").write_text("""
        add_library(core src/core.cpp)
        add_library(math src/math.cpp)
        target_link_libraries(math PUBLIC core)
    """)

    (tmp_path / "CMakeLists.txt").write_text("""
        add_executable(app src/main.cpp)
        target_link_libraries(app PRIVATE core math)
    """)

    graph = build_dependency_graph(str(tmp_path))

    assert set(graph.nodes()) == {"app", "core", "math"}
    assert set(graph.edges()) == {("app", "core"),
                                  ("app", "math"),
                                  ("math", "core")}


def test_filter_graph_by_target():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ("app", "core"),
        ("app", "math"),
        ("math", "core")
    ])

    filtered = filter_graph_by_target(graph, "app", max_depth=1)
    assert set(filtered.nodes()) == {"app", "core", "math"}
    assert set(filtered.edges()) == {("app", "core"),
                                     ("app", "math"),
                                     ("math", "core")}

    filtered = filter_graph_by_target(graph, "math", max_depth=1)
    assert set(filtered.nodes()) == {"core", "math"}
    assert set(filtered.edges()) == {("math", "core")}

    filtered = filter_graph_by_target(graph, "core")
    assert set(filtered.nodes()) == set()  # why not {"core"}?
    assert set(filtered.edges()) == set()


def test_exclude_external_dependencies():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ("app", "core"),
        ("app", "external1"),
        ("math", "core"),
        ("math", "external2")
    ])

    cmake_targets = {"app", "core", "math"}
    exclude_external_dependencies(graph, cmake_targets)

    assert set(graph.nodes()) == cmake_targets
    assert set(graph.edges()) == {("app", "core"), ("math", "core")}
