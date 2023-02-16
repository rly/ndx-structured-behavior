# ndx-beadl Extension for NWB

The extension *ndx_beadl* defines a collection of interlinked table data structures for
storing behavioral tasks and data. While the extension has been designed with BEADL in 
mind, the data structures are general and are intended to be useful even without BEADL. 
For additional information about BEADL, please visit [https://beadl.org/](https://beadl.org/).

The *ndx-beadl* data model consists of three main components:

![ndx-beadl schema](docs/tutorial_nwb_userdays_2022/beadl_components_p1.png?raw=true "ndx-beadl schema")
![ndx-beadl schema](docs/tutorial_nwb_userdays_2022/beadl_components_p2.png?raw=true "ndx-beadl schema")


## Installation

```python
git clone https://github.com/rly/ndx-beadl.git
cd ndx-beadl
pip install -e . 
```

## Usage

https://github.com/rly/ndx-beadl/blob/a1b6380febdb964eeba4466c5901e103ef2fe463/src/pynwb/tests/example.py#L1-L90

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
