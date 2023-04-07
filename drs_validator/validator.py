import os, sys
import json
import requests
import jsonschema
from string import Template

class DRS_Validator:
    """Validate DrsObject GET requests and response schema.

        EXPECTED_CONTENT_TYPE: Content type expected from GET request; always "application/json"
        OBJECT_SCHEMA_LOOKUP: What schema to use based on status code of GET request
        REPORT_FORMAT: Format in which to print test results to terminal
    """

    EXPECTED_CONTENT_TYPE = "application/json"
    OBJECT_SCHEMA_LOOKUP = {"DrsObject": [200], "Error": [400, 401, 403, 404, 500]}
    REPORT_TEMPLATE = Template("""{object_id : ${uniq_id}, test_name : ${test_name}, pass : ${test_passed}, message : ${msg}}""")

    def __init__(self, schema_dir, base_url):
        """Set up an instance of DRS_Validator.

        Args:
            schema_dir (str/pathlike): Absolute path to dir containing schema in JSON format; user-provided
            base_url (str/pathlike): URL prefix to which object_ids are appended, to construct a URL; user-provided
        """

        self.base_url = base_url
        self.schema_dir = schema_dir

    def validate_object_request(self, object_id, exp_status):
        """Function to validate GET request response.

        Args:
            object_id (str): Unique identifier for DRS object
            exp_status (str): Expected HTTP status code for GET request to base_url/object_id
        """

        self.id = object_id
        ## construct url and make a GET request
        object_url = self.base_url+object_id
        response = requests.get(object_url)

        ## store response object and status_code as instance attribute for testing
        self.json = response.json()
        self.status_code = response.status_code

        ## Check that response returns expected status code
        try:
            assert response.status_code == exp_status
            self.passed_status_code_check = True
        except AssertionError as ae:
            self.passed_status_code_check = False

        sys.stderr.write(json.dumps(self.REPORT_TEMPLATE.substitute(uniq_id = self.id, 
                                          test_name = "Check HTTP status code", 
                                          test_passed = self.passed_status_code_check, 
                                          msg = f"Expected - {exp_status}; Received - {self.status_code}"))+"\n\n")

        ## Check that response object is JSON
        try:
            assert self.EXPECTED_CONTENT_TYPE in response.headers["content-type"]
            self.passed_object_type_test = True
        except AssertionError as ae:
            self.passed_object_type_test = False

        sys.stderr.write(json.dumps(self.REPORT_TEMPLATE.substitute(uniq_id = self.id, 
                                  test_name = "Check response object type", 
                                  test_passed = self.passed_object_type_test, 
                                  msg = f"Expected: {self.EXPECTED_CONTENT_TYPE} in header; Received: {response.headers['content-type']}"))+"\n\n")

    def validate_object_schema(self):
        """Select appropriate schema, then validate that the reponse JSON is formatted
            according to the corresponding schema. Caller ONLY IF object is JSON
        """

        ## pick the correct schema name and contruct a schema filepath
        self.schema_name = [k for k in self.OBJECT_SCHEMA_LOOKUP.keys() if self.status_code in self.OBJECT_SCHEMA_LOOKUP[k]][0]
        schema_file = os.path.join(self.schema_dir, self.schema_name+".json")

        ## load the schema file
        with open(schema_file, "r") as sp:
            self.schema = json.load(sp)

        ## set up a resolver for any relative $ref paths in the chosen schema and store as instance attribute
        ref_resolver = jsonschema.RefResolver(base_uri = "file://" + self.schema_dir + "/", referrer = self.schema)

        ## check that response.json matches schema
        try:
            jsonschema.validate(self.json, self.schema, resolver = ref_resolver)
            self.passed_schema_validation = True
            schema_stderr = f"{self.id} endpoint instance matches {self.schema_name} schema."
        except Exception as e:
            self.passed_schema_validation = False
            schema_stderr = f"{self.id} endpoint instance does not match {self.schema_name} schema, see {self.id}.log."
            ## write schema validation errors to object_id.log to enable troubleshooting
            with open(f"{self.id}.log", "w") as error_log:
                error_log.write(str(e))
            error_log.close()

        sys.stderr.write(json.dumps(self.REPORT_TEMPLATE.substitute(uniq_id = self.id, 
                                  test_name = "Check response JSON against schema", 
                                  test_passed = self.passed_schema_validation, 
                                  msg = schema_stderr))+"\n\n")


    def validate(self, object_id, exp_status):
        """Wrap around the validation functions defined above.

        Args:
            object_id (_type_): _description_
            exp_status (_type_): _description_
        """
        self.validate_object_request(object_id, exp_status)
        if self.passed_object_type_test:
            self.validate_object_schema()
        else:
            sys.stderr.write("Object received was not a valid JSON, and so not checked against schema.")


