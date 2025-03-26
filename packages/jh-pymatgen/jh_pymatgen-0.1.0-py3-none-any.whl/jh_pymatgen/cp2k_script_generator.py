#from structure_process import cp2k_to_structure

# Global variables
cp2k_PotDir = None
cp2k_basisDir = None
GeoOpt_template_path = None
NEB_template_path=None
SCF_P_template_path=None

in_pc_PotDir=None
in_pc_basisDir=None


        
def set_global_variables(cp2k_pot_dir=None, cp2k_basis_dir=None, template_GeoOpt=None,template_NEB=None,template_SCF_P=None,pyFunc_pot_dir=None, pyFunc_basis_dir=None):
    global cp2k_PotDir, cp2k_basisDir, GeoOpt_template_path, NEB_template_path,in_pc_PotDir, in_pc_basisDir,SCF_P_template_path
    if cp2k_pot_dir is not None:
        cp2k_PotDir = cp2k_pot_dir
    if cp2k_basis_dir is not None:
        cp2k_basisDir = cp2k_basis_dir
    if template_GeoOpt is not None:
        GeoOpt_template_path = template_GeoOpt
    if template_NEB is not None:
        NEB_template_path = template_NEB
    if pyFunc_pot_dir is not None:
        in_pc_PotDir = pyFunc_pot_dir
    if pyFunc_basis_dir is not None:
        in_pc_basisDir = pyFunc_basis_dir
    if template_SCF_P is not None:
        SCF_P_template_path = template_SCF_P


        

def check_global_variable():
    print("cp2k_PotDir=",cp2k_PotDir)
    print("cp2k_basisDir=",cp2k_basisDir)
    print("GeoOpt_template_path=",GeoOpt_template_path)
    print("NEB_template_path=",NEB_template_path)
    print("SCF_P_template_path=",SCF_P_template_path)
    print("in_pc_PotDir=",in_pc_PotDir)
    print("in_pc_basisDir=",in_pc_basisDir)
    
    print("\n\n")
    print(
        "Note: CP2K requires 'cp2k_PotDir' and 'cp2k_basisDir', specified in the .sh file. They must be accessible by CP2K.\n"
        "'in_pc_PotDir' and 'in_pc_basisDir' are used by Python functions. They must be accessible by PC running Python.\n")


def structure_to_cp2k_cell_coord(structure):
    """
    Convert a pymatgen Structure into CP2K CELL and COORD sections.
    
    Args:
        structure (Structure): Pymatgen structure object.
    
    Returns:
        str: CP2K formatted CELL and COORD strings.
    """
    # Extract lattice parameters
    lattice = structure.lattice.matrix
    
    # Format CELL section
    cell_str = "&CELL\n"
    cell_str += f"    A   {lattice[0][0]:.10f}  {lattice[0][1]:.10f}  {lattice[0][2]:.10f}\n"
    cell_str += f"    B   {lattice[1][0]:.10f}  {lattice[1][1]:.10f}  {lattice[1][2]:.10f}\n"
    cell_str += f"    C   {lattice[2][0]:.10f}  {lattice[2][1]:.10f}  {lattice[2][2]:.10f}\n"
    cell_str += "&END CELL\n\n"

    # Format COORD section
    coord_str = "&COORD\n"
    for site in structure:
        element = site.specie.symbol
        x, y, z = site.coords
        coord_str += f"{element:<2}  {x:.10f}  {y:.10f}  {z:.10f}\n"
    coord_str += "&END COORD\n"

    # Combine CELL and COORD sections
    cp2k_cell_coord = cell_str + coord_str
    return cp2k_cell_coord

from pymatgen.core.structure import Structure


def structure_to_cp2k_kind_section(structure, gth_pot_file=in_pc_PotDir, basis_file=in_pc_basisDir):
    """
    Parse GTH_POTENTIALS and BASIS_MOLOPT files to generate CP2K KIND sections from a pymatgen Structure.

    Args:
        structure (pymatgen.core.structure.Structure): Pymatgen structure object.
        gth_pot_file (str): Path to the GTH_POTENTIALS file.
        basis_file (str): Path to the BASIS_MOLOPT file.

    Returns:
        str: CP2K formatted KIND sections.
    """

    # Raise error if any required variable is still missing
    required_vars = {'in_pc_PotDir': in_pc_PotDir, 'in_pc_basisDir': in_pc_basisDir}
    missing_vars = [k for k, v in required_vars.items() if v is None]
    
    if missing_vars:
        error_message = (
            f"Missing required global variables: {', '.join(missing_vars)}\n\n"
            "'in_pc_PotDir' and 'in_pc_basisDir' must be set.\n\n"
            r"jh.set_global_variables("
            r"pyFunc_pot_dir=r\"G:\My Drive\KUET\CP2K\jupyter_notebook_codes\cp2k codes\GTH_POTENTIALS\"",
            r"pyFunc_basis_dir=r\"G:\My Drive\KUET\CP2K\jupyter_notebook_codes\cp2k codes\BASIS_MOLOPT\""
            r")\n"
        )
        
        print(error_message)
        raise RuntimeError(error_message)



    # Extract unique elements from the structure
    elements = sorted(set(site.specie.symbol for site in structure))


    # Read GTH potentials and basis sets
    with open(in_pc_PotDir, "r") as f:
        gth_data = f.readlines()

    with open(in_pc_basisDir, "r") as f:
        basis_data = f.readlines()

    # Initialize the KIND sections
    kind_sections = ""

    # Loop through each element
    for element in elements:
        # Find GTH potential for the element
        gth_potential = None
        for i, line in enumerate(gth_data):
            if line.startswith(element):
                gth_potential = line.split()[1]
                break

        # Find Basis Set for the element
        basis_set = None
        for i, line in enumerate(basis_data):
            if line.startswith(element):
                basis_set = line.split()[1]
                break

        # Error handling if potential or basis is not found
        if gth_potential is None:
            raise ValueError(f"Potential not found for element: {element} in {gth_pot_file}")
        if basis_set is None:
            raise ValueError(f"Basis set not found for element: {element} in {basis_file}")

        # Generate KIND section
        kind_section = f"""&KIND {element}
    POTENTIAL {gth_potential}
    BASIS_SET {basis_set}
&END KIND

"""
        kind_sections += kind_section

    return kind_sections

###### Define few Alias of the function, so that I dont have to remember the exact name of the original function ############
structure_to_cp2k_kind=structure_to_cp2k_kind_section
#############################################################################################################################


#############################################################################################################
#############################################################################################################
#############################################################################################################


import os
def generate_GeoOpt_script_cp2k(material_name, material_ID, unit_cell_size, label='bulk', CH=0, cell_and_coord="", kind="", 
                                k_point_scheme="MONKHORST-PACK 2 2 2", output_path='Default'):

    from cp2k_script_generator import cp2k_PotDir, cp2k_basisDir, GeoOpt_template_path
    # Raise error if any required variable is still missing
    required_vars = {'cp2k_PotDir': cp2k_PotDir, 'cp2k_basisDir': cp2k_basisDir, 'GeoOpt_template_path': GeoOpt_template_path}
    missing_vars = [k for k, v in required_vars.items() if v is None]
    
    if missing_vars:
        error_message = (
            f"Missing required global variables: {', '.join(missing_vars)}\n\n"
            "Please set these variables using the 'set_global_variables()' function. Example:\n\n"
            "import jh_pymatgen as jh\n"
            "jh.set_global_variables(\n"
            "    cp2k_pot_dir=\"/home/nka/cp2k/Basis_and_Potentials/GTH_POTENTIALS\",\n"
            "    cp2k_basis_dir=\"/home/nka/cp2k/Basis_and_Potentials/BASIS_MOLOPT\",\n"
            "    template_GeoOpt=r\"G:\\My Drive\\KUET\\CP2K\\jupyter_notebook_codes\\cp2k codes\\GeoOpt_KUET - template.sh\"\n"
            ")\n"
        )
        
        print(error_message)
        raise RuntimeError(error_message)
    
    if isinstance(unit_cell_size, tuple):
        unit_cell_size=''.join(map(str, unit_cell_size))

    if output_path == 'Default':
        output_path = os.path.join(os.getcwd(), f"GeoOpt_{material_ID}_{material_name}_{unit_cell_size}_{label}_Ch_{str(CH)}.sh")
    
    with open(GeoOpt_template_path, 'r') as file:
        template = file.read()

    replacements = {
        "${material_name_placeholder}": material_name,
        "${material_ID_placeholder}": material_ID,         
        "${unit_cell_size_placeholder}": unit_cell_size,
        "${label_placeholder}": label,
        "${CH_placeholder}": str(CH),
        "${directory_potential_file}": cp2k_PotDir,
        "${directory_basis_file}": cp2k_basisDir,
        "${k-point_scheme_placeholder}": k_point_scheme,
        "${CELL and COORD placeholder}": cell_and_coord,
        "${KIND placeholder}": kind,
        "${input_placeholder}": f"Geo_Opt_{material_ID}_{material_name}_{unit_cell_size}_{label}_Ch_{str(CH)}"
    }
    
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    with open(output_path, 'w') as file:
        file.write(template)
    
    print(f"CP2K input script generated: {output_path}")





#############################################################################################################
#############################################################################################################


import os

def generate_NEB_script_cp2k(material_name, material_ID, unit_cell_size, label='bulk', CH=0, cell_and_coord="", kind="",replica="", 
                NEB_points=10,k_point_scheme="MONKHORST-PACK 2 2 2",output_path='Default'):
    

    from cp2k_script_generator import cp2k_PotDir, cp2k_basisDir, NEB_template_path
    
    # Raise error if any required variable is still missing
    required_vars = {'cp2k_PotDir': cp2k_PotDir, 'cp2k_basisDir': cp2k_basisDir, 'NEB_template_path': NEB_template_path}
    missing_vars = [k for k, v in required_vars.items() if v is None]
    if missing_vars:
        error_message = (
            f"Missing required global variables: {', '.join(missing_vars)}\n\n"
            "Please set these variables using the 'set_global_variables()' function. Example:\n\n"
            "import jh_pymatgen as jh\n"
            "jh.set_global_variables(\n"
            "    cp2k_pot_dir=\"/home/nka/cp2k/Basis_and_Potentials/GTH_POTENTIALS\",\n"
            "    cp2k_basis_dir=\"/home/nka/cp2k/Basis_and_Potentials/BASIS_MOLOPT\",\n"
            "    template_GeoOpt=r\"G:\\My Drive\\KUET\\CP2K\\jupyter_notebook_codes\\cp2k codes\\GeoOpt_KUET - template.sh\"\n"
            "    template_NEB=r\"G:\\My Drive\\KUET\\CP2K\\jupyter_notebook_codes\\cp2k codes\\NEB_KUET - template.sh\"\n"
            ")\n"
        )
        
        # Print only the error message without the traceback
        print(error_message)
        raise RuntimeError(error_message)


    if isinstance(unit_cell_size, tuple):
        unit_cell_size=''.join(map(str, unit_cell_size))

    if output_path =='Default':
        output_path = os.path.join(os.getcwd(), f"NEB_{material_ID}_{material_name}_{unit_cell_size}_{label}_Ch_{str(CH)}.sh")
    
    with open(NEB_template_path, 'r') as file:
        template = file.read()

    replacements = {
        "${NEB_points_placeholder}":str(NEB_points),
        "${material_name_placeholder}": material_name,
        "${material_ID_placeholder}": material_ID,         
        "${unit_cell_size_placeholder}": unit_cell_size,
        "${label_placeholder}":label,
        "${CH_placeholder}": str(CH),
        "${directory_potential_file}": cp2k_PotDir,
        "${directory_basis_file}": cp2k_basisDir,
        "${k-point_scheme_placeholder}": k_point_scheme,
        "${CELL and COORD placeholder}": cell_and_coord,
        "${KIND placeholder}": kind,
        "${REPLICA_placeholder}":replica,
        "${input_placeholder}":f"NEB_{material_ID}_{material_name}_{unit_cell_size}_{label}_Ch_{str(CH)}"
    }
    
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    with open(output_path, 'w') as file:
        file.write(template)
    
    print(f"CP2K input script generated: {output_path}")


def generate_SCF_P_script_after_NEB(material_name, material_ID, unit_cell_size, label='bulk', replica_files_loc=None, output_path='Default'):
    

    from cp2k_script_generator import cp2k_PotDir, cp2k_basisDir, SCF_P_template_path
    
    # Raise error if any required variable is still missing
    required_vars = {'SCF_P_template_path': SCF_P_template_path, 'cp2k_basisDir': cp2k_basisDir, 'NEB_template_path': NEB_template_path}
    missing_vars = [k for k, v in required_vars.items() if v is None]
    if missing_vars:
        error_message = (
            f"Missing required global variables: {', '.join(missing_vars)}\n\n"
            "Please set these variables using the 'set_global_variables()' function. Example:\n\n"
            "import jh_pymatgen as jh\n"
            "jh.set_global_variables(\n"
            "    cp2k_pot_dir=\"/home/nka/cp2k/Basis_and_Potentials/GTH_POTENTIALS\",\n"
            "    cp2k_basis_dir=\"/home/nka/cp2k/Basis_and_Potentials/BASIS_MOLOPT\",\n"
            "    SCF_P_template_path=r\"G:\\My Drive\\KUET\\CP2K\\jupyter_notebook_codes\\cp2k codes\\Polarization_KUET - template.sh\"\n"
            ")\n"
        )
        
        # Print only the error message without the traceback
        print(error_message)
        raise RuntimeError(error_message)
    if replica_files_loc is None:
        raise RuntimeError("You must supply the 'replica_files_loc'. This is the directory where you run the NEB, and the generated replicas are located.")

    if isinstance(unit_cell_size, tuple):
        unit_cell_size=''.join(map(str, unit_cell_size))

    if output_path =='Default':
        output_path = os.path.join(os.getcwd(), f"SCF_P_{material_ID}_{material_name}_{unit_cell_size}_{label}_Ch_{str(CH)}.sh")
    
    with open(NEB_template_path, 'r') as file:
        template = file.read()

    replacements = {
        "${material_name_placeholder}": material_name,
        "${material_ID_placeholder}": material_ID,         
        "${unit_cell_size_placeholder}": unit_cell_size,
        "${label_placeholder}":label,
        "${CH_placeholder}": str(CH),
        "${replica_files_loc_placeholder}":replica_files_loc,
        "${directory_potential_file}": cp2k_PotDir,
        "${directory_basis_file}": cp2k_basisDir,
        "${k-point_scheme_placeholder}": k_point_scheme,
        #"${CELL and COORD placeholder}": cell_and_coord,
        "${KIND placeholder}": kind,
        #"${REPLICA_placeholder}":replica,
        "${input_placeholder}":f"NEB_{material_ID}_{material_name}_{unit_cell_size}_{label}_Ch_{str(CH)}"
    }
    
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    with open(output_path, 'w') as file:
        file.write(template)
    
    print(f"CP2K input script generated: {output_path}")



###############################################################################################################################
###############################################################################################################################

import os
import re
from pymatgen.core import Structure, Lattice, Element
import re
def cp2k_to_structure_ReDefined_in_this_file(cp2k_input_fileName):        #cp2k_to_structure() function is defined in structure_process.py. 
                                                                          #It is redefined again to avoid dependency.
    with open(cp2k_input_fileName, "r") as f:
        cp2k_input_str = f.read()
    
    # Extract lattice vectors from the CELL section
    cell_match = re.findall(r'&CELL([\s\S]*?)&END CELL', cp2k_input_str)
    if not cell_match:
        raise ValueError("CELL section not found in CP2K input.")
    
    cell_lines = cell_match[0].strip().split('\n')
    lattice_vectors = []
    for line in cell_lines:
        if line.strip().startswith(('A', 'B', 'C')):
            lattice_vectors.append([float(x) for x in line.split()[1:]])
    
    if len(lattice_vectors) != 3:
        raise ValueError("Incomplete CELL section in CP2K input.")
    
    # Create Lattice object
    lattice = Lattice(lattice_vectors)

    # Extract atomic coordinates from the COORD section
    coord_match = re.findall(r'&COORD([\s\S]*?)&END COORD', cp2k_input_str)
    if not coord_match:
        raise ValueError("COORD section not found in CP2K input.")
    
    coord_lines = coord_match[0].strip().split('\n')
    species = []
    coords = []
    
    for line in coord_lines:
        parts = line.split()
        if len(parts) >= 4:
            species.append(parts[0])
            coords.append([float(x) for x in parts[1:4]])
    
    # Create Structure object with Cartesian coordinates
    structure = Structure(lattice, species, coords, coords_are_cartesian=True)

    return structure


def get_NEB_items_after_GeoOpt(*directories):
    #A geometry optimization run creates a cpki file and a pdb file. The information from those files can be used in NEB simulation.
    #This function extracts the required informations from the files generated by a Geometry Optimization run.
    #
    #For example, you run a 
    #          geometry optimization of structure-1 in directory-1
    #          geometry optimization of structure-2 in directory-2
    # Then you call the function:    get_replicas_from_pdb_files_and_cell_coord_from_cpki(directory-1,directory-2)
    
    def get_structure_and_cell_coord_from_cpki_file(directory):
        cpki_file = None
        for file in os.listdir(directory):
            if file.endswith(".cpki"):
                cpki_file = os.path.join(directory, file)
                break
    
        if not cpki_file:
            print("No cpki file found in the directory:", directory)
            return ""
        print("Reading", cpki_file)
        
        structure=cp2k_to_structure_ReDefined_in_this_file(cpki_file)
        cp2k_cell_coord=structure_to_cp2k_cell_coord(structure)
        
        return structure,cp2k_cell_coord
    
    def get_one_replica_from_pdb_file(directory):
        pdb_file = None
        for file in os.listdir(directory):
            if file.endswith(".pdb"):
                pdb_file = os.path.join(directory, file)
                break
        
        if not pdb_file:
            print("No PDB file found in the directory.")
            return ""
        
        print("Reading", pdb_file)
        with open(pdb_file, 'r') as file:
            lines = file.readlines()
        
        last_coords = []
        inside_last_step = False
    
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("ATOM"):
                inside_last_step = True
                parts = lines[i].split()
                coord = f"{parts[3]} {parts[4]} {parts[5]}"
                last_coords.append(coord)
            elif inside_last_step and lines[i].startswith("REMARK"):
                break
    
        last_coords.reverse()
    
        replica_coords = "    &REPLICA\n"
        replica_coords += "      &COORD\n"
        for coord in last_coords:
            replica_coords += f"         {coord}\n"
        replica_coords += "      &END COORD\n"
        replica_coords += "    &END REPLICA\n\n"
    
        return replica_coords
        
    All_replica_coord=""
    cp2k_cell_coord=""
    for directory in directories:
        if not cp2k_cell_coord:
            structure,cp2k_cell_coord=get_structure_and_cell_coord_from_cpki_file(directory)
            kind=structure_to_cp2k_kind(structure)

        tmp=get_one_replica_from_pdb_file(directory)
        All_replica_coord=All_replica_coord+tmp

    print("\tReturning Structure, &CELL, &COORD, &KIND from cpki file\n\tReturning &REPLICA from pdb files...")
    return structure,cp2k_cell_coord,kind,All_replica_coord
