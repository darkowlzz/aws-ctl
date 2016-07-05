import click

from utils import LAST_INSTANCE, create_instances, get_instance_state, \
    instance_turn_on, instance_turn_off, kill_instance


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
    create_instances(region, image, mincount, maxcount, keyname, instancetype)


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--image', default='ami-fce3c696',
              prompt='Image ID', help='ID of the AMI.')
@click.option('--keyname', prompt='KeyName',
              help='Name of keypair.')
@click.option('--instancetype', default='t2.micro',
              prompt='Instance Type', help='AWS Instance Type')
def run_instance(region, image, keyname, instancetype):
    """Run EC2 instance"""
    create_instances(region, image, 1, 1, keyname, instancetype)


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--id', default=LAST_INSTANCE,
              prompt='Instance ID', help='The instance\'s id identifier.')
def instance_state(region, id):
    """Get EC2 instance state"""
    response = get_instance_state(region, id)
    if response:
        click.echo('Instance ID: ' + response['id'])
        click.echo('State: ' + response['state'])
    else:
        click.echo('Instance not found')


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--id', default=LAST_INSTANCE,
              prompt='Instance ID', help='The instance\'s id identifier.')
def start_instance(region, id):
    """Start EC2 instance"""
    response = instance_turn_on(region, id)
    click.echo('State: ' + response['state'])


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--id', default=LAST_INSTANCE,
              prompt='Instance ID', help='The instance\'s id identifier.')
def terminate_instance(region, id):
    """Terminate EC2 instance"""
    response = kill_instance(region, id)
    click.echo('State: ' + response['state'])


@ec2.command()
@click.option('--region', default='us-east-1',
              prompt='AWS Region', help='AWS region.')
@click.option('--id', default=LAST_INSTANCE,
              prompt='Instance ID', help='The instance\'s id identifier.')
def stop_instance(region, id):
    """Stop EC2 instance"""
    response = instance_turn_off(region, id)
    click.echo('State: ' + response['state'])
