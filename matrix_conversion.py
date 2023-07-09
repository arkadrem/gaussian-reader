import numpy as np
import re


def matrix_read(state):
    matrix_array = []
    for line in state[1:]:
        line = line.strip()
        if line != '':
            split_elements = [elem.strip() for elem in line.split("\t")]
            matrix_array.append(split_elements)

    divided_matrix_array = []

    for array in matrix_array:
        divided_subarray = []

        for string in array:
            if " " in string:
                divided_subarray.extend(string.split(" "))
            else:
                divided_subarray.append(string)

        divided_matrix_array.append(divided_subarray)

    return divided_matrix_array


def matrix_dictionary(empty_lines, lines):
    empty_line_index = empty_lines[2] + 1 if len(empty_lines) >= 3 else len(lines)

    constants = [line.strip() for line in lines[empty_line_index:] if line.strip() != '']

    dictionary = {}

    for item in constants:
        key, value = item.split('=')
        key = key.strip()
        value = value.strip()
        if key != "" and value != "":
            dictionary[key] = float(value)

    return dictionary


def matrix_without_constants(matrix_without_constants, dictionary):
    for subarray in matrix_without_constants:
        for i in range(len(subarray)):
            if subarray[i] in dictionary:
                subarray[i] = dictionary[subarray[i]]

    return matrix_without_constants


def matrix_in_arrays(matrix_without_constants):
    atom_names = []
    r_atom = []
    r_value = []
    a_atom = []
    a_value = []
    d_atom = []
    d_value = []

    for subarray in matrix_without_constants:
        atom_names.append(subarray[0])

        for element in subarray[1:]:
            try:
                float_value = float(element)
            except ValueError:
                continue

            if subarray.index(element) == 1:
                r_atom.append(int(float_value))
            elif subarray.index(element) == 2:
                r_value.append(float_value)
            elif subarray.index(element) == 3:
                a_atom.append(int(float_value))
            elif subarray.index(element) == 4:
                a_value.append(float_value)
            elif subarray.index(element) == 5:
                d_atom.append(int(float_value))
            elif subarray.index(element) == 6:
                d_value.append(float_value)

    return atom_names, r_atom, r_value, a_atom, a_value, d_atom, d_value


def extract_elements(arrays):
    extracted_arrays = list(zip(*arrays))
    return extracted_arrays


def write_xyz(atom_names, r_atom, r_value, a_atom, a_value, d_atom, d_value):
    npart = len(atom_names)

    # first atom at the origin
    xyz_arr = np.zeros([npart, 3])
    if npart > 1:
        # second atom at [r01, 0, 0]
        xyz_arr[1] = [r_value[0], 0.0, 0.0]

    if npart > 2:
        # third atom in the xy-plane
        i = r_atom[1] - 1
        j = a_atom[0] - 1
        r = r_value[1]
        theta = a_value[0] * np.pi / 180.0
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        a_i = xyz_arr[i]
        b_ij = xyz_arr[j] - xyz_arr[i]
        if b_ij[0] < 0:
            x = a_i[0] - x
            y = a_i[1] - y
        else:
            x = a_i[0] + x
            y = a_i[1] + y
        xyz_arr[2] = [x, y, 0.0]

    for n in range(3, npart):
        # xyz coordinates, from the positions of the last three atoms
        r = r_value[n - 1]
        theta = a_value[n - 2] * np.pi / 180.0
        phi = d_value[n - 3] * np.pi / 180.0

        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        sin_phi = np.sin(phi)
        cos_phi = np.cos(phi)

        x = r * cos_theta
        y = r * cos_phi * sin_theta
        z = r * sin_phi * sin_theta

        i = r_atom[n - 1] - 1
        j = a_atom[n - 2] - 1
        k = d_atom[n - 3] - 1
        a = xyz_arr[k]
        b = xyz_arr[j]
        c = xyz_arr[i]

        ab = b - a
        bc = c - b
        bc = bc / np.linalg.norm(bc)
        nv = np.cross(ab, bc)
        nv = nv / np.linalg.norm(nv)
        ncbc = np.cross(nv, bc)

        new_x = c[0] - bc[0] * x + ncbc[0] * y + nv[0] * z
        new_y = c[1] - bc[1] * x + ncbc[1] * y + nv[1] * z
        new_z = c[2] - bc[2] * x + ncbc[2] * y + nv[2] * z
        xyz_arr[n] = [new_x, new_y, new_z]

    extracted_arrays = extract_elements(xyz_arr)
    x = extracted_arrays[0]
    y = extracted_arrays[1]
    z = extracted_arrays[2]
    atoms = [re.sub(r'\d', '', string) for string in atom_names]

    indices_to_remove = []

    for i, element in enumerate(atoms):
        if element == "X":
            indices_to_remove.append(i)

    atoms = list(atoms)
    x = list(x)
    y = list(y)
    z = list(z)

    for index in sorted(indices_to_remove, reverse=True):
        del atoms[index]
        del x[index]
        del y[index]
        del z[index]

    x = [round(element, 3) for element in x]
    y = [round(element, 3) for element in y]
    z = [round(element, 3) for element in z]

    return x, y, z, atoms
