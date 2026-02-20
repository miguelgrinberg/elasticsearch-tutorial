# Connecting to Elasticsearch
:::::{tab-set}
:sync-group: lang
:class: hidden

::::{tab-item} Python
:sync: py
&nbsp;
::::

::::{tab-item} JavaScript
:sync: js
&nbsp;
::::

:::::

In this section you are going to write code to connect to your Elasticsearch instance.

To create a connection, an Elasticsearch client must be created with the appropriate connection options. You will now do this to verify that you can connect to the Elasticsearch instance created by `start-local`.

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py

Copy the following code into a file named *main.py* in your project directory:

```python
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class DB:
    def __init__(self):
        self.client = Elasticsearch(os.environ['ELASTICSEARCH_URL'],
                                    api_key=os.environ['ELASTIC_API_KEY'])

    def check(self):
        return self.client.info()


if __name__ == '__main__':
    db = DB()
    print(db.check())
```

The first thing that happens in this file after the imports is the call to the `load_dotenv()` function from the [python-dotenv](https://github.com/theskumar/python-dotenv) package. This function reads the variables that are stored in the *.env* file and imports them into the Python process as environment variables. Once they are imported, they can be accessed from the `os.environ` dictionary.
::::

::::{tab-item} JavaScript
:sync: js

Copy the following code into a file named *main.js* in your project directory:


```js
require('dotenv').config({ quiet: true });
const { Client } = require('@elastic/elasticsearch');

class DB {
  constructor() {
    this.client = new Client({
      node: process.env.ELASTICSEARCH_URL,
      auth: { apiKey: process.env.ELASTIC_API_KEY },
    });
  }

  async check() {
    return await this.client.info();
  }
}

async function main() {
    const db = new DB();
    console.log(await db.check());
}

main();
```

The first line in this file invokes the `config` function of the `dotenv` package. This reads the variables that are stored in the *.env* file and imports them into the process as environment variables. Once they are imported, they can be accessed from the `process.env` object.
::::

:::::

The `DB` class is where all the database logic for the project will be defined. In the class constructor, an instance of the Elasticsearch client is created. The Elasticsearch URL and the API key are read from the environment and passed as arguments, to allow the client to authenticate.

The `check` method of the `DB` class calls the `info` method of the client and returns its response. Calling the `info` method is often done as a way to test that a connection to the Elasticsearch server can be established. If the call succeeds, some basic information about the Elasticsearch instance is returned.

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py

The last three lines of the application define the code that will run when the script is started. In this first version, the application creates an instance of the `DB` class, and prints the result of calling its `check` method.

::::

::::{tab-item} JavaScript
:sync: js

:::{hint}
The methods of the Elasticsearch client for JavaScript return promises. They can be invoked with async/await or promise syntax.
:::

The `main` function defines the code that will run when the script is started. In this first, version, the application creates an instance of the `DB` class, and prints the result of calling its `check` method.

::::

:::::

Run the application as follows:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py
```bash
python main.py
```
::::

::::{tab-item} JavaScript
:sync: js
```bash
node main.js
```
::::

:::::

The value returned by the `check` method should be printed to your terminal. This is, in turn, the response returned by Elasticsearch's `info` method. It should look more or less like the following, but note that some values such as versions, dates and hashes in your response will be different:

```js
{
  name: 'elasticsearch',
  cluster_name: 'docker-cluster',
  cluster_uuid: 'iBKIYoyUTmWo9z9DmHE0Xw',
  version: {
    number: '9.3.0',
    build_flavor: 'default',
    build_type: 'docker',
    build_hash: '17b451d8979a29e31935fe1eb901310350b30e62',
    build_date: '2026-01-29T10:05:46.708397977Z',
    build_snapshot: false,
    lucene_version: '10.3.2',
    minimum_wire_compatibility_version: '8.19.0',
    minimum_index_compatibility_version: '8.0.0'
  },
  tagline: 'You Know, for Search'
}
```

:::{hint}
Fun fact: among the fields in the response to `info` you should find Elasticsearch's iconic `tagline` field, which is always set to the string ["You Know, for Search"](https://www.elastic.co/blog/you-know-for-search-inc).
:::
