import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="notion-tools",
    version="0.0.1",
    author="Josh Holbrook",
    author_email="josh.holbrook@gmail.com",
    description="Python toolkit for Notion.so",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfhbrook/notion-tools",
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points=dict(console_scripts=["notion=notion.cli:cli"]),
)
