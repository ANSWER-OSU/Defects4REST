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

import importlib
from defects4rest.src.utils.issue_metadata import get_bug_info

def run(project_name, issue_id=None, action="deploy", buggy=False, patched=None):
    project_key = project_name.lower()
    module_name = f"defects4rest.src.deployment_scripts.deploy_{project_key}"
    print(f"Checking out {module_name}")

    try:
        deploy_module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"No deploy script found for project: '{project_key}'")
        return

    bug_data = get_bug_info(project_key, issue_id)

    if not bug_data:
        print(f"No issue info found for project '{project_name}' issue ID {issue_id}")
        return

    # Select SHA
    sha = None
    if buggy:
        sha = bug_data.get("buggy")
        if not sha:
            print(f"No buggy SHA found for {project_name} bug {issue_id}")
            return

    elif patched is not None:
        patch_list = bug_data.get("patched", [])
        if patched <= 0 or patched > len(patch_list):
            print(f"Invalid patch index. {len(patch_list)} patch(es) available.")
            return
        sha = patch_list[patched - 1]


    if action == "deploy":
        if hasattr(deploy_module, "main"):
            print(f"Deploying {project_name} at SHA: {sha}")
            deploy_module.main(sha, issue_id)
        else:
            print(f"'main' function not implemented in {module_name}")

    elif action == "stop":
        if hasattr(deploy_module, "stop"):
            print(f"Stopping {project_name}...")
            deploy_module.stop()
        else:
            print(f"'stop' function not implemented in {module_name}")

    elif action == "clean":
        if hasattr(deploy_module, "clean"):
            print(f"Cleaning {project_name}...")
            deploy_module.clean()
        else:
            print(f"'clean' function not implemented in {module_name}")

    else:
        print("No action taken. Use --start, --stop, or --clean.")

