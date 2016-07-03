import click


@click.group()
def s3():
    """S3 controller"""
    pass


@s3.command()
def create_bucket():
    """Create S3 bucket"""
    click.echo('Creating bucket...')
