# ndx-structured-behavior Extension for NWB

[![PyPI version](https://badge.fury.io/py/ndx-structured-behavior.svg)](https://badge.fury.io/py/ndx-structured-behavior)

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
