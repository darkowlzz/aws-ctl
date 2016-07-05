from unittest import TestCase
import boto3
from moto import mock_ec2
from ctl.ec2.utils import create_instances


class TestEC2(TestCase):
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
