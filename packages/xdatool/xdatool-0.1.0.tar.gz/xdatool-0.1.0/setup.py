from setuptools import setup, find_packages

setup(
    name='xdatool',  # Changed unique name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': [
            'kingalters-devkey=devkey.cli:main',  # Updated entry point
        ],
    },
    include_package_data=True,
    package_data={
        'devkey': ['*.json', '*.yaml', '*.yml'],
    },
    author='kingalters',
    author_email='someone@example.com',
    description='A description of your dev key module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kingalters/kingalters-devkey',  # Updated URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)