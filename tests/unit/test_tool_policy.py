"""Pure unit tests -- no network. Verifies the classification heuristic
against the project brief's own seven worked examples (section 9),
plus the explicit action-group overrides (section 6/3.9)."""

from app.security import tool_policy


def test_namespace_of():
    assert tool_policy.namespace_of("lifecycle_open_model") == "lifecycle"
    assert tool_policy.namespace_of("query_get_node_info") == "query"


def test_operation_class_worked_examples():
    # Exactly the seven examples given in the project brief.
    assert tool_policy.get_operation_class("query_get_node_info") == "READ"
    assert tool_policy.get_operation_class("analysis_get_mass_balance") == "READ"
    assert tool_policy.get_operation_class("links_set_loss_coeff") == "WRITE"
    assert tool_policy.get_operation_class("building_add_node") == "WRITE"
    assert tool_policy.get_operation_class("lifecycle_step_simulation") == "SIMULATION_CONTROL"
    assert tool_policy.get_operation_class("editing_delete_object") == "DESTRUCTIVE"
    assert tool_policy.get_operation_class("gym_start_optimization") == "OPTIMIZATION"


def test_gym_namespace_is_always_optimization():
    # Even a gym_* read-style getter is OPTIMIZATION -- the whole
    # namespace is treated as higher-risk/higher-cost per the brief.
    assert tool_policy.get_operation_class("gym_get_job") == "OPTIMIZATION"
    assert tool_policy.get_operation_class("gym_list_jobs") == "OPTIMIZATION"


def test_lifecycle_pure_getters_are_read():
    assert tool_policy.get_operation_class("lifecycle_get_simulation_state") == "READ"
    assert tool_policy.get_operation_class("lifecycle_list_sessions") == "READ"
    assert tool_policy.get_operation_class("lifecycle_is_between_events") == "READ"


def test_destructive_markers():
    assert tool_policy.get_operation_class("tables_clear_points") == "DESTRUCTIVE"
    assert tool_policy.is_destructive("editing_delete_object") is True
    assert tool_policy.is_destructive("query_get_node_info") is False


def test_action_group_prefix_mapping():
    assert tool_policy.get_action_group("lifecycle_open_model") == "core"
    assert tool_policy.get_action_group("nodes_get_tag") == "hydraulics"
    assert tool_policy.get_action_group("links_get_tag") == "hydraulics"
    assert tool_policy.get_action_group("xsect_list_shapes") == "hydraulics"
    assert tool_policy.get_action_group("twod_get_mesh_summary") == "twod"
    assert tool_policy.get_action_group("gym_start_optimization") == "optimization"
    assert tool_policy.get_action_group("hotstart_save_hotstart") == "optimization"


def test_action_group_explicit_overrides():
    # Confirmed live: these three exist on the real registry with names
    # that don't match their actual engineering domain by prefix alone.
    assert tool_policy.get_action_group("spatial_get_quality") == "water-quality"
    assert tool_policy.get_action_group("spatial_set_treatment") == "water-quality"
    assert tool_policy.get_action_group("spatial_add_lid") == "infrastructure"
    # Ordinary spatial_* tools are unaffected by the override table.
    assert tool_policy.get_action_group("spatial_get_coordinates") == "spatial"


def test_unknown_namespace_falls_back_to_core():
    assert tool_policy.get_action_group("totally_unknown_tool") == "core"
