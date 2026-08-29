"""Action-group routing and READ/WRITE/SIMULATION_CONTROL/DESTRUCTIVE/
OPTIMIZATION classification for every tool the upstream MCP server
reports.

Classification is namespace + verb heuristic, per the project's own
design brief: "exact overrides for exceptional tools, then namespace,
then action verbs in the tool name." Verified against the brief's own
worked examples (see tests/unit/test_tool_policy.py) -- all seven check
out under this heuristic without needing a per-tool override table for
565 tools, which would be unmaintainable as the upstream registry
evolves. Only a handful of genuine cross-namespace exceptions get an
explicit override (see TOOL_ACTION_GROUP_OVERRIDES below).
"""

from __future__ import annotations

ACTION_GROUPS = (
    "core",
    "model-builder",
    "hydrology",
    "hydraulics",
    "forcing-controls",
    "results",
    "twod",
    "spatial",
    "water-quality",
    "infrastructure",
    "optimization",
)

OPERATION_CLASSES = ("READ", "WRITE", "SIMULATION_CONTROL", "DESTRUCTIVE", "OPTIMIZATION")

# Namespace -> action group. A tool's namespace is the segment before its
# first underscore (lifecycle_open_model -> "lifecycle").
PREFIX_TO_GROUP: dict[str, str] = {
    "lifecycle": "core",
    "model": "core",
    "datetime": "core",
    "building": "model-builder",
    "editing": "model-builder",
    "tables": "model-builder",
    "subcatchments": "hydrology",
    "climate": "hydrology",
    "inflows": "hydrology",
    "nodes": "hydraulics",
    "links": "hydraulics",
    "xsect": "hydraulics",
    "forcing": "forcing-controls",
    "controls": "forcing-controls",
    "query": "results",
    "analysis": "results",
    "twod": "twod",
    "spatial": "spatial",
    "geopackage": "spatial",
    "quality": "water-quality",
    "pollutants": "water-quality",
    "infrastructure": "infrastructure",
    "hotstart": "optimization",
    "gym": "optimization",
}

# Explicit per-tool overrides for tools whose namespace prefix doesn't
# match their actual engineering domain. Confirmed against the live
# registry's real tool names, not guessed -- spatial_get_quality and
# spatial_set_treatment are water-quality operations despite the
# "spatial_" prefix; spatial_add_lid places infrastructure, not GIS data.
TOOL_ACTION_GROUP_OVERRIDES: dict[str, str] = {
    "spatial_get_quality": "water-quality",
    "spatial_set_treatment": "water-quality",
    "spatial_add_lid": "infrastructure",
}

_READ_VERB_PREFIXES = (
    "get_",
    "list_",
    "is_",
    "find_",
    "search_",
    "describe_",
    "validate_",
    "compare_",
    "export_",
    "lookup",
)
_DESTRUCTIVE_MARKERS = ("delete_", "clear_")


def namespace_of(tool_name: str) -> str:
    return tool_name.split("_", 1)[0]


def get_action_group(tool_name: str) -> str:
    if tool_name in TOOL_ACTION_GROUP_OVERRIDES:
        return TOOL_ACTION_GROUP_OVERRIDES[tool_name]
    namespace = namespace_of(tool_name)
    return PREFIX_TO_GROUP.get(namespace, "core")


def get_operation_class(tool_name: str) -> str:
    namespace = namespace_of(tool_name)
    if namespace == "gym":
        return "OPTIMIZATION"

    remainder = tool_name[len(namespace) + 1 :] if "_" in tool_name else ""

    if remainder == "count" or remainder.endswith("_count"):
        return "READ"
    if any(remainder.startswith(marker) for marker in _DESTRUCTIVE_MARKERS):
        return "DESTRUCTIVE"
    if any(remainder.startswith(prefix) for prefix in _READ_VERB_PREFIXES):
        return "READ"
    if namespace == "lifecycle":
        # Anything in lifecycle_* that isn't a pure getter mutates
        # simulation state (open/close/run/step/stride/until/save/load/
        # events_*) -- classify the namespace's default as
        # SIMULATION_CONTROL rather than WRITE.
        return "SIMULATION_CONTROL"
    return "WRITE"


def is_destructive(tool_name: str) -> bool:
    return get_operation_class(tool_name) == "DESTRUCTIVE"
