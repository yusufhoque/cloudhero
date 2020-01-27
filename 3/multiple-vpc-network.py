# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create nodejs template with the back-end and front-end templates."""


COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GlobalComputeUrl(project, collection, name):
    return ''.join([COMPUTE_URL_BASE, 'projects/', project, '/global/', collection, '/', name])

def GenerateConfig(context):
    """Generate configuration."""
    resources = [{
        'name': 'managementnet',
        'type': 'compute.v1.network',
        'properties': {
            'autoCreateSubnetworks': False
        }
    }, {
        'name': 'managementsubnet-us',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.managementnet.selfLink)',
            'region': 'us-central1',
            'ipCidrRange': '10.130.0.0/20'
        }
    }, {
        'name': 'privatenet',
        'type': 'compute.v1.network',
        'properties': {
            'autoCreateSubnetworks': False
        }
    }, {
        'name': 'privatesubnet-us',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.privatenet.selfLink)',
            'region': 'us-central1',
            'ipCidrRange': '172.16.0.0/24'
        }
    }, {
        'name': 'privatesubnet-eu',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.privatenet.selfLink)',
            'region': 'europe-west1',
            'ipCidrRange': '172.20.0.0/20'
        }
    }, {
        'name': 'managementnet-allow-icmp-ssh-rdp',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.managementnet.selfLink)',
            'sourceRanges': [ '0.0.0.0/0'],
            'allowed': [{
                'IPProtocol': 'tcp',
                'ports': [ 22,3389 ]
            }, {
                'IPProtocol': 'icmp'
            }]
        }
    }, {
        'name': 'privatenet-allow-icmp-ssh-rdp',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.privatenet.selfLink)',
            'sourceRanges': [ '0.0.0.0/0'],
            'allowed': [{
                'IPProtocol': 'tcp',
                'ports': [ 22,3389 ]
            }, {
                'IPProtocol': 'icmp'
            }]
        }
    }, {
        'name': 'vm-appliance',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': 'us-central1-c',
            'machineType': 'zones/us-central1-c/machineTypes/n1-standard-4',
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-9'
                }
            }],
            'networkInterfaces': [{
                'subnetwork': '$(ref.privatesubnet-us.selfLink)',
                'accessConfigs': [{
                    'name': 'external-nat',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }, {
                'subnetwork': '$(ref.managementsubnet-us.selfLink)'
            }, {
                'network': GlobalComputeUrl(context.env['project'], 'networks', 'default')
            }]
        }
    }, {
        'name': 'managementnet-us-vm',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': 'us-central1-c',
            'machineType': 'zones/us-central1-c/machineTypes/f1-micro',
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-9'
                }
            }],
            'networkInterfaces': [{
                'subnetwork': '$(ref.managementsubnet-us.selfLink)',
                'accessConfigs': [{
                    'name': 'external-nat',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }]
        }
    }, {
        'name': 'privatenet-us-vm',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': 'us-central1-c',
            'machineType': 'zones/us-central1-c/machineTypes/n1-standard-1',
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-9'
                }
            }],
            'networkInterfaces': [{
                'subnetwork': '$(ref.privatesubnet-us.selfLink)',
                'accessConfigs': [{
                    'name': 'external-nat',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }]
        }
    }]
    return {'resources': resources}