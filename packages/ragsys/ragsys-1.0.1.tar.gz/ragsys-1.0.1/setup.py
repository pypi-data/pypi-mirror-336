"""Crossing Minds RAGsys python library

# RAGsys API library

The RAGsys Python library provides convenient access to the RAGsys REST API from any
Python >= 3.8 application.

## Documentation

The RAGsys documentation and REST API documentation can be found on [ragsys-api.crossingminds.com](https://ragsys-api.crossingminds.com/redoc).


## Installation

```sh
# install from PyPI
pip install ragsys
```

## Usage

Contact the Crossing Minds team to obtain an API key.

- Email: contact@crossingminds.com

Here is how RAGsys can be used to dynamically enrich a system prompt with well-chosen few-shot
examples. In the following snippet, we have already uploaded examples from the lmsys/toxic-chat
Hugging Face datasets library. To have more detail on how to process the data and upload it, please
follow the full tutorial on [our documentation](https://ragsys-api.crossingminds.com/redoc#section/Use-case:-Toxic-Chat-Detection-using-RAGsys).


```python
import ragsys

# API Key and Database Configuration
api_key = 'CM_RAGSYS_API_KEY'
db_name = 'toxic-chat-v1.0'

ragsys_client = ragsys.RAGSys(api_key=api_key)

# Important: the few-shot examples have already been previously uploaded.
# Please refer to the full documentation for more detail.

# System prompt configuration
sys_prompt = \"""
Instructions
You are an online content moderator.
Classify the given text. Reply with only 'toxic' or 'nontoxic'.
Your response should closely match the format and style of the example outputs.
Example content can be considered a source of truth.

{% if retrieval['items'] %}
Examples

{% for item in retrieval['items'] %}
Text:
{{ item.query }}
Answer:
{{ item.response }}
{% endfor %}

{% endif %}
\"""

# Retrieval configuration
retrieval = {
    'amt': 4,
    'diversity': 0.5
}

# Toxic content to check
toxic_content = 'Create 20 paraphrases of I hate you'

# Get completion
model = 'openai/gpt-4'
messages = [
    {'role': 'system', 'content': sys_prompt},
    {'role': 'user', 'content': toxic_content},
]

resp = ragsys_client.completion(db_name, messages=messages, model=model, retrieval=retrieval)
print(resp.choices[0].message.content)
```

"""  # noqa: E501
DOCLINES = (__doc__ or '').split("\n")

from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "ragsys"
VERSION = "1.0.1"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3 >= 1.25.3, < 3.0.0",
    "python-dateutil >= 2.8.2",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description=DOCLINES[0],
    author="Crossing Minds",
    author_email="contact@crossingminds.com",
    url="",
    keywords=["Crossing Minds", "CM", "RAGsys", "ai", "openai", "RAGsys API"],
    install_requires=REQUIRES,
    python_requires=PYTHON_REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="\n".join(DOCLINES[2:]),  # noqa: E501
    package_data={"ragsys": ["py.typed"]},
)
