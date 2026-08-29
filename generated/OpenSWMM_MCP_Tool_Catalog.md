# OpenSWMM MCP Tool Catalog

Generated from the live upstream server -- 565 tools.

## Namespace: analysis

### analysis_compare_scenarios

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Compare time-series output between two simulation sessions.

Retrieves the specified variable for all elements of the given type from
both sessions and returns summary statistics of the differences (mean,
max, min of the element-wise peak differences).

**Input arguments**

- `session_a` (string)
- `session_b` (string)
- `element_type` (string)
- `variable` (string)

---

### analysis_export_results

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Export node and link time-series results to CSV or JSON.

Writes one file containing all node and link output variables for every
reporting period.  Useful for downstream analysis in spreadsheets or
data-science tools.

**Input arguments**

- `session_id` (string)
- `output_path` (string)
- `format` (string)

---

### analysis_get_capacity_summary

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Summarise hydraulic capacity usage across all links in the model.

Returns a list of links whose maximum depth-to-full-depth ratio exceeds
*max_filling_threshold*, sorted by filling ratio in descending order.

**Input arguments**

- `session_id` (string)
- `max_filling_threshold` (number)

---

### analysis_get_flooding_summary

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Summarise flooding across all nodes in the model.

Returns a list of nodes that experienced flooding (volume > *min_flood_volume*),
sorted by total flood volume in descending order.

**Input arguments**

- `session_id` (string)
- `min_flood_volume` (number)

---

### analysis_get_mass_balance

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Retrieve mass-balance continuity errors and volumetric totals.

Returns the runoff, routing, and (if pollutants exist) quality continuity
errors together with the individual volume components (rainfall, runoff,
flooding, outflow, etc.).

**Input arguments**

- `session_id` (string)

---

### analysis_get_pump_summary

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return post-simulation performance statistics for all pump links.

Equivalent to the Pumping Summary section of the SWMM ``.rpt`` file.
Only links of type PUMP are returned; if the model has no pumps the
list will be empty.

Each entry includes:

* ``link_id`` — pump identifier
* ``pump_curve_idx`` — index of the pump curve used (``-1`` = ideal pump)
* ``num_startups`` — total on/off cycles during the simulation
* ``total_on_time`` — cumulative run time (seconds)
* ``total_volume`` — total volume pumped
* ``pct_time_on`` — percentage of simulation duration the pump was active

**Input arguments**

- `session_id` (string)

---

### analysis_get_quality_losses

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return per-pollutant evaporation and seepage mass losses.

These are the quality mass-balance loss terms the routing continuity
accounts for but which :func:`get_mass_balance` does not surface (it
reports continuity *errors* and volumetric totals). For every modelled
pollutant, returns the cumulative mass lost to evaporation and to
seepage (model mass units).

Requires the ``openswmm`` backend and a session in ``running`` or
``ended`` state.

**Input arguments**

- `session_id` (string)

---

### analysis_get_report_snapshot

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the full post-simulation report as structured data.

Assembles the programmatic equivalent of the SWMM ``.rpt`` file into a
single structured response covering:

* **Routing diagnostics** — time-step statistics and convergence metrics
  (average/min/max step, total steps, number and percentage of
  non-converging steps, average iterations, maximum Courant number)
* **Runoff continuity** — rainfall, evaporation, infiltration, runoff, and
  storage change volumes with continuity error
* **Flow routing continuity** — inflow components, flooding, outflow, and
  loss volumes with continuity error
* **Quality continuity** — per-pollutant mass balance with seep and evap
  losses (empty when no pollutants are modelled)
* **Node flooding summary** — all nodes that experienced overflow, sorted
  by total flood volume
* **Storage volume summary** — all STORAGE-type nodes with depth and
  volume statistics
* **Link flow summary** — all links with peak flow, velocity, filling
  ratio, total volume, and surcharge time
* **Pump summary** — PUMP links with startup count, total on-time,
  volume pumped, and percentage time on
* **Subcatchment runoff summary** — precipitation, runoff volume, peak
  rate, and runoff coefficient per subcatchment

**Input arguments**

- `session_id` (string)

---

### analysis_get_statistics

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Retrieve post-simulation statistics for a single model element.

Returns peak / max values and duration statistics collected by the engine
during the simulation run.

**Input arguments**

- `session_id` (string)
- `element_type` (string)
- `element_id` (string)

---

### analysis_get_time_series

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Retrieve a time series of output results for a model element.

Reads from the binary ``.out`` file produced by the simulation.  The
``start_period`` and ``end_period`` parameters select a slice of the
reporting periods (0-indexed).  Use ``downsample`` to skip periods for
large result sets (e.g. ``downsample=10`` returns every 10th value).

**Input arguments**

- `session_id` (string)
- `element_type` (string)
- `element_id` (string)
- `variable` (string)
- `start_period` (integer)
- `end_period` (integer)
- `downsample` (integer)

---

### analysis_output_link_attribute

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return all variable values for a link at a single reporting period.

Variables are returned as a dict keyed by name: ``flow``, ``depth``,
``velocity``, ``volume``, ``capacity``, plus ``pollutant_i`` columns
when pollutants are tracked.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `period` (integer)

---

### analysis_output_link_results

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return one link variable across all links at a single reporting period.

``variable`` is one of: ``flow``, ``depth``, ``velocity``, ``volume``,
``capacity``.

Returns a list of ``{id, index, value}`` records.

**Input arguments**

- `session_id` (string)
- `variable` (string)
- `period` (integer)

---

### analysis_output_metadata

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return header metadata for the .out file (counts + timing + version).

Combines several small reader getters into one call so an LLM can size
a subsequent batch read in a single round-trip.

**Input arguments**

- `session_id` (string)

---

### analysis_output_node_attribute

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return all variable values for a node at a single reporting period.

Variables are returned as a dict keyed by name: ``depth``, ``head``,
``volume``, ``lateral_inflow``, ``total_inflow``, ``overflow``, plus
``pollutant_0`` .. ``pollutant_{n-1}`` when pollutants are tracked.

Wraps ``swmm_output_get_node_attribute`` — the per-object snapshot
accessor distinct from ``get_time_series`` (one variable over time)
and ``get_node_result`` (one variable over all nodes at one period).

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `period` (integer)

---

### analysis_output_node_results

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return one node variable across all nodes at a single reporting period.

``variable`` is one of: ``depth``, ``head``, ``volume``,
``lateral_inflow``, ``total_inflow``, ``overflow``.

Returns a list of ``{id, index, value}`` records ordered by node index
(which matches the .out file's stored order).

**Input arguments**

- `session_id` (string)
- `variable` (string)
- `period` (integer)

---

### analysis_output_node_stats

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return post-run node statistics aggregated from the .out file.

Wraps the four engine-level accessors
``swmm_output_get_node_stat_max_depth`` /
``_max_overflow`` /
``_vol_flooded`` /
``_time_flooded``.

These differ from :func:`get_flooding_summary` in two ways:

  * the aggregation is computed from the **binary output file**
    (so it works even after the engine handle is closed); and
  * the response covers a **single named node**, not a filtered
    list across the whole network.

**Input arguments**

- `session_id` (string)
- `node_id` (string)

---

### analysis_output_period_count

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of reporting periods written to the .out file.

**Input arguments**

- `session_id` (string)

---

### analysis_output_period_time

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the elapsed time (project time units) for a reporting period.

The value combines with ``start_date`` (from :func:`output_metadata`)
to produce an absolute timestamp.

**Input arguments**

- `session_id` (string)
- `period` (integer)

---

### analysis_output_pollutant_count

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of pollutants tracked in the .out file.

**Input arguments**

- `session_id` (string)

---

### analysis_output_subcatch_attribute

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return all variable values for a subcatchment at a reporting period.

Variables: ``rainfall``, ``snow_depth``, ``evap``, ``infil``, ``runoff``,
``gw_flow``, ``gw_elev``, ``soil_moist``, plus ``pollutant_i`` columns
when pollutants are tracked.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `period` (integer)

---

### analysis_output_subcatch_results

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return one subcatchment variable across all subcatchments at a period.

``variable`` is one of: ``rainfall``, ``snow_depth``, ``evap``, ``infil``,
``runoff``, ``gw_flow``, ``gw_elev``, ``soil_moist``.

Returns a list of ``{id, index, value}`` records.

**Input arguments**

- `session_id` (string)
- `variable` (string)
- `period` (integer)

---

### analysis_output_system_result

- **Namespace**: analysis
- **Action Group**: results
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return a single system-level variable at a single reporting period.

Cheaper than ``get_time_series`` when only one timestep is needed.
``variable`` is one of: ``temperature``, ``rainfall``, ``snow_depth``,
``evap``, ``infil``, ``runoff``, ``dw_inflow``, ``gw_inflow``,
``lat_inflow``, ``flooding``, ``outflow``, ``storage``, ``evap_total``,
``pet``.

**Input arguments**

- `session_id` (string)
- `variable` (string)
- `period` (integer)

---

## Namespace: building

### building_add_curve

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a curve to the model.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `curve_type` (string)
- `x_values` (any)
- `y_values` (any)

---

### building_add_gage

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a rain gage to the model.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)

---

### building_add_link

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a link (conduit, pump, orifice, weir, or outlet) to the model.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `link_type` (string)
- `from_node` (string)
- `to_node` (string)
- `length` (number)
- `roughness` (number)
- `xsect_shape` (string)
- `xsect_geom1` (number)
- `xsect_geom2` (number)
- `xsect_geom3` (number)
- `xsect_geom4` (number)

---

### building_add_node

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a node to the model being built.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `node_type` (string)
- `invert_elev` (number)
- `max_depth` (number)
- `x` (any)
- `y` (any)

---

### building_add_pollutant

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a pollutant to the model.

Valid in ``building`` or ``opened`` state.  After adding, the pollutant
can be referenced by its ID when configuring buildup/washoff or quality
injection.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (string)
- `units` (string)
- `kdecay` (number)
- `rain_conc` (number)
- `gw_conc` (number)
- `init_conc` (number)
- `snow_only` (boolean)

---

### building_add_subcatchment

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a subcatchment to the model.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `area` (number)
- `imperv_pct` (number)
- `slope` (number)
- `width` (number)
- `outlet_node` (string)

---

### building_add_timeseries

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a time series to the model.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `times` (any)
- `values` (any)

---

### building_create_model

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create an empty SWMM model and start a building session.

Returns metadata for the new session.  Use the ``add_node``, ``add_link``,
``add_subcatchment``, and related tools to populate the model before
calling ``validate_model`` or ``write_model``.

**Input arguments**

- `session_id` (string)

---

### building_pop_last_link

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the most recently added link (undo of ``add_link``).

The supplied ``link_id`` must match the current tail of the link
list, otherwise the engine returns ``SWMM_ERR_BADINDEX``.

**Input arguments**

- `session_id` (string)
- `link_id` (string)

---

### building_pop_last_node

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the most recently added node (undo of ``add_node``).

The supplied ``node_id`` must match the current tail of the node
list. If any link still references the tail node, the engine
refuses the pop — call ``pop_last_link`` for those links first.

**Input arguments**

- `session_id` (string)
- `node_id` (string)

---

### building_set_option

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a simulation option on the model being built.

**Input arguments**

- `session_id` (string)
- `option` (string)
- `value` (string)

---

### building_validate_model

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Validate the model being built.

Runs the engine's built-in validation checks and returns any warnings
or errors.  A model with no messages is considered valid.

**Input arguments**

- `session_id` (string)

---

### building_write_model

- **Namespace**: building
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Finalize and write the model to an ``.inp`` file.

If the session is still in ``building`` state, the :class:`ModelBuilder` is
finalized to produce a :class:`Solver`, which is then used to write the
file.  If the session already has a solver (e.g. it was previously
finalized), the existing solver writes the file directly.

**Input arguments**

- `session_id` (string)
- `output_path` (string)

---

## Namespace: climate

### climate_get_climate_config

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read the full climate configuration of the model (read-only).

Returns temperature, evaporation, wind, snowmelt-global, areal-depletion,
and monthly-adjustment settings in the project's display units.

**Input arguments**

- `session_id` (string)

---

### climate_set_adjustments

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Edit the [ADJUSTMENTS] monthly arrays (12 values each): temperature
offsets, and evaporation / rainfall / conductivity multipliers. Conductivity
values <= 0 are stored as 1.0 (legacy behaviour).

**Input arguments**

- `session_id` (string)
- `temperature` (any)
- `evaporation` (any)
- `rainfall` (any)
- `conductivity` (any)

---

### climate_set_areal_depletion

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Edit the snow areal-depletion curves (10 fractions in [0, 1] each) for
impervious and/or pervious surfaces.

**Input arguments**

- `session_id` (string)
- `impervious` (any)
- `pervious` (any)

---

### climate_set_evaporation_config

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Edit [EVAPORATION] config. ``method`` is constant/monthly/timeseries/
temperature/file. ``monthly`` and ``pan_coeff`` are 12 values each. Setting
``timeseries`` also switches the method to TIMESERIES.

**Input arguments**

- `session_id` (string)
- `method` (any)
- `monthly` (any)
- `timeseries` (any)
- `pan_coeff` (any)
- `recovery_pattern` (any)
- `dry_only` (any)

---

### climate_set_snowmelt_config

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Edit the [TEMPERATURE] SNOWMELT globals: snow/rain dividing temperature,
ATI weight (TIPM, 0..1), and negative-melt ratio (RNM, 0..1).

**Input arguments**

- `session_id` (string)
- `divide_temp` (any)
- `ati_weight` (any)
- `neg_melt_ratio` (any)

---

### climate_set_temperature_config

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Edit [TEMPERATURE] config. ``source`` is none/timeseries/file. Setting
``timeseries`` also switches the source to TIMESERIES. ``latitude`` must be
in [-90, 90]; ``longitude_correction_min`` is minutes of solar-time offset.
``file_units`` is the climate-file temperature units: auto/c10/c/f.

**Input arguments**

- `session_id` (string)
- `source` (any)
- `timeseries` (any)
- `elevation` (any)
- `latitude` (any)
- `longitude_correction_min` (any)
- `file_start` (any)
- `file_units` (any)

---

### climate_set_windspeed_config

- **Namespace**: climate
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Edit [TEMPERATURE] WINDSPEED config. ``source`` is monthly/file;
``monthly`` is 12 average wind speeds.

**Input arguments**

- `session_id` (string)
- `source` (any)
- `monthly` (any)

---

## Namespace: controls

### controls_add_rule

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a control rule to the model (lifecycle-spanning).

Accepts the full SWMM rule text including the ``RULE <id>`` header,
one or more ``IF`` / ``AND`` / ``OR`` clauses, and a ``THEN`` action
block (and optional ``ELSE`` / ``PRIORITY`` clauses). Lines are
newline-separated within the string.

Works in any non-closed state. The runtime-only counterpart
``forcing.add_control_rule`` enforces ``state=running`` and is the
right tool when adding rules mid-simulation.

Example
-------
.. code-block:: text

    RULE PUMP_ON
    IF NODE J1 DEPTH > 5.0
    THEN PUMP P1 STATUS = ON

**Input arguments**

- `session_id` (string)
- `rule_text` (string)

---

### controls_clear_rules

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Remove every control rule from the model.

**Input arguments**

- `session_id` (string)

---

### controls_count

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of control rules defined in the model.

**Input arguments**

- `session_id` (string)

---

### controls_find_references

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the indices of control rules that reference an object by name.

Wraps ``Controls.find_references``. Scans each rule's clauses for an
object-type keyword (``NODE`` / ``LINK`` / ``CONDUIT`` / ``PUMP`` /
``ORIFICE`` / ``WEIR`` / ``OUTLET``) immediately followed by
*object_name* (case-insensitive). Read-only — no rule text is edited.
Use this before deleting or renaming an object to find the rules that
would be affected.

**Input arguments**

- `session_id` (string)
- `object_name` (string)

---

### controls_get_id

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the canonical rule name parsed from the I{rule_index}-th
control rule's text (the first token after the ``RULE`` keyword,
case-insensitive).

When the rule text is malformed (no parseable ``RULE`` keyword
token), ``name`` is ``None`` so callers can render a sentinel
display label like ``Rule N [unnamed]`` without catching exceptions.

**Input arguments**

- `session_id` (string)
- `rule_index` (integer)

---

### controls_get_rule

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the full text of the I{rule_index}-th control rule.

The rule text is multi-line: a ``RULE <id>`` header followed by ``IF``
/ ``AND`` / ``OR`` clauses and a ``THEN`` action block.

**Input arguments**

- `session_id` (string)
- `rule_index` (integer)

---

### controls_list_rules

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return all control rules as a list of ``{index, name, text}`` dicts.

**Input arguments**

- `session_id` (string)

---

### controls_remove_rule

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove a single control rule by index (later rules shift down by one).

Wraps ``Controls.remove_rule``. Unlike :func:`clear_rules`, which drops
every rule, this deletes only the I{rule_index}-th rule; all rules after
it renumber down. Requires the engine to be in ``building`` or ``opened``
state.

**Input arguments**

- `session_id` (string)
- `rule_index` (integer)

---

### controls_set_link_setting

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a continuous control setting on a link (RUNNING state only).

Maps to ``swmm_control_set_link_setting``. Used for pump speeds,
orifice openings, weir crest positions — anywhere the engine model
accepts a 0..1 (or higher, depending on link type) continuous value.

Distinct from :func:`set_link_status` which sets a discrete OPEN/CLOSED
state. The plan documents the split: ``setting`` is continuous,
``status`` is binary.

For mid-simulation control, prefer ``forcing.set_link_control`` which
is functionally equivalent — both wrap the same C call. This tool
exists in the ``controls`` namespace for naming symmetry with the rest
of the rule-management surface.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `setting` (number)

---

### controls_set_link_status

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the discrete OPEN/CLOSED status of a link (RUNNING state only).

Maps to ``swmm_control_set_link_status``. The boolean ``open`` is
forwarded as the inverse to v1's keyword-only ``closed`` argument.

For continuous control settings (pump speed, orifice opening),
use :func:`set_link_setting`.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `open` (boolean)

---

### controls_validate_rule

- **Namespace**: controls
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Validate control-rule text WITHOUT adding it to the model.

Parses *rule_text* through the engine's rule compiler and reports
whether it is syntactically valid. On failure ``message`` carries the
engine's diagnostic string; on success it is empty. Use this to
pre-flight a rule before committing it via :func:`add_rule` (or the
runtime ``forcing.add_control_rule``).

Accepts the full SWMM rule text (the ``RULE <id>`` header, ``IF`` /
``AND`` / ``OR`` clauses, and a ``THEN`` action block). Works in any
non-closed state and never mutates the model.

**Input arguments**

- `session_id` (string)
- `rule_text` (string)

---

## Namespace: datetime

### datetime_add_seconds

- **Namespace**: datetime
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Advance a SWMM DateTime by a number of seconds (may be negative).

**Input arguments**

- `value` (number)
- `seconds` (number)

---

### datetime_decode_date

- **Namespace**: datetime
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Decode the calendar date (year, month, day) from a SWMM DateTime.

**Input arguments**

- `value` (number)

---

### datetime_decode_time

- **Namespace**: datetime
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Decode the time-of-day (hour, minute, second) from a SWMM DateTime.

**Input arguments**

- `value` (number)

---

### datetime_encode_date

- **Namespace**: datetime
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Encode a calendar date as a SWMM DateTime (days since 1899-12-30).

The returned ``value`` has a zero time-of-day fraction; add a time
component with :func:`encode_time` (sum the two values) or advance it
with :func:`add_seconds`.

**Input arguments**

- `year` (integer)
- `month` (integer)
- `day` (integer)

---

### datetime_encode_time

- **Namespace**: datetime
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Encode a time-of-day as the fractional part of a SWMM DateTime.

**Input arguments**

- `hour` (integer)
- `minute` (integer)
- `second` (integer)

---

### datetime_time_diff

- **Namespace**: datetime
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return ``value1 - value2`` as a whole number of seconds.

**Input arguments**

- `value1` (number)
- `value2` (number)

---

## Namespace: editing

### editing_analyze_impact

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Preview what would be affected if an object were deleted, without deleting it.

Use this to inspect cascades and reference nullifications before calling
``delete_object``.  No objects are modified.

**Input arguments**

- `session_id` (string)
- `object_type` (string)
- `object_id` (string)

---

### editing_configure_gage

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Configure a rain gage's data source and recording parameters.

Only fields that are explicitly provided (non-null) are updated.
Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `rain_type` (any)
- `rain_interval` (any)
- `data_source` (any)
- `timeseries_id` (any)
- `filename` (any)
- `station_id` (any)

---

### editing_convert_link

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Convert a link to a different type in place.

Common properties (endpoint nodes, offsets, initial flow) are preserved.
Type-specific properties are cleared and new-type defaults applied.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `new_type` (string)

---

### editing_convert_node

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Convert a node to a different type in place.

Common properties (invert elevation, max depth, coordinates) are preserved.
Type-specific properties for the old type are cleared and sensible defaults
for the new type are applied.  Non-fatal topology warnings are reported but
do not prevent conversion.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `new_type` (string)

---

### editing_delete_object

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Delete a model object and cascade-delete or nullify all referencing objects.

When ``dry_run`` is ``True`` the impact is analysed but nothing is deleted
(equivalent to :func:`analyze_impact`).

**Cascade policy**

* Links that reference a deleted node as an endpoint are **deleted**.
* Subcatchment ``outlet_node``, inlet-usage ``node_index``, and similar
  weak references are **nullified** (set to -1).
* All integer cross-references whose value exceeded the deleted index are
  decremented by 1.

**Input arguments**

- `session_id` (string)
- `object_type` (string)
- `object_id` (string)
- `dry_run` (boolean)

---

### editing_get_gage_metadata

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the data-source metadata :func:`configure_gage` writes.

``configure_gage`` is write-only for these fields and
``query_get_gage_info`` does not return them, so this is the only way to
verify what a gage was configured with:

* ``rain_interval`` — recording interval in seconds.
* ``rain_units`` — ``in`` / ``mm``, the depth unit declared for a *file*
  source. Distinct from ``rain_type`` (intensity / volume / cumulative),
  which ``query_get_gage_info`` already reports.
* ``timeseries_id`` — assigned series id (empty for a file source).
* ``station_id`` — station id within an external file (empty otherwise).

Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)

---

### editing_get_gage_scale_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a rain gage's rainfall scale factor.

The scale factor multiplies the gage's raw rainfall series — values
above 1.0 amplify, below 1.0 attenuate. :func:`configure_gage` does
not touch it; use :func:`set_gage_scale_factor` to change it.
Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)

---

### editing_get_gage_snow_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a rain gage's snow catch factor (SCF).

The SCF corrects the physical gage's snow-catch deficiency: below the snow
temperature threshold, snowfall is multiplied by it. Distinct from the
rainfall :func:`get_gage_scale_factor` — SCF affects only the snow branch.
Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)

---

### editing_get_subcatch_rain_scale_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a subcatchment's rainfall scale factor.

Optional ``[SUBCATCHMENTS]`` token 9 (default 1.0). Multiplies this
subcatchment's gage-derived rainfall only, composing with the gage's own
scale factor. Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)

---

### editing_get_subcatch_snow_scale_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a subcatchment's snowfall scale factor.

Optional ``[SUBCATCHMENTS]`` token 10 (default 1.0). Composes with the gage
snow catch factor (SCF). Valid in ``building``, ``opened``, or
``initialized`` state.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)

---

### editing_rename_gage

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a rain gage (wraps ``swmm_gage_rename``).

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `new_id` (string)

---

### editing_rename_landuse

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a land use.

Land uses are referenced positionally, so buildup / washoff rows and
subcatchment coverages follow automatically.

**Input arguments**

- `session_id` (string)
- `landuse_id` (string)
- `new_id` (string)

---

### editing_rename_link

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a link (wraps ``swmm_link_rename``).

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `new_id` (string)

---

### editing_rename_node

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a node (wraps ``swmm_node_rename``).

The new id must be unique across the node namespace and non-empty.
The engine returns SWMM_ERR_BADPARAM on collision or empty input.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `new_id` (string)

---

### editing_rename_pattern

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a time pattern, updating every stored reference to it.

**Input arguments**

- `session_id` (string)
- `pattern_id` (string)
- `new_id` (string)

---

### editing_rename_pollutant

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a pollutant.

Name-stored references (``[INFLOWS]`` / ``[DWF]`` constituent rows) follow
the new name; index-stored ones (co-pollutant, buildup / washoff columns)
are positional and unaffected.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (string)
- `new_id` (string)

---

### editing_rename_subcatchment

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a subcatchment (wraps ``swmm_subcatch_rename``).

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `new_id` (string)

---

### editing_rename_transect

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename a transect (by id or zero-based index), updating stored references.

**Input arguments**

- `session_id` (string)
- `transect_id` (any)
- `new_id` (string)

---

### editing_set_gage_rain_units

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the rain-depth units declared for a file-based gage.

``rain_units`` is ``in`` (inches) or ``mm`` (millimetres). This is the
depth unit of the values in the external file — *not* the rain type
(intensity / volume / cumulative), which :func:`configure_gage` sets.
:func:`configure_gage` does not touch it. Valid in ``building``,
``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `rain_units` (string)

---

### editing_set_gage_scale_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a rain gage's rainfall scale factor.

The scale factor multiplies the gage's raw rainfall series. Maps to the
v1 ``Gage.scale_factor`` attribute, which :func:`configure_gage` leaves
untouched. Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `scale_factor` (number)

---

### editing_set_gage_snow_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a rain gage's snow catch factor (SCF; must be > 0).

The SCF multiplies the gage's snowfall (the below-freezing branch of the
rain/snow split); it does not touch rainfall. Maps to the ``Gage.snow_factor``
attribute, distinct from :func:`set_gage_scale_factor`. Valid in
``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `snow_factor` (number)

---

### editing_set_gage_station_id

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the station id a file-based gage reads from.

:func:`configure_gage` only applies ``station_id`` alongside a
``filename``; this sets it on its own, e.g. to point an already-configured
file source at a different station. Valid in ``building``, ``opened``, or
``initialized`` state.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `station_id` (string)

---

### editing_set_link_properties

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update geometry properties of an existing link in place.

Only fields that are explicitly provided (non-null) are updated.
Valid in ``building``, ``opened``, or ``initialized`` state.

Cross-section fields (``xsect_shape``, ``xsect_geom1``–``xsect_geom4``)
are applied as a group only when ``xsect_shape`` is provided.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `length` (any)
- `roughness` (any)
- `offset_up` (any)
- `offset_dn` (any)
- `initial_flow` (any)
- `max_flow` (any)
- `xsect_shape` (any)
- `xsect_geom1` (any)
- `xsect_geom2` (any)
- `xsect_geom3` (any)
- `xsect_geom4` (any)

---

### editing_set_node_properties

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update geometry properties of an existing node in place.

Only fields that are explicitly provided (non-null) are updated.
All others are left unchanged.  Valid in ``building``, ``opened``,
or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `invert_elev` (any)
- `max_depth` (any)
- `initial_depth` (any)
- `surcharge_depth` (any)
- `ponded_area` (any)

---

### editing_set_subcatch_rain_scale_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a subcatchment's rainfall scale factor (must be > 0).

Optional ``[SUBCATCHMENTS]`` token 9. Settable mid-run for parameter
sweeps / RTC. Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `scale_factor` (number)

---

### editing_set_subcatch_snow_scale_factor

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a subcatchment's snowfall scale factor (must be > 0).

Optional ``[SUBCATCHMENTS]`` token 10. Composes with the gage snow catch
factor (SCF); settable mid-run. Valid in ``building``, ``opened``, or
``initialized`` state.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `scale_factor` (number)

---

### editing_set_subcatchment_properties

- **Namespace**: editing
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update properties of an existing subcatchment in place.

Only fields that are explicitly provided (non-null) are updated.
Valid in ``building``, ``opened``, or ``initialized`` state.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `area` (any)
- `width` (any)
- `slope` (any)
- `imperv_pct` (any)
- `n_imperv` (any)
- `n_perv` (any)
- `ds_imperv` (any)
- `ds_perv` (any)
- `outlet_node_id` (any)
- `gage_id` (any)

---

## Namespace: forcing

### forcing_add_control_rule

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a new control rule to the running simulation.

The rule is specified in SWMM rule syntax and takes effect immediately.

**Input arguments**

- `session_id` (string)
- `rule_text` (string)

---

### forcing_clear_forcing

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Clear forcing overrides.

If both *target_type* and *element_id* are ``None`` (the default), all
forcing overrides across the entire model are removed.  Otherwise, only
the forcing on the specified element is cleared.

**Input arguments**

- `session_id` (string)
- `target_type` (any)
- `element_id` (any)

---

### forcing_get_climate_evap_rate

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current climate-derived evaporation rate (read-only).

Reports the broadcast potential-evapotranspiration rate the engine would
apply in the absence of any PET forcing, including monthly adjustments,
in user units (in/day for US projects, mm/day for SI). Intended for
caller-side composition: read this rate, apply your own adjustment
logic, and prescribe the result via ``forcing_set_forcing`` with
``target_type="subcatchment"`` and ``variable="evap"``.

**Input arguments**

- `session_id` (string)

---

### forcing_get_climate_state

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the current climate inputs (read-only).

Returns the air temperature, wind speed, dry-only flag, and the
climate-derived evaporation rate the engine is currently using (after any
forcing). Requires the ``openswmm`` backend.

**Input arguments**

- `session_id` (string)

---

### forcing_set_climate_dry_only

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Toggle the climate "evaporate only during dry weather" rule.

When enabled, evaporation is suppressed during rainfall periods. Requires
the ``openswmm`` backend; takes effect on the next step.

**Input arguments**

- `session_id` (string)
- `flag` (boolean)

---

### forcing_set_climate_forcing

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Apply a model-global climate forcing override.

Overrides a climate input that applies to the whole model (not a single
element): air temperature, wind speed, or potential evaporation. These
feed snowmelt, evaporation, and other climate-driven processes from the
next step on.

Climate forcing is a v1-only capability and requires the ``openswmm``
backend.

**Input arguments**

- `session_id` (string)
- `variable` (string)
- `value` (number)
- `mode` (string)
- `persist` (boolean)

---

### forcing_set_forcing

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Apply a runtime forcing override to a model element.

Overrides the value of a specific variable on a node, link, subcatchment,
or rain gage for the current (and optionally future) timesteps.

**Input arguments**

- `session_id` (string)
- `target_type` (string)
- `element_id` (string)
- `variable` (string)
- `value` (number)
- `mode` (string)
- `persist` (boolean)

---

### forcing_set_link_control

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the control setting on a link.

Directly overrides a link's control setting (e.g. pump speed, orifice
opening fraction) for the current timestep.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `setting` (number)

---

### forcing_set_link_quality

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Force a pollutant concentration on a link (RUNNING state only).

Overrides the in-link concentration of a single pollutant for the
current (and, with ``persist=True``, future) timesteps. The
element-keyed :func:`set_forcing` covers node quality but not link
quality, so this is the dedicated link-quality forcing tool.

Link quality forcing is a v1-only capability and requires the
``openswmm`` backend.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `pollutant` (string)
- `value` (number)
- `mode` (string)
- `persist` (boolean)

---

### forcing_set_persistent_forcing

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Apply a forcing override that **persists across timesteps**.

Equivalent to :func:`set_forcing` with ``persist=True``, surfaced as
its own tool so an LLM doesn't have to know about the persist flag
to get a sticky override.  Use :func:`clear_forcing` to remove the
override later.

Sticky overrides are a v1-only capability — they require the new
engine.  On the legacy backend the call is rejected with
``NOT_SUPPORTED`` because legacy resets API values every step
automatically.

**Input arguments**

- `session_id` (string)
- `target_type` (string)
- `element_id` (string)
- `variable` (string)
- `value` (number)
- `mode` (string)

---

### forcing_set_rainfall_override

- **Namespace**: forcing
- **Action Group**: forcing-controls
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Override rainfall on a rain gage with a persistent replacement value.

This is a convenience shortcut that applies a ``REPLACE`` + ``PERSIST``
forcing on the specified rain gage.  Use :func:`clear_forcing` to remove
the override later.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `rainfall` (number)

---

## Namespace: geopackage

### geopackage_close_geopackage

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Close a GeoPackage connection.

**Input arguments**

- `session_id` (string)

---

### geopackage_compare_sim_vs_observed

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Compare simulated results against observed data.

**Input arguments**

- `session_id` (string)
- `simulation_id` (string)
- `element_type` (string)
- `element_id` (string)
- `variable` (string)
- `observed_series_id` (integer)

---

### geopackage_get_result_summary

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read a summary statistic from the GeoPackage.

**Input arguments**

- `session_id` (string)
- `simulation_id` (string)
- `element_type` (string)
- `element_id` (string)
- `variable` (string)

---

### geopackage_get_result_timeseries

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read a simulation result timeseries from the GeoPackage.

**Input arguments**

- `session_id` (string)
- `simulation_id` (string)
- `element_type` (string)
- `element_id` (string)
- `variable` (string)

---

### geopackage_import_observed_data

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Import observed/sensor data into the GeoPackage for calibration.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `variable` (string)
- `element_type` (string)
- `element_id` (string)
- `timestamps` (any)
- `values` (any)
- `source` (string)
- `units` (string)

---

### geopackage_is_registered

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Check whether the GeoPackage plugin is registered.

:returns: Dict with the boolean ``registered`` flag.

---

### geopackage_last_error

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the most recent error message from the GeoPackage library.

**Input arguments**

- `session_id` (string)

---

### geopackage_list_simulations

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

List all simulation runs in the GeoPackage.

**Input arguments**

- `session_id` (string)

---

### geopackage_open_geopackage

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Open a GeoPackage file for querying results or observed data.

**Input arguments**

- `path` (string)
- `session_id` (string)

---

### geopackage_query_double

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Run a read-only SQL query and return the first double result.

**Input arguments**

- `session_id` (string)
- `sql` (string)

---

### geopackage_query_int

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Run a read-only SQL query and return the first integer result.

**Input arguments**

- `session_id` (string)
- `sql` (string)

---

### geopackage_register

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Register the GeoPackage plugin.

**Input arguments**

- `key` (string)
- `org` (string)
- `email` (string)
- `deploy` (string)

---

### geopackage_topology_edge_count

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of topology edges for a simulation.

**Input arguments**

- `session_id` (string)
- `simulation_id` (string)

---

### geopackage_write_observed_value

- **Namespace**: geopackage
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Write a single observed data point to an existing series.

Use ``import_observed_data`` to create a series and bulk-load points;
this tool appends one point to a series that already exists.

**Input arguments**

- `session_id` (string)
- `series_id` (integer)
- `timestamp` (string)
- `value` (number)
- `flag` (string)

---

## Namespace: gym

### gym_apply_design

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Apply a job's optimized design vector to an open model session.

Picks I{evaluation} (C{"best"} by default, or a 1-based evaluation
number from the job log) and writes its decision values onto the
session's model elements through the same engine surface the design
factories use: link roughness, link length, conduit diameter
(xsect geom1), and node maximum depth, each clipped to the factory's
[low, high] design range.

The session must be open or initialized on the new engine. The
change is in-memory — call C{building_write_model} to persist a new
C{.inp}, or rerun the simulation to evaluate it. Requires the gym
extra.

For a C{"market"} job (operational tuning) there is no model edit: the
optimized controller config is written to C{market_config.tuned.json} in
the job's output dir and its path is returned; C{session_id} is ignored.
A C{"schedule"} job similarly writes C{schedule.tuned.json} (the optimized
open-loop control schedule).

**Input arguments**

- `job_id` (string)
- `session_id` (string)
- `evaluation` (any)

---

### gym_cancel_job

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Request cooperative cancellation; takes effect between evaluations.

**Input arguments**

- `job_id` (string)

---

### gym_compare_runs

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Score several finished jobs' Pareto fronts with the same indicators.

Returns one row per job (front size + each indicator value) so runs
of different algorithms, budgets, or scenarios can be compared
directly. Argument requirements per indicator match
C{gym_score_front}. Requires the gym extra.

**Input arguments**

- `job_ids` (array)
- `indicators` (array)
- `reference_point` (any)
- `ideal_point` (any)
- `reference_front` (any)
- `weights` (any)

---

### gym_create_env_config

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Validate and persist a named environment config as JSON.

I{config} must satisfy the EnvConfig schema (see
C{gym_list_capabilities} for kinds, params, and env types). The
config is written to C{<config_dir>/<name>.json} — user-visible,
reviewable, and versionable — and survives server restarts.

**Input arguments**

- `name` (string)
- `config` (object)
- `overwrite` (boolean)
- `config_dir` (any)

---

### gym_decode_policy

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Decode a control-curve result vector into per-asset PWL curves.

For a finished C{control_curve} optimization job, maps a chosen decision
vector back onto each controlled link's human-readable curve — the applied
(monotonic-projected) C{y_values} at each fixed C{x_knot}, with the
observed node and attribute. I{index} selects which point: C{"best"} (the
convenience single pick) or an integer string indexing the Pareto front
(C{"0"}, C{"1"}, ...). Requires the gym extra.

**Input arguments**

- `job_id` (string)
- `index` (string)

---

### gym_delete_env_config

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Delete the named stored config.

**Input arguments**

- `name` (string)
- `config_dir` (any)

---

### gym_describe_benchmark

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

List or describe the registered C{OpenSWMM/*} benchmark env IDs.

Without I{benchmark_id}, returns all Gymnasium registry entries whose
ID starts with C{"OpenSWMM/"}. With it, returns that entry's details.
Requires the gym extra.

**Input arguments**

- `benchmark_id` (any)

---

### gym_env_close

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Close the interactive env and release its engine handle.

**Input arguments**

- `env_id` (string)

---

### gym_env_open

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Open an interactive env the LLM can drive step by step.

Builds the env from a stored config I{name} or inline I{config}
(exactly one) and holds it server-side under I{env_id}. Call
C{gym_env_reset} to start an episode, C{gym_env_step} repeatedly to
control it, and C{gym_env_close} when done — open envs hold engine
handles and are swept after prolonged idleness. Requires the gym
extra.

**Input arguments**

- `env_id` (string)
- `name` (any)
- `config` (any)
- `config_dir` (any)

---

### gym_env_reset

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Reset the interactive env and return the initial observation.

**Input arguments**

- `env_id` (string)
- `seed` (any)

---

### gym_env_step

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Advance the interactive env one control interval.

I{action} mirrors the env's Dict action space, e.g.
C{{"runtime": {"orifice_setting": [0.4]}}}. Omitted leaves default
to the Box midpoint; values are clipped to the leaf bounds. Returns
the observation, reward (scalar, or vector for C{mo_rtc}),
termination flags, and the per-term reward components from C{info}.

**Input arguments**

- `env_id` (string)
- `action` (any)

---

### gym_get_env_config

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Return the full stored config JSON for I{name}.

**Input arguments**

- `name` (string)
- `config_dir` (any)

---

### gym_get_job

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Return the progress snapshot of an optimization job.

**Input arguments**

- `job_id` (string)

---

### gym_get_job_results

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Return the results of a finished job.

Includes every evaluation's labeled decision vector and objective
costs, the Pareto-optimal subset (multi-objective), a convenient
single best pick, and artifact paths.

**Input arguments**

- `job_id` (string)

---

### gym_list_capabilities

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

List the full declarative vocabulary for environment configs.

Returns every registered kind — reward terms, runtime/design action
factories, and wrappers — with a one-line description and the JSON
schema of its C{params}, plus the valid C{env_type} values. Derived
from the kind registry, so it is always in sync with what
C{gym_create_env_config} accepts.

Also returns the C{EnvConfig} envelope schema, the C{ObservationSpec}
schema and its valid feature keys (C{observation_features}), and one
worked C{example} per common env_type, so the whole config shape is
discoverable without reading source.

Works without the gym extra installed (pure metadata).

---

### gym_list_env_configs

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

List stored config names in the config directory.

**Input arguments**

- `config_dir` (any)

---

### gym_list_envs

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

List open interactive envs with their idle times and step counts.

---

### gym_list_jobs

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

List all optimization jobs (newest first) with their states.

---

### gym_pareto_filter

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Return the non-dominated subset of objective vectors.

Pass either I{front} (inline list of cost vectors, minimize) or
I{job_id} (a finished optimization job — its already-Pareto front is
re-filtered, which is a cheap no-op check). Returns the front and
the indices of the surviving rows. Requires the gym extra.

**Input arguments**

- `front` (any)
- `job_id` (any)

---

### gym_run_episode

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Run one episode of a stored or inline env config and return totals.

Pass either a stored config I{name} or an inline I{config} (exactly
one). I{policy} selects the per-step action source:

  - C{{"kind": "constant", "action": {"runtime": {...}}}} — fixed
    action every step; omitted leaves default to the Box midpoint
    (so C{policy=None} runs a neutral do-nothing baseline).
  - C{{"kind": "random", "seed": 7}} — uniform samples from the
    action space.
  - C{{"kind": "replay", "actions": [{...}, ...]}} — explicit
    per-step sequence; the episode stops when it is exhausted.

Artifacts (C{trajectory.jsonl}, C{summary.json}) are written to
I{run_dir}, defaulting to C{<inp_dir>/gym_runs/<run_id>/} so they
are always user-reviewable. Requires the gym extra.

**Input arguments**

- `name` (any)
- `config` (any)
- `policy` (any)
- `run_dir` (any)
- `max_steps` (integer)
- `seed` (any)
- `config_dir` (any)

---

### gym_score_front

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Compute quality indicators over a front of cost vectors.

Available indicators and their required arguments:

  - C{hypervolume}: I{reference_point} (nadir / worst-case).
  - C{normalized_hypervolume}: I{ideal_point} + I{reference_point}.
  - C{igd}, C{igd_plus}, C{epsilon_indicator}: I{reference_front}.
  - C{spread}: no extra arguments.
  - C{r2_indicator}: I{weights} (list of weight vectors) +
    I{reference_point}.

The front comes from I{front} (inline) or I{job_id} (finished job),
exactly one. Requires the gym extra.

**Input arguments**

- `indicators` (array)
- `front` (any)
- `job_id` (any)
- `reference_point` (any)
- `ideal_point` (any)
- `reference_front` (any)
- `weights` (any)

---

### gym_start_optimization

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Start a background design-search job; returns immediately.

The env config (stored I{name} or inline I{config}, exactly one)
must have a searchable static factory: design_factories (env_type
C{cip} or C{joint}) or a policy_factory (env_type C{control_curve},
C{market}, C{schedule}). For C{control_curve} the decision vector is
the per-knot breakpoint settings; decode a result with
C{gym_decode_policy}.
I{optimization} sets the run, e.g.::

    {"algorithm": "random_search", "budget": 40, "seed": 7}
    {"algorithm": "nsga2", "budget": 400, "population_size": 20}

Algorithms: C{random_search}, C{grid_search} (grid_levels per
dimension), or a Platypus MOEA — C{nsga2}, C{nsga3}, C{spea2},
C{moead}, C{gde3} (requires platypus-opt). Each evaluation is one
episode; objectives are the direction-adjusted reward-term totals
(costs to minimize). Artifacts (C{job.json}, C{evaluations.jsonl},
C{result.json}) land in I{output_dir}, defaulting to
C{<inp_dir>/gym_runs/<job_id>/}.

Poll with C{gym_get_job}; fetch results with C{gym_get_job_results};
stop with C{gym_cancel_job}. Requires the gym extra.

**Input arguments**

- `name` (any)
- `config` (any)
- `optimization` (any)
- `output_dir` (any)
- `config_dir` (any)

---

### gym_validate_env_config

- **Namespace**: gym
- **Action Group**: optimization
- **Operation Class**: OPTIMIZATION
- **Destructive**: No

**Description**

Instantiate the config against the real engine and report spaces.

Pass either a stored config I{name} or an inline I{config} dict
(exactly one). The env is constructed, reset once so every element
ID is resolved against the model, then closed — catching bad IDs and
inconsistent specs before any long run. Requires the gym extra.

Returns the resolved observation size, the full (wrapped) action
space, and the reward-term wiring.

**Input arguments**

- `name` (any)
- `config` (any)
- `config_dir` (any)

---

## Namespace: hotstart

### hotstart_clone_session

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Clone an existing session by saving and re-applying its hot-start state.

A new session is created using the same ``.inp`` file as the source.
The source's current hydraulic state is written to a temporary hot-start
file and then applied to the freshly opened target session.

**Input arguments**

- `source_id` (string)
- `target_id` (string)

---

### hotstart_get_file_sim_time

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the simulation moment stored *inside* a hot-start file.

This is the timestamp the state was captured at, read from the file's
header — not the live clock. ``lifecycle_get_simulation_time`` reports the
running session's current time; this tool answers "what point in the run
does this checkpoint represent?" without applying it to anything.

No session state is touched; ``session_id`` is accepted only so the tool
is uniform with the rest of the namespace.

**Input arguments**

- `session_id` (string)
- `path` (string)

---

### hotstart_load_hotstart

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Load a previously saved hot-start file into a session.

The hot-start file is opened and its state is applied to the session's
solver, allowing a simulation to resume from a saved checkpoint.

**Input arguments**

- `session_id` (string)
- `path` (string)

---

### hotstart_save_hotstart

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Save the current simulation state to a hot-start file.

The session must be in the ``"running"`` or ``"ended"`` state so that
there is meaningful hydraulic state to persist.

**Input arguments**

- `session_id` (string)
- `path` (string)

---

### hotstart_saves_add

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Append a new SAVE HOTSTART entry.

``datetime_oadate`` is decimal days (OADate). Use ``0.0`` to schedule
a save at end of simulation.

**Input arguments**

- `session_id` (string)
- `path` (string)
- `datetime_oadate` (number)

---

### hotstart_saves_clear

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove every scheduled save.

**Input arguments**

- `session_id` (string)

---

### hotstart_saves_count

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of scheduled SAVE HOTSTART entries in [FILES].

**Input arguments**

- `session_id` (string)

---

### hotstart_saves_get

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the path + datetime of the I{index}-th scheduled save.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### hotstart_saves_remove

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the I{index}-th scheduled save. Trailing entries shift down.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### hotstart_saves_set

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update the path and/or datetime of the I{index}-th scheduled save.

Fields not supplied (None) are left unchanged.  v1 SaveSchedule
requires a full entry replacement, so we read-modify-write.

**Input arguments**

- `session_id` (string)
- `index` (integer)
- `path` (any)
- `datetime_oadate` (any)

---

### hotstart_seed_hotstart_state

- **Namespace**: hotstart
- **Action Group**: optimization
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Seed specific element states from a hot-start file into a session.

Opens the hot-start file at ``path``, overrides individual element
states with the supplied id→value maps, and applies the result to the
session's solver. This surfaces the engine's hot-start state setters
(``set_node_depth`` / ``set_node_head`` / ``set_link_depth`` /
``set_link_flow`` / ``set_subcatchment_runoff``) so callers can build
deterministic initial conditions — e.g. reproducible RL episode resets.

All values are in the model's project units (see ``get_unit_system``):
depths/heads in project length units, flows in project flow units,
runoff in project flow units.

**Input arguments**

- `session_id` (string)
- `path` (string)
- `node_depths` (any)
- `node_heads` (any)
- `link_depths` (any)
- `link_flows` (any)
- `subcatchment_runoffs` (any)

---

## Namespace: inflows

### inflows_add_dwf

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a dry-weather flow to a node.

``constituent`` is ``"FLOW"`` or a pollutant ID. ``avg_value`` is the
constant baseline value. The four pattern arguments are pattern IDs
(empty string = unused); use ``tables.pattern_add`` to create them.

Pattern coupling: this tool does not verify that the named patterns
exist before forwarding to the engine. A dangling reference will be
surfaced by the engine at lookup time, not here.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `constituent` (string)
- `avg_value` (number)
- `monthly_pattern` (string)
- `daily_pattern` (string)
- `hourly_pattern` (string)
- `weekend_pattern` (string)

---

### inflows_add_external

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add an external inflow to a node.

``constituent`` is either ``"FLOW"`` or a pollutant ID. ``inflow_type``
is one of ``"FLOW"``, ``"CONCEN"``, ``"MASS"``. ``ts_name`` references
an existing ``[TIMESERIES]`` entry (empty string for none).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `constituent` (string)
- `ts_name` (string)
- `inflow_type` (string)
- `m_factor` (number)
- `s_factor` (number)
- `baseline` (number)
- `pattern` (string)

---

### inflows_add_hydrograph

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a unit-hydrograph parameter line.

``month`` is ``"all"``/``-1`` (the default), ``"jan"``..``"dec"``, or
``0..11``. ``response`` is ``"short"``/``"medium"``/``"long"`` or
``0..2``.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `month` (any)
- `response` (any)
- `r` (number)
- `t` (number)
- `k` (number)
- `dmax` (number)
- `drecov` (number)
- `dinit` (number)

---

### inflows_add_hydrograph_gage

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a rain gage to a unit-hydrograph group.

The gage drives the RDII calculation for every node that references
this hydrograph via :func:`add_rdii`.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `gage_name` (string)

---

### inflows_add_rdii

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign an RDII inflow to a node.

``uh_name`` references a unit hydrograph group created via
:func:`add_hydrograph`. ``area`` is the contributing sewershed area
(project area units).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `uh_name` (string)
- `area` (number)

---

### inflows_add_rdii_decay

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add an exponential IA-decay row for a ``(uh_name, response)`` pair.

Replaces the legacy linear ``drecov`` rate from :func:`add_hydrograph`
with a physically-based recovery model:

    depletion: dIA/dt = -k_dep * rainfall
    recovery:  dIA/dt = +k_0 + k_T * exp(theta_rec * (T - T_ref))

Recovery is suppressed when ``T <= T_freeze``. The hydrograph row for
``(uh_name, response)`` must already exist.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `response` (any)
- `k_dep` (number)
- `k_0` (number)
- `k_T` (number)
- `T_ref` (number)
- `theta_rec` (number)
- `T_freeze` (number)

---

### inflows_clear_hydrograph_group_months

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Clear the month-specific rows of a UH group, keeping the ALL-months row.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)

---

### inflows_dwf_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of dry-weather-flow rows in the model.

**Input arguments**

- `session_id` (string)

---

### inflows_ext_inflow_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of external inflow rows in the model.

**Input arguments**

- `session_id` (string)

---

### inflows_get_dwf

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the I{entry_index}-th dry-weather-flow row as a dict.

Returns the persisted ``[DWF]`` row: node, constituent, average value,
and the four pattern IDs (monthly / daily / hourly / weekend).

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_get_external

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the I{entry_index}-th external inflow row as a dict.

Returns the persisted ``[INFLOWS]`` row: node, constituent, time-series
name, inflow type, scale (``m_factor``), unit conversion (``s_factor``),
baseline, and baseline pattern.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_get_hydrograph

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the I{entry_index}-th hydrograph row as a dict.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_get_hydrograph_gage

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the I{entry_index}-th UH-to-gage assignment as ``(uh_name, gage_name)``.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_get_rdii

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the I{entry_index}-th RDII assignment as ``(node_idx, uh_name, area)``.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_get_rdii_decay

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the I{entry_index}-th exponential-decay row as a dict.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_hydrograph_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of hydrograph parameter rows in the model.

**Input arguments**

- `session_id` (string)

---

### inflows_hydrograph_gage_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of UH-to-gage assignments in the model.

**Input arguments**

- `session_id` (string)

---

### inflows_hydrograph_group_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of *unique* unit-hydrograph group names.

A UH "group" is identified by name; the engine stores one row per
``(group, month, response)``. This count is the number of distinct
group names across parameter entries and gage assignments — the
figure a GUI Object Browser needs for the Unit Hydrographs section.

**Input arguments**

- `session_id` (string)

---

### inflows_list_hydrograph_groups

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the unit-hydrograph groups as a list of ``{index, name}`` dicts.

Groups are enumerated in first-occurrence order across the parameter
entry list (matches the order in which they appear in the
``[HYDROGRAPHS]`` section of the input file). Convenience wrapper
that batches ``hydrograph_group_count`` + N x
``get_hydrograph_group_id`` so an LLM (or GUI Object Browser) can
populate the Unit Hydrographs node in a single call.

**Input arguments**

- `session_id` (string)

---

### inflows_rdii_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of RDII inflow rows in the model.

**Input arguments**

- `session_id` (string)

---

### inflows_rdii_decay_count

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of exponential IA-decay rows in the model.

**Input arguments**

- `session_id` (string)

---

### inflows_remove_dwf

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the I{entry_index}-th dry-weather-flow row.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_remove_external

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the I{entry_index}-th external inflow row.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_remove_hydrograph_entry

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove a single ``(uh_name, month, response)`` hydrograph parameter row.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `month` (any)
- `response` (any)

---

### inflows_remove_hydrograph_group

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove an entire unit-hydrograph group (all rows + its gage assignment).

**Input arguments**

- `session_id` (string)
- `uh_name` (string)

---

### inflows_remove_rdii

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the I{entry_index}-th RDII assignment.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)

---

### inflows_remove_rdii_decay

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the exponential IA-decay row for a ``(uh_name, response)`` pair.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `response` (any)

---

### inflows_rename_hydrograph_group

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Rename the I{group_index}-th unit-hydrograph group.

``group_index`` is the position from :func:`list_hydrograph_groups`.

**Input arguments**

- `session_id` (string)
- `group_index` (integer)
- `new_id` (string)

---

### inflows_set_dwf_baseline

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the average (baseline) value of the I{entry_index}-th DWF row.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)
- `avg_value` (number)

---

### inflows_set_external_baseline

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the baseline (constant) value of the I{entry_index}-th external inflow.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)
- `baseline` (number)

---

### inflows_set_external_scale

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the time-series scale factor (``s_factor``) of the I{entry_index}-th external inflow.

Note: this sets ``s_factor`` (the engine's only runtime "scale" setter),
not the ``m_factor`` multiplier — ``m_factor`` is set only at
:func:`add_external` time.

**Input arguments**

- `session_id` (string)
- `entry_index` (integer)
- `scale` (number)

---

### inflows_set_hydrograph_gage

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set (replace) the rain gage assigned to an existing UH group.

Unlike :func:`add_hydrograph_gage` (which appends a new assignment row),
this updates the gage of a group that already has one.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `gage_name` (string)

---

### inflows_set_hydrograph_ia

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update the initial-abstraction parameters of an existing UH row.

Edits ``dmax``/``drecov``/``dinit`` in place, leaving R/T/K untouched.
The ``(uh_name, month, response)`` row must already exist. ``drecov`` is
ignored at runtime when an exponential-decay row exists for the same
``(uh_name, response)`` pair (see :func:`add_rdii_decay`).

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `month` (any)
- `response` (any)
- `dmax` (number)
- `drecov` (number)
- `dinit` (number)

---

### inflows_set_hydrograph_rtk

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update the R/T/K parameters of an existing ``(uh_name, month, response)`` row.

Unlike :func:`add_hydrograph`, this edits the row in place and leaves its
IA parameters (``dmax``/``drecov``/``dinit``) untouched. The row must
already exist. ``month``/``response`` accept the same tokens as
:func:`add_hydrograph`.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `month` (any)
- `response` (any)
- `r` (number)
- `t` (number)
- `k` (number)

---

### inflows_set_rdii_decay

- **Namespace**: inflows
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Update an existing exponential IA-decay row in place.

Same parameter meaning as :func:`add_rdii_decay`; the
``(uh_name, response)`` decay row must already exist.

**Input arguments**

- `session_id` (string)
- `uh_name` (string)
- `response` (any)
- `k_dep` (number)
- `k_0` (number)
- `k_T` (number)
- `T_ref` (number)
- `theta_rec` (number)
- `T_freeze` (number)

---

## Namespace: infrastructure

### infrastructure_add_inlet

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create a new inlet. Returns the assigned index.

``inlet_type`` is a string identifying the inlet geometry family
(e.g. ``"GRATE"``, ``"CURB"``, ``"SLOTTED"``, ``"CUSTOM"`` —
consult the engine docs for the exact set).

**Input arguments**

- `session_id` (string)
- `inlet_id` (string)
- `inlet_type` (string)

---

### infrastructure_add_lid

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Define a new LID control (not a usage).

``lid_type`` accepts a string (``bio_cell``, ``rain_garden``,
``green_roof``, ``infil_trench``, ``perm_pavement``, ``rain_barrel``,
``rooftop_disconn``, ``vegetative_swale``) or the integer code (0..7).

Distinct from ``spatial_quality.add_lid`` which is actually
``lid_usage_add`` — placing an LID instance on a subcatchment.
This tool *defines* what an LID is; the layer setters
(:func:`set_lid_surface`, :func:`set_lid_soil`, :func:`set_lid_storage`,
:func:`set_lid_drain`) configure its hydraulic behaviour. Then use
:func:`add_lid_usage` to attach instances to subcatchments.

**Input arguments**

- `session_id` (string)
- `lid_id` (string)
- `lid_type` (string)

---

### infrastructure_add_lid_usage

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Attach ``number`` instances of an LID control to a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `lid_index` (integer)
- `number` (integer)
- `area` (number)
- `width` (number)
- `init_sat` (number)
- `from_imperv` (number)

---

### infrastructure_add_street

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create a new (empty) street cross-section. Returns its index.

**Input arguments**

- `session_id` (string)
- `street_id` (string)

---

### infrastructure_add_transect

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create a new (empty) transect. Returns the assigned zero-based index.

Populate the transect with :func:`set_transect_roughness` and
:func:`add_transect_station` calls.

**Input arguments**

- `session_id` (string)
- `transect_id` (string)

---

### infrastructure_add_transect_station

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Append a single (station, elevation) point to a transect's profile.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `station` (number)
- `elevation` (number)

---

### infrastructure_clear_stations

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Remove all (station, elevation) points from a transect's profile.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_get_bank_stations

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back a transect's left/right bank station positions.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_get_comments

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the comment text attached to a transect.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_get_encroachment_stations

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back a transect's left/right encroachment station positions.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_get_lid_drain

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read LID underdrain parameters. Inverse of :func:`set_lid_drain`.

Returns ``coeff``, ``expon``, ``offset``.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)

---

### infrastructure_get_lid_drainmat

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read LID drainage-mat parameters. Inverse of :func:`set_lid_drainmat`.

Returns ``thick``, ``void_frac``, ``roughness``.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)

---

### infrastructure_get_lid_pavement

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read LID porous-pavement parameters. Inverse of :func:`set_lid_pavement`.

Returns ``thick``, ``void_ratio``, ``frac_imperv``, ``ksat``,
``clog_factor``, ``regen_days``.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)

---

### infrastructure_get_lid_soil

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read LID soil-layer parameters. Inverse of :func:`set_lid_soil`.

Returns ``thick``, ``porosity``, ``fc``, ``wp``, ``ksat``, ``kslope``.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)

---

### infrastructure_get_lid_storage

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read LID storage-layer parameters. Inverse of :func:`set_lid_storage`.

Returns ``thick``, ``void_frac``, ``ksat``.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)

---

### infrastructure_get_lid_surface

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read LID surface-layer parameters. Inverse of :func:`set_lid_surface`.

Returns ``storage``, ``roughness``, ``slope`` — the same keys
:func:`set_lid_surface` accepts.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)

---

### infrastructure_get_modifiers

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back a transect's roughness / station / elevation modifier factors.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_get_station

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back a single (station, elevation) point from a transect's profile.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `station_index` (integer)

---

### infrastructure_get_street_params

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back a street cross-section's geometric parameters.

Inverse of :func:`set_street_params`. Returns a ``params`` dict with
keys ``t_crown``, ``h_curb``, ``sx``, ``n_road``, ``gutter_depres``,
``gutter_width``, ``sides``, ``back_width``, ``back_slope``, ``back_n``.

**Input arguments**

- `session_id` (string)
- `street_index` (integer)

---

### infrastructure_get_transect_roughness

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read back the three Manning's roughness values of a transect.

Inverse of :func:`set_transect_roughness`. Returns ``n_left`` /
``n_right`` (overbank) and ``n_channel`` (main channel).

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_inlet_count

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of inlets defined in the model.

**Input arguments**

- `session_id` (string)

---

### infrastructure_lid_count

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of LID controls defined in the model.

**Input arguments**

- `session_id` (string)

---

### infrastructure_lid_usage_count

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of ``[LID_USAGE]`` placement rows across all subcatchments.

**Input arguments**

- `session_id` (string)

---

### infrastructure_lid_usage_get

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Read one ``[LID_USAGE]`` placement row by global index.

Returns the owning subcatchment/LID indices and the placement
parameters (``number``, ``area``, ``width``, ``init_sat``,
``from_imperv``, ``to_perv``, ``from_perv``).

**Input arguments**

- `session_id` (string)
- `usage_index` (integer)

---

### infrastructure_lid_usage_remove

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove one ``[LID_USAGE]`` placement row by global index.

**Input arguments**

- `session_id` (string)
- `usage_index` (integer)

---

### infrastructure_remove_transect

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove a transect by string ID or integer index.

**Input arguments**

- `session_id` (string)
- `transect` (any)

---

### infrastructure_set_bank_stations

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a transect's left/right bank station positions.

The bank stations delimit the main channel from the overbank zones
(which use the left/right roughness from :func:`set_transect_roughness`).

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `left` (number)
- `right` (number)

---

### infrastructure_set_comments

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the comment text attached to a transect.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `text` (string)

---

### infrastructure_set_encroachment_stations

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a transect's left/right encroachment station positions.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `left` (number)
- `right` (number)

---

### infrastructure_set_inlet_params

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the operational parameters for an inlet.

``grate_type`` identifies a grate-style family (e.g. ``"P_BAR-50"``);
consult the engine for the available identifiers. ``open_area`` is
the open-area fraction; ``splash_veloc`` is the splash-over velocity.

**Input arguments**

- `session_id` (string)
- `inlet_index` (integer)
- `length` (number)
- `width` (number)
- `grate_type` (string)
- `open_area` (number)
- `splash_veloc` (number)

---

### infrastructure_set_lid_drain

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set LID underdrain parameters: discharge coefficient, exponent, offset.

Drain flow follows Q = coeff * h^expon for head above offset.

**Input arguments**

- `session_id` (string)
- `lid_index` (integer)
- `coeff` (number)
- `expon` (number)
- `offset` (number)

---

### infrastructure_set_lid_drainmat

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set LID drainage-mat layer parameters (``green_roof`` LIDs).

``lid_index`` accepts a string LID ID or an integer index. The mat is
described by its thickness, void fraction, and Manning's roughness.

**Input arguments**

- `session_id` (string)
- `lid_index` (any)
- `thick` (number)
- `void_frac` (number)
- `roughness` (number)

---

### infrastructure_set_lid_pavement

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set LID porous-pavement layer parameters (``perm_pavement`` LIDs).

**Input arguments**

- `session_id` (string)
- `lid_index` (any)
- `thick` (number)
- `void_ratio` (number)
- `frac_imperv` (number)
- `ksat` (number)
- `clog_factor` (number)
- `regen_days` (number)

---

### infrastructure_set_lid_soil

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set LID soil-layer parameters.

**Input arguments**

- `session_id` (string)
- `lid_index` (integer)
- `thick` (number)
- `porosity` (number)
- `fc` (number)
- `wp` (number)
- `ksat` (number)
- `kslope` (number)

---

### infrastructure_set_lid_storage

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set LID storage-layer parameters: thickness, void fraction, k_sat.

**Input arguments**

- `session_id` (string)
- `lid_index` (integer)
- `thick` (number)
- `void_frac` (number)
- `ksat` (number)

---

### infrastructure_set_lid_surface

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set LID surface-layer parameters: storage depth, roughness, slope.

**Input arguments**

- `session_id` (string)
- `lid_index` (integer)
- `storage` (number)
- `roughness` (number)
- `slope` (number)

---

### infrastructure_set_modifiers

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a transect's modifier factors.

``n_factor`` scales roughness, ``x_factor`` scales station distances,
and ``y_factor`` scales elevations.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `n_factor` (number)
- `x_factor` (number)
- `y_factor` (number)

---

### infrastructure_set_street_params

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the full geometry of a street cross-section.

**Input arguments**

- `session_id` (string)
- `street_index` (integer)
- `t_crown` (number)
- `h_curb` (number)
- `sx` (number)
- `n_road` (number)
- `gutter_depres` (number)
- `gutter_width` (number)
- `sides` (integer)
- `back_width` (number)
- `back_slope` (number)
- `back_n` (number)

---

### infrastructure_set_transect_roughness

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set Manning's roughness values for the three transect zones.

``n_left`` and ``n_right`` are the overbank roughness; ``n_channel``
is the main channel.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)
- `n_left` (number)
- `n_right` (number)
- `n_channel` (number)

---

### infrastructure_station_count

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of (station, elevation) points in a transect's profile.

**Input arguments**

- `session_id` (string)
- `transect_index` (integer)

---

### infrastructure_street_count

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of street cross-sections in the model.

**Input arguments**

- `session_id` (string)

---

### infrastructure_transect_count

- **Namespace**: infrastructure
- **Action Group**: infrastructure
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of transects defined in the model.

**Input arguments**

- `session_id` (string)

---

## Namespace: lifecycle

### lifecycle_close_model

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Close and clean up a simulation session.

Tears down the solver (ending the run if necessary), releases all engine
resources, and removes the session from the registry.

**Input arguments**

- `session_id` (string)

---

### lifecycle_events_add

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Append a new event window (OADate decimal days).

**Input arguments**

- `session_id` (string)
- `start_oadate` (number)
- `end_oadate` (number)

---

### lifecycle_events_clear

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Remove every event window. Safe on an already-empty list.

**Input arguments**

- `session_id` (string)

---

### lifecycle_events_count

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of [EVENTS] rows in the model.

**Input arguments**

- `session_id` (string)

---

### lifecycle_events_get

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Return the start/end OADate of the I{index}-th event.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### lifecycle_events_remove

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Remove the I{index}-th event; trailing entries shift down.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### lifecycle_events_set

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Overwrite the I{index}-th event window.

**Input arguments**

- `session_id` (string)
- `index` (integer)
- `start_oadate` (number)
- `end_oadate` (number)

---

### lifecycle_get_open_diagnostics

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return validation errors and warnings recorded during a (lenient) open.

After ``open_model(..., lenient_open=True)`` the engine records post-parse
validation problems instead of raising, leaving the session in the
editable ``opened`` state. This tool reads those accumulators
(``Solver.open_errors`` / ``Solver.open_warnings``) so callers can inspect
and fix issues before initialising or editing the model. A strict open
that succeeds leaves both lists empty. New engine only.

**Input arguments**

- `session_id` (string)

---

### lifecycle_get_simulation_state

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current session and solver state.

Includes the session lifecycle state, the raw engine state code, and basic
model metadata (counts and file path).

**Input arguments**

- `session_id` (string)

---

### lifecycle_get_simulation_time

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current simulation timing information.

Includes start time, end time, current time, elapsed fraction, and the
routing timestep (seconds).

**Input arguments**

- `session_id` (string)

---

### lifecycle_get_steady_state_skip

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return whether SKIP_STEADY_STATE routing skip is enabled.

**Input arguments**

- `session_id` (string)

---

### lifecycle_is_between_events

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return whether the current sim time falls inside a defined event window.

**Input arguments**

- `session_id` (string)

---

### lifecycle_list_sessions

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

List all active simulation sessions.

Returns metadata for every session currently managed by the server.

---

### lifecycle_load_runoff_interface

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Open the runoff interface file for reading (USE mode).

The file's header is verified against the current model
(subcatchment count, pollutant count, flow units).

.. note::

   USE-mode auto-skip — making the engine bypass its own runoff
   computation when the file is open — is a follow-up to Phase 1b.
   Today's USE mode is an advanced manual feature.  After opening,
   the caller must drive the simulation **and** invoke
   ``read_runoff_step`` between :func:`step_simulation` calls
   (currently only exposed through the Python binding, not MCP).
   Most LLM workflows should prefer SAVE mode plus a downstream
   routing-only run that consumes the file via an external script.

**Input arguments**

- `session_id` (string)
- `path` (string)

---

### lifecycle_open_model

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Open a SWMM model file and initialise the engine.

Creates a new simulation session, parses the .inp file, and prepares the
engine for simulation. Returns a summary of the loaded model.

**Input arguments**

- `inp_path` (string)
- `session_id` (string)
- `rpt_path` (any)
- `out_path` (any)
- `engine` (string)
- `lenient_open` (boolean)

---

### lifecycle_run_for_steps

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Run up to *max_steps* steps using the v1 ``Solver.steps()`` iterator.

Slightly different from ``stride(max_steps)``: ``stride`` is one C
call, while ``run_for_steps`` issues the steps inside a Python loop
so progress can be reported (via ``ctx.report_progress``) every
*progress_interval* steps.  Use ``stride`` for raw speed, this one
when you want intermediate progress.

The simulation stops at whichever happens first: *max_steps* steps
completed, or the engine reaches the end of the simulation.
Auto-starts the solver if needed.

**Input arguments**

- `session_id` (string)
- `max_steps` (integer)
- `progress_interval` (integer)

---

### lifecycle_run_simulation

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Run the full simulation to completion.

Starts the solver (if not already started), steps through every timestep,
and reports progress as a percentage.  Returns continuity errors and timing.

**Input arguments**

- `session_id` (string)

---

### lifecycle_save_runoff_interface

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Open the runoff interface file for writing (SAVE mode).

Call this **before** :func:`run_simulation` (or before the first
:func:`step_simulation`).  The engine auto-emits one record per
runoff substep until the session is closed, at which point the
file is finalised automatically — there is no separate "close"
tool needed for ordinary flows.

**Input arguments**

- `session_id` (string)
- `path` (string)

---

### lifecycle_set_steady_state_skip

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Enable or disable SKIP_STEADY_STATE routing.

When enabled the engine skips routing during periods with unchanged
flows; useful for long dry-weather periods between rainfall events.

**Input arguments**

- `session_id` (string)
- `enabled` (boolean)

---

### lifecycle_step_simulation

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Advance the simulation by one or more timesteps.

Automatically starts the solver if the session is in the 'initialized'
state.  Returns the current simulation time and whether the run completed.

**Input arguments**

- `session_id` (string)
- `num_steps` (integer)

---

### lifecycle_stride

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Advance the simulation by N timesteps in a single engine call.

Faster than calling :func:`step_simulation` N times — the C engine
loops internally, so we pay one ``asyncio.to_thread`` crossing
regardless of N.

Auto-starts the solver if the session is in the ``initialized``
state.

**Input arguments**

- `session_id` (string)
- `num_steps` (integer)

---

### lifecycle_until_datetime

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Advance the simulation until the wall-clock simulation datetime reaches *target_iso*.

Maps to ``Solver.until(datetime)``.  The engine stops at the next
routing-step boundary >= the target datetime.  Auto-starts the
solver if needed.

**Input arguments**

- `session_id` (string)
- `target_iso` (string)

---

### lifecycle_until_elapsed

- **Namespace**: lifecycle
- **Action Group**: core
- **Operation Class**: SIMULATION_CONTROL
- **Destructive**: No

**Description**

Advance the simulation until at least *seconds* of sim-time have elapsed.

Maps to ``Solver.until(timedelta(seconds=seconds))``.  The engine
stops at the next routing-step boundary >= the target.  Auto-starts
the solver if needed.

**Input arguments**

- `session_id` (string)
- `seconds` (number)

---

## Namespace: links

### links_get_barrels

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of parallel barrels for a conduit.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_closed

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return whether a link is currently closed (no flow).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_control_setting

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current continuous control setting (e.g. pump speed, orifice opening).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_control_settings_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current control settings for all links as {id, index, value} records.

**Input arguments**

- `session_id` (string)

---

### links_get_crest_height

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the crest height for a weir link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_culvert_code

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the FHWA HDS-5 culvert inlet code (0 = not a culvert).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_depths_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current depths for all links.

**Input arguments**

- `session_id` (string)

---

### links_get_discharge_coeff

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the discharge coefficient (Cd) for a weir / orifice.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_end_contractions

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of end contractions on a weir (0 / 1 / 2).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_flap_gate

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return whether a conduit / orifice has a flap gate.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_flows_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current flows for all links as {id, index, value} records.

**Input arguments**

- `session_id` (string)

---

### links_get_ids_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the list of all link IDs in index order.

**Input arguments**

- `session_id` (string)

---

### links_get_loss_coeff

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the conduit's head-loss coefficients as ``(inlet, outlet, avg)``.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_orifice_open_close_rate

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the orifice open/close rate (time, in hours, to fully operate the gate).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_outlet_expon

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the outlet rating-curve exponent (functional rating types only).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_outlet_rating_type

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the outlet rating-curve classification.

``rating_type`` enum: 0=FUNCTIONAL_HEAD, 1=FUNCTIONAL_DEPTH,
2=TABULAR_HEAD, 3=TABULAR_DEPTH.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_pump_curve

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the pump-curve index for a pump link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_pump_init_state

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the initial ON/OFF state of a pump (1 = on, 0 = off).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_pump_shutoff_depth

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the wet-well depth below which the pump shuts off.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_pump_startup_depth

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the wet-well depth above which the pump starts up.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_quality

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current concentration of a pollutant in a link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `pollutant_index` (integer)

---

### links_get_quality_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return pollutant concentrations across all links for one pollutant.

**Input arguments**

- `session_id` (string)
- `pollutant_index` (integer)

---

### links_get_seep_rate

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the conduit seepage rate (depth/time).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_tag

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the link's free-form tag string (empty string when unset).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_target_setting

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the target setting (the value the link is transitioning toward).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_get_target_settings_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current target settings for all links as {id, index, value} records.

**Input arguments**

- `session_id` (string)

---

### links_get_xsect

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a link's cross-section shape plus its four geometry parameters.

``shape`` is the ``XSectShape`` enum name; ``shape_code`` is its integer
value. ``g1..g4`` are the shape-dependent geometry values (for most
closed conduits g1 is the full depth / max height).

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_hyd_power

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the current hydraulic power dissipated in a link.

Unlike the ``stat_*`` tools, ``hyd_power`` lives directly on the Link
(not under ``link.stats``) — it's the instantaneous value, not a
cumulative statistic.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_set_barrels

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the number of parallel barrels for a conduit.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `barrels` (integer)

---

### links_set_closed

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Close or open a link (binary on/off state).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `closed` (boolean)

---

### links_set_control_setting

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the control setting (typically 0..1) on a link.

Distinct from forcing.set_link_control / controls.set_link_setting only
in namespace — all three wrap the same C call. Use this when working
primarily through the links namespace.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `setting` (number)

---

### links_set_crest_height

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the weir crest height.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `crest_height` (number)

---

### links_set_culvert_code

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the FHWA HDS-5 culvert inlet code.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `culvert_code` (integer)

---

### links_set_discharge_coeff

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the discharge coefficient (Cd).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `discharge_coeff` (number)

---

### links_set_end_contractions

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the number of end contractions on a weir.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `end_contractions` (integer)

---

### links_set_flap_gate

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the flap-gate flag (prevents backflow).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `has_flap_gate` (boolean)

---

### links_set_flows_bulk

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set flows for all links from a positional array (length = link count).

**Input arguments**

- `session_id` (string)
- `flows` (any)

---

### links_set_loss_coeff

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the conduit head-loss coefficients (entrance, exit, average).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `inlet` (number)
- `outlet` (number)
- `avg` (number)

---

### links_set_orifice_open_close_rate

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the orifice open/close rate (hours to fully operate the gate).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `open_close_rate` (number)

---

### links_set_outlet_expon

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the outlet rating-curve exponent.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `expon` (number)

---

### links_set_outlet_rating_type

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the outlet rating-curve classification (integer code 0..3).

0=FUNCTIONAL_HEAD, 1=FUNCTIONAL_DEPTH, 2=TABULAR_HEAD, 3=TABULAR_DEPTH.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `rating_type` (integer)

---

### links_set_pump_curve

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a pump curve to a pump link (curve type PUMP1..PUMP4).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `curve_index` (integer)

---

### links_set_pump_init_state

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the initial ON/OFF state of a pump.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `init_on` (boolean)

---

### links_set_pump_shutoff_depth

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the wet-well depth below which the pump shuts off.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shutoff_depth` (number)

---

### links_set_pump_startup_depth

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the wet-well depth above which the pump starts up.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `startup_depth` (number)

---

### links_set_seep_rate

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the conduit seepage rate.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `seep_rate` (number)

---

### links_set_tag

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the link's free-form tag string (empty string clears it).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `tag` (string)

---

### links_set_target_setting

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the gradual-transition target setting on a link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `target` (number)

---

### links_stat_max_filling

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the peak depth/full-depth ratio (0..1+) for a conduit.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_max_flow

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the peak flow recorded for a link over the simulation.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_max_velocity

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the peak velocity for a link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_pump_cycles

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the on/off cycle count for a pump link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_pump_on_time

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return total on-time (seconds) for a pump link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_pump_volume

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return total volume pumped by a pump link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_surcharge_time

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return total surcharge duration (hours) for a link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

### links_stat_vol_flow

- **Namespace**: links
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the total volume conveyed through a link.

**Input arguments**

- `session_id` (string)
- `link_id` (any)

---

## Namespace: model

### model_add_title_line

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Append a line to the [TITLE] section.

**Input arguments**

- `session_id` (string)
- `text` (string)

---

### model_clear_title

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Remove every line from the [TITLE] section (BUILDING).

**Input arguments**

- `session_id` (string)

---

### model_file_path_get

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Read an external-file slot's resolved and original paths.

``role`` selects the slot: scalar roles ``RAINFALL``, ``RUNOFF``,
``RDII``, ``INFLOWS``, ``OUTFLOWS``, ``HOTSTART_USE``, ``CLIMATE_TEMP``
(``owner`` ignored), or vector roles ``HOTSTART_SAVE`` (owner = decimal
index), ``RAINGAGE_DATA`` (owner = gage id), ``TIMESERIES_DATA``
(owner = series id). Returns both the engine-resolved absolute path and
the original token as authored in the ``.inp``; either may be empty.

**Input arguments**

- `session_id` (string)
- `role` (string)
- `owner` (string)

---

### model_file_path_set

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the original token for an external-file slot.

Clears the cached absolute resolution (the engine re-resolves on next
use). For vector roles the ``owner`` must already exist in the model.
Pass an empty ``new_path`` to clear the slot. See ``model_file_path_get``
for the role list.

**Input arguments**

- `session_id` (string)
- `role` (string)
- `new_path` (string)
- `owner` (string)

---

### model_files_get

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the path / value for a [FILES] section field.

Common keys: ``RAINFALL_PATH``, ``RUNOFF_PATH``, ``RDII_PATH``,
``HOTSTART_USE_PATH``, ``HOTSTART_SAVE_PATH``.

**Input arguments**

- `session_id` (string)
- `key` (string)

---

### model_files_set

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a [FILES] section field. Empty value clears the field.

**Input arguments**

- `session_id` (string)
- `key` (string)
- `value` (string)

---

### model_get_crs

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the model's coordinate reference system string.

**Input arguments**

- `session_id` (string)

---

### model_get_option

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a SWMM option value as a string.

Example keys: ``FLOW_UNITS``, ``FLOW_ROUTING``, ``ROUTING_STEP``,
``REPORT_STEP``, ``SURCHARGE_METHOD``. Consult the SWMM 5 reference
for the full key list.

**Input arguments**

- `session_id` (string)
- `key` (string)

---

### model_get_option_ext

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return an extension option value (unknown to base SWMM).

**Input arguments**

- `session_id` (string)
- `key` (string)

---

### model_get_pattern_factors

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read a time pattern's type and multiplier factors.

Surfaces ``solver.patterns[...]`` — the multiplier list whose length
depends on the pattern type (12 monthly, 7 daily, 24 hourly/weekend).

**Input arguments**

- `session_id` (string)
- `pattern_id` (string)

---

### model_get_report_start

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the report start date/time as an ISO 8601 string.

Surfaces the ``report_start_datetime`` property (present on both
ModelBuilder and Solver). The report start is the instant from which
reported results begin; it may lag the simulation start.

**Input arguments**

- `session_id` (string)

---

### model_get_title

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the full [TITLE] section as a list of lines (BUILDING).

Convenience wrapper that batches get_title_count + N x get_title_line.

**Input arguments**

- `session_id` (string)

---

### model_get_title_count

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of lines in the C{[TITLE]} section (BUILDING).

**Input arguments**

- `session_id` (string)

---

### model_get_title_line

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the I{line_index}-th line of the [TITLE] section (BUILDING).

**Input arguments**

- `session_id` (string)
- `line_index` (integer)

---

### model_get_unit_system

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Report the model's flow units and unit system.

Because the engine returns every quantity in the units declared in the
``.inp`` file (project units), a client must know those units to
interpret returned magnitudes. This tool resolves ``[OPTIONS]
FLOW_UNITS`` and classifies it:

* ``flow_units`` — the raw token, e.g. ``"CFS"`` / ``"CMS"``.
* ``unit_system`` — ``"US"`` (CFS/GPM/MGD) or ``"SI"`` (CMS/LPS/MLD).

Works in BUILDING (ModelBuilder) and OPENED/RUNNING/ENDED (Solver)
states.

**Input arguments**

- `session_id` (string)

---

### model_get_userflag_bool

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a boolean user flag (application-defined metadata).

**Input arguments**

- `session_id` (string)
- `name` (string)

---

### model_get_userflag_int

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return an integer user flag.

**Input arguments**

- `session_id` (string)
- `name` (string)

---

### model_get_userflag_real

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a real-valued user flag.

**Input arguments**

- `session_id` (string)
- `name` (string)

---

### model_list_aquifers

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

List the model's ``[AQUIFERS]`` entries.

Returns ``count`` and the ordered list of aquifer ``ids``.

**Input arguments**

- `session_id` (string)

---

### model_list_snowpacks

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

List the model's ``[SNOWPACKS]`` entries.

Returns ``count`` and the ordered list of snowpack ``ids``.

**Input arguments**

- `session_id` (string)

---

### model_plugin_get

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the (path, args) of the I{index}-th plugin entry.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### model_plugin_remove

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the plugin entry matching ``path_or_id``.

**Input arguments**

- `session_id` (string)
- `path_or_id` (string)

---

### model_plugin_set

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add or update a plugin entry.

``path_or_id`` is the library path, plugin id, or ``id:version`` string.

**Input arguments**

- `session_id` (string)
- `path_or_id` (string)
- `args` (string)

---

### model_plugins_count

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of [PLUGINS] entries on the engine.

**Input arguments**

- `session_id` (string)

---

### model_set_option

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a SWMM option (string key, string value).

Accepts any key the engine's option API recognizes, including the
``FV_*`` family that configures the explicit finite-volume solver
(``FLOW_ROUTING`` = ``FV``): ``FV_CELL_LENGTH``, ``FV_MIN_CELLS``,
``FV_CFL``, ``FV_RIEMANN``, ``FV_ORDER``, ``FV_LIMITER``,
``FV_SCALAR_SCHEME``, ``FV_TIME_INTEGRATION``, ``FV_SLOT_CELERITY``,
``FV_DISPERSION``, ``FV_STRUCTURE_COUPLING``, ``FV_COMPACTION``,
``FV_BACKEND`` and ``FV_MIN_PARALLEL_CELLS``.  These are inert under
the other routing models rather than rejected, so they can be set
before ``FLOW_ROUTING`` is switched.

Note that finite-volume routing needs a resolved mesh to reproduce
dynamic-wave peak flows -- set ``FV_CELL_LENGTH`` rather than leaving
it at the one-cell-per-conduit default when peaks matter.

**Input arguments**

- `session_id` (string)
- `key` (string)
- `value` (string)

---

### model_set_option_ext

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set an extension option.

**Input arguments**

- `session_id` (string)
- `key` (string)
- `value` (string)

---

### model_set_report_start

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the report start date/time from an ISO 8601 string.

``report_start`` is parsed with :meth:`datetime.datetime.fromisoformat`
(e.g. ``"1998-01-01T00:00:00"`` or ``"1998-01-01 00:00:00"``).

**Input arguments**

- `session_id` (string)
- `report_start` (string)

---

### model_set_title

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Replace all [TITLE] lines with new text (newline-separated, BUILDING).

**Input arguments**

- `session_id` (string)
- `text` (string)

---

### model_set_userflag_bool

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a boolean user flag.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `value` (boolean)

---

### model_set_userflag_int

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set an integer user flag.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `value` (integer)

---

### model_set_userflag_real

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a real-valued user flag.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `value` (number)

---

### model_userflag_clear_value

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the flag value assigned to a specific object (idempotent).

**Input arguments**

- `session_id` (string)
- `obj_type` (string)
- `obj_name` (string)
- `flag_name` (string)

---

### model_userflag_define

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Define (or redefine) a user-flag schema entry ([USER_FLAGS]).

``flag_type`` is ``"BOOLEAN"``, ``"INTEGER"``, ``"REAL"``, or
``"STRING"``. The name is stored uppercase. Redefining an existing
name overwrites its definition; previously assigned per-object values
are kept as-is.

**Input arguments**

- `session_id` (string)
- `name` (string)
- `flag_type` (string)
- `description` (string)

---

### model_userflag_get_value

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the flag value assigned to a specific object ([USER_FLAG_VALUES]).

``obj_type`` is an object type token (e.g. ``"NODE"``, ``"LINK"``,
``"SUBCATCHMENT"``). The value is returned in its INP string form
(BOOLEAN as YES/NO, INTEGER/REAL as decimals, STRING verbatim);
``value`` is ``None`` and ``assigned`` is ``False`` when unset.

**Input arguments**

- `session_id` (string)
- `obj_type` (string)
- `obj_name` (string)
- `flag_name` (string)

---

### model_userflag_list_defs

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

List every user-flag schema definition ([USER_FLAGS]), in insertion order.

Each entry reports ``name``, ``flag_type`` (BOOLEAN / INTEGER / REAL /
STRING), and ``description``.

**Input arguments**

- `session_id` (string)

---

### model_userflag_set_value

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a flag value to a specific object from a string.

The flag must already be defined (see ``model_userflag_define``); its
declared type drives parsing. BOOLEAN accepts YES/NO/TRUE/FALSE/1/0;
INTEGER a decimal integer; REAL a decimal number; STRING is stored
verbatim.

**Input arguments**

- `session_id` (string)
- `obj_type` (string)
- `obj_name` (string)
- `flag_name` (string)
- `value` (string)

---

### model_userflag_undefine

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove a user-flag definition and all per-object values assigned to it.

**Input arguments**

- `session_id` (string)
- `name` (string)

---

### model_write_with_plugin

- **Namespace**: model
- **Action Group**: core
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Write the model to disk via an output plugin (or built-in writer).

Pass an empty ``output_plugin_id`` (the default) to use the built-in
`.inp` writer. Non-empty values select a registered output plugin
(e.g. GeoPackage / HDF5).

**Input arguments**

- `session_id` (string)
- `path` (string)
- `output_plugin_id` (string)

---

## Namespace: nodes

### nodes_depth_from_volume

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Compute the depth corresponding to a given storage volume.

Inverts the storage curve / functional relationship for a storage node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `volume` (number)

---

### nodes_get_depths_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current depths for all nodes as a list of {id, index, value}.

**Input arguments**

- `session_id` (string)

---

### nodes_get_divider_type

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the divider rule type for a divider node.

``divider_type`` enum: 0=CUTOFF, 1=OVERFLOW, 2=TABULAR, 3=WEIR.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_exfil_params

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return Green-Ampt exfiltration params ``(suction, ksat, imd)`` for a storage node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_heads_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current heads for all nodes as a list of {id, index, value}.

**Input arguments**

- `session_id` (string)

---

### nodes_get_ids_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the IDs of all nodes in storage order as ``{count, ids}``.

**Input arguments**

- `session_id` (string)

---

### nodes_get_inflows_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current total inflows for all nodes.

**Input arguments**

- `session_id` (string)

---

### nodes_get_outfall_flap_gate

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return whether an outfall has a flap gate (prevents backflow).

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_outfall_param

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the outfall parameter value (fixed stage or computed param).

Meaning depends on the outfall type: for FIXED it's the stage
elevation; for TIDAL / TIMESERIES it's an index into a curve / series.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_outfall_route_to

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the subcatchment index outfall discharge is routed to (-1 = none).

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_outfall_tidal

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the tidal-curve index assigned to a TIDAL outfall.

Read-back of the curve set via ``set_outfall_tidal``.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_outfall_timeseries

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the stage-time-series index assigned to a TIMESERIES outfall.

Read-back of the series set via ``set_outfall_timeseries``.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_outfall_type

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the outfall boundary type code for an outfall node.

``outfall_type`` enum: 0=FREE, 1=NORMAL, 2=FIXED, 3=TIDAL, 4=TIMESERIES.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_overflows_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current overflow rates for all nodes.

**Input arguments**

- `session_id` (string)

---

### nodes_get_quality

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current concentration of a pollutant at a node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `pollutant_index` (integer)

---

### nodes_get_quality_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return pollutant concentrations at all nodes for one pollutant.

``pollutant_index`` is a 0-based pollutant index (see
``query.get_pollutant_info`` or ``analysis.output_pollutant_count``).

**Input arguments**

- `session_id` (string)
- `pollutant_index` (integer)

---

### nodes_get_storage_curve

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the storage-curve index assigned to a storage node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_storage_functional

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return functional storage params ``(a, b, c)`` for a storage node.

Functional form: ``area = a * depth^b + c``.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_storage_geometry

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a storage node's surface-area relation and its raw dimensions.

``shape`` is the engine's ``StorageShape``: ``tabular`` (curve, see
``get_storage_curve``), ``functional`` (``a``/``b``/``c``, see
``get_storage_functional``), or one of the four *geometric* shapes, whose
three raw dimensions ``p1``/``p2``/``p3`` this tool returns:

* ``cylindrical`` — p1 = major axis, p2 = minor axis.
* ``conical`` — p1, p2 = base axes, p3 = side slope.
* ``paraboloid`` — p1, p2 = top axes, p3 = height.
* ``pyramidal`` — p1 = length, p2 = width, p3 = side slope.

``p1``/``p2``/``p3`` are zero for a non-geometric shape.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_storage_seep_rate

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the seepage rate for a storage node (depth/time).

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_get_tag

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the free-form tag string for a node (empty if untagged).

Tags come from the INP ``[TAGS]`` section, are keyed by index, and
persist across ``rename``.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_is_virtual

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

Report whether a node is a virtual junction.

A virtual junction is a zero-storage, momentum-transmitting JUNCTION
connecting exactly two conduits of identical cross-section (INP
``[VIRTUAL_JUNCTIONS]``). Use ``virtual_eligible`` to test whether a
non-virtual node could be converted.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_set_depths_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set depths for all nodes from an array (length must equal node count).

Use case: initialize a hot-start or override an entire depth field
before a step. The array is positional — index ``i`` maps to node
``i`` in storage order (see ``query.list_nodes`` for the canonical
order).

**Input arguments**

- `session_id` (string)
- `depths` (any)

---

### nodes_set_divider_type

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the divider rule type for a divider node.

``divider_type``: ``cutoff`` / ``overflow`` / ``tabular`` / ``weir`` or
the integer code (0..3).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `divider_type` (string)

---

### nodes_set_exfil_params

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set Green-Ampt exfiltration params for a storage node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `suction` (number)
- `ksat` (number)
- `imd` (number)

---

### nodes_set_head_boundary

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Apply a one-shot head boundary value at a node for the current step.

Runs against the running simulation; the value applies to the next
routing step only (it is not persistent).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `head` (number)

---

### nodes_set_lat_inflows_bulk

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set lateral inflows for all nodes from an array.

Positional, length must equal node count.

**Input arguments**

- `session_id` (string)
- `inflows` (any)

---

### nodes_set_outfall_flap_gate

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set whether an outfall has a flap gate.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `has_gate` (boolean)

---

### nodes_set_outfall_route_to

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Route outfall discharge to a subcatchment (``-1`` = none).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `subcatch_index` (integer)

---

### nodes_set_outfall_stage

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the fixed stage elevation for a FIXED outfall.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `stage` (number)

---

### nodes_set_outfall_tidal

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a tidal curve to a TIDAL outfall (hour-of-day vs stage).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `curve_index` (integer)

---

### nodes_set_outfall_timeseries

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a time series to a TIMESERIES outfall (time vs stage).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `timeseries_index` (integer)

---

### nodes_set_outfall_type

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the outfall boundary type for an outfall node.

``outfall_type``: ``free`` / ``normal`` / ``fixed`` / ``tidal`` /
``timeseries`` or the integer code (0..4).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `outfall_type` (string)

---

### nodes_set_quality_mass_flux

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Inject a persistent pollutant mass flux at a node (mass/sec).

Runs against the running simulation; persists until cleared.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `pollutant_index` (integer)
- `mass_flux` (number)

---

### nodes_set_storage_curve

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a storage curve to a storage node.

``curve_index`` references a curve defined via ``tables.add_curve``
(with ``curve_type='storage'``).

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `curve_index` (integer)

---

### nodes_set_storage_functional

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set functional storage params ``area = a * depth^b + c``.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `a` (number)
- `b` (number)
- `c` (number)

---

### nodes_set_storage_geometry

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a storage node's geometric surface-area relation.

When ``shape`` is given it is applied first — which detaches any storage
curve and re-derives the internal area coefficients — then ``p1``/``p2``/
``p3`` are supplied. Leave ``shape`` empty to redimension the node's
current shape. See ``get_storage_geometry`` for the per-shape meaning of
the three dimensions.

Valid shapes here are the geometric ones: ``cylindrical``, ``conical``,
``paraboloid``, ``pyramidal``. Use ``set_storage_curve`` for ``tabular``
and ``set_storage_functional`` for ``functional``.

The engine requires p1 > 0, p2 > 0, p3 >= 0, and p3 != 0 for
``paraboloid``.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `shape` (string)
- `p1` (number)
- `p2` (number)
- `p3` (number)

---

### nodes_set_storage_seep_rate

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the seepage rate for a storage node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `rate` (number)

---

### nodes_set_tag

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set (or clear) the free-form tag string for a node.

An empty string clears the tag.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `tag` (string)

---

### nodes_stat_max_depth

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the peak depth recorded for a node over the simulation.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_stat_max_overflow

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the peak overflow rate for a node over the simulation.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_stat_time_flooded

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the total flooded duration (hours) for a node.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_stat_vol_flooded

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the total flooded volume for a node over the simulation.

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

### nodes_virtual_eligible

- **Namespace**: nodes
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Dry-run check of the virtual-junction usage rules for a node.

Read-only; nothing is changed. ``eligible`` is ``True`` (``rule_code`` 0)
when the node satisfies every structural rule — exactly two attached
conduits of identical cross-section, zero offsets, no lateral inflow
sources, dynamic-wave routing — so converting it would succeed. Otherwise
``rule_code`` is the distinct ERR_VJ_* code identifying the violated rule
(609 = not exactly two conduits, 611 = cross-section mismatch, 613 =
nonzero offset, 617 = a lateral inflow source targets the node).

**Input arguments**

- `session_id` (string)
- `node_id` (any)

---

## Namespace: pollutants

### pollutants_add

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a new pollutant to the model (BUILDING state).

``units``: ``mg_per_l`` (0), ``ug_per_l`` (1), or ``count_per_l`` (2).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (string)
- `units` (string)

---

### pollutants_count

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of pollutants defined in the model.

**Input arguments**

- `session_id` (string)

---

### pollutants_get_co_pollutant

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the co-pollutant index assigned to this pollutant (-1 = none).

v1 surfaces co-pollutant as an optional ``(Pollutant, fraction)`` tuple;
we project that down to the legacy ``(index, fraction)`` shape so the
JSON contract is preserved (with ``fraction`` exposed as a new field).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_dwf_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the concentration of this pollutant in dry-weather flow.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_gw_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the concentration of this pollutant in groundwater.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_init_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the initial concentration throughout the system.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_kdecay

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the first-order decay coefficient (1/day) for a pollutant.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_mwt

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the molecular weight of a pollutant (g/mol).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_rain_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the concentration of this pollutant in rainfall.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_rdii_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the concentration of this pollutant in RDII.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_snow_only

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the snow-only flag for a pollutant (True = transported only in snow).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_get_units

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the concentration units for a pollutant (mg/L / ug/L / #/L).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### pollutants_set_co_pollutant

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a co-pollutant (set ``co_pollutant_index`` to ``-1`` to clear).

v1 requires a fraction alongside the co-pollutant.  Defaults to ``1.0``
so callers that previously only supplied an index see the same effective
behaviour.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `co_pollutant_index` (integer)
- `fraction` (number)

---

### pollutants_set_dwf_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the dry-weather-flow concentration.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `dwf_conc` (number)

---

### pollutants_set_gw_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the groundwater concentration.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `gw_conc` (number)

---

### pollutants_set_init_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the initial system-wide concentration.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `init_conc` (number)

---

### pollutants_set_kdecay

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the first-order decay coefficient (1/day).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `kdecay` (number)

---

### pollutants_set_link_quality

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Override a link's pollutant concentration mid-simulation.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `pollutant_id` (any)
- `concentration` (number)

---

### pollutants_set_mwt

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the molecular weight (g/mol).

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `molecular_weight` (number)

---

### pollutants_set_node_quality

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Override a node's pollutant concentration mid-simulation.

Runs against the running simulation. Pass the node_id (string) and the
pollutant_id (string or int index); the value is the override
concentration in the pollutant's units.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `pollutant_id` (any)
- `concentration` (number)

---

### pollutants_set_rain_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the rainfall concentration.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `rain_conc` (number)

---

### pollutants_set_rdii_conc

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the RDII concentration.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `rdii_conc` (number)

---

### pollutants_set_snow_only

- **Namespace**: pollutants
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the snow-only flag for a pollutant.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)
- `snow_only` (boolean)

---

## Namespace: quality

### quality_buildup_get

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the buildup function parameters for a (landuse, pollutant) pair.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)
- `pollutant_id` (any)

---

### quality_buildup_set

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the buildup function for a (landuse, pollutant) pair.

``function``: ``none`` / ``power`` / ``exponential`` / ``saturation`` /
``external``. ``normalizer``: ``per_area`` / ``per_curb``.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)
- `pollutant_id` (any)
- `function` (string)
- `c1` (number)
- `c2` (number)
- `c3` (number)
- `normalizer` (string)

---

### quality_get_sweep_interval

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the days-between-street-sweeps for a landuse.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)

---

### quality_get_sweep_removal

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the sweep removal fraction (0..1) for a landuse.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)

---

### quality_landuse_add

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a new landuse to the model (BUILDING state).

**Input arguments**

- `session_id` (string)
- `landuse_id` (string)

---

### quality_landuse_count

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of landuses defined in the model.

**Input arguments**

- `session_id` (string)

---

### quality_landuse_id

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the string id of the I{index}-th landuse.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### quality_landuse_index

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the integer index for a landuse string id (-1 if not found).

**Input arguments**

- `session_id` (string)
- `landuse_id` (string)

---

### quality_set_sweep_interval

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the days-between-street-sweeps for a landuse.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)
- `days` (number)

---

### quality_set_sweep_removal

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the sweep removal fraction for a landuse (must be in [0, 1]).

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)
- `fraction` (number)

---

### quality_treatment_clear

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove the treatment expression for a (node, pollutant) pair.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `pollutant_id` (any)

---

### quality_treatment_get

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the treatment expression text for a (node, pollutant) pair.

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `pollutant_id` (any)

---

### quality_treatment_validate_expression

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Check a treatment expression parses, without writing it to the model.

Nothing in the engine is modified. Call this before
``spatial_set_treatment`` so a malformed expression is caught here rather
than surfacing much later as an opaque run-time error.

Returns ``valid``; when ``False``, ``message`` is the engine's diagnostic
and ``column`` is the 0-based character offset in ``expression`` where the
parse failed (``-1`` when the failure is not attributable to a position).

**Input arguments**

- `session_id` (string)
- `expression` (string)

---

### quality_washoff_get

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the washoff function parameters for a (landuse, pollutant) pair.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)
- `pollutant_id` (any)

---

### quality_washoff_set

- **Namespace**: quality
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the washoff function for a (landuse, pollutant) pair.

``function``: ``exponential`` / ``rating_curve`` / ``event_mean_conc``.

**Input arguments**

- `session_id` (string)
- `landuse_id` (any)
- `pollutant_id` (any)
- `function` (string)
- `c1` (number)
- `c2` (number)
- `sweep_efficiency` (number)
- `bmp_efficiency` (number)

---

## Namespace: query

### query_find_elements

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Search for model elements by ID pattern and/or type.

*pattern* is a Python regex matched against element IDs (case-insensitive).
*element_type* restricts the search to ``"node"``, ``"link"``,
``"subcatchment"``, or ``"gage"``.  Both are optional; when neither is
given all elements are returned.

**Input arguments**

- `session_id` (string)
- `pattern` (any)
- `element_type` (any)

---

### query_get_gage_info

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return properties and state for one or all rain gages.

When *gage_id* is given, returns a single GageInfo.  When omitted,
returns a list of GageInfo for every rain gage in the model.

**Input arguments**

- `session_id` (string)
- `gage_id` (any)

---

### query_get_link_info

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return properties and state for one or all links.

When *link_id* is given, returns a single :class:`LinkInfo`. When
omitted, returns a list of :class:`LinkInfo` for every link in the
model.

Phase 4d adds ``start_index`` / ``limit`` for paginated reads of the
all-mode response, mirroring :func:`get_node_info`.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `start_index` (integer)
- `limit` (any)

---

### query_get_node_info

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return properties and state for one or all nodes.

When *node_id* is given, returns a single :class:`NodeInfo`. When
omitted, returns a list of :class:`NodeInfo` for every node in the
model.  The optional *properties* list filters which fields are
included (not yet implemented; reserved for future optimisation).

Phase 4d adds ``start_index`` and ``limit`` for paginated reads of
the all-mode response.  Both default to "no pagination" (return
every node).  Pagination is applied **after** the bulk fetch — the
underlying engine still does one pass over the entire network
regardless of slice — so callers can safely make many small paged
calls without re-paying the bulk-fetch cost beyond the per-call
Python-side slice.

**Input arguments**

- `session_id` (string)
- `node_id` (any)
- `properties` (any)
- `start_index` (integer)
- `limit` (any)

---

### query_get_pollutant_info

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return definition and properties for one or all pollutants.

When *pollutant_id* is given, returns a single PollutantInfo.  When
omitted, returns a list of PollutantInfo for every pollutant in the model.
Valid in any non-closed session state.

**Input arguments**

- `session_id` (string)
- `pollutant_id` (any)

---

### query_get_subcatchment_info

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return properties and state for one or all subcatchments.

When *subcatch_id* is given, returns a single SubcatchmentInfo.  When
omitted, returns a list of SubcatchmentInfo for every subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### query_get_system_summary

- **Namespace**: query
- **Action Group**: results
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return a full system summary including counts, options, and timing.

Provides an overview of the loaded model's configuration and, if a
simulation is running or has ended, the current simulation time.

**Input arguments**

- `session_id` (string)

---

## Namespace: spatial

### spatial_add_lid

- **Namespace**: spatial
- **Action Group**: infrastructure
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a Low Impact Development (LID) control to a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `lid_idx` (integer)
- `number` (integer)
- `area` (number)
- `width` (number)
- `init_sat` (number)
- `from_imperv` (number)

---

### spatial_get_all_coordinates

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return coordinates for **all** elements of a given type in one call.

This is much faster than calling :func:`get_coordinates` in a loop.
For nodes, a single C-level bulk read (memcpy) is used.  For links,
subcatchments, and gages, all per-element reads are batched inside a
single thread call to avoid per-element async overhead.

Returns a list of ``{"id": "...", "x": ..., "y": ...}`` records, one per
element, in index order.

**Input arguments**

- `session_id` (string)
- `element_type` (string)

---

### spatial_get_all_polygons

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the boundary polygon for **all** subcatchments in one call.

Each record contains the subcatchment ID, its centroid, and its full
polygon vertex list.  All reads are batched inside a single thread to
avoid per-subcatchment async overhead.

Returns a list of records::

    {"id": "S1", "centroid": [x, y], "vertex_count": 6,
     "polygon": [[x0,y0], ..., [x5,y5]]}

Subcatchments with no polygon geometry return ``"polygon": []``.

**Input arguments**

- `session_id` (string)

---

### spatial_get_all_vertices

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the polyline vertices for **all** links in one call.

Each link entry contains its full ordered polyline (upstream endpoint,
any interior shape-points, downstream endpoint).  All reads are batched
inside a single thread to avoid per-link async overhead.

Returns a list of records::

    {"id": "C1", "vertex_count": 3, "vertices": [[x0,y0], [x1,y1], [x2,y2]]}

Links with no stored geometry return ``"vertices": []``.

**Input arguments**

- `session_id` (string)

---

### spatial_get_coordinates

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Retrieve the spatial coordinates for a model element.

Supports nodes (x, y), links (x, y centroid), and subcatchments (x, y
centroid) depending on the data stored in the model.

**Input arguments**

- `session_id` (string)
- `element_type` (string)
- `element_id` (string)

---

### spatial_get_crs

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the coordinate reference system (CRS) string for the model.

The CRS is stored as a string such as an EPSG code (e.g. ``EPSG:4326``),
a PROJ string, or a WKT string.  An empty string means no CRS has been
assigned.

**Input arguments**

- `session_id` (string)

---

### spatial_get_model_geometry

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return complete geometry for the entire model in a single call.

This is the primary endpoint for rendering a SWMM model.  It returns all
spatial data needed to draw nodes, links (pipes/channels), subcatchments
(watersheds), and rain gages — plus the model CRS and bounding box.

All data is fetched with minimal thread hops:

- **Nodes** use a single C-level bulk memcpy for coordinates.
- **Links**, **subcatchments**, and **gages** batch all per-element reads
  inside one thread call each.

Response structure::

    {
      "session_id": "default",
      "crs": "EPSG:4326",
      "bounds": {"min_x": ..., "min_y": ..., "max_x": ..., "max_y": ...},
      "nodes": [
        {"id": "J1", "type": 0, "type_name": "JUNCTION", "x": 0.0, "y": 0.0}
      ],
      "links": [
        {"id": "C1", "type": 0, "type_name": "CONDUIT",
         "from_node": "J1", "to_node": "J2",
         "vertices": [[x0,y0], [x1,y1], ...]}
      ],
      "subcatchments": [
        {"id": "S1", "centroid": [x, y],
         "polygon": [[x0,y0], ...], "outlet_node_idx": 0}
      ],
      "gages": [
        {"id": "RG1", "x": 0.0, "y": 0.0}
      ]
    }

**Input arguments**

- `session_id` (string)

---

### spatial_get_polygon

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the polygon vertices of a subcatchment (watershed boundary).

Vertices define the closed boundary polygon of the subcatchment in model
coordinates.  An empty list means no polygon geometry has been assigned.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)

---

### spatial_get_quality

- **Namespace**: spatial
- **Action Group**: water-quality
- **Operation Class**: READ
- **Destructive**: No

**Description**

Retrieve water-quality concentrations for a model element.

When *pollutant* is ``None`` all tracked pollutants are returned;
otherwise only the named pollutant's concentration is included.

**Input arguments**

- `session_id` (string)
- `element_type` (string)
- `element_id` (string)
- `pollutant` (any)

---

### spatial_get_vertices

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the ordered polyline vertices for a link (pipe or channel).

Vertices are returned in upstream-to-downstream order.  For conduits with
no interior vertices only the two endpoint coordinates (from the connected
nodes) are returned.

**Input arguments**

- `session_id` (string)
- `link_id` (string)

---

### spatial_set_coordinates

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the spatial coordinates for a model element.

**Input arguments**

- `session_id` (string)
- `element_type` (string)
- `element_id` (string)
- `x` (number)
- `y` (number)

---

### spatial_set_crs

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the coordinate reference system (CRS) string for the model.

**Input arguments**

- `session_id` (string)
- `crs` (string)

---

### spatial_set_gage_coord

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the (x, y) symbol coordinates of a rain gage.

Complements :func:`get_all_coordinates` (which reads gage coordinates
via ``element_type="gage"``).  The element-keyed :func:`set_coordinates`
tool handles nodes / links / subcatchments only; this is the dedicated
gage-coordinate setter.

**Input arguments**

- `session_id` (string)
- `gage_id` (string)
- `x` (number)
- `y` (number)

---

### spatial_set_node_coords_bulk

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set **all** node coordinates in one bulk call.

The inverse of reading node coordinates via :func:`get_all_coordinates`
(``element_type="node"``).  *coordinates* must be a list of ``[x, y]``
pairs in node-index order, one per node in the model; a single C-level
bulk write (memcpy) replaces every node's coordinates at once.

**Input arguments**

- `session_id` (string)
- `coordinates` (array)

---

### spatial_set_polygon

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the polygon boundary of a subcatchment (watershed).

Replaces any existing polygon geometry.  Each entry in *polygon* must be
a two-element list ``[x, y]``.  Pass an empty list to clear the polygon.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (string)
- `polygon` (array)

---

### spatial_set_treatment

- **Namespace**: spatial
- **Action Group**: water-quality
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign a treatment expression to a node for a given pollutant.

Treatment expressions use SWMM's built-in syntax (e.g.
``"R = 0.5 * C"`` to remove 50 % of concentration *C*).

**Input arguments**

- `session_id` (string)
- `node_id` (string)
- `pollutant` (string)
- `expression` (string)

---

### spatial_set_vertices

- **Namespace**: spatial
- **Action Group**: spatial
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the ordered polyline vertices for a link.

Replaces any existing interior vertices.  Each entry in *vertices* must
be a two-element list ``[x, y]``.  Pass an empty list to clear all
interior vertices.

**Input arguments**

- `session_id` (string)
- `link_id` (string)
- `vertices` (array)

---

## Namespace: subcatchments

### subcatchments_aquifer_add

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a new ``[AQUIFERS]`` entry with default parameters.

Returns the new aquifer's zero-based index. Configure it with
``aquifer_set_param`` / ``aquifer_set_evap_pattern``, then attach it to a
subcatchment with ``set_aquifer``.

**Input arguments**

- `session_id` (string)
- `aquifer_id` (string)

---

### subcatchments_aquifer_get_evap_pattern

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return an aquifer's upper-zone evaporation pattern name (empty if none).

The trailing ``ETupat`` column of the ``[AQUIFERS]`` line — a MONTHLY
``[PATTERNS]`` name scaling the upper-zone evaporation fraction. The 12
numeric columns are reached via ``aquifer_get_param``.

**Input arguments**

- `session_id` (string)
- `aquifer_id` (any)

---

### subcatchments_aquifer_get_param

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return an aquifer parameter value (input-file units).

``aquifer_id`` is an aquifer name or index (``[AQUIFERS]`` section).
``param`` is one of: porosity, wilting_point, field_capacity,
conductivity, conduct_slope, tension_slope, upper_evap_frac,
lower_evap_depth, lower_loss_coeff, bottom_elev, water_table_elev,
upper_moisture (or the integer code 0..11).

**Input arguments**

- `session_id` (string)
- `aquifer_id` (any)
- `param` (any)

---

### subcatchments_aquifer_id

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the string id of the ``index``-th aquifer.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### subcatchments_aquifer_set_evap_pattern

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set (or clear) an aquifer's upper-zone evaporation pattern.

``pattern_id`` is a MONTHLY ``[PATTERNS]`` name; an empty string clears
it. Pre-start-only — the engine raises while the simulation is running.

**Input arguments**

- `session_id` (string)
- `aquifer_id` (any)
- `pattern_id` (string)

---

### subcatchments_aquifer_set_param

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set an aquifer parameter value (input-file units).

``aquifer_id`` is an aquifer name or index. ``param`` accepts the same
tokens as ``aquifer_get_param``. Flux-coefficient parameters take effect
on the next step mid-run; structural / initial-condition parameters are
pre-start-only and the engine raises while the simulation is running.

**Input arguments**

- `session_id` (string)
- `aquifer_id` (any)
- `param` (any)
- `value` (number)

---

### subcatchments_get_aquifer

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the aquifer index assigned to a subcatchment (-1 if none).

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_coverage

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the land-use coverage fraction (0..1) for a (subcatch, landuse) pair.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `landuse_index` (integer)

---

### subcatchments_get_coverages

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return every land-use coverage for a subcatchment in one call.

Bulk peer of ``get_coverage``: ``coverages[i]`` is the coverage of
land-use index ``i``, in PERCENT (0-100) as stored in the INP
``[COVERAGES]`` section. Resolve the land-use names with
``quality_landuse_id``.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_evap

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current evaporation rate for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_groundwater

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current groundwater flow for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_gw_node

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the node index receiving a subcatchment's groundwater (-1 if none).

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_gw_params

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the ``[GROUNDWATER]`` flow parameters for a subcatchment.

Keys: ``surf_elev``, ``a1``, ``b1``, ``a2``, ``b2``, ``a3``, ``tw``,
``hstar``. The subcatchment must have an aquifer assigned.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_ids_bulk

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the IDs of all subcatchments in storage order as ``{count, ids}``.

**Input arguments**

- `session_id` (string)

---

### subcatchments_get_infil

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current infiltration rate for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_infil_curve_number

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the SCS Curve Number and drying time for a subcatchment.

``drying_time`` is the third ``[INFILTRATION]`` column -- days for a fully
saturated soil to dry -- and is what ``set_infil_curve_number`` preserves
when it is not given one.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_infil_green_ampt

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return Green-Ampt params ``(suction, conductivity, initial_deficit)``.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_infil_horton

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return Horton infiltration params ``(f0, fmin, decay, dry_time)``.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_infil_model

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the infiltration model type for a subcatchment.

Model codes: 0=HORTON, 1=MOD_HORTON, 2=GREEN_AMPT, 3=MOD_GREEN_AMPT,
4=CURVE_NUMBER.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_initial_loading

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the ``[LOADINGS]`` initial pollutant buildup on a subcatchment.

The mass per unit area present at simulation start (0.0 when unset),
which overrides the DRY_DAYS-derived buildup. ``pollutant_id`` is a
pollutant name or index.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `pollutant_id` (any)

---

### subcatchments_get_ponded_quality

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the ponded pollutant mass on a subcatchment surface.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `pollutant_index` (integer)

---

### subcatchments_get_quality

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the runoff pollutant concentration for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `pollutant_index` (integer)

---

### subcatchments_get_quality_bulk

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return pollutant concentrations across all subcatchments for one pollutant.

**Input arguments**

- `session_id` (string)
- `pollutant_index` (integer)

---

### subcatchments_get_rainfall

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current rainfall rate for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_runoff

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current runoff rate for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_runoff_bulk

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return current runoff rates for all subcatchments.

**Input arguments**

- `session_id` (string)

---

### subcatchments_get_snow_depth

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current snow depth on a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_tag

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the free-form tag string for a subcatchment (empty if untagged).

Tags come from the INP ``[TAGS]`` section and are keyed by index.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_get_zero_imperv_pct

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the ``[SUBAREAS] PctZero`` value for a subcatchment.

The percentage (0-100) of the impervious area that has no depression
storage.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_set_aquifer

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Assign (or detach) the aquifer for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `aquifer` (any)

---

### subcatchments_set_coverage

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the land-use coverage fraction (0..1) for a (subcatch, landuse) pair.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `landuse_index` (integer)
- `fraction` (number)

---

### subcatchments_set_gw_node

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set (or detach) the node receiving a subcatchment's groundwater flow.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `node` (any)

---

### subcatchments_set_gw_params

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the ``[GROUNDWATER]`` flow parameters for a subcatchment.

Token order matches the INP ``[GROUNDWATER]`` section. The subcatchment
must have an aquifer assigned.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `surf_elev` (number)
- `a1` (number)
- `b1` (number)
- `a2` (number)
- `b2` (number)
- `a3` (number)
- `tw` (number)
- `hstar` (number)

---

### subcatchments_set_gw_state

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Inject the groundwater state on a subcatchment (running only).

Overwrites the live upper-zone moisture and/or saturated-zone depth so a
caller can warm-start or perturb groundwater mid-run. Pass a negative
value to leave that field unchanged.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `theta` (number)
- `lower_depth` (number)

---

### subcatchments_set_infil_curve_number

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the SCS Curve Number for a subcatchment.

The engine writes both ``[INFILTRATION]`` columns in one call. Leave
``drying_time`` unset to keep the subcatchment's current value and change
only the curve number.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `curve_number` (number)
- `drying_time` (any)

---

### subcatchments_set_infil_green_ampt

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set Green-Ampt infiltration params for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `suction` (number)
- `conductivity` (number)
- `initial_deficit` (number)

---

### subcatchments_set_infil_horton

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set Horton infiltration params for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `f0` (number)
- `fmin` (number)
- `decay` (number)
- `dry_time` (number)

---

### subcatchments_set_infil_model

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Switch the active infiltration model for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `model` (integer)

---

### subcatchments_set_initial_loading

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the ``[LOADINGS]`` initial pollutant buildup on a subcatchment.

``initial_loading`` is the buildup mass per unit area present at
simulation start. ``pollutant_id`` is a pollutant name or index.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `pollutant_id` (any)
- `initial_loading` (number)

---

### subcatchments_set_outlet_subcatchment

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Route a subcatchment's runoff to another subcatchment.

``outlet_subcatch_id`` is the receiving subcatchment's name or index.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `outlet_subcatch_id` (any)

---

### subcatchments_set_ponded_quality

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the ponded pollutant mass on a subcatchment surface.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `pollutant_index` (integer)
- `ponded_mass` (number)

---

### subcatchments_set_snow_state

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Inject the snow-pack state on one snow surface (running only).

Overwrites the live snow-pack state on a single snow subarea so a caller
can warm-start or perturb the snowpack mid-run. Pass the documented
sentinel (negative for depths, -1000 for ATI) to leave a field unchanged.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `surface` (integer)
- `swe` (number)
- `free_water` (number)
- `ati` (number)
- `cold_content` (number)

---

### subcatchments_set_tag

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set (or clear) the free-form tag string for a subcatchment.

An empty string clears the tag.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `tag` (string)

---

### subcatchments_set_zero_imperv_pct

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the ``[SUBAREAS] PctZero`` value for a subcatchment.

``pct`` is the percentage (0-100) of the impervious area having no
depression storage.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)
- `pct` (number)

---

### subcatchments_snowpack_add

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Add a new ``[SNOWPACKS]`` definition with zeroed parameters.

Returns the new snowpack's zero-based index. Configure the three
snow-melt surfaces with ``snowpack_set_surface`` and the redistribution
row with ``snowpack_set_removal``.

**Input arguments**

- `session_id` (string)
- `snowpack_id` (string)

---

### subcatchments_snowpack_count

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of ``[SNOWPACKS]`` definitions in the model.

**Input arguments**

- `session_id` (string)

---

### subcatchments_snowpack_get_removal

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Read a snowpack's REMOVAL row (snow redistribution fractions).

**Input arguments**

- `session_id` (string)
- `snowpack_id` (any)

---

### subcatchments_snowpack_get_removal_subcatch

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the destination subcatchment for a snowpack's ``fsubcatch``
removal fraction (empty if none).

**Input arguments**

- `session_id` (string)
- `snowpack_id` (any)

---

### subcatchments_snowpack_get_surface

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Read one snow-melt surface of a snowpack definition.

``surface`` is ``plowable``, ``impervious`` or ``pervious`` (or the codes
0, 1, 2). Returns the seven ``[SNOWPACKS]`` values — see
``snowpack_set_surface`` for their meaning.

**Input arguments**

- `session_id` (string)
- `snowpack_id` (any)
- `surface` (any)

---

### subcatchments_snowpack_id

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the string id of the ``index``-th snowpack.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### subcatchments_snowpack_set_removal

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set a snowpack's REMOVAL row (pre-start-only).

**Input arguments**

- `session_id` (string)
- `snowpack_id` (any)
- `dsnow` (number)
- `fout` (number)
- `fimp` (number)
- `fperv` (number)
- `fimelt` (number)
- `fsubcatch` (number)

---

### subcatchments_snowpack_set_removal_subcatch

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set (or clear) the destination subcatchment for a snowpack's
``fsubcatch`` removal fraction.

An empty ``subcatch_id`` clears it. Pre-start-only.

**Input arguments**

- `session_id` (string)
- `snowpack_id` (any)
- `subcatch_id` (string)

---

### subcatchments_snowpack_set_surface

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set one snow-melt surface of a snowpack definition (pre-start-only).

**Input arguments**

- `session_id` (string)
- `snowpack_id` (any)
- `surface` (any)
- `cmin` (number)
- `cmax` (number)
- `tbase` (number)
- `fwfrac` (number)
- `sd0` (number)
- `fw0` (number)
- `last` (number)

---

### subcatchments_stat_max_runoff

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return the peak runoff rate for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_stat_precip

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return total precipitation volume for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

### subcatchments_stat_runoff_vol

- **Namespace**: subcatchments
- **Action Group**: hydrology
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return total runoff volume for a subcatchment.

**Input arguments**

- `session_id` (string)
- `subcatch_id` (any)

---

## Namespace: tables

### tables_add_curve

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create a curve and populate it with ``(x, y)`` points.

``curve_type`` is a string (``storage``, ``diversion``, ``tidal``,
``rating``, ``control``, ``shape``, ``pump1``..``pump4``, ``weir``) or
the engine integer code directly. Requires the ``building`` state.

**Input arguments**

- `session_id` (string)
- `curve_id` (string)
- `curve_type` (string)
- `x_values` (any)
- `y_values` (any)

---

### tables_add_point

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Append a single ``(x, y)`` data point to an existing table.

**Input arguments**

- `session_id` (string)
- `table_id` (any)
- `x` (number)
- `y` (number)

---

### tables_add_timeseries

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create a time series and populate it with ``(time, value)`` points.

Requires the session to be in the ``building`` state. Points are added
in input order; the engine does not sort them.

**Input arguments**

- `session_id` (string)
- `ts_id` (string)
- `times` (any)
- `values` (any)

---

### tables_clear_points

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Remove all data points from a table (the table itself remains).

**Input arguments**

- `session_id` (string)
- `table_id` (any)

---

### tables_count

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of curves and time series in the model.

The count combines both since the engine stores them in a single table
namespace. Patterns are counted separately; see ``pattern_count``.

**Input arguments**

- `session_id` (string)

---

### tables_get_id

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the string ID of a table by zero-based index.

**Input arguments**

- `session_id` (string)
- `index` (integer)

---

### tables_get_index

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the zero-based index of a table by string ID.

Returns ``-1`` if no table with that ID exists.

**Input arguments**

- `session_id` (string)
- `table_id` (string)

---

### tables_get_point

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read a single ``(x, y)`` data point from a table by point index.

**Input arguments**

- `session_id` (string)
- `table_id` (any)
- `point_index` (integer)

---

### tables_get_point_count

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of data points in a table.

**Input arguments**

- `session_id` (string)
- `table_id` (any)

---

### tables_get_points

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return all data points in a table as a list of ``[x, y]`` pairs.

Reads ``table.points`` (a NumPy array) in a single C call and projects
each row to ``[x, y]`` floats for the JSON wire format.

**Input arguments**

- `session_id` (string)
- `table_id` (any)

---

### tables_get_type

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the type of a table (curve kind or time series).

Surfaces ``Tables.get_type`` — a ``TableType`` enum identifying the
table (e.g. ``STORAGE``, ``RATING``, ``PUMP1`` for curves, or the
time-series kind). ``table_id`` is a string ID or integer index.
Reports both the enum ``type`` name and its integer ``type_code``.

**Input arguments**

- `session_id` (string)
- `table_id` (any)

---

### tables_lookup

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Interpolate a Y value from a table at the given X.

Uses the engine's cursor-optimized lookup; values outside the table's
X range clamp to the nearest endpoint.

**Input arguments**

- `session_id` (string)
- `table_id` (any)
- `x` (number)

---

### tables_pattern_add

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Create a time pattern and (optionally) seed its multiplier factors.

``pattern_type`` accepts a string (``monthly``, ``daily``, ``hourly``,
``weekend``) or the integer engine code. When ``factors`` is supplied,
it is applied via ``pattern.set_factors`` immediately after creation.
Expected factor counts: 12 for monthly, 7 for daily, 24 for hourly /
weekend.

**Input arguments**

- `session_id` (string)
- `pattern_id` (string)
- `pattern_type` (string)
- `factors` (any)

---

### tables_pattern_count

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the number of time patterns in the model.

**Input arguments**

- `session_id` (string)

---

### tables_pattern_remove

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Remove a time pattern by string ID or integer index (BUILDING state).

Mutation; requires the session to be in the ``building`` state (mirrors
``pattern_add``).

**Input arguments**

- `session_id` (string)
- `pattern_id` (any)

---

### tables_pattern_set_factors

- **Namespace**: tables
- **Action Group**: model-builder
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Replace the multiplier factors of an existing time pattern.

Pattern length is determined by ``pattern_type``; supplying a factor
count that does not match will raise an engine error.  The
``pattern_type`` argument was added in v1 — it tells the engine which
block (monthly / daily / hourly / weekend) the factors apply to.

**Input arguments**

- `session_id` (string)
- `pattern_index` (integer)
- `pattern_type` (string)
- `factors` (any)

---

## Namespace: twod

### twod_add_triangle_coupling

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Couple a 2D mesh triangle to a 1D SWMM node (node->cell exchange).

Appends one ``[2D_TRIANGLE_NODE_MAP]`` row; it does **not** overwrite,
so a triangle may carry several rows (one per node). ``cd`` is the
discharge coefficient (> 0, default 0.65) and ``area`` the effective
exchange area in **m2** (> 0, default 1.0). Use
``twod_clear_triangle_couplings`` to re-author the whole set.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `node_name` (string)
- `cd` (number)
- `area` (number)

---

### twod_clear_triangle_couplings

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: DESTRUCTIVE
- **Destructive**: Yes

**Description**

Remove every authored triangle (node->cell) coupling row.

Also resets the legacy per-triangle mirror read by
``twod_get_coupling_map``. Vertex couplings are untouched.

**Input arguments**

- `session_id` (string)

---

### twod_force_clear

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Clear every 2D forcing override (rainfall and coupling flux).

**Input arguments**

- `session_id` (string)

---

### twod_force_coupling_flux

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Force the 1D<->2D coupling flux on a triangle (m/s, positive = into 2D).

``mode`` is ``"replace"`` or ``"add"``; ``persist=True`` holds the
forcing until cleared, otherwise it resets after one step.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `value` (number)
- `mode` (string)
- `persist` (boolean)

---

### twod_force_evap

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Force evaporation on the 2D surface (m/s).

``triangle`` < 0 (the default) applies the rate uniformly to every
triangle; otherwise only the given triangle is forced. ``mode`` is
``"replace"`` or ``"add"``; ``persist=True`` holds the forcing until
cleared, otherwise it resets after one step.

**Input arguments**

- `session_id` (string)
- `value` (number)
- `triangle` (integer)
- `mode` (string)
- `persist` (boolean)

---

### twod_force_rainfall

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Force rainfall on the 2D surface (m/s).

``triangle`` < 0 (the default) applies the rate uniformly to every
triangle; otherwise only the given triangle is forced. ``mode`` is
``"replace"`` or ``"add"``; ``persist=True`` holds the forcing until
cleared, otherwise it resets after one step.

**Input arguments**

- `session_id` (string)
- `value` (number)
- `triangle` (integer)
- `mode` (string)
- `persist` (boolean)

---

### twod_get_coupling_map

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

List every 2D mesh entity coupled to a 1D node.

Returns ``vertex_couplings`` (vertex index -> node index) and
``triangle_couplings`` (triangle index -> node index). These are the
exchange points where the 2D surface trades flow with the drainage
network.

``triangle_coupling_rows`` is the authoritative
``[2D_TRIANGLE_NODE_MAP]`` row list — ``{row, triangle, node_index,
cd, area}`` — and is what ``twod_add_triangle_coupling`` writes. Prefer
it over ``triangle_couplings``, which is a lossy per-triangle mirror
showing only one node per triangle.

**Input arguments**

- `session_id` (string)

---

### twod_get_edge_bc

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the boundary condition on one triangle edge.

Reports the BC type (WALL / NORMAL_FLOW / SPECIFIED_STAGE /
SPECIFIED_FLOW / RATING_CURVE), the constant head and slope, the
prescribed per-metre flow, and the cumulative flux through the edge.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `edge` (integer)

---

### twod_get_edge_conveyance

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Read per-edge conveyance factors (1.0 = unrestricted, 0.0 = wall).

With ``triangle`` >= 0 returns the single factor at (triangle, edge);
with ``triangle`` < 0 (default) returns a whole-mesh summary plus the
list of restricted edges (factor < 1), so berms / barriers are easy to
spot.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `edge` (integer)

---

### twod_get_edge_geometry_bulk

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return time-invariant per-edge geometry for the whole mesh.

For every triangle edge (indexed ``[tri*3 + edge]``) reports its length
(m) and the outward unit-normal components ``nx`` / ``ny``. Returns
summary statistics for each array plus the per-edge values in
``[offset, offset+limit)`` when ``limit`` > 0, each entry as
``{triangle, edge, length, nx, ny}``. Pairs with ``twod_get_state_bulk``
(``variable="edge_flux"``), which shares the same ``[tri*3 + edge]``
indexing.

**Input arguments**

- `session_id` (string)
- `offset` (integer)
- `limit` (integer)

---

### twod_get_mass_balance

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the global 2D mass-balance terms (m3) and continuity error.

Terms: initial/final storage, rainfall in, 1D->2D coupling in,
2D->1D coupling out, outfall in/out, evaporation out, boundary
in/out, and the overall continuity error as a fraction of total
inflow.

**Input arguments**

- `session_id` (string)

---

### twod_get_mesh_geometry

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return mesh geometry for a window of triangles.

For each triangle in ``[offset, offset+limit)``: its vertex indices,
area, centroid, Manning's n, and the three neighbour triangle indices
(-1 = boundary). Also reports vertex elevation summary statistics.
Use ``twod_get_mesh_summary`` first to learn the mesh size.

**Input arguments**

- `session_id` (string)
- `offset` (integer)
- `limit` (integer)

---

### twod_get_mesh_summary

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Report whether the model has an active 2D surface and its mesh sizes.

Returns ``active``, vertex / triangle counts, the number of boundary
edges, and how many vertices / triangles are coupled to 1D nodes.
Safe to call on any opened model — ``active`` is ``False`` when the
model carries no ``[2D_*]`` sections.

**Input arguments**

- `session_id` (string)

---

### twod_get_solver_params

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the 2D solver parameters.

Reports the dry-depth threshold (m). The explicit-marcher
configuration (THETA, CFL_NUMBER, LTS_TIERS, H_MOVE, FROUDE_MAX,
COUPLING_AREA, ...) lives in ``[2D_OPTIONS]`` and is read with
``model_get_option_ext``. The retired CVODE tolerances no longer
exist.

**Input arguments**

- `session_id` (string)

---

### twod_get_state

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the current 2D state at one triangle.

Reports depth (m), head (m), rainfall (m/s), net source (m/s), and the
1D<->2D coupling flux (m3/s, positive = into the 2D surface).

**Input arguments**

- `session_id` (string)
- `triangle` (integer)

---

### twod_get_state_bulk

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Summarise a 2D state variable over the whole mesh.

``variable`` is one of ``"depth"``, ``"head"``, ``"vertex_head"``,
``"vertex_render_depth"``, ``"coupling_flux"``, or ``"edge_flux"``.
Returns count / min / max / mean, plus the values in
``[offset, offset+limit)`` when ``limit`` > 0 (``edge_flux`` and the
others are indexed per triangle except ``vertex_head`` and
``vertex_render_depth``, which are per vertex; ``edge_flux`` is ``[tri*3 +
edge]``). ``vertex_render_depth`` is the render-oriented signed vertex
water depth (``eta_v - z_v``) GUIs should interpolate for 2D
water-surface rendering.

**Input arguments**

- `session_id` (string)
- `variable` (string)
- `offset` (integer)
- `limit` (integer)

---

### twod_get_stats

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return cumulative per-triangle statistics with worst-case hot spots.

For max depth (m), max velocity magnitude (m/s), and max absolute
continuity residual (m3/s): summary statistics plus the ``top_n`` triangles with
the largest values (index + value), ranked descending.

**Input arguments**

- `session_id` (string)
- `top_n` (integer)

---

### twod_get_totals

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return whole-surface totals and internal-stepper diagnostics.

Reports max depth over the surface (m), total ponded volume (m3),
total 1D<->2D exchange flow (m3/s), the explicit marcher's sub-step
count for the last advance, and its last sub-step size (s).

**Input arguments**

- `session_id` (string)

---

### twod_get_triangle_initial_conditions

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the initial water depth and velocity of a 2D triangle.

``init_depth`` is the ``[2D_TRIANGLES]`` INIT_DEPTH column in **mesh
length units** — feet on a US-FLOW_UNITS project, metres on an SI
project (the same convention as the vertex Z column), *not* the SI
metres used by the run-time state tools. ``init_u`` / ``init_v`` are
the ``[2D_INITIAL_VELOCITY]`` components and are always in m/s.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)

---

### twod_get_triangle_tag

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the descriptive tag of a 2D triangle (empty if untagged).

**Input arguments**

- `session_id` (string)
- `triangle` (integer)

---

### twod_get_vertex_coupling_params

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the 1D<->2D exchange parameters of a mesh vertex.

Reports the ``[2D_VERTEX_NODE_MAP]`` CD (discharge coefficient,
default 0.65) and AREA (effective exchange area in m2, default 1.0)
columns. Use ``twod_get_coupling_map`` for which node each vertex is
coupled to.

**Input arguments**

- `session_id` (string)
- `vertex` (integer)

---

### twod_get_vertex_head

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the reconstructed water-surface head (m) at one mesh vertex.

Triangle-based state is the solver's native representation; this is the
per-vertex value reconstructed for rendering. Use
``twod_get_state_bulk`` with ``variable="vertex_head"`` to read every
vertex at once.

**Input arguments**

- `session_id` (string)
- `vertex` (integer)

---

### twod_get_vertex_tag

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: READ
- **Destructive**: No

**Description**

Return the descriptive tag of a 2D vertex (empty if untagged).

**Input arguments**

- `session_id` (string)
- `vertex` (integer)

---

### twod_reset_edge_conveyance

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Reset every edge's conveyance factor to 1.0 (unrestricted).

**Input arguments**

- `session_id` (string)

---

### twod_set_edge_bc

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Configure the boundary condition on one triangle edge.

``bc_type`` (optional) is WALL, NORMAL_FLOW, SPECIFIED_STAGE,
SPECIFIED_FLOW, or RATING_CURVE. The remaining parameters apply only
when provided: ``head`` (constant stage, m), ``slope`` (NORMAL_FLOW bed
slope), ``flow`` (per-metre discharge, m3/s/m), ``tseries_name``
(stage timeseries; "" clears), ``flow_tseries_name`` (flow timeseries;
"" clears), ``rating_curve_name`` (stage-to-flow curve; "" clears).

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `edge` (integer)
- `bc_type` (string)
- `head` (any)
- `slope` (any)
- `flow` (any)
- `tseries_name` (any)
- `flow_tseries_name` (any)
- `rating_curve_name` (any)

---

### twod_set_edge_conveyance

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the conveyance factor on one triangle edge (in [0, 1]).

0.0 makes the edge a wall; 1.0 leaves it unrestricted. Interior edges
mirror the value to the neighbouring triangle's partner slot so mass
conservation is preserved. Apply between routing steps.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `edge` (integer)
- `conveyance` (number)

---

### twod_set_solver_params

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set 2D solver parameters; omitted parameters are left unchanged.

``dry_depth`` is the wet/dry threshold (m). The explicit-marcher
configuration (THETA, CFL_NUMBER, LTS_TIERS, H_MOVE, FROUDE_MAX,
COUPLING_AREA, ...) lives in ``[2D_OPTIONS]`` and is set with
``model_set_option_ext``. The retired CVODE tolerances no longer
exist.

**Input arguments**

- `session_id` (string)
- `dry_depth` (any)

---

### twod_set_triangle_initial_conditions

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the initial depth and/or velocity of a 2D triangle.

``depth`` (>= 0) is in **mesh length units** — feet on a US-FLOW_UNITS
project, metres on an SI project, matching the vertex Z column — and
persists in the ``INIT_DEPTH`` column of ``[2D_TRIANGLES]``. ``u`` and
``v`` are the initial velocity components in **m/s** and must be given
together; they persist as ``[2D_INITIAL_VELOCITY]`` rows. Both are
applied when the 2D surface initializes (t = 0 only — a hotstart still
zeroes face momentum), so set them before the run starts.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `depth` (any)
- `u` (any)
- `v` (any)

---

### twod_set_triangle_mannings

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set Manning's roughness for a 2D mesh triangle (must be > 0).

Persists in the ``MANNINGS_N`` column of ``[2D_TRIANGLES]`` on save.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `n` (number)

---

### twod_set_triangle_tag

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the descriptive tag of a 2D triangle (``[2D_TRIANGLES]`` TAG).

An empty string clears the tag.

**Input arguments**

- `session_id` (string)
- `triangle` (integer)
- `tag` (string)

---

### twod_set_vertex_coupled_node

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Couple a 2D mesh vertex to a 1D SWMM node by name.

Establishes the per-vertex 1D<->2D exchange point. Pass an empty string
to clear the coupling.

**Input arguments**

- `session_id` (string)
- `vertex` (integer)
- `node_name` (string)

---

### twod_set_vertex_coupling_params

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the 1D<->2D exchange parameters of a mesh vertex.

``cd`` is the orifice/weir discharge coefficient (must be > 0, engine
default 0.65) and ``area`` the effective exchange area in **m2** (must
be > 0, default 1.0). Omitted parameters are left unchanged. Both
persist in ``[2D_VERTEX_NODE_MAP]``; pair with
``twod_set_vertex_coupled_node``, which establishes the coupling
itself.

**Input arguments**

- `session_id` (string)
- `vertex` (integer)
- `cd` (any)
- `area` (any)

---

### twod_set_vertex_tag

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the descriptive tag of a 2D vertex (``[2D_VERTICES]`` TAG).

An empty string clears the tag. Distinct from the 1D<->2D coupling node.

**Input arguments**

- `session_id` (string)
- `vertex` (integer)
- `tag` (string)

---

### twod_set_vertex_z

- **Namespace**: twod
- **Action Group**: twod
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Set the ground elevation of a mesh vertex (m).

Updates derived geometry for every triangle incident to the vertex.
Useful for what-if terrain edits (berms, regrading) between steps.

**Input arguments**

- `session_id` (string)
- `vertex` (integer)
- `z` (number)

---

## Namespace: xsect

### xsect_area_of_depth

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Flow area at a depth, or at a list of depths in one batched call.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `depth` (any)

---

### xsect_area_of_sectfactor

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Flow area for a section factor -- the step that solves for normal depth.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `section_factor` (any)

---

### xsect_critical_depth

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Critical depth for a flow, or for a list of flows.

``flow`` is in the section's ``flow_units`` (echoed in the response).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `flow` (any)

---

### xsect_depth_of_area

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Depth of flow for a given area -- the inverse of ``area_of_depth``.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `area` (any)

---

### xsect_dsda

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Derivative of the section factor with respect to area (dS/dA).

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `area` (any)

---

### xsect_hydrad_of_area

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Hydraulic radius for a given flow area, or a list of areas.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `area` (any)

---

### xsect_hydrad_of_depth

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Hydraulic radius (area / wetted perimeter) at a depth or list of depths.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `depth` (any)

---

### xsect_list_shapes

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: READ
- **Destructive**: No

**Description**

List every cross-section shape name accepted by the ``shape`` argument.

IRREGULAR / CUSTOM / STREET_XSECT are tabulated shapes: they carry no
inline geometry and must be built with ``properties_from_transect`` /
``properties_from_curve`` / ``properties_from_street``, or reached through
``link_id``.

**Input arguments**

- `session_id` (string)

---

### xsect_properties

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Return a section's full geometric properties.

Full depth / area / hydraulic radius / section factor, the maximum width
and area, whether the section is open to the atmosphere, and its unit
system. Name the section with ``link_id`` or with ``shape`` +
``geom1``..``geom4`` + ``units``.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)

---

### xsect_properties_from_curve

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Build a custom section from a normalized shape curve.

Mirrors a ``SHAPE``-type ``[CURVES]`` entry scaled to ``full_depth``:
``curve_depths`` are y/yFull in [0, 1] ascending, ``curve_widths`` the
matching w/wMax. Returns the resulting section's full properties.

**Input arguments**

- `session_id` (string)
- `full_depth` (number)
- `curve_depths` (any)
- `curve_widths` (any)
- `units` (string)

---

### xsect_properties_from_street

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Build a street section. Mirrors a ``[STREETS]`` entry.

``width`` is curb-to-crown, ``slope`` and ``back_slope`` are in percent,
``sides`` is 1 (half street) or 2 (full street). Returns the resulting
section's full properties.

**Input arguments**

- `session_id` (string)
- `width` (number)
- `curb_height` (number)
- `slope` (number)
- `roughness` (number)
- `gutter_depression` (number)
- `gutter_width` (number)
- `sides` (integer)
- `back_width` (number)
- `back_slope` (number)
- `back_roughness` (number)
- `units` (string)

---

### xsect_properties_from_transect

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Build an irregular (natural channel) section from transect data.

Mirrors a ``[TRANSECTS]`` entry and returns the resulting section's full
properties. ``n_channel`` must be > 0; ``n_left`` / ``n_right`` default to
``n_channel`` when left at 0. Pass the same value for ``left_bank`` and
``right_bank`` for a channel with no overbanks.

**Input arguments**

- `session_id` (string)
- `stations` (any)
- `elevations` (any)
- `left_bank` (number)
- `right_bank` (number)
- `n_channel` (number)
- `n_left` (number)
- `n_right` (number)
- `length_factor` (number)
- `units` (string)

---

### xsect_sectfactor_of_area

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Section factor (A*R^(2/3)) for a given flow area, or a list of areas.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `area` (any)

---

### xsect_width_of_depth

- **Namespace**: xsect
- **Action Group**: hydraulics
- **Operation Class**: WRITE
- **Destructive**: No

**Description**

Top width of the water surface at a depth, or at a list of depths.

**Input arguments**

- `session_id` (string)
- `link_id` (any)
- `shape` (string)
- `geom1` (number)
- `geom2` (number)
- `geom3` (number)
- `geom4` (number)
- `units` (string)
- `depth` (any)

---
