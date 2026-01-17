#-------------------------------------------------------------------------------
# Copyright (c) 2026 Rahil Piyush Mehta, Kausar Y. Moshood, Huwaida Rahman Yafie and Manish Motwani
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""NocoDB API script for creating test data for issues."""
import requests

def issue_2242(args):
    """Create test project with City and Country tables and 1000 linked records."""
    PORT = args["port"]

    PROJECT_NAME = "Buggy2242"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    print("\nRunning issue#2242 prerequisites...")

    # Sign up and get auth token
    print(f"Signing up...")
    credentials = requests.post(f"http://localhost:{PORT}/api/v1/db/auth/user/signup", json={"email":"admin@admin.com", "password":"@Admin123"})
    if credentials.status_code == 200 or credentials.status_code == 201:
        print("Signed up.")
    else:
        print(f"Error: Received status code {credentials.text}")

    headers["xc-auth"] = credentials.json().get("token")

    # Create project
    print(f"Creating a project...")
    project = requests.post(f"http://localhost:{PORT}/api/v1/db/meta/projects/", json={"title":PROJECT_NAME}, headers=headers)
    if project.status_code == 200 or project.status_code == 201:
        print("Project created.")
    else:
        print(f"Error: Received status code {project.text}")

    baseId = project.json().get("id")
    print(f"Project ID: {baseId}\n")

    # Create City table
    schemaCity = {
        "title": "City",
        "table_name": "City",
        "columns": [
        { "title": "ID", "column_name": "ID", "uidt": "ID", "pk": "true" },
        { "title": "Title", "column_name": "Title", "uidt": "SingleLineText" }
        ]
    }

    print(f"Creating Table A: City...")
    tableCity = requests.post(f"http://localhost:{PORT}/api/v1/db/meta/projects/{baseId}/tables/", json=schemaCity, headers=headers)
    if project.status_code == 200 or project.status_code == 201:
        print("Table: City created.")
    else:
        print(f"Error: Received status code {project.status_code}")
    tableCity_data = tableCity.json()
    print(f"Table-City ID: {tableCity_data.get({id})}\n")

    # Create Country table
    print(f"Creating Table B: Country...")
    schemaCountry = schemaCountry = {
        "title": "Country",
        "table_name": "Country",
        "columns": [
        { "title": "ID", "column_name": "ID", "uidt": "ID", "pk": "true" },
        { "title": "Title", "column_name": "Title", "uidt": "SingleLineText" }
        ]
    }
    tableCountry = requests.post(f"http://localhost:{PORT}/api/v1/db/meta/projects/{baseId}/tables/", json=schemaCountry, headers=headers)
    if project.status_code == 200 or project.status_code == 201:
        print("Table: Country created.")
    else:
        print(f"Error: Received status code {project.text}")
    tableCountry_data = tableCountry.json()
    print(f"Table-Country ID: {tableCountry_data.get('id')}\n")

    # Create linked record fields between tables
    print(f"Creating a Linked Record Fields...")

    linkedCity = {
        "title": "countryRead",
        "uidt": "LinkToAnotherRecord",
        "parentId": tableCity_data.get("id"),
        "childId": tableCountry_data.get("id"),
        "type": 'mm',
        "onDelete": 'CASCADE'
    };
    linkedCountry = {
        "title": "cityList",
        "uidt": "LinkToAnotherRecord",
        "parentId": tableCountry_data.get("id"),
        "childId": tableCity_data.get("id"),
        "type": 'hm',
    }

    requests.post(f"http://localhost:{PORT}/api/v1/db/meta/tables/{tableCity_data.get('id')}/columns/", json=linkedCity, headers=headers)

    requests.post(f"http://localhost:{PORT}/api/v1/db/meta/tables/{tableCity_data.get('id')}/columns/", json=linkedCountry, headers=headers)

    print("Linked Record fields created.\n")

    # Populate 1000 city records
    print("Populating 1000 records for City...")
    cityRecords = []
    for i in range(1,1000):
        cityRecords.append({"Title": f"City {i}"})
    requests.post(f"http://localhost:{PORT}/api/v1/db/data/bulk/noco/{PROJECT_NAME}/City/", json=cityRecords, headers=headers)
    print("City records populated.\n")

    # Populate country records
    print("Populating records for Country...")
    requests.post(f"http://localhost:{PORT}/api/v1/db/data/bulk/noco/{PROJECT_NAME}/Country/", json=[{"Title": "Country 1"}, {"Title": "Country 2"}], headers=headers)
    print("Country records populated.\n")

    # Create linked records between cities and countries
    print("Populating linked records...")
    for i in range(1,1000):
        requests.post(f"http://localhost:{PORT}/api/v1/db/data/noco/{PROJECT_NAME}/City/{i}/mm/countryRead/1", headers=headers)

    for i in range(1,1000):
        requests.post(f"http://localhost:{PORT}/api/v1/db/data/noco/{PROJECT_NAME}/Country/1/hm/cityList/{i}", headers=headers)

    print("Linked records populated.\n")

    print("Prequisites done.")
    print("You can now move to Triggering Behavior.\n")