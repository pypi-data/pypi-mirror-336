from setuptools import setup, find_packages

setup(
    name='fastconvert',
    version='1.0.3',
    description='A powerful CLI tool for converting files between different formats.',
    long_description=open('README_PYPI.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='qwez',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pillow',
        'opencv-python'
    ],
    entry_points={
        'console_scripts': [
            'fastconvert=fastconvert:convert'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)