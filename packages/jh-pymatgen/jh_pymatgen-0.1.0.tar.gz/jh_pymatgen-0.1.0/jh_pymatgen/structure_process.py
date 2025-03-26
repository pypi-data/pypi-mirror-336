
# ######################################################################################################
# ######################################################################################################
from mp_api.client import MPRester
#This function will download cif files.
#download_cif('mp-149', 'mp-150', 'mp-151')
def download_cif(*mpids,api_key=None):
    if api_key is None:
        error_message = (
            "'api_key' is missing. Please provide api_key. Usage: \n"
            "api_key='<your key>'\n"
            "download_cif('mp-149', 'mp-150', 'mp-151', api_key=api_key)"
        )
        raise RuntimeError(error_message)
    
    # Initialize MPRester with the API key
    with MPRester(api_key) as mpr:
        for mpid in mpids:
            # Fetch the structure corresponding to the MPID
            docs = mpr.materials.search(material_ids=[mpid], fields=["structure"])
        
            # Check if the response contains the structure
            if docs:
                structure = docs[0].structure
            
                # Write the structure to a CIF file
                cif_filename = f"{mpid}.cif"
                structure.to(fmt="cif", filename=cif_filename)
                print(f"CIF file for {mpid} downloaded and saved as {cif_filename}")
            else:
                print(f"No structure found for material id {mpid}")
######################################################################################################
######################################################################################################

# import matplotlib.pyplot as plt
# colors = plt.get_cmap('tab20')
# # Function to create the color dictionary
# def generate_element_colors(elements):
#     element_colors = {}
#     num_elements = len(elements)
    
#     # Generate a color for each element using the colormap
#     for i, element in enumerate(elements):
#         color = colors(i / num_elements)  # Normalize i to get a range between 0 and 1
#         # Convert the color from RGBA to hexadecimal format
#         hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]*255), int(color[1]*255), int(color[2]*255))
#         element_colors[element] = hex_color
    
#     return element_colors

# # Example usage:
# elements = ["H", "Hf", "Zr", "Si", "La", "Y", "Nb", "Ta", "W", "Ti", "N", "O", "C", "P"]
# element_colors = generate_element_colors(elements)



element_colors = {
    "H": "#d9d9d9",  # Light Gray
    "Hf": "#1f77b4",  # Blue
    "Zr": "#ff7f0e",  # Orange
    "Si": "#bcbd22",  # Olive Green
    "La": "#e377c2",  # Pink
    "Y": "#9467bd",   # Purple
    "Nb": "#8c564b",  # Brown
    "Ta": "#17becf",  # Cyan
    "W": "#7f7f7f",   # Dark Gray
    "Ti": "#2ca02c",  # Green
    "N": "#9e2a2f",   # Dark Red (changed from bright red to a more subdued tone)
    "O": "#ff9896"    # Light Red
}

def set_element_colors(color_dict="Default"):
    global element_colors
    if color_dict != "Default":
        element_colors = color_dict

def print_color_dict():
    print(element_colors)


from pymatgen.io.cif import CifParser
import py3Dmol
from IPython.display import display  # Needed for Jupyter Notebook


def visualize_structure(FileName, face='z', width=800, height=500, axis_offset=5, axis_length=10):
    viewer = py3Dmol.view(width=width, height=height)
    from jh_pymatgen.structure_process import element_colors             #Importing the global element colors dictionary.
    
    # Check if the input is a Structure or string
    structure = None  # Initialize structure
    structure=get_structure(FileName)  #The get_structure function takes various FileName as input, then extract and return pymatgen structure.
    
    cif_str = structure.to(fmt="cif")  # Convert to structure format string
    viewer.addModel(cif_str, "cif")
        
    # Extract lattice parameters (a, b, c) after checking for structure
    if structure:
        a, b, c = structure.lattice.abc
    else:
        raise ValueError("Structure not found in input CIF data")


    # Apply visualization style with stick and sphere sizes adjusted
    viewer.setStyle({"stick": {"radius": 0.15}, "sphere": {"scale": 0.4}})  # Adjusted stick radius

    # Extract unique elements from the structure
    if structure:
        elements = sorted(set(site.specie.symbol for site in structure.sites))

        # Apply colors to the atoms in the structure based on element_colors
        for el in elements:
            color = element_colors.get(el, "gray")  # Default to gray if not found
            viewer.setStyle({"elem": el}, {"sphere": {"radius": 0.5, "color": color}, "stick": {"radius": 0.15}})  # Stick radius set smaller

        # Assign colors for the legend
        legend_colors = [element_colors.get(el, "gray") for el in elements]

        # Dynamically calculate legend offset based on lattice dimensions
        legend_offset = max(a, b, c) / 2 + 5  # Position the legend outside the structure

        # Add element legend at the top-right corner, dynamically shifted
        for i, (el, color) in enumerate(zip(elements, legend_colors)):
            viewer.addSphere({
                "center": {"x": axis_offset + legend_offset, "y": legend_offset - i * 2, "z": 0},
                "radius": 0.6,
                "color": color
            })
            viewer.addLabel(f"{el}", {
                "position": {"x": axis_offset + legend_offset + 2, "y": legend_offset - i * 2, "z": 0},
                "fontColor": "black",
                "backgroundColor": "white",
                "fontSize": 12,
                "alignment": "left"
            })
    
    # Move the axes away from the structure using an offset
    origin = {"x": -axis_offset, "y": -axis_offset, "z": -axis_offset}
    
    # X-axis (Red)
    viewer.addArrow({
        "start": origin,
        "end": {"x": origin["x"] + axis_length, "y": origin["y"], "z": origin["z"]},
        "color": "red",
        "radius": 0.2
    })
    viewer.addLabel(f"X (a = {a:.2f} Å)", {
        "position": {"x": origin["x"] + axis_length + 1, "y": origin["y"], "z": origin["z"]},
        "fontColor": "red",
        "backgroundColor": "white",
        "fontSize": 12,
        "alignment": "center"
    })
    
    # Y-axis (Green)
    viewer.addArrow({
        "start": origin,
        "end": {"x": origin["x"], "y": origin["y"] + axis_length, "z": origin["z"]},
        "color": "green",
        "radius": 0.2
    })
    viewer.addLabel(f"Y (b = {b:.2f} Å)", {
        "position": {"x": origin["x"], "y": origin["y"] + axis_length + 1, "z": origin["z"]},
        "fontColor": "green",
        "backgroundColor": "white",
        "fontSize": 12,
        "alignment": "center"
    })
    
    # Z-axis (Blue)
    viewer.addArrow({
        "start": origin,
        "end": {"x": origin["x"], "y": origin["y"], "z": origin["z"] + axis_length},
        "color": "blue",
        "radius": 0.2
    })
    viewer.addLabel(f"Z (c = {c:.2f} Å)", {
        "position": {"x": origin["x"], "y": origin["y"], "z": origin["z"] + axis_length + 1},
        "fontColor": "blue",
        "backgroundColor": "white",
        "fontSize": 12,
        "alignment": "center"
    })
    
    # Draw unit cell border
    lattice = structure.lattice.matrix
    vertices = [
        [0, 0, 0],  # Origin
        lattice[0],  # a
        lattice[1],  # b
        lattice[2],  # c
        lattice[0] + lattice[1],  # a + b
        lattice[0] + lattice[2],  # a + c
        lattice[1] + lattice[2],  # b + c
        lattice[0] + lattice[1] + lattice[2],  # a + b + c
    ]
    
    # Draw lines to form unit cell
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 5),
        (2, 4), (2, 6),
        (3, 5), (3, 6),
        (4, 7), (5, 7), (6, 7),
    ]
    
    for start, end in edges:
        viewer.addLine({
            "start": {"x": vertices[start][0], "y": vertices[start][1], "z": vertices[start][2]},
            "end": {"x": vertices[end][0], "y": vertices[end][1], "z": vertices[end][2]},
            "color": "black",
            "radius": 0.1
        })


    # Adjust view based on the selected face
    if face == 'x':  
        viewer.rotate(90, 'y')  # Rotate to view perpendicular to YZ plane
    elif face == 'y':  
        viewer.rotate(90, 'x')  # Rotate to view perpendicular to XZ plane
    elif face == 'z':  
        viewer.rotate(0, 'z')   # Default view (perpendicular to XY plane)
    # Center and zoom
    viewer.zoomTo()
    
    # ✅ Properly renders in Jupyter Notebook
    display(viewer)


###### Define few Alias of the function, so that I dont have to remember the exact name of the original function ############
visualize=visualize_structure
#############################################################################################################################
def visualize_with_deleted_atoms(original_structure, modified_structure, face='z', remove_bond=False, width=800, height=500, axis_offset=5, axis_length=10):
    viewer = py3Dmol.view(width=width, height=height)

    from jh_pymatgen.structure_process import element_colors             #Importing the global element colors dictionary.

    if not isinstance(original_structure, Structure) or not isinstance(modified_structure, Structure):
        raise TypeError("Both inputs must be pymatgen Structure objects. To get this, you can use 'create_supercell()' or 'get_structure()' function.")

    # Detect deleted atoms
    original_coords = {tuple(site.frac_coords) for site in original_structure}
    modified_coords = {tuple(site.frac_coords) for site in modified_structure}
    deleted_coords = original_coords - modified_coords

    if remove_bond:
        cif_str = modified_structure.to(fmt="cif")
        opacity = 0.7
    else:
        cif_str = original_structure.to(fmt="cif")
        opacity = 1

    viewer.addModel(cif_str, "cif")

    # Extract lattice parameters
    if original_structure:
        a, b, c = original_structure.lattice.abc
    else:
        raise ValueError("Structure not found in input CIF data")

    # Apply visualization style
    viewer.setStyle({"stick": {"radius": 0.15}, "sphere": {"scale": 0.4}})

    # Extract unique elements from the structure
    elements = sorted(set(site.specie.symbol for site in original_structure.sites))

    # Apply colors to the atoms
    for el in elements:
        color = element_colors.get(el, "gray")
        viewer.setStyle({"elem": el}, {"sphere": {"radius": 0.5, "color": color}, "stick": {"radius": 0.15}})

    ################# Assign legend colors ###########################################
    legend_colors = [element_colors.get(el, "gray") for el in elements]
    legend_offset = max(a, b, c) / 2 + 5

    for i, (el, color) in enumerate(zip(elements, legend_colors)):
        viewer.addSphere({
            "center": {"x": axis_offset + legend_offset, "y": legend_offset - i * 2, "z": 0},
            "radius": 0.6,
            "color": color
        })
        viewer.addLabel(f"{el}", {
            "position": {"x": axis_offset + legend_offset + 2, "y": legend_offset - i * 2, "z": 0},
            "fontColor": "black",
            "backgroundColor": "white",
            "fontSize": 12,
            "alignment": "left"
        })

    ################################# Highlight deleted atoms ###################################
    # Color map for deleted atoms
    import matplotlib as plt
    deleted_elements = sorted(set(site.specie.symbol for site in original_structure if tuple(site.frac_coords) in deleted_coords))
    deleted_colors = plt.pyplot.get_cmap('Set2')

    original_indices = list(range(len(original_structure)))
    color_map = {el: 'red' if len(deleted_elements) == 1 else plt.colors.rgb2hex(deleted_colors(i)[:3]) for i, el in enumerate(deleted_elements)}

    for site, index in zip(original_structure, original_indices):
        if tuple(site.frac_coords) in deleted_coords:
            i += 1
            deleted_element = site.specie.symbol
            color = color_map.get(deleted_element, 'red')
            viewer.addSphere({
                "center": {"x": site.x, "y": site.y, "z": site.z},
                "radius": 0.6,
                "color": color,
                "opacity": opacity
            })
            # Add legend for deleted atoms
            viewer.addSphere({
                "center": {"x": axis_offset + legend_offset, "y": legend_offset - i * 2, "z": 0},
                "radius": 0.6,
                "color": color,
                "opacity": opacity
            })
            viewer.addLabel(f"Del {deleted_element} [{index}]", {
                "position": {"x": axis_offset + legend_offset + 2, "y": legend_offset - i * 2, "z": 0},
                "fontColor": "black",
                "backgroundColor": "white",
                "fontSize": 12,
                "alignment": "left"
            })
      
    ############################# Adding Arrows ###########################################
    # Move the axes away from the structure using an offset
    origin = {"x": -axis_offset, "y": -axis_offset, "z": -axis_offset}
    
    # X-axis (Red)
    viewer.addArrow({
        "start": origin,
        "end": {"x": origin["x"] + axis_length, "y": origin["y"], "z": origin["z"]},
        "color": "red",
        "radius": 0.2
    })
    viewer.addLabel(f"X (a = {a:.2f} Å)", {
        "position": {"x": origin["x"] + axis_length + 1, "y": origin["y"], "z": origin["z"]},
        "fontColor": "red",
        "backgroundColor": "white",
        "fontSize": 12,
        "alignment": "center"
    })
    
    # Y-axis (Green)
    viewer.addArrow({
        "start": origin,
        "end": {"x": origin["x"], "y": origin["y"] + axis_length, "z": origin["z"]},
        "color": "green",
        "radius": 0.2
    })
    viewer.addLabel(f"Y (b = {b:.2f} Å)", {
        "position": {"x": origin["x"], "y": origin["y"] + axis_length + 1, "z": origin["z"]},
        "fontColor": "green",
        "backgroundColor": "white",
        "fontSize": 12,
        "alignment": "center"
    })
    
    # Z-axis (Blue)
    viewer.addArrow({
        "start": origin,
        "end": {"x": origin["x"], "y": origin["y"], "z": origin["z"] + axis_length},
        "color": "blue",
        "radius": 0.2
    })
    viewer.addLabel(f"Z (c = {c:.2f} Å)", {
        "position": {"x": origin["x"], "y": origin["y"], "z": origin["z"] + axis_length + 1},
        "fontColor": "blue",
        "backgroundColor": "white",
        "fontSize": 12,
        "alignment": "center"
    })
    
    ############################## Draw unit cell border ########################################### 
    lattice = original_structure.lattice.matrix
    vertices = [
        [0, 0, 0],  # Origin
        lattice[0],  # a
        lattice[1],  # b
        lattice[2],  # c
        lattice[0] + lattice[1],  # a + b
        lattice[0] + lattice[2],  # a + c
        lattice[1] + lattice[2],  # b + c
        lattice[0] + lattice[1] + lattice[2],  # a + b + c
    ]
    
    # Draw lines to form unit cell
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 5),
        (2, 4), (2, 6),
        (3, 5), (3, 6),
        (4, 7), (5, 7), (6, 7),
    ]
    
    for start, end in edges:
        viewer.addLine({
            "start": {"x": vertices[start][0], "y": vertices[start][1], "z": vertices[start][2]},
            "end": {"x": vertices[end][0], "y": vertices[end][1], "z": vertices[end][2]},
            "color": "black",
            "radius": 0.1
        })


    ############################ Adjust view based on the selected face ################################
    if face == 'x':  
        viewer.rotate(90, 'y')  # Rotate to view perpendicular to YZ plane
    elif face == 'y':  
        viewer.rotate(90, 'x')  # Rotate to view perpendicular to XZ plane
    elif face == 'z':  
        viewer.rotate(0, 'z')   # Default view (perpendicular to XY plane)
    # Center and zoom
    viewer.zoomTo()
    
    # ✅ Properly renders in Jupyter Notebook
    display(viewer)



# Import required libraries
from pymatgen.io.cif import CifParser
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer  # Correct import path

def create_supercell(FileName, multiplication_factors):
    """
    Creates a supercell from a CIF string or pymatgen Structure, converts it to the standard unit cell,
    and applies the provided multiplication factors.

    Args:
    - cif_data_or_structure (str or Structure): A CIF string or a pymatgen Structure object.
    - multiplication_factors (tuple): A tuple (x, y, z) that defines the supercell's size in each direction.

    Returns:
    - Structure: The resulting supercell as a pymatgen Structure object.
    """
        
    standard_structure=get_structure(FileName) #The get_structure function takes various FileName as input, then extract and return pymatgen structure.
    
    # 1. Convert to the Standard Unit Cell (using SpacegroupAnalyzer)
    sg_analyzer = SpacegroupAnalyzer(standard_structure)
    standard_structure = sg_analyzer.get_conventional_standard_structure()
    
    # 2. Create a Supercell (e.g., 2x2x2 supercell)
    supercell_matrix = [[multiplication_factors[0], 0, 0], 
                        [0, multiplication_factors[1], 0],
                        [0, 0, multiplication_factors[2]]]  # 2x2x2 supercell
    supercell = standard_structure * supercell_matrix
    
    return supercell
###### Define few Alias of the function, so that I dont have to remember the exact name of the original function ############
supercell=create_supercell
#############################################################################################################################

from pymatgen.core import Structure, Lattice
import numpy as np
def stack_structures(structure_1, structure_2, axis='z', interlayer_dist='Default'):
    """
    Stacks two supercells along a specified axis to create a combined supercell with adjustable interlayer distance.

    Args:
    - structure_1 (Structure): First supercell as a pymatgen Structure object.
    - structure_2 (Structure): Second supercell as a pymatgen Structure object.
    - axis (str): Axis to stack along ('x', 'y', or 'z'). Default is 'z'.
    - interlayer_dist (float): Desired interlayer distance in Ångströms. If None, defaults to the lattice vector shift.

    Returns:
    - Structure: The stacked structure as a pymatgen Structure object.
    - float: The applied interlayer distance.
    """
    if not isinstance(structure_1, Structure) or not isinstance(structure_2, Structure):
        raise TypeError("Both inputs must be pymatgen Structure objects. To get this, you can use 'create_supercell()' or 'get_structure()' function.")
    
    # Get lattice matrices
    lattice1 = structure_1.lattice.matrix
    lattice2 = structure_2.lattice.matrix
    #Lattice matrix shape:
    #[a   0    0,
    #0     b   0,
    #0     0    c]

    # Determine stacking axis index
    axis_index = {'x': 0, 'y': 1, 'z': 2}.get(axis, 2)

    # Calculate the default interlayer distance
    max_structure_1 = max(site.coords[axis_index] for site in structure_1)   # Finding maximum coordinate of the atoms present in structure_1
    min_structure_2 = min(site.coords[axis_index] for site in structure_2)   # Finding minimum coordinate of the atoms present in structure_2
    default_interlayer_distance = lattice1[axis_index][axis_index] + (min_structure_2 - max_structure_1)
    # For 'y-axis', axis_index=1.
    #lattice1[axis_index]=[0    b    0]
    #lattice1[axis_index][axis_index]=b

    
    # Use specified interlayer distance, or fall back to the default
    if isinstance(interlayer_dist, str):   
        #Value of interlayer_dist is either a float or "Default". Therefore if it is a str, I must use a default value   
        #if interlayer_dist =='Default':
        interlayer_dist = default_interlayer_distance

    # Expand lattice along the specified axis according to the chosen interlayer distance
    new_lattice = np.array(lattice1)
    new_lattice[axis_index] += lattice2[axis_index]  # Initial stacking
    new_lattice[axis_index][axis_index] += interlayer_dist - default_interlayer_distance  # Adjust lattice size

    # Create new structure with the combined lattice
    stacked_structure = Structure(Lattice(new_lattice), [], [])

    # Add all sites from structure_1
    # Keep the atoms of structure_1 at their original position
    for site in structure_1:
        stacked_structure.append(site.specie, site.coords, coords_are_cartesian=True)


    ########## Creating a temporary structure_2. I will shift the coordinate of the atoms in it.######
    tmp_structure_2=structure_2.copy()
    tmp_structure_2.clear()   #Clear the structure completely. Then update the sites again in the for loop
    #Now this is an empty structure. No atom is present in this structure.
    #################################################################################################

    # Shift the atoms of structure_2 by a translation operation.
    # Then add them in the stacked_structure
    for site in structure_2:
        new_coords_structure_2 = site.coords.copy()
        new_coords_structure_2[axis_index] += max_structure_1 + interlayer_dist - min_structure_2
        stacked_structure.append(site.specie, new_coords_structure_2, coords_are_cartesian=True)

        #Also store the site information (atomic specis and their shifted-coordinates) in previously emptied structure.
        #From this, the interlayer distance will be computed later
        tmp_structure_2.append(site.specie, new_coords_structure_2, coords_are_cartesian=True)


    # ######## Compute interlayer distance ##########
    max_structure_1 = max(site.coords[axis_index] for site in structure_1)
    min_structure_2 = min(site.coords[axis_index] for site in tmp_structure_2)
    interlayer_distance = min_structure_2 - max_structure_1
    print(f"Interlayer distance: {interlayer_distance:.3f} \u212B")


    return stacked_structure

###### Define few Alias of the function, so that I dont have to remember the exact name of the original function ############
stack=stack_structures
#############################################################################################################################



######################################################################################################
######################################################################################################
from pymatgen.io.cif import CifParser
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer  # Correct import path

def get_structure_from_cif(cif_filename):
    # Load structure from CIF file
    parser = CifParser(cif_filename)
    structure = parser.parse_structures(primitive=True)[0]  # Equivalent to old behavior
    return structure

from pymatgen.core import Structure, Lattice, Element
import re
def cp2k_to_structure(cp2k_input_fileName, return_cell_section_only=False,return_lattice_only=False):
    with open(cp2k_input_fileName, "r") as f:
        cp2k_input_str = f.read()
    
    # Extract the content between &SUBSYS and &END SUBSYS
    subsys_match = re.findall(r'&SUBSYS([\s\S]*?)&END SUBSYS', cp2k_input_str)
    if not subsys_match:
        raise ValueError("&SUBSYS section not found in CP2K input.")
    
    subsys_str = subsys_match[0]  # This is the valid section
    
    # Extract lattice vectors from the CELL section
    cell_match = re.findall(r'&CELL([\s\S]*?)&END CELL', subsys_str)
    if not cell_match:
        raise ValueError("CELL section not found in CP2K input.")

    if return_cell_section_only:
        return cell_match
    
    cell_lines = cell_match[0].strip().split('\n')
    lattice_vectors = []
    for line in cell_lines:
        if line.strip().startswith(('A', 'B', 'C')):
            lattice_vectors.append([float(x) for x in line.split()[1:]])
    
    if len(lattice_vectors) != 3:
        raise ValueError("Incomplete CELL section in CP2K input.")
    
    # Create Lattice object
    lattice = Lattice(lattice_vectors)
    if return_lattice_only:
        return lattice

    # Extract atomic coordinates from the COORD section
    coord_match = re.findall(r'&COORD([\s\S]*?)&END COORD', subsys_str)
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

    structure = Structure(lattice, species, coords, coords_are_cartesian=True)

    return structure


def get_structure(FileName):
    #This function takes various FileName as input, and extract pymatgen structure from that FileName.
    if isinstance(FileName, Structure):
        # If it's already a pymatgen Structure, use it directly
        standard_structure = FileName
    elif isinstance(FileName, str):                #Filename is provided. Have to extract the structure from the filename.
        if FileName.find('.cif')>-1:
            standard_structure=get_structure_from_cif(FileName)
        elif FileName.find('.cpki')>-1:
            standard_structure=cp2k_to_structure(FileName)
    else:
        raise TypeError("Input should be either a CIF string, cpki or a pymatgen Structure")
    return standard_structure




from pymatgen.analysis.local_env import MinimumDistanceNN
from collections import defaultdict

def analyze_bonding(FileName):
    structure=get_structure(FileName) #The get_structure function takes various FileName as input, then extract and return pymatgen structure.
    print("Analysing the structure....")
    mdnn = MinimumDistanceNN()  # Distance-based neighbor finder
    bonding_info = defaultdict(lambda: defaultdict(lambda: {"count": 0, "indices": []}))

    # Analyze each site in the structure
    for i, site in enumerate(structure):
        species = site.specie.symbol
        neighbors = mdnn.get_nn_info(structure, i)
        bond_counts = defaultdict(int)

        for neighbor in neighbors:
            neighbor_species = neighbor['site'].specie.symbol
            bond_counts[neighbor_species] += 1

        # Record unique bonding environments
        bond_signature = tuple(sorted(bond_counts.items()))
        bonding_info[species][bond_signature]["count"] += 1
        bonding_info[species][bond_signature]["indices"].append(i)

    # Generate organized report
    report = "Bonding Analysis Report:\n\n"
    for species, environments in bonding_info.items():
        report += f"Element: {species}\n"
        # Sort environments by species and bond counts for better readability
        sorted_environments = sorted(environments.items(), key=lambda x: (len(x[0]), sorted(x[0])))
        for bond_signature, data in sorted_environments:
            bonds_str = ", ".join(f"{num} - {elem} atoms" for elem, num in bond_signature)
            report += f"\tBonds with {bonds_str}. Total {data['count']} such {species} atoms.\n"
            report += f"\tIndices: {data['indices']}\n\n"
    print(report)


from pymatgen.core import Structure

def delete_atoms_from_structure(FileName, sites=None):
    """
    Deletes atoms from the structure at the specified indices.

    Parameters:
    - FileName (str): Path to the structure file.
    - sites (list or int, optional): List of atom indices to delete, or a single index.

    Returns:
    - Structure: A new pymatgen Structure object with specified atoms removed.
    """
    # Get the structure
    structure = get_structure(FileName)
    
    # Return the original structure if no sites are specified
    if sites is None:
        return structure
    
    # Ensure sites is a list, even if a single index is provided
    if isinstance(sites, int):
        sites = [sites]
    
    # Create a copy of the structure and remove the specified sites
    tmp_structure = structure.copy()
    tmp_structure.remove_sites(sites)
    
    return tmp_structure

###### Define few Alias of the function, so that I dont have to remember the exact name of the original function ############
delete_atoms=delete_atoms_from_structure
#############################################################################################################################

import os
import re

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




    
def get_optimized_images_structures_after_NEB(directory,Print=False):
    All_files=os.listdir(directory)
    
    cpki_file = None
    for file in All_files:
        if file.endswith(".cpki"):
            cpki_file = os.path.join(directory, file)
            if Print:
                print("Reading: ", cpki_file)
            lattice=cp2k_to_structure(cpki_file, return_lattice_only=True)

    
    ################## Now finding coordinates from *Replica_nr_*.xyz Files ################
    # Relaxed pattern to match any file containing "Replica" and ending with ".xyz"
    pattern = re.compile(r".*Replica.*\.xyz$")  
    # List files in directory and filter by pattern
    files = [f for f in All_files if pattern.match(f)]

    # Sort files using sequence number nr_XX if present
    def extract_nr(filename):
        match = re.search(r"nr_(\d+)", filename)
        return int(match.group(1)) if match else float('inf')

    def create_structure_lattice_and_lines(lattice,lines):
        species = []
        coords = []    
        for i in range(len(lines) - 1, -1, -1):
            line=lines[i]
            if line.startswith("i = ") or "E =" in lines[i]:
                break
        
            parts = line.split()
            if len(parts) >= 4:
                species.append(parts[0])
                coords.append([float(x) for x in parts[1:4]])
        species.reverse()
        coords.reverse()
        return Structure(lattice, species, coords, coords_are_cartesian=True)

    
    files.sort(key=extract_nr)
    optimized_replicas={}
    for file in files:
        match = re.search(r"(Replica_nr_\d+)", file)
        string = match.group(1)
        file_path = os.path.join(directory, file)
        if Print:
            print("Reading:", file_path)
    
        with open(file_path, 'r') as f:
            lines = f.readlines()
        structure=create_structure_lattice_and_lines(lattice,lines)
        optimized_replicas[string]=structure

    return optimized_replicas


import ipywidgets as widgets
from IPython.display import display, clear_output
import time

def animate_structures(replicas,face='z', auto_movement=False, interval=100,iteration=3):
    """
    Animates the visualization of structure replicas using a slider or automatic movement.
    
    Parameters:
    - replicas: A dictionary of optimized structure replicas.
    - auto_movement: Boolean to control automatic movement.
    - interval: Interval (in ms) between automatic movements if auto_movement is True.
    """
    
    # Define the output widget to render the 3D structure visualization
    output = widgets.Output()

    # Get the keys from the replicas dictionary
    keys = list(replicas.keys())

    # Create the slider widget for manual navigation
    slider = widgets.IntSlider(
        min=0, max=len(keys) - 1, step=1, value=0, description="Structure: "
    )

    # Function to update the structure based on the slider's value
    def update_view(change):
        # Clear the previous output
        with output:
            output.clear_output(wait=True)
            # Get the structure corresponding to the key at slider.value
            structure = replicas[keys[slider.value]]
            # Call the new custom visualization function
            #new_visualize_structure(structure)
            visualize_structure(structure,face=face)

    # Link the slider to the update function
    slider.observe(update_view, names="value")

    # Display the slider and output widget
    display(slider, output)

    # Initialize the first structure
    with output:
        visualize_structure(replicas[keys[slider.value]])

    # Optionally, auto-move through the replicas if `auto_movement` is True
    if auto_movement:
        for itr in range(iteration):
            for i in range(len(keys)):
                slider.value = i
                time.sleep(interval / 1000)  # Convert ms to seconds



def animate_NEB_images(directory,face='z', interval_ms=100,iteration=3):
    optimized_replicas=get_optimized_images_structures_after_NEB(directory)
    animate_structures(optimized_replicas,face=face, auto_movement=True, interval=interval_ms,iteration=iteration)

############################################################
# Code that is under test stage
############################################################


