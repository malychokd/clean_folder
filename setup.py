from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.1',
    description='Clean and sort files',
    url='https://github.com/malychokd/Tutorial/blob/main/mod6_dz_sort.py',
    author='Denys Malychok',
    author_email='d.malychok@ukr.net',
    license='',
    packages=find_namespace_packages(),
    #install_requires=['sys', 'os', 'shutil', 'pathlib'],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)