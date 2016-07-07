from unittest import TestCase
import boto3
import os
import pickle
from moto import mock_ec2
from ctl.ec2.utils import create_instances, add_to_recent, last_instance, \
    instance_turn_on, instance_turn_off, get_instance_state


# Used in testing recent data storage
data_file_path = os.path.join(
    os.path.dirname(__file__), 'ec2-test.dat'
)


class TestEC2(TestCase):
    def test_add_to_recent(self):
        obj = {
            'number': 7,
            'foo': 'bar'
        }
        add_to_recent(obj, data_path=data_file_path)
        with open(data_file_path, 'rb') as f:
            robj = pickle.load(f)
            self.assertEqual(robj['number'], obj['number'])
            self.assertEqual(robj['foo'], obj['foo'])

    def test_last_instance(self):
        obj = {
            'Instances': [
                {
                    'id': 'selfishghost',
                    'region': 'dreamland'
                }
            ]
        }
        add_to_recent(obj, data_path=data_file_path)
        robj = last_instance(data_path=data_file_path)
        self.assertEqual(robj['id'], obj['Instances'][0]['id'])
        self.assertEqual(robj['region'], obj['Instances'][0]['region'])

    @mock_ec2
    def test_create_instance(self):
        create_instances('us-east-1', 'ami-fce3c696', 1, 1, 'foo', 't2.micro')

        conn = boto3.resource('ec2', region_name='us-east-1')
        instances = conn.instances.all()
        total_instances = 0
        for i in instances:
            total_instances += 1
        self.assertEqual(total_instances, 1)

    @mock_ec2
    def test_create_instances(self):
        create_instances('us-east-1', 'ami-fce3c696', 5, 5, 'foo', 't2.micro')

        conn = boto3.resource('ec2', region_name='us-east-1')
        instances = conn.instances.all()
        total_instances = 0
        for i in instances:
            total_instances += 1
        self.assertEqual(total_instances, 5)

    @mock_ec2
    def test_instance_turn_off(self):
        create_instances('us-east-1', 'ami-fce3c696', 1, 1, 'foo',
                         't2.micro', data_file_path)
        li = last_instance(data_file_path)
        state = instance_turn_off('us-east-1', li['InstanceId'])
        self.assertEqual(state['state'], 'stopping')

    @mock_ec2
    def test_instance_turn_on(self):
        create_instances('us-east-1', 'ami-fce3c696', 1, 1, 'foo',
                         't2.micro', data_file_path)
        li = last_instance(data_file_path)
        state = instance_turn_off('us-east-1', li['InstanceId'])
        self.assertEqual(state['state'], 'stopping')
        state = instance_turn_on('us-east-1', li['InstanceId'])
        self.assertEqual(state['state'], 'pending')

    @mock_ec2
    def test_get_instance_state(self):
        create_instances('us-east-1', 'ami-fce3c696', 1, 1, 'foo',
                         't2.micro', data_file_path)
        li = last_instance(data_file_path)
        state = get_instance_state('us-east-1', li['InstanceId'])
        self.assertEqual(state['state'], 'running')
        instance_turn_off('us-east-1', li['InstanceId'])
        state = get_instance_state('us-east-1', li['InstanceId'])
        self.assertEqual(state['state'], 'stopped')
