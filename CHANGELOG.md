# Changelog for ndx-structured-behavior

## 0.2.0 (Upcoming)

### Breaking changes
- As pynwb 4 added an `EventsTable` to the core namespace, the `EventsTable` neurodata type defined in this extension is removed. 
  `TaskRecording.events` and the `TrialsTable.events` region now refer to the core `EventsTable`.
- The `EventsTable` Python class is replaced by helpers, since the core type is used directly:
  - `EventsTable(description=..., event_types_table=...)` -> `create_events_table(event_types_table=..., description=...)`
  - `events.add_event(...)` -> `add_event(events, ...)`
  - `events.populate_from_matlab(data_path=...)` -> `populate_events_table_from_matlab(events, data_path=...)`

  `ndx_structured_behavior.EventsTable` is still importable and is now `pynwb.event.EventsTable`.
- `event_type` and `value` are now ordinary columns on the core `EventsTable` rather than being
  guaranteed by this extension's schema. `duration` and `annotation` come from the core type.

### Requirements
- Minimum supported versions are now Python 3.10, pynwb 4.1.0, hdmf 6.2.0 and scipy 1.14.1.
