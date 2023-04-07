# DRS Endpoint Test Suite

This repository contains a test suite class, DRS_Validator to check the compliance of DRS objects returned by a GET request.  

The schemas used to validate DRS object endpoints are from the [**DRS Schemas Repository**](https://github.com/ga4gh/data-repository-service-schemas).


## Quick Start
Assuming you have setup the DRS Starter Kit and populated test data into it, you can replicate the present tests as follows:  
```
git clone <this repo>
cd <this repo>
pip install -r requirements.txt

python DRS_Validator/validator_runner.py \
-s full/path/to/<this repo>/json_schema \
-u http://localhost:5000/ga4gh/drs/v1/objects/ \
-i full/path/to/<this repo>/test_objects.txt
```  

`validator_runner.py` wraps around the class definition and works with comma-separated input files, which must contain three columns: object id, expected status code, and expected content type.  

Test results are printed to the terminal in the format:  
```
{"object_id" : "object_id", \
"test_name" : "name_of_test", \
"pass" : "True/False", \
"message" : "log message"}
```  

## Install

DRS_Validator can be used without explicit installation via validator_runner.py as shown in [Quick Start](#quick-start). This is useful to run tests on several DRS objects from an input file as described above.  

DRS_Validator can be installed as follows, once the repo is pulled down with `git clone`.  

### Install with conda
```
cd <path/to/this_repo>
conda env create -f env.yaml
conda activate drs_endpoint_test

python setup.py install
```

### Install with pip
```
cd <path/to/this_repo>
pip install -r requirements.txt

python setup.py install
```  

## Using DRS_Validator

With a DRS starter kit deployed, DRS_Validator can be used in scripts by importing as:

```your_script.py
from drs_validator.validator import DRS_Validator

## create an instance
## ensure that schema_dir is an absolute path
validator_instance = DRS_Validator(schema_dir, base_url)

## test an object
validator_instance.validate(object_id, expected_status_code)
```

## DRS_Validator class

The class instantiates with two user-specified attributes, `base_url`, and `schema_dir` and takes the `object_id` and the expected HTTP status code to test the endpoint.  

Three tests are run:  
1. A GET request is sent and the status code received is checked against the expected code  
2. The header of the GET response is read to ensure that the content-type is JSON  
3. **IF** test 2 is passed, the response JSON is checked against the appropriate schema using `jsonschema`. The right schema is picked based on the status code received:  

    - Status Code 200: DrsObject.json  
    - Any 400/500 Status Codes: Error.json  

If the GET response fails Tests 1 and 2, the expected and received status code/content-type are noted in the test results. If the GET response fails Test 3, a new file, `<object_id>.log`, is created in the working directory. This is where errors thrown by jsonschema are written for reference and to enable troubleshooting.  

### Class Attributes  
- `EXPECTED_CONTENT_TYPE`: value="application/json"; DRS endpoints are always JSON  
- `OBJECT_SCHEMA_LOOKUP`: Dictionary with schema names as keys and lists of corresponding status codes as values  
- `REPORT_FORMAT`: Template string for formatting test results that are printed to terminal  

### Instance Attributes  
- `schema_dir`: is the path to a directory containing all (JSON) schema that are required to validate the response of the GET request made to `base_url`/`object_id`  
- `base_url`: the url prefix that is added to the DRS object's `object_id`, to contruct a url for a GET request  
- `id`: object id  
- `json`: JSON from the object's GET response  
- `status_code`: HTTP status code received from the object's GET response  
- `passed_status_code_check`: Result of Test 1 (bool)  
- `passed_object_type_test`: Result of Test 2 (bool)  
- `schema_name`: name of schema used for validation  
- `schema`: the chosen schema  
- `passed_schema_validation`: Result of Test 3 (bool)  

### Other Scripts  
- `yaml_to_json.py`: Convert schema from yaml to json.
- usage:
    ```
    python yaml_to_json.py -i <abs/path/to/dir/with/yaml_files> -o <abs/path/to/ouput dir>
    ```