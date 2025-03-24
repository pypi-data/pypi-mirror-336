import json
from setuptools import setup
from pathlib import Path
import os


githuburl = 'https://github.com/STEdyd666/dash-blueprint-components'

here = Path(__file__).parent
with open('package.json') as f:
    package = json.load(f)
long_description = (here / 'README.md').read_text()

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers = [
        'Framework :: Dash',
    ],
    project_urls={
        "Bug Reports": os.path.join(githuburl, "issues"),
        "Source": githuburl,
        "Documentation": "https://dash-blueprint-components.com/blueprint"
    },
)
