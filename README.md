# Causality Project
This repository represents a student project between HTW Berlin and Signavio.
The goal is to provide a toolkit of approaches for causality testing of process changes and their potential impacts.

## Environment

| Software | Version |
| - | - |
| OS | Windows 10 |
| Python | 3.8 |

| System | |
| - | - |
| CPU | AMD Ryzen 9 5950x |
| RAM | 32GB DDR4 |
| GPU | Nvidia RTX 3090 |
| SSD | PCIe NVMe |

## Structure

### root
The root directory of the project could contain testing files and jupyter notebooks with examples.<br>
In addition, you will find environment.py, which contains important environment variables for the project.

### resources
The resource directory contains all necessary files which are used for testing and research.

#### bpmns
This directory contains all BPMNs used for research, which are used for the simulation.

#### case_tables
This directory contains all CSV files which representing case tables used for research.

#### csv_logs
This directory contains all CSV files which representing event-logs used for research.

#### simulation_data
This directory contains all CSV files which representing scenarios used for simulation.

#### xes_logs
This directory contains all extern XES files which representing event-logs used for research.

#### causality_feature_tables
This directory contains the results of the investigation.

### documentation
This directory contains additional documentation.

### source
This directory contains the source-code.