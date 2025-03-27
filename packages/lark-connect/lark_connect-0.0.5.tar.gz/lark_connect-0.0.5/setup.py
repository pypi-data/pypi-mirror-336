from setuptools import setup, find_packages

setup(
    name='lark-connect',
    version='0.0.5',
    description="A Python package for integrating with Lark API to send messages, manage bots, "
                "and interact with Lark apps.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='wontae.jeon',
    author_email='wontae@aidenlab.io',
    install_requires=['requests'],
    packages=find_packages(exclude=[]),
    keywords=['lark', 'incode8'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
