
import setuptools

setuptools.setup(
    name="certora-cli-alpha-oz-minver",
    version="20250325.7.39.773685",
    author="Certora",
    author_email="support@certora.com",
    description="Runner for the Certora Prover",
    long_description="Commit ee9b056.                    Build and Run scripts for executing the Certora Prover on Solidity smart contracts.",
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/certora-cli-alpha-oz-minver",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['click', 'json5', 'pycryptodome', 'requests', 'rich', 'sly', 'tabulate', 'tqdm', 'StrEnum', 'universalmutator', 'jinja2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "certoraRun = certora_cli.certoraRun:entry_point",
            "certoraMutate = certora_cli.certoraMutate:mutate_entry_point",
            "certoraEqCheck = certora_cli.certoraEqCheck:equiv_check_entry_point",
            "certoraSolanaProver = certora_cli.certoraSolanaProver:entry_point",
            "certoraSorobanProver = certora_cli.certoraSorobanProver:entry_point",
            "certoraEVMProver = certora_cli.certoraEVMProver:entry_point"
        ]
    },
    python_requires='>=3.11',
)
