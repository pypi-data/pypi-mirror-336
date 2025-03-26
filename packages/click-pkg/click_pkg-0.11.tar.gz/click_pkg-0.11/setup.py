import pathlib
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

keywords = "click-shop-api,click,click-merchant,click-pkg,click-api,click-python-integration,click-integration,click-python,click-gateway,click-payment,click-payment-gateway,click-integration-python,click-api-client,click-django,click-rest-api,click-fastapi" # noqa

setup(
    name='click-pkg',
    version='0.11',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages(),
    url='https://github.com/Muhammadali-Akbarov/click-pkg',
    keywords=keywords,
    install_requires=[
        'requests==2.*',
        "dataclasses==0.*;python_version<'3.7'",
    ],
    extras_require={
        'django': [
            'djangorestframework==3.*',
            'django>=3.0,<5.0',
        ],
        'fastapi': [
            'fastapi>=0.68.0',
            'pydantic>=1.8.0,<2.0.0',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
