import argparse
import pandas as pd
from drs_validator.validator import DRS_Validator


parser = argparse.ArgumentParser("Verify DRS endpoints from comma-separated input file containing the columns: \
                                 [object_id, Expected Status Code, Expected Content Type]")
parser.add_argument("-s", "--schema_dir", help = "Absolute path to directory containing all required schema in JSON format.")
parser.add_argument("-u", "--base_url", help = "URL prefix to which GET requests will be made.") ## base_url for this test: "http://localhost:5000/ga4gh/drs/v1/objects/"
parser.add_argument("-i", "--input_file", help = "Absolute path to comma-separated input file to read test object_ids and expected outputs from.")
args = parser.parse_args()

schema_dir = args.schema_dir
input_file = args.input_file

validator = DRS_Validator(schema_dir, args.base_url)
data = pd.read_csv(input_file, sep = ",", header = 0)
for i in data.index:
    object_id, exp_status, exp_type = data.loc[i].to_list()
    validator.validate(object_id, exp_status)