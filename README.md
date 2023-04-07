# DRS Endpoint Test Suite

This repository is a submission for the GA4GH Developer technical assessment. It contains a test suite class, DRS_Validator, that runs tests to check the compliance of DRS object endpoints returned by a GET request.  

The schemas used to validate DRS object endpoints are from the [**DRS Schemas Repository**](https://github.com/ga4gh/data-repository-service-schemas).

1. [Quick Start](#quick-start)
2. [Install](#install)
    - [With Conda](#in-a-conda-env)
    - [With pip](#with-pip)
3. [Usage](#using-drs_validator)
4. [Next Steps](#next-steps)
5. [The DRS_Validator Class](#the-drs_validator-class)
    - [Class Attributes](#class-attributes)
    - [Instance Attributes](#instance-attributes)
    - [Methods](#methods-in-drs_validator)
6. [Other Scripts](#other-scripts)


## Quick Start
Assuming you have setup the DRS Starter Kit and populated test data into it, you can replicate the present tests as follows:  
```
git clone https://github.com/bruhad-dave/drs-validator.git
cd drs-validator
pip install -r requirements.txt

python validator_runner.py \
-s full/path/to/drs-validator/json_schema \
-u http://localhost:5000/ga4gh/drs/v1/objects/ \
-i full/path/to/drs-validator/test_objects.txt
```  

`validator_runner.py` wraps around the class definition and works with comma-separated input files, where the first two columns **must** contain the object id and expected status code respectively. Note that the script expects there to be a header in the input file.  

Test results are printed to the terminal in the format:  
```
{"object_id" : "object_id", \
"test_name" : "name_of_test", \
"pass" : "True/False", \
"message" : "log message"}
```  

See [below](#the-drs_validator-class) for more detailed descriptions of the tests and outcomes.

## Install

DRS_Validator can be used without explicit installation via `validator_runner.py` as shown in [Quick Start](#quick-start). This is useful to run tests on several DRS objects from an input file as described above, without making changes to your local environment.  

DRS_Validator can be installed as follows, once the repo is pulled down with `git clone`.  

### In a conda env
```
cd <abs/path/to/drs-validator>
conda env create -f env.yaml
conda activate drs_endpoint_test
```

DRS_Validator is now ready to use programmatically in this conda env. To close the environment, run `conda deactivate`

### With pip
```
cd <abs/path/to/drs-validator>
pip install -r requirements.txt

python setup.py install ## `pip install .` would also work
```  

## Using DRS_Validator

With a DRS starter kit deployed, and installation as above, DRS_Validator can be used programmatically by importing as:

```your_script.py
from drs_validator.validator import DRS_Validator

## create an instance
## ensure that schema_dir is an absolute path
validator_instance = DRS_Validator(schema_dir, base_url)

## test an object
validator_instance.validate(object_id, expected_status_code)
```

## Next Steps

DRS_Validator can be extended to:  
    - add tests for object_id and URI compliance  
    - add tests for requests that need authorization  
    - add Code-202 schema  
    - add tests for AccessURL methods  

The code can also be packaged with Docker if needed or if its complexity or the number of dependencies increases. The current implementation is as barebones as possible so any user with a python installation can viably use it; it could also be packaged as a conda recipe or to PyPI for one-step installation.  

## The DRS_Validator class

The class instantiates with two user-specified attributes, `base_url`, and `schema_dir` and takes the `object_id` and the expected HTTP status code to test the endpoint.  

Three tests are run:  
1. A GET request is sent and the status code received is checked against the expected code  
2. The header of the GET response is read to ensure that the content type is JSON  
3. **IF** test 2 is passed, the response JSON is checked against the appropriate schema using `jsonschema`. The right schema is picked based on the status code received (this is based on [DRS docs](https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.2.0/docs/)):  

    - Status Code 200: DrsObject.json  
    - 400/500 Status Codes: Error.json  

If the GET response fails Tests 1 and 2, the expected and received status code/content-type are noted in the test results. If the GET response fails Test 3, a new file, `<object_id>.log`, is created in the working directory. This is where errors thrown by jsonschema are written for reference and to enable troubleshooting.  

### Class Attributes  
- `EXPECTED_CONTENT_TYPE`: value="application/json"; DRS endpoints are always JSON  
- `OBJECT_SCHEMA_LOOKUP`: Dictionary with schema names as keys and lists of corresponding status codes as values  
- `REPORT_TEMPLATE`: Template string for formatting test results that are printed to terminal  

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

### Methods in DRS_Validator
- `validate_object_request(object_id, exp_status)`: can be used to ONLY run Tests 1 and 2
- `validate_object_schema()`: can be used to run Test 3 (but requires that `validate_object_request` be called first)
- `validate(object_id, exp_status)`: wraps around the two methods above; only calls `validate_object_schema()` if response content type is JSON

### Other Scripts  
- `validator_runner.py`: Can be run to use DRS_Validator without installation; described above
- usage:  
    ```
    python validator_runner.py -s <abs/path/to/schema/dir> -u <base/url> -i <abs/path/to/input/csv>
    ```
- options:  
    - `-s`: Absolute path to directory containing JSON schemas
    - `-u`: Base url to use as suffix for object ID in order to make GET requests
    - `-i`: Path to comma-separated, headered input file, where column 1 contains object ids and column 2 contains corresponding expected status codes


- `yaml_to_json.py`: Convert schema from yaml to json. Also takes care of any schema references within a given schema file.  
- usage:  
    ```
    python yaml_to_json.py -i <abs/path/to/dir/with/yaml_files> -o <abs/path/to/ouput dir>
    ```
- options:  
    - `-i`: Absolute path to directory containing schemas in YAML format
    - `o`: Absolute path to dorectory where you'd like the converted JSON files to be written.