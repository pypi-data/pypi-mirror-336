from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='IsoGen',  # required
    version='2025.3.23',
    description='IsoGen: a deep learning based water isotope generator (emulator)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feng Zhu',
    author_email='fengzhu@ucar.edu',
    url='https://github.com/fzhu2e/isogen',
    packages=find_packages(),
    include_package_data=True,
    license='BSD-3',
    zip_safe=False,
    keywords=['Deep Learning', 'Water Isotope', 'Emulator'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'colorama',
        'tqdm',
        'torch',
    ],
)
