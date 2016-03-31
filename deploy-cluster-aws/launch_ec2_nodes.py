# -*- coding: utf-8 -*-
"""This script:
1. Launches the specified number of nodes (instances) on Amazon EC2,
2. tags them with the specified tag,
3. waits until those instances exist and are running,
4. for each instance, allocates an elastic IP address
   and associates it with that instance, and
5. creates three files:
   * add2known_hosts.sh
   * add2dbconf
   * hostlist.py
"""

from __future__ import unicode_literals
import os
import time
import argparse
import botocore
import boto3


def get_naeips(client0):
    """Get a list of non-associated elastic IP addresses (NAEIPs) on EC2.

    Args:
        client0: A client created from an EC2 resource.
                 e.g. client0 = ec2.meta.client
                 See http://boto3.readthedocs.org/en/latest/guide/clients.html

    Returns:
        A list of NAEIPs in the EC2 account associated with the client.
        To interpret the contents, see http://tinyurl.com/hrnuy74
    """
    # response is a dict with 2 keys: Addresses and ResponseMetadata
    # See http://tinyurl.com/hrnuy74
    response = client0.describe_addresses()
    allocated_eips = response['Addresses']
    non_associated_eips = []
    for eip in allocated_eips:
        if 'InstanceId' not in eip:
            non_associated_eips.append(eip)
    return non_associated_eips


AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION = os.environ['AWS_REGION']

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
# allocated-but-unassociated EC2-Classic elastic IP addresses
print('Checking if you have enough allocated-but-unassociated ' +
      'EC2-Classic elastic IP addresses...')

non_associated_eips = get_naeips(client)

print('You have {} allocated elactic IPs which are '
      'not already associated with instances'.
      format(len(non_associated_eips)))

# Note that the allocated addresses may include
# EC2-Classic and EC2-VPC elastic IP addresses.
# For now, I will assume that doesn't matter.
# -Troy

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
                  'EC2-Classic elastic IP address on EC2. '
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

wait_time = 45
print('Waiting {} seconds to make sure all instances are ready...'.
      format(wait_time))
time.sleep(wait_time)

# Get a list of the pubic DNS names of the instances_with_tag
publist = []
for instance in instances_with_tag:
    public_dns_name = getattr(instance, 'public_dns_name', None)
    if public_dns_name is not None:
        publist.append(public_dns_name)

# Create shellscript add2known_hosts.sh for adding remote keys to known_hosts
with open('add2known_hosts.sh', 'w') as f:
    f.write('#! /bin/bash\n')
    for public_dns_name in publist:
        f.write('ssh-keyscan ' + public_dns_name + ' >> ~/.ssh/known_hosts\n')

# Create a file named add2dbconf, overwriting one if it already exists
with open('add2dbconf', 'w') as f:
    f.write('## The host:port of a node that RethinkDB will connect to\n')
    for public_dns_name in publist:
        f.write('join=' + public_dns_name + ':29015\n')

# Note: The original code by Andreas wrote a file with lines of the form
#       join=public_dns_name_0:29015
#       join=public_dns_name_1:29015
#       but it stopped about halfway through the list of public_dns_names
#       (publist). In principle, it's only strictly necessary to
#       have one join= line.
#       Maybe Andreas thought that more is better, but all is too much?
#       Below is Andreas' original code. -Troy
# localFile = open('add2dbconf', 'w')
# before = 'join='
# after = ':29015'
# localFile.write('## The host:port of a node that rethinkdb will connect to\n')
# for entry in range(0,int(len(publist)/2)):
#     localFile.write(before + publist[entry] + after + '\n')

# Create a file named hostlist.py, overwriting one if it already exists
with open('hostlist.py', 'w') as f:
    f.write('hosts_dev = {}'.format(publist))
