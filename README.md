# ndx-structured-behavior Extension for NWB

An NWB extension for storing structured behavior programs and data, such as from BAABL/BEADL.

The extension *ndx_structured_behavior* defines a collection of interlinked table data structures for
storing behavioral tasks and data. While the extension has been designed with BEADL in
mind, the data structures are general and are intended to be useful even without BEADL.
For additional information about BEADL, please visit [https://beadl.org/](https://beadl.org/).

The *ndx-structured-behavior* data model:

![ndx-structured-behavior schema](docs/tutorials/beadl_overview.png?raw=true "ndx-structured-behavior schema")

## Installation

```python
git clone https://github.com/rly/ndx-structured-behavior.git
cd ndx-structured-behavior
pip install -e .
```

## Usage

https://github.com/rly/ndx-structured-behavior/main/src/pynwb/tests/example.py#L1-L90

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
