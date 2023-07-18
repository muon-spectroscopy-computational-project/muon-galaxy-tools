import yaml


def main():
    with open("params.yaml") as f:
        existing_params = yaml.safe_load(f)

    with open("incoming_params") as f:
        incoming_params = yaml.safe_load(f)

    merged_params = {**existing_params, **incoming_params}

    with open("params.yaml", "w") as f:
        yaml.safe_dump(merged_params, f)


if __name__ == "__main__":
    main()
