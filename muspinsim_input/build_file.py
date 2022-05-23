import json
import sys
import re
from muspinsim import MuSpinInput

def write_file(file_name, content):
    """
    Write muspinsim file
    :param file_name: name of file
    :param content: list of strings containing blocks to write
    """
    with open(file_name, "w") as f:
        f.write(
            """
#######################################################
#Muspinsim Input File
#Generated using Muon Galaxy Tool Muspinsim_Input
#######################################################\n\n"""
        )
        f.write("".join(content))


def build_block(title, vals):
    """
    Build keyword block
    :param title: string - Keyword
    :param vals: list of strings - lines containing values for keyword
    :return: A string containing formatted keyword block
    """
    return "{0}\n    {1}\n".format(title, "\n    ".join(vals))

def remove_bracket_whitespace(entry):
    stck = []
    new_str = ""
    for i, char in enumerate(entry):
        if char == '(':
            stck.append(i)
        elif char == ')':
            if len(stck) == 0:
                raise ValueError(
                    "Could not parse entry {0}"
                    "brackets mismatch - unexpected ')' found on char {1}".format(entry, i)
                )
            stck.pop()
        elif char == ' ':
            if len(stck) > 0:
                continue
        new_str += char

    if len(stck) != 0:
        raise ValueError(
            "Could not parse entry {0}"
            "brackets mismatch - unclosed '(' found on char(s): {1}".format(entry, stck)
        )
    return new_str

def split_into_args(entry, nargs=1):
    """
    Helper function to split input into a list of args
    :param entry: a string containing a user inputted line
    :param nargs: number of expected arguments
    :return: a list of arguments found
    :exception: ValueError - if number of arguments found does not match expected (nargs)
    """

    # remove square brackets and extra whitespace/newline
    content = " ".join(entry.replace("[", "").replace("]", "").split())

    # remove whitespace in between expressions/functions
    # split on whitespace to separate args

    content = re.split(r"\s", remove_bracket_whitespace(content))
    chars = [elem.strip() for elem in content if elem != ""]
    if len(chars) != nargs:
        raise ValueError(
            "Could not parse entry {0}"
            " incorrect number of args"
            " found {1}:\n({2})\nBut expected {3}".format(entry, len(chars), chars, nargs)
        )
    return chars


def parse_matrix(entry_string, size):
    """
    Helper function to parse and format matrix/vector to be readable by Muspinsim
    :param entry_string: a user input string for a matrix/vector
    :param size: (x, y) integer tuple: dimensions of matrix
    :return: a list of strings of length y, each string containing x elements (space separated)
    """
    content = split_into_args(entry_string, nargs=size[0] * size[1])
    return [" ".join(content[x : x + size[0]]) for x in range(0, len(content), size[0])]


def parse_interactions(interaction):
    """
    Helper function to build keyword blocks for all interaction parameters entered
        (hyperfine, zeeman, dipolar, quadrupolar and dissipation)

    :param interaction: a dictionary containing all interaction parameters
    :return: a string containing several formatted blocks
    """

    options = interaction["interaction_options"]
    interaction_type = options["interaction"]
    try:
        return {
            "zeeman": lambda options: build_block(
                "zeeman {0}".format(options["zeeman_index"]),
                parse_matrix(options["zeeman_vector"], (3, 1)),
            ),
            "hyperfine": lambda options: build_block(
                "hyperfine {0} {1}".format(
                    options["hfine_index"],
                    options["hfine_e_index"] if options["hfine_e_index"] else "",
                ).strip(),
                parse_matrix(options["hfine_matrix"], (3, 3)),
            ),
            "dipolar": lambda options: build_block(
                "dipolar {0} {1}".format(options["di_index"], options["di_index_2"]),
                parse_matrix(options["di_vector"], (3, 1)),
            ),
            "quadrupolar": lambda options: build_block(
                "quadrupolar {0}".format(options["quad_index"]),
                parse_matrix(options["quad_matrix"], (3, 3)),
            ),
            "dissipation": lambda options: build_block(
                "dissipation {0}".format(options["dis_index"]),
                [options["dis_val"]],
            ),
        }.get(interaction_type)(options)
    except ValueError as e:
        raise ValueError("Error occurred when parsing {0}")


def parse_orientation(orientation):
    """
    Helper function to parse orientation keyword arguments
    :param orientation: a dictionary containing one set of orientation arguments
    :return: a formatted string
    """

    options = orientation["orientation_options"]
    preset = options["orientation_preset"]

    return {
        "zcw": lambda options: "zcw({0})".format(
            " ".join(split_into_args(options["zcw_n"], 1))
        ),
        "eulrange": lambda options: "eulrange({0})".format(
            " ".join(split_into_args(options["eul_n"], 1))
        ),
        "2_polar": lambda options: "{0} {1}".format(
            " ".join(split_into_args(options["theta"], 1)),
            " ".join(split_into_args(options["phi"], 1)),
        ),
        "3_euler": lambda entries: "{0} {1} {2}".format(
            " ".join(split_into_args(options["eul_1"], 1)),
            " ".join(split_into_args(options["eul_2"], 1)),
            " ".join(split_into_args(options["eul_3"], 1)),
        ),
        "4_euler": lambda options: "{0} {1} {2} {3}".format(
            " ".join(split_into_args(options["eul_1"], 1)),
            " ".join(split_into_args(options["eul_2"], 1)),
            " ".join(split_into_args(options["eul_3"], 1)),
            options["weight"],
        ),
    }.get(preset)(options)


def parse_polarization(polarization):
    """
    Helper function to parse polarization keyword arguments
    :param polarization: a dictionary containing one set of polarization arguments
    :return: a formatted string
    """
    options = polarization["polarization_options"]
    preset = options["polarization_preset"]
    if preset != 'custom':
        return preset
    else:
        try:
            return " ".join(split_into_args(options["polarization"], 1))
        except ValueError:
            return " ".join(split_into_args(options["polarization"], 3))


def parse_field(field):
    """
    Helper function to parse field keyword arguments
    :param field: a dictionary containing one set of field arguments
    :return: a formatted string
    """
    try:
        return  " ".join(split_into_args(field["field"], 1))
    except ValueError:
        return " ".join(split_into_args(field["field"], 3))


def main():
    input_json_path = sys.argv[1]
    mu_params = json.load(open(input_json_path, "r"))

    out_file_name = mu_params["out_file_prefix"]

    # combine all sections
    mu_params = {
        **mu_params["species"],
        **mu_params["interaction_params"],
        **mu_params["experiment_params"],
    }

    # get experiment parameters
    experiment = mu_params["experiment"]
    mu_params = {**mu_params, **experiment}

    if experiment["experiment_preset"] == "custom":
        del mu_params["experiment_preset"]
    del mu_params["experiment"]

    euler_convention = mu_params["euler_convention"]

    file_contents = [
        build_block("name", [out_file_name.replace(' ', '_')])
    ]

    for keyword, values in mu_params.items():
        if values and values not in ['None']:
            try:
                file_contents.append(
                    {
                        "spins": lambda values: build_block(
                            "spins",
                            [
                                " ".join(
                                    [
                                        i["spin_options"]["spin"]
                                        if "spin" in i['spin_options'].keys()
                                        else i["spin_options"]["spin_preset"]
                                        for i in values
                                    ]
                                )
                            ],
                        ),
                        # either 1x3 vector or scalar or function
                        "fields": lambda values: build_block(
                            'field',
                            [parse_field(entry) for entry in values]
                        ),
                        # either scalar or single function
                        "times": lambda values: build_block(
                            "time",
                            [" ".join(split_into_args(entry["time"], 1)) for entry in values],
                        ),
                        # either scalar or single function
                        "temperatures": lambda values: build_block(
                            "temperature",
                            [" ".join(split_into_args(entry["temperature"], 1)) for entry in values],
                        ),
                        "x_axis": lambda value: build_block("x_axis", [value]),
                        "y_axis": lambda value: build_block("y_axis", [value]),
                        "average_axes": lambda values: build_block(
                            "average_axes", [v.strip() for v in values.split(",")]
                        ),
                        "experiment_preset": lambda value: build_block(
                            "experiment", [value]
                        ),
                        "orientations": lambda values: build_block(
                            "orientation {0}".format(euler_convention),
                            [parse_orientation(entry) for entry in values],
                        ),
                        "interactions": lambda values: "".join(
                            [parse_interactions(entry) for entry in values]
                        ),
                        "polarizations": lambda values: build_block(
                            "polarization",
                            [parse_polarization(entry) for entry in values],
                        ),
                    }.get(keyword, lambda _: "")(values)
                )
            except ValueError as e:
                sys.stderr.write("Error occurred when parsing {0}\n{1}".format(keyword, str(e)))
                sys.exit(1)

    write_file("outfile.in", file_contents)

    try:
        mu_inp = MuSpinInput(open("outfile.in"))
        res = mu_inp.evaluate()
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()