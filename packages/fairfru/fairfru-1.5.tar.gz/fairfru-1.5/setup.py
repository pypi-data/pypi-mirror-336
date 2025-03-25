import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="fairfru",
    version="1.5",
    author="Lisa Koutsoviti, Gonzalo Napoles",
    packages=["fairfru"],
    description="A bias measure using the fuzzy rough set theory",
    long_description= long_description,
    long_description_content_type='text/markdown'
)