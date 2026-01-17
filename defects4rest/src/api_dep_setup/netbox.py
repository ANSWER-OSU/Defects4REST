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

"""NetBox API setup script for creating test data for specific issues."""
import requests
import time
import subprocess
from defects4rest.src.utils.shell import run, pretty_section, pretty_step
import json

def check_server_status():
    """Check if NetBox API is responding with retries."""
    pretty_step("Checking service status")

    max_retries = 4
    retry_delay = 30
    for attempt in range(1, max_retries + 1):
        try:
            run([
                'curl', '-X', 'GET',
                'http://localhost:8080/api/',
                '-H', 'accept: application/json',
                '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567'
            ])
            pretty_step("Command succeeded!")
            break

        except subprocess.CalledProcessError as e:
            if e.returncode == 56:
                if attempt < max_retries:
                    pretty_step(
                        f"Connection reset detected. Retrying in {retry_delay} seconds... (attempt {attempt}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    pretty_step("Max retries reached. Giving up.", "red")
                    raise
            else:
                pretty_step(f"Different error occurred (exit code {e.returncode})", "red")
                raise

def issue_18363(args):
    """Create test data for issue 18363: site, cluster, VM, and interface."""
    pretty_section("Running the pre requisite for issue 18363")

    check_server_status()

    pretty_step("Step 1: Create a site")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/dcim/sites/',
        '-H', 'accept: application/json',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-d', '{"name": "Test Site", "slug": "test-site"}'
    ])

    pretty_step("Step 2: Create a cluster type")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/cluster-types/',
        '-H', 'accept: application/json',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-d', '{"name": "VMware", "slug": "vmware"}'
    ])

    pretty_step("Step 3: Create a cluster")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/clusters/',
        '-H', 'accept: application/json',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-d', '{"name": "Test Cluster", "type": 1}'
    ])

    pretty_step("Step 4: Create a virtual machine")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/virtual-machines/',
        '-H', 'accept: application/json',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-d', '{"name": "test-vm", "status": "active", "cluster": 1}'
    ])

    pretty_step("Step 5: Create an interface on the virtual machine")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/interfaces/',
        '-H', 'accept: application/json',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-d', '{"virtual_machine": 1, "name": "eth0", "type": "virtual"}'
    ])

def issue_18368(args):
    """Create test data for issue 18368: MAC address without tags."""
    pretty_section("Running the pre requisite for issue 18368")
    check_server_status()

    pretty_step("Step 1: Create a MAC address WITHOUT tags")

    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/dcim/mac-addresses/',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-H', 'Content-Type: application/json',
        '-d', '{"mac_address": "00:11:22:33:44:55"}'
    ])

def issue_18447(args):
    """Create test data for issue 18447: cluster, VM, and multiple interfaces."""
    pretty_section("Running the pre requisite for issue 18447")
    check_server_status()

    pretty_step("Step 1: Create a Cluster Type")

    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/cluster-types/',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-H', 'Content-Type: application/json',
        '-d', '{"name": "VMware", "slug": "vmware"}'
    ])

    pretty_step("Step 2: Create a Cluster (using the type ID)")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/clusters/',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-H', 'Content-Type: application/json',
        '-d', '{"name": "Test-Cluster", "type": 1}'
    ])

    pretty_step("Step 3: Create a Virtual Machine")
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/virtual-machines/',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-H', 'Content-Type: application/json',
        '-d', '{"name": "test-vm-01", "cluster": 1, "status": "active"}'
    ])

    pretty_step("Step 4: Create Multiple Interfaces")
    # First interface
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/interfaces/',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-H', 'Content-Type: application/json',
        '-d', '{"name": "eth0", "virtual_machine": 1, "enabled": true}'
    ])
    # Second interface
    run([
        'curl', '-X', 'POST',
        'http://localhost:8080/api/virtualization/interfaces/',
        '-H', 'Authorization: Token 0123456789abcdef0123456789abcdef01234567',
        '-H', 'Content-Type: application/json',
        '-d', '{"name": "et10", "virtual_machine": 1, "enabled": true}'
    ])

def issue_18991(args):
    """Create test data for issue 18991: devices, ports, and cable connections."""
    pretty_section("Running the pre requisite for issue 18991")
    check_server_status()

    pretty_step("Step 1: Create a Site")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/sites/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "name": "Test Site",
            "slug": "test-site"
        })
        ]
    )

    pretty_step("Step 2: Create a Manufacturer")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/manufacturers/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "name": "Test Manufacturer",
            "slug": "test-manufacturer"
        })
        ]
    )

    pretty_step("Step 3: Create a Device Type with Front and Rear Ports")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/device-types/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "manufacturer": 1,
            "model": "Patch Panel 24",
            "slug": "patch-panel-24"
        })
        ]
    )

    pretty_step("Step 4: Create a Device Role")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/device-roles/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "name": "Patch Panel",
            "slug": "patch-panel",
            "color": "9e9e9e"
        })
        ]
    )

    pretty_step("Step 5: Create a Device")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/devices/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "name": "patch-panel-01",
            "device_type": 1,
            "role": 1,
            "site": 1
        })
        ]
    )

    pretty_step("Step 6: Create a Rear Port Template (for the device type)")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/rear-port-templates/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "device_type": 1,
            "name": "Rear Port 1",
            "type": "8p8c",
            "positions": 1
        })
        ]
    )

    pretty_step("Step 7: Create a Front Port Template (for the device type)")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/front-port-templates/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "device_type": 1,
            "name": "Front Port 1",
            "type": "8p8c",
            "rear_port": 1,
            "rear_port_position": 1
        })
        ]
    )

    pretty_step("Step 8: Create Rear Port on Device")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/rear-ports/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "device": 1,
            "name": "Rear Port 1",
            "type": "8p8c",
            "positions": 1
        })
        ]
    )

    pretty_step("Step 9: Create Front Port on Device")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/front-ports/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "device": 1,
            "name": "Front Port 1",
            "type": "8p8c",
            "rear_port": 1,
            "rear_port_position": 1
        })
        ]
    )

    pretty_step("Step 10: Create a Second Device (for cable connection)")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/devices/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "name": "switch-01",
            "device_type": 1,
            "role": 1,
            "site": 1
        })
        ]
    )

    pretty_step("Step 11: Create an Interface on Second Device")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/interfaces/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "device": 2,
            "name": "eth0",
            "type": "1000base-t"
        })
        ]
    )

    pretty_step("Step 12: Create a Cable connecting Front Port to Interface")
    run(
        [
            "curl",
            "-X", "POST",
            f"http://localhost:8080/api/dcim/cables/",
            "-H", f"Authorization: Token 0123456789abcdef0123456789abcdef01234567",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps({
            "a_terminations": [
                {
                    "object_type": "dcim.frontport",
                    "object_id": 1
                }
            ],
            "b_terminations": [
                {
                    "object_type": "dcim.interface",
                    "object_id": 1
                }
            ],
            "type": "cat6"
        })
        ]
    )