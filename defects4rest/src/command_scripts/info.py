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

"""
Defects4Rest bug information retrieval and display module.

This module provides functionality to read and display bug/defect information
from CSV files stored in the defects4rest package data directory.
"""
import pandas as pd
import textwrap
from defects4rest.src.utils.resources import data_csv
from defects4rest.src.utils.shell import pretty_section , pretty_step

def run(project_name, issue_id):
    """
    Display detailed bug information for a specific project and issue.

    Reads bug data from the project's CSV file and prints formatted information
    including metadata, patch messages, patched files, file types, and SHAs.

    Returns:
        None: Prints information to stdout or error messages if not found.
    """
    # Get the path to the project's CSV file
    pretty_section(f"{project_name.capitalize()} (Issue #{issue_id})")
    csv_res = data_csv(project_name)
    print(f"Reading: {csv_res}")

    # Check if the CSV file exists before attempting to read it
    if not csv_res.is_file():
        pretty_section(f"Project not found{f' at: {csv_res}'} ",color='red')
        return

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(str(csv_res))

    # Filter the DataFrame to find the row matching the given issue_id
    row = df[df["issue_no"] == issue_id]

    # Check if the issue was found in the DataFrame
    if row.empty:
        print(f"Bug ID {issue_id} not found{f' in: {csv_res}'}")
        return


    row = row.iloc[0]
    # Create a text wrapper for formatting long text to 90 characters per line
    wrapper = textwrap.TextWrapper(width=90, break_long_words=False)

    print("\nProject Metadata")
    print(f"Project       : {project_name}")
    print(f"Bug ID        : {issue_id}")
    print(f"Issue Number  : {row.get('issue_no', 'N/A')}")
    print(f"Issue URL     : {row.get('issue_url', 'N/A')}")
    print(f"Title         : {row.get('title', 'N/A')}")
    print(f"Days to Fix   : {row.get('days_to_fix', 'N/A')}")

    # Display patch commit messages if they exist
    if "patch_msgs" in row and pd.notna(row["patch_msgs"]):
        print("\nPatch Commit Message(s)")
        # Split multiple messages by " | " delimiter and display each one
        for msg in str(row["patch_msgs"]).split(" | "):
            msg = msg.strip()
            if msg:
                # Use the text wrapper to format long commit messages
                print("- " + wrapper.fill(msg))

    # Display the list of patched files if available
    if "patched_files" in row and pd.notna(row["patched_files"]):
        print("\nPatched Files")
        # Split multiple file paths by " | " delimiter
        for f in str(row["patched_files"]).split(" | "):
            f = f.strip()
            if f:
                print("- " + f)

    # Display the types of files that were patched
    if "patched_file_types" in row and pd.notna(row["patched_file_types"]):
        # Use a set to remove duplicate file types
        types = {t.strip() for t in str(row["patched_file_types"]).split(" | ") if t.strip()}
        print("\nPatched File Types")
        # Sort the types alphabetically before displaying
        for t in sorted(types):
            print("- " + t)

    print("\nSHAs")
    buggy_sha = row.get("buggy_sha", "N/A")
    print(f"Buggy SHA     : {buggy_sha}")

    # Handle patch SHAs which may contain multiple values
    patch_sha_field = row.get("patch_sha", "N/A")
    if patch_sha_field != "N/A" and pd.notna(patch_sha_field):
        # Split multiple patch SHAs by " | " delimiter
        patch_shas = [sha.strip() for sha in str(patch_sha_field).split(" | ") if sha.strip()]
        if patch_shas:
            # Display the first patch SHA on the main line
            print(f"Patch SHA(s)  : {patch_shas[0]}")
            # Display any additional patch SHAs with aligned indentation
            for sha in patch_shas[1:]:
                print("                " + sha)
        else:
            print("Patch SHA(s)  : N/A")
    else:
        print("Patch SHA(s)  : N/A")

    pretty_section(f" ")