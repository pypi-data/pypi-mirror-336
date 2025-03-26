from setuptools import setup, find_packages

setup(
    name='fastconvert',
    version='1.0.0',
    description='A powerful CLI tool for converting files between different formats.',
    long_description=open('README_PYPI.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='qwez',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.7',
        'Pillow',
        'python-magic-bin==0.4.14',
        'pypdf2==3.0.1',
        'opencv-python'
    ],
    entry_points={
        'console_scripts': [
            'fastconvert=fastconvert.fastconvert:convert'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)