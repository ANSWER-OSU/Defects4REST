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
from defects4rest.src.utils.shell import pretty_section, pretty_step

def create_account(port, endpoint):
    """Create a user account."""
    pretty_step(f"Creating a user account...")
    credentials = requests.post(f"http://localhost:{port}/{endpoint}", json={"email":"admin@admin.com", "password":"@Admin123"})
    if credentials.status_code == 200 or credentials.status_code == 201:
        pretty_step("   Account created.")
        return credentials
    else:
        pretty_step(f"Error: Received status code {credentials.text}")

def issue_2242(args):
    """Create test project with City and Country tables and 1000 linked records."""
    PORT = args["port"]

    PROJECT_NAME = "Buggy2242"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    pretty_section("Running issue#2242 prerequisites...")

    # Sign up and get auth token
    pretty_step(f"Signing up...")
    credentials = create_account(PORT, "api/v1/db/auth/user/signup")

    headers["xc-auth"] = credentials.json().get("token")

    # Create project
    pretty_step(f"Creating a project...")
    project = requests.post(f"http://localhost:{PORT}/api/v1/db/meta/projects/", json={"title":PROJECT_NAME}, headers=headers)
    if project.status_code == 200 or project.status_code == 201:
        pretty_step("Project created.")
    else:
        pretty_step(f"Error: Received status code {project.text}")

    baseId = project.json().get("id")
    pretty_step(f"  Project ID: {baseId}")

    # Create City table
    schemaCity = {
        "title": "City",
        "table_name": "City",
        "columns": [
        { "title": "ID", "column_name": "ID", "uidt": "ID", "pk": "true" },
        { "title": "Title", "column_name": "Title", "uidt": "SingleLineText" }
        ]
    }

    pretty_step(f"Creating Table A: City...")
    tableCity = requests.post(f"http://localhost:{PORT}/api/v1/db/meta/projects/{baseId}/tables/", json=schemaCity, headers=headers)
    if project.status_code == 200 or project.status_code == 201:
        pretty_step("   Table: City created.")
    else:
        pretty_step(f"  Error: Received status code {project.status_code}")
    tableCity_data = tableCity.json()
    pretty_step(f"  Table-City ID: {tableCity_data.get('id')}")

    # Create Country table
    pretty_step(f"Creating Table B: Country...")
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
        pretty_step("   Table: Country created.")
    else:
        pretty_step(f"  Error: Received status code {project.text}")
    tableCountry_data = tableCountry.json()
    pretty_step(f"  Table-Country ID: {tableCountry_data.get('id')}")

    # Create linked record fields between tables
    pretty_step(f"Creating a Linked Record Fields...")

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

    pretty_step("   Linked Record fields created.")

    # Populate 1000 city records
    pretty_step("Populating 1000 records for City...")
    cityRecords = []
    for i in range(1,1000):
        cityRecords.append({"Title": f"City {i}"})
    requests.post(f"http://localhost:{PORT}/api/v1/db/data/bulk/noco/{PROJECT_NAME}/City/", json=cityRecords, headers=headers)
    pretty_step("   City records populated.")

    # Populate country records
    pretty_step("Populating records for Country...")
    requests.post(f"http://localhost:{PORT}/api/v1/db/data/bulk/noco/{PROJECT_NAME}/Country/", json=[{"Title": "Country 1"}, {"Title": "Country 2"}], headers=headers)
    pretty_step("   Country records populated.")

    # Create linked records between cities and countries
    pretty_step("Populating linked records...")
    for i in range(1,1000):
        requests.post(f"http://localhost:{PORT}/api/v1/db/data/noco/{PROJECT_NAME}/City/{i}/mm/countryRead/1", headers=headers)

    for i in range(1,1000):
        requests.post(f"http://localhost:{PORT}/api/v1/db/data/noco/{PROJECT_NAME}/Country/1/hm/cityList/{i}", headers=headers)

    pretty_step("   Linked records populated.")

    pretty_step("Prequisites done.")
    pretty_step("You can now move to Triggering Behavior.\n")
    pretty_step("Use the following credentials to sign in:")
    pretty_step("  Super User: admin@admin.com")
    pretty_step("  Password: @Admin123")

def issue_1756(args):
    port = args["port"]

    request = create_account(port, "api/v1/db/auth/user/signup")

    pretty_step("Use the following credentials to sign in:")
    pretty_step("  Super User: admin@admin.com")
    pretty_step("  Password: @Admin123")

def issue_1866(args):
    port = args["port"]

    request = create_account(port, "api/v1/db/auth/user/signup")

    pretty_step("Use the following credentials to sign in:")
    pretty_step("  Super User: admin@admin.com")
    pretty_step("  Password: @Admin123")

def issue_1981(args):
    port = args["port"]

    request = create_account(port, "api/v1/db/auth/user/signup")

    pretty_step("Use the following credentials to sign in:")
    pretty_step("  Super User: admin@admin.com")
    pretty_step("  Password: @Admin123")

def issue_2776(args):
    port = args["port"]

    request = create_account(port, "api/v1/db/auth/user/signup")

    pretty_step("Use the following credentials to sign in:")
    pretty_step("  Super User: admin@admin.com")
    pretty_step("  Password: @Admin123")

def issue_7535(args):
    port = args["port"]

    request = create_account(port, "api/v1/auth/user/signup")

    pretty_step("Use the following credentials to sign in:")
    pretty_step("  Super User: admin@admin.com")
    pretty_step("  Password: @Admin123")

