# Standard library
import os
import time
import json
from collections import defaultdict
from typing import List, Dict, Callable, Tuple, Literal, Set
from functools import cache, cached_property

# Local
from scope.callgraph.dtos.Range import Range
from scope.ext.withrepo.withrepo import RepoFile, File
from scope.callgraph.resources.tree_sitter import (
    TREE_SITTER_REF_DEF_QUERIES,
    EXT_TO_TREE_SITTER_LANGUAGE,
)

# Third party
from tree_sitter import Language, Parser, Tree, Node
from tree_sitter_languages import get_parser, get_language
import rustworkx as rx
import numpy as np
from tqdm import tqdm

NODE_TYPE_LITERAL = Literal["definition", "reference"]


class ASTNode:
    def __init__(
        self,
        id: int,
        path: str,
        node_type: str,
        node_key: str,
        name_node: Node = None,
        body_node: Node = None,
    ):
        self.id = id
        self.path = path
        self.ext = os.path.splitext(path)[1]
        self.language = EXT_TO_TREE_SITTER_LANGUAGE.get(self.ext)
        self.name: str = None
        self.node_type: NODE_TYPE_LITERAL = node_type
        self.node_key: str = node_key
        self.name_range: Range = None
        self.code_range: Range = None
        self.error = None
        self.callers: List[int] = []
        self.calling: List[int] = []
        self.ambiguous_reference: bool = False
        if name_node or body_node:
            self.from_treesitter_nodes(name_node, body_node)

    def from_treesitter_nodes(self, name_node: Node, body_node: Node):
        if name_node:
            self.name = name_node.text.decode("utf-8")
            start_line, start_col = name_node.start_point
            end_line, end_col = name_node.end_point
            self.name_range = Range(
                start_line,
                start_col,
                end_line,
                end_col,
            )
            self.code_range = Range(
                start_line,
                start_col,
                end_line,
                end_col,
            )
        if body_node:
            body_start_line, body_start_col = body_node.start_point
            body_end_line, body_end_col = body_node.end_point
            self.code_range = Range(
                body_start_line,
                body_start_col,
                body_end_line,
                body_end_col,
            )

    def __repr__(self):
        return f"ASTNode(path={self.path}, name={self.name}, name_range={str(self.name_range)}, code_range={str(self.code_range)}, type={self.node_type}, callers={len(self.callers)}, calling={len(self.calling)})"

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.path, self.name, self.name_range, self.code_range))

    def __eq__(self, other):
        return (
            self.path == other.path
            and self.name == other.name
            and self.name_range == other.name_range
            and self.code_range == other.code_range
        )

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "name": self.name,
            "name_range": self.name_range.to_list(),
            "code_range": self.code_range.to_list(),
            # "type": self.node_type,
        }

    def invalid(self):
        return all([not self.name, not self.name_range or not self.code_range])

    @classmethod
    def from_dict(cls, ast_node_dict: Dict):
        ast_node = cls(
            id=ast_node_dict["id"],
            path=ast_node_dict["path"],
            node_type="definition",
        )
        ast_node.name = ast_node_dict["name"]
        ast_node.name_range = Range(
            start_line=ast_node_dict["name_range"][0],
            start_column=ast_node_dict["name_range"][1],
            end_line=ast_node_dict["name_range"][2],
            end_column=ast_node_dict["name_range"][3],
        )
        ast_node.code_range = Range(
            start_line=ast_node_dict["code_range"][0],
            start_column=ast_node_dict["code_range"][1],
            end_line=ast_node_dict["code_range"][2],
            end_column=ast_node_dict["code_range"][3],
        )
        return ast_node


class ScopeASTBuilder:
    def __init__(self, files: List[File], timeit: bool = False):
        self.files = files
        self.ext_set = set(file.file_extension for file in files)
        self.ext_to_sitter_language: Dict[str, Language] = {}
        self.ext_to_parser: Dict[str, Parser] = {}
        self.trees: Dict[str, Tree] = {}
        self.nodes: Dict[str, List[ASTNode]] = {}
        self.node_lookup: Dict[int, ASTNode] = {}
        self.language_groups: Dict[str, Set[str]] = defaultdict(set)
        self.global_id = 0
        self.timeit = timeit
        self._setup_parsers()
        self._setup_trees()
        # self.tree_data = self.walk_trees()
        self._parse()

    @property
    def has_errors(self) -> bool:
        return any(node.error for node in self.nodes.values())

    def _setup_parsers(self):
        for ext in self.ext_set:
            lang = EXT_TO_TREE_SITTER_LANGUAGE.get(ext)
            if lang is None:
                continue
            parser_language = get_language(lang)
            self.ext_to_sitter_language[ext] = parser_language
            parser = get_parser(lang)
            self.ext_to_parser[ext] = parser

    def _setup_trees(self):
        files_to_remove = set()
        for file in self.files:
            parser = self.ext_to_parser.get(file.file_extension)
            if parser is None:
                files_to_remove.add(file.abs_path)
                continue
            file_content = file.content.encode()
            self.trees[file.file_name] = parser.parse(file_content)

        _files = [file for file in self.files if file.abs_path not in files_to_remove]
        self.files = _files

    def _walk_tree(self, tree: Tree):
        cursor = tree.walk()

        def traverse():
            node_data = {
                "type": cursor.node.type,
                "text": cursor.node.text.decode("utf-8"),
                "start_point": cursor.node.start_point,
                "end_point": cursor.node.end_point,
            }

            # Store the current node data
            yield node_data

            # If the node has children, traverse them
            if cursor.goto_first_child():
                while True:
                    yield from traverse()
                    if not cursor.goto_next_sibling():
                        break
                cursor.goto_parent()

        yield from traverse()

    def walk_trees(self):
        tree_data = defaultdict(list)
        unique_types = set()
        for file_name, tree in self.trees.items():
            for node in self._walk_tree(tree):
                tree_data[file_name].append(node)
                unique_types.add(node["type"])
        print(json.dumps(list(unique_types), indent=4))
        return dict(tree_data)

    def _parse_file(self, file: RepoFile) -> List[ASTNode]:
        tree = self.trees.get(file.file_name)
        parser_language = self.ext_to_sitter_language.get(file.file_extension)
        lang = EXT_TO_TREE_SITTER_LANGUAGE.get(file.file_extension)
        if not lang or not tree:
            return []
        query_groups = TREE_SITTER_REF_DEF_QUERIES.get(lang, {})

        nodes = set()
        for ident_type, queries in query_groups.items():
            for query in queries:
                ref_query = queries[query]["query"]
                output_name = queries[query]["output_name"]
                output_body = queries[query].get("output_body")
                try:
                    sitter_query = parser_language.query(ref_query)
                except Exception as e:
                    print(
                        f"Error parsing query {ref_query} for file {file.file_name}: {e}"
                    )
                    continue
                try:
                    matches = sitter_query.matches(tree.root_node)
                except Exception as e:
                    print(
                        f"Error matching query {ref_query} for file {file.file_name}: {e}"
                    )
                    continue

                # Each match is a tuple of (match_index, match_dict, which can have multiple keys)
                # TODO: We only have single queries w/ multiple keys, we need to support multiple keys
                for match in matches:
                    try:
                        ts_node = match[1]
                        ts_name_node = ts_node.get(output_name)
                        ts_body_node = ts_node.get(output_body)
                        node_key = query
                        node = ASTNode(
                            self.global_id,
                            file.path,
                            ident_type,
                            node_key,
                            ts_name_node,
                            ts_body_node,
                        )
                        self.global_id += 1
                        if node.invalid():
                            print(f"Skipping invalid ASTNode: {node}")
                            continue
                        nodes.add(node)
                    except Exception as e:
                        import traceback

                        traceback.print_exc()
                        print(
                            f"Error constructing ASTNode for query {ref_query} for file {file.file_name}: {e}"
                        )
        return list(nodes)

    def _parse(self):
        for file in self.files:
            self.nodes[file.path] = self._parse_file(file)
            self.language_groups[file.language].add(file.path)
        for nodes in self.nodes.values():
            for node in nodes:
                self.node_lookup[node.id] = node

    def mark_ambiguous_references(self):
        shared_definitions = defaultdict(list)
        for d in self.definitions():
            shared_definitions[d.name].append(d)
        shared_definitions = {k: v for k, v in shared_definitions.items() if len(v) > 1}
        for r in self.references():
            if r.name in shared_definitions:
                shared_defs = shared_definitions[r.name]
                ref_and_def_share_location = any(r.path == d.path for d in shared_defs)
                if not ref_and_def_share_location:
                    r.ambiguous_reference = True


class ScopeAST:
    def __init__(self, files: List[File], build: bool = True):
        self.files = None
        self.nodes = None
        self.language_groups = None
        if build:
            builder = ScopeASTBuilder(files)
            self.files = builder.files
            self.nodes = builder.nodes
            self.language_groups = builder.language_groups

    def __repr__(self):
        unique_definitions = {d.name for d in self.definitions()}
        unique_references = {r.name for r in self.references()}
        len_defs = len(self.definitions())
        len_refs = len(self.references())
        len_defs_unique = len(unique_definitions)
        len_refs_unique = len(unique_references)
        return f"ScopeAST(files={len(self.files)} defs={len_defs} unique_defs={len_defs_unique} refs={len_refs} unique_refs={len_refs_unique})"

    @classmethod
    def empty(cls):
        return cls([])

    def split_by_language(self) -> List["ScopeAST"]:
        asts = []
        for lang, paths in self.language_groups.items():
            files = [f for f in self.files if f.path in paths]
            nodes = defaultdict(list)
            for path, node_list in self.nodes.items():
                if path in paths:
                    nodes[lang].extend(node_list)
            ast = ScopeAST.empty()
            ast.files = files
            ast.nodes = nodes
            ast.language_groups = {lang: paths}
            asts.append(ast)
        return asts

    @cache
    def definitions(self, path: str = None) -> List[ASTNode]:
        return self.search(
            lambda p, node: node.node_type == "definition"
            and (path is None or p.path == path)
        )

    @cache
    def references(self, path: str = None) -> List[ASTNode]:
        return self.search(
            lambda p, node: node.node_type == "reference"
            and (path is None or p.path == path)
        )

    def search(
        self, search_callback: Callable[[RepoFile, ASTNode], bool]
    ) -> List[ASTNode]:
        hits = []
        for file in self.files:
            for node in self.nodes[file.path]:
                if search_callback(file, node):
                    hits.append(node)
        return hits


class ApproximateCallGraphBuilder:
    def __init__(
        self, ast: ScopeAST, timeit: bool = False, prune_references: bool = True
    ):
        self.ast = ast
        self.callgraph_lookup: Dict[int, ASTNode] = {}
        self.callgraph: rx.PyDiGraph = rx.PyDiGraph(multigraph=False)
        self.node_indices: Dict[int, int] = {}
        self.timeit = timeit
        self.prune_references = prune_references

    @cache
    def get_containing_def_for_ref(self, path: str, ref_range: Range) -> ASTNode | None:
        # find smallest range that contains ref
        containing_defs: List[ASTNode] = []
        for defn in self.ast.definitions(path):
            if defn.code_range.contains(ref_range):
                containing_defs.append(defn)
        if not containing_defs:
            return None
        return min(containing_defs, key=lambda x: x.code_range.height())

    # Add some heuristic bias (if defn.calling are ambiguous and have the same name, prefer the ones that shares the same location with defn)
    def prune_calling(self, refs_at_path: List[ASTNode], defn: ASTNode):
        if len(defn.calling) <= 1:
            return

        calling_lookup = [self.callgraph_lookup[c] for c in defn.calling]
        namespace_counts: Dict[str, int] = defaultdict(int)
        for c in calling_lookup:
            namespace_counts[c.name] += 1

        defn_calling_copy = defn.calling
        defn.calling = []
        # print("namespace_counts: ", namespace_counts)
        for name, count in namespace_counts.items():
            if count <= 1:
                matching_defs = [c for c in calling_lookup if c.name == name]
                for d in matching_defs:
                    defn.calling.append(d.id)
                continue
            matching_defs = [c for c in calling_lookup if c.path == defn.path]
            for d in matching_defs:
                # NOTE: this check might be problematic, might have to compare the name range instead
                if defn.code_range.contains(d.code_range):
                    defn.calling.append(d.id)
                    break
            else:
                # NOTE: I think I need to add nodes here
                pass

        if not defn.calling:
            defn.calling = defn_calling_copy

    def _mark_references_for_path(self, path):
        """
        For all definitions in a path:
        - find the encapsulating definitions for the given definition (callers)
        - find the definitions that references the given definition (calling)
        """

        # Mark all definitions that are calling the given definition (ignore self-references)
        for defn in self.ast.definitions(path):
            for r in self.ast.references(path):
                if r.name != defn.name:
                    continue
                containing_defn = self.get_containing_def_for_ref(path, r.name_range)
                if (
                    containing_defn
                    and containing_defn != defn
                    and containing_defn.name != defn.name
                    and containing_defn.language == defn.language
                ):
                    defn.callers.append(containing_defn.id)

        # Mark all definitions that are called by the given definition (ignore self-references)
        for defn in self.ast.definitions(path):
            for r in self.ast.references(defn.path):
                if defn.code_range.contains(r.name_range):
                    for d in self.ast.definitions(r.path):
                        if d.name != r.name or d.language != defn.language:
                            continue
                        if d != defn and d.name != defn.name:
                            defn.calling.append(d.id)
            if self.prune_references:
                refs_at_path = self.ast.references(defn.path)
                self.prune_calling(refs_at_path, defn)

    def _mark_references(self, progress_bar: bool = False):
        time_start = time.time()
        paths = list(set([d.path for d in self.ast.definitions()]))
        if progress_bar:
            paths = tqdm(paths, total=len(paths), desc="Marking references")
        for path in paths:
            self._mark_references_for_path(path)
        if self.timeit:
            print(f"Time taken to mark references: {time.time() - time_start} seconds")

    def run(self, progress_bar: bool = False):
        # self.ast.mark_ambiguous_references()
        self.callgraph_lookup = {d.id: d for d in self.ast.definitions()}
        self._mark_references(progress_bar)

        time_start = time.time()

        nodes_added = self.callgraph.add_nodes_from(self.ast.definitions())
        print(f"Adding {len(self.ast.definitions())} nodes to the graph")

        node_indices = {d.id: ni for ni, d in zip(nodes_added, self.ast.definitions())}
        edges_to_add = []
        for d in self.ast.definitions():
            for caller in d.callers:
                caller_id = node_indices[caller]
                d_id = node_indices[d.id]
                edges_to_add.append((caller_id, d_id, [caller_id, d_id]))
            for callee in d.calling:
                callee_id = node_indices[callee]
                d_id = node_indices[d.id]
                edges_to_add.append((d_id, callee_id, [d_id, callee_id]))
        self.callgraph.add_edges_from(edges_to_add)
        if self.timeit:
            print(
                f"Time taken to build callgraph with rustworkx: {time.time() - time_start} seconds"
            )

        self.node_indices = node_indices


class ApproximateCallGraph:
    def __init__(
        self,
        callgraph: rx.PyDiGraph,
        callgraph_lookup: Dict[int, ASTNode],
        node_indices: Dict[int, int],
    ):
        self.callgraph = callgraph
        self.callgraph_lookup = callgraph_lookup
        self.node_indices = node_indices
        self.reversed_node_indices = {v: k for k, v in node_indices.items()}

    def __repr__(self):
        return f"ApproximateCallGraph(nodes={len(self.callgraph.nodes())}, edges={len(self.callgraph.edges())})"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def build(
        cls,
        ast: ScopeAST,
        timeit: bool = False,
        progress_bar: bool = False,
        prune_references: bool = True,
    ):
        builder = ApproximateCallGraphBuilder(ast, timeit, prune_references)
        builder.run(progress_bar)
        return cls(
            callgraph=builder.callgraph,
            callgraph_lookup=builder.callgraph_lookup,
            node_indices=builder.node_indices,
        )

    @classmethod
    def from_nodes_and_edges(cls, nodes: List[ASTNode], edges: List[Tuple[int, int]]):
        callgraph = rx.PyDiGraph(multigraph=False)
        callgraph.add_nodes_from(nodes)
        callgraph.add_edges_from([(s, t, [s, t]) for s, t in edges])
        return cls(
            callgraph=callgraph,
            callgraph_lookup={d.id: d for d in nodes},
            node_indices={d.id: i for i, d in enumerate(nodes)},
        )

    @cached_property
    def nodes(self) -> List[ASTNode]:
        return self.callgraph.nodes()

    @cached_property
    def edges(self) -> List[Tuple[int, int]]:
        return self.callgraph.edges()

    @cached_property
    def identifiers(self) -> List[str]:
        return list({d.name for d in self.nodes})

    def is_acyclic(self) -> bool:
        return rx.is_directed_acyclic_graph(self.callgraph)

    def adjacency_matrix(self) -> np.ndarray:
        return rx.adjacency_matrix(self.callgraph)

    def callers(self, node: ASTNode) -> List[ASTNode]:
        id = self.node_indices[node.id]
        return self.callgraph.predecessors(id)

    def calling(self, node: ASTNode) -> List[ASTNode]:
        id = self.node_indices[node.id]
        return self.callgraph.successors(id)

    def cycles(self):
        if self.is_acyclic():
            return []
        cycles = []
        for id in self.reversed_node_indices:
            edges = rx.digraph_find_cycle(self.callgraph, id)
            cycle_nodes = []
            if edges:
                for edge in edges:
                    start_node = self.reversed_node_indices[edge[0]]
                    end_node = self.reversed_node_indices[edge[1]]
                    start_node_name = self.callgraph_lookup[start_node]
                    end_node_name = self.callgraph_lookup[end_node]
                    cycle_nodes.append([start_node_name, end_node_name])
                cycles.append(cycle_nodes)
        return cycles

    def remove_cycles(self):
        cycles = self.cycles()
        for cycle_nodes_list in cycles:
            for cycle_nodes in cycle_nodes_list:
                try:
                    parent_node = cycle_nodes[0]
                    child_node = cycle_nodes[1]
                    parent_node_index = self.node_indices[parent_node.id]
                    child_node_index = self.node_indices[child_node.id]
                    self.callgraph.remove_edge(parent_node_index, child_node_index)
                    print(
                        f"Removed edge between {parent_node.name} and {child_node.name}"
                    )
                except Exception:
                    continue
                    # print(f"Error removing edge between {parent_node.name} and {child_node.name}: {e}")
