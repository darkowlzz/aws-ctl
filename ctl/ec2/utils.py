import pickle
import boto3
import os
import ctl

DATA_DIR = 'data'
DATA_FILE = 'ec2.dat'
LAST_INSTANCE = 'use last available instance'

ctrl_home_dir = os.path.dirname(
    os.path.dirname(os.path.realpath(ctl.__file__))
)
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
    try:
        with open(ctrl_data_file_path, 'rb') as f:
            return pickle.load(f)['Instances'][0]
    except EOFError:
        return None


# Create EC2 instances and add the response to ec2 recent
def create_instances(region, image, mincount, maxcount, keyname, instancetype):
    client = boto3.client('ec2', region_name=region)
    response = client.run_instances(
        ImageId=image,
        MinCount=mincount,
        MaxCount=maxcount,
        KeyName=keyname,
        InstanceType=instancetype
    )
    add_to_recent(response)


# Get instance state details
def get_instance_state(region, id):
    ec2 = boto3.resource('ec2', region_name=region)
    if id == LAST_INSTANCE:
        li = last_instance()
        if li:
            instance = ec2.Instance(li['InstanceId'])
        else:
            return None
    else:
        instance = ec2.Instance(id)
    return {
        'id': instance.instance_id,
        'state': instance.state['Name']
    }


# Start an instance from Stop state
def instance_turn_on(region, id):
    client = boto3.client('ec2', region_name=region)
    if id == LAST_INSTANCE:
        li = last_instance()
        id = li['InstanceId']

    resp = client.start_instances(
        InstanceIds=[id]
    )
    return {'state': resp['StartingInstances'][0]['CurrentState']['Name']}


# Stop an instance from Running state
def instance_turn_off(region, id):
    client = boto3.client('ec2', region_name=region)
    if id == LAST_INSTANCE:
        li = last_instance()
        id = li['InstanceId']

    resp = client.stop_instances(
        InstanceIds=[id]
    )
    return {'state': resp['StoppingInstances'][0]['CurrentState']['Name']}


# Terminate an instance
def kill_instance(region, id):
    client = boto3.client('ec2', region_name=region)
    if id == LAST_INSTANCE:
        li = last_instance()
        id = li['InstanceId']

    resp = client.terminate_instances(
        InstanceIds=[id]
    )
    return {'state': resp['TerminatingInstances'][0]['CurrentState']['Name']}
