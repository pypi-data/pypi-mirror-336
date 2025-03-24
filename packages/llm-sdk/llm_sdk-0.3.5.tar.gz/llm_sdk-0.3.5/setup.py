from setuptools import setup, find_packages

setup(
    name='llm-sdk',
    version='0.3.5',
    author='Olsi Hoxha',
    author_email='olsihoxha824@gmail.com',
    description='SDK to get all the available LLM models per Provider',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
        'pydantic'
    ],
    python_requires='>=3.6',
    package_data={
        'llm_sdk': ['*'],
    },
    include_package_data=True,
)