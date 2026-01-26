import re
import numpy as np
import pandas as pd
import openpyxl

def extract_energies(file_content, state_type='SINGLET'):
    """
    Extracts the excitation energies (in eV) for Singlet or Triplet states.

    Args:
        file_content (str): The full string content of the ORCA output file.
        state_type (str): Either 'SINGLET' or 'TRIPLET'.

    Returns:
        dict: A dictionary mapping the state number (e.g., 1 for S1 or T1)
              to its energy in eV.
    """
    energies = {}
    # Regex to capture the state number and energy in eV
    energy_pattern = re.compile(r"STATE\s+(\d+):\s+E=\s+.*? au\s+(-?\d+\.\d+)\s+eV")
    
    header = f"TD-DFT/TDA EXCITED STATES ({state_type}S)"
    in_section = False
    
    # Determine the offset for triplet state indexing
    n_singlets = 0
    if state_type == 'TRIPLET':
        # Find the number of singlets to correctly index the triplets
        singlet_section = re.search(r"TD-DFT/TDA EXCITED STATES \(SINGLETS\)(.*?)Entering triplet calculation", file_content, re.DOTALL)
        if singlet_section:
            n_singlets = len(re.findall(r"STATE\s+\d+:", singlet_section.group(1)))

    for line in file_content.splitlines():
        if header in line:
            in_section = True
            continue
        # Stop parsing when the section ends
        if in_section and ("Entering triplet calculation" in line or "SPIN-ORBIT COUPLING" in line):
            break
        
        if in_section:
            match = energy_pattern.search(line)
            if match:
                state_num_abs = int(match.group(1))
                energy_ev = float(match.group(2))
                
                if state_type == 'SINGLET':
                    state_index = state_num_abs
                else: # Triplet
                    state_index = state_num_abs - n_singlets
                
                energies[state_index] = energy_ev
                
    return energies

def extract_socme_from_content(file_content):
    """
    Extracts the SOCME table from the string content of an ORCA output file.
    """
    socme_data = []
    in_socme_table_section = False
    socme_pattern = re.compile(
        r"^\s*(\d+)\s+(\d+)\s+"
        r"\(\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*\)\s+"
        r"\(\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*\)\s+"
        r"\(\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*\)"
    )

    for line in file_content.splitlines():
        if "CALCULATED SOCME BETWEEN TRIPLETS AND SINGLETS" in line:
            in_socme_table_section = True
            continue
        if "SOC stabilization of the ground state" in line:
            in_socme_table_section = False
            break
        
        if in_socme_table_section:
            match = socme_pattern.match(line)
            if match:
                groups = match.groups()
                row_data = [
                    int(groups[0]), int(groups[1]),
                    float(groups[2]), float(groups[3]),
                    float(groups[4]), float(groups[5]),
                    float(groups[6]), float(groups[7])
                ]
                socme_data.append(row_data)
    return np.array(socme_data)

def main():
    """
    Main function to run the interactive script.
    """
    # --- Get user input ---
    file_name = input("Please enter the name of the ORCA output file: ")
    singlets_input = input("Enter the desired singlet states, separated by commas (e.g., 0,1,6): ")
    try:
        target_singlets = [int(s.strip()) for s in singlets_input.split(',')]
    except ValueError:
        print("\nError: Invalid input. Please enter only numbers separated by commas.")
        return

    output_filename = input("Enter the name for the output Excel file (e.g., results.xlsx): ")
    if not output_filename.endswith('.xlsx'):
        output_filename += '.xlsx'

    # --- Process the file ---
    try:
        with open(file_name, 'r') as f:
            content = f.read()
        
        # Extract all necessary data
        singlet_energies = extract_energies(content, 'SINGLET')
        triplet_energies = extract_energies(content, 'TRIPLET')
        socme_array = extract_socme_from_content(content)

        if socme_array.size > 0:
            soc_vectors = socme_array[:, 2:]
            magnitudes = np.linalg.norm(soc_vectors, axis=1)
            
            # --- Filter data and prepare for saving ---
            table_data = []
            for i in range(len(socme_array)):
                triplet_state, singlet_state = int(socme_array[i, 0]), int(socme_array[i, 1])
                
                if singlet_state in target_singlets:
                    magnitude = magnitudes[i]
                    # Get energies from the dictionaries, S0 is the ground state (0.0 eV)
                    t_energy = triplet_energies.get(triplet_state, 'N/A')
                    s_energy = singlet_energies.get(singlet_state, 0.0) # Default to 0.0 for S0
                    
                    table_data.append([triplet_state, t_energy, singlet_state, s_energy, magnitude])
            
            if not table_data:
                print("No couplings found for the specified singlet states.")
                return

            # --- Create a pandas DataFrame and save to Excel ---
            headers = [
                "Triplet State", "Triplet Energy (eV)",
                "Singlet State", "Singlet Energy (eV)",
                "SOC (cm-1)"
            ]
            df = pd.DataFrame(table_data, columns=headers)
            df.to_excel(output_filename, index=False)
            
            
            print(f"\n✅ Success! Data has been saved to '{output_filename}' with formatted headers.")

        else:
            print("Could not find or extract the SOCME table from the file content.")

    except FileNotFoundError:
        print(f"\nError: The file '{file_name}' was not found in the current directory.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# --- Run the script ---
if __name__ == "__main__":
    main()

