import glob
import json
import csv

def main():
    json_files = scan_json_files()

    for json_file in json_files:
        flatten_json_data = load_flatten_json(json_file)
        csv_file = json_file.replace('.json', '.csv')
        write_to_csv(flatten_json_data, csv_file)

def scan_json_files():
    json_files = glob.glob(f'data/**/*.json', recursive=True)
    return json_files

def load_flatten_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        keys_to_remove = []
        for key in data.keys():
            if isinstance(data[key], (dict, list)):
                flattened_data = to_flatten_json(data[key], parent_key=key, separator='_')
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del data[key]

        data.update(flattened_data)
    return data

def to_flatten_json(json_obj, parent_key='', separator='_'):
    flattened = {}
    for key, value in json_obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(to_flatten_json(value, new_key, separator=separator))
        elif isinstance(value, list):
            flatten_list(new_key, value, flattened, separator)
        else:
            flattened[new_key] = value
    return flattened

def flatten_list(key, value, flattened_data, separator='_'):
    if isinstance(value, list):
        for i, item in enumerate(value):
            flattened_data[f"{key}{separator}{i}"] = item
    else:
        flattened_data[key] = value

def write_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='') as csvf:
        csv_writer = csv.writer(csvf)
        csv_writer.writerow(data.keys())
        csv_writer.writerow(data.values())


if __name__ == "__main__":
    main()
