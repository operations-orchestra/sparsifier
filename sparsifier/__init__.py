"""Sparsifier: turns bulk sources into the few entries the Record keeps. Skeleton.

Readings: the series stays in the source; the sparsifier records only status changes, each
with a pointer into the source (decided 17 November 2026; see docs/DESIGN.md 7a). In this demo
the generator applies a fixed rule itself (example_device/readings.py); this is where a real
rule, owned by each subsystem, would live. Data quality: numbers per run from histograms, and
the plots relevant to an incident.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from utils import Entry

STATUS = "skeleton"
ROLE = "Reduces bulk sources (readings, data-quality histograms) to status changes and pointers."
EXAMPLE = {
    "input": "The LV readback of HBP02, one sample a minute, from the control-system archive",
    "output": "Entry(type='lv_voltage_status', element='HBP02', t_start=<first sample in the new status>, "
              "known_at=<when the rule could tell>, payload={'value': 'drifting down', ...}, raw_ref='source://...')",
    "produces": "dcs/lv_voltage_status",
}


@dataclass(frozen=True)
class Series:
    element: str
    quantity: str                      # e.g. "lv_voltage"
    times: list[int]
    values: list[float]
    pointer: str                       # where the series lives in the source


class StatusRule(Protocol):
    """When a reading counts as normal, drifting, low, high or off. One per quantity and subsystem."""

    def classify(self, series: Series) -> list[str]:
        raise NotImplementedError


class Sparsifier(Protocol):
    def status_changes(self, series: Series, rule: StatusRule) -> list[Entry]:
        """One state entry per change of status, pointing back into the source."""
        raise NotImplementedError

    def quality_summary(self, run: int, part: str, histograms: list[str]) -> list[Entry]:
        """A few numbers per run and part from its histograms, with pointers to them."""
        raise NotImplementedError
