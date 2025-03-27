from setuptools import setup, find_packages

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pip-terraform',
    version='0.2.1',
    author='Jaimin Raval',
    author_email='jaiminraval100@gmail.com',
    description='A cross-platform Terraform installation utility',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pip-terraform',
    packages=find_packages(),
    
    # Entry points for CLI
    entry_points={
        'console_scripts': [
            'pip-terraform=pip_terraform.cli:main',
        ],
    },
    
    # Specify Python version requirements
    python_requires='>=3.7',
    
    # Specify dependencies
    install_requires=[
        'requests>=2.25.1',
        'setuptools',
    ],
    
    # Optional: Add classifiers for PyPI
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Systems Administration',
    ],
    
    # Keywords to help people find your package
    keywords='terraform installation devops infrastructure',
    
    # Specify platform-specific requirements if needed
    platforms=['Darwin', 'Linux', 'Windows'],
)