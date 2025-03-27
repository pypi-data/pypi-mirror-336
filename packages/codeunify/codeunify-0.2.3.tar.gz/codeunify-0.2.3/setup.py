from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup function
setup(
    name='codeunify',
    version='0.2.3',
    description='A library to combine multiple code files into one for easier AI context and error analysis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Phillip Chananda', 
    author_email='takuphilchan@gmail.com',  
    url='https://github.com/takuphilchan/codeunify', 
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    entry_points={
        "console_scripts": [
            "codeunify=codeunify.core.combine:main",
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',  # Update according to the status of your library
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    project_urls={
        "Bug Tracker": "https://github.com/takuphilchan/codeunify/issues", 
        "Documentation": "https://github.com/takuphilchan/codeunify#readme", 
        "Source Code": "https://github.com/takuphilchan/codeunify",
    },
)
