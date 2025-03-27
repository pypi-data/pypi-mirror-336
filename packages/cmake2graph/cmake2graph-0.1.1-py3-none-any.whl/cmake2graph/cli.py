#!/usr/bin/env python

# Description: Visualize CMake target dependencies as a directed graph.
# Usage: python cmake2graph /path/to/cpp-cmake-project
# cmake2graph /path/to/cpp-cmake-project --output graph.png --target my_target

import os
import argparse
import networkx as nx
import matplotlib.pyplot as plt


def parse_cmake_file(cmake_file):
    """
    Parse a CMakeLists.txt file to extract target dependencies.
    Returns a tuple of (targets, dependencies) where:
    - targets is a set of all defined targets
    - dependencies is a dict of target -> list of dependencies
    """
    targets = set()
    dependencies = {}

    with open(cmake_file, 'r') as f:
        content = f.read()
        # Remove comments and join line continuations
        content = ' '.join(
            line.split('#')[0].strip()
            for line in content.splitlines()
        )

        # Split by commands while preserving parentheses content
        commands = content.replace('(', ' ( ').replace(')', ' ) ').split()

        i = 0
        while i < len(commands):
            cmd = commands[i].lower()
            if cmd in ('add_executable', 'add_library'):
                # Find content between parentheses
                try:
                    start = commands.index('(', i)
                    end = commands.index(')', start)
                    target_name = commands[start + 1]
                    targets.add(target_name)
                except (ValueError, IndexError):
                    pass
                i = end + 1 if 'end' in locals() else i + 1
            elif cmd in ('target_link_libraries', 'add_dependencies'):
                try:
                    start = commands.index('(', i)
                    end = commands.index(')', start)
                    target = commands[start + 1]
                    deps = commands[start + 2:end]
                    if target not in dependencies:
                        dependencies[target] = []
                    dependencies[target].extend(
                        d for d in deps if d != 'PUBLIC' and d != 'PRIVATE'
                    )
                except (ValueError, IndexError):
                    pass
                i = end + 1 if 'end' in locals() else i + 1
            else:
                i += 1

    return targets, dependencies


def build_dependency_graph(cmake_dir):
    """
    Build a directed graph of dependencies from CMake files in the
    given directory, including nested directories.
    """
    graph = nx.DiGraph()
    all_targets = set()
    all_dependencies = {}

    # First pass: collect all targets
    for root, _, files in os.walk(cmake_dir):
        for file in files:
            if file == "CMakeLists.txt":
                cmake_file = os.path.join(root, file)
                targets, deps = parse_cmake_file(cmake_file)
                all_targets.update(targets)
                for target, dependencies in deps.items():
                    if target not in all_dependencies:
                        all_dependencies[target] = []
                    all_dependencies[target].extend(dependencies)

    # Second pass: build graph with verified targets
    for target in all_targets:
        graph.add_node(target)

    for target, deps in all_dependencies.items():
        if target in all_targets:  # Only add edges for known targets
            for dep in deps:
                graph.add_edge(target, dep)

    return graph


def filter_graph_by_target(graph, target, max_depth=None):
    """
    Filter the graph to include only the specified target
    and its dependencies up to a given depth.
    """
    if target not in graph:
        raise ValueError(f"Target '{target}' not found in the graph.")

    filtered_graph = nx.DiGraph()
    nodes_to_visit = [(target, 0)]  # (node, current_depth)
    visited = set()

    while nodes_to_visit:
        current_node, current_depth = nodes_to_visit.pop(0)
        if (current_node in visited or
                (max_depth is not None and current_depth > max_depth)):
            continue
        visited.add(current_node)
        for neighbor in graph.successors(current_node):
            filtered_graph.add_edge(current_node, neighbor)
            nodes_to_visit.append((neighbor, current_depth + 1))

    return filtered_graph


def exclude_external_dependencies(graph, cmake_targets):
    """
    Exclude nodes from the graph that are not part of the
    CMake project targets.
    """
    external_nodes = [node for node in graph if node not in cmake_targets]
    graph.remove_nodes_from(external_nodes)


def visualize_graph(graph, output_file=None):
    """
    Visualize the dependency graph using matplotlib with improved
    layout and styling. Optionally save the graph to a file.
    """
    plt.figure(figsize=(12, 8))  # Larger figure size

    pos = nx.planar_layout(graph, scale=2)

    # print(graph.nodes)
    # print(dict(enumerate(nx.bfs_layers(graph,
    # ["app", "core_tests", "math_tests"]))))
    # pos = nx.bfs_layout(graph, ["app", "math_tests", "core_tests"])

    # Draw edges with arrows
    nx.draw_networkx_edges(graph, pos,
                           edge_color='black',
                           arrows=True,
                           arrowsize=20,
                           width=1.5,
                           alpha=1,
                           node_size=3000)

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos,
                           node_color='lightblue',
                           node_size=3000,
                           alpha=0.4,
                           linewidths=1,
                           edgecolors='darkblue')

    # Draw labels with slight offset for better visibility
    nx.draw_networkx_labels(graph, pos,
                            font_size=10,
                            font_weight='bold',
                            font_family='sans-serif')

    plt.title("CMake Target Dependencies", pad=20, fontsize=14)
    plt.axis('off')  # Hide axes

    # Add some padding around the graph
    plt.margins(0.2)

    if output_file:
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
    else:
        plt.show()

    plt.close()  # Clean up the figure


def main():
    parser = argparse.ArgumentParser(description="Visualize CMake target "
                                     "dependencies as a directed graph.")
    parser.add_argument("cmake_dir", help="Path to the directory "
                        "containing CMakeLists.txt files.")
    parser.add_argument("--output", help="Path to save the graph image "
                        "(e.g., graph.png).")
    parser.add_argument("--target",
                        help="Target to visualize dependencies for.")
    parser.add_argument("--depth", type=int,
                        help="Maximum depth of dependencies to include.")
    parser.add_argument("--exclude-external", action="store_true",
                        help="Exclude external libraries from the graph.")
    args = parser.parse_args()

    graph = build_dependency_graph(args.cmake_dir)

    if args.exclude_external:
        cmake_targets = set(graph.nodes)
        exclude_external_dependencies(graph, cmake_targets)

    if args.target:
        try:
            graph = filter_graph_by_target(graph, args.target, args.depth)
        except ValueError as e:
            print(e)
            return

    visualize_graph(graph, args.output)


if __name__ == "__main__":
    main()
