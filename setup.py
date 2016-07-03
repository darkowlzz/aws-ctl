from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='aws-ctl',
    version='0.1',
    description='AWS Controller',
    long_description=readme(),
    author='darkowlzz',
    author_email='me@darkowlzz.space',
    license='MIT',
    packages=['ctl'],
    install_requires=['click', 'boto3', 'flake8'],
    entry_points='''
        [console_scripts]
        ec2-ctl=ctl.ec2:ec2
        s3-ctl=ctl.s3:s3
    ''',
    zip_safe=False
)
