from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the dependencies from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    env_requirements = f.read().splitlines()

# Additional dependencies not in the file
cli_dependencies = [
    "typer",
    "pyyaml",
]

# Combine the two lists
install_requires = env_requirements + cli_dependencies 

setup(
    name="remoterl",
    version="1.0.2",
    packages=find_packages(), 
    include_package_data=True,
    package_data={
        "remoterl.cli": ["*.yaml"],  # explicitly specify the cli subpackage
    },
    entry_points={
        "console_scripts": [
            "remoterl=remoterl.cli.cli:app",
        ],
    },
    install_requires=install_requires,
    author="JunHo Park",
    author_email="junho@ccnets.org",
    url="https://github.com/ccnets-team/remoterl",
    description="Remote RL for training and inference on AWS SageMaker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Dual Licensed (REMOTE RL COMMERCIAL LICENSE or GNU GPLv3)",
    keywords="remote rl reinforcement-learning sagemaker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
