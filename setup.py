from setuptools import setup, find_namespace_packages

setup(
    name='Willy',
    version='v1.0.1',
    description='Personal Assistant Willy',
    url='https://github.com/Yar-Mel/CLI',
    author='Yaroslav Melnychuk',
    author_email='Yarmel.dev@gmail.com',
    license='GNU',
    packages=find_namespace_packages(),
    classifiers=["Programming Language :: Python :: 3",
                "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                "Operating System :: OS Independent",
                ],
    entry_points={'console_scripts':['willy = entry_point:main']}
)
