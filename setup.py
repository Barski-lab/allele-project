from setuptools import setup, find_packages
import os

setup(
    name='allele-project',
    description='Projects allele specific alignments on reference genome',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    version='0.0.1',
    url='https://github.com/Barski-lab/allele-project',
    download_url=('https://github.com/Barski-lab/allele-project'),
    author='Michael Kotliar',
    author_email='misha.kotliar@gmail.com',
    license = 'MIT',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "allele-project=allele_project.main:main"
        ]
    }
)