# SBDB-close-approach-data API test framework

Test framework to test SBDB close approach data API: https://ssd-api.jpl.nasa.gov/cad.api , more information on the API is available at https://ssd-api.jpl.nasa.gov/doc/cad.html.  
The API offers various filters and limits. In this project we are mainly focusing on testing filters. We can further develop to add on more filters and limits. We are using pytest framework for testing. 

**Execution Steps**:
1. Clone the repository 
2. Enter into SBDB-close-approach-data
   **cd SBDB-close-approach-data/**
3. Create docker image using the below command:
   **docker build -t sbdbcloseapproachapi:1.0 .**
3. Start a container in interactive mode, expose port 80 to view the test results using below command
   **docker run --name sbdb_close_approach_api_1.0 -it -p 80:7000 sbdbcloseapproachapi:1.0**
4. Run tests using below command:
   **python run.py [--keyword testname]**
   --keyword testname : selects the tests which contain testname in it, by default keyword is test so all tests are selected.
5. Once the test execution is done, to visulaise the test report, open **http://localhost/report.html** on browser

**Approach Taken:**

**Project structure:**

/cases/ - contains testcases 

/cases/test_sbdb_close_approach_api.py - contains the tests we execute on sbdb_close_approach_api

/data/ - contains data used in tests

/data/data.json - file used to get data which is used to obtain expected data

/qa_utilities/ - contains utility functions

/qa_utilities/get_test_data.py - Contains code to fetch data from SBDB close approch API and write into /data/data.json. By executing **python qa_utilities/get_test_data.py** command, we create a data.json file in /data folder which contains data for all currently known close approaches that have happened or will happen in the 20th and 21st centuries

/Dockerfile - is used to create Docker image

/pip_packages.txt - file contains the packages to be installed for execution of tests

/run.py - Conatins code to execute tests. By executing **python run.py** all tests within /cases folder are executed.

/start.sh - Is the file that gets executed as soon as container is created. Here we are invoking http.server in background to be able to fetch the test report on browser and we are executing python qa_utilities/get_test_data.py to create data.json

In this project we fetch response of https://ssd-api.jpl.nasa.gov/cad.api with zero or more filters and validate the response.
/data/data.json file is created by passing filters date_min='1900-01-01', date_max='2100-12-31', dist_max=1 to https://ssd-api.jpl.nasa.gov/cad.api API, only data part of the API response is captured in this file. If we have access to database, we can fetch this data from the database. We read data.json and filter the data based on the filters we pass to the API to obtain expected output. We further validate the API response with same filters and expected output to match.

