from setuptools import setup
import os

setup(
    name='localizesh-processor-rst',
    version=os.environ.get('VERSION'),
    description="Localize.sh RST processor",
    package_dir={"localizesh_processor_rst": "src"},
    long_description=open('README.md').read(),
    install_requires=[
        "localizesh-sdk>=0.1.4",
        "docutils>=0.21.2",
        "parameterized>=0.9.0",
    ],
)

