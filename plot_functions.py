import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance
import numpy as np

import matrix_conversion
from input_functions import input_coordinates
from output_functions import scf, optimized_coordinates


def general_plot(atoms, x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z)

    coordinates = np.column_stack((x, y, z))
    dist_matrix = distance.cdist(coordinates, coordinates)

    num_points = len(x)
    for i in range(num_points):
        closest_point_index = np.argsort(dist_matrix[i])[1]  # Exclude the point itself
        ax.plot([x[i], x[closest_point_index]], [y[i], y[closest_point_index]],
                [z[i], z[closest_point_index]], 'k-', linewidth=0.5)

    for xi, yi, zi, label in zip(x, y, z, atoms):
        ax.text(xi, yi, zi, label, color='red')

    ax.set_xlabel('x [Å]')
    ax.set_ylabel('y [Å]')
    ax.set_zlabel('z [Å]')
    ax.set_title('Molecule')
    plt.show()


def input_plot_coordinates(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']

    if len(empty_lines) >= 2:
        start_index = empty_lines[1] + 1
        end_index = empty_lines[2] if len(empty_lines) >= 3 else len(lines)
        state = lines[start_index:end_index]

        if len(state) > 1:
            next_line = state[1]
            split_next_line = next_line.split(" ")
            if len(split_next_line) > 1:
                atoms, x, y, z = input_coordinates(state)
            else:
                divided_matrix_array = matrix_conversion.matrix_read(state)
                dictionary = matrix_conversion.matrix_dictionary(empty_lines, lines)
                matrix_without_constants = matrix_conversion.matrix_without_constants(divided_matrix_array, dictionary)
                atom_names, r_atom, r_value, a_atom, a_value, d_atom, d_value = \
                    matrix_conversion.matrix_in_arrays(matrix_without_constants)
                x, y, z, atoms = matrix_conversion.write_xyz(atom_names, r_atom, r_value, a_atom, a_value, d_atom,
                                                             d_value)

    return atoms, x, y, z


def original_molecule(input_file):
    atoms, x, y, z = input_plot_coordinates(input_file)

    general_plot(atoms, x, y, z)



def energy_plot(output_file):
    scf_list = scf(output_file)
    indices = range(len(scf_list))

    plt.plot(indices, scf_list)
    plt.xlabel('Step')
    plt.ylabel('Energy [a. u.]')
    plt.title('Energy of molecule')

    # Add annotations for the first and last points
    plt.text(indices[0], scf_list[0], f'{scf_list[0]:.2f}', ha='right', va='bottom')
    plt.text(indices[-1], scf_list[-1], f'{scf_list[-1]:.2f}', ha='left', va='top')

    plt.show()



def optimized_molecule(input_file, output_file):
    atoms = input_plot_coordinates(input_file)
    atoms = atoms[0]

    coordinates_list = optimized_coordinates(output_file)
    coordinates = coordinates_list[-1]

    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]

    general_plot(atoms, x, y, z)
