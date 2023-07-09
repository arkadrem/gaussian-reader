import re
import pandas as pd


def open_output(output_file):
    with open(output_file, 'r') as file:
        lines = file.readlines()

    data = pd.DataFrame({'line': lines})
    return data


def scf(output_file):
    with open(output_file, 'r') as file:
        lines = file.readlines()

    scf_pattern = r'SCF Done:  E\((\w+)\) =  (-?\d+\.\d+)'
    content = ''.join(lines)
    matches = re.findall(scf_pattern, content)

    scf_list = [float(match[1]) for match in matches]

    return scf_list


def molecule_energy(output_file):
    scf_list = scf(output_file)
    energy = scf_list[-1]
    energy_h = round(energy, 3)
    energy_kj = round(energy * 2625.4996394799, 3)
    return f"{energy_h} a.u. = {energy_kj} kJ/mol"


def thermochemistry(output_file):
    data = open_output(output_file)
    temp_press_regex = r'Temperature\s+(\d+\.\d+)\s+Kelvin\.\s+Pressure\s+(\d+\.\d+)\s+Atm\.'

    match = data['line'].str.extract(temp_press_regex, expand=False).dropna().astype(float)
    if match.empty:
        return None

    temperature = match.iloc[0, 0]
    pressure = match.iloc[0, 1]

    mass_regex = r'Molecular mass:\s+(\d+\.\d+)\s+amu\.'
    molecular_mass = data['line'].str.extract(mass_regex, expand=False).dropna().astype(float).iloc[0]

    temperature_c = temperature - 273.15
    pressure_pa = pressure * 101325

    return f"Temperature: {temperature_c} C\nPressure: {pressure_pa} Pa\nMass of molecule: {molecular_mass} a.u."


def frequencies(output_file):
    data = open_output(output_file)
    freq_lines = data[data['line'].str.startswith(' Frequencies --')]['line']
    freq_list = []

    for line in freq_lines:
        info = line.split('Frequencies --')[1].strip().split()
        freq_list.extend(info)

    freq_list = freq_list[len(freq_list) // 2:]
    return f"{freq_list}" if freq_list else None


def optimized_coordinates(output_file):
    data = open_output(output_file)
    lines = data['line']

    start_indexes = [i + 4 for i, line in enumerate(lines) if 'Input orientation' in line]

    lines_after_list = []

    for start_index in start_indexes:
        lines_after = []
        for line in lines[start_index + 1:]:
            if line.startswith(' --------'):
                break
            else:
                lines_after.append(line.strip())
        lines_after_list.append(lines_after)

    coordinates_list = []

    for array in lines_after_list:
        nested_array = [[word] for word in array]
        split_array = [[word for word in sublist[0].split()] for sublist in nested_array]
        modified_array = [sublist[3:] for sublist in split_array]

        x_array = [float(sublist[0]) for sublist in modified_array]
        y_array = [float(sublist[1]) for sublist in modified_array]
        z_array = [float(sublist[2]) for sublist in modified_array]

        coordinates_list.append((x_array, y_array, z_array))

    return coordinates_list


def latest_coordinates(output_file):
    coordinates_list = optimized_coordinates(output_file)
    last_coordinates = coordinates_list[-1]
    return f"x: {last_coordinates[0]}\ny: {last_coordinates[1]}" \
           f"\nz: {last_coordinates[2]}"


def joke(output):
    with open(output, 'r') as file:
        lines = file.readlines()

    lines.reverse()
    name = None
    quote = []
    lines_iter = iter(lines)

    for line in lines_iter:
        if line.startswith(' Job cpu time'):
            name = next(lines_iter).strip()
            next_line = next(lines_iter).strip()
            if next_line:
                quote.append(next_line)
            for line in lines_iter:
                if line.strip() == '':
                    break
                quote.append(line.strip())
            break

    quote.reverse()
    quote = " ".join(quote)
    lines.reverse()

    return f"{quote}\n {name}"
