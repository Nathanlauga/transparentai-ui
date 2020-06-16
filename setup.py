from setuptools import setup, find_packages
import os

path = os.path.dirname(os.path.abspath(__file__))
with open(path+"/README.md", "r") as fh:
    long_description = fh.read()
fh.close()

setup(
    name='transparentai-ui',
    version='0.1.0',
    description="Webapp to supervise the ethics of your AI.",
    license='MIT',
    author='Nathan LAUGA',
    author_email='nathan.lauga@protonmail.com',
    url='https://github.com/Nathanlauga/transparentai-ui',
    packages=find_packages(exclude=['tests*']),
    # packages=['transparentai_ui'],
    include_package_data=True,
    install_requires=[
        'transparentai',
        'click',
        'flask',
        'Flask-Babel',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'gunicorn'
    ],
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requires='>=3.6',
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            "transparentai = transparentai_ui.__main__:main"
        ]
    },
)
