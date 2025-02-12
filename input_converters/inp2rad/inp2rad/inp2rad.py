# Copyright 1986-2025 Altair Engineering Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import tkinter as tk
from tkinter import filedialog
import sys
import re
import time
import argparse

#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  GLOBAL VARIABLES SECTION
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
input_file_path = ""
input_file_name = ""
original_lines = []
run_timer = True # run a timer to check the script performance
or_gui = True # if script is being run from or_gui, different messages
start_time = 0
# initialize a variable tracking max modulus to be used as basis of spring 'weld' stiffness
e_magnitude = 10.0
# initialize a variable tracking max density to be used as basis of spring 'weld' mass
rho_magnitude = 1e-9
spotflag_default = 27 #change tied interface spotflag (27, 28 options usually)


debug_mode = False # enables writing of intermediate files for debugging

#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
# Functions to convert aspects of the .inp Model
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|

####################################################################################################
# Function to identify nodes defined in systems                                                    #
####################################################################################################
def convert_transforms(input_lines):
    transform_lines = []
    transform_data = []
    transform_id = 0

    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        if line.lower().startswith('*system id='):
            parts = line.split('=', 1)
            if len(parts) > 1:
                transform_id = parts[1].strip()

            i += 1
            coords_line = input_lines[i].strip()
            if coords_line.startswith("*"):
                transform_id = 0

            else:
                try:
                    coords = [float(coord.strip()) for coord in coords_line.split(',')]
                except ValueError:
                    # Skip lines that cannot be converted to floats
                    i += 1
                    continue

                # Extract the required coordinates
                Xa, Ya, Za = coords[0], coords[1], coords[2]
                Xb, Yb, Zb = coords[3], coords[4], coords[5]

                # Check if there is a second line for the Z-axis direction
                if i + 1 < len(input_lines) and not input_lines[i + 1].startswith('*'):
                    i += 1
                    z_axis_line = input_lines[i].strip()
                    try:
                        z_coords = [float(coord.strip()) for coord in z_axis_line.split(',')]
                        Xc, Yc, Zc = z_coords[0], z_coords[1], z_coords[2]
                    except ValueError:
                        # Default Z-axis direction if not provided
                        Xc, Yc, Zc = 0.0, 0.0, 1.0
                else:
                    # Default Z-axis direction if not provided
                    Xc, Yc, Zc = 0.0, 0.0, 1.0

            if not transform_id == 0:
                # Generate the Radioss format output
                transform_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                transform_lines.append(f"/TRANSFORM/POSITION/{transform_id}")
                transform_lines.append(f"System {transform_id}")
                transform_lines.append(f"{'':>90}{transform_id:>10}")
                transform_lines.append(f"          {0.0:>20.8f}{0.0:>20.8f}{0.0:>20.8f}")
                transform_lines.append(f"          {1.0:>20.8f}{0.0:>20.8f}{0.0:>20.8f}")
                transform_lines.append(f"          {0.0:>20.8f}{1.0:>20.8f}{0.0:>20.8f}")
                transform_lines.append(f"          {Xa:>20.8f}{Ya:>20.8f}{Za:>20.8f}")
                transform_lines.append(f"          {Xb:>20.8f}{Yb:>20.8f}{Zb:>20.8f}")
                transform_lines.append(f"          {Xc:>20.8f}{Yc:>20.8f}{Zc:>20.8f}")

                transform_data.append(transform_id)

        i += 1

    return transform_lines, transform_data


####################################################################################################
# Function to read nodes sped up by filtering                                                      #
####################################################################################################
def read_nodes(input_lines):
    node_data = {}
    inside_node_section = False
    transform_id = 0
    remaining_lines = []

    for line in input_lines:
        if line.lower().startswith('*system id='):
            parts = line.split('=', 1)
            if len(parts) > 1:
                transform_id = parts[1].strip()
            inside_node_section = False

        if (
            line.lower().startswith('*node')
            and 'print' not in line.lower()
            and 'output' not in line.lower()
            and 'file' not in line.lower()
            ):
            inside_node_section = True

        elif inside_node_section and line.startswith('*'):
            inside_node_section = False

        if inside_node_section and not line.startswith('*'):
            if transform_id not in node_data:
                node_data[transform_id] = []
            node_data[transform_id].append(line)

        else:
            remaining_lines.append(line)  # Collect the remaining lines

    if not debug_mode:
        return node_data, remaining_lines

####################################################################################################
#debug to check the filtered input                                                                 #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_filter_postnodes.inp"  # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)   # FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in remaining_lines:  # for debug
            test_output_file.write(filtered_line) # Write the filtered deck # for debug

    print("postnodes written")
    return node_data, remaining_lines


####################################################################################################
# Function to convert nodes                                                                        #
####################################################################################################
def convert_nodes(node_data):
    node_lines = {}
    for transform_id, nodes in node_data.items():
        node_lines[transform_id] = []
        for line in nodes:
            # Process the node data
            nodes = line.strip().split(',')
            node_id = nodes[0].strip()
            coords = [float(coord.strip()) for coord in nodes[1:]]
            radioss_coords = ''.join(f"{coord:>20.15g}" for coord in coords)
            node_lines[transform_id].append(f"{node_id:>10}{radioss_coords}")

    return node_lines


####################################################################################################
# Function to preprocess ELEMENT D3COUP and COUPLNG DISTRIBUTION lines for easier handling         #
####################################################################################################
def convert_distcoup(input_lines):
    elset_pattern = re.compile(r'\bELSET\s*=\s*("([\w\-+/ ]+)"|[\w\-+/ ]+)', re.IGNORECASE)
    refnode_pattern = re.compile(r'REF NODE\s*=\s*(\d+)', re.IGNORECASE)
    surface_pattern = re.compile(r'SURFACE\s*=\s*("([\w\-+/ ]+)"|[\w\-+/ ]+)', re.IGNORECASE)

    output_lines = []
    remaining_lines = []
    element_data = {}
    coupling_data = {}
    current_elset = None
    current_refnode = None
    current_surface = None
    refnode = None

    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        if re.search(r'^\s*\*ELEMENT\s*,\s*TYPE\s*=\s*DCOUP3D\b', line, re.IGNORECASE):
            elset_match = elset_pattern.search(line)
            if elset_match:
                current_elset = elset_match.group(1)
            i += 1
            element_line = input_lines[i].strip()
            element_id, refnode = element_line.split(',')
            element_data[current_elset] = {
                'element_id': element_id, 'refnode': refnode, 'nodes': [], 'count': 0
                }

        elif line.lower().startswith('*distributing coupling'):
            elset_match = elset_pattern.search(line)
            if elset_match:
                current_elset = elset_match.group(1)
            i += 1
            j = 1
            while i < len(input_lines) and not input_lines[i].startswith('*'):
                node, weight = input_lines[i].strip().split(',')
                element_data[current_elset]['nodes'].append((node, weight))
                element_data[current_elset]['count'] = str(j)
                j += 1
                i += 1
            i -= 1

        elif line.lower().startswith('*coupling'):
            if debug_mode:
                print(f"found a coupling on line {line}")
            refnode_match = refnode_pattern.search(line)
            surface_match = surface_pattern.search(line)
            if refnode_match and surface_match:
                current_refnode = refnode_match.group(1)
                current_surface = surface_match.group(1)
                if debug_mode:
                    print(f"refnode {current_refnode}, surface {current_surface}")
                if i + 1 < len(input_lines) and input_lines[i + 1].strip().lower().startswith('*distributing'):
                    coupling_data[current_surface] = {'refnode': current_refnode, 'nodes': []}
                    coupling_data[current_surface]['count'] = str(j)

                else:
                    if debug_mode:
                        print (f"appending {line}")
                    remaining_lines.append(line)
                    
            else:
                if debug_mode:
                    print (f"ref and surf no match: appending {line}")
                remaining_lines.append(line)
        

        elif re.search(r'^\s*\*SURFACE\s*,\s*(?=.*\bTYPE\s*=\s*NODE\b)(?!.*\bINTERACTION\b)', line, re.IGNORECASE):
            surface_match = re.search(r'NAME\s*=\s*("([^"]+)"|([^,]+))', line, re.IGNORECASE)
            if surface_match:
                current_surface = surface_match.group(1)
            if current_surface not in coupling_data:
                remaining_lines.append(input_lines[i])
                i += 1
                while i < len(input_lines) and not input_lines[i].startswith('*'):
                    remaining_lines.append(input_lines[i])
                    i += 1
                i -= 1

            else:
                i += 1
                j = 1
                while i < len(input_lines) and not input_lines[i].startswith('*'):
                    node, weight = input_lines[i].strip().split(',')
                    coupling_data[current_surface]['nodes'].append((node, weight))
                    coupling_data[current_surface]['count'] = str(j)
                    j += 1
                    i += 1
                i -= 1

        else:
            remaining_lines.append(line)

        i += 1

    output_lines.extend(remaining_lines)

    for elset, data in element_data.items():
        if 'element_id' not in data:
            print(f"Error: Missing element_id for elset={elset}")
            continue
        output_lines.append(f"*DISCOUP, ID={data['element_id']}")
        output_lines.append(elset)
        output_lines.append(data['count'])
        output_lines.append(data['refnode'])
        for node, weight in data.get('nodes', []):
            nset_name = f"nodeset_for_{node}"
            output_lines.append(f"{nset_name}, {weight}")
        for node, weight in data.get('nodes', []):
            nset_name = f"nodeset_for_{node}"
            output_lines.append(f"*NSET, NSET={nset_name}")
            output_lines.append(node)

    for surface, data in coupling_data.items():
        if refnode:
            output_lines.append("*DISCOUP, ID=placeholder")
            output_lines.append(surface)
            output_lines.append(data['count'])
            output_lines.append(data['refnode'])
            for node, weight in data.get('nodes', []):
                nset_name = f"nodeset_for_{node}"
                output_lines.append(f"{nset_name}, {weight}")
            for node, weight in data.get('nodes', []):
                nset_name = f"nodeset_for_{node}"
                output_lines.append(f"*NSET, NSET={nset_name}")
                output_lines.append(node)

    return output_lines


####################################################################################################
# Function to convert nsets                                                                        #
####################################################################################################
def convert_nsets(input_lines, nset_references):
    nsets = {}  # Dictionary to store NSET information by name
    nset_counter = 0  # Counter to assign unique IDs to NSETs
    output_lines = []  # Store all lines to write back (debug feature)
    nested_nset = False

    i = 0  # Line index for iteration
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Regular expression to find '*SURFACE' of type 'Node'
        ntype_pattern = r'^\s*\*SURFACE\s*,\s*(?=.*\bTYPE\s*=\s*NODE\b)(?=.*\bNAME\s*=\s*[\w\-]+)?.*'
        matchnode = re.search(ntype_pattern, line, re.IGNORECASE)

        # Regular expression to find '*KINEMATIC COUPLING' implied NSET
        kcoup_pattern = r'^\s*\*KINEMATIC\s+COUPLING\s*,\s*REF\s*NODE\s*=\s*[^,]+'
        matchkc = re.search(kcoup_pattern, line, re.IGNORECASE)


        # Check if the line is an NSET definition with 'generate'
        if line.lower().startswith('*nset') and 'generate' in line.lower():
            # Extract the NSET name
            nset_name = re.search(r'nset\s*=\s*([^,]+)', line, re.IGNORECASE).group(1).strip()
            # Initialize NSET entry
            nsets[nset_name] = {'id': None, 'values': [], 'is_referenced': False}

            # Get the next line with start, end, and (optional) step values for the range
            next_line = input_lines[i + 1].strip()
            if next_line.endswith(','):
            # Remove trailing comma
                next_line = next_line.rstrip(',')
            else:
                next_line = next_line

            parts = list(map(int, next_line.split(',')))  # Convert to integers
            
            # Ensure there are at least two values (start, end), and set step = 1 if missing
            if len(parts) == 2:
                start, end = parts
                step = 1  # Default step
            elif len(parts) == 3:
                start, end, step = parts
            else:
                raise ValueError(f"Invalid range format in NSET definition: {next_line}")

            # Generate the range of numbers
            values = list(range(start, end + 1, step))

            # Break up values into groups of 8 per line and format them
            formatted_lines = []
            for j in range(0, len(values), 8):
                formatted_lines.append(', '.join(map(str, values[j:j + 8])) + '\n')

            # Replace the next line with the generated values
            output_lines.append(line + '\n')  # Append the current NSET line
            output_lines.extend(formatted_lines)  # Append the generated lines

            # Store the values in the nsets dictionary
            nsets[nset_name]['values'].extend(values)

            # Skip the next line since it's replaced with the generated values
            i += 2

        # Check if it's a normal NSET definition (no 'generate')
        elif line.lower().startswith('*nset') and 'generate' not in line.lower():
            # Extract the NSET name
            nset_name = re.search(r'nset\s*=\s*([^,]+)', line, re.IGNORECASE).group(1).strip()
            nsets[nset_name] = {'id': None, 'values': [], 'is_referenced': False}

            for parents in nset_references.items():
                if nset_name in parents:
                    nested_nset = True

            # Move to the next line(s) to gather the NSET values
            i += 1
            nset_values = []

            if nested_nset is False:
                while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                    value_line = input_lines[i].strip()
                    if value_line:  # Make sure it's not an empty line
                        nset_values.extend(value_line.split(','))  # Split values by comma
                    i += 1

                # Store the collected values in the nsets dictionary
                nsets[nset_name]['values'].extend(
                    [
                        value.strip()
                        for value in nset_values
                        if value.strip()
                    ]
                )

                # Add the collected NSET values to the output
                output_lines.append(line + '\n')
                for j in range(0, len(nset_values), 8):
                    output_lines.append(', '.join(map(str, nset_values[j:j + 8])) + '\n')

            elif nested_nset is True:

                for referenced_nset in nset_references.get(nset_name, []):

                    # Retrieve values from `nsets` for each referenced NSET, if it exists
                    contained_values = []

                    if referenced_nset in nsets:
                        contained_values.extend(nsets[referenced_nset].get('values', []))

                    # Extend the main nset_values list with the contained values
                    nset_values.extend(contained_values)
                    #print(f"The new set content is: {nset_values}") #for debug

                # Store the collected values in the `nsets` dictionary
                nsets[nset_name]['values'].extend(
                    [
                        value.strip() if isinstance(value, str) else value
                        for value in nset_values
                        if str(value).strip()
                    ]
                )

                # Add the collected NSET values to the output
                output_lines.append(line + '\n')
                for j in range(0, len(nset_values), 8):
                    output_lines.append(', '.join(map(str, nset_values[j:j + 8])) + '\n')

                # Reset `nested_nset` after processing
                nested_nset = False

        # Check for SURFACE type NODE NSET definition
        elif matchnode:
            # Extract the NSET name
            nset_name_match = re.search(r'\bNAME\s*=\s*([^,]+)', line, re.IGNORECASE)
            nset_name = nset_name_match.group(1).strip()
            nsets[nset_name] = {'id': None, 'values': [], 'is_referenced': False}

            # Move to the next line(s) to gather the NSET values
            i += 1
            nset_values = []
            hold_incase = []

            while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                value_line = input_lines[i].strip()
                if value_line:  # Make sure it's not an empty line
                    # Extract only the first value before the first comma
                    node_value = value_line.split(',')[0].strip()
                    hold_incase.append(node_value)
                    if node_value.isdigit():
                        nset_values.append(node_value)
                i += 1

            # Store the collected values in the nsets dictionary
            if nset_values:
                nsets[nset_name]['values'].extend(
                    [
                        value
                        for value in nset_values
                        if value  # Ensure no empty values are added
                    ]
                )

            else:
                del nsets[nset_name]
                # If no nset numeric values, Add the original name back to the output
                output_lines.append(line + '\n')
                for j in range(0, len(hold_incase), 8):
                    output_lines.append(', '.join(map(str, hold_incase[j:j + 8])) + '\n')

            # Add the collected NSET values to the output
            for j in range(0, len(nset_values), 8):
                output_lines.append(', '.join(map(str, nset_values[j:j + 8])) + '\n')

            matchnode = False

        # Check for KINEMATIC COUPLING type NODE NSET definition
        elif matchkc:
            # Extract the NSET name
            refnode_match = re.search(r'\bREF NODE\s*=\s*([^,]+)', line, re.IGNORECASE)
            refnode = refnode_match.group(1).strip()
            nset_name = f"NODES_FOR_KC_WITH_REF_NODE_{refnode}"
            nsets[nset_name] = {'id': None, 'values': [], 'is_referenced': False}

            # Move to the next line(s) to gather the NSET values
            i += 1
            nset_values = []
            hold_incase = []

            while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                value_line = input_lines[i].strip()
                if value_line:  # Make sure it's not an empty line
                    # Extract only the first value before the first comma
                    node_value = value_line.split(',')[0].strip()
                    hold_incase.append(node_value)
                    if node_value.isdigit():
                        nset_values.append(node_value)
                    else:
                        nset_values = []

                i += 1

            # Store the collected values in the nsets dictionary
            if nset_values:
                nsets[nset_name]['values'].extend(
                    [
                        value
                        for value in nset_values
                        if value  # Ensure no empty values are added
                    ]
                )

                # Add the collected NSET values to the output
                output_lines.append(line + '\n')
                output_lines.append(f"{nset_name}\n")

            else:
                del nsets[nset_name]
                # If no nset numeric values, Add the original name back to the output
                output_lines.append(line + '\n')
                for j in range(0, len(hold_incase), 8):
                    output_lines.append(', '.join(map(str, hold_incase[j:j + 8])) + '\n')


            matchkc = False

        elif line.lower().startswith('*node output') and 'nset' in line.lower():
            noutmatch = re.search(r'nset\s*=\s*([^,]+)', line, re.IGNORECASE)
            if noutmatch:
                referenced_noutput_name = noutmatch.group(1).strip()
                if referenced_noutput_name in nsets:
                    nsets[referenced_noutput_name]['is_referenced'] = True
            output_lines.append(line + '\n')
            i += 1

        elif line.lower().startswith('*node print') and 'nset' in line.lower():
            noutmatch = re.search(r'nset\s*=\s*([^,]+)', line, re.IGNORECASE)
            if noutmatch:
                referenced_noutput_name = noutmatch.group(1).strip()
                if referenced_noutput_name in nsets:
                    nsets[referenced_noutput_name]['is_referenced'] = True
            output_lines.append(line + '\n')
            i += 1

        else:
            # Handle lines that are not part of NSET blocks
            output_lines.append(line + '\n')
            i += 1

    # Assign unique IDs to each NSET
    for nset_name in nsets:
        nset_counter += 1
        nsets[nset_name]['id'] = nset_counter

    if not debug_mode:
        return nsets, nset_counter, output_lines  #debug, remove comment to skip filtered output

####################################################################################################
#debug to check the filtered input                                                                 #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_filter_postnsets.inp"  # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)  # FOR DEBUG
    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in output_lines: # For debug
            test_output_file.write(filtered_line)  # Write the filtered deck # for debug

    print("postnsets written") 
    return nsets, nset_counter, output_lines

####################################################################################################
# Function create /GRNOD/NODE and /TH/NODE from nset data                                          #
####################################################################################################
def create_nblocks(nsets):
    nset_blocks = []
    for nset_name, nset_data in nsets.items():
        nset_counter = nset_data['id']
        nset_values = nset_data['values']

        grnod_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
        grnod_block += f"/GRNOD/NODE/{nset_counter}\n"
        grnod_block += f"{nset_name}\n"
        for i in range(0, len(nset_values), 10):
            row_values = nset_values[i:i+10]
            # Right-justified columns
            formatted_row = ''.join(f"{value:>10}" for value in row_values)
            grnod_block += formatted_row + '\n'

        thnod_block = ""
        if nset_data['is_referenced']:
            thnod_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            thnod_block += f"/TH/NODE/{nset_counter}\n"
            thnod_block += f"{nset_name}\n"
            thnod_block += "#     var1      var2      var3      var4      var5      var6      var7      var8      var9     var10\n"
            thnod_block += "DEF       REACX     REACY     REACZ\n"
            thnod_block += "#    NODid     Iskew                                           NODname\n"
            formatted_values = '\n'.join(f"{value:>10}" for value in nset_values)
            thnod_block += formatted_values + '\n'

        nset_blocks.append((grnod_block, thnod_block))

    return nset_blocks

####################################################################################################
# Function to convert material data                                                                #
####################################################################################################
def convert_materials(input_lines):
    fct_id = 0  # Initialize the function ID
    global e_magnitude
    global rho_magnitude
    material_names = {}  # initializes a dictionary of Material name relationships
    current_material_name = None
    material_id = 1  # Initialize the material ID

    other_rigid_mats_processed_list = []
    i = 0  # Initialize an index for iterating through input_lines

    #this section checks for material attributes and stores them
    #against the dictionary of material names
    while i < len(input_lines):
        line = input_lines[i].strip()

        material_line_pattern = r'^\s*\*MATERIAL\s*,?\s*NAME\s*=\s*[^,]+(?:\s*,\s*.+)?$'
        material_line_match = re.search(material_line_pattern, line, re.IGNORECASE)

        rigid_line_pattern = r'^\s*\*ELEMENT\s*,?\s*TYPE\s*=\s*R3D[34]\b.*$'
        rigid_line_match = re.search(rigid_line_pattern, line, re.IGNORECASE)

        superelastic_pattern = r'^\*\s*superelastic\b'
        superelastic_line_match = re.search(superelastic_pattern, line, re.IGNORECASE)

        neohooke_pattern = r'^\*\s*hyperelastic\b.*,\s*neo hooke'
        neohooke_line_match = re.search(neohooke_pattern, line, re.IGNORECASE)

        ogden_pattern = r'^\*\s*hyperelastic\b.*,\s*ogden'
        ogden_line_match = re.search(ogden_pattern, line, re.IGNORECASE)

        mooney_rivlin_pattern = r'^\*\s*hyperelastic\b.*,\s*mooney-rivlin'
        mooney_rivlin_line_match = re.search(mooney_rivlin_pattern, line, re.IGNORECASE)

        mass_line_pattern = r'^\s*\*mass\s*,?\s*elset\s*=\s*[^,]+(?:\s*,\s*.+)?$'
        mass_line_match = re.search(mass_line_pattern, line, re.IGNORECASE)

        if material_line_match:
            material_name = line.split('=')[1].strip()#.lower()

            # Assign a material ID to the material
            material_names[material_name] = {'material_id': material_id}
            current_material_name = material_name  # Set the current material name

            material_id += 1  # Increment the material ID

            i += 1
            continue

        #special treatment for rigid entities, we create a mat void,
        #since in .inp, there is no material
        if rigid_line_match:
            # regular expression to find 'elset =' or 'elset='
            elset_pattern = r'\bELSET\s*=\s*("([\w\-+/ ]+)"|[\w\-+/ ]+)'
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            #this_check_added since rigid elements don't need to be in an elset
            #but should have been assigned one by now!
            if elset_match is None:
                print("Something went wrong")
            else:
                material_name = elset_match.group(1).strip()
                if material_name not in other_rigid_mats_processed_list:
                    # Assign a material ID to the material
                    material_names[material_name] = {'material_id': material_id}
                    current_material_name = material_name  # Set the current material name
                    material_names[current_material_name]['rigid'] = "yes"

                    material_id += 1  # Increment the material ID
                    other_rigid_mats_processed_list.append(material_name)
            i += 1
            continue

        # mass
        elif mass_line_match:
            # regular expression to find 'elset =' or 'elset='
            elset_pattern = r'\bELSET\s*=\s*("([\w\-+/ ]+)"|[\w\-+/ ]+)'
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            material_name = elset_match.group(1).strip()
            if material_name:
                material_id += 1  # Increment the material ID
                material_names[material_name] = {'material_id': material_id}
                material_names[material_name]['masselement'] = "yes"
            i += 1

            massdata_line = input_lines[i].strip()
            massdata_value = massdata_line.split(',')[0]

            massdata_value = float(massdata_value)
            material_names[material_name]['mass'] = massdata_value

            continue

        # density
        elif current_material_name and line.lower().startswith('*density'):
            i += 1
            density_line = input_lines[i].strip()
            density_value = float(density_line.split(',')[0])
            material_names[current_material_name]['rho'] = density_value
            rho_magnitude = max(rho_magnitude, density_value)

        # elastic
        elif (
                current_material_name
                and line.strip().lower().startswith('*elastic')
                and not 'traction' in line.strip().lower()
            ):
            i += 1
            elastic_line = input_lines[i].strip()
            elastic_values = elastic_line.split(',')[0:2]
            emodulus, poissrat = map(float, elastic_values)
            material_names[current_material_name]['emodulus'] = emodulus
            e_magnitude = max(e_magnitude, emodulus)
            material_names[current_material_name]['poissrat'] = poissrat

        # connect/cohesive
        elif (
                current_material_name
                and line.strip().lower().startswith('*elastic')
                and 'traction' in line.strip().lower()
             ):
            i += 1
            cohesive_line = input_lines[i].strip()
            cohesive_values = cohesive_line.split(',')[0:4]
            emodulus, gmodulus1, gmodulus2, temperature = map(float, cohesive_values)
            material_names[current_material_name]['emodulus'] = emodulus
            e_magnitude = max(e_magnitude, emodulus)

            if gmodulus1 != gmodulus2:
                print("**************************************************************************")
                print("WARNING: Cohesive Material With Different G1, G2 Values In Material:")
                print(f"         {current_material_name}")
                print("         Only The First G Value  Is Used")
                print("**************************************************************************")

            material_names[current_material_name]['gmodulus'] = gmodulus1
            if temperature:
                print("*****************************************************************")
                print("WARNING: Cohesive Temperature Dependent Data Present In Material:")
                print(f"         {current_material_name}")
                print("         Temperature Dependent Data Will Not Be Translated")
                print("         Only The First Temperature Data Set Is Used")
                print("*****************************************************************")

        # hyperfoam
        elif current_material_name and line.lower().startswith('*hyperfoam'):
            hyperfoam_line = input_lines[i].strip()

            #default value for poissons ratio in case one is not defined in data
            poissrat = 0.1

            # Use regular expressions to extract relevant information
            match = re.search(
                r'POISSON=([-+]?\d*\.\d+|\d+(?:[eE][-+]?\d+)?)', hyperfoam_line, re.IGNORECASE
                )

            if match:
                poissrat = float(match.group(1))

            material_names[current_material_name]['poissrat'] = poissrat

        # uniaxial test
        elif current_material_name and line.lower().startswith('*uniaxial test data'):
            i += 1
            uniaxial_data = []  # Initialize uniaxial_data for the current material
            while i < len(input_lines) and not input_lines[i].startswith('*'):
                # Read and convert the hyperfoam uniaxial test data (changing to positive data)
                data_line = input_lines[i].strip()
                # Extract the first two fields
                data_values = [float(val) for val in data_line.split(',')[:2]]
                # Swap x and y values
                uniaxial_data.append((abs(data_values[1]), abs(data_values[0])))
                i += 1
 # Check if the first uniaxial data pair starts with a non-zero value, and if so, insert 0,0 pair
                uniaxial_data.sort(key=lambda pair: abs(pair[0]))
            if uniaxial_data and uniaxial_data[0][0] != 0.0:
                uniaxial_data.insert(0, (0.0, 0.0))
            fct_id += 1  # Increment the fct_id
            material_names[current_material_name]['uniaxial_data'] = {
                 'fct_id': fct_id,
                 'xy_data': uniaxial_data
            } # assign each uniaxial data set a function id
            i -= 1

        # plastic
        elif current_material_name and line.strip().lower().startswith('*plastic'):
            # Check if there's rate data and extract the rate value if it exists
            rate_data = 'rate=' in line.lower()
            rate_value = 1.0  # Default rate value

            if rate_data:
                # Extract the rate value after 'rate='
                rate_value_str = line.lower().split('rate=')[1].split()[0]
                rate_value = float(rate_value_str)

            i += 1
            plastic_data = []  # Initialize plastic_data for the current material

            # Extract data while the line does not start with '*'
            while i < len(input_lines) and not input_lines[i].startswith('*'):
                # Read and convert the plastic data (changing to positive data)
                data_line = input_lines[i].strip()
                x, y = map(float, data_line.split(',')[0:2])
                plastic_data.append((abs(y), abs(x)))
                i += 1

            fct_id += 1  # Increment the function ID

            # Initialize the material entry for plastic data if it does not exist
            if 'plastic_data' not in material_names[current_material_name]:
                material_names[current_material_name]['plastic_data'] = {'rate_sets': []}

            # Store plastic data in a rate set, whether rate-dependent or independent
            material_names[current_material_name]['plastic_data']['rate_sets'].append({
                'fct_id': fct_id,
                'rate': rate_value,
                'xy_data': plastic_data
            })
            i -= 1  # Adjust index to account for the last increment

        # ogden params
        elif current_material_name and ogden_line_match and not 'test data input' in line.lower():
            i += 1
            ogden_line = input_lines[i].strip()
            ogden_values = ogden_line.split(',')[0:3]
            ogden_mu, ogden_alpha, ogden_D = map(float, ogden_values)
            material_names[current_material_name]['ogden_mu'] = ogden_mu
            material_names[current_material_name]['ogden_alpha'] = ogden_alpha
            material_names[current_material_name]['ogden_D'] = ogden_D

        # neo-hooke params
        elif current_material_name and neohooke_line_match:
            i += 1
            neohooke_line = input_lines[i].strip()
            neohooke_mu = float(neohooke_line.split(',')[0])
            #neohooke_mu = map(float, neohooke_values)
            material_names[current_material_name]['neohooke_mu'] = neohooke_mu

        # ogden test_data
        elif current_material_name and ogden_line_match and 'test data input' in line.lower():
            # Set default values
            ogden_n = 1
            poissrat = 0.45

            # Search for N= and POISSON= in the line, ignoring spaces around the equals sign
            n_match = re.search(r'\bN\s*=\s*([\d.]+)', line, re.IGNORECASE)
            poisson_match = re.search(r'\bPOISSON\s*=\s*([\d.]+)', line, re.IGNORECASE)

            # If matches found, convert to float and update the values
            if n_match:
                ogden_n = int(n_match.group(1))
            if poisson_match:
                poissrat = float(poisson_match.group(1))

            # Assign to the material properties dictionary
            material_names[current_material_name]['ogden_n'] = ogden_n
            material_names[current_material_name]['poissrat'] = poissrat

        # mooney-rivlin
        elif current_material_name and mooney_rivlin_line_match:
            i += 1
            mr_line = input_lines[i].strip()
            mr_values = mr_line.split(',')[0:2]

            mr_mu1, mr_mu2 = map(float, mr_values)
            material_names[current_material_name]['mr_mu1'] = mr_mu1
            material_names[current_material_name]['mr_mu2'] = mr_mu2

        # superelastic
        elif current_material_name and superelastic_line_match:
            i += 1
            se_line = input_lines[i].strip()
            se_values = [value.strip() for value in se_line.split(',')]

            if len(se_values) != 8:
                raise ValueError(f"Expected 8 values but got {len(se_values)} in line: {se_line}")

            se_mm, se_mpr, se_uts, se_tbt, se_tet, se_trbt, se_tret, se_tbc = map(float, se_values)
            material_names[current_material_name]['se_mm'] = se_mm
            material_names[current_material_name]['se_mpr'] = se_mpr
            material_names[current_material_name]['se_uts'] = se_uts
            material_names[current_material_name]['se_tbt'] = se_tbt
            material_names[current_material_name]['se_tet'] = se_tet
            material_names[current_material_name]['se_trbt'] = se_trbt
            material_names[current_material_name]['se_tret'] = se_tret
            material_names[current_material_name]['se_tbc'] = se_tbc

            i += 1
            se_line = input_lines[i].strip()
            se_values = [value.strip() for value in se_line.split(',')]

            if len(se_values) != 3:
                raise ValueError(f"Expected 3 values but got {len(se_values)} in line: {se_line}")

            se_reftemp, se_slope_load, se_slope_unload = map(float, se_values)
            material_names[current_material_name]['se_reftemp'] = se_reftemp + 273
            material_names[current_material_name]['se_slope_load'] = se_slope_load
            material_names[current_material_name]['se_slope_unload'] = se_slope_unload


        i += 1  # Move to the next line

    return material_names, fct_id # return material names to main convert def


###############################################################################################
# Functions to check what type of materials to write based on stored dictionary data:         #
#  called by file write section and used to call relevant material write def (next section)   #
###############################################################################################
# checks for variables for elastic material and returns them to the material write section
def check_if_mass(properties):
    desired_mps = ['material_id', 'masselement', 'mass']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )

def check_if_elast(properties):
    desired_mps = ['material_id', 'rho', 'emodulus', 'poissrat']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for cohesive material and returns them to the material write section
def check_if_cohesive(properties):
    desired_mps = ['material_id', 'rho', 'emodulus', 'gmodulus']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for plastic material and returns them to the material write section
def check_if_plast(properties):
    desired_mps = ['material_id', 'rho', 'emodulus', 'poissrat', 'plastic_data']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for neo-hooke material and returns them to the material write section
def check_if_neohooke(properties):
    desired_mps = ['material_id', 'rho', 'neohooke_mu']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for ogden material and returns them to the material write section
def check_if_ogden(properties):
    desired_mps = ['material_id', 'rho', 'ogden_mu', 'ogden_alpha', 'ogden_D']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for ogden material and returns them to the material write section
def check_if_ogden_c(properties):
    desired_mps = ['material_id', 'rho', 'ogden_n', 'poissrat', 'uniaxial_data']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for mooney-rivlin material and returns them to the material write section
def check_if_mr(properties):
    desired_mps = ['material_id', 'rho', 'mr_mu1', 'mr_mu2']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for superealstic material and returns them to the material write section
def check_if_se(properties):
    desired_mps = ['material_id', 'rho', 'emodulus', 'poissrat', 'se_mm', 'se_mpr', 'se_uts',
        'se_tbt', 'se_tet', 'se_trbt', 'se_tret', 'se_tbc', 'se_reftemp', 'se_slope_load',
        'se_slope_unload'
        ]
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for hyperfoam material and returns them to the material write section
def check_if_hypf(properties):
    desired_mps = ['material_id', 'rho', 'poissrat', 'uniaxial_data']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )
# checks variables for rigid material and returns them to the material write section
def check_if_rigid(properties):
    desired_mps = ['material_id', 'rigid']
    return all(
        prop in properties for prop in desired_mps) and len(properties) == len(desired_mps
        )


###############################################################################################
# Functions to write new materials,  called in write section                                  #
###############################################################################################
# MAT LAW1
# writes elastic material
def write_elastic_material(
    material_id, material_name, rho, emodulus, poissrat, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/ELAST/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}                   0\n")
    output_file.write("#                  E                  nu\n")
    output_file.write(f"{emodulus:>20.15g}{poissrat:>20.15g}\n")

# MAT LAW36
# writes plastic material
def write_plastic_material(
    material_id, material_name, rho, emodulus, poissrat, plastic_data, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/PLAS_TAB/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}                   0\n")
    output_file.write("#                  E                  nu           Eps_p_max               Eps_t               Eps_m\n")
    output_file.write(f"{emodulus:>20.15g}{poissrat:>20.15g}                   0                   0                   0\n")

    # Determine the number of functions
    numbfunct = len(plastic_data['rate_sets']) if 'rate_sets' in plastic_data else 1
    output_file.write("#  N_funct  F_smooth              C_hard               F_cut               Eps_f                  VP\n")
    output_file.write(f"{numbfunct:>10}         0                   0                   0                   0                   0\n")
    output_file.write("#  fct_IDp              Fscale   Fct_IDE                EInf                  CE\n")
    output_file.write("         0                   0         0                   0                   0\n")

    # Write function IDs for rate-dependent sets or main data
    function_ids = [rate_set.get('fct_id') for rate_set in plastic_data.get('rate_sets')]
    for i in range(0, len(function_ids), 5):
        output_file.write("# func_ID1  func_ID2  func_ID3  func_ID4  func_ID5\n")
        output_file.write("".join(f"{fid:>10}" for fid in function_ids[i:i+5]).ljust(50) + "\n")

    # Write scales for rate-dependent sets
    rates = [rate_set['rate'] for rate_set in plastic_data.get('rate_sets', [{'rate': 1.0}])]
    for i in range(0, len(rates), 5):
        output_file.write("#           Fscale_1            Fscale_2            Fscale_3            Fscale_4            Fscale_5\n")
        output_file.write("                   0                   0                   0                   0                   0\n")

    # Write rate values for rate-dependent sets
    rates = [rate_set['rate'] for rate_set in plastic_data.get('rate_sets', [{'rate': 1.0}])]
    for i in range(0, len(rates), 5):
        output_file.write("#          Eps_dot_1           Eps_dot_2           Eps_dot_3           Eps_dot_4           Eps_dot_5\n")
        output_file.write("".join(f"{rate:>20.8e}" for rate in rates[i:i+5]).ljust(100) + "\n")

    # Write each set of XY data as functions
    for rate_set in plastic_data.get('rate_sets'):
        fct_id = rate_set['fct_id']
        xy_data = rate_set['xy_data']
        rate = rate_set['rate']
        output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
        output_file.write(f"/FUNCT/{fct_id}\n")
        output_file.write(f"{material_name} rate: {rate} \n")
        output_file.write("#                  X                   Y\n")
        for x, y in xy_data:
            output_file.write(f"{x:>20.15g}{y:>20.15g}\n")

# MAT LAW42
# writes law42 neo-hooke material
def write_neohooke_material(
    material_id, material_name, rho, neohooke_mu, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW42/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}                   0\n")
    output_file.write("#                 Nu           sigma_cut           funIDbulk         Fscale_bulk         M    I_form\n")
    output_file.write("               0.495                                                                                \n")
    output_file.write("#               Mu_1                Mu_2                Mu_3                Mu_4                Mu_5\n")
    neohooke_mu = neohooke_mu * 2
    output_file.write(f"{neohooke_mu:>20.15g}                 0.0\n")
    output_file.write("# blank card\n")
    output_file.write("\n")
    output_file.write("#            alpha_1             alpha_2             alpha_3             alpha_4             alpha_5\n")
    output_file.write("                 2.0                 0.0\n")
    output_file.write("# blank card\n")
    output_file.write("\n")

# MAT LAW42
# writes law42 mooney-rivlin material
def write_mr_material(
    material_id, material_name, rho, mr_mu1, mr_mu2, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW42/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}                   0\n")
    output_file.write("#                 Nu           sigma_cut           funIDbulk         Fscale_bulk         M    I_form\n")
    output_file.write("               0.495                                                                                \n")
    output_file.write("#               Mu_1                Mu_2                Mu_3                Mu_4                Mu_5\n")
    mr_mu1 = mr_mu1 * 2
    mr_mu2 = mr_mu2 * -2
    output_file.write(f"{mr_mu1:>20.15g}{mr_mu2:>20.15g}\n")
    output_file.write("# blank card\n")
    output_file.write("\n")
    output_file.write("#            alpha_1             alpha_2             alpha_3             alpha_4             alpha_5\n")
    output_file.write("                 2.0                -2.0\n")
    output_file.write("# blank card\n")
    output_file.write("\n")

# MAT LAW59
# writes law59 connect material
def write_coh_material(
    material_id, material_name, rho, emodulus, gmodulus, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write("#WARNING: This law has no temperature dependency in Radioss, only 'coldest' props taken from inp\n")
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW59/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}\n")
    output_file.write("#                  E                   G     Imass     Icomp               Ecomp\n")
    output_file.write(f"{emodulus:>20.15g}{gmodulus:>20.15g}                                                                                \n")
    output_file.write("#   Nb_fct   Fsmooth                Fcut\n")
    output_file.write("         0         0                   0\n")

# MAT LAW69
# writes law69 ogden material
def write_ogden_c_material(
    material_id, material_name, rho, ogden_n, poissrat, uniaxial_data, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW69/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}                   0\n")
    output_file.write("#   Law_ID fct_IDblk                  nu           Fscaleblk    N_pair    Icheck\n")
    output_file.write(f"         1         0{poissrat:>20.15g}                   0{ogden_n:>10}         0\n")
    output_file.write("#  FCT_ID1\n")
    function_id = uniaxial_data['fct_id']  # Extract the function_id from the uniaxial_data dictionary
    output_file.write(f"{function_id:>10}\n")
    #extract the function data pairs from the uniaxial_data dictionary
    xy_data = uniaxial_data['xy_data']
    #write the asssociated material function
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/FUNCT/{function_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#                  X                   Y\n")
    #write the function x y pairs
    for item in xy_data:
        x, y = item
        output_file.write(f"{x:>20.15g}{y:>20.15g}\n")

# MAT LAW70
# writes law70 foam material
def write_hypf_material(
    material_id, material_name, rho, poissrat, uniaxial_data, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW70/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}\n")
    output_file.write("#                 EO                  NU               E_max             EPS_max     Itens\n")
    #extract the function data pairs from the uniaxial_data dictionary
    xy_data = uniaxial_data['xy_data']
    #calculate EO from xy data
    x2, y2 = xy_data[1]  # Take Second data point in uniaxial data to calculate EO
    hypf_EO = 10 * y2 / x2
    #calculate E_Max from xy data
    x_penultimate, y_penultimate = xy_data[-2]  # Penultimate data point in uniaxial data
    x_final, y_final = xy_data[-1]  # Final data point in uniaxial data
    hypf_emax = (y_final - y_penultimate) / (x_final - x_penultimate)
    #continue_writing
    output_file.write(f"{hypf_EO:>20.15g}{poissrat:>20.15g}{hypf_emax:>20.15g}                   0                   0\n")
    output_file.write("#              F_cut   Ismooth     Nload   Nunload     Iflag               Shape                 Hys\n")
    output_file.write("                   0         0         1         0         4                   0                   0\n")
    output_file.write("#  fct_IDL          Eps_._load          Fscaleload\n")
    function_id = uniaxial_data['fct_id']  # Extract the function_id from the uniaxial_data dictionary
    # Write the extracted function_id
    output_file.write(f"{function_id:>10}                   0                   0\n")
    #write the asssociated material function
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/FUNCT/{function_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#                  X                   Y\n")
    #write the function x y pairs
    for item in xy_data:
        x, y = item
        output_file.write(f"{x:>20.15g}{y:>20.15g}\n")

# MAT LAW71
# writes law71 superelastic material
def write_supere_material(
    material_id, material_name, rho, emodulus, poissrat, se_mm, se_mpr, se_uts, se_tbt, se_tet, se_trbt, se_tret, se_tbc,
    se_reftemp, se_slope_load, se_slope_unload, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW71/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}\n")
    output_file.write("#                  E                  NU              E_mart\n")
    output_file.write(f"{emodulus:>20.15g}{se_mpr:>20.15g}{se_mm:>20.15g}\n")

    #calculate alpha from se_tbt (start stress in tension) and se_tbc (start stress in compression)
    root_two_thirds = (2 / 3) ** 0.5 # root 2/3
    top = se_tbc - se_tbt # comp - tens
    bottom = se_tbc + se_tbt # comp + tens
    alpha = root_two_thirds * (top / bottom)

    output_file.write("#           sig_AS_s            sig_AS_f            sig_SA_s            sig_SA_f               alpha\n")
    output_file.write(f"{se_tbt:>20.15g}{se_tet:>20.15g}{se_trbt:>20.15g}{se_tret:>20.15g}{alpha:>20.15g}\n")
    output_file.write("#               EpsL                 CAS                 CSA               TS_AS               TF_AS\n")
    output_file.write(f"{se_uts:>20.15g}{se_slope_load:>20.15g}{se_slope_unload:>20.15g}{se_reftemp:>20.15g}{se_reftemp:>20.15g}\n")
    output_file.write("#              TS_SA               TF_SA                  CP                TINI\n")
    output_file.write(f"{se_reftemp:>20.15g}{se_reftemp:>20.15g}               10e30{se_reftemp:>20.15g}\n")

# MAT LAW82
# writes law82 ogden material
def write_ogden_material(
    material_id, material_name, rho, ogden_mu, ogden_alpha, ogden_D, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/LAW82/{material_id}\n")
    output_file.write(material_name + "\n")
    output_file.write("#              RHO_I\n")
    output_file.write(f"{rho:>20.15g}                   0\n")
    output_file.write("#        N                            nu\n")
    output_file.write("         1                             0\n")
    output_file.write("#               Mu_i\n")
    output_file.write(f"{ogden_mu:>20.15g}\n")
    output_file.write("#            Alpha_i\n")
    output_file.write(f"{ogden_alpha:>20.15g}\n")
    output_file.write("#                D_i\n")
    output_file.write(f"{ogden_D:>20.15g}\n")


# RIGIDS
# writes void material for rigid parts
def write_rigid_material(
    material_id, material_name, output_file
    ):
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/MAT/VOID/{material_id}\n")
    #print(f"/MAT/VOID/{material_id}\n")
    output_file.write(material_name + "\n")
    #print(f"name: {material_name}")
    output_file.write("#                RHO                   E                  NU\n")
    output_file.write(f"              7.8E-9              210000                 0.3\n")

# MASSES
# writes admas cards
def write_admas(material_name, nsets, mass, output_file):
    nset_data = nsets.get(material_name)
    #look up the nset counter for the referenced nset (based on the surface)
    admas_grnid = nset_data['id'] if nset_data else 0
    output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    output_file.write(f"/ADMAS/0/{admas_grnid}\n")
    #print(f"ADMAS derived from {material_name}\n")
    output_file.write(f"ADMAS from ELSET: {material_name}\n")
    #print(f"name: {material_name}")
    output_file.write("#               Mass   grnd_ID\n")
    output_file.write(f"{mass:>20.15g}{admas_grnid:>10}\n")

####################################################################################################
# Function to convert Properties/Parts                                                             #
#                                                                                                  #
#   'PARTS' are linked to the ELSETS defined at element creation (if existing)                     #
#                                                                                                  #
#   RIGID elements have special treatment, if an ELSET is defined, it is used as the               #
#           PROP and PART, if it doesn't exist, we create new part and prop                        #
#                                                                                                  #
#   Usually 'PARTS' don't really exist in .inp, (ignoring parts in the context of instances)       #
#                                                                                                  #
#     we observe logic as follows:                                                                 #
#                                                                                                  #
#   The ELSET existing for an element at element creation becomes its 'PART' (same as PROP)        #
#                                                                                                  #
#   Except in cases where the section references an ELSET that then references the ELSET defined   #
#   at element creation  in which case the ELSET, ELSET is PROP, and 'Element ELSET' is PART       #
#                                                                                                  #
#   Other unreferenced ELSETS are retained in the model                                            #
#                                                                                                  #
####################################################################################################
def convert_props(input_lines, material_names):
    prop_id = 1  # Initialize the property ID
    property_names = {}  # initializes a dictionary of Property name relationships
    other_rigid_props_processed_list = []
    i = 0  # Initialize an index for iterating through input_lines
    # Regular expression pattern for ELSET matching
    elset_pattern = r'\bELSET\s*=\s*("([\w\-+/ ]+)"|[\w\-+/ ]+)'

    #this section checks for property attributes
    #and stores them against the dictionary of property names
    while i < len(input_lines):
        line = input_lines[i].strip()

        #define pattern matches for various element types (+ rigid elements)
        shell_line_pattern = r'^\s*\*SHELL\s+SECTION\s*,\s*ELSET\s*=\s*[^,]+\s*,?.*$'
        shell_line_match = re.search(shell_line_pattern, line, re.IGNORECASE)
        membrane_line_pattern = r'^\s*\*membrane\s+SECTION\s*,\s*ELSET\s*=\s*[^,]+\s*,?.*$'
        membrane_line_match = re.search(membrane_line_pattern, line, re.IGNORECASE)
        solid_line_pattern = r'^\s*\*solid\s+SECTION\s*,\s*ELSET\s*=\s*[^,]+\s*,?.*$'
        solid_line_match = re.search(solid_line_pattern, line, re.IGNORECASE)
        cohesive_line_pattern = r'^\s*\*cohesive\s+SECTION\s*,\s*ELSET\s*=\s*[^,]+\s*,?.*$'
        cohesive_line_match = re.search(cohesive_line_pattern, line, re.IGNORECASE)
        connector_line_pattern = r'^\s*\*connector\s+SECTION\s*,\s*ELSET\s*=\s*[^,]+\s*,?.*$'
        connector_line_match = re.search(connector_line_pattern, line, re.IGNORECASE)
        rigid_line_pattern = r'^\s*\*ELEMENT\s*,?\s*TYPE\s*=\s*R3D[34]\b.*$'
        rigid_line_match = re.search(rigid_line_pattern, line, re.IGNORECASE)
        massdef_line_pattern = r'^\s*\*MASS\s*,\s*ELSET\s*=\s*[^,]+\s*,?.*$'
        massdef_line_match = re.search(massdef_line_pattern, line, re.IGNORECASE)
        dcoup_line_pattern = r'^\s*\*ELEMENT\s*,?\s*TYPE\s*=\s*DCOUP3D\b.*$'
        dcoup_line_match = re.search(dcoup_line_pattern, line, re.IGNORECASE)

        if shell_line_match:
            section_type = 'shell'
            # regular expression to find 'material =' or 'material='
            mat_pattern = r'material\s*=\s*([^,]+)'
            match = re.search(mat_pattern, line, re.IGNORECASE)
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            if elset_match:
                property_name = elset_match.group(1).strip()
            if match:
                material_name = match.group(1).strip()
            i += 1 # Move to the next line
            if i < len(input_lines):
                next_line = input_lines[i].strip()
                shthk = next_line.split(',')[0].strip()

        elif membrane_line_match:
            section_type = 'membrane'
            # regular expression to find 'material =' or 'material='
            mat_pattern = r'material\s*=\s*([^,]+)'
            match = re.search(mat_pattern, line, re.IGNORECASE)
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            if elset_match:
                property_name = elset_match.group(1).strip()
            if match:
                material_name = match.group(1).strip()
            i += 1 # Move to the next line
            if i < len(input_lines):
                next_line = input_lines[i].strip()
                shthk = next_line.split(',')[0].strip()

        elif solid_line_match:
            section_type = 'solid'
            # regular expression to find 'material =' or 'material='
            mat_pattern = r'material\s*=\s*([^,]+)'
            match = re.search(mat_pattern, line, re.IGNORECASE)
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            if elset_match:
                property_name = elset_match.group(1).strip()
            if match:
                material_name = match.group(1).strip()

        elif cohesive_line_match:
            section_type = 'cohesive'
            # regular expression to find 'material =' or 'material='
            mat_pattern = r'material\s*=\s*([^,]+)'
            match = re.search(mat_pattern, line, re.IGNORECASE)
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            if elset_match:
                property_name = elset_match.group(1).strip()
            if match:
                material_name = match.group(1).strip()

        elif connector_line_match:
            section_type = 'connector'
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            if elset_match:
                property_name = elset_match.group(1).strip()
                material_name = elset_match.group(1).strip()
            i += 1 # Move to the next line
            if i < len(input_lines):
                next_line = input_lines[i].strip()
                conntype = next_line.split(',')[0].strip()

        elif massdef_line_match:
            section_type = 'massdef'
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            if elset_match:
                property_name = elset_match.group(1).strip()
                material_name = elset_match.group(1).strip()

        elif dcoup_line_match:
            section_type = 'dcoup'
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)

            if elset_match:
                property_name = "this_is_a_dcoup3d"


        #deal with rigid bodies
        elif rigid_line_match:
            # regular expression to find 'elset =' or 'elset='
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)
            #this_check_added since rigid elements don't need to be in an elset
            #but should have been assigned one by now!
            if elset_match is None:
                print ("Something Went Wrong")
            else:
                section_type = 'void_for_rigid'
                material_name = elset_match.group(1).strip()

        else:
            section_type = None

        # Extract property/part name and create a dictionary entry, rigids are special case
        if section_type == 'shell':
            # Assign a property ID to the property
            property_names[property_name] = {'prop_id': prop_id}
            property_names[property_name]['nint'] = '5'
            property_names[property_name]['shthk'] = shthk

        elif section_type == 'membrane':
            # Assign a property ID to the property
            property_names[property_name] = {'prop_id': prop_id}
            property_names[property_name]['nint'] = '1'
            property_names[property_name]['shthk'] = shthk

        elif section_type == 'cohesive':
            # Assign a property ID to the property
            property_names[property_name] = {'prop_id': prop_id}
            property_names[property_name]['nint'] = '888'

        elif section_type == 'connector':
            # Assign a property ID to the property
            property_names[property_name] = {'prop_id': prop_id}
            property_names[property_name]['nint'] = '555'
            property_names[property_name]['conntype'] = conntype
            property_names[property_name]['material_id'] = 0
            # Increment the property ID
            prop_id += 1


        elif section_type == 'solid':
            # Assign a property ID to the property
            property_names[property_name] = {'prop_id': prop_id}
            property_names[property_name]['nint'] = '999'

        elif section_type == 'dcoup':
            if property_name not in other_rigid_props_processed_list:
                # Assign a property ID to the property
                property_names[property_name] = {'prop_id': prop_id}
                other_rigid_props_processed_list.append(property_name)
                property_names[property_name]['nint'] = '333'
            section_type = None
            property_name = None

        elif section_type == 'void_for_rigid':
            property_name = elset_match.group(1).strip()
            if property_name not in other_rigid_props_processed_list:
                # Assign a property ID to the property
                property_names[property_name] = {'prop_id': prop_id}
                other_rigid_props_processed_list.append(property_name)
                property_names[property_name]['nint'] = '998'
                property_names[property_name]['shthk'] = '0.01'

        elif section_type == 'massdef':
            # Assign a property ID to the property
            property_names[property_name] = {'prop_id': prop_id}
            property_names[property_name]['nint'] = '777'

        if section_type and material_name in material_names:
            material_id = material_names[material_name]['material_id']
            property_names[property_name]['material_id'] = material_id

            section_type = None
            property_name = None
            # Increment the property ID
            prop_id += 1

            i += 1
        else:
            i += 1  # Move to the next line

    return property_names, prop_id


####################################################################################################
# Def to write parts                                                                               #
####################################################################################################
def write_parts(property_names, non_numeric_references, output_file):
    for property_name, property_data in property_names.items():
        # Look up the value (part_name) for the matching key
        part_name = next(
            (values[0] for key, values in non_numeric_references.items() if key == property_name),
            property_name  # Default to property_name if no match
        )

        if not property_data['nint'] == '777' and not property_data['nint'] == '333':
            #extract the property_id from dictionary and use as part_id
            part_id = property_data['prop_id']
            #extract the material_id from dictionary
            material_id = property_data['material_id']
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PART/{part_id}\n")
            output_file.write(part_name + "\n")
            output_file.write("#     prop       mat    subset\n")
            output_file.write(f"{part_id:>10}{material_id:>10}         0\n")


####################################################################################################
# Def to write properties                                                                          #
####################################################################################################
def write_props(property_names, output_file):
    for property_name, property_data in property_names.items():
        property_id = property_data['prop_id'] #generate property_id for this def
       #print(property_data)
        prop_type = property_data['nint']  # Get the 'type' value from property_data (nint value)
        # Check prop_type and write different cards based on its value
        if prop_type == '5': #5 is code for Shells
            shthk = float(property_data['shthk'])  # Get the 'shthk' value from property_data
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PROP/SHELL/{property_id}\n")
            output_file.write(property_name + "\n")
            output_file.write("#   Ishell    Ismstr     Ish3n    Idrill                            P_thick_fail\n")
            output_file.write("        24        -1         1         0                                       0\n")
            output_file.write("#                 hm                  hf                  hr                  dm                  dn\n")
            output_file.write("                   0                   0                   0                   0                .015\n")
            output_file.write("#        N                         Thick              Ashear              Ithick     Iplas\n")
            output_file.write(f"{prop_type:>10}          {shthk:>20.15g}                .833                   1         1\n")
        elif prop_type == '1': #1 is code for Membrane Shells
            shthk = float(property_data['shthk'])  # Get the 'shthk' value from property_data
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PROP/SHELL/{property_id}\n")
            output_file.write(property_name + "\n")
            output_file.write("#   Ishell    Ismstr     Ish3n    Idrill                            P_thick_fail\n")
            output_file.write("        24        -1         1         0                                       0\n")
            output_file.write("#                 hm                  hf                  hr                  dm                  dn\n")
            output_file.write("                   0                   0                   0                   0                .015\n")
            output_file.write("#        N                         Thick              Ashear              Ithick     Iplas\n")
            output_file.write(f"{prop_type:>10}          {shthk:>20.15g}                .833                   0         0\n")
        elif prop_type == '888': #888 is code for Cohesives
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PROP/TYPE43/{property_id}\n")
            output_file.write(property_name + "\n")
            output_file.write("#   Ismstr                                                                            True_Thickness\n")
            output_file.write("        -1                                                                                          \n")
        elif prop_type == '999': #999 is code for Solids
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PROP/SOLID/{property_id}\n")
            output_file.write(property_name + "\n")
            output_file.write("#   Isolid    Ismstr               Icpre  Itetra10     Inpts   Itetra4    Iframe                  dn\n")
            output_file.write("        24        -1                  -1         2         0         3         0                  .1\n")
            output_file.write("#                q_a                 q_b                   h            LAMBDA_V                MU_V\n")
            output_file.write("                 1.1                 .05                   0                   0                   0\n")
            output_file.write("#             dt_min            Vdef_min            Vdef_max             ASP_max             COL_min\n")
            output_file.write("                 0.0                0.01               100.0               100.0                0.01\n")
        elif prop_type == '998': #998 is code for Void
            shthk = float(property_data['shthk'])  # Get the 'shthk' value from property_data (hardcoded as 0.01 currently for void
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PROP/VOID/{property_id}\n")
            output_file.write(property_name + "\n")
            output_file.write("#              Thick\n")
            output_file.write(f"{shthk:>20.15g}\n")
        elif prop_type == '997': #997 is code for Thk Shells
            output_file.write("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
            output_file.write(f"/PROP/TYPE20/{property_id}\n")
            output_file.write(property_name + "\n")
            output_file.write("#   Isolid    Ismstr                                   Inpts      Iint                            dn\n")
            output_file.write("        15        -1                                       5         0                            .1\n")
            output_file.write("#                q_a                 q_b                   h\n")
            output_file.write("                 1.1                 .05                   0\n")
            output_file.write("#             dt_min\n")
            output_file.write("                   0\n")


####################################################################################################
# Function to convert CONN3D2 of type BEAM to Type13 Springs                                       #
####################################################################################################
def convert_connbeams(property_names):
    spring_k = e_magnitude * 5                       #
    spring_rk = e_magnitude * 7                      #    Spring Stiffnesses and densities are based
    spring_mass = rho_magnitude * 1                  #        on material values from model
    spring_inertia = rho_magnitude * 1.5             #

    conn_beams = []

    for property_name, property_data in property_names.items():
        property_id = property_data['prop_id'] #generate property_id for this def
        prop_type = property_data['nint']  # Get the 'type' value from property_data (nint value)
        # Check prop_type and write different cards based on its value

        if prop_type == '555': #555 is code for Beam type Springs
            conntype = property_data['conntype']  # Get the 'conntype' value from property_data

            conn_beams.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            conn_beams.append(f"#Spring PROP for connection definition: {property_name}: for .inp CONN3D2 Beams")
            conn_beams.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            conn_beams.append(f"/PROP/TYPE13/{property_id}\n{property_name}")
            conn_beams.append("#               Mass             Inertia   skew_ID   sens_ID    Isflag     Ifail     Ileng    Ifail2")
            conn_beams.append(f"{spring_mass:>20.4e}{spring_inertia:>20.4e}         0         0         0         0         0         0")
            conn_beams.append("#                 K1                  C1                  A1                  B1                  D1")
            conn_beams.append(f"{spring_k:>20.4e}                   0                   0                   0                   0")
            conn_beams.append("# fct_ID11        H1  fct_ID21  fct_ID31  fct_ID41                    delta_min1          delta_max1")
            conn_beams.append("         0         0         0         0         0                             0                   0")
            conn_beams.append("#                 F1                  E1             Ascale1             Hscale1")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("#                 K2                  C2                  A2                  B2                  D2")
            conn_beams.append(f"{spring_k:>20.4e}                   0                   0                   0                   0")
            conn_beams.append("# fct_ID12        H2  fct_ID22  fct_ID32  fct_ID42                    delta_min2          delta_max2")
            conn_beams.append("         0         0         0         0         0                             0                   0")
            conn_beams.append("#                 F2                  E2             Ascale2             Hscale2")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("#                 K3                  C3                  A3                  B3                  D3")
            conn_beams.append(f"{spring_k:>20.4e}                   0                   0                   0                   0")
            conn_beams.append("# fct_ID13        H3  fct_ID23  fct_ID33  fct_ID43                    delta_min3          delta_max3")
            conn_beams.append("         0         0         0         0         0                             0                   0")
            conn_beams.append("#                 F3                  E3             Ascale3             Hscale3")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("#                 K4                  C4                  A4                  B4                  D4")
            if conntype.lower() == 'hinge':
                conn_beams.append("                   0                   0                   0                   0                   0")
            else:
                conn_beams.append(f"{spring_rk:>20.4e}                   0                   0                   0                   0")
            conn_beams.append("# fct_ID14        H4  fct_ID24  fct_ID34  fct_ID44                    delta_min4          delta_max4")
            conn_beams.append("         0         0         0         0         0                             0                   0")
            conn_beams.append("#                 F4                  E4             Ascale4             Hscale4")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("#                 K5                  C5                  A5                  B5                  D5")
            conn_beams.append(f"{spring_rk:>20.4e}                   0                   0                   0                   0")
            conn_beams.append("# fct_ID15        H5  fct_ID25  fct_ID35  fct_ID45                    delta_min5          delta_max5")
            conn_beams.append("         0         0         0         0         0                             0                   0")
            conn_beams.append("#                 F5                  E5             Ascale5             Hscale5")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("#                 K6                  C6                  A6                  B6                  D6")
            conn_beams.append(f"{spring_rk:>20.4e}                   0                   0                   0                   0")
            conn_beams.append("# fct_ID16        H6  fct_ID26  fct_ID36  fct_ID46                    delta_min6          delta_max6")
            conn_beams.append("         0         0         0         0         0                             0                   0")
            conn_beams.append("#                 F6                  E6             Ascale6             Hscale6")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("#                 V0              Omega0               F_cut   Fsmooth")
            conn_beams.append("                   0                   0                   0         0")
            conn_beams.append("#                  C                   n               alpha                beta")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("                   0                   0                   0                   0")
            conn_beams.append("                   0                   0                   0                   0")

    return conn_beams


####################################################################################################
# Function to extract standalone *ELSET (not prop linked), used by (Some) TIE, RBODY and DLOAD     #
#   and elsets referenced by name by those types that ARE prop linked,                             #
#   has later sub function: 'write_element_groups'                                                 #
####################################################################################################
def prepare_elsets(input_lines, elsets_for_expansion_dict, relsets_for_expansion_dict):
    elset_dicts = {} #initialize a dictionary to track elsets being processed between defs
    elset_processing_list = []

    inside_surface_section = False

    for line in input_lines:

        stype_pattern = r'^\*SURFACE\s*,\s*(?!.*TYPE\s*=\s*NODE)(?:NAME\s*=\s*[^\s,]+|TYPE\s*=\s*[^\s,]+)'

        matchelement = re.search(stype_pattern, line, re.IGNORECASE)

        if matchelement:
            inside_surface_section = True
            continue  # Skip the *SURFACE line

        if inside_surface_section and line.startswith('*'):
            inside_surface_section = False

        if inside_surface_section:
            surface_values = line.split(",")  # Split the line by comma
            surface_el = surface_values[0].strip()

            # Check if surface_el is a numerical ID or a text string
            if surface_el.isdigit():
                continue

            elset_name = surface_el
            #this is to handle syntax where a blank line creates an
            #'All Exterior Surfs' Surface, this is handled in Surface Parsing Separately
            if elset_name == '':
                elset_name = 'IGNORE Automatic Surf All'
            elset_processing_list.append(elset_name)
            continue

    for elset_name, elements in elsets_for_expansion_dict.items():
        elset_values = []
        elset_values.extend(list(elements))
        elset_dicts[elset_name] = elset_values

    for elset_name, elements in relsets_for_expansion_dict.items():
        elset_values = []
        elset_values.extend(list(elements))
        elset_dicts[elset_name] = elset_values

# this section creates a dictionary of elset element ids recorded against their elset_name
    inside_elset_section = False
    elset_name = None

    for elset_name in elset_processing_list:

        if elset_name == 'IGNORE Automatic Surf All':
            continue

        if elset_name in elset_dicts.keys():
            continue

        elset_line_pattern = r'^\s*\*ELSET\s*,?\s*ELSET\s*=\s*{}\b'.format(re.escape(elset_name))
        elset_found = False
        if run_timer and elset_name:
            elapsed_time = time.time() - start_time
            print(f"Elsets being built:    {elapsed_time:8.3f} seconds: ({elset_name} done)")

        for line in input_lines:
            elset_line_match = re.search(elset_line_pattern, line, re.IGNORECASE)
            if elset_line_match:
                inside_elset_section = True
                elset_values = []
                elset_found = True
                continue

            if inside_elset_section and line.startswith('*'):
                inside_elset_section = False
                continue

            if inside_elset_section and line.strip():  # Skip empty lines
                values = line.split(',')
                elset_values.extend([value.strip() for value in values if value.strip()])
                elset_dicts[elset_name] = elset_values

        if not elset_found:
            elset_values = []
            elset_dicts[elset_name] = elset_values

    return elset_dicts


####################################################################################################
# Function to parse element data, has sub functions                                                #
# 'process_element_block' and 'convert_elements'                                                   #
####################################################################################################
def parse_element_data(input_lines, elset_dicts, property_names, non_numeric_references, nsets, nset_counter):
    max_elem_id = 0  # Initialize the maximum element ID
    element_dicts = {}  # Dictionary to store element type dictionaries
    current_element_type = None
    current_element_block = []
    remaining_lines = []
    ppmselect = False

    for line in input_lines:
        # Regular expression to find '*ELEMENT,TYPE='
        etype_pattern = r'^\s*\*ELEMENT\s*,\s*TYPE\s*='
        match = re.search(etype_pattern, line, re.IGNORECASE)

        if match: #Instance of a *ELEMENT line
            #calls 'process_element_block' subdef below
            if any(current_element_block):
                element_dict, max_elem_id = process_element_block(
                    current_element_block, current_element_type, max_elem_id
                    )

                if element_dict:
                    current_element_dicts = element_dicts.get(current_element_type, [])
                    #print(current_element_type)
                    try:
                        property_id = property_names[prop_match]['prop_id']
                        current_element_dicts.append(
                            {"ELSET": elset, "PROP_ID": property_id, "elements": element_dict}
                            )
                    except:
                        current_element_dicts.append(
                            {"ELSET": elset, "PROP_ID": 0, "elements": element_dict}
                            )
                        print ("Warning: No Property Found for Element, if using PrePoMax, use PARTS as Property assignment, not 'Selection'")
                        ppmselect = True
                    element_dicts[current_element_type] = current_element_dicts
                    if current_element_type.lower() == 'sc8r':
                        property_names[prop_match]['nint'] = '997'
                    current_element_block = []  # Start a new element block
                    current_element_type = None

            # regular expression to find element_type_string
            element_type_pattern = r'\bTYPE\s*=\s*([^,]+)'
            element_type_match = re.search(element_type_pattern, line, re.IGNORECASE)
            current_element_type = element_type_match.group(1).strip()
            if current_element_type.lower() == 'dcoup3d':
                prop_match = 'this_is_a_dcoup3d'
                current_element_block = []  # Start a new element block buffer
                continue

            # regular expression to find 'elset =' or 'elset='
            elset_pattern = r'\bELSET\s*=\s*("([\w\-+/ ]+)"|[\w\-+/ ]+)'
            elset_match = re.search(elset_pattern, line, re.IGNORECASE)

            #this_check_added since rigid elements don't need to be in an elset
            #but should have been assigned one by now!
            if elset_match is None:
                print("Something Went Wrong, No Elset Found")
            else:
                elset = elset_match.group(1).strip()

                # Normalize elset for comparison: remove spaces and convert to lowercase
                normalized_elset = elset.replace(" ", "").lower()

                # Find the property in a case-insensitive and space-agnostic way
                prop_match = next(
                    (key for key in property_names
                     if key.replace(" ", "").lower() == normalized_elset), None
                )

                if not prop_match:
                    # Check in non_numeric_references with similar normalization
                    prop_match = next(
                        (key for key, values in non_numeric_references.items()
                         if normalized_elset in [v.replace(" ", "").lower() for v in values]), None
                    )

                if prop_match:
                    property_id = property_names[prop_match]['prop_id']
                    current_element_block = []  # Start a new element block buffer

                else:
                    # Handle the case where the substituted elset doesn't exist in property_names
                    current_element_block = []  # Start a new element block buffer

            continue

        if current_element_type and not line.startswith('*'):
            current_element_block.append(line)

        elif current_element_type and line.startswith('*'):
            remaining_lines.append(line)
            #calls 'process_element_block' subdef below
            if any(current_element_block):
                element_dict, max_elem_id = process_element_block(
                    current_element_block, current_element_type, max_elem_id
                    )
                current_element_dicts = element_dicts.get(current_element_type, [])
                try:
                    property_id = property_names[prop_match]['prop_id']
                    current_element_dicts.append(
                        {"ELSET": elset, "PROP_ID": property_id, "elements": element_dict}
                        )
                except:
                    current_element_dicts.append(
                        {"ELSET": elset, "PROP_ID": 0, "elements": element_dict}
                        )
                    print ("WARNING: No Property Found for Element,")
                    print ("         if using PrePoMax, use PARTS for Property assignment, not 'Selection'")
                    ppmselect = True
                element_dicts[current_element_type] = current_element_dicts
                if current_element_type.lower() == 'sc8r':
                    property_names[elset]['nint'] = '997'
                current_element_block = []  # Start a new element block
                current_element_type = None
        else:
            remaining_lines.append(line)  # Collect the remaining lines
            #input_lines = remaining_lines  # commented for now

    #calls the 'convert elements' subdef below (format for output)
    (elset_dicts, element_lines, sh3n_list, shell_list, brick_list,
     nsets, nset_counter) = convert_elements(elset_dicts,
     element_dicts, nsets, nset_counter
     )

    if not debug_mode:
        return (
            elset_dicts, element_lines, element_dicts, sh3n_list, shell_list, brick_list,
            property_names, max_elem_id, input_lines, nsets, nset_counter, ppmselect
            )


####################################################################################################
#debug to check the filtered input                                                                 #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_filter_postelements.inp"#FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)#FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in input_lines:  # for debug
            test_output_file.write(filtered_line) # Write the filtered deck # for debug

    print("postelements written")
    return (
        elset_dicts, element_lines, element_dicts, sh3n_list, shell_list, brick_list,
        property_names, max_elem_id, input_lines, nsets, nset_counter, ppmselect
        )


####################################################################################################
#SubFunction to process the element block passed by 'parse_element_data'                           #
####################################################################################################
def process_element_block(current_element_block, current_element_type, max_elem_id):
    element_list = []  # List to store dictionaries for element IDs and nodes

    # Concatenate lines into a single string, removing newlines and whitespaces
    element_data_str = ''.join(current_element_block)
    element_data_str = element_data_str.replace(' ', '')

    # Determine the number of nodes based on the element_type
    element_type_nodes = {
        'MASS': 1, 'DCOUP3D': 1, 'CONN3D2': 2, 'S3': 3, 'S3R': 3, 'M3D3': 3,
        'R3D3': 3, 'S4': 4, 'S4R': 4, 'R3D4': 4, 'M3D4R': 4, 'C3D4': 4,
        'C3D6': 6, 'COH3D6': 6, 'SC6R': 6, 'SC8R': 8, 'C3D8': 8,
        'C3D8I': 8, 'COH3D8': 8,'C3D8R': 8, 'C3D10': 10, 'C3D10M': 10
    }

    num_nodes = element_type_nodes.get(current_element_type, 0)

    if num_nodes == 0:
        print(f"Warning: Unknown element type {current_element_type}")

        if or_gui:
            print("### INFO ###")
            print(f"element type {current_element_type} is not yet supported by A2R")
            print("please try to use an alternative")
            print("or you may try standalone conversion by calling this script at commandline")
            sys.exit("A2R unable to continue")

        else:
            print("### INFO ###")
            print(f"element type {current_element_type} is not yet supported by A2R")
            print("please try to use an alternative")
            print("process will attempt to continue the best it can")
            print("")
            input("press enter to continue")

        return [element_list, max_elem_id]

    # Remove trailing '\n' and replace newlines with commas
    element_data_str = element_data_str.rstrip('\n').replace('\n', ',').replace(',,', ',')

    # Ensure no trailing commas
    if element_data_str.endswith(','):
    # Remove trailing comma
        element_data_str = element_data_str.rstrip(',')
    else:
        element_data_str = element_data_str

    # Split the concatenated string into element and node data
    elements = element_data_str.split(',')

    # Iterate through the elements with step size of num_nodes + 1 (1 for element ID + nodes)
    for i in range(0, len(elements), num_nodes + 1):
        # If we can't get the full set of element ID + nodes, mark it as incomplete
        if i + num_nodes + 1 > len(elements):
            incomplete_element = elements[i:]
            print(f"Warning: Incomplete element definition at index {i}")
            print(f"Incomplete element data: {incomplete_element}")
            continue


        element_id = int(elements[i])
        max_elem_id = max(max_elem_id, element_id)

        # Extract nodes and validate their count
        nodes = elements[i + 1: i + num_nodes + 1]
        if len(nodes) != num_nodes:
            print(f"Warning: Element {element_id} has an incorrect number of nodes ({len(nodes)} instead of {num_nodes})")
            print(f"Element data: ID = {element_id}, Nodes = {nodes}")
            continue  # Skip malformed elements

        element_data = {
            'element_id': element_id,
            'nodes': nodes
        }
        element_list.append(element_data)

    return element_list, max_elem_id


####################################################################################################
# Function to convert elements data dictionary for output                                          #
####################################################################################################
def convert_elements(elset_dicts, element_dicts, nsets, nset_counter):
    element_lines = []
    sh3n_list = []
    shell_list = []
    brick_list = []
    spring_list = []

    for element_type, element_list in element_dicts.items():

        for element_dict in element_list:
            elset = element_dict["ELSET"]
            property_id = element_dict ["PROP_ID"]

            if element_type.lower() == "mass":
                nset_counter += 1
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# Node Set for Masses from Elset: {elset}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/GRNOD/NODE/{nset_counter}")  # Output section header
                nsets[elset] = {'id': nset_counter}
                element_lines.append(f"nodes with added mass from Elset {elset}")
                element_lines.append("#   NODEID")
                for element in element_dict["elements"]:
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{formatted_nodes}")

            elif element_type.lower() == "conn3d2":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# Spring Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/SPRING/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to sh3n_list
                    spring_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

            elif (element_type.lower() == "s3"
                or element_type.lower() == "s3r"
                or element_type.lower() == "r3d3"
                or element_type.lower() == "m3d3"
                ):
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 3 Noded Shell Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/SH3N/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to sh3n_list
                    sh3n_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif (element_type.lower() == "s4"
                or element_type.lower() == "s4r"
                or element_type.lower() == "r3d4"
                or element_type.lower() == "m3d4r"
                ):
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 4 Noded Shell Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/SHELL/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to shell_list
                    shell_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif element_type.lower() == "c3d4":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 4 Noded Tetrahedral Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/TETRA4/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    nodes = [nodes[0], nodes[2], nodes[1], nodes[3]]
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif element_type.lower() == "c3d6":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 6 Noded Degenerated Penta Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/BRICK/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    nodes = [nodes[0], nodes[1], nodes[2], nodes[2], nodes[3], nodes[4], nodes[5], nodes[5]]
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif element_type.lower() == "coh3d6":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 6 Noded Degenerated Penta Cohesive Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/BRICK/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    nodes = [nodes[0], nodes[1], nodes[2], nodes[2], nodes[3], nodes[4], nodes[5], nodes[5]]
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif element_type.lower() == "sc6r":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 6 Noded Degenerated Penta Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/BRICK/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    nodes = [nodes[0], nodes[1], nodes[2], nodes[2], nodes[3], nodes[4], nodes[5], nodes[5]]
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif (element_type.lower() == "c3d8"
                or element_type.lower() == "c3d8i"
                or element_type.lower() == "c3d8r"
                ):
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 8 Noded Brick Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/BRICK/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(',')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif element_type.lower() == "coh3d8":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 8 Noded Cohesive Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/BRICK/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(',')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif element_type.lower() == "sc8r":
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 8 Noded Thick Shell Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/BRICK/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(',')
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

            elif (element_type.lower() == "c3d10"
                or element_type.lower() == "c3d10m"
                ):
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"# 10 Noded Tetrahedral Elements for PART: {elset}, PID: {property_id}")
                element_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                element_lines.append(f"/TETRA10/{property_id}")  # Output section header
                for element in element_dict["elements"]:
                    element_id = element.get('element_id', '')
                    # Add element_id to brick_list
                    brick_list.append(element_id)
                    nodes = ', '.join(element.get('nodes', []))
                    nodes = nodes.split(', ')
                    nodes = [nodes[0], nodes[2], nodes[1], nodes[3], nodes[6], nodes[5], nodes[4], nodes[7], nodes[9], nodes[8]]
                    formatted_nodes = ''.join([value.rjust(10) for value in nodes])
                    element_lines.append(f"{element_id:>10}\n{formatted_nodes}")

                    #check if this elset is referenced in elset_dicts (means it maybe referenced by another card), add the element_id
                    if elset in elset_dicts:
                        elset_dict = elset_dicts[elset]
                        elset_dict.append(element_id)

    return elset_dicts, element_lines, sh3n_list, shell_list, brick_list, nsets, nset_counter


####################################################################################################
# Takes data from 'convert_elsets' and 'convert_elements' and writes the Radioss Groups            #
# for 'Standalone' (not prop linked) Elsets                                                        #
####################################################################################################
def write_element_groups(nset_counter, nsets, sh3n_list, shell_list, brick_list, elset_dicts):
    elset_mapping_set = {}  # Create empty dictionaries
    elset_blocks = []
    grnset_lines = []
    grngrn_store = {} #initialises dictionary for creating the final grnod/grnod for each elset

# this section looks up the element ids in the elset dictionary and establishes their element type,
# by cross referencing against element type lists created during element creation

    # Iterate through the initial elset data
    for elset_name, values in elset_dicts.items():

        # Initialize a list to hold numeric values, filtering for set-set by name refs
        numeric_values = []

        # Try converting each value to int, handling non-numeric values
        for value in values:
            if isinstance(value, int):
                numeric_values.append(int(value))  # Attempt to convert to int
            elif isinstance(value, str) and value.isdigit():
                # Convert numeric strings to integers
                numeric_values.append(int(value))

            else:
                print(f"Warning: Skipping non-integer value '{value}' in elset '{elset_name}'") # For debug
                continue

        elset_values_sh3n = list(set(numeric_values) & set(sh3n_list))
        elset_values_shell = list(set(numeric_values) & set(shell_list))
        elset_values_brick = list(set(numeric_values) & set(brick_list))

        # sh3n mapping
        # Initialize the mapped name based on the sh3n mapping
        if elset_values_sh3n:
            mapped_name = f"{elset_name}_sh3n"
            # Create a new entry in the elset_mapping_set dictionary if not already present
            if mapped_name not in elset_mapping_set:
                elset_mapping_set[mapped_name] = []

            # Append the value to the mapped name in the dictionary entry
            for value in elset_values_sh3n:
                elset_mapping_set[mapped_name].append(value)

        # shell mapping
        # Initialize the mapped name based on the shell mapping
        if elset_values_shell:
            mapped_name = f"{elset_name}_shell"
            # Create a new entry in the elset_mapping_set dictionary if not already present
            if mapped_name not in elset_mapping_set:
                elset_mapping_set[mapped_name] = []

            # Append the value to the mapped name in the dictionary entry
            for value in elset_values_shell:
                elset_mapping_set[mapped_name].append(value)

        # brick mapping
        # Initialize the mapped name based on the brick mapping
        if elset_values_brick:
            mapped_name = f"{elset_name}_brick"
            # Create a new entry in the elset_mapping_set dictionary if not already present
            if mapped_name not in elset_mapping_set:
                elset_mapping_set[mapped_name] = []

            # Append the value to the mapped name in the dictionary entry
            for value in elset_values_brick:
                elset_mapping_set[mapped_name].append(value)

    for elset, elset_data in elset_mapping_set.items():
        element_type = elset.split("_")[-1]  # Extract the element type (e.g., sh3n, shell, brick)
        elset_basename = elset.rsplit("_", 1)[0]  # Extract the elset basename (e.g., sh3n, shell, brick)

        # Initialize lines for each element type
        elset_lines = []
        nelset_lines = []

        # Define headers and titles based on element_type
        if element_type == "sh3n":
            nset_counter += 1
            elset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            elset_lines.append("#Tria Element Group for standalone *ELSET entries in .inp input")
            elset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            elset_lines.append(f"/GRSH3N/SH3N/{nset_counter}")
            elset_sh3n_short_name = f"{elset_basename}___sh3ns"
            elset_sh3n_name = f"Group of SH3Ns derived from {elset_basename}"
            elset_lines.append(f"{elset_sh3n_name}")
            elset_lines.append("#    SH3NS")
            nsets[elset_sh3n_short_name] = {'id': nset_counter} # Store the name/ID relationship
            nset_counter += 1
            nelset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            nelset_lines.append("#Node group based on standalone SH3N *ELSET entries in .inp input")
            nelset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            nelset_lines.append(f"/GRNOD/GRSH3N/{nset_counter}")
            nelset_sh3n_short_name = f"{elset_basename}___grnod"
            nelset_sh3n_name = f"Node Group of SH3Ns derived from {elset_basename}"
            nset_data = nsets.get(elset_sh3n_short_name)
            #look up the nset counter for the referenced nset (based on the surface)
            nelset_counter = nset_data['id'] if nset_data else 0
            nelset_lines.append(f"{nelset_sh3n_name}")
            nelset_lines.append("# GRSH3NID")
            nelset_lines.append(f"{nelset_counter:10d}")
            nsets[nelset_sh3n_short_name] = {'id': nset_counter} # Store the name/ID relationship

            # Create a new entry in the grngrn_store dictionary (to keep track of grnod/grnods)
            if elset_basename not in grngrn_store:
                grngrn_store[elset_basename] = []
            # Append the value to the mapped name in the dictionary entry
            grngrn_store[elset_basename].append(nset_counter)

        elif element_type == "shell":
            nset_counter += 1
            elset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            elset_lines.append("#Quadrilateral Shell Element Group for standalone *ELSET entries in .inp input")
            elset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            elset_lines.append(f"/GRSHEL/SHEL/{nset_counter}")
            elset_shell_short_name = f"{elset_basename}___shells"
            elset_shell_name = f"Group of SHELLs derived from {elset_basename}"
            elset_lines.append(f"{elset_shell_name}")
            elset_lines.append("#   SHELLS")
            nsets[elset_shell_short_name] = {'id': nset_counter} # Store the name/ID relationship
            nset_counter += 1
            nelset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            nelset_lines.append("#Node group based on standalone SHELL *ELSET entries in .inp input")
            nelset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            nelset_lines.append(f"/GRNOD/GRSHEL/{nset_counter}")
            nelset_shell_short_name = f"{elset_basename}___grnod"
            nelset_shell_name = f"Node Group of SHELLs derived from {elset_basename}"
            nset_data = nsets.get(elset_shell_short_name)
            #look up the nset counter for the referenced nset (based on the surface)
            nelset_counter = nset_data['id'] if nset_data else 0
            nelset_lines.append(f"{nelset_shell_name}")
            nelset_lines.append("# GRSHELID")
            nelset_lines.append(f"{nelset_counter:10d}")
            nsets[nelset_shell_short_name] = {'id': nset_counter} # Store the name/ID relationship

            # Create a new entry in the grngrn_store dictionary (to keep track of grnod/grnods)
            if elset_basename not in grngrn_store:
                grngrn_store[elset_basename] = []
            # Append the value to the mapped name in the dictionary entry
            grngrn_store[elset_basename].append(nset_counter)

        elif element_type == "brick":
            nset_counter += 1
            elset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            elset_lines.append("#Solid Element Group for standalone *ELSET entries in .inp input")
            elset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            elset_lines.append(f"/GRBRIC/BRIC/{nset_counter}")
            elset_brick_short_name = f"{elset_basename}___bricks"
            elset_brick_name = f"Group of BRICKs,PENTAs,TETRAs derived from {elset_basename}"
            elset_lines.append(f"{elset_brick_name}")
            elset_lines.append("#   BRICKS")
            nsets[elset_brick_short_name] = {'id': nset_counter} # Store the name/ID relationship
            nset_counter += 1
            nelset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            nelset_lines.append("#Node group based on standalone BRICK *ELSET entries in .inp input")
            nelset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            nelset_lines.append(f"/GRNOD/GRBRIC/{nset_counter}")
            nelset_brick_short_name = f"{elset_basename}___grnod"
            nelset_brick_name = f"Node Group of BRICKs derived from {elset_basename}"
            nset_data = nsets.get(elset_brick_short_name)
            #look up the nset counter for the referenced nset (based on the surface)
            nelset_counter = nset_data['id'] if nset_data else 0
            nelset_lines.append(f"{nelset_brick_name}")
            nelset_lines.append("# GRBRICID")
            nelset_lines.append(f"{nelset_counter:10d}")
            nsets[nelset_brick_short_name] = {'id': nset_counter} # Store the name/ID relationship

            # Create a new entry in the grngrn_store dictionary (to keep track of grnod/grnods)
            if elset_basename not in grngrn_store:
                grngrn_store[elset_basename] = []
            # Append the value to the mapped name in the dictionary entry
            grngrn_store[elset_basename].append(nset_counter)

        # Extract element IDs from elset_data
        element_ids = elset_data
        elements_per_line = []

        # Iterate through element IDs and format them in 10 x 10 wide fixed format fields
        for element_id in element_ids:
            elements_per_line.append(f"{element_id:10d}")

            # Check if we have collected 10 elements
            if len(elements_per_line) == 10:
                elset_lines.append("".join(elements_per_line))
                elements_per_line = []

        # If there are remaining elements, add them to the last line
        if elements_per_line:
            elset_lines.append("".join(elements_per_line))

        # Formatted output for the elsets and nodesets
        elset_output = "\n".join(elset_lines)
        nelset_output = "\n".join(nelset_lines)

        # Append the formatted output to elset_blocks
        elset_blocks.append(elset_output)
        elset_blocks.append(nelset_output)

    # Add one further Node Group, representing all nodes of the element groups
    for grelset, grnodids in grngrn_store.items():
        formatted_grnodids = [f"{grnodid:10d}" for grnodid in grnodids]

        nset_counter += 1
        grnset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
        grnset_lines.append("#Node group based on all *ELSET entries in .inp input")
        grnset_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
        grnset_lines.append(f"/GRNOD/GRNOD/{nset_counter}")
        grnset_name = f"Node Group of all nodes of {grelset}"
        grnset_lines.append(f"{grnset_name}")
        grnset_lines.append("#  GRNODID")
        grnset_lines.append("".join(formatted_grnodids))
        nsets[grelset] = {'id': nset_counter} # Store the name/ID relationship

    grnset_output = "\n".join(grnset_lines)
    elset_blocks.append(grnset_output)

    return elset_blocks, nset_counter, nsets, elset_dicts


####################################################################################################################
# Function to convert segment data dictionary for later use by 'parse_surface_data', only runs if segments present #
####################################################################################################################
def convert_segments(element_dicts, input_lines):
    segment_dictionary = {}
    segments_converted_already = False # Initialize a flag to track if we did this already

    for line in input_lines:
        # Regular expression to find '*SURFACE' of type 'Element'
        stype_pattern = r'^\*SURFACE\s*,\s*(?:NAME\s*=\s*[^\s,]+|TYPE\s*=\s*[^\s,]+)\s*(?!.*TYPE\s*=\s*NODE)'
        matchelement = re.search(stype_pattern, line, re.IGNORECASE)

        if matchelement and not segments_converted_already:
            segments_converted_already = True # Set the flag to True to indicate we have converted segments already

            for element_type, element_list in element_dicts.items():

                for element_dict in element_list:
                    for element in element_dict["elements"]:
                        element_id = element.get('element_id', '')
                        nodes = element.get('nodes', [])

############### NB, all node indexing listed is from 0 (if there are 4 nodes in an element, they are nodes 0,1,2,3)

                        if (element_type.lower() == 'c3d6'
                            or element_type.lower() == 'coh3d6'
                            or element_type.lower() == 'sc6r'
                            ):
                            s1_nodes = [nodes[0], nodes[2], nodes[1]]  # Order as 0, 2, 1
                            s2_nodes = [nodes[5], nodes[3], nodes[4]]  # Order as 5, 3, 4
                            s3_nodes = [nodes[0], nodes[1], nodes[4], nodes[3]]  # Order as 0, 1, 4, 3
                            s4_nodes = [nodes[1], nodes[2], nodes[5], nodes[4]]  # Order as 1, 2, 5, 4
                            s5_nodes = [nodes[2], nodes[0], nodes[3], nodes[5]]  # Order as 2, 0, 3, 5
                            segment_dictionary[element_id] = {
                                's1': s1_nodes,
                                's2': s2_nodes, 
                                's3': s3_nodes, 
                                's4': s4_nodes, 
                                's5': s5_nodes, 
                            }
                        elif (element_type.lower() == 'c3d8'
                            or element_type.lower() == 'c3d8i'
                            or element_type.lower() == 'coh3d8'
                            or element_type.lower() == 'c3d8r'
                            or element_type.lower() == 'sc8r'
                            ):
                            s1_nodes = [nodes[0], nodes[3], nodes[2], nodes[1]]  # Order as 0, 3, 2, 1
                            s2_nodes = [nodes[7], nodes[4], nodes[5], nodes[6]]  # Order as 7, 4, 5, 6
                            s3_nodes = [nodes[0], nodes[1], nodes[5], nodes[4]]  # Order as 0, 1, 5, 4
                            s4_nodes = [nodes[1], nodes[2], nodes[6], nodes[5]]  # Order as 1, 2, 6, 5
                            s5_nodes = [nodes[2], nodes[3], nodes[7], nodes[6]]  # Order as 2, 3, 7, 6
                            s6_nodes = [nodes[3], nodes[0], nodes[4], nodes[7]]  # Order as 3, 0, 4, 7
                            segment_dictionary[element_id] = {
                                's1': s1_nodes,
                                's2': s2_nodes,
                                's3': s3_nodes, 
                                's4': s4_nodes,
                                's5': s5_nodes, 
                                's6': s6_nodes, 
                            }
                        elif element_type.lower() == 'c3d4':
                            s1_nodes = [nodes[0], nodes[2], nodes[1]]  # Order as 0, 2, 1
                            s2_nodes = [nodes[0], nodes[1], nodes[3]]  # Order as 0, 1, 3
                            s3_nodes = [nodes[1], nodes[2], nodes[3]]  # Order as 1, 2, 3
                            s4_nodes = [nodes[2], nodes[0], nodes[3]]  # Order as 2, 0, 3
                            segment_dictionary[element_id] = {
                                's1': s1_nodes,
                                's2': s2_nodes,
                                's3': s3_nodes, 
                                's4': s4_nodes, 
                            }
                        elif (element_type.lower() == 'c3d10'
                            or element_type.lower() == 'c3d10m'):
                            s1_nodes = [nodes[0], nodes[2], nodes[1]]  # Order as 0, 2, 1
                            s2_nodes = [nodes[0], nodes[1], nodes[3]]  # Order as 0, 1, 3
                            s3_nodes = [nodes[1], nodes[2], nodes[3]]  # Order as 1, 2, 3
                            s4_nodes = [nodes[2], nodes[0], nodes[3]]  # Order as 2, 0, 3
                            segment_dictionary[element_id] = {
                                's1': s1_nodes,
                                's2': s2_nodes,
                                's3': s3_nodes, 
                                's4': s4_nodes, 
                            }
                        elif (element_type.lower() == 's4'
                            or element_type.lower() == 's4r'
                            or element_type.lower() == 'r3d4'
                            or element_type.lower() == 'm3d4r'):
                            spos_nodes = [nodes[0], nodes[1], nodes[2], nodes[3]]  # Order as 0, 1, 2, 3
                            sneg_nodes = [nodes[3], nodes[2], nodes[1], nodes[0]]  # Order as 3, 2, 1, 0
                            segment_dictionary[element_id] = {
                                'spos': spos_nodes,
                                'sneg': sneg_nodes,
                            }
                        elif (element_type.lower() == 's3'
                            or element_type.lower() == 's3r'
                            or element_type.lower() == 'r3d3'
                            or element_type.lower() == 'm3d3'
                            ):
                            spos_nodes = [nodes[0], nodes[1], nodes[2]]  # Order as 0, 1, 2
                            sneg_nodes = [nodes[2], nodes[1], nodes[0]]  # Order as 2, 1, 0
                            segment_dictionary[element_id] = {
                                'spos': spos_nodes,
                                'sneg': sneg_nodes,
                            }

            return segment_dictionary


#########################################################################################################################
# New Faster Function to parse segment surfaces, based on segment_dictionary                                            #
#########################################################################################################################
def parse_surface_data(input_lines, elset_dicts, nset_counter, nsets,
    segment_dictionary, property_names
    ):
    surf_id = 0 # Initialize surface id
    surf_name_to_id = {} # Initialize surf id - name dictionary
    surface_lines = []
    current_surface_name = None
    current_node_surface_name = None
    surf_already_processed = False
    allsurf = False
    prop_id_list = []  # Initialize an empty list
    prop_lines = []

    remaining_lines = []

    for line in input_lines:
        stype_pattern = r'^\*SURFACE\s*,\s*(?:NAME\s*=\s*[^\s,]+|TYPE\s*=\s*[^\s,]+)\s*(?!.*TYPE\s*=\s*NODE)' # Regular expression to find '*SURFACE' of type 'Element'
        ntype_pattern = r'^\s*\*SURFACE\s*,\s*(?=.*\bTYPE\s*=\s*NODE\b)(?=.*\bNAME\s*=\s*[\w\-]+)?.*' # Regular expression to find '*SURFACE' of type 'Node'
        matchelement = re.search(stype_pattern, line, re.IGNORECASE)
        matchnode = re.search(ntype_pattern, line, re.IGNORECASE)

        if matchnode:
            current_surface_name = None
            surf_already_processed = False
            # Extract surface name from the current line
            surface_name_match = re.search(r'\bNAME\s*=\s*([^,]+)', line, re.IGNORECASE)
            surface_name = surface_name_match.group(1).strip()
            nset_new_name = f"{surface_name}___originalnodeset"
            current_node_surface_name = surface_name
            continue

        if matchelement:
            current_node_surface_name = None
            surf_already_processed = False
            # Extract surface name from the current line
            surface_name_match = re.search(r'\bNAME\s*=\s*([^,]+)', line, re.IGNORECASE)
            surface_name = surface_name_match.group(1).strip()#.lower()
            current_surface_name = surface_name
            surf_id += 1 # Increment the surf_id
            surf_name_to_id[surface_name] = surf_id  # Store the name/ID relationship
            continue

        if current_node_surface_name and not line.startswith('*'):
            surface_values = line.split(",")  # Split the line by comma
            nset_name = surface_values[0].strip()#.lower()
            nset_data = nsets.get(nset_name)
            #look up the nset counter for the referenced nset (based on the surface)
            ref_nset_counter = nset_data['id'] if nset_data else 0
            nsets[nset_new_name] = {'id': ref_nset_counter}
            continue

        if current_node_surface_name and line.startswith('*'):
            current_node_surface_name = None

        if current_surface_name and not line.startswith('*'):
            surface_values = line.split(",")  # Split the line by comma
            surface_el = surface_values[0].strip()
            surface_side = surface_values[1].strip().lower()

            # Check if surface_el is a numerical ID or a text string
            if surface_el.isdigit():
                surface_el = int(surface_el)
                surface_el_byname = None

            else:
                surface_el_byname = surface_el
                surface_el = None
                if not surface_el_byname:
                    surface_el_byname = current_surface_name
                    allsurf = True

            if surface_el and not surf_already_processed:
                nset_name = f"{current_surface_name}___nodes"
                nset_counter += 1
                nsets[nset_name] = {'id': nset_counter} # Store the name/ID relationship
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"#Node Group generated from SURF SEGS, {nset_name}")
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"/GRNOD/SURF/{nset_counter}\n{nset_name}")
                surface_lines.append(f"{surf_id:>10}")

                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"#SURF SEGS for surface {surface_name}")
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"/SURF/SEG/{surf_id}\n{surface_name}")
                surf_already_processed = True

            if surface_el_byname and not surf_already_processed and not allsurf:
                nset_name = f"{current_surface_name}___nodes"
                nset_counter += 1
                nsets[nset_name] = {'id': nset_counter} # Store the name/ID relationship
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"#Node Group generated from SURF SEGS, {nset_name}")
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"/GRNOD/SURF/{nset_counter}\n{nset_name}")
                surface_lines.append(f"{surf_id:>10}")

                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"#SURF SEGS for surface {surface_name}")
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"/SURF/SEG/{surf_id}\n{surface_name}")
                surf_already_processed = True
            surf_holder = []

            if surface_el is not None:
                if surface_el in segment_dictionary:
                    nodes = segment_dictionary[surface_el].get(surface_side, [])
                    segment_nodes = ''.join([f"{node:>10}" for node in nodes])
                    surf_holder.append(f"          {segment_nodes}")

            if surface_el_byname is not None and allsurf is False:
                for elset_name, surface_els in elset_dicts.items():
                    if elset_name == surface_el_byname:
                        try:
                            surface_els = [int(surface_els) for surface_els in surface_els]
                        except ValueError:
                            print(f"Warning: Unable to convert value '{surface_els}' to numeric surf set. It will be skipped.")

                        for surface_el in surface_els:
                            if surface_side:
                                nodes = segment_dictionary[surface_el].get(surface_side, [])
                                segment_nodes = ''.join([f"{node:>10}" for node in nodes])
                                surf_holder.append(f"          {segment_nodes}")
                            else:
                            # Iterate over all possible surface sides and create a separate line for each side
                                surface_sides = ['s1', 's2', 's3', 's4', 's5', 's6', 'spos', 'sneg']
                                for surf_iter in surface_sides:
                                    nodes = segment_dictionary[surface_el].get(surf_iter, [])
                                    if nodes:  # Check if nodes exist (i.e., not an empty list)
                                        segment_nodes = ''.join([f"{node:>10}" for node in nodes])
                                        surf_holder.append(f"          {segment_nodes}")


            if surface_el_byname is not None and allsurf is True:
                for property_name, property_data in property_names.items():
                    # Extract the property_id from the sub-dictionary and convert it to an integer
                    property_id = int(property_data['prop_id'])
                    # Append the integer 'property_id' to the list
                    prop_id_list.append(property_id)

                surf_id += 1
                props_per_line = []

                for property_id in prop_id_list:
                    props_per_line.append(f"{property_id:10d}")

                # Check if we have collected 10 elements
                    if len(props_per_line) == 10:
                        prop_lines.append("".join(props_per_line))
                        props_per_line = []

                # If there are remaining elements, add them to the last line
                if props_per_line:
                    prop_lines.append("".join(props_per_line))

                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"#SURF PART EXT for all parts from .inp surf:\n#{current_surface_name}")
                surface_lines.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                surface_lines.append(f"/SURF/PART/EXT/{surf_id}\n{current_surface_name}")
                surface_lines.extend(prop_lines)
                allsurf = False

            surface_lines.extend(surf_holder)
            surface_side = None
            surface_el = None
            surface_el_byname = None
            continue

        if current_surface_name and line.startswith('*'):
            remaining_lines.append(line)
            current_surface_name = None
            surf_already_processed = False

        else:
            remaining_lines.append(line)  # Collect the remaining lines

    return surface_lines, surf_id, surf_name_to_id, nset_counter, nsets, elset_dicts, input_lines


#########################################################################################################################
# Function to parse surface_interaction data for friction                                                               #
#########################################################################################################################
def parse_surface_interaction_data(input_lines):
    friction_dict = {} # Initialize friction dictionary
    friction_name = None
    friction_line = False

    for line in input_lines:
        fric_pattern = r'^\s*\*SURFACE INTERACTION\s*,\s*NAME\s*=' # Regular expression to find '*SURFACE INTERACTION'
        matchfric = re.search(fric_pattern, line, re.IGNORECASE)

        if matchfric:
            # Extract friction name from the current line
            friction_name_match = re.search(r'\bNAME\s*=\s*([^,]+)', line, re.IGNORECASE)
            friction_name = friction_name_match.group(1).strip()

        elif friction_name and (line.lower().strip().startswith('*friction')):
            friction_line = True
            continue

        elif friction_name and friction_line is True and not line.startswith('*'):
            friction_data = line.split(",")  # Split the line by comma
            friction_value = friction_data[0].strip().rstrip(",")
            friction_dict[friction_name] = friction_value
            friction_line = False

        elif friction_name and friction_line is True and line.startswith('*'):
            friction_name = None

    return friction_dict


#################################################################################################################################
# Function to convert *CONTACT data to Type24: deals with all exterior option, and contact pairs                                #
#################################################################################################################################
def convert_contacts(input_lines, property_names, surf_id, friction_dict, surf_name_to_id):
    contacts = []
    friction_ref = []
    contact_name = None
    interaction_name = None
    prop_id_list = []  # Initialize an empty list
    prop_lines = []
    ppmcontact = False
    contactpair = False
    inter_id = 0  # initialize interface id counter

    i = 0 # Initialize an index for iterating through input_lines

    #this section checks for contact attributes and stores them as variables
    while i < len(input_lines):
        line = input_lines[i].strip()
        conpair_pattern = r'^\s*\*CONTACT PAIR\s*(,.*)?$' # Regular expression to find '*CONTACT' contact entry section
        contype_pattern = r'^\s*\*CONTACT\s*(,.*)?$' # Regular expression to find '*CONTACT' contact entry section
        ppmtype_pattern = r'^\s*\*Surface interaction\s*,\s*Name\s*=\s*RADIOSS_GENERAL\s*(,.*)?$' # Regular expression to find special ppm input for general contact entry section
        matchconpair = re.search(conpair_pattern, line, re.IGNORECASE)
        matchcont = re.search(contype_pattern, line, re.IGNORECASE)
        matchppm = re.search(ppmtype_pattern, line, re.IGNORECASE)

        if matchcont or matchppm:
            if matchppm:
                ppmcontact = True
            inter_id += 1
            contact_name = f"General Contact ID {inter_id}"
            contact_properties_exist = False
            i += 1

        elif matchconpair:
            interactionmatch = re.search(r'INTERACTION\s*=\s*([^\s,]+)', line, re.IGNORECASE)

            if interactionmatch:
                interaction_name = interactionmatch.group(1)
                contactpair = True
                i += 1

        elif contactpair:
            contact_pair_groups = line.split(",")  # Split the line by comma
            secondary_surf = contact_pair_groups[0].strip()
            main_surf = contact_pair_groups[1].strip()
            secondary_surf_id = surf_name_to_id.get(secondary_surf, 0) #look up the surf counter for the referenced surface
            main_surf_id = surf_name_to_id.get(main_surf, 0) #look up the surf counter for the referenced surface
            if secondary_surf_id != 0 and main_surf_id != 0:
                inter_id += 1 # Increment the inter_id

                contacts.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                contacts.append(f"#Contact from Contact Pair: ID {inter_id} : Interaction Name: {interaction_name}")
                contacts.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                contacts.append(f"/INTER/TYPE24/{inter_id}\n{interaction_name}")
                contacts.append("# Surf_ID1  Surf_ID2      Istf                       Irem_i2                Idel")
                contacts.append(f"{main_surf_id:>10}{secondary_surf_id:>10}         4                             0                   0")
                contacts.append("# grnd_IDS                         Iedge          Edge_angle           Gap_max_s           Gap_max_m")
                contacts.append("         0                             0                   0                   0                   0")
                contacts.append("#              Stmin               Stmax     Igap0     Ipen0            Ipen_max")
                contacts.append("                   0                   0         0         0                   0")
                contacts.append("#              Stfac                Fric                                  Tstart               Tstop")
                contactpair = False

        # Check for the line indicating contact inclusions
        elif ppmcontact or (contact_name and re.search(r'^\*CONTACT\s+INCLUSIONS\s*,\s*ALL\s+EXTERIOR', line, re.IGNORECASE)):
            for property_name, property_data in property_names.items():
                # Extract the property_id from the sub-dictionary and convert it to an integer
                property_id = int(property_data['prop_id'])
                # Append the integer 'property_id' to the list (excluding springs and dummy property for masses)
                if not property_data['nint'] == '777' and not property_data['nint'] == '555':
                    prop_id_list.append(property_id)

            surf_id += 1
            props_per_line = []

            for property_id in prop_id_list:
                props_per_line.append(f"{property_id:10d}")

            # Check if we have collected 10 elements
                if len(props_per_line) == 10:
                    prop_lines.append("".join(props_per_line))
                    props_per_line = []

            # If there are remaining elements, add them to the last line
            if props_per_line:
                prop_lines.append("".join(props_per_line))

            contact_name = f"General Contact ID {inter_id}"
            contacts.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            contacts.append("#SURF PART EXT for all parts")
            contacts.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            contacts.append(f"/SURF/PART/EXT/{surf_id}\n{contact_name}")
            contacts.extend(prop_lines)
            contacts.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            contacts.append(f"#General Self Contact: ID {inter_id}")
            contacts.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            contacts.append(f"/INTER/TYPE24/{inter_id}\n{contact_name}")
            contacts.append("# Surf_ID1  Surf_ID2      Istf                       Irem_i2                Idel")
            contacts.append(f"{surf_id:>10}         0         4                             0                   0")
            contacts.append("# grnd_IDS                         Iedge          Edge_angle           Gap_max_s           Gap_max_m")
            contacts.append("         0                             0                   0                   0                   0")
            contacts.append("#              Stmin               Stmax     Igap0     Ipen0            Ipen_max")
            contacts.append("                   0                   0         0         0                   0")
            contacts.append("#              Stfac                Fric                                  Tstart               Tstop")
            if ppmcontact:
                contact_properties_exist = True
                friction_ref = "RADIOSS_GENERAL"
                friction_value = float(friction_dict.get(friction_ref.strip(), 0))
                contacts.append(f"                   0          {friction_value:>10.8g}                                       0                   0")
                contacts.append("#      IBC                        Inacti               ViscS                             ")
                contacts.append("       000                             5                   0")
                contacts.append("#    Ifric    Ifiltr               Xfreq             sens_ID                                 fric_ID")
                contacts.append("         0         0                   0                   0                                       0")
                contact_name = None
                ppmcontact = False
            i += 1

        elif contact_name and line.lower().startswith('*contact property assignment'):
            contact_properties_exist = True
            i += 1 # move to next line

            property_line = input_lines[i].strip()
            friction_ref = property_line.split(',')[2]
            friction_value = float(friction_dict.get(friction_ref.strip(), 0))
            contacts.append(f"                   0          {friction_value:>10.8g}                                       0                   0")
            contacts.append("#      IBC                        Inacti               ViscS                             ")
            contacts.append("       000                             5                   0")
            contacts.append("#    Ifric    Ifiltr               Xfreq             sens_ID                                 fric_ID")
            contacts.append("         0         0                   0                   0                                       0")
            contact_name = None

        elif interaction_name:
            contact_properties_exist = True
            friction_ref = interaction_name
            friction_value = float(friction_dict.get(friction_ref.strip(), 0))
            contacts.append(f"                   0          {friction_value:>10.8g}                                       0                   0")
            contacts.append("#      IBC                        Inacti               ViscS                             ")
            contacts.append("       000                             5                   0")
            contacts.append("#    Ifric    Ifiltr               Xfreq             sens_ID                                 fric_ID")
            contacts.append("         0         0                   0                   0                                       0")
            interaction_name = None

        else:
            i += 1 # move to the next line if no match

    if contact_name and contact_properties_exist is False:

        contacts.append("                   0                 0.0                                       0                   0")
        contacts.append("#      IBC                        Inacti               ViscS                             ")
        contacts.append("       000                             5                   0")
        contacts.append("#    Ifric    Ifiltr               Xfreq             sens_ID                                 fric_ID")
        contacts.append("         0         0                   0                   0                                       0")
        contact_name = None

    return contacts, surf_id, inter_id


####################################################################################################
# Function to convert *TIE to Type2                                                                #
####################################################################################################
def convert_ties(input_lines, surf_name_to_id, nsets, inter_id):
    tied_contacts = []
    tied_contact_name = None

    for line in input_lines:
        # Updated regex pattern to match names with special characters
        tctype_pattern = r'^\s*\*TIE\s*,\s*NAME\s*='  # Keep the same for detecting TIE
        matchtie = re.search(tctype_pattern, line, re.IGNORECASE)
        tc_type_match = re.search(r'TYPE\s*=\s*([^,]+)', line, re.IGNORECASE)

        if matchtie:
            # Extract tied contact name from the current line
            # Regex to capture names with special characters
            tc_name_match = re.search(r'NAME\s*=\s*([^,]+)', line, re.IGNORECASE)
            tc_postol_match = re.search(r'POSITION TOLERANCE\s*=\s*([^,]+)', line, re.IGNORECASE)
            if tc_name_match:
                tied_contact_name = tc_name_match.group(1).strip()  # Extracted name
            else:
                tied_contact_name = None  # Handle the case if NAME is not found

            tc_postol_value = 0
            if tc_postol_match:
                tc_postol_value = float(tc_postol_match.group(1).strip())

            tc_type = "node to surface"
            if tc_type_match:
                tc_type = tc_type_match.group(1).strip().lower()

        elif tied_contact_name and not line.startswith('*'):
            contact_groups = line.split(",")  # Split the line by comma
            surface_for_nodes = contact_groups[0].strip()
            surface_to_tie_to = contact_groups[1].strip()
            nodes_to_tie = f"{surface_for_nodes}___nodes"
            nset_data = nsets.get(nodes_to_tie)
            #look up the nset counter for the referenced nset (based on the surface)
            tie_nset_id = nset_data['id'] if nset_data else 0
            if tie_nset_id == 0:
                nodes_to_tie = f"{surface_for_nodes}___originalnodeset"
                nset_data = nsets.get(nodes_to_tie)
                #look up the nset counter for the referenced nset (based on original nodeset)
                tie_nset_id = nset_data['id'] if nset_data else 0
            #look up the surf counter for the referenced surface
            tie_surf_id = surf_name_to_id.get(surface_to_tie_to, 0)
            tie_holder = []
            if tie_surf_id != 0 and tie_nset_id != 0:
                inter_id += 1 # Increment the inter_id
                #create the first tie for each surface pair (nodes for surf 1, surfs for surf 2)
                tie_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                tie_holder.append(f"#Tied interface definition: {tied_contact_name}")
                tie_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                tie_holder.append(f"/INTER/TYPE2/{inter_id}\n{tied_contact_name}")
                tie_holder.append("#  Grnd_ID   Surf_id    Ignore  Spotflag     Level   Isearch     Idel2                       dSearch")
                tie_holder.append(f"{tie_nset_id:>10}{tie_surf_id:>10}         3        {spotflag_default:>2}         0         0         2                    {tc_postol_value:>10.8g}")
                tie_holder.append("#              Stfac                Visc                          Istf")
                tie_holder.append("                   0                   0                             0")

            if tc_type == "surface to surface":
                #create a symmetric tie for each surf pair if type is surf - surf (surfs for surf 1, nodes for surf 2)
                symm_surface_for_nodes = contact_groups[1].strip()
                symm_surface_to_tie_to = contact_groups[0].strip()
                symm_nodes_to_tie = f"{symm_surface_for_nodes}___nodes"
                nset_data = nsets.get(symm_nodes_to_tie)
                symm_tie_nset_id = nset_data['id'] if nset_data else 0 #look up the nset counter for the referenced nset (based on the surface)
                symm_tie_surf_id = surf_name_to_id.get(symm_surface_to_tie_to, 0) #look up the surf counter for the referenced surface
                if symm_tie_surf_id != 0 and symm_tie_nset_id != 0:
                    inter_id += 1 # Increment the inter_id
                    tie_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                    tie_holder.append(f"#Tied interface definition (symm for s2s): {tied_contact_name}")
                    tie_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                    tie_holder.append(f"/INTER/TYPE2/{inter_id}\n{tied_contact_name}_symm")
                    tie_holder.append("#  Grnd_ID   Surf_id    Ignore  Spotflag     Level   Isearch     Idel2                       dSearch")
                    tie_holder.append(f"{symm_tie_nset_id:>10}{symm_tie_surf_id:>10}         3        27         0         0         2                    {tc_postol_value:>10.8g}")
                    tie_holder.append("#              Stfac                Visc                          Istf")
                    tie_holder.append("                   0                   0                             0")

            tied_contacts.extend(tie_holder)

        elif tied_contact_name and line.startswith('*'):
            tied_contact_name = None

    return tied_contacts, inter_id


####################################################################################################
# Function to convert amplitudes to functions                                                      #
####################################################################################################
def read_amplitudes(input_lines, fct_id):
    functs_dict = {}
    inside_amplitude_section = False
    amplitude_name = None
    data_blocks = []
    current_data_block = []

    # Loop over all input lines
    for line in input_lines:
        line = line.strip()
        # Detect *AMPLITUDE section
        if line.lower().startswith('*amplitude'):
            inside_amplitude_section = True
            if current_data_block:
                data_blocks.append(current_data_block)
            current_data_block = [line]

        elif inside_amplitude_section and not line.startswith('*'):
            current_data_block.append(line)

        elif line.startswith('*'):
            inside_amplitude_section = False

    if current_data_block:
        data_blocks.append(current_data_block)

    for block in data_blocks:
        header = block[0]
        # Extract the name of the amplitude using regex
        amplitude_name_match = re.search(r"name\s*=\s*([\w\-\.]+)", header, re.IGNORECASE)
        amplitude_name = amplitude_name_match.group(1)
        fct_id += 1

        data = " ".join(block[1:])  # Combine all lines of data

        data = re.sub(r",\s*$", "", data)  # Remove trailing comma
        values = [float(v) for v in re.split(r"[,\s]+", data) if v]  # Split and convert to float

        if len(values) % 2 != 0:
            print("Warning: Uneven data in block, ignoring the last value.")
            values = values[:-1]

        functs_dict[amplitude_name] = {
            'id': fct_id,
            'data': list(zip(values[::2], values[1::2]))
            }

    # Always create a default amplitude at the end for use where one isn't called
    fct_id += 1  # Increment fct_id for the default amplitude
    default_amplitude_name = 'DEFAULT CONSTANT OVER STEP'
    functs_dict[default_amplitude_name] = {
        'id': fct_id,
        'data': [(0.0, 1.0), (1.0, 1.0)]  # Default data as (abscissa, ordinate) pairs
    }

    return functs_dict, fct_id


####################################################################################################
# Function to convert BOUNDARY and CLOAD data, BCS, CLOAD and IMPDISPS only for now                #
####################################################################################################
def convert_boundary(input_lines, nset_counter, nsets, functs_dict, fct_id):
    boundary_data = {}
    impd_data = {}
    impv_data = {}
    cload_data = {}

    section = None
    amplitude_name = None
    opsection = False
    imptype = 'DISPLACEMENT'

    op_pattern = r'op\s*=\s*new'
    amplitude_pattern = r'amplitude\s*=\s*([^ ]+)'
    type_pattern = r'type\s*=\s*([^ ]+)'

    # Define boundary condition mappings for text entry boundary conditions
    boundary_condition_mappings = {
        'ENCASTRE': ['1', '2', '3', '4', '5', '6'],
        'PINNED': ['1', '2', '3', '0', '0', '0'],
        'XSYMM': ['1', '0', '0', '0', '5', '6'],
        'YSYMM': ['0', '2', '0', '4', '0', '6'],
        'ZSYMM': ['0', '0', '3', '4', '5', '0']
    }

    for line in input_lines:
        line = line.strip()

        if line.lower().startswith("*boundary") and re.search(r'type\s*=', line.lower()):
            section = "*boundary"
            type_match = re.search(type_pattern, line, re.IGNORECASE)
            imptype = type_match.group(1).strip()  # Get the value after '=' and strip any spaces
            amplitude_match = re.search(amplitude_pattern, line, re.IGNORECASE)
            if amplitude_match:
                amplitude_name = amplitude_match.group(1).strip()  # Get the value after '=' and strip any spaces
            else:
                amplitude_name = 'DEFAULT CONSTANT OVER STEP'
            opsection = False

            # Check for 'op=new' to clear existing data
            if re.search(op_pattern, line.lower()):
                # Clear existing data for this section
                opsection = True
            continue

        # Check for boundary or cload section
        if line.lower().startswith("*boundary") and 'amplitude' not in line.lower():
            section = "*boundary"
            imptype = 'DISPLACEMENT'
            amplitude_name = 'DEFAULT CONSTANT OVER STEP'  # Reset amplitude name for BCS boundaries
            opsection = False

            # Check for 'op=new' to clear existing data
            if re.search(op_pattern, line.lower()):
                # Clear existing data for this section
                opsection = True
            continue

        if line.lower().startswith("*boundary") and re.search(r'amplitude\s*=', line.lower()):
            section = "*boundary"
            imptype = 'DISPLACEMENT'
            amplitude_match = re.search(amplitude_pattern, line, re.IGNORECASE)
            amplitude_name = amplitude_match.group(1).strip()  # Get the value after '=' and strip any spaces
            opsection = False

            # Check for 'op=new' to clear existing data
            if re.search(op_pattern, line.lower()):
                # Clear existing data for this section
                opsection = True
            continue

        if line.lower().startswith("*cload") and re.search(r'amplitude\s*=', line.lower()):
            section = "*cload"
            amplitude_match = re.search(amplitude_pattern, line, re.IGNORECASE)
            if amplitude_match:
                amplitude_name = amplitude_match.group(1).strip()  # Get the value after '=' and strip any spaces
            opsection = False

            # Check for 'op=new' to clear existing data
            if re.search(op_pattern, line.lower()):
                # Clear existing data for this section
                opsection = True
            continue

        if line.lower().startswith("*cload") and not re.search(r'amplitude\s*=', line.lower()):
            section = "*cload"
            amplitude_name = 'DEFAULT CONSTANT OVER STEP'  # set cload as constant if no amplitude defined
            opsection = False

            # Check for 'op=new' to clear existing data
            if re.search(op_pattern, line.lower()):
                # Clear existing data for this section
                opsection = True
            continue

        if line.startswith("*"):
            section = None

        elif section == "*boundary" and not line.startswith("*"):
            fields = line.split(',')
            fields = [f.strip() for f in fields]  # Clean up any extra whitespace

            if imptype == 'DISPLACEMENT':

                if len(fields) >= 2 and not len(fields) >= 4:
                    boundary_name = fields[0]  # First field
                    boundary_dir1 = fields[1]  # Second field

                    # Check if boundary_dir1 is a predefined string condition
                    if boundary_dir1 in boundary_condition_mappings:
                        boundary_dir = boundary_condition_mappings[boundary_dir1]
                    else:
                    # Otherwise, parse as integer ranges for boundary_dir1 and boundary_dir2
                        boundary_dir1 = int(boundary_dir1)
                        # Set the 3rd field to the 2nd field if it's empty
                        boundary_dir2 = int(fields[2]) if len(fields) >= 3 and fields[2] != '' else boundary_dir1
                        # Generate the list of directions for BCS (range between dir1 and dir2)
                        boundary_dir = list(map(str, range(boundary_dir1, boundary_dir2 + 1)))

                    # Store the BCS data
                    if opsection is True:
                        opsection = False
                        if boundary_name in boundary_data:
                            del boundary_data[boundary_name]
                        if boundary_name in impd_data:
                            del impd_data[boundary_name]
                        if boundary_name in impv_data:
                            del impv_data[boundary_name]

                    if boundary_name not in boundary_data:
                        boundary_data[boundary_name] = boundary_dir
                    else:
                        boundary_data[boundary_name].extend(boundary_dir)

                if len(fields) >= 4:
                    impd_name = fields[0]  # First field
                    impd_dir = "X" if fields[1] == "1" else "Y" if fields[1] == "2" else "Z" if fields[1] == "3" else \
                               "XX" if fields[1] == "4" else "YY" if fields[1] == "5" else "ZZ" if fields[1] == "6" else None
                    impd_val = fields[3].strip() if fields[3] != '' else "0.0"  # Set 4th field to 0.0 if empty

                    try:
                        impd_val_float = float(impd_val)  # Convert to float
                    except ValueError:
                        raise ValueError(f"Invalid value for impd_val: {impd_val}")

                    # Check if impd_val is equivalent to 0.0
                    if impd_val_float == 0.0:
                        # Handle as BCS instead of IMPDISP
                        if len(fields) >= 2:
                            boundary_name = fields[0]  # First field
                            boundary_dir1 = int(fields[1])  # Second field

                            # Set the 3rd field to the 2nd field if it's empty
                            boundary_dir2 = int(fields[2]) if len(fields) >= 3 and fields[2] != '' else boundary_dir1

                            # Generate the list of directions for BCS (range between dir1 and dir2)
                            boundary_dir = list(map(str, range(boundary_dir1, boundary_dir2 + 1)))

                            if opsection is True:
                                opsection = False
                                if boundary_name in boundary_data:
                                    del boundary_data[boundary_name]
                                if boundary_name in impd_data:
                                    del impd_data[boundary_name]
                                if boundary_name in impv_data:
                                    del impv_data[boundary_name]

                            if boundary_name not in boundary_data:
                                boundary_data[boundary_name] = boundary_dir
                            else:
                                boundary_data[boundary_name].extend(boundary_dir)

                    else:
                        # Continue treating as IMPDISP
                        impd_val = float(impd_val)  # Convert value to float

                        if opsection is True:
                            opsection = False
                            if impd_name in boundary_data:
                                del boundary_data[impd_name]
                            if impd_name in impd_data:
                                del impd_data[impd_name]
                            if impd_name in impv_data:
                                del impv_data[impd_name]

                        # If impd_name is already in the dictionary, append to its list
                        if impd_name not in impd_data:
                            impd_data[impd_name] = []

                        # Add this entry to the list
                        impd_data[impd_name].append((impd_dir, impd_val, amplitude_name))

            elif imptype == 'VELOCITY':

                if len(fields) >= 2 and not len(fields) >= 4:
                    boundary_name = fields[0]  # First field
                    boundary_dir1 = fields[1]  # Second field

                    # Check if boundary_dir1 is a predefined string condition
                    if boundary_dir1 in boundary_condition_mappings:
                        boundary_dir = boundary_condition_mappings[boundary_dir1]
                    else:
                    # Otherwise, parse as integer ranges for boundary_dir1 and boundary_dir2
                        boundary_dir1 = int(boundary_dir1)
                        # Set the 3rd field to the 2nd field if it's empty
                        boundary_dir2 = (
                            int(fields[2])
                            if len(fields) >= 3
                            and fields[2] != ''
                            else boundary_dir1
                            )
                        # Generate the list of directions for BCS (range between dir1 and dir2)
                        boundary_dir = list(map(str, range(boundary_dir1, boundary_dir2 + 1)))

                    # Store the BCS data
                    if opsection is True:
                        opsection = False
                        if boundary_name in boundary_data:
                            del boundary_data[boundary_name]
                        if boundary_name in impd_data:
                            del impd_data[boundary_name]
                        if boundary_name in impv_data:
                            del impv_data[boundary_name]

                    if boundary_name not in boundary_data:
                        boundary_data[boundary_name] = boundary_dir
                    else:
                        boundary_data[boundary_name].extend(boundary_dir)

                if len(fields) >= 4:
                    impv_name = fields[0]  # First field
                    impv_dir = "X" if fields[1] == "1" else "Y" if fields[1] == "2" else "Z" if fields[1] == "3" else \
                               "XX" if fields[1] == "4" else "YY" if fields[1] == "5" else "ZZ" if fields[1] == "6" else None
                    impv_val = fields[3].strip() if fields[3] != '' else "0.0"  # Set 4th field to 0.0 if empty

                    try:
                        impv_val_float = float(impv_val)  # Convert to float
                    except ValueError:
                        raise ValueError(f"Invalid value for impv_val: {impv_val}")

                    # Check if impv_val is equivalent to 0.0
                    if impv_val_float == 0.0:
                        # Handle as BCS instead of IMPDISP
                        if len(fields) >= 2:
                            boundary_name = fields[0]  # First field
                            boundary_dir1 = int(fields[1])  # Second field

                            # Set the 3rd field to the 2nd field if it's empty
                            boundary_dir2 = int(fields[2]) if len(fields) >= 3 and fields[2] != '' else boundary_dir1

                            # Generate the list of directions for BCS (range between dir1 and dir2)
                            boundary_dir = list(map(str, range(boundary_dir1, boundary_dir2 + 1)))

                            if opsection is True:
                                opsection = False
                                if boundary_name in boundary_data:
                                    del boundary_data[boundary_name]
                                if boundary_name in impd_data:
                                    del impd_data[boundary_name]
                                if boundary_name in impv_data:
                                    del impv_data[boundary_name]

                            if boundary_name not in boundary_data:
                                boundary_data[boundary_name] = boundary_dir
                            else:
                                boundary_data[boundary_name].extend(boundary_dir)

                    else:
                        # Continue treating as IMPVEL
                        impv_val = float(impv_val)  # Convert value to float

                        if opsection is True:
                            opsection = False
                            if impv_name in boundary_data:
                                del boundary_data[impv_name]
                            if impv_name in impd_data:
                                del impd_data[impv_name]
                            if impv_name in impv_data:
                                del impv_data[impv_name]

                        # If impd_name is already in the dictionary, append to its list
                        if impv_name not in impv_data:
                            impv_data[impv_name] = []

                        # Add this entry to the list
                        impv_data[impv_name].append((impv_dir, impv_val, amplitude_name))

        elif section == "*cload" and not line.startswith("*"):
            fields = line.split(',')
            fields = [f.strip() for f in fields]  # Clean up any extra whitespace

            if len(fields) >= 3:
                cload_name = fields[0]  # First field
                cload_dir = "X" if fields[1] == "1" else "Y" if fields[1] == "2" else "Z" if fields[1] == "3" else \
                           "XX" if fields[1] == "4" else "YY" if fields[1] == "5" else "ZZ" if fields[1] == "6" else None
                cload_val = fields[2].strip() if fields[2] != '' else "0.0"  # Set 3rd field to 0.0 if empty

                try:
                    cload_val_float = float(cload_val)  # Convert to float
                except ValueError:
                    raise ValueError(f"Invalid value for cload_val: {cload_val}")

                # create cload data
                cload_val = float(cload_val)  # Convert value to float

                if opsection is True:
                    opsection = False
                    if cload_name in cload_data:
                        del cload_data[cload_name]

                # If cload_name is already in the dictionary, append to its list
                if cload_name not in cload_data:
                    cload_data[cload_name] = []

                # Add this entry to the list
                cload_data[cload_name].append((cload_dir, cload_val, amplitude_name))

    boundary_blocks = []  # Placeholder for output blocks

    # BCS Block
    for boundary_name, boundary_dirs in boundary_data.items():
        if boundary_name.isdigit():
            nset_counter += 1
            ref_nset_counter = nset_counter
            bcs_grnod = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            bcs_grnod += f"/GRNOD/NODE/{ref_nset_counter}\n"
            bcs_grnod += f"node group containing only node {boundary_name} for BCS\n"
            bcs_grnod += "#   NODEID\n"
            bcs_grnod += f"{boundary_name:>10}"
        else:
            nset_data = nsets.get(boundary_name)
            ref_nset_counter = nset_data['id'] if nset_data else 0
            bcs_grnod = None

        combined_bcs_dir = ''.join(['1' if boundary_dir in boundary_dirs else '0' for boundary_dir in ['1', '2', '3']])
        combined_bcsr_dir = ''.join(['1' if boundary_dir in boundary_dirs else '0' for boundary_dir in ['4', '5', '6']])
        bcs_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
        bcs_block += f"/BCS/{ref_nset_counter}\n{boundary_name}\n"
        bcs_block += "#  Tra rot   skew_ID  grnod_ID\n"
        bcs_block += f"   {combined_bcs_dir} {combined_bcsr_dir}         0{ref_nset_counter:>10}"
        boundary_blocks.append(bcs_block)

        if bcs_grnod is not None:
            boundary_blocks.append(bcs_grnod)

    # IMPDISP Block
    for impd_name, impd_entries in impd_data.items():
        impd_first_entry = True  # Track if it's the first entry for this impd_name

        if impd_name.isdigit():
            nset_counter += 1
            ref_nset_counter = nset_counter
            grnod_nset_counter = ref_nset_counter
            impd_grnod = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            impd_grnod += f"/GRNOD/NODE/{ref_nset_counter}\n"
            impd_grnod += f"node group containing only node {impd_name} for IMPDISP\n"
            impd_grnod += "#   NODEID\n"
            impd_grnod += f"{impd_name:>10}"

        else:
            nset_data = nsets.get(impd_name)
            ref_nset_counter = nset_data['id'] if nset_data else 0
            grnod_nset_counter = ref_nset_counter
            impd_grnod = None

        # Create a separate block for each entry under the same impd_name
        for impd_dir, impd_val, amplitude_name in impd_entries:
            # Increment nset_counter for each subsequent entry
            if not impd_first_entry:
                grnod_nset_counter = ref_nset_counter
                nset_counter += 1
                ref_nset_counter = nset_counter
                impd_grnod = None

            # Lookup funct_id based on amplitude_name
            if amplitude_name and amplitude_name in functs_dict:
                funct_id = functs_dict[amplitude_name].get('id', 1)  # Default to 1 if no 'id' is found
            else:
                funct_id = 1  # Default funct_id if no amplitude_name or no match found

            impdisp_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            impdisp_block += f"/IMPDISP/{ref_nset_counter}\n{impd_name}\n"
            impdisp_block += f"# References Amplitude: {amplitude_name}\n"  # Add amplitude name as a comment
            impdisp_block += "#   Ifunct       DIR     Iskew   Isensor   Gnod_id               Icoor\n"
            impdisp_block += f"{funct_id:>10}{impd_dir:>10}         0         0{grnod_nset_counter:>10}                   0\n"
            impdisp_block += "#            Scale_x             Scale_y              Tstart               Tstop\n"
            impdisp_block += f"                   1{impd_val:>20.15g}                   0                1E31"
            boundary_blocks.append(impdisp_block)

            # Append the GRNOD block if it's a digit
            if impd_grnod is not None:
                boundary_blocks.append(impd_grnod)

            # Set first_entry to False after handling the first entry
            impd_first_entry = False

    # IMPVEL Block
    for impv_name, impv_entries in impv_data.items():
        impv_first_entry = True  # Track if it's the first entry for this impd_name

        if impv_name.isdigit():
            nset_counter += 1
            ref_nset_counter = nset_counter
            grnod_nset_counter = ref_nset_counter
            impd_grnod = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            impd_grnod += f"/GRNOD/NODE/{ref_nset_counter}\n"
            impd_grnod += f"node group containing only node {impd_name} for IMPVEL\n"
            impd_grnod += "#   NODEID\n"
            impd_grnod += f"{impv_name:>10}"

        else:
            nset_data = nsets.get(impv_name)
            ref_nset_counter = nset_data['id'] if nset_data else 0
            grnod_nset_counter = ref_nset_counter
            impv_grnod = None

        # Create a separate block for each entry under the same impd_name
        for impv_dir, impv_val, amplitude_name in impv_entries:
            # Increment nset_counter for each subsequent entry
            if not impv_first_entry:
                grnod_nset_counter = ref_nset_counter
                nset_counter += 1
                ref_nset_counter = nset_counter
                impv_grnod = None

            # Lookup funct_id based on amplitude_name
            if amplitude_name and amplitude_name in functs_dict:
                funct_id = functs_dict[amplitude_name].get('id', 1)  # Default to 1 if no 'id' is found
            else:
                funct_id = 1  # Default funct_id if no amplitude_name or no match found

            impvel_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            impvel_block += f"/IMPVEL/{ref_nset_counter}\n{impv_name}\n"
            impvel_block += f"# References Amplitude: {amplitude_name}\n"  # Add amplitude name as a comment
            impvel_block += "#   Ifunct       DIR     Iskew   Isensor   Gnod_id     Frame     Icoor\n"
            impvel_block += f"{funct_id:>10}{impv_dir:>10}         0         0{grnod_nset_counter:>10}         0         0\n"
            impvel_block += "#            Scale_x             Scale_y              Tstart               Tstop\n"
            impvel_block += f"                   1{impv_val:>20.15g}                   0                1E31"
            boundary_blocks.append(impvel_block)

            # Append the GRNOD block if it's a digit
            if impv_grnod is not None:
                boundary_blocks.append(impv_grnod)

            # Set first_entry to False after handling the first entry
            impv_first_entry = False

    # CLOAD Block
    for cload_name, cload_entries in cload_data.items():
        cload_first_entry = True  # Track if it's the first entry for this cload_name

        if cload_name.isdigit():
            for entry in cload_entries:
                nset_counter += 1
                ref_nset_counter = nset_counter
                grnod_nset_counter = ref_nset_counter

                cload_grnod = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
                cload_grnod += f"/GRNOD/NODE/{ref_nset_counter}\n"
                cload_grnod += f"node group containing only node {cload_name} for CLOAD\n"
                cload_grnod += "#   NODEID\n"
                cload_grnod += f"{cload_name:>10}"

        else:
            nset_data = nsets.get(cload_name)
            ref_nset_counter = nset_data['id'] if nset_data else 0
            grnod_nset_counter = ref_nset_counter
            cload_grnod = None

        # Create a separate block for each entry under the same impd_name
        for cload_dir, cload_val, amplitude_name in cload_entries:
            # Increment nset_counter for each subsequent entry
            if not cload_first_entry:
                grnod_nset_counter = ref_nset_counter
                nset_counter += 1
                ref_nset_counter = nset_counter
                cload_grnod = None

            # Lookup funct_id based on amplitude_name
            if amplitude_name and amplitude_name in functs_dict:
                funct_id = functs_dict[amplitude_name].get('id', 1)  # Default to 1 if no 'id' is found
            else:
                funct_id = 1  # Default funct_id if no amplitude_name or no match found

            cload_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            cload_block += f"/CLOAD/{ref_nset_counter}\n{cload_name}\n"
            cload_block += f"# References Amplitude: {amplitude_name}\n"  # Add amplitude name as a comment
            cload_block += "#  fct_IDT       DIR   skew ID   sens_ID   Grnd_id                      Ascale_x            Fscale_y\n"
            cload_block += f"{funct_id:>10}{cload_dir:>10}         0         0{grnod_nset_counter:>10}                             1{cload_val:>20.15g}"
            boundary_blocks.append(cload_block)

            # Append the GRNOD block if it's a digit
            if cload_grnod is not None:
                boundary_blocks.append(cload_grnod)

            # Set first_entry to False after handling the first entry
            cload_first_entry = False

    return boundary_blocks, nset_counter, fct_id


####################################################################################################
# Function to write functions, based on amplitudes                                                 #
####################################################################################################
def write_functions(functs_dict):
    function_blocks = []

    # Iterate over the dictionary and write each function
    for amplitude_name, funct_data in functs_dict.items():
        funct_id = funct_data['id']
        amplitude_data = funct_data['data']

        # Start of function block
        function_blocks.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
        function_blocks.append(f"# FUNCTION {funct_id} from *AMPLITUDE {amplitude_name}")
        function_blocks.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
        function_blocks.append(f"/FUNCT/{funct_id}")
        function_blocks.append(amplitude_name)

        # Column headers
        function_blocks.append("#                  X                   Y")

        # Write the abscissa and ordinate pairs
        for abscissa, ordinate in amplitude_data:
            function_blocks.append(f"{abscissa:>20.8f}{ordinate:>20.8f}")  # Right-justify in 20-wide fields with 8 decimals

    return function_blocks


####################################################################################################
# Function to convert Velocity Initial Conditions, works for either elset name or single node ID   #
####################################################################################################
def convert_initial(input_lines, nset_counter, nsets):
    iniv_data = {}
    section = None

    for line in input_lines:
        line = line.strip()
        if re.search(r'^\s*\*initial\s+conditions\s*,\s*type\s*=\s*velocity\s*$', line, re.IGNORECASE):
            section = "*inivel"
            continue
        if line.startswith("*"):
            section = None
        elif section == "*inivel":
            fields = line.split(',')
            iniv_name = fields[0].strip()
            iniv_dir = int(fields[1].strip())  # Convert to integer
            iniv_mag_x = 0.0
            iniv_mag_y = 0.0
            iniv_mag_z = 0.0
            # Initialize the dictionary entry for iniv_name if it doesn't exist
            if iniv_name not in iniv_data:
                iniv_data[iniv_name] = {}

            if iniv_dir == 1:
                iniv_mag_x = float(fields[2].strip()) # Convert iniv_mag to a float
                iniv_data[iniv_name]['iniv_mag_x'] = iniv_mag_x
            elif 'iniv_mag_x' not in iniv_data[iniv_name]:
                iniv_data[iniv_name]['iniv_mag_x'] = iniv_mag_x
            if iniv_dir == 2:
                iniv_mag_y = float(fields[2].strip()) # Convert iniv_mag to a float
                iniv_data[iniv_name]['iniv_mag_y'] = iniv_mag_y
            elif 'iniv_mag_y' not in iniv_data[iniv_name]:
                iniv_data[iniv_name]['iniv_mag_y'] = iniv_mag_y
            if iniv_dir == 3:
                iniv_mag_z = float(fields[2].strip()) # Convert iniv_mag to a float
                iniv_data[iniv_name]['iniv_mag_z'] = iniv_mag_z
            elif 'iniv_mag_z' not in iniv_data[iniv_name]:
                iniv_data[iniv_name]['iniv_mag_z'] = iniv_mag_z

    iniv_groups = {}
    for iniv_name, iniv_mags in iniv_data.items():
        if iniv_name.isdigit():
            # Use tuple of iniv_mags as a unique key to group by
            mag_key = (
                iniv_mags.get('iniv_mag_x'),
                iniv_mags.get('iniv_mag_y'),
                iniv_mags.get('iniv_mag_z')
            )
            if mag_key not in iniv_groups:
                iniv_groups[mag_key] = []
            iniv_groups[mag_key].append(iniv_name)
        else:
            iniv_groups[(None, None, None)] = iniv_groups.get((None, None, None), []) + [(iniv_name, iniv_mags)]

    initial_blocks = []

    for mag_key, iniv_names in iniv_groups.items():
        if mag_key == (None, None, None):  # Skip non-digit iniv_names
            for iniv_name, iniv_mags in iniv_names:
                nset_data = nsets.get(iniv_name)
                ref_nset_counter = nset_data['id'] if nset_data else 0
                iniv_mag_x = iniv_mags.get('iniv_mag_x')
                iniv_mag_y = iniv_mags.get('iniv_mag_y')
                iniv_mag_z = iniv_mags.get('iniv_mag_z')
                iniv_block = (
                    "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
                    f"/INIVEL/TRA/{ref_nset_counter}\n{iniv_name}\n"
                    "#                 Vx                  Vy                  Vz   Gnod_id   Skew_id\n"
                    f"{iniv_mag_x:>20.15g}{iniv_mag_y:>20.15g}{iniv_mag_z:>20.15g}{ref_nset_counter:>10}"
                )
                initial_blocks.append(iniv_block)
            continue

        # Digit iniv_names with same iniv_mags values
        nset_counter += 1
        ref_nset_counter = nset_counter
        iniv_grnod = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
        iniv_grnod += f"/GRNOD/NODE/{nset_counter}\n"
        iniv_grnod += "node group containing multiple nodes with same INIVEL values\n"
        iniv_grnod += "#   NODEID\n"

        # Split iniv_names into chunks of 10 for formatting
        for i in range(0, len(iniv_names), 10):
            chunk = iniv_names[i:i+10]
            iniv_grnod += "".join(f"{node:>10}" for node in chunk) + "\n"

        # Create INIVEL block
        iniv_mag_x, iniv_mag_y, iniv_mag_z = mag_key
        iniv_block = (
            "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            f"/INIVEL/TRA/{ref_nset_counter}\n"
            "Shared INIVEL for group of nodes\n"
            "#                 Vx                  Vy                  Vz   Gnod_id   Skew_id\n"
            f"{iniv_mag_x:>20.15g}{iniv_mag_y:>20.15g}{iniv_mag_z:>20.15g}{ref_nset_counter:>10}"
        )

        initial_blocks.append(iniv_grnod)
        initial_blocks.append(iniv_block)

    return initial_blocks, nset_counter


####################################################################################################
# Function to convert *DLOADS (only checking Grav type currently)                                  #
####################################################################################################
def convert_dloads(input_lines, nset_counter, nsets, property_names, functs_dict, fct_id):
    dload_data = {}

    amplitude_name = None
    already_set = False
    section = None
    skipgrav = False

    for line in input_lines:
        line = line.strip()
        if line.lower().startswith("*dload"):
            section = "*dload"
            amplitude_pattern = r'amplitude\s*=\s*([^ ]+)'
            amplitude_match = re.search(amplitude_pattern, line, re.IGNORECASE)
            if amplitude_match:
                amplitude_name = amplitude_match.group(1).strip()  # Get the value after '=' and strip any spaces
            continue
        if line.startswith("*"):
            section = None
        elif section == "*dload":
            fields = line.split(',')
            dload_name = fields[0].strip()
            dload_type = fields[1].strip()

            if dload_name:
                elset_values = []
                if dload_name.isdigit():
                    skipgrav = True
                    continue
                #check if dload name is a single part?
                if dload_name in property_names:
                    prop_ids = []
                    property_id = property_names[dload_name]['prop_id'] #this is for ref in title and to get node group (same as part number)
                    prop_ids.append(property_id)

                elif dload_name in nsets:
                    already_set = True
                    ref_nset_counter = nsets[dload_name]['id']

                else:
                    inside_elset_section = False
                    for line in input_lines:
                        elset_line_pattern = r'^\s*\*ELSET\s*,?\s*ELSET\s*=\s*{}\b'.format(re.escape(dload_name))

                        elset_line_match = re.search(elset_line_pattern, line, re.IGNORECASE)
                        if elset_line_match:
                            inside_elset_section = True
                            elset_values = []
                            prop_ids = []
                            continue

                        if inside_elset_section and line.startswith('*'):
                            inside_elset_section = False
                            continue

                        if inside_elset_section and line.strip():  # Skip empty lines
                            values = line.split(',')
                            elset_values.extend([value.strip() for value in values if value.strip()])
                            continue

                    for values in elset_values:
                        property_id = property_names[values]['prop_id']
                        prop_ids.append(property_id)

            else:
                if skipgrav:
                    continue
                prop_ids = []
                property_id = 'all'
                prop_ids.append(property_id)

            if dload_type.lower() == "grav":
                dload_mag = float(fields[2].strip()) # Convert dload_mag to a float
                dload_dir = [float(x) if x.strip() else 0.0 for x in fields[3:6]]  # Convert dload_dir to a list of floats, treating empty fields as 0.0
                dload_dirb = [0.0, 1.0, 0.0] # set Z' as global Y for now
                # Calculate the cross product of dir and dirb
                cross_product = [
                    dload_dir[1] * dload_dirb[2] - dload_dir[2] * dload_dirb[1],
                    dload_dir[2] * dload_dirb[0] - dload_dir[0] * dload_dirb[2],
                    dload_dir[0] * dload_dirb[1] - dload_dir[1] * dload_dirb[0]
                ]

                # First Check if the cross product is the zero vector for .inp Value and global Y
                if cross_product == [0, 0, 0]: # vectors are parallel
                    dload_dirb = [0.0 ,0.0, 1.0] # change to global Z if original vector was global Y

                # Calculate the radiossvalues of dir and dirb
                cross_product = [
                    dload_dir[1] * dload_dirb[2] - dload_dir[2] * dload_dirb[1],
                    dload_dir[2] * dload_dirb[0] - dload_dir[0] * dload_dirb[2],
                    dload_dir[0] * dload_dirb[1] - dload_dir[1] * dload_dirb[0]
                ]

                dload_dir = cross_product # set Y' as cross product of original vector and arbitrary Y or Z

                if dload_name not in dload_data:
                    dload_data[dload_name] = {"TYPE": dload_type, "MAG": dload_mag, "DIR": dload_dir, "DIR2": dload_dirb}

    dload_blocks = []

    if skipgrav:
        return dload_blocks, nset_counter, fct_id

    for dload_name, data in dload_data.items():
        dload_type = data["TYPE"]
        dload_mag = data["MAG"]
        dload_dir = data["DIR"]
        dload_dirb = data["DIR2"]

        if not already_set:
            if dload_name:
                nset_counter += 1
            ref_nset_counter = nset_counter if dload_name else 0
        skewandgravid = nset_counter
        dgrav_block = "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
        dgrav_block += f"/SKEW/FIX/{skewandgravid}\nSkew for Gravity {dload_name}\n"
        dgrav_block += "#                 OX                  OY                  OZ\n"
        dgrav_block += "                 0.0                 0.0                 0.0\n"
        dgrav_block += "#                 X1                  Y1                  Z1\n"
        dgrav_block += f"{dload_dirb[0]:20.15g}{dload_dirb[1]:20.15g}{dload_dirb[2]:20.15g}\n"
        dgrav_block += "#                 X2                  Y2                  Z2\n"
        dgrav_block += f"{dload_dir[0]:20.15g}{dload_dir[1]:20.15g}{dload_dir[2]:20.15g}\n"
        dgrav_block += "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
        dgrav_block += "# Gravity From .inp DLOAD\n"

        if amplitude_name and amplitude_name in functs_dict:
            funct_id = functs_dict[amplitude_name].get('id')  # Get function ID for Amplitude from directory
        else:
            fct_id  += 1 # increment fct_id for the gravity constant load curve
            funct_id = fct_id  # Default funct_id if no amplitude_name or no match found
        dgrav_block += "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
        dgrav_block += f"/GRAV/{skewandgravid}\nGravity {dload_name}\n"
        dgrav_block += "#funct_IDT       DIR   skew_ID   Isensor  Grnod_id                      Ascale_X            Fscale_Y\n"
        dgrav_block += f"{funct_id:>10}         X{skewandgravid:>10}         0{ref_nset_counter:>10}                             0{dload_mag:>20.15g}\n"

        if not already_set and not property_id == 'all':
            dgrav_block += "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            dgrav_block += f"/GRNOD/PART/{nset_counter}\n"
            dgrav_block += f"{dload_name} secondary nodes\n"
            dgrav_block += "#  PARTIDS\n"
            part_id_rows = []
            for i in range(0, len(prop_ids), 10):
                row_values = prop_ids[i:i+10]
                formatted_row = ''.join(f"{value:>10}" for value in row_values) + '\n'
                part_id_rows.append(formatted_row)

            # Join all part_id_rows with a newline between each row
            dgrav_block += '\n'.join(part_id_rows)

        if not amplitude_name:
            dgrav_block += "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            dgrav_block += "# Constant Function for use with Gravity Card, (magnitude is defined on /GRAV card)\n"
            dgrav_block += "#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n"
            dgrav_block += f"/FUNCT/{funct_id}\n"
            dgrav_block += "Gravity Constant\n"
            dgrav_block += "#                  X                   Y\n"
            dgrav_block += "                   0                   1\n"
            dgrav_block += "                 1.0                   1"

        dload_blocks.append(dgrav_block)

    return dload_blocks, nset_counter, fct_id


####################################################################################################
# Function to create /RBODY from Rigid parts or Nset                                               #
# if in future we convert more coupkin, kincoup, logic will need to change)                        #
####################################################################################################
def convert_rigids(
        input_lines, property_names, nsets, nset_counter,
        relsets_for_expansion_dict, mpc_rigids, max_elem_id
        ):
    rigid_bodies = []
    prop_pattern = r'elset\s*=\s*([^,]+)'
    rigidnset_pattern = r'nset\s*=\s*([^,]+)'
    rigid_part = False
    rigid_nset = False
    rigid_elset = False

    if mpc_rigids:
        for nodeset, refnode in mpc_rigids:
            input_lines.append (f"*rigid body, ref node = {refnode}, nset = {nodeset}")
            print (f"*rigid body, ref node = {refnode}, elset = {nodeset}")

    for line in input_lines:
        if line.lower().strip().startswith('*rigid body'):

            propmatch = re.search(prop_pattern, line, re.IGNORECASE)
            if propmatch:
                property_name = propmatch.group(1).strip()

            rigidnsetmatch = re.search(rigidnset_pattern, line, re.IGNORECASE)

            if rigidnsetmatch:
                property_name = "no_property_name_this_rigid_uses_an_nset"
                nset_name = re.search(r'nset\s*=\s*([^,]+)', line, re.IGNORECASE).group(1).strip()

            #this is to find ref_node
            rbody_id_pattern = r'ref\s*node\s*=\s*([^,]+)'
            rbody_id_match = re.search(rbody_id_pattern, line, re.IGNORECASE)

            if rbody_id_match:
                rbody_id = rbody_id_match.group(1).strip()

                if rbody_id.isdigit():
                    rbody_id = rbody_id

                else:
                    rbody_name = rbody_id
                    print("ref node for rbody is a set, searching for value") # for info
                    nset_data = nsets.get(rbody_name)
                    rbody_id = nset_data['values'] if nset_data else 0

                    # Extract `rbody_id` as digit from list (of single item)
                    if isinstance(rbody_id, list) and rbody_id[0].isdigit():
                        rbody_id = (rbody_id)[0]

                    print(f"Extracted rbody ref node number: {rbody_id} from {rbody_name}") # for info

            else:
                rbody_id = None  # or handle the case where the pattern is not found

            if property_name in property_names:
                rigid_part = True
                property_id = property_names[property_name]['prop_id'] #this is for ref in title and to get node group (same as part number)
                max_elem_id += 1 # increment max element id to use as rigid body id
                nset_counter += 1 # increment nset counter for the node group

            elif property_name in relsets_for_expansion_dict:
                rigid_elset = True
                property_id = "based on nset derived from" #this is for ref in title
                max_elem_id += 1 # increment max element id to use as rigid body id
                nelset_name = f"{property_name}___grnod"
                nset_data = nsets.get(nelset_name)
                ref_nset_counter = nset_data['id'] if nset_data else 0

            elif property_name == "no_property_name_this_rigid_uses_an_nset":
                rigid_nset = True
                property_id = "based on nset" #this is for ref in title
                max_elem_id += 1 # increment max element id to use as rigid body id
                nset_data = nsets.get(nset_name)
                ref_nset_counter = nset_data['id'] if nset_data else 0

            else: continue

            if rigid_part is True:

                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"# RBODY for Part {property_id}")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"/RBODY/{max_elem_id}")
                rigid_bodies.append(f"{property_name}")
                rigid_bodies.append("#     RBID     ISENS     NSKEW    ISPHER                MASS   Gnod_id     IKREM      ICOG   Surf_id")
                rigid_bodies.append(f"{rbody_id:>10}         0         0         0                   0{nset_counter:>10}         0         3         0")
                rigid_bodies.append("#                Jxx                 Jyy                 Jzz")
                rigid_bodies.append("                   0                   0                   0")
                rigid_bodies.append("#                Jxy                 Jyz                 Jxz")
                rigid_bodies.append("                   0                   0                   0")
                rigid_bodies.append("#  Ioptoff   Iexpams")
                rigid_bodies.append("         0         0")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"/GRNOD/PART/{nset_counter}")
                rigid_bodies.append(f"{property_name} secondary nodes")
                rigid_bodies.append("#   PARTID")
                rigid_bodies.append(f"{property_id:>10}")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                nset_counter += 1
                rigid_bodies.append(f"/GRNOD/NODE/{nset_counter}")
                rigid_bodies.append(f"{property_name} main node")
                rigid_bodies.append("#   NODEID")
                rigid_bodies.append(f"{rbody_id:>10}")

                rigid_part = False

            elif rigid_nset is True:

                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"# RBODY {property_id} {nset_name}")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"/RBODY/{max_elem_id}")
                rigid_bodies.append(f"{nset_name}")
                rigid_bodies.append("#     RBID     ISENS     NSKEW    ISPHER                MASS   Gnod_id     IKREM      ICOG   Surf_id")
                rigid_bodies.append(f"{rbody_id:>10}         0         0         0                   0{ref_nset_counter:>10}         0         3         0")
                rigid_bodies.append("#                Jxx                 Jyy                 Jzz")
                rigid_bodies.append("                   0                   0                   0")
                rigid_bodies.append("#                Jxy                 Jyz                 Jxz")
                rigid_bodies.append("                   0                   0                   0")
                rigid_bodies.append("#  Ioptoff   Iexpams")
                rigid_bodies.append("         0         0")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                nset_counter += 1
                rigid_bodies.append(f"/GRNOD/NODE/{nset_counter}")
                rigid_bodies.append(f"RBODY {nset_name} main node")
                rigid_bodies.append("#   NODEID")
                rigid_bodies.append(f"{rbody_id:>10}")

                rigid_nset = False

            elif rigid_elset is True:

                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"# RBODY {property_id} {property_name}")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                rigid_bodies.append(f"/RBODY/{max_elem_id}")
                rigid_bodies.append(f"{property_name}")
                rigid_bodies.append("#     RBID     ISENS     NSKEW    ISPHER                MASS   Gnod_id     IKREM      ICOG   Surf_id")
                rigid_bodies.append(f"{rbody_id:>10}         0         0         0                   0{ref_nset_counter:>10}         0         3         0")
                rigid_bodies.append("#                Jxx                 Jyy                 Jzz")
                rigid_bodies.append("                   0                   0                   0")
                rigid_bodies.append("#                Jxy                 Jyz                 Jxz")
                rigid_bodies.append("                   0                   0                   0")
                rigid_bodies.append("#  Ioptoff   Iexpams")
                rigid_bodies.append("         0         0")
                rigid_bodies.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                nset_counter += 1
                rigid_bodies.append(f"/GRNOD/NODE/{nset_counter}")
                rigid_bodies.append(f"RBODY {property_name} main node")
                rigid_bodies.append("#   NODEID")
                rigid_bodies.append(f"{rbody_id:>10}")

                rigid_elset = False

    return rigid_bodies, nset_counter, max_elem_id


######################################################################################################
# Function to create /RBODY from *COUPLING KINEMATIC assumes all 6 DOF coupled                       #
# *COUPLING, DISTRIBUTING are dealt with in RBE3 section                                             #
######################################################################################################
def convert_coupling(input_lines, nsets, max_elem_id):
    coupling_holder = []
    coupling_name = None
    couplingk = False
    kcoupling = False

    for line in input_lines:
        # Updated regex pattern to ensure both 'COUPLING' and 'CONSTRAINT' are present in the line
        #if re.search(r'COUPLING', line, re.IGNORECASE) and re.search(r'CONSTRAINT', line, re.IGNORECASE):
        if re.search(r'\bCOUPLING\b', line, re.IGNORECASE) and re.search(r'\bCONSTRAINT\b', line, re.IGNORECASE):
            couplingk = True
            if debug_mode:
                print(f"found a coupling")

        if re.search(r'^\s*\*KINEMATIC\s+COUPLING\s*,\s*REF\s*NODE\s*=\s*[^,]+', line, re.IGNORECASE):
            kcoupling = True

        if couplingk:
            kcoupling = False
            # Extract data from coupling line
            # Regex patterns to capture specific fields allowing for flexible spacing and order
            coupling_name_match = re.search(r'CONSTRAINT\s+NAME\s*=\s*([^,]+)', line, re.IGNORECASE)
            coupling_surf_match = re.search(r'SURFACE\s*=\s*([^,]+)', line, re.IGNORECASE)
            coupling_rbodyid_match = re.search(r'REF\s+NODE\s*=\s*([^,]+)', line, re.IGNORECASE)

            if coupling_name_match:
                coupling_name = coupling_name_match.group(1).strip()  # Extracted name
                if debug_mode:
                    print(f"coupling name is {coupling_name}")
            else:
                coupling_name = None  # Handle the case if NAME is not found

            if coupling_surf_match:
                coupling_surf = coupling_surf_match.group(1).strip()

            if coupling_rbodyid_match:
                rbody_id = coupling_rbodyid_match.group(1).strip()

        if kcoupling:
            couplingk = False
            # Extract data from coupling line
            coupling_rbodyid_match = re.search(r'REF\s+NODE\s*=\s*([^,]+)', line, re.IGNORECASE)
            if coupling_rbodyid_match:
                rbody_id = coupling_rbodyid_match.group(1).strip()
                continue
            coupling_name = f"KINEMATIC COUPLING for REF NODE {rbody_id}"
            coupling_surf = f"{line.strip()}"

        if couplingk or kcoupling:
            if not rbody_id.isdigit():
                print("ref node for rbody is a set, searching for value")
                #pattern locate the set for the ref node
                nset_pattern = r'^\s*\*nset\s*,\s*nset\s*=\s*{}\b'.format(re.escape(rbody_id))
                #to match a single value on a nset line for ref node
                number_pattern = r'\b(\d+),?\b'

                in_nset_block = False

                for line in input_lines:
                    if in_nset_block:
                        # Search for numbers in lines following the *nset header
                        refnodenumbermatch = re.findall(number_pattern, line)
                        if refnodenumbermatch:
                            # Extract all matched numbers and update rbody_id
                            # to the first found number (or handle multiple as needed)
                            # Use the first found number as rbody_id
                            rbody_id = refnodenumbermatch[0]
                            print(f"Extracted rbody ref node number: {rbody_id}") # Debug print
                            couplingk = False
                            kcoupling = False
                            break
                        # Stop if a non-number line or blank line appears
                        if not line.strip() or line.startswith("*"):
                            in_nset_block = False  # End the block search

                    # Detect the *nset line to start the block
                    refnodesetmatch = re.search(nset_pattern, line, re.IGNORECASE)
                    if refnodesetmatch:
                        in_nset_block = True  # Start reading numbers in subsequent

            max_elem_id += 1 # increment max element id to use as rigid body id

            nodes_set_id = f"{coupling_surf}"
            nset_data = nsets.get(nodes_set_id)
            #look up the nset counter for the referenced nset (based on the surface)
            coupling_nset_id = nset_data['id'] if nset_data else 0

            if coupling_nset_id == 0:
                nodes_set_id = f"{coupling_surf}___nodes"
                nset_data = nsets.get(nodes_set_id)
                #look up the nset counter for the referenced nset (based on the surface)
                coupling_nset_id = nset_data['id'] if nset_data else 0

            if coupling_nset_id == 0:
                nodes_set_id = f"{coupling_surf}___originalnodeset"
                nset_data = nsets.get(nodes_set_id)
                #look up the nset counter for the referenced nset (based on original nodeset)
                coupling_nset_id = nset_data['id'] if nset_data else 0
            #input(f"found nset: {nodes_set_id} id: {coupling_nset_id}")

            if  coupling_nset_id != 0:

                coupling_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                coupling_holder.append(f"# RBODY for Coupling {coupling_name}")
                coupling_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
                coupling_holder.append(f"/RBODY/{max_elem_id}")
                coupling_holder.append(f"{coupling_name}")
                coupling_holder.append("#     RBID     ISENS     NSKEW    ISPHER                MASS   Gnod_id     IKREM      ICOG   Surf_id")
                coupling_holder.append(f"{rbody_id:>10}         0         0         0                   0{coupling_nset_id:>10}         0         3         0")
                coupling_holder.append("#                Jxx                 Jyy                 Jzz")
                coupling_holder.append("                   0                   0                   0")
                coupling_holder.append("#                Jxy                 Jyz                 Jxz")
                coupling_holder.append("                   0                   0                   0")
                coupling_holder.append("#  Ioptoff   Iexpams")
                coupling_holder.append("         0         0")

    return coupling_holder, max_elem_id


######################################################################################################
# Function to create /RBE3 from *COUPLING assigns weights on main nodes                              #
######################################################################################################
def convert_discoup(input_lines, nsets, max_elem_id):
    discoup_data = []
    discoup_holder = []
    discoup_name = None
    num_nodeset_lines = 0
    ref_node = None
    nodeset_lines = []

    i = 0

    while i < len(input_lines):
        line = input_lines[i].strip()

        if line.startswith("*DISCOUP"):
            id_match = re.search(r'ID\s*=\s*([^,]+)', line, re.IGNORECASE)  # Extract ID value from the current line
            if id_match:
                id_value = id_match.group(1).strip()

                if not id_value.isdigit():
                    max_elem_id += 1  # Increment max element id to use as id
                    id_value = str(max_elem_id)

            id_match = None  # Reset the match object to None
            i += 1
            discoup_name = input_lines[i].strip()
            i += 1
            num_nodeset_lines = int(input_lines[i].strip())
            i += 1
            ref_node = input_lines[i].strip()
            nodeset_lines = []
            for j in range(num_nodeset_lines):
                i += 1
                j += 1
                nodeset_lines.append(input_lines[i].strip())

            discoup_data.append({
                'id': id_value,
                'name': discoup_name,
                'num_nodeset_lines': num_nodeset_lines,
                'ref_node': ref_node,
                'nodeset_lines': nodeset_lines
            })

        i += 1

    for data in discoup_data:
        discoup_name = data['name']
        ref_node = data['ref_node']
        nodeset_lines = data['nodeset_lines']
        num_nodeset_lines = data['num_nodeset_lines']
        id_value = data['id']

        if not ref_node.isdigit():
            print("ref node for rbe3 is a set, searching for value")
            #pattern locate the set for the ref node
            nset_pattern = r'^\s*\*nset\s*,\s*nset\s*=\s*{}\b'.format(re.escape(ref_node))
            #to match a single value on a nset line for ref node
            number_pattern = r'\b(\d+),?\b'

            in_nset_block = False

            for line in input_lines:
                if in_nset_block:
                    # Search for numbers in lines following the *nset header
                    refnodenumbermatch = re.findall(number_pattern, line)
                    if refnodenumbermatch:
                        # Extract all matched numbers and update rbody_id
                        # to the first found number (or handle multiple as needed)
                        # Use the first found number as rbody_id
                        ref_node = refnodenumbermatch[0]
                        print(f"Extracted rbe3 ref node number: {ref_node}") # Debug print
                        break
                    # Stop if a non-number line or blank line appears
                    if not line.strip() or line.startswith("*"):
                        in_nset_block = False  # End the block search

                # Detect the *nset line to start the block
                refnodesetmatch = re.search(nset_pattern, line, re.IGNORECASE)
                if refnodesetmatch:
                    in_nset_block = True  # Start reading numbers in subsequent

        if id_value:

            discoup_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            discoup_holder.append(f"# RBE3 for Coupling {discoup_name}")
            discoup_holder.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            discoup_holder.append(f"/RBE3/{id_value}")
            discoup_holder.append(f"{discoup_name}")
            discoup_holder.append("# Node_IDr Trarotref     N_set   I_modif")
            discoup_holder.append(f"{ref_node:>10}          {num_nodeset_lines:>10}         1")
            discoup_holder.append("#                WTi Trarot_Mi  skew_Idi  grnd_IDi")
            for nodeset_line in nodeset_lines:
                nodeset_name, weight = nodeset_line.split(',')
                weight = float(weight)
                nodeset_id = nsets.get(nodeset_name)['id']
                discoup_holder.append(f"{weight:>20.8g}   111 000          {nodeset_id:>10}")


    return discoup_holder, max_elem_id


####################################################################################################
# Function to Parse control card information for Engine                                            #
####################################################################################################
def parse_control_data(input_lines, simple_file_name):
    engine_file = []

    dt_value = 5e-7               #
    run_time = 1.0                #
    anim_number = 100             #    These lines define some arbitrary default values
    anim_interval = 1e-2          #          Will be modified by parsed data
    th_interval = 1e-4            #               If available

    dt_set = False                #    Tracks whether dt was set by a 'MASS SCALING' input


    i = 0 # Initialize an index for iterating through input_lines

    #this section checks for control attributes and stores them as variables
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Define a regular expression pattern to match the line starting with '*VARIABLE MASS SCALING'
        cst_pattern = r'^\s*\*VARIABLE MASS SCALING.*$'

        # Use re.search to find the first match (case-insensitive)
        cst_match = re.search(cst_pattern, line, re.IGNORECASE)

        # Define a regular expression pattern to match the line starting with '*FIXED MASS SCALING'
        fst_pattern = r'^\s*\*FIXED MASS SCALING.*$'

        # Use re.search to find the first match (case-insensitive)
        fst_match = re.search(fst_pattern, line, re.IGNORECASE)

        # Define a regular expression pattern to match the line starting with '*DYNAMIC, EXPLICIT'
        runtime_pattern = r'^\s*\*DYNAMIC(?:\s*,\s*\w+\s*=\s*\w+)?\s*,\s*EXPLICIT(?:\s*=\s*\d+)?\s*,?\s*$'

        # Use re.search to find the first match (case-insensitive)
        runtime_match = re.search(runtime_pattern, line, re.IGNORECASE)

        # Define a regular expression pattern to match the line starting with '*DYNAMIC, EXPLICIT'
        direct_runtime_pattern = r'^\s*\*DYNAMIC(?:\s*,\s*\w+\s*=\s*\w+)?\s*,\s*DIRECT\s*,\s*EXPLICIT(?:\s*=\s*\d+)?\s*,?\s*$'

        # Use re.search to find the first match (case-insensitive)
        direct_runtime_match = re.search(direct_runtime_pattern, line, re.IGNORECASE)

        # Define a regular expression pattern to match line starting '*OUTPUT, FIELD'
        field_pattern = r'^\s*\*OUTPUT\s*,\s*FIELD\s*.*$'

        # Use re.search to find the first match (case-insensitive)
        field_match = re.search(field_pattern, line, re.IGNORECASE)

        if cst_match:
            # Define a regular expression pattern to match 'DT' and its value
            dt_pattern = r'\bDT\s*=\s*([\d.eE+-]+)'

            # Use re.search to find the first match (case-insensitive)
            dt_match = re.search(dt_pattern, line, re.IGNORECASE)

            if dt_match:
                dt_value = dt_match.group(1)
                dt_set = True

        if fst_match:
            # Define a regular expression pattern to match 'DT' and its value
            dt_pattern = r'\bDT\s*=\s*([\d.eE+-]+)'

            # Use re.search to find the first match (case-insensitive)
            dt_match = re.search(dt_pattern, line, re.IGNORECASE)

            if dt_match:
                dt_value = dt_match.group(1)
                dt_set = True

        if runtime_match:
            i += 1

            data_line = input_lines[i].strip()
            timevalues = data_line.split(',')
            if not dt_set and timevalues[0].strip():
                dt_value = float(data_line.split(',')[0])
            run_time = float(data_line.split(',')[1])
            anim_interval = run_time / anim_number
            th_interval = anim_interval / 100

        if direct_runtime_match:
            i += 1

            data_line = input_lines[i].strip()
            timevalues = data_line.split(',')
            if not dt_set and timevalues[0].strip():
                dt_value = float(data_line.split(',')[0])
            run_time = float(data_line.split(',')[1])
            anim_interval = run_time / anim_number
            th_interval = anim_interval / 100

        if field_match:
            # Define a regular expression pattern to match 'NUMBER INTERVAL =' followed by digits
            interval_pattern = r'NUMBER INTERVAL\s*=\s*(\d+)'

            # Define a regular expression pattern to match 'TIME INTERVAL =' followed by digits
            time_interval_pattern = r'TIME INTERVAL\s*=\s*(\d+)'
            anim_interval_pattern = r'=\s*([\d.]+)\s*$'

            # Use re.search to find the first match (case-insensitive)
            interval_match = re.search(interval_pattern, line, re.IGNORECASE)

            # Use re.search to find the first match (case-insensitive)
            time_interval_match = re.search(time_interval_pattern, line, re.IGNORECASE)

            if interval_match:
                anim_number = int(interval_match.group(1))
                anim_interval = run_time / anim_number
                th_interval = anim_interval / 100

            elif time_interval_match:
                anim_value = re.search(anim_interval_pattern, line)
                anim_interval = float(anim_value.group(1))
                th_interval = anim_interval / 100
        i += 1

    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/PRINT/-100/50\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append(f"/RUN/{simple_file_name}/1\n")
    engine_file.append(f"{run_time}\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/PARITH/OFF\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/DT\n")
    engine_file.append(f"0  {anim_interval}\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/VECT/DISP\n")
    engine_file.append("/ANIM/VECT/VEL\n")
    engine_file.append("/ANIM/VECT/ACC\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/VECT/CONT\n")
    engine_file.append("/ANIM/VECT/CONT2\n")
    engine_file.append("/ANIM/VECT/PCONT\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/BRICK/TENS/STRESS\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/ELEM/EPSP\n")
    engine_file.append("/ANIM/ELEM/ENER\n")
    engine_file.append("/ANIM/ELEM/VONM\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/SHELL/EPSP/UPPER\n")
    engine_file.append("/ANIM/SHELL/EPSP/LOWER\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/NODA/DT\n")
    engine_file.append("/ANIM/NODA/DMAS\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/ANIM/SHELL/TENS/STRESS/UPPER\n")
    engine_file.append("/ANIM/SHELL/TENS/STRESS/LOWER\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/DT/NODA/CST/0\n")
    engine_file.append(f"0.9  {dt_value}\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/DT1TET10\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/STOP\n")
    engine_file.append("0  0  0  1  1\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/TFILE/4\n")
    engine_file.append(f"{th_interval}\n")
    engine_file.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
    engine_file.append("/TH/TITLE\n")

    return engine_file


####################################################################################################
# Function to convert *MPC ties to Type13 Springs                                                  #
####################################################################################################
def convert_mpc_ties(input_lines, prop_id, max_elem_id):
    global rho_magnitude
    global e_magnitude
    processing_mpcs = False

    spring_k = e_magnitude * 5                       #
    spring_rk = e_magnitude * 7                      #    Spring Stiffnesses and densities are based
    spring_mass = rho_magnitude * 1                  #        on material values from model
    spring_inertia = rho_magnitude * 1.5             #

    mpc_ties = []
    mpc_rigids = []

    for line in input_lines:
        mpc_type_pattern = r'^\s*\*MPC?' # Regular expression to find '*MPC' contact entry
        matchmpc = re.search(mpc_type_pattern, line, re.IGNORECASE)

        if matchmpc:
            # Extract tied contact name from the current line
            processing_mpcs = True

            prop_id += 1 #increment the global prop_id
            spring_prop_name = f"SpringBeams_for_Connections_{prop_id}"
            mpc_ties.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            mpc_ties.append(f"#Spring PART for connection definition: {spring_prop_name}: for .inp *MPC TIE")
            mpc_ties.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            mpc_ties.append(f"/PART/{prop_id}\n{spring_prop_name}")
            mpc_ties.append("#     prop       mat    subset")
            mpc_ties.append(f"{prop_id:>10}         0         0")
            mpc_ties.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            mpc_ties.append(f"#Spring PROP for connection definition: {spring_prop_name}: for .inp *MPC TIE")
            mpc_ties.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            mpc_ties.append(f"/PROP/TYPE13/{prop_id}\n{spring_prop_name}")
            mpc_ties.append("#               Mass             Inertia   skew_ID   sens_ID    Isflag     Ifail     Ileng    Ifail2")
            mpc_ties.append(f"{spring_mass:>20.4e}{spring_inertia:>20.4e}         0         0         0         0         0         0")
            mpc_ties.append("#                 K1                  C1                  A1                  B1                  D1")
            mpc_ties.append(f"{spring_k:>20.4e}                   0                   0                   0                   0")
            mpc_ties.append("# fct_ID11        H1  fct_ID21  fct_ID31  fct_ID41                    delta_min1          delta_max1")
            mpc_ties.append("         0         0         0         0         0                             0                   0")
            mpc_ties.append("#                 F1                  E1             Ascale1             Hscale1")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#                 K2                  C2                  A2                  B2                  D2")
            mpc_ties.append(f"{spring_k:>20.4e}                   0                   0                   0                   0")
            mpc_ties.append("# fct_ID12        H2  fct_ID22  fct_ID32  fct_ID42                    delta_min2          delta_max2")
            mpc_ties.append("         0         0         0         0         0                             0                   0")
            mpc_ties.append("#                 F2                  E2             Ascale2             Hscale2")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#                 K3                  C3                  A3                  B3                  D3")
            mpc_ties.append(f"{spring_k:>20.4e}                   0                   0                   0                   0")
            mpc_ties.append("# fct_ID13        H3  fct_ID23  fct_ID33  fct_ID43                    delta_min3          delta_max3")
            mpc_ties.append("         0         0         0         0         0                             0                   0")
            mpc_ties.append("#                 F3                  E3             Ascale3             Hscale3")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#                 K4                  C4                  A4                  B4                  D4")
            mpc_ties.append(f"{spring_rk:>20.4e}                   0                   0                   0                   0")
            mpc_ties.append("# fct_ID14        H4  fct_ID24  fct_ID34  fct_ID44                    delta_min4          delta_max4")
            mpc_ties.append("         0         0         0         0         0                             0                   0")
            mpc_ties.append("#                 F4                  E4             Ascale4             Hscale4")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#                 K5                  C5                  A5                  B5                  D5")
            mpc_ties.append(f"{spring_rk:>20.4e}                   0                   0                   0                   0")
            mpc_ties.append("# fct_ID15        H5  fct_ID25  fct_ID35  fct_ID45                    delta_min5          delta_max5")
            mpc_ties.append("         0         0         0         0         0                             0                   0")
            mpc_ties.append("#                 F5                  E5             Ascale5             Hscale5")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#                 K6                  C6                  A6                  B6                  D6")
            mpc_ties.append(f"{spring_rk:>20.4e}                   0                   0                   0                   0")
            mpc_ties.append("# fct_ID16        H6  fct_ID26  fct_ID36  fct_ID46                    delta_min6          delta_max6")
            mpc_ties.append("         0         0         0         0         0                             0                   0")
            mpc_ties.append("#                 F6                  E6             Ascale6             Hscale6")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#                 V0              Omega0               F_cut   Fsmooth")
            mpc_ties.append("                   0                   0                   0         0")
            mpc_ties.append("#                  C                   n               alpha                beta")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("                   0                   0                   0                   0")
            mpc_ties.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            mpc_ties.append(f"#Spring Elements for connection definition: {spring_prop_name}: for .inp *MPC TIE")
            mpc_ties.append("#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|")
            mpc_ties.append(f"/SPRING/{prop_id}")
            mpc_ties.append("#  Sprg_ID  NodeID_1  NodeID_2")

            continue #(skip the *MPC line itself)

        if processing_mpcs and line.startswith('*'):
            processing_mpcs = False

        if processing_mpcs and not line.startswith('*'):
            mpcdata = line.split(",")  # Split the line by comma
            mpc_type = mpcdata[0].strip()
            mpc_node_1 = mpcdata[1].strip()
            mpc_node_2 = mpcdata[2].strip()
            max_elem_id += 1 # Increment the max elem_id

            #create a spring for each .inp TIE *MPC)
            if mpc_type.lower() == 'tie':
                mpc_ties.append(f"{max_elem_id:>10}{mpc_node_1:>10}{mpc_node_2:>10}")

            elif mpc_type.lower() == 'beam':
                prop_id -= 1  #de-increment the global prop_id
                mpc_ties = []
                mpc_rigids.append((mpc_node_1, mpc_node_2))

            else:
                prop_id -= 1  #de-increment the global prop_id
                mpc_ties = []

    return mpc_ties, mpc_rigids, prop_id, max_elem_id


####################################################################################################
# Function to convert elements data (special element by element approach for AT) No longer used in #
# this version, here for reference                                                                 #
#                                                                                                  #
# Rework this at some point for special cases where every element needs it's own part/prop         #
#                             (element thickness with offset)                                      #
####################################################################################################
def convert_elements_at(input_lines):
    element_lines = []
    distribution_values = {}  # Initialize distribution_values dictionary
    inside_element_section = False
    inside_distribution_section = False

    # Process the input to collect distribution values
    for line in input_lines:
        if line.startswith('*Distribution'):
            inside_distribution_section = True
            continue  # Skip the '*Distribution' line itself
        if line.startswith('*'):
            inside_distribution_section = False

        if inside_distribution_section and not line.startswith('*'):
            if not line.startswith(','):  # Skip lines starting with comma
                distribution_id, distribution_value = map(float, line.split(','))
                distribution_values[int(distribution_id)] = distribution_value

    for line in input_lines:
        if line.startswith('*Element, type=S4R'):
            inside_element_section = True
        elif line.startswith('*Distribution'):
            inside_distribution_section = True
        elif line.startswith('*'):
            inside_element_section = False
            inside_distribution_section = False

        if inside_distribution_section and not line.startswith('*'):
            if not line.startswith(','): # Skip lines starting with comma
                distribution_id, distribution_value = map(float, line.split(','))
                distribution_values[int(distribution_id)] = distribution_value

        if inside_element_section and not line.startswith('*'):
            elements = line.strip().split(',')
            element_id = int(elements[0])
            # Get distribution value for the element
            thickness_value = distribution_values.get(element_id, 0.0)

            # Format the first five elements with 10-wide fields, right-justified
            formatted_shell_values = ' '.join(f"{element.strip():>10}" for element in elements[:5])

            prop_type11_value = thickness_value

            export_format = f"/PART/{element_id}\n" \
                            f"{element_id}\n" \
                            f"{element_id:>10}         1         0\n" \
                            f"/SHELL/{element_id}\n" \
                            f"{element_id:>10}{elements[1]:>10}{elements[2]:>10}{elements[3]:>10}{elements[4]:>10}                             0\n" \
                            f"/PROP/TYPE11/{element_id}\n" \
                            f"{prop_type11_value:<20.15g}\n" \
                            f"        24                             1\n" \
                            f"\n" \
                            f"         5          {prop_type11_value:>20.15g}                 1.0\n" \
                            f"                                                                                         1        20\n" \
                            f"                   0{prop_type11_value / 5:>20.15g}{prop_type11_value * 0.1:>20.15g}         1\n" \
                            f"                   0{prop_type11_value / 5:>20.15g}{prop_type11_value * 0.3:>20.15g}         1\n" \
                            f"                   0{prop_type11_value / 5:>20.15g}{prop_type11_value * 0.5:>20.15g}         1\n" \
                            f"                   0{prop_type11_value / 5:>20.15g}{prop_type11_value * 0.7:>20.15g}         1\n" \
                            f"                   0{prop_type11_value / 5:>20.15g}{prop_type11_value * 0.9:>20.15g}         1"

            element_lines.append(export_format)
    return element_lines


####################################################################################################
#                                                                                                  #
#-  Main Conversion  Tasks Function and input/output below                                         #
#                                                                                                  #
####################################################################################################
# Main conversion function, calling other functions
def main_conversion_sp(input_lines, simple_file_name, elsets_for_expansion_dict,
    non_numeric_references, relsets_for_expansion_dict, nset_references
    ):

    transform_lines, transform_data = convert_transforms(input_lines)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Transforms Done:       {elapsed_time:8.3f} seconds")

    node_data, input_lines = read_nodes(input_lines)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Nodes Read:            {elapsed_time:8.3f} seconds")

    node_lines = convert_nodes(node_data)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Nodes Done:            {elapsed_time:8.3f} seconds")

    input_lines = convert_distcoup(input_lines)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Dist Coups Prep Done:  {elapsed_time:8.3f} seconds")

    nsets, nset_counter, input_lines = convert_nsets(input_lines, nset_references)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Nsets Read:            {elapsed_time:8.3f} seconds")

    nset_blocks = create_nblocks(nsets)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Nsets Done:            {elapsed_time:8.3f} seconds")

    material_names, fct_id = convert_materials(input_lines)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Materials Done:        {elapsed_time:8.3f} seconds")

    property_names, prop_id = convert_props(input_lines, material_names)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Props/Parts Done:      {elapsed_time:8.3f} seconds")

    elset_dicts = prepare_elsets(input_lines, elsets_for_expansion_dict, relsets_for_expansion_dict)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Elset Prep Done:       {elapsed_time:8.3f} seconds")

    #new dictionary based version for element writing
    (elset_dicts, element_lines, element_dicts, sh3n_list, shell_list, brick_list, property_names,
        max_elem_id, input_lines, nsets, nset_counter, ppmselect
        ) = parse_element_data(input_lines, elset_dicts, property_names, non_numeric_references,
        nsets, nset_counter
        )

    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Elements Done:         {elapsed_time:8.3f} seconds")

    elset_blocks, nset_counter, nsets, elset_dicts = write_element_groups(nset_counter, nsets,
        sh3n_list, shell_list, brick_list, elset_dicts
        )
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Elsets Done:           {elapsed_time:8.3f} seconds")

    segment_dictionary = convert_segments(element_dicts, input_lines)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Segments Done:         {elapsed_time:8.3f} seconds")

    (surface_lines, surf_id, surf_name_to_id, nset_counter, nsets, elset_dicts,
     input_lines) = parse_surface_data(input_lines, elset_dicts, nset_counter,
     nsets, segment_dictionary, property_names
     )

    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Surf Sets Done:        {elapsed_time:8.3f} seconds")

    friction_dict = parse_surface_interaction_data(input_lines)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Friction Done:         {elapsed_time:8.3f} seconds")

    contacts, surf_id, inter_id = convert_contacts(input_lines, property_names, surf_id,
        friction_dict, surf_name_to_id
        )
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Contacts Done:         {elapsed_time:8.3f} seconds")

    tied_contacts, inter_id = convert_ties(input_lines, surf_name_to_id, nsets, inter_id)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Tied Contacts Done:    {elapsed_time:8.3f} seconds")

    functs_dict, fct_id = read_amplitudes(input_lines, fct_id)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Functions Done:        {elapsed_time:8.3f} seconds")

    boundary_blocks, nset_counter, fct_id = convert_boundary(input_lines, nset_counter,
        nsets, functs_dict, fct_id
        )
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Boundaries Done:       {elapsed_time:8.3f} seconds")

    function_blocks = write_functions(functs_dict)

    initial_blocks, nset_counter = convert_initial(input_lines, nset_counter, nsets)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Ini Conditions Done:   {elapsed_time:8.3f} seconds")

    dload_blocks, nset_counter, fct_id = convert_dloads(input_lines, nset_counter, nsets,
        property_names, functs_dict, fct_id
        )
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Gravity Done:          {elapsed_time:8.3f} seconds")

    mpc_ties, mpc_rigids, prop_id, max_elem_id = convert_mpc_ties(input_lines, prop_id,
        max_elem_id
        )
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"MPC-Springs Done:      {elapsed_time:8.3f} seconds")

    conn_beams = convert_connbeams(property_names)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Spring Beams Done:     {elapsed_time:8.3f} seconds")

    rigid_bodies, nset_counter, max_elem_id = convert_rigids(input_lines, property_names,
        nsets, nset_counter, relsets_for_expansion_dict, mpc_rigids, max_elem_id
        )
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Part Rbodies Done:     {elapsed_time:8.3f} seconds")

    couplings, max_elem_id = convert_coupling(input_lines, nsets, max_elem_id)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Coupling Rbodies Done: {elapsed_time:8.3f} seconds")

    discoups, max_elem_id = convert_discoup(input_lines, nsets, max_elem_id)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"DisCoups Done:         {elapsed_time:8.3f} seconds")

    engine_file = parse_control_data(input_lines, simple_file_name)
    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Engine File Done:      {elapsed_time:8.3f} seconds")

    return (
            transform_lines, transform_data, node_lines, nsets, nset_blocks, material_names,
            property_names, ppmselect, element_lines, elset_blocks, surface_lines, contacts,
            tied_contacts, boundary_blocks, function_blocks, initial_blocks, dload_blocks,
            rigid_bodies, couplings, discoups, mpc_ties, conn_beams, engine_file
           )


####################################################################################################
# Define Text Blocks for headers of each Radioss deck section                                      #
####################################################################################################
def write_output(transform_lines, transform_data, node_lines, nset_blocks, material_names,
 property_names, ppmselect, non_numeric_references, nsets, element_lines, elset_blocks,
 surface_lines, contacts, tied_contacts, boundary_blocks, function_blocks, initial_blocks,
 dload_blocks, rigid_bodies, couplings, discoups, mpc_ties, conn_beams, engine_file,
 simple_file_name, output_file_name, output_file_path, engine_file_name, engine_file_path
 ):

    global start_time
    global run_timer
    global or_gui

    header_block = f"""#RADIOSS STARTER
# Input deck generated by inp2rad python script, please verify correct input!
# REPORT ISSUES to https://github.com/OpenRadioss/Tools/discussions
/BEGIN
{simple_file_name}
      2023         0
                  Mg                  mm                   s
                  Mg                  mm                   s
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  1. MATERIALS:
"""
    part_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  2. PARTS 
"""
    prop_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  3. PROPS 
"""
    nodes_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  4. NODES:
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
"""
    elements_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  5. ELEMENTS:
"""
    group_and_th_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  6. GRNOD groups and time history requests
"""
    boundary_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  7. BCS and IMPDISP definitions
"""
    functions_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  8. FUNCTIONS
"""
    rigidp_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  9. RIGID BODY from PART definitions
"""
    rigidc_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 10. RIGID BODY from COUPLING definitions
"""
    rbe3_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 11. RBE3 from COUPLING and DCOUP3D definitions
"""
    mpc_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 12. SPRING MPCs from TIE definitions
"""
    tied_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 13. TIED INTERFACES
"""
    contact_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 14. INTERFACES
"""
    surface_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 15. SURFACES
"""
    transforms_header = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#- 16. TRANSFORMS
"""
    footer = """#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
/END
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
"""


####################################################################################################
# Write output to Radioss Starter deck  (_0000.rad)                                                #
####################################################################################################
    with open(output_file_path, "w") as output_file:

        if run_timer:
            elapsed_time = time.time() - start_time
            print("")
            print(f"Writing Radioss Files ---------->")
            print("")

        output_file.write(header_block)  # Write the header block

        #MAT LAW1
        for material_name, properties in material_names.items():
            #print(material_names)
            if check_if_elast(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                emodulus = properties['emodulus']
                poissrat = properties['poissrat']
    # Write the card format for materials elastic properties
                write_elastic_material(material_id, material_name, rho,
                    emodulus, poissrat, output_file
                    )

        #MAT LAW36
        for material_name, properties in material_names.items():
            if check_if_plast(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                emodulus = properties['emodulus']
                poissrat = properties['poissrat']
                plastic_data = properties['plastic_data']
    # Write the card format for materials with elasto-plastic properties
                write_plastic_material(material_id, material_name, rho, emodulus, poissrat,
                    plastic_data, output_file
                    )

        #MAT LAW42
        for material_name, properties in material_names.items():
            if check_if_neohooke(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                neohooke_mu = properties['neohooke_mu']
    # Write the card format for materials with mooney-rivlin properties
                write_neohooke_material(material_id, material_name, rho, neohooke_mu, output_file)

        #MAT LAW42
        for material_name, properties in material_names.items():
            if check_if_mr(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                mr_mu1 = properties['mr_mu1']
                mr_mu2 = properties['mr_mu2']
    # Write the card format for materials with mooney-rivlin properties
                write_mr_material(material_id, material_name, rho, mr_mu1, mr_mu2, output_file)

        #MAT LAW59
        for material_name, properties in material_names.items():
            if check_if_cohesive(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                emodulus = properties['emodulus']
                gmodulus = properties['gmodulus']
    # Write the card format for materials with cohesive properties
                write_coh_material(material_id, material_name, rho, emodulus,
                    gmodulus, output_file
                    )

        #MAT LAW69
        for material_name, properties in material_names.items():
            if check_if_ogden_c(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                ogden_n = properties['ogden_n']
                poissrat = properties['poissrat']
                uniaxial_data = properties['uniaxial_data']
    # Write the card format for materials with ogden properties
                write_ogden_c_material(material_id, material_name, rho, ogden_n,
                    poissrat, uniaxial_data, output_file
                    )

        #MAT LAW70
        for material_name, properties in material_names.items():
            if check_if_hypf(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                poissrat = properties['poissrat']
                uniaxial_data = properties['uniaxial_data']
    # Write the card format for materials with foam properties
                write_hypf_material(material_id, material_name, rho, poissrat, uniaxial_data,
                    output_file
                    )

        #MAT LAW71
        for material_name, properties in material_names.items():
            if check_if_se(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                emodulus = properties['emodulus']
                poissrat = properties['poissrat']
                se_mm = properties['se_mm']
                se_mpr = properties['se_mpr']
                se_uts = properties['se_uts']
                se_tbt = properties['se_tbt']
                se_tet = properties['se_tet']
                se_trbt = properties['se_trbt']
                se_tret = properties['se_tret']
                se_tbc = properties['se_tbc']
                se_reftemp = properties['se_reftemp']
                se_slope_load = properties['se_slope_load']
                se_slope_unload = properties['se_slope_unload']

    # Write the card format for materials with superelastic properties
                write_supere_material(material_id, material_name, rho, emodulus, poissrat, se_mm, se_mpr,
                    se_uts, se_tbt, se_tet, se_trbt, se_tret, se_tbc, se_reftemp, se_slope_load,
                    se_slope_unload, output_file
                    )

        #MAT LAW82
        for material_name, properties in material_names.items():
            if check_if_ogden(properties):
                material_id = properties['material_id']
                rho = properties['rho']
                ogden_mu = properties['ogden_mu']
                ogden_alpha = properties['ogden_alpha']
                ogden_D = properties['ogden_D']
    # Write the card format for materials with ogden properties
                write_ogden_material(material_id, material_name, rho, ogden_mu, ogden_alpha,
                    ogden_D, output_file
                    )

        #MAT VOID
        for material_name, properties in material_names.items():
            if check_if_rigid(properties):
                material_id = properties['material_id']
    # Write the card format for materials with rigid properties
                write_rigid_material(material_id, material_name, output_file)

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Materials Written:     {elapsed_time:8.3f} seconds")

        #MASS
        for material_name, properties in material_names.items():
            if check_if_mass(properties):
                mass = properties['mass']
                #input(f"mass is {mass}")

    # Write the card format for /ADMAS masses
                write_admas(material_name, nsets, mass, output_file)

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"ADMAS Written:         {elapsed_time:8.3f} seconds")


    # Write parts and properties
        output_file.write(part_header)  # Write the part/el/prop section header
        write_parts(property_names, non_numeric_references, output_file)
        output_file.write(prop_header)  # Write the part/el/prop section header
        write_props(property_names, output_file)
        output_file.write(nodes_header)  # Write the node section header

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Parts/Props Written:   {elapsed_time:8.3f} seconds")

        for transform_id, lines in node_lines.items():
            if transform_id in transform_data:
                output_file.write(f"//SUBMODEL/{transform_id}\n")
                output_file.write(f"Submodel for Transform Skew {transform_id}\n")
                output_file.write("         0         0         0         0         0         0         0\n")

            output_file.write("/NODE\n")
            for node_line in lines:
                #print(node_line)
                output_file.write(node_line + '\n')

            if transform_id in transform_data:
                output_file.write(f"//ENDSUB\n")

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Nodes Written:         {elapsed_time:8.3f} seconds")

        output_file.write(elements_header)  # Write the element section header
        for element_line in element_lines:
            output_file.write(element_line + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Elements Written:      {elapsed_time:8.3f} seconds")

        output_file.write(group_and_th_header)  # Write the group and th section header
        for nset_block in nset_blocks:
            for block in nset_block:
                output_file.write(block)

        for elset_block in elset_blocks:
            # Only write the block if it's not just a newline
            if elset_block.strip():
                output_file.write(elset_block + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Sets Written:          {elapsed_time:8.3f} seconds")


        output_file.write(boundary_header)  # Write the boundary condition section header
        for boundary_block in boundary_blocks:
            output_file.write(boundary_block + '\n')


        for initial_block in initial_blocks:
            output_file.write(initial_block + '\n')


        for dload_block in dload_blocks:
            output_file.write(dload_block + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"BCS/Loads Written:     {elapsed_time:8.3f} seconds")


        output_file.write(functions_header) # Write the functions section header
        for functions in function_blocks:
            output_file.write(functions + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Functions Written:     {elapsed_time:8.3f} seconds")


        output_file.write(rigidp_header)  # Write the rigid entity section header for parts
        for rigid_body in rigid_bodies:
            output_file.write(rigid_body + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"PART RBODYs Written:   {elapsed_time:8.3f} seconds")

        output_file.write(rigidc_header)  # Write the rigid entity section header for couplings
        for coupling in couplings:
            output_file.write(coupling + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"COUP RBODYs Written:   {elapsed_time:8.3f} seconds")

        output_file.write(rbe3_header)  # Write the RBE3 section header for couplings
        for discoup in discoups:
            output_file.write(discoup + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"RBE3s Written:         {elapsed_time:8.3f} seconds")

        output_file.write(mpc_header)  # Write the mpc section header for ties
        for mpc_tie in mpc_ties:
            output_file.write(mpc_tie + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"SpringTies Written:    {elapsed_time:8.3f} seconds")

        for conn_beam in conn_beams:
            output_file.write(conn_beam + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"SpringBeams Written:   {elapsed_time:8.3f} seconds")

        output_file.write(tied_header)  # Write the tied contact section header for ties
        for tied_contact in tied_contacts:
            output_file.write(tied_contact + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Tied Contacts Written: {elapsed_time:8.3f} seconds")

        output_file.write(contact_header)  # Write the contact section header for contacts
        for contact in contacts:
            output_file.write(contact + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Contacts Written:      {elapsed_time:8.3f} seconds")

        output_file.write(surface_header)  # Write the surface section header for surfaces
        for surface_line in surface_lines:
            output_file.write(surface_line + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Surf Sets Written:     {elapsed_time:8.3f} seconds")

        output_file.write(transforms_header)  # Write the transform section header for transforms
        for transform_line in transform_lines:
            output_file.write(transform_line + '\n')

        if run_timer:
            elapsed_time = time.time() - start_time
            print(f"Transforms Written:    {elapsed_time:8.3f} seconds")

        output_file.write(footer)  # Write the /END card footer


####################################################################################################
# Write output to Radioss Engine file (_0001.rad)                                                  #
####################################################################################################
    with open(engine_file_path, "w") as engine_output:
        for engine_file_lines in engine_file:
            engine_output.write(engine_file_lines)  # Write the engine file

    if run_timer:
        elapsed_time = time.time() - start_time
        print(f"Engine Written:        {elapsed_time:8.3f} seconds")

    if or_gui:
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Print the total processing time
        print("")
        print(f"Reading Completed in   {elapsed_time:8.3f} seconds")
        print("")
        print(f"OpenRadioss Starter written to: {output_file_name}")
        print("")
        print(f"OpenRadioss Engine written to:  {engine_file_name}")
        print("")

    else:
        print("")
        print(f"Conversion Completed. Output written to {output_file_name} and {engine_file_name}")

    if run_timer and not or_gui:
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Print the total processing time
        print("")
        print(f"Total Processing time: {elapsed_time:8.3f} seconds")

    if ppmselect:
        print("INFO: PrePoMax Internal Select detected, part/prop assignment incomplete")
        print("      please correct PART IDs for elements in rad file or return to PPM")
        print("      and assign properties by Part instead of 'Selection'")
    

    if not or_gui:
        input("Press Enter to exit...")

    output_done = True

    if ppmselect:
        output_done = False

    return output_done


####################################################################################################
# Function to Read input file and then run the code on it, starting a progress timer               #
####################################################################################################
def input_read(input_file_path):
    global input_file_name
    global run_timer
    global or_gui
    global original_lines
    global start_time

    input_file_name = os.path.basename(input_file_path)
    simple_file_name = os.path.splitext(input_file_name)[0]
    # Use stripped filename with .rad extension
    output_file_name = os.path.splitext(input_file_name)[0] + "_0000.rad"
    output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)
    # Use stripped filename with .rad extension
    engine_file_name = os.path.splitext(input_file_name)[0] + "_0001.rad"
    engine_file_path = os.path.join(os.path.dirname(input_file_path), engine_file_name)

#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
    if or_gui:
        print("Reading .inp file, Please wait...")

    else:
        print("Converting .inp file, Please wait...")

    with open(input_file_path, "r") as input_file:


####################################################################################################
# Start a timer to check script performance                                                        #
####################################################################################################

        if run_timer:
            start_time = time.time()
            print("Starting Timer:           0.000 seconds")

        if or_gui:
            start_time = time.time()


####################################################################################################
# Pass the input lines from the .inp deck as a list                                                #
####################################################################################################

        original_lines = input_file.readlines()

####################################################################################################
# Check for INCLUDE files and process contents                                                     #
####################################################################################################
            
    expanded_lines = []
    include_pattern = re.compile(r'\*INCLUDE\s*,\s*INPUT\s*=\s*(.+)', re.IGNORECASE)

    for line in original_lines:
        match = include_pattern.match(line.strip())
        if match:
            include_path = match.group(1).strip()
            include_path = os.path.normpath(os.path.join(os.path.dirname(input_file_path), include_path))  # Resolve relative path
            if os.path.exists(include_path):
                print(f"Including file: {include_path}")
                with open(include_path, "r") as include_file:
                    expanded_lines.extend(include_file.readlines())
            else:
                print(f"Warning: Included file {include_path} not found. Keeping original reference.")
                expanded_lines.append(line)
        else:
            expanded_lines.append(line)

    return (expanded_lines, input_file_name, simple_file_name, output_file_name, 
            output_file_path, engine_file_name, engine_file_path)
            
            
####################################################################################################
# Line pre-processor, strips comment lines, special characters etc                                 #
####################################################################################################
def preprocess_lines(original_lines):
    input_lines = []
    elset_counter = 1  # Counter for generating placeholder elset names
    system_counter = 0

    for line in original_lines:
        if line.lower().startswith('*assembly'):
            if or_gui:
                print("### INFO ###")
                print("part/instance models are not (yet!) supported by the A2R script")
                print("please use a flattened model")
                print("or you may try standalone conversion by calling this script at commandline")
                sys.exit("A2R unable to continue")
                break

            print("### INFO ###")
            print("part/instance models are not (yet!) supported by the A2R script")
            print("if possible use a flattened model")
            print("process will attempt to continue the best it can")
            print("")
            input("press enter to continue")

        if not line.startswith('**'):
            modified_line = line.replace('"', '').replace('@', '_').replace('(', '_').replace(')', '_').replace('`', '_')

            if modified_line.lower().startswith('*system'):
                system_counter += 1
                modified_line = f'*SYSTEM ID={system_counter}\n'

            # Check for lines starting with '*ELEMENT'
            if modified_line.lower().startswith('*element') and not modified_line.lower().startswith('*element output'):
                # Split the line into components by commas
                components = modified_line.split(',')

                # Check for any component containing 'elset' (case insensitive)
                has_elset = any(re.search(r'\belset\s*=', component, re.IGNORECASE) for component in components)

                # Check for 'TYPE=R', 'TYPE =R', 'TYPE= R', 'TYPE = R' (case insensitive)
                has_type_r = any(re.search(r'\bTYPE\s*=\s*R', component, re.IGNORECASE) for component in components)

                if not has_elset and not has_type_r:
                    # If there's no ELSET, add a placeholder elset
                    modified_line = modified_line.strip() + f', ELSET=placeholder_elset_{elset_counter}\n'
                    elset_counter += 1

                if not has_elset and has_type_r:
                    # If there's no ELSET, add a placeholder rigidelset
                    modified_line = modified_line.strip() + f', ELSET=placeholder_rigidelset_{elset_counter}\n'
                    elset_counter += 1


            input_lines.append(modified_line)

    return input_lines


####################################################################################################
# Expands elsets that need to be expanded (with generate statements)                               #
####################################################################################################
def expand_elset_ranges(input_lines):
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Check if the line starts with *Elset and has 'generate'
        if line.lower().startswith('*elset') and 'generate' in line.lower():
            # Remove ", generate" from the line
            line = re.sub(r',\s*generate', '', line, flags=re.IGNORECASE)
            input_lines[i] = line + '\n'
            # Move to the next line to get the range details
            next_line = input_lines[i + 1].strip()
            start, end, step = map(int, next_line.split(','))

            # Generate the range of numbers
            values = list(range(start, end + 1, step))

            # Replace the next line with the generated values in the format of 16 per line
            formatted_lines = []
            for j in range(0, len(values), 16):
                # Join the numbers with a comma
                line_values = ', '.join(map(str, values[j:j+16]))

                # If it's not the last line, append a comma at the end
                if j + 16 < len(values):  # More values to come
                    formatted_lines.append(line_values + ',\n')
                else:  # Last line, no trailing comma
                    formatted_lines.append(line_values + '\n')

            # Update the input_lines by replacing the next line with the formatted output
            input_lines[i + 1] = ''.join(formatted_lines)

        # Move to the next line
        i += 1

    if not debug_mode:
        return input_lines  # debug, remove comment to skip filtered output


#####################################################################################################
#debug to check the expanded input                                                                  #
#####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_expanded.inp"  # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)  # FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in input_lines:  # for debug
            test_output_file.write(filtered_line) # Write the filtered deck # for debug

    print("expanded written")
    return input_lines


####################################################################################################
# Creates part elsets from intersection with Referenced Elsets                                     #
####################################################################################################
def create_part_elsets(input_lines):
    placeholder_sets = {}  # Dictionary to store placeholder_elset names, element data, and TYPE
    elset_sets = {}  # Dictionary to store elset names and their element IDs
    referenced_elsets = set()  # Set to store elsets referenced in section cards
    buffer = []  # Buffer to store new lines for replacement
    placeholder_found = False  # Flag to check if any placeholder is found

    # Step 1: Collect all placeholder_elset and their element data
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Check for *ELEMENT line with placeholder_elset
        if line.lower().startswith('*element') and 'placeholder_elset_' in line.lower():
            placeholder_found = True  # Placeholder found, set the flag

            # Extract the placeholder_elset name
            placeholder_elset_name = re.search(r'placeholder_elset_\d+', line, re.IGNORECASE).group(0)

            # Extract the TYPE from the *ELEMENT line
            type_match = re.search(r'\bTYPE\s*=\s*([\w\d]+)', line, re.IGNORECASE)
            element_type = type_match.group(1) if type_match else "UNKNOWN_TYPE"

            # Determine the number of nodes based on the TYPE
            num_nodes = 1  # Default fallback
            if element_type == 'MASS':
                num_nodes = 1
            elif element_type == 'CONN3D2':
                num_nodes = 2
            elif element_type == 'S3':
                num_nodes = 3
            elif element_type == 'S3R':
                num_nodes = 3
            elif element_type == 'M3D3':
                num_nodes = 3
            elif element_type == 'R3D3':
                num_nodes = 3
            elif element_type == 'S4':
                num_nodes = 4
            elif element_type == 'S4R':
                num_nodes = 4
            elif element_type == 'R3D4':
                num_nodes = 4
            elif element_type == 'M3D4R':
                num_nodes = 4
            elif element_type == 'C3D4':
                num_nodes = 4
            elif element_type == 'C3D6':
                num_nodes = 6
            elif element_type == 'COH3D6':
                num_nodes = 6
            elif element_type == 'SC6R':
                num_nodes = 6
            elif element_type == 'SC8R':
                num_nodes = 8
            elif element_type == 'C3D8':
                num_nodes = 8
            elif element_type == 'C3D8I':
                num_nodes = 8
            elif element_type == 'COH3D8':
                num_nodes = 8
            elif element_type == 'C3D8R':
                num_nodes = 8
            elif element_type == 'C3D10':
                num_nodes = 10
            elif element_type == 'C3D10M':
                num_nodes = 10

            element_data = {}

            # Read the following lines to collect element IDs and their full data
            i += 1
            current_element_id = None
            collected_nodes = []  # To store nodes across multiple lines if needed

            while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                element_line = input_lines[i].strip()

                # Determine if the line is for an element ID or nodal data
                if current_element_id is None:
                    elements = element_line.split(',')
                    current_element_id = elements[0].strip()  # First element as ID
                    collected_nodes = elements[1:]  # Start collecting nodes

                else:
                    # Continue collecting nodal data until we reach the required number of nodes
                    collected_nodes.extend(element_line.split(','))

                # Check if we have collected enough nodes
                if len(collected_nodes) >= num_nodes:
                    # Store the full node data for this element ID
                    element_data[current_element_id] = ', '.join(collected_nodes[:num_nodes]).strip()
                    current_element_id = None  # Reset for the next element
                    collected_nodes = []  # Reset the nodes collector

                i += 1

            # Store the element data and TYPE for this placeholder_elset
            placeholder_sets[placeholder_elset_name] = {"data": element_data, "type": element_type}
        else:
            i += 1

    # If no placeholder was found, return the original input_lines
    if not placeholder_found:
        return input_lines


    # Step 2: Collect referenced elsets from *Solid Section,
    #*Shell Section, *Cohesive Section, *Membrane Section, *Connector section lines
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Check for section card lines (*Solid Section, *Shell Section, *Membrane Section)
        if re.match(r'\*(solid|shell|cohesive|membrane|connector)\s+section', line, re.IGNORECASE):
            # Extract the elset name
            elset_match = re.search(r'elset\s*=\s*([&\w\-]+)', line, re.IGNORECASE)
            if elset_match:
                elset_name = elset_match.group(1)
                referenced_elsets.add(elset_name)
                #print(f"cross reference match: {elset_name}")  # for debug
        i += 1


    # Step 3: Collect all elsets and their element IDs, but only if they are referenced
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Updated check for *ELSET line with flexible spacing
        if re.match(r'\*elset\s*,\s*elset\s*=\s*', line, re.IGNORECASE):
            # Extract the elset name
            elset_name = re.search(r'elset\s*=\s*([&\w\-]+)', line, re.IGNORECASE).group(1)

            # Only process elsets that were referenced in a section card
            if elset_name in referenced_elsets:
                element_ids = []
                # Read the following lines to collect element IDs
                i += 1
                while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                    element_ids.extend(input_lines[i].split(','))
                    i += 1

                # Store the collected element IDs for this elset
                elset_sets[elset_name] = set(el.strip() for el in element_ids)
            else:
                # Skip this elset if it wasn't referenced
                # Move to the next line to avoid re-checking the same elset
                while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                    i += 1
                # Increment i here to skip the elset line as well
                i += 1
        else:
            i += 1


    # Step 4: Find intersections between placeholder_sets and elset_sets
    for elset_name, elset_ids in elset_sets.items():
        for placeholder_name, placeholder_content in list(placeholder_sets.items()):
            placeholder_data = placeholder_content["data"]
            placeholder_type = placeholder_content["type"]

            # Find the intersection between the placeholder element IDs and the elset IDs
            placeholder_ids = set(placeholder_data.keys())
            intersection_ids = placeholder_ids.intersection(elset_ids)

            if intersection_ids:
                # Write the new *ELEMENT header with the original TYPE and the intersecting elset name
                new_element_header = f'*ELEMENT,TYPE={placeholder_type},ELSET={elset_name}\n'
                buffer.append(new_element_header)

                # Write the element data for the intersecting IDs
                for element_id in intersection_ids:
                    element_data = placeholder_data[element_id]
                    # Write all nodes on one line after the element ID
                    buffer.append(f'{element_id}, {element_data}\n')

                # Remove processed IDs from the placeholder set to avoid reprocessing
                for element_id in intersection_ids:
                    del placeholder_sets[placeholder_name]["data"][element_id]

                # If the placeholder is empty, we can remove it entirely
                if not placeholder_sets[placeholder_name]["data"]:
                    del placeholder_sets[placeholder_name]


    # Step 5: Delete all placeholder blocks and insert buffered lines
    modified_lines = []
    inside_placeholder_block = False

    i = 0
    while i < len(input_lines):
        line = input_lines[i]

        # Check if we are entering a placeholder block
        if line.lower().startswith('*element') and 'placeholder_elset_' in line.lower():
            inside_placeholder_block = True
            # Skip the current *ELEMENT line (beginning of placeholder block)

        elif inside_placeholder_block:
            # Continue skipping lines inside the placeholder block
            if line.startswith('*'):
                # We've reached the end of the placeholder block, stop skipping
                inside_placeholder_block = False
                buffer.append(line)

                # Insert the buffered lines after exiting the block (only once)
                modified_lines.extend(buffer)
                buffer = []  # Clear the buffer

            # Skip all lines within the placeholder block

        else:
            # If not inside a placeholder block, just add the line to the output
            modified_lines.append(line)

        i += 1


    if not debug_mode:
        return [line.rstrip() + '\n' for line in modified_lines] # debug, remove comment to skip filtered output

####################################################################################################
#debug to check the expanded input                                                                 #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_partcreation.inp"  # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)  # FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in modified_lines:  # for debug
            test_output_file.write(filtered_line) # Write the filtered deck # for debug

    print("partcreation written")
    return [line.rstrip() + '\n' for line in modified_lines]  # Ensure lines end with a newline


####################################################################################################
# Creates rigid elsets from intersection with Referenced Elsets                                    #
####################################################################################################
def create_rigid_elsets(input_lines):
    placeholder_rigidsets = {} # Dictionary to store placeholder_rigidelset names, element data
    rigid_elset_sets = {}  # Dictionary to store rigid elset names and their element IDs
    referenced_rigid_elsets = set()  # Set to store rigid elsets referenced in rigid cards
    rigid_buffer = [] # Buffer to store new lines for replacement
    rigid_placeholder_found = False  # Flag to check if any placeholder is found

    # Step 1 Rigid: Collect all placeholder_rigidelset and their element data
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Check for *ELEMENT line with placeholder_elset
        if line.lower().startswith('*element') and 'placeholder_rigidelset_' in line.lower():
            rigid_placeholder_found = True  # Rigid Placeholder found, set the flag

            # Extract the placeholder_elset name
            placeholder_rigidelset_name = re.search(r'placeholder_rigidelset_\d+', line, re.IGNORECASE).group(0)

            # Extract the TYPE from the *ELEMENT line
            type_match = re.search(r'\bTYPE\s*=\s*([\w\d]+)', line, re.IGNORECASE)
            element_type = type_match.group(1) if type_match else "UNKNOWN_TYPE"

            # Determine the number of nodes based on the TYPE
            num_nodes = 1  # Default fallback
            if element_type == 'MASS':
                num_nodes = 1
            elif element_type == 'CONN3D2':
                num_nodes = 2
            elif element_type == 'S3':
                num_nodes = 3
            elif element_type == 'S3R':
                num_nodes = 3
            elif element_type == 'M3D3':
                num_nodes = 3
            elif element_type == 'R3D3':
                num_nodes = 3
            elif element_type == 'S4':
                num_nodes = 4
            elif element_type == 'S4R':
                num_nodes = 4
            elif element_type == 'R3D4':
                num_nodes = 4
            elif element_type == 'M3D4R':
                num_nodes = 4
            elif element_type == 'C3D4':
                num_nodes = 4
            elif element_type == 'C3D6':
                num_nodes = 6
            elif element_type == 'COH3D6':
                num_nodes = 6
            elif element_type == 'SC6R':
                num_nodes = 6
            elif element_type == 'SC8R':
                num_nodes = 8
            elif element_type == 'C3D8':
                num_nodes = 8
            elif element_type == 'C3D8I':
                num_nodes = 8
            elif element_type == 'COH3D8':
                num_nodes = 8
            elif element_type == 'C3D8R':
                num_nodes = 8
            elif element_type == 'C3D10':
                num_nodes = 10
            elif element_type == 'C3D10M':
                num_nodes = 10

            element_data = {}

            # Read the following lines to collect element IDs and their full data
            i += 1
            current_element_id = None
            collected_nodes = []  # To store nodes across multiple lines if needed

            while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                element_line = input_lines[i].strip()

                # Determine if the line is for an element ID or nodal data
                if current_element_id is None:
                    elements = element_line.split(',')
                    current_element_id = elements[0].strip()  # First element as ID
                    collected_nodes = elements[1:]  # Start collecting nodes

                else:
                    # Continue collecting nodal data until we reach the required number of nodes
                    collected_nodes.extend(element_line.split(','))

                # Check if we have collected enough nodes
                if len(collected_nodes) >= num_nodes:
                    # Store the full node data for this element ID
                    element_data[current_element_id] = ', '.join(collected_nodes[:num_nodes]).strip()
                    current_element_id = None  # Reset for the next element
                    collected_nodes = []  # Reset the nodes collector

                i += 1

            # Store the element data and TYPE for this placeholder_elset
            placeholder_rigidsets[placeholder_rigidelset_name] = {"data": element_data, "type": element_type}
        else:
            i += 1

    # If no placeholder was found, return the original input_lines
    if not rigid_placeholder_found:
        return input_lines


    # Step 2 Rigid: For Rigid Elements, Collect referenced elsets from *Rigid Body lines
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Check for rigid body card lines (*Rigid Body)
        if re.match(r'^\s*\*rigid body\b', line, re.IGNORECASE):
            elset_pattern = r'\bELSET\s*=\s*([\w\-+/ ]+)'  # Flexible matching for 'elset=' or 'elset ='
            rigid_body_match = re.search(elset_pattern, line, re.IGNORECASE)
            if rigid_body_match:
                elset_name = rigid_body_match.group(1).strip()
                referenced_rigid_elsets.add(elset_name)
        i += 1


   # Step 3 Rigid: Collect all Rigid elsets and their element IDs, but only if they are referenced
    i = 0
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Updated check for *ELSET line with flexible spacing
        if re.match(r'\*elset\s*,\s*elset\s*=\s*', line, re.IGNORECASE):
            # Extract the elset name
            elset_name = re.search(r'\bELSET\s*=\s*([\w\-+/]+)', line, re.IGNORECASE).group(1)
            # Only process elsets that were referenced in a rigid body
            if elset_name in referenced_rigid_elsets:
                element_ids = []
                # Read the following lines to collect element IDs
                i += 1
                while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                    element_ids.extend(input_lines[i].split(','))
                    i += 1

                # Store the collected element IDs for this elset
                rigid_elset_sets[elset_name] = set(el.strip() for el in element_ids)
            else:
                # Skip this elset if it wasn't referenced
                # Move to the next line to avoid re-checking the same elset
                while i < len(input_lines) and not input_lines[i].strip().startswith('*'):
                    i += 1
                # Increment i here to skip the elset line as well
                i += 1
        else:
            i += 1


    # Step 4 Rigid: Find intersections between placeholder_rigidsets and rigid_elset_sets
    for elset_name, elset_ids in rigid_elset_sets.items():
        for placeholder_name, placeholder_content in list(placeholder_rigidsets.items()):
            placeholder_data = placeholder_content["data"]
            placeholder_type = placeholder_content["type"]

            # Find the intersection between the placeholder element IDs and the elset IDs
            placeholder_ids = set(placeholder_data.keys())
            intersection_ids = placeholder_ids.intersection(elset_ids)

            if intersection_ids:
                # Write the new *ELEMENT header with the original TYPE and the intersecting elset name
                new_element_header = f'*ELEMENT,TYPE={placeholder_type},ELSET={elset_name}\n'
                rigid_buffer.append(new_element_header)

                # Write the element data for the intersecting IDs
                for element_id in intersection_ids:
                    element_data = placeholder_data[element_id]
                    # Write all nodes on one line after the element ID
                    rigid_buffer.append(f'{element_id}, {element_data}\n')

                # Remove processed IDs from the placeholder set to avoid reprocessing
                for element_id in intersection_ids:
                    del placeholder_rigidsets[placeholder_name]["data"][element_id]

                # If the placeholder is empty, we can remove it entirely
                if not placeholder_rigidsets[placeholder_name]["data"]:
                    del placeholder_rigidsets[placeholder_name]

    # Step 5 Rigid: Delete all rigid_placeholder blocks and insert buffered lines
    modified_rigid_lines = []
    inside_rigid_placeholder_block = False

    i = 0
    while i < len(input_lines):
        line = input_lines[i]

        # Check if we are entering a placeholder block
        if line.lower().startswith('*element') and 'placeholder_rigidelset_' in line.lower():
            inside_rigid_placeholder_block = True
            # Skip the current *ELEMENT line (beginning of placeholder block)

        elif inside_rigid_placeholder_block:
            # Continue skipping lines inside the placeholder block
            if line.startswith('*'):
                # We've reached the end of the placeholder block, stop skipping
                inside_rigid_placeholder_block = False
                rigid_buffer.append(line)

                modified_rigid_lines.extend(rigid_buffer)
                rigid_buffer = []  # Clear the buffer

            # Skip all lines within the placeholder block

        else:
            # If not inside a placeholder block, just add the line to the output
            modified_rigid_lines.append(line)

        i += 1


    if not debug_mode:
        return [line.rstrip() + '\n' for line in modified_rigid_lines]  # debug, remove comment to skip filtered output

####################################################################################################
#debug to check the rigid expanded input                                                           #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_rigidpartcreation.inp" # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)   # FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in modified_rigid_lines:  # for debug
            test_output_file.write(filtered_line) # Write the filtered deck # for debug

    print("rigid partcreation written")
    return [line.rstrip() + '\n' for line in modified_rigid_lines]  # Ensure lines end with a newline


####################################################################################################
# update input lines format for ppm rigid bodies with rot node                                     #
####################################################################################################
def ppm_rigids(input_lines):

    modified_ppm_lines = []
    rotref_substitute = []

    # Step 1 Find Rigids with Rot Node
    i = 0
    while i < len(input_lines):
        line = input_lines[i]

        if line.lower().strip().startswith('*rigid body'):

            #this is to find ref_node
            rbody_id_pattern = r'ref\s*node\s*=\s*([^,]+)'
            rbody_id_match = re.search(rbody_id_pattern, line, re.IGNORECASE)

            #this is to find ppm calculix rot_node and call def to convert input format to .inp ref node
            rbody_rotid_pattern = r'rot\s*node\s*=\s*([^,]+)'
            rbody_rotid_match = re.search(rbody_rotid_pattern, line, re.IGNORECASE)

            if rbody_rotid_match:
                rbody_rotid = rbody_rotid_match.group(1).strip()
                rbody_id = rbody_id_match.group(1).strip()

                rotref_substitute.append((rbody_rotid, rbody_id))

                i += 1

            else:
                i += 1

        else:
            i += 1
    # If no rot_nodes were found, return original lines
    if not rotref_substitute:
        return input_lines


    # Step 2: Parse Boundary and Cload Sections and modify if necessary
    section = None
    i = 0
    while i < len(input_lines):
        line = input_lines[i]

        # Check for boundary or cload section
        if line.lower().startswith("*boundary") :
            section = "*boundary"
            modified_ppm_lines.append(line)

        elif line.lower().startswith("*cload"):
            section = "*cload"
            modified_ppm_lines.append(line)

        elif line.startswith("*"):
            section = None
            modified_ppm_lines.append(line)

        elif section == "*boundary" and not line.startswith("*"):
            fields = line.split(',')
            fields = [f.strip() for f in fields]  # Clean up any extra whitespace

            if len(fields) >= 2:
                boundary_name = fields[0]  # First field
                boundary_dir1 = int(fields[1])  # Second field
                # Set the 3rd field to the 2nd field if it's empty
                boundary_dir2 = int(fields[2]) if len(fields) >= 3 and fields[2] != '' else boundary_dir1
                # Generate the list of directions for BCS (range between dir1 and dir2)
                impd_val = fields[3] if len(fields) >= 4 and fields[3] else "0.0"

                # Check if boundary_name matches any in rotref_substitute and apply substitution
                for rot_node, ref_node in rotref_substitute:
                    if boundary_name == rot_node:
                        boundary_name = ref_node  # Substitute the ref_node for rot_node if matched
                        boundary_dir1 += 3
                        boundary_dir2 += 3
                        break  # Stop after first match

                # Store the modified boundary line in the desired format
                modified_line = f"{boundary_name}, {boundary_dir1}, {boundary_dir2}, {impd_val}\n"
                modified_ppm_lines.append(modified_line)

        elif section == "*cload" and not line.startswith("*"):
            fields = line.split(',')
            fields = [f.strip() for f in fields]  # Clean up any extra whitespace

            if len(fields) >= 3:
                cload_name = fields[0]  # First field
                cload_dir = int(fields[1])  # Second field
                cload_val = fields[2].strip() if fields[2] != '' else "0.0"  # Set 3rd field to 0.0 if empty

                # Check if cload_name matches any in rotref_substitute and apply substitution
                for rot_node, ref_node in rotref_substitute:
                    if cload_name == rot_node:
                        cload_name = ref_node  # Substitute the ref_node for rot_node if matched
                        cload_dir += 3
                        break  # Stop after first match

                # Store the modified boundary line in the desired format
                modified_line = f"{cload_name}, {cload_dir}, {cload_val}\n"
                modified_ppm_lines.append(modified_line)


        # Store lines that aren't part of a specific section unchanged
        else:
            modified_ppm_lines.append(line)

        i += 1

    if not debug_mode:
        return [line.rstrip() + '\n' for line in modified_ppm_lines] # debug, remove comment to skip filtered output


####################################################################################################
#debug to check the rigid expanded input                                                           #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_rotnode_substitutions.inp" # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)  # FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:    # for debug
        for filtered_line in modified_ppm_lines:  # for debug
            test_output_file.write(filtered_line) # Write the filtered deck # for debug

    print("rotnode subs written")
    return [line.rstrip() + '\n' for line in modified_ppm_lines]  # Ensure lines end with a newline


####################################################################################################
# find referenced elsets (reference other elsets by name)                                          #
####################################################################################################
def find_referenced_elsets(input_lines):
    elset_references = {}
    non_numeric_references = {}
    i = 0

    # Step 1: Collect initial elset references
    while i < len(input_lines):
        line = input_lines[i].strip()

        # Match *ELSET line pattern
        elset_pattern = r'^\s*\*elset\s*,\s*elset\s*=\s*([\w\-/ ]+)(?:\s*,\s*.+)?$'
        elset_match = re.search(elset_pattern, line, re.IGNORECASE)

        if elset_match:
            parent_elset = elset_match.group(1).strip()
            # Move to the next lines to collect referenced elsets
            j = i + 1
            referenced_elsets = []
            non_numeric_items = []
            while j < len(input_lines) and input_lines[j].strip() and not input_lines[j].startswith('*'):
                referenced_line = input_lines[j].strip()
                # Split the line into individual items by commas
                referenced_elset_items = [item.strip() for item in referenced_line.split(',') if item.strip()]
                # Add items (numbers or elset names) to the list
                referenced_elsets.extend(referenced_elset_items)
                # Collect non-numeric items
                non_numeric_items.extend([item for item in referenced_elset_items if not item.isdigit()])
                j += 1

            # Store the initial references in the dictionary
            elset_references[parent_elset] = referenced_elsets
            # Store the non-numeric references in the second dictionary
            non_numeric_references[parent_elset] = non_numeric_items

        i += 1

    # Step 2: Resolve all references so each elset only contains numbers
    def resolve_elset(elset_name):

        resolved_values = []
        for item in elset_references.get(elset_name, []):
            # Check if item is already an integer
            if isinstance(item, int):
                resolved_values.append(item)
            # If it's a string representation of a number, convert it to an integer
            elif item.isdigit():
                resolved_values.append(int(item))
            else:  # Another elset name, resolve it recursively
                #input(f"this is the item: {item}")
                if item != elset_name:
                    resolved_values.extend(resolve_elset(item))  # Recursively resolve

        # Update the current elset with resolved numeric values only (keeps duplicates for each set)
        elset_references[elset_name] = resolved_values
        return resolved_values

    # Step 3: Resolve all elsets in the dictionary
    for elset_name in list(elset_references.keys()):
        resolve_elset(elset_name)
    elset_references = {name: values for name, values in elset_references.items() if any(isinstance(v, int) for v in values)}
    non_numeric_references = {k: v for k, v in non_numeric_references.items() if v}
    #print(elset_references)
    return elset_references, non_numeric_references


####################################################################################################
# find referenced nsets (reference other nsets by name)                                            #
####################################################################################################
def find_referenced_nsets(input_lines):
    nset_references = {}
    i = 0

    while i < len(input_lines):
        line = input_lines[i].strip()

        # Match *NSET line pattern
        nset_pattern = r'^\s*\*nset\s*,\s*nset\s*=\s*([^,]+)(?:\s*,\s*.+)?$'
        nset_match = re.search(nset_pattern, line, re.IGNORECASE)

        if nset_match:
            parent_nset = nset_match.group(1).strip()  # The main ELSET name

            # Move to the next lines to collect referenced nsets
            j = i + 1
            referenced_nsets = []
            while j < len(input_lines) and input_lines[j].strip() and not input_lines[j].startswith('*'):
                # Collect the referenced elset lines, which might be comma-separated
                referenced_line = input_lines[j].strip()

                # Split the line into individual items by commas
                referenced_nset_items = [item.strip() for item in referenced_line.split(',') if item.strip()]

                # Add non-self-referenced items to the list
                referenced_nsets.extend([nset for nset in referenced_nset_items if nset != parent_nset and not nset.isdigit()])

                j += 1

            # Store the references in a dictionary
            if referenced_nsets:
                nset_references[parent_nset] = referenced_nsets

        i += 1

    return nset_references


####################################################################################################
# replace referenced elsets (reference other elsets by name)                                       #
####################################################################################################
def replace_elsets_in_sections(input_lines, elset_references):
    elsets_for_expansion_dict = {}
    relsets_for_expansion_dict = {}
    for parents, elements in elset_references.items():
        elsets_for_expansion_dict[parents] = elements
        relsets_for_expansion_dict[parents] = elements

    if not debug_mode:
        return input_lines, elsets_for_expansion_dict, relsets_for_expansion_dict # debug, remove comment to skip filtered input


####################################################################################################
#debug to check the filtered input                                                                 #
####################################################################################################
    output_filter = os.path.splitext(input_file_name)[0] + "_test_filter.inp"  # FOR DEBUG
    output_filter_path = os.path.join(os.path.dirname(input_file_path), output_filter)  # FOR DEBUG

    with open(output_filter_path, "w") as test_output_file:
        for parents, elset_names in elsets_for_expansion_dict.items():
            test_output_file.write(f"{parents}\n")       # Write `parents` with newline
            test_output_file.write(f"{elset_names}\n")   # Write `elset_names` with newline

    print("filter written")
    return input_lines, elsets_for_expansion_dict, relsets_for_expansion_dict


####################################################################################################
# Call the main_conversion function to get the necessary data from the conversion blocks           #
####################################################################################################
####################################################################################################
# Get input file                                                                                   #
####################################################################################################
def start(input_file_path):
    try:
        (original_lines, input_file_name, simple_file_name, output_file_name, output_file_path,
         engine_file_name, engine_file_path) = input_read(input_file_path)

####################################################################################################
# Prepare input file (removes comments, special characters)                                        #
####################################################################################################
        input_lines = preprocess_lines(original_lines)
        input_lines = expand_elset_ranges(input_lines)
        elset_references, non_numeric_references = find_referenced_elsets(input_lines)
        nset_references = find_referenced_nsets(input_lines)
        input_lines = create_part_elsets(input_lines)
        input_lines = create_rigid_elsets(input_lines)
        input_lines = ppm_rigids(input_lines)
        (input_lines, elsets_for_expansion_dict, relsets_for_expansion_dict
         ) = replace_elsets_in_sections(input_lines, elset_references)

####################################################################################################
# Call the main_conversion function to get the necessary data from the conversion blocks           #
####################################################################################################
        (transform_lines, transform_data, node_lines, nsets, nset_blocks, material_names,
         property_names, ppmselect, element_lines, elset_blocks, surface_lines, contacts,
         tied_contacts, boundary_blocks, function_blocks, initial_blocks, dload_blocks,
         rigid_bodies, couplings, discoups, mpc_ties, conn_beams, engine_file
         ) = main_conversion_sp(input_lines, simple_file_name, elsets_for_expansion_dict,
         non_numeric_references, relsets_for_expansion_dict, nset_references
         )

####################################################################################################
# Call the output function to write data to Radioss from the conversion blocks                     #
####################################################################################################
        output_done = write_output(transform_lines, transform_data, node_lines, nset_blocks,
                                   material_names, property_names, ppmselect,
                                   non_numeric_references, nsets, element_lines, elset_blocks,
                                   surface_lines, contacts, tied_contacts, boundary_blocks,
                                   function_blocks, initial_blocks, dload_blocks, rigid_bodies,
                                   couplings, discoups, mpc_ties, conn_beams, engine_file,
                                   simple_file_name, output_file_name, output_file_path,
                                   engine_file_name, engine_file_path
                                   )

####################################################################################################
# Return Status (True if script completed )                                                        #
####################################################################################################
        return output_done

    except Exception as e:
        # Log the error and return failure
        print("------------------------------------------------------------")
        print(f"Error in inp2rad: {e}")
        return False


def execute_gui(input_deck,tm):
    input_file_path=input_deck
    run_timer = tm
    or_gui = True    # When run in Batch mode, avoids interaction.
    try:
        # Call the start function and capture its return value
        success = start(input_file_path)
        return success
    except Exception as e:
        # Handle unexpected exceptions
        return False

if __name__ == "__main__":

#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  FOR Subprocess based INPUT (called from command line or OpenRadioss gui submission tool)
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
    if len (sys.argv) == 1:
        root = tk.Tk()
        root.withdraw()

        input_file_path = filedialog.askopenfilename(
            title="Select Input File", filetypes=[(".inp File", "*.inp")])

        if not input_file_path:
            print("No input file selected. Exiting...")
            sys.exit()
        or_gui = False
        run_timer = True

    # take input file from OpenRadioss special submission gui version
    elif len(sys.argv) >= 2:
        parser = argparse.ArgumentParser(description="A2R Converter")
        parser.add_argument('input_file', nargs='?', help="Path to the input file")
        parser.add_argument('--timer', '-t', action='store_true', help="Run with timer")
        args = parser.parse_args()

        or_gui = True    # When run in Batch mode, avoids interaction.
        run_timer = args.timer
        input_file_path = args.input_file
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
#-  FOR SELF CONTAINED INPUT (opens a file browser if script is called without file argument)
#---1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|
    start(input_file_path)
