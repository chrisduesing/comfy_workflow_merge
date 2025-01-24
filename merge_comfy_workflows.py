import json
import argparse

# Load the JSON files
def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Save the JSON to a file
def save_json(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

# Merge two JSON objects
def merge_json(json1, json2, y_offset):
    merged = {
        "last_node_id": json1["last_node_id"] + json2["last_node_id"],
        "last_link_id": json1["last_link_id"] + json2["last_link_id"],
        "nodes": [],
        "links": [],
        "groups": json1.get("groups", []) + json2.get("groups", []),
        "config": json1.get("config", {}),
        "extra": json1.get("extra", {}),
        "version": json1.get("version", 0.4)
    }

    # Update nodes and links to prevent conflicts
    node_id_offset = json1["last_node_id"]
    link_id_offset = json1["last_link_id"]

    for node in json1["nodes"]:
        merged["nodes"].append(node)
    for node in json2["nodes"]:
        node["id"] += node_id_offset
        print(node["pos"])
        node["pos"][1] += y_offset  # Offset the y position
        if "inputs" in node:
            for input_item in node["inputs"]:
                if "link" in input_item and input_item["link"] is not None:
                    input_item["link"] += link_id_offset
        if "outputs" in node:
            for output_item in node["outputs"]:
                if "links" in output_item and output_item["links"]:
                    output_item["links"] = [link + link_id_offset for link in output_item["links"]]
        merged["nodes"].append(node)

    for link in json1["links"]:
        merged["links"].append(link)
    for link in json2["links"]:
        link[0] += link_id_offset
        link[1] += node_id_offset
        link[3] += node_id_offset
        merged["links"].append(link)

    return merged

# Function to merge JSON files with parameters
def merge_json_files(file1, file2, y_offset, output_file):
    json1 = load_json(file1)
    json2 = load_json(file2)
    merged_json = merge_json(json1, json2, y_offset)
    save_json(output_file, merged_json)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Merge two JSON files with node and link conflict resolution.")
    parser.add_argument("file1", help="Path to the first JSON file")
    parser.add_argument("file2", help="Path to the second JSON file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    parser.add_argument("--y_offset", type=int, default=1000, help="Y offset for nodes from the second file (default: 1000)")

    args = parser.parse_args()

    merge_json_files(args.file1, args.file2, args.y_offset, args.output_file)

if __name__ == "__main__":
    main()