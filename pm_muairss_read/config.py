import json
import yaml


def main():
    with open("params.yaml") as f:
        existing_params = yaml.safe_load(f)

    with open("inputs.json") as f:
        incoming_params = json.load(f)

    clustering_params = incoming_params["clustering"]
    merged_params = {**existing_params, **clustering_params}

    clustering_save_params = incoming_params["clustering_save"]
    if clustering_save_params["clustering_save_type"] != "none":
        merged_params = {**merged_params, **clustering_save_params}

    with open("params.yaml", "w") as f:
        yaml.safe_dump(merged_params, f)


if __name__ == "__main__":
    main()
