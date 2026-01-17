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

"""SeaweedFS API setup script for creating test data for issues."""
import boto3
import random
import string

def issue_6576(args):
    """
    Create S3 bucket with test object and generate presigned URL for issue 6576.
    Tests x-id=GetObject parameter handling bug.
    """
    S3_URL = args.get("s3_url", "http://127.0.0.1:8333")
    ACCESS_KEY = "power_user_key"
    SECRET_KEY = "power_user_secret"

    # Generate random bucket name
    bucket_name = f"bug-demo-bucket-{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
    object_name = "hello.txt"

    # Connect to SeaweedFS S3 API
    s3_client = boto3.client(
        "s3",
        endpoint_url=S3_URL,
        region_name="us-east-1",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    # Create test bucket
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    except Exception as e:
        print(f"Bucket already exists or could not be created: {e}")

    # Upload sample test object
    sentinel_content = b"Hello SeaweedFS"
    s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=sentinel_content)
    print(f"Uploaded sample object '{object_name}'.")

    # Generate presigned URL with 10 minute expiry
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=600
    )

    # Add x-id parameter to trigger the bug
    presigned_url += "&x-id=GetObject"

    print("\n=== Pre-requisite complete ===")
    print(f"Presigned URL (valid 10 minutes):\n{presigned_url}\n")
    print("You can now use this URL in curl to trigger defect #6576.\n")

    # Return test data for automated testing
    return {
        "bucket": bucket_name,
        "object": object_name,
        "url": presigned_url
    }