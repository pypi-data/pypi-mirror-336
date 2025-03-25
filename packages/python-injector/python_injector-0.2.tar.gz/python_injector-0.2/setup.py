from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
    
setup(
    name='python_injector',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g., 'requests'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/mjdarvishi/python_injector',
    author='Mohammad Javad Darvishi',
    author_email='mjdarvishi1374@gmail.com',
)
