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

"""Kafka REST API setup script for creating test data for specific issues."""
import subprocess
from defects4rest.src.utils.shell import pretty_step, pretty_section

def issue_37(args):
    """Create test topics for issue 37."""
    pretty_section("Running the prerequisites for issue#475...")

    pretty_step("Creating topics...")
    # Create topicA
    subprocess.run(
        [
            "docker", "exec", "kafka-broker",
            "kafka-topics",
            "--create",
            "--topic", "topicA",
            "--bootstrap-server", "localhost:9092",
            "--partitions", "1",
            "--replication-factor", "1",
        ]
    )

    # Create topicB
    subprocess.run(
        [
            "docker", "exec", "kafka-broker",
            "kafka-topics",
            "--create",
            "--topic", "topicB",
            "--bootstrap-server", "localhost:9092",
            "--partitions", "1",
            "--replication-factor", "1",
        ]
    )

    # Verify topics via REST API
    subprocess.run(
        ["curl", "http://localhost:8082/topics"]
    )

    pretty_section("Prerequisites setup finished.")

def issue_475(args):
    """Create compressed topic with test messages for issue 475."""
    pretty_section("Running the prerequisites for issue#475...")

    # Create topic with gzip compression
    pretty_step("Creating compressed topic...")
    subprocess.run(
        [
            "docker", "exec", "kafka-broker",
            "kafka-topics",
            "--create",
            "--topic", "compressed-topic",
            "--bootstrap-server", "localhost:9092",
            "--partitions", "1",
            "--replication-factor", "1",
            "--config", "compression.type=gzip",
        ],
        check=True
    )

    # Produce 300 small messages to test compression
    pretty_step("Producing small messages to compressed topic...")
    messages = "\n".join(f"msg-{i}" for i in range(1, 301)) + "\n"
    subprocess.run(
        [
            "docker", "exec", "-i", "kafka-broker",
            "kafka-console-producer",
            "--broker-list", "localhost:9092",
            "--topic", "compressed-topic",
            "--producer-property", "compression.type=gzip",
        ],
        input=messages,
        text=True,
        check=True
    )

    pretty_section("Prerequisites setup finished.")