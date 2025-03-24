from setuptools import setup, find_packages
from setuptools.command.install import install
import setuptools_scm
from pathlib import Path
import shutil
import re

PACKAGE_NAME = "spectHR"
VERSION_FILE = Path(__file__).parent / "_version.py"
# Custom function to adjust version for PyPI upload
def get_version():
    # Use setuptools_scm to get the version
    version = setuptools_scm.get_version()

    # Check if it's a local version with '+' or 'd' in it, and remove that part
    if '+' in version or 'd' in version:
        version = re.sub(r'\+.*$', '', version)  # Remove everything after '+'
        version = re.sub(r'\.d\d+$', '', version)  # Remove the date part, if exists

    return version
# Custom post-installation script to copy Jupyter notebooks
def install_notebook():
    """Copies Jupyter notebooks to the user's home directory."""
    notebook_src = Path(__file__).parent / "spectHR/notebooks/SpectHR.ipynb"
    notebook_dest = Path.home() / "SpectHR.ipynb"
    data_src =  Path(__file__).parent / "SUB_002.xdf"
    if notebook_src.exists():
        shutil.copy(notebook_src, notebook_dest)
        print(f"Notebook copied to {notebook_dest}")
    else:
        print("Notebook file not found!")
    if data_src.exists():
        shutil.copy(data_src, Path.home())
        print(f"Data copied to {Path.home()}")
    else:
        print("Example data file not copied!")

class PostInstallCommand(install):
    """Post-installation command to copy Jupyter notebooks."""
    def run(self):
        install.run(self)
        install_notebook()  # Call the function after install

setup(
    name=PACKAGE_NAME,
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "version_scheme": "post-release",  # Ensure versioning is PEP 440 compliant
        "local_scheme": "node-and-date",  # Can use commit hash for dev versions
    },
    version=get_version(),  # Dynamically adjust version
    setup_requires=["setuptools_scm"],
    description="HRApp: An Interactive Heart Rate Variability (HRV) Analysis Tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="GPL-2.0-only",
    author="Mark Span",
    author_email="m.m.span@rug.nl",
    url="https://github.com/MarkSpan/spectHR",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires=">=3.10",
    packages=find_packages() + ["spectHR.images", "spectHR.notebooks"],
    package_data={
        'spectHR': ['spectHR/images/*', 'spectHR/notebooks/*', 'SUB_002.xdf'],
    },
    include_package_data=True,
    install_requires=[
        "ipython",
        "ipympl",
        "ipyvuetify",
        "ipywidgets",
        "jupyter",
        "jupyterlab>=4.0.0",
        "matplotlib",
        "mplcursors",
        "numpy",
        "pandas",
        "pyxdf",
        "scipy",
        "seaborn",
        "wheel",
        "easywebdav",
    ],
    cmdclass={"install": PostInstallCommand},  # Runs post-install command
    entry_points={
        "console_scripts": [
            "install-spectHR-notebooks=spectHR.install_notebook:install_notebook"
        ]
    },
    project_urls={
        "Homepage": "https://github.com/MarkSpan/spectHR"
    }
)
