from setuptools import setup, find_packages

setup(
    name="mcp-smarthub",
    version="0.2.6",
    packages=find_packages(include=["mcp_smarthub", "mcp_smarthub.*"]),
    install_requires=[
        "mcp>=1.4.1",
        "snowflake-connector-python>=3.14.0",
        "uvicorn>=0.34.0",
        "fastapi>=0.109.0",
        "typing-extensions>=4.9.0",
    ],
    entry_points={
        "console_scripts": ["mcp_smarthub=mcp_smarthub.server:run_server"],
        "mcp.v1": ["mcp_smarthub=mcp_smarthub.server:mcp"],
    },
)