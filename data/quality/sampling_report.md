# Sampling and Reduction Report

## Dataset Information

- Source: `data/source-sample/source_sample.csv`
- Original records: 18
- Retained records: 18
- Source columns: 8
- Sampling method: Complete dataset retention
- Random sampling: Not applied
- Record reduction: None

## Sampling Decision

All 18 source records were retained.

The dataset is small enough to process in full. Retaining every
record preserves all available departments, cost centres,
account categories, reporting months, and financial measures.

## Preservation Check

- Original record count: 18
- Retained record count: 18
- Records excluded: 0
- Records lost: 0
- Preservation status: PASSED

## Canonical Expansion Plan

Each source record will later produce four canonical financial
measure records:

- budget_amount
- actual_amount
- committed_amount
- forecast_amount

Expected canonical records: 18 × 4 = 72

## Generated Information

- Report generated at: 2026-11-03T14:40:21.144017+00:00
- Sampling script: `scripts/data_pipeline/sample_data.py`
