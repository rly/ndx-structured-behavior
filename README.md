# ndx-structured-behavior Extension for NWB

The extension *ndx_structured_behavior* defines a collection of interlinked table data structures for
storing behavioral tasks and data. While the extension has been designed with BEADL in
mind, the data structures are general and are intended to be useful even without BEADL.
For additional information about BEADL, please visit [https://beadl.org/](https://beadl.org/).

The *ndx-structured-behavior* data model consists of three main components:

![ndx-structured-behavior schema](docs/tutorial_nwb_userdays_2022/beadl_components_p1.png?raw=true "ndx-structured-behavior schema")
![ndx-structured-behavior schema](docs/tutorial_nwb_userdays_2022/beadl_components_p2.png?raw=true "ndx-structured-behavior schema")


## Installation

```python
git clone https://github.com/rly/ndx-structured-behavior.git
cd ndx-structured-behavior
pip install -e .
```

## Usage

https://github.com/rly/ndx-structured-behavior/blob/5df21f406a7e03587650157a6f3ec07be508b1f9/src/pynwb/tests/example.py#L1-L90

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
