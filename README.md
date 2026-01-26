# ORCA_SOCME_Extractor
A Python utility to extract **Spin-Orbit Coupling Matrix Elements (SOCME)** and excitation energies from **ORCA** quantum chemistry output files. 

This script parses standard ORCA output files (specifically TD-DFT/TDA calculations), calculates the magnitude of the coupling vectors, filters based on specific Singlet states, and exports the results to a clean Excel spreadsheet.

## Features

- **Automated Parsing:** Reads excitation energies for both Singlet and Triplet states.
- **SOC Calculation:** Extracts the calculated SOCME between triplets and singlets and computes the magnitude ($\sqrt{x^2 + y^2 + z^2}$).
- **Filtering:** Allows the user to specify which Singlet states to target (e.g., S0, S1).
- **Excel Export:** Saves a formatted `.xlsx` file containing:
  - Triplet State Index & Energy (eV)
  - Singlet State Index & Energy (eV)
  - SOC Magnitude ($cm^{-1}$)

## Prerequisites

You need Python 3 installed along with the following libraries:
- `numpy`
- `pandas`
- `openpyxl` (for Excel export)

## Installation

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/orca-socme-extractor.git](https://github.com/YOUR_USERNAME/orca-socme-extractor.git)
   cd orca-socme-extractor
