# -*- coding: utf-8 -*-
"""This script:
0. allocates more elastic IP addresses if necessary,
1. launches the specified number of nodes (instances) on Amazon EC2,
2. tags them with the specified tag,
3. waits until those instances exist and are running,
4. for each instance, it associates an elastic IP address
   with that instance,
5. writes the shellscript add2known_hosts.sh
6. (over)writes a file named hostlist.py
   containing a list of all public DNS names.
"""

from __future__ import unicode_literals
import time
import argparse
import botocore
import boto3
from awscommon import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    get_naeips,
)

parser = argparse.ArgumentParser()
parser.add_argument("--tag",
                    help="tag to add to all launched instances on AWS",
                    required=True)
parser.add_argument("--nodes",
                    help="number of nodes in the cluster",
                    required=True,
                    type=int)
args = parser.parse_args()

tag = args.tag
num_nodes = int(args.nodes)

# Get an AWS EC2 "resource"
# See http://boto3.readthedocs.org/en/latest/guide/resources.html
ec2 = boto3.resource(service_name='ec2',
                     region_name=AWS_REGION,
                     aws_access_key_id=AWS_ACCESS_KEY_ID,
                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Create a client from the EC2 resource
# See http://boto3.readthedocs.org/en/latest/guide/clients.html
client = ec2.meta.client

# Before launching any instances, make sure they have sufficient
# allocated-but-unassociated EC2 elastic IP addresses
print('Checking if you have enough allocated-but-unassociated ' +
      'EC2 elastic IP addresses...')

non_associated_eips = get_naeips(client)

print('You have {} allocated elactic IPs which are '
      'not already associated with instances'.
      format(len(non_associated_eips)))

if num_nodes > len(non_associated_eips):
    num_eips_to_allocate = num_nodes - len(non_associated_eips)
    print('You want to launch {} instances'.
          format(num_nodes))
    print('so {} more elastic IPs must be allocated'.
          format(num_eips_to_allocate))
    for _ in range(num_eips_to_allocate):
        try:
            # Allocate an elastic IP address
            # response is a dict. See http://tinyurl.com/z2n7u9k
            response = client.allocate_address(DryRun=False, Domain='standard')
        except botocore.exceptions.ClientError:
            print('Something went wrong when allocating an '
                  'EC2 elastic IP address on EC2. '
                  'Maybe you are already at the maximum number allowed '
                  'by your AWS account? More details:')
            raise
        except:
            print('Unexpected error:')
            raise

print('Commencing launch of {} instances on Amazon EC2...'.
      format(num_nodes))

for _ in range(num_nodes):
    # Request the launch of one instance at a time
    # (so list_of_instances should contain only one item)
    list_of_instances = ec2.create_instances(
            ImageId='ami-accff2b1',          # ubuntu-image
            # 'ami-596b7235',                 # ubuntu w/ iops storage
            MinCount=1,
            MaxCount=1,
            KeyName='bigchaindb',
            InstanceType='m3.2xlarge',
            # 'c3.8xlarge',
            # 'c4.8xlarge',
            SecurityGroupIds=['bigchaindb']
            )

    # Tag the just-launched instances (should be just one)
    for instance in list_of_instances:
        time.sleep(5)
        instance.create_tags(Tags=[{'Key': 'Name', 'Value': tag}])

# Get a list of all instances with the specified tag.
# (Technically, instances_with_tag is an ec2.instancesCollection.)
filters = [{'Name': 'tag:Name', 'Values': [tag]}]
instances_with_tag = ec2.instances.filter(Filters=filters)
print('The launched instances will have these ids:'.format(tag))
for instance in instances_with_tag:
    print(instance.id)

print('Waiting until all those instances exist...')
for instance in instances_with_tag:
    instance.wait_until_exists()

print('Waiting until all those instances are running...')
for instance in instances_with_tag:
    instance.wait_until_running()

print('Associating allocated-but-unassociated elastic IPs ' +
      'with the instances...')

# Get a list of elastic IPs which are allocated but
# not associated with any instances.
# There should be enough because we checked earlier and
# allocated more if necessary.
non_associated_eips_2 = get_naeips(client)

for i, instance in enumerate(instances_with_tag):
    print('Grabbing an allocated but non-associated elastic IP...')
    eip = non_associated_eips_2[i]
    public_ip = eip['PublicIp']
    print('The public IP address {}'.format(public_ip))

    # Associate that Elastic IP address with an instance
    response2 = client.associate_address(
        DryRun=False,
        InstanceId=instance.instance_id,
        PublicIp=public_ip
        )
    print('was associated with the instance with id {}'.
          format(instance.instance_id))

# Get a list of the pubic DNS names of the instances_with_tag
hosts_dev = []
for instance in instances_with_tag:
    public_dns_name = getattr(instance, 'public_dns_name', None)
    if public_dns_name is not None:
        hosts_dev.append(public_dns_name)

# Write a shellscript to add remote keys to ~/.ssh/known_hosts
print('Preparing shellscript to add remote keys to known_hosts')
with open('add2known_hosts.sh', 'w') as f:
    f.write('#!/bin/bash\n')
    for public_dns_name in hosts_dev:
        f.write('ssh-keyscan ' + public_dns_name + ' >> ~/.ssh/known_hosts\n')

# Create a file named hostlist.py containing hosts_dev.
# If a hostlist.py already exists, it will be overwritten.
print('Writing hostlist.py')
with open('hostlist.py', 'w') as f:
    f.write('# -*- coding: utf-8 -*-\n')
    f.write('from __future__ import unicode_literals\n')
    f.write('hosts_dev = {}\n'.format(hosts_dev))

# Wait
wait_time = 45
print('Waiting {} seconds to make sure all instances are ready...'.
      format(wait_time))
time.sleep(wait_time)
