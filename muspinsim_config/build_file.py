import json
import re
import sys

from muspinsim import MuSpinInput


def write_file(file_name, content):
    """
    Write muspinsim file
    :param file_name: name of file
    :param content: list of strings containing blocks to write
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(
            """
#######################################################
# Muspinsim Input File
# Generated using Muon Galaxy Tool Muspinsim_Input
#######################################################\n\n"""
        )
        file.write("".join(content))


def build_block(title, vals):
    """
    Build keyword block
    :param title: string - Keyword
    :param vals: list of strings - lines containing values for keyword
    :return: A string containing formatted keyword block
    """
    return "{0}\n    {1}\n".format(title, "\n    ".join(vals))


def format_entry(entry):
    """
    Helper function to remove whitespace between function parameters
    and remove ',' or ';' inbetween parameters
    :param entry: string - user entry
    :return: string containing only valid parameters
    """
    stck = []
    new_str = ""
    for i, char in enumerate(entry):
        if char == "(":
            stck.append(i)
        elif char == ")":
            if len(stck) == 0:
                raise ValueError(
                    f"Could not parse entry {entry} brackets mismatch - "
                    f"unexpected ')' found on char {i}"
                )
            stck.pop()
        elif char == " " and len(stck) > 0:
            continue

        # remove ',' between functions
        elif char in [",", ";"] and len(stck) == 0:
            new_str += " "
            continue
        new_str += char

    if len(stck) != 0:
        raise ValueError(
            f"Could not parse entry {entry} brackets mismatch - unclosed '(' "
            f"found on char(s): {stck}"
        )
    return new_str


def split_into_args(entry, nargs=1):
    """
    Helper function to split input into a list of args
    :param entry: a string containing a user inputted line
    :param nargs: number of expected arguments
    :return: a list of arguments found
    :exception: ValueError - if number of arguments
        found does not match expected (nargs)
    """

    # remove square brackets and extra whitespace/newline
    content = " ".join(entry.replace("[", "").replace("]", "").split())

    # remove whitespace in between expressions/functions
    # remove commas/semicolons in between expressions/functions
    # split on whitespace to separate args

    content = re.split(r"\s", format_entry(content))
    chars = [elem.strip() for elem in content if elem != ""]
    if len(chars) != nargs:
        raise ValueError(
            f"Could not parse entry {entry} incorrect number of args found "
            f"{len(chars)}:\n({chars})\nBut expected {nargs}"
        )
    return chars


def parse_matrix(entry_string, size):
    """
    Helper function to parse and format matrix/vector
    to be readable by MuSpinSim
    :param entry_string: a user input string for a matrix/vector
    :param size: (x, y) integer tuple: dimensions of matrix
    :return: a list of strings of length y, each string
    containing x elements (space separated)
    """
    content = split_into_args(entry_string, nargs=size[0] * size[1])
    return [
        " ".join(content[x: x + size[0]])
        for x in range(0, len(content), size[0])
    ]


def parse_interactions(interaction):
    """
    Helper function to build keyword blocks for all
    interaction parameters entered
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
                (
                    f"hyperfine {options['hfine_index']} "
                    f"""{
                        options['hfine_e_index']
                        if options['hfine_e_index'] else ''
                    }"""
                ).strip(),
                parse_matrix(options["hfine_matrix"], (3, 3)),
            ),
            "dipolar": lambda options: build_block(
                f"dipolar {options['di_index']} {options['di_index_2']}",
                parse_matrix(options["di_vector"], (3, 1)),
            ),
            "quadrupolar": lambda options: build_block(
                f"quadrupolar {options['quad_index']}",
                parse_matrix(options["quad_matrix"], (3, 3)),
            ),
            "dissipation": lambda options: build_block(
                f"dissipation {options['dis_index']}",
                [options["dis_val"]],
            ),
        }.get(interaction_type)(options)
    except ValueError as exc:
        raise ValueError(f"Error occurred when parsing {exc}") from exc


def parse_orientation(orientation):
    """
    Helper function to parse orientation keyword arguments
    :param orientation: a dictionary containing one set of
        orientation arguments
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
        "3_euler": lambda options: "{0} {1} {2}".format(
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
    :param polarization: a dictionary containing one set
        of polarization arguments
    :return: a formatted string
    """
    options = polarization["polarization_options"]
    preset = options["polarization_preset"]
    if preset != "custom":
        return preset
    else:
        try:
            return " ".join(split_into_args(options["polarization"], 1))
        except ValueError:
            return " ".join(split_into_args(options["polarization"], 3))


def parse_field(field, field_type):
    """
    Helper function to parse field keyword arguments
    :param field: a dictionary containing one set of field arguments
    :param field_type: a string giving the type of field, either field or
                       intrinsic_field
    :return: a formatted string
    """
    try:
        return " ".join(split_into_args(field[field_type], 1))
    except ValueError:
        return " ".join(split_into_args(field[field_type], 3))


def parse_fitting_variables(fitting_variables):
    """
    Helper function to parse field keyword fitting_variables
    :param fitting_variables: a dictionary containing one set of
        arguments
    :return: a formatted string
    """
    return "{0} {1} {2} {3}".format(
        fitting_variables["var_name"].strip().replace(" ", "_"),
        " ".join(split_into_args(fitting_variables["start_val"], 1))
        if fitting_variables["start_val"].strip() != ""
        else "",
        " ".join(split_into_args(fitting_variables["min_bound"], 1))
        if fitting_variables["min_bound"].strip() != ""
        else "",
        " ".join(split_into_args(fitting_variables["max_bound"], 1))
        if fitting_variables["max_bound"].strip() != ""
        else "",
    ).strip()


def parse_spin(spin):
    """
    Helper function for parsing a spin
    :param spin: a dictionary containing a spin object from the config either
                 just a spin_preset or a custom value with a name and
                 atomic_mass
    """
    if spin["spin_preset"] != "custom":
        return spin["spin_preset"]
    else:
        elem_name = spin["spin"].strip()
        if elem_name not in ["e", "mu"]:
            elem_name = elem_name.capitalize()
        return (
            f"{int(spin['atomic_mass']) if spin['atomic_mass'] else ''}"
            f"{elem_name}"
        ).strip()


def parse_celio(celio_params):
    """
    Helper function for parsing Celio's method parameters
    :param celio_params: a dictionary containing the parameters for Celio's
                         method
    """
    options = celio_params["celio_options"]
    if not options["celio_enabled"]:
        return ""
    else:
        # Now have celio_k and potentially celio_averages
        celio_k = options["celio_k"]
        celio_averages = options["celio_averages"]

        # As celio_averages is optional so may be None
        if celio_averages is None:
            celio_averages = ""

        return build_block("celio", [f"{celio_k} {celio_averages}".strip()])


parse_func_dict = {
    "spins": lambda values: build_block(
        "spins",
        [" ".join([parse_spin(entry["spin_options"]) for entry in values])],
    ),
    # either 1x3 vector or scalar or function
    "fields": lambda values: build_block(
        "field", [parse_field(entry, "field") for entry in values]
    ),
    "intrinsic_fields": lambda values: build_block(
        "intrinsic_field",
        [parse_field(entry, "intrinsic_field") for entry in values],
    ),
    # either scalar or single function
    "times": lambda values: build_block(
        "time",
        [" ".join(split_into_args(entry["time"], 1)) for entry in values],
    ),
    # either scalar or single function
    "temperatures": lambda values: build_block(
        "temperature",
        [
            " ".join(split_into_args(entry["temperature"], 1))
            for entry in values
        ],
    ),
    "axes_options": {
        "x_axis_options": {
            "x_axis": lambda value: build_block("x_axis", [value]),
            "average_axes": lambda values: build_block(
                "average_axes", values),
        },
        "x_axis": lambda value: build_block("x_axis", [value]),
        "y_axis": lambda value: build_block("y_axis", [value]),
        "average_axes": lambda values: build_block(
            "average_axes", values)
    },
    "average_axes": lambda values: build_block("average_axes", values),
    "experiment_preset": lambda value: build_block("experiment", [value]),
    "orientations": lambda values: build_block(
        f"orientation {EULER_CONVENTION}",
        [parse_orientation(entry) for entry in values],
    ),
    "interactions": lambda values: "".join(
        [parse_interactions(entry) for entry in values]
    ),
    "polarizations": lambda values: build_block(
        "polarization",
        [parse_polarization(entry) for entry in values],
    ),
    "celio_params": parse_celio,
    "fitting": lambda value: build_block(
        "fitting_data", ['load("fitting_data.dat")']
    ),
    "fitting_method": lambda value: build_block("fitting_method", [value]),
    "fitting_variables": lambda values: build_block(
        "fitting_variables",
        [parse_fitting_variables(entry) for entry in values],
    ),
    "fitting_tolerance": lambda value: build_block(
        "fitting_tolerance",
        [str(value)],
    ),
}
EULER_CONVENTION = "ZYZ"

# Gives replacement values in the case a parameter is unassigned
parse_none_dict = {
    # Allow average_axis to be None as by default is orientation in
    # muspinsim but letting the UI present this here instead
    "average_axes": ["none"],
}


def parse_dict(dictionary, params, file_contents) -> bool:
    """
    Helper function for parsing nested dictionaries defined above
    containing parse functions
    :returns: Whether an error occurred
    """

    err_found = False
    for keyword, val in params.items():

        # Either don't allow the value to be None or replace
        # with value in the parse_none_dict above
        should_assign = val and val not in ["None"]
        if not should_assign and keyword in parse_none_dict:
            should_assign = keyword in parse_none_dict
            val = parse_none_dict[keyword]

        if should_assign:
            try:
                keyword_func = dictionary.get(keyword)
                # Check for nested dict, and add that contents as well if found
                if isinstance(keyword_func, dict):
                    err_found = err_found or parse_dict(
                        keyword_func, val, file_contents)
                else:
                    if keyword_func:
                        file_contents.append(keyword_func(val))

            except ValueError as exc:
                sys.stderr.write(
                    f"Error occurred when parsing {keyword}\n{str(exc)}"
                )
                err_found = True
    return err_found


def main():
    """
    Entry point
    """
    input_json_path = sys.argv[1]
    mu_input_params = json.load(open(input_json_path, "r", encoding="utf-8"))

    out_file_name = mu_input_params["out_file_prefix"].strip().replace(
        " ", "_")

    # Check if using a template
    template_path = None
    if (mu_input_params["use_structure_file_conditional"]
            ["use_structure_file"]) == "true":
        template_path = "muspinsim_gen_out.in"

    # combine all sections
    mu_params = {
        **(mu_input_params["use_structure_file_conditional"]
           ["interaction_params"]),
        **mu_input_params["experiment_params"],
        **mu_input_params["fitting_params"]["fitting_options"],
    }
    mu_params.update(
        **mu_input_params["use_structure_file_conditional"]["spins"]
    )

    # get experiment parameters
    experiment = mu_params["experiment"]
    mu_params = {**mu_params, **experiment}

    if experiment["experiment_preset"] == "custom":
        del mu_params["experiment_preset"]
    del mu_params["experiment"]

    global EULER_CONVENTION
    EULER_CONVENTION = mu_params["euler_convention"]

    file_contents = [
        build_block("name", [out_file_name.strip().replace(" ", "_")])
    ]

    if parse_dict(parse_func_dict, mu_params, file_contents):
        sys.exit(1)

    # Load and append the template if specified
    if template_path is not None:
        # Check if we have already defined spins above
        spins_line = None
        spins_line_index = None
        if ("spins" in mu_params):
            # Find the current line definition in the file
            # In the format 'spins\n e\n'
            for i, line in enumerate(file_contents):
                if line.startswith("spins"):
                    spins_line = line.split("\n")[1].strip()
                    spins_line_index = i
            if spins_line_index is not None:
                del file_contents[spins_line_index]

        # Append the template file's contents
        with open(template_path, encoding="utf-8") as template_file:

            while line := template_file.readline():
                # Append the spins if needed
                if line.startswith("spins") and spins_line is not None:
                    next_line = template_file.readline().strip()
                    file_contents += f"spins\n    {next_line} {spins_line}\n"
                else:
                    file_contents += line

    write_file("outfile.in", file_contents)

    try:
        MuSpinInput(open("outfile.in", encoding="utf-8"))
    except Exception as exc:  # pylint: disable=broad-except
        sys.stdout.write(
            "Warning, This created file may not work properly. Error(s) "
            f"encountered when trying to parse the file : {str(exc)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
