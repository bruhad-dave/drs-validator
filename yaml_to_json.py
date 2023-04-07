import os
import json
import yaml
import argparse

parser = argparse.ArgumentParser("Convert yaml to json.")
parser.add_argument("-i", "--input_dir", help = "Absolute path to directory containing yaml files to be converted.")
parser.add_argument("-o", "--outdir", help = "Absolute path to directory to write json to. Defaults to input_dir.")
args = parser.parse_args()

def yaml_to_json(yaml_file, outdir):
    """Convert yaml file to json. Also converts .yaml file extensions in $ref paths to json

    Args:
        yaml_file (str/pathlike): yaml file to convert
        outdir (str/pathlike): path to output directory
    """
    base_dir, yaml_filename = os.path.split(yaml_file)
    json_filename = yaml_filename.replace(".yaml", ".json")

    if not outdir:
        outdir = base_dir
    else:
        outdir = os.path.abspath(outdir)

    json_file = os.path.join(outdir, json_filename)

    with open(yaml_file, "r") as yf:
        yaml_data = yaml.safe_load(yf)
        json_str = json.dumps(yaml_data).replace(".yaml", ".json")
        clean_yaml_data = json.loads(json_str)

    with open(json_file, "w") as jf:
        json.dump(clean_yaml_data, jf, indent=4)

if not args.outdir:
    outdir = args.input_dir
else:
    outdir = args.outdir

if not os.path.exists(outdir):
    os.mkdir(outdir)

for every_file in os.listdir("ga4gh_techtest/yaml_schema"):
    if every_file.endswith(".yaml"):
        # print(every_file)
        yaml_input = os.path.abspath(args.input_dir+every_file)
        yaml_to_json(yaml_file = yaml_input, outdir = outdir)

