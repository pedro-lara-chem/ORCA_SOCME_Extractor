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
```
2. Install the required dependencies:
  ```bash
pip install -r requirements.txt
```
## Usage

1. Place your ORCA output file (e.g., calculation.out) in the same directory as the script (or know the path to it).
2. Run the script:
   ```bash
   python extract_SOCME.py
   ```
3. Follow the interactive prompts:
   * File Name: Enter the name ofyour ORCA output file.
   * Singlet States :Enter the indices of the singlets you are interested in (comma-separated).
   * Note: 0 usually represents the Ground State (S0).
   * Output Name: Enter the desired name for your Excel file.
## Example Interaction
```bash
Please enter the name of the ORCA output file: my_calc.out
Enter the desired singlet states, separated by commas (e.g., 0,1,6): 0, 1
Enter the name for the output Excel file (e.g., results.xlsx): soc_data.xlsx

✅ Success! Data has been saved to 'soc_data.xlsx' with formatted headers.
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.
