import click
import pickle
import boto3
import os

DATA_DIR = 'data'
DATA_FILE = 'ec2.dat'
LAST_INSTANCE = 'use last available instance'

ctrl_home_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ctrl_data_dir_path = os.path.join(ctrl_home_dir, DATA_DIR)
ctrl_data_file_path = os.path.join(ctrl_data_dir_path, DATA_FILE)

if not os.path.exists(ctrl_data_dir_path):
    os.makedirs(ctrl_data_dir_path)


# Add an object to recent persistent storage
def add_to_recent(obj):
    with open(ctrl_data_file_path, 'wb') as f:
        pickle.dump(obj, f)


# Return the last available instance
def last_instance():
    with open(ctrl_data_file_path, 'rb') as f:
        return pickle.load(f)['Instances'][0]


@click.group()
def ec2():
    """EC2 controller"""
    pass


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--image', default='ami-fce3c696',
              prompt='Image ID', help='ID of the AMI.')
@click.option('--mincount', default=1, prompt='Min Count',
              help='Minimum number of instances to launch.')
@click.option('--maxcount', default=1, prompt='Max Count',
              help='Maximum number of instances to launch.')
@click.option('--keyname', prompt='KeyName',
              help='Name of keypair.')
@click.option('--instancetype', default='t2.micro',
              prompt='Instance Type', help='AWS Instance Type')
def run_instances(region, image, mincount, maxcount, keyname, instancetype):
    """Run EC2 instances"""
    client = boto3.client('ec2', region_name=region)
    response = client.run_instances(
        ImageId=image,
        MinCount=mincount,
        MaxCount=maxcount,
        KeyName=keyname,
        InstanceType=instancetype
    )
    add_to_recent(response)


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--id', default=LAST_INSTANCE,
              prompt='Instance ID', help='The instance\'s id identifier.')
def instance_state(region, id):
    """Get EC2 instance state"""
    ec2 = boto3.resource('ec2', region_name=region)
    if id == LAST_INSTANCE:
        li = last_instance()
        instance = ec2.Instance(li['InstanceId'])
    else:
        instance = ec2.Instance(id)
    click.echo('Instance ID: ' + instance.instance_id)
    click.echo('State: ' + instance.state['Name'])


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--id', default=LAST_INSTANCE,
              prompt='Instance ID', help='The instance\'s id identifier.')
def terminate_instance(region, id):
    """Terminate EC2 instance"""
    client = boto3.client('ec2', region_name=region)
    if id == LAST_INSTANCE:
        li = last_instance()
        id = li['InstanceId']

    resp = client.terminate_instances(
        InstanceIds=[id]
    )
    click.echo(
        'State: ' +
        resp['TerminatingInstances'][0]['CurrentState']['Name']
    )
