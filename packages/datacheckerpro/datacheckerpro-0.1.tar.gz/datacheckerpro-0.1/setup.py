from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-16") as file:
    long_description = file.read()
setup(
    name='datacheckerpro',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Okoli Ogechukwu Abimbola',
    author_email='okoliogechi74@gmail.com',
    description="A simple datavalidator for validating email, phone numbers, dates, and URLs.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Data-Epic/data-validator-ogechukw-okoli",
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license_file='LICENSE',
)