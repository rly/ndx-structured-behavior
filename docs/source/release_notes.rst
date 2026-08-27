Release Notes
=============

## Structured Behavior 0.2.0 (Upcoming)

### Breaking changes
- As pynwb 4 added `EventsTable` to the core namespace, this extension doesn't need to define its own `EventsTable`.
 `TaskRecording.events` and the `TrialsTable.events` region now refer to the core `EventsTable`, and `event_type`/`value` are ordinary columns on it.
- The `EventsTable` class is replaced by `create_events_table()`, `add_event()` and
  `populate_events_table_from_matlab()`. `ndx_structured_behavior.EventsTable` is still importable
  and is now `pynwb.event.EventsTable`.

### Requirements
- Minimum supported versions are now Python 3.10, pynwb 4.1.0, hdmf 6.2.0 and scipy 1.14.1.

## Structured Behavior 0.1.0 (unreleased)

This extension defines a formal standard for storing task programs and behavioral data within NWB.
Some of the recent updates include the following:

### Enhancements
- Optional `duration` column for `EventsTable` and `ActionsTable`.
- The `StatesTable`, `EventsTable`, and `ActionsTable` are stored within `TaskRecording` to be added to a NWBFile.
