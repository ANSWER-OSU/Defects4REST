# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------


#SBATCH -c 4                         
#SBATCH -p dgx2                     
#SBATCH -J API_NAME
#SBATCH --output=slurm_API_NAME.out
#SBATCH --error=slurm_API_NAME.err
#SBATCH --time=7-00:00:00


# Check if an argument was provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <API URL> <GitHub token> <Root dir>"
    exit 1
fi

REPO_URL=$1
GITHUB_TOKEN=$2
ROOT_DIR=$3

python3 github_issue_processor.py --repo-url "$REPO_URL" --token "$GITHUB_TOKEN" --resultpath "$ROOT_DIR"

