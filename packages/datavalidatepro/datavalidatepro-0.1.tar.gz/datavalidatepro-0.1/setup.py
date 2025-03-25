from setuptools import setup, find_packages


setup(
    name='datavalidatepro',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Okoli Ogechukwu Abimbola',
    author_email='okoliogechi74@gmail.com',
    description="A simple datavalidator for validating email, phone numbers, dates, and URLs."
    "TO validate Url's, use the validate_url() method"
    "For that of phone numbers, use the Validate_phone() method."
    "Also users can validate a phone_number from 6 continents by using the continentname_numbers etc"
    "For that of emails use the Validate_email() method."
    "Lastly,to validate dates, use the  validate_date method. Note: These methods return a boolean True if valid and False if Invalid",
    long_description_content_type='text/markdown',
    url="https://github.com/Data-Epic/data-validator-ogechukwu-okoli",
    classifiers=[
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license_file='LICENSE',
)