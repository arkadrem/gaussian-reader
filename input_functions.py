import pandas as pd

import matrix_conversion


def open_input(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = pd.DataFrame({'line': lines})
    return data


def memory(input_file):
    data = open_input(input_file)
    mem_lines = data[data['line'].str.startswith('%mem')]
    if mem_lines.empty:
        return "Default"
    else:
        mem_values = mem_lines['line'].str.split('=').str[1].str.strip()
        return mem_values.iloc[0] if not mem_values.empty else None


def checkpoint(input_file):
    data = open_input(input_file)
    chk_lines = data[data['line'].str.startswith('%chk')]
    if chk_lines.empty:
        return "There is no checkpoint file"
    else:
        chk_values = chk_lines['line'].str.split('=').str[1].str.strip()
        return chk_values.iloc[0] if not chk_values.empty else None


def options(input_file):
    data = open_input(input_file)
    p_lines = data[data['line'].str.startswith('#')]
    return p_lines['line'].str.strip().str[2:].iat[0] if not p_lines.empty else None


def comment(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']

    if len(empty_lines) >= 2:
        start_index = empty_lines[0] + 1
        end_index = empty_lines[1]
        comment_line = lines[start_index:end_index]
        print(comment_line)
        return ''.join(comment_line).strip()
    else:
        return None


def charge(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']

    if len(empty_lines) >= 2:
        start_index = empty_lines[1] + 1
        end_index = empty_lines[2] if len(empty_lines) >= 3 else len(lines)
        state = lines[start_index:end_index]

        separate_strings = state[0].split()
        return separate_strings[0] if separate_strings else None
    else:
        return None


def multiplicity(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']

    if len(empty_lines) >= 2:
        start_index = empty_lines[1] + 1
        end_index = empty_lines[2] if len(empty_lines) >= 3 else len(lines)
        state = lines[start_index:end_index]

        separate_strings = state[0].split()
        return separate_strings[1] if separate_strings else None
    else:
        return None


def coordinates(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']

    if len(empty_lines) >= 2:
        start_index = empty_lines[1] + 1
        end_index = empty_lines[2] if len(empty_lines) >= 3 else len(lines)
        state = lines[start_index:end_index]

        if len(state) > 1:
            next_line = state[1]
            split_next_line = next_line.split(" " or '\t')
            if len(split_next_line) > 1:
                atoms, x, y, z = input_coordinates(state)
                atoms = ", ".join(atoms)
                print(atoms)
                return f"Type: Cartesian coordinates\nAtoms: {atoms}\nx: {x}\ny: {y}\nz: {z}"
            else:
                divided_matrix_array = matrix_conversion.matrix_read(state)
                dictionary = matrix_conversion.matrix_dictionary(empty_lines, lines)
                matrix_without_constants = matrix_conversion.matrix_without_constants(divided_matrix_array, dictionary)
                atom_names, r_atom, r_value, a_atom, a_value, d_atom, d_value = \
                    matrix_conversion.matrix_in_arrays(matrix_without_constants)
                x, y, z, atoms = matrix_conversion.write_xyz(atom_names, r_atom, r_value, a_atom, a_value, d_atom,
                                                             d_value)

                return f"Type: internal coordinates\nAtoms: {atoms}\nx: {x}\ny: {y}\nz: {z}"

    return None


def input_coordinates(state):
    cartesian_array = []
    for line in state[1:]:
        line = line.strip()
        if line != '':
            split_elements = [elem.strip() for elem in line.split("\t")]
            cartesian_array.append(split_elements)

    atoms = []
    x = []
    y = []
    z = []

    for i in cartesian_array:
        split_indices = [elem.strip() for elem in i[0].split()]
        atoms.append(split_indices[0])
        x.append(float(split_indices[1]))
        y.append(float(split_indices[2]))
        z.append(float(split_indices[3]))

    return atoms, x, y, z
