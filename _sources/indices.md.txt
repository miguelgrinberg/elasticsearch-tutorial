# Working with Documents and Indices
:::::{invisible-tab-set}
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

Two very important concepts in Elasticsearch are *documents* and *indices*.

A document is collection of fields with their associated values. To work with Elasticsearch you have to organize your data into documents, and then add all your documents to an index. You can think of an index as a collection of documents that are stored in a highly optimized format designed to perform efficient searches.

If you have worked with other databases, you may know that many of them require a schema definition, which is essentially a detailed description of data that you want to store. An Elasticsearch index can be configured with a schema or *mapping* if desired, but the mapping can automatically be derived from the data as it is added. In this tutorial you are going to let Elasticsearch figure out the mapping on its own, which works quite well for simple data types such as text, numbers and dates.

## Creating an index

This is how you create an Elasticsearch index using the Python client library:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
client.indices.create(index='documents')
```
::::

::::{tab-item} JavaScript
:sync: js
```js
await client.indices.create({ index: 'documents' });
```
::::

:::::

:::{hint}
Indices in Elasticsearch are identified with a name, which is passed as an argument to most methods of the client. An Elasticsearch server can store multiple indices, each with its own collection of documents.
:::

Here is how to delete an index:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
client.indices.delete(index='documents')
```
::::

::::{tab-item} JavaScript
:sync: js
```js
await this.client.indices.delete({ index: 'documents' });
```
::::

:::::

If you attempt to create an index with a name that is already assigned to an existing index, you will get an error.

Next you will add a {lang-id}`createIndex,py:create_index` method to the application, along with a few other improvements.

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py

Replace the contents of your *main.py* file to the following code:

```python
import json
import os
import sys
from typing import Any, Iterator
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

load_dotenv()


class DB:
    def __init__(self, index: str):
        self.client = Elasticsearch(os.environ['ELASTICSEARCH_URL'],
                                    api_key=os.environ['ELASTIC_API_KEY'])
        self.index = index

    def check(self):
        return self.client.info()

    def create_index(self):
        self.client.indices.delete(index=self.index, ignore_unavailable=True)
        self.client.indices.create(index=self.index)

    # more methods will be added here later


if __name__ == '__main__':
    db = DB('documents')
    if sys.argv[1] == 'check':
        print(db.check())
    elif sys.argv[1] == 'create':
        db.create_index()
    # more commands will be added here later
    else:
        print('Error: valid commands are check and create')
```
::::

::::{tab-item} JavaScript
:sync: js

Replace the contents of your *main.js* file to the following code:

```js
const fs = require('fs');
const readline = require('readline');
require('dotenv').config({ quiet: true });
const { Client } = require('@elastic/elasticsearch');

class DB {
  constructor(index) {
    this.client = new Client({
      node: process.env.ELASTICSEARCH_URL,
      auth: { apiKey: process.env.ELASTIC_API_KEY },
    });
    this.index = index;
  }

  async check() {
    return await this.client.info();
  }

  async createIndex() {
    await this.client.indices.delete({ index: this.index, ignore_unavailable: true });
    await this.client.indices.create({ index: this.index });
  }

  // more methods will be added here later
}

async function main() {
  const db = new DB('documents');
  if (process.argv[2] == 'check') {
    console.log(await db.check());
  }
  else if (process.argv[2] == 'create') {
    await db.createIndex('documents');
  }
  // more commands will be added here later
  else {
    console.log('Error: valid commands are check and create');
  }
}

main();
```
::::

:::::

There are a few improvements in this version of the project.

First of all, you will notice that there are new imports. Some of these imports are going to be unused for now, but they will be used later.

The constructor of the `DB` class now takes the `index` name as an argument. This name is stored in an `index` instance variable.

The new {lang-id}`createIndex,py:create_index` method first deletes the index with the name that was passed in the constructor. The `ignore_unavailable` option, given to the `delete` call, prevents a failure when the index name isn't found. After deleting the index, a new index is created with that name.

Then at the bottom, an instance of the `DB` class is created with the index name `documents`, and then a simple command-line parser looks for a `check` or `create` argument. For `check`, it prints the results of calling the `check` method as the previous version of the application, and for `create`, it calls the new {lang-id}`createIndex,py:create_index` method.

Try calling this new version of the application with the `check` and `create` arguments as follows:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```bash
# to check the Elasticsearch connection
python main.py check

# to recreate the index
python main.py create
```
::::

::::{tab-item} JavaScript
:sync: js
```bash
# to check the Elasticsearch connection
node main.js check

# to recreate the index
node main.js create
```
::::

:::::


## Adding documents to an index

Elasticsearch documents are represented as [JSON](https://en.wikipedia.org/wiki/JSON) objects with a set of key/value pairs. To add a document to an index, the `index` method of the Elasticsearch client is used. Here is an example:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
document = {
    'name': 'Work From Home Policy',
    'category': 'teams',
    'contents': 'The purpose of this full-time work-from-home policy is...',
    'created_on': '2023-11-02',
}
client.index(index='my_documents', document=document, id='1')
```
::::

::::{tab-item} JavaScript
:sync: js

```js
document = {
    name: 'Work From Home Policy',
    category: 'teams',
    contents: 'The purpose of this full-time work-from-home policy is...',
    created_on: '2023-11-02',
}
await this.client.index({ index: this.index, document: document, id: '1' });
```
::::

:::::

In this example, the `id` field assigns an unique identifier to the document. If it is omitted, Elasticsearch assigns a randomly generated identifier on its own. The document identifier can later be used to retrieve, update or delete the document in the index.

Let's add two more methods to the `DB` class, to add and retrieve documents. Be careful to insert the new methods in the place indicated by the comment, leaving remaining parts of the application untouched.

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
    def add_document(self, document: dict[str, Any], id: str | None = None):
        self.client.index(index=self.index, document=document, id=id)

    def get_document(self, id: str):
        return self.client.get(index=self.index, id=id)

    # more methods will be added here later
```
::::

::::{tab-item} JavaScript
:sync: js

```js
  async addDocument(document, id) {
    await this.client.index({ index: this.index, id: id, document: document });
  }

  async getDocument(id) {
    return await this.client.get({ index: this.index, id: id });
  }
  
  // more methods will be added here later
```
::::

:::::

The {lang-id}`addDocument,py:add_document` method a document, given as a dictionary, and an optional identifier for it. It inserts the document into the index, under the given identifier if one was provided, or with a randomly generated one if not.

The {lang-id}`getDocument,py:get_document` method takes a document identifier as an argument, and returns the document as a response. 

To see the new methods in action, extend the command-line parsing at the bottom of the application with new `add` and `get` options:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
    elif sys.argv[1] == 'add':
        db.add_document({
            'name': 'Work From Home Policy',
            'category': 'teams',
            'content': 'The purpose of this full-time work-from-home policy is...',
            'created_on': '2023-11-02',
        }, id='1')
    elif sys.argv[1] == 'get':
        print(db.get_document(sys.argv[2]))
    # more commands will be added here later
    else:
        print('Error: valid commands are check, create, add and get')
```
::::

::::{tab-item} JavaScript
:sync: js

```js
  else if (process.argv[2] == 'add') {
    await db.addDocument({
      name: 'Work From Home Policy',
      category: 'teams',
      content: 'The purpose of this full-time work-from-home policy is...',
      created_on: '2023-11-02',
    }, '1');
  }
  else if (process.argv[2] == 'get') {
    console.log(await db.getDocument(process.argv[3]));
  }
  // more commands will be added here later
  else {
    console.log('Error: valid commands are check, create, add and get');
  }
```
::::

:::::

The new `add` command inserts a test document into the index, identified as `"1"`. The `get` command retrieves the document with the identifier given in the command and prints it to the terminal. Try these commands as follows:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```bash
# insert a test document with id="1"
python main.py add

# retrieve document with id="1"
python main.py get 1
```
::::

::::{tab-item} JavaScript
:sync: js

```bash
# insert a test document with id="1"
node main.js add

# retrieve document with id="1"
node main.js get 1
```
::::

:::::

The `get` command should print the following information:

```js
{
  _index: 'documents',
  _id: '1',
  _version: 1,
  _seq_no: 0,
  _primary_term: 1,
  found: true,
  _source: {
    name: 'Work From Home Policy',
    category: 'teams',
    content: 'The purpose of this full-time work-from-home policy is...',
    created_on: '2023-11-02'
  }
}
```

In this response, the actual contents of the document are in the `_source` field. The other top-level fields are document metadata. You probably recognize the `_id` field, which has the document identifier, and `_index`, which has the index name.

## Ingesting documents in bulk

When setting up a new Elasticsearch index for a real project, you are likely going to need to import a large number of documents. You could ingest all these documents by iterating over them and calling the client's `index` method for each, but this could take a long time for large datasets. To make this process more efficient, Elasticsearch provides a *bulk* feature that allows you to send multiple index operations in a single call.

Now you are going to implement a bulk ingest option using a dataset in [NDJSON](https://github.com/ndjson/ndjson-spec) format (Newline Delimited JSON), a format derived from JSON in which each line is a complete JSON object. Download the dataset to the project directory using `curl`:

```bash
curl -L -o data.ndjson https://gist.githubusercontent.com/miguelgrinberg/4aa9a1f046238ed4a4c478078d2387f8/raw/332f8c8de4191ec6694228b587e40a3eb80c15cb/data.ndjson
```

The new ingest solution will read and parse documents from this file one by one and feed them to the bulk helper provided by the Elasticsearch client. The bulk helper will then assemble bulk requests and send them to Elasticsearch.

The {lang-id}`addManyDocuments,py:add_many_documents` method shown below implements the bulk ingest solution.

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
    def add_many_documents(self, data_file: str):
        def get_next_document() -> Iterator[dict[str, Any]]:
            id = 0
            with open(data_file, 'r') as f:
                for line in f:
                    document = json.loads(line)
                    id += 1
                    yield {'_index': self.index, '_id': str(id), '_source': document}

        response = bulk(client=self.client, actions=get_next_document(), stats_only=True)
        if response[1] != 0:
            raise RuntimeError('Bulk ingest failure')
        return response[0]

    # more methods will be added here later
```

Let's start to analyze this method from the `bulk` call. This function takes the client and a list of actions to perform as arguments. The `stats_only` given last requests that the return value from this function is just a summary of operations. This result will come as a tuple of two numbers indicating how many documents were processed and how many failed. For this application if there is at least one error a `RuntimeError` is raised. On success, the method returns the number of documents that were inserted into the index.

The core of the bulk ingest process is in the `actions` argument, which is set to a `get_next_document` generator function. The bulk helper will call the generator to get the documents. It will compile these documents into chunks, and send each chunk to Elasticsearch. There are optional arguments that can be passed to the `bulk` helper to control how the chunking process works.

The implementation of the `get_next_document` generator function opens the NDJSON data file and reads it one line at a time in a loop. For each line, it parses it as a JSON object and then it yields a dictionary with the target index name (in the `_index` key), the desired identifier for the document (in the `_id` key) and the document data (in the `_source` key).

To assign unique identifiers to documents, the generator function maintains a counter which gets incremented for each document. This is just one of many alternatives to provide identifiers, it is not necessary for these identifiers to be numbers. It is also possible to omit the `_id` key to have Elasticsearch generate random identifiers.
::::

::::{tab-item} JavaScript
:sync: js
```js
  async addManyDocuments(dataFile) {
    async function * getNextDocument() {
      const fileStream = fs.createReadStream(dataFile);
      const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });
      for await (const line of rl) {
        yield JSON.parse(line);
      }
    }
    const index = this.index;
    let counter = 0;
    const result = await this.client.helpers.bulk({
      datasource: getNextDocument(),
      onDocument(doc) {
        return {
          index: { _index: index, _id: ++counter }
        }
      }
    });
    if (result.failed) {
      throw new Error('Some documents failed to ingest.');
    }
    return result.total;
  }

  // more methods will be added here later
```

Let's start to analyze this method from the `helpers.bulk` method of the client. This method takes the a list of actions to perform in the `datasource` argument, and a document processing function in `onDocument`. The return value of this method is an object with several details about the bulk operation, in particular how many documents were processed successfully and how many failed. For this application an excecption is raised if there is at least one error. On success, the method returns the number of documents that were inserted into the index.

The ingest process is fed by the `datasource` argument, which in this case is the `getNextDocument` generator function. The function opens the data file and reads it one line at a time. Each line is parsed as a JSON object and returned it.

As the bulk helper receives each document from the generator function, it calls the `onDocument` function with it as an argument. This function returns the operation that needs to be performed with this document. By returning an object with an `index` key it indicates that the document is to be stored in the index. The `_index` and `_id` provide the name of the index and the unique identifier respectively.

The identifiers are generated from a numeric incrementing counter in this case. This is just one of many alternatives to provide identifiers, it is not necessary for these identifiers to be numbers. It is also possible to omit the `_id` key to have Elasticsearch generate random identifiers.
::::

:::::

Let's add a new `bulk` command to the application that uses the new method:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
    elif sys.argv[1] == 'bulk':
        count = db.add_many_documents(sys.argv[2])
        print(f'Ingested {count} documents.')
    # more commands will be added here later
    else:
        print('Error: valid commands are check, create, add, get and bulk')
```
::::

::::{tab-item} JavaScript
:sync: js
```js
  else if (process.argv[2] == 'bulk') {
    const count = await db.addManyDocuments(process.argv[3]);
    console.log(`Ingested ${count} documents.`);
  }
  // more commands will be added here later
  else {
    console.log('Error: valid commands are check, create, add, get and bulk');
  }
```
::::

:::::

This new `bulk` command takes an argument that is the filename of the NDJSON data file to ingest. Make sure you have downloaded the *data.ndjson* file as instructed above, and then run the ingest as follows:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```bash
python main.py bulk data.ndjson
```
::::

::::{tab-item} JavaScript
:sync: js
```bash
node main.js bulk data.ndjson
```
::::

:::::

The output of this command should indicate that 15 documents were ingested.

:::{hint}
While this tutorial uses a small example dataset, the bulk ingest solution presented here is very robust and is able to scale to very large amounts of data. Thanks to the use of generators and the chunking applied by the bulk helper, it is possible to ingest datasets that are larger than the amount of memory available to the process.
:::
