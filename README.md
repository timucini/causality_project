# Causality Project
This repository represents a student project between the HTW Berlin and Signavio. The goal is to provide a toolbox of approaches for causality testing of process changes and their potential impacts.

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
Additionally you can find there the environment.py, which contains important environment variables for the project.

### resources
The resource directory contains all necessary files which are used for testing and research.

#### bpmns
This directory contains all BPMNs used for research, for example for simulation.

#### case_tables
This directory contains all CSV files representing a case table used for research.

#### csv_logs
This directory contains all CSV files representing a event-log used for research.

#### simulation_data
This directory contains all CSV files representing a scenario used for simulation.

#### xes_logs
This directory contains all extern XES files representing a event-log used for research.

#### causality_feature_tables
This directory contains the results of the investigation.

### source
This directory contains the source-code.