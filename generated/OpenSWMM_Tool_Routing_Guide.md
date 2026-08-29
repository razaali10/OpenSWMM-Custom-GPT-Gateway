# OpenSWMM Tool Routing Guide

Curated mapping from engineering tasks to the action groups most likely to contain the right tool -- use listOpenSwmmNamespaces/searchOpenSwmmTools/getOpenSwmmToolSchema to find the exact tool and its real input schema before calling it.

## Model inventory

Preferred action groups: `core`, `results`

## Flood investigation

Preferred action groups: `results`, `hydraulics`, `twod`

## Pipe capacity review

Preferred action groups: `hydraulics`, `results`

## Pump analysis

Preferred action groups: `hydraulics`, `results`

## Storage analysis

Preferred action groups: `hydraulics`, `results`

## Rainfall-runoff review

Preferred action groups: `hydrology`, `results`

## Groundwater review

Preferred action groups: `hydrology`

## RDII review

Preferred action groups: `hydrology`

## Water quality review

Preferred action groups: `water-quality`

## 2D surface flooding

Preferred action groups: `twod`, `results`

## 1D/2D coupling

Preferred action groups: `twod`, `hydraulics`

## RTC controls

Preferred action groups: `forcing-controls`

## Model construction

Preferred action groups: `model-builder`, `core`

## Model modification

Preferred action groups: `model-builder`

## Scenario comparison

Preferred action groups: `results`, `core`

## LID design

Preferred action groups: `infrastructure`, `hydrology`

## Optimization

Preferred action groups: `optimization`

## All action groups (live tool counts)

- `core`: 67 tools
- `forcing-controls`: 22 tools
- `hydraulics`: 114 tools
- `hydrology`: 98 tools
- `infrastructure`: 43 tools
- `model-builder`: 56 tools
- `optimization`: 34 tools
- `results`: 29 tools
- `spatial`: 28 tools
- `twod`: 34 tools
- `water-quality`: 40 tools