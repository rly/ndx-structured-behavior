# ndx-structured-behavior Extension for NWB

[![PyPI version](https://badge.fury.io/py/ndx-structured-behavior.svg)](https://badge.fury.io/py/ndx-structured-behavior)

> **Version 0.2.0 is not stable and is subject to major breaking changes.**
> NWBEP001, developed as the [ndx-events](https://github.com/rly/ndx-events) extension, has been merged
> into the core NWB schema (version 2.10.0), which now defines `EventsTable`, `TimestampVectorData`, and
> `DurationVectorData`. This extension is not yet fully integrated with those core types, and completing
> that integration is expected to change the on-disk layout.

An NWB extension for storing structured behavior programs and data, such as from BAABL/BEADL.

The extension *ndx_structured_behavior* defines a collection of interlinked table data structures for
storing behavioral tasks and data. While the extension has been designed with BEADL in
mind, the data structures are general and are intended to be useful even without BEADL.
For additional information about BEADL, please visit [https://beadl.org/](https://beadl.org/).

The *ndx-structured-behavior* data model:

![ndx-structured-behavior schema](https://raw.githubusercontent.com/rly/ndx-structured-behavior/main/docs/tutorials/beadl_overview.png "ndx-structured-behavior schema")

## Installation

```bash
pip install ndx-structured-behavior
```

## Usage

See [example.py](https://github.com/rly/ndx-structured-behavior/blob/main/src/pynwb/tests/example.py) for an example of how to use this extension.

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
