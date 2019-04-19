# Python Developer Applicant Programming Test for Cylance, Inc

## Setup instructions:

0. Initialize a new virtual environment of your choosing. I use:
   > `python -m venv .env` 
   and 
   > `source .env/bin/activate`

1. Use the 
    > `pip install -r requirements.txt` 
    command to install the project dependencies.

A predefined build task has been made for users of Visual Studio code in `.vscode/tasks.json` for running or testing the server.

Or:

2. Run the server
   > `python pdapt.py`

3. Test the app
   > `coverage run tests.py && coverage html`



# Description
Design and implement a RESTful web API that can be used to maintain a database of GUIDs (Globally Unique Identifier) and associated
metadata. The API must expose commands to perform CRUD operations (Create, Read, Update, Delete). 
DONE: The application should use a cache layer to quickly serve the most recently used GUIDs. 

DONE: GUIDs should be 32 hexadecimal characters, all uppercase. The GUIDs should be valid only
for a limited period of time, with a default of 30 days from the time of creation, if an expiration time is not provided. The expiration time should be formatted in Unix Time. 
Input and output data should be valid JSON format.

Validations should be put in place to make sure input data
conforms the specified formats. Code must be documented.

# Bonus points if the solution is fully asynchronous.


### Commands specification

# Create
Creates a new GUID and stores it in the database along with the metadata
provided. If a GUID is not specified, the system should generate a random one.

DONE - Example 1
URL: PUT /guid/9094E4C980C74043A4B586B420E69DDF
Input:
{
"expire": "1427736345",
"user": "Cylance, Inc."
}
Output:
{
"guid": "9094E4C980C74043A4B586B420E69DDF",
"expire": "1427736345",
"user": "Cylance, Inc."
}

DONE - Example 2
URL: PUT /guid
Input:
{
"user": "Cylance, Inc."
}
Output:
{
"guid": "9094E4C980C74043A4B586B420E69DDF",
"expire": "1427736345",
"user": "Cylance, Inc."
}

# Read
Returns the metadata associated to the given GUID.

DONE - Example 3
URL: GET /guid/9094E4C980C74043A4B586B420E69DDF
Output:
{
"guid": "9094E4C980C74043A4B586B420E69DDF",
"expire": "1427736345",
"user": "Cylance, Inc."
}

# Update
Updates the metadata associated to the given GUID. The GUID itself cannot be
updated using this command.

DONE - Example 4
URL: PUT /guid/9094E4C980C74043A4B586B420E69DDF

Input:
{
"expire": "1427822745",
}

Output:
{
"guid": "9094E4C980C74043A4B586B420E69DDF",
"expire": "1427822745",
"user": "Cylance, Inc."
}

# Delete
Deletes the GUID and its associated data.
DONE - Example 5
URL: DELETE /guid/9094E4C980C74043A4B586B420E69DDF
No output.

# Error code returns
The following response codes should be returned by the service:

200's on accepted/successful requests

400's on client errors

500's on server errors
Suggestions
Use the Tornado web framework for the RESTful interface
Use Redis for the cache
Use MySQL or MongoDB to store data permanently