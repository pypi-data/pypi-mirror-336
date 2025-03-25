from setuptools import setup, find_packages

setup(
    name='aws_services',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['boto3'],
    author='Your Name',
    author_email='cvedant136@gmail.com',
    description='Reusable AWS integration library (Lambda, SQS, SNS, etc.)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/x23393131/aws_services',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
