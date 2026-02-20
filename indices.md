# Working with Documents and Indices
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

::::{tab-item} Go
:sync: go
&nbsp;
::::

:::::

Two very important concepts in Elasticsearch are *documents* and *indices*.

A document is collection of fields with their associated values. To work with Elasticsearch you have to organize your data into documents, and then add all your documents to an index. You can think of an index as a collection of documents that are stored in a highly optimized format designed to perform efficient searches.

If you have worked with other databases, you may know that many of them require a schema definition, which is essentially a detailed description of data that you want to store. An Elasticsearch index can be configured with a schema or *mapping* if desired, but the mapping can automatically be derived from the data as it is added. In this tutorial you are going to let Elasticsearch figure out the mapping on its own, which works quite well for simple data types such as text, numbers and dates.

## Creating an index

This is how you create an Elasticsearch index using the Python client library:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

::::{tab-item} Go
:sync: go
```go
response, err := Client.Indices.Create("documents").Do(context.Background())
```
::::

:::::

:::{hint}
Indices in Elasticsearch are identified with a name, which is passed as an argument to most methods of the client. An Elasticsearch server can store multiple indices, each with its own collection of documents.
:::

Here is how to delete an index:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

::::{tab-item} Go
:sync: go
```go
response, err := Client.Indices.Delete("documents").Do(context.Background())
```
::::

:::::

If you attempt to create an index with a name that is already assigned to an existing index, you will get an error.

Next you will add a {lang-id}`createIndex,py:create_index` method to the application, along with a few other improvements.

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

    # add more methods before this line


if __name__ == '__main__':
    db = DB('documents')
    if sys.argv[1] == 'check':
        print(db.check())
    elif sys.argv[1] == 'create':
        db.create_index()
    # add more commands before this line
    else:
        print('Error: unknown command')
```

First of all, you will notice that there are new imports. Some of these imports are going to be unused for now, but they will be used later.

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

  // add more methods before this line
}

async function main() {
  const db = new DB('documents');
  if (process.argv[2] == 'check') {
    console.log(await db.check());
  }
  else if (process.argv[2] == 'create') {
    await db.createIndex('documents');
  }
  // add more commands before this line
  else {
    console.log('Error: unknown command');
  }
}

main();
```

First of all, you will notice that there are new imports. Some of these imports are going to be unused for now, but they will be used later.

::::

::::{tab-item} Go
:sync: go

Replace the contents of your *main.go* file to the following code:
```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"

    "github.com/elastic/go-elasticsearch/v9"
    "github.com/elastic/go-elasticsearch/v9/typedapi/core/info"
    "github.com/joho/godotenv"
)

type Document struct {
    Title    string `json:"title"`
    Category string `json:"category"`
    Summary  string `json:"summary"`
    Content  string `json:"content"`
}

type DB struct {
    Client *elasticsearch.TypedClient
    Index  string
}

func NewDB(index string) (*DB, error) {
    client, err := elasticsearch.NewTypedClient(
        elasticsearch.Config{
            Addresses: []string{os.Getenv("ELASTICSEARCH_URL")},
            APIKey:    os.Getenv("ELASTIC_API_KEY"),
        },
    )
    if err != nil {
        return nil, err
    }
    return &DB{Client: client, Index: index}, nil
}

func (db DB) Close(ctx context.Context) error {
    return db.Client.Close(ctx)
}

func (db DB) Check(ctx context.Context) (*info.Response, error) {
    return db.Client.Info().Do(ctx)
}

func (db DB) CreateIndex(ctx context.Context) error {
    if _, err := db.Client.Indices.Delete(db.Index).IgnoreUnavailable(true).Do(ctx); err != nil {
        return err
    }
    _, err := db.Client.Indices.Create(db.Index).Do(ctx)
    return err
}

// add more functions before this line

func main() {
    err := godotenv.Load()
    if err != nil {
        log.Fatal("Error loading .env file")
    }
    db, err := NewDB("documents")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close(context.Background())

    if os.Args[1] == "check" {
        response, err := db.Check(context.Background())
        if err == nil {
            printableResponse, _ := json.Marshal(response)
            fmt.Println(string(printableResponse))
        }
    } else if os.Args[1] == "create" {
        err = db.CreateIndex(context.Background())
    // add more commands before this line
    } else {
        log.Fatal(fmt.Errorf("Error: unknown command"))
    }
    if err != nil {
        log.Fatal(err)
    }
}
```
::::

:::::

The constructor of the `DB` {lang-text}`class,go:struct` now takes `index` name as an argument, the name of the index to use. This name is stored, so that it can be used in all operations later.

The new {lang-id}`createIndex,py:create_index,go:CreateIndex` {lang-text}`method,go:function` first deletes the index with the name that was passed in the constructor. The {lang-id}`ignore_unavailable,go:IgnoreUnavailable` option, given to the delete call, prevents a failure when the index name isn't found. After deleting the index, a new index is created with that name.

{lang-text}`In the main function,py:Then at the bottom`, an instance of the `DB` class is created with the index name `documents`, and then a simple command-line parser looks for a `check` or `create` argument. For `check`, it prints the results of calling the `check` method as the previous version of the application did, and for `create`, it calls the new {lang-id}`createIndex,py:create_index,go:CreateIndex` {lang-text}`method,go:function`.

:::{hint}
Note the location of the `add more ___ before this line` comments in the code. These indicate the places where you will need to add more functionality later.
:::

Try calling this new version of the application with the `check` and `create` arguments as follows:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

::::{tab-item} Go
:sync: go
```bash
# to check the Elasticsearch connection
go run ./main.go check

# to recreate the index
go run ./main.go create
```
::::

:::::


## Adding documents to an index

Elasticsearch documents are represented as [JSON](https://en.wikipedia.org/wiki/JSON) objects with a set of key/value pairs. To add a document to an index, the `index` method of the Elasticsearch client is used. Here is an example:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py
```python
document = {
    'title': 'Work From Home Policy',
    'category': 'teams',
    'contents': 'The purpose of this full-time work-from-home policy is...',
}
client.index(index='my_documents', document=document, id='1')
```
::::

::::{tab-item} JavaScript
:sync: js

```js
document = {
    title: 'Work From Home Policy',
    category: 'teams',
    contents: 'The purpose of this full-time work-from-home policy is...',
}
await this.client.index({ index: this.index, document: document, id: '1' });
```
::::

::::{tab-item} Go
:sync: go

```go
document := `{
    "title": "Work From Home Policy",
    "category": "teams",
    "content": "The purpose of this full-time work-from-home policy is..."
}`
response, err := db.Client.Index(db.Index).Id("1").Raw(
    strings.NewReader(document),
).Do(context.Background())
```
::::

:::::

In this example, the {lang-id}`id,go:Id` {lang-text}`field,go:option` assigns a unique identifier to the document. If it is omitted, Elasticsearch assigns a randomly generated identifier on its own. The document identifier can later be used to retrieve, update or delete the document in the index.

Let's add two more {lang-text}`methods,go:functions` to the `DB` class, to add and retrieve documents. Be careful to insert them in the place indicated by the comment, leaving the remaining parts of the application untouched.

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py
```python
    def add_document(self, document: dict[str, Any], id: str | None = None):
        self.client.index(index=self.index, document=document, id=id)

    def get_document(self, id: str):
        return self.client.get(index=self.index, id=id)

    # add more methods before this line
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
  
  // add more methods before this line
```
::::

::::{tab-item} Go
:sync: go
```go
func (db DB) AddDocument(ctx context.Context, document string, id string) error {
    _, err := db.Client.Index(db.Index).Id(id).Raw(
        strings.NewReader(document),
    ).Do(context.Background())
    return err
}

func (db DB) GetDocument(ctx context.Context, id string) (*get.Response, error) {
    return db.Client.Get(db.Index, id).Do(ctx)
}

// add more functions before this line
```

There are two new imports required by this added code that you need to insert at the top:

```go
import (
    // ...
    "strings"
    "github.com/elastic/go-elasticsearch/v9/typedapi/core/get"
)
```


::::

:::::

The {lang-id}`addDocument,py:add_document,go:AddDocument` {lang-text}`method,go:function` takes a document, given as a {lang-text}`object,py:dictionary,go:JSON string`, and an optional unique identifier for it. It inserts the document into the index, under the given identifier.

The {lang-id}`getDocument,py:get_document,go:GetDocument` method takes a document identifier as an argument, and returns the document as a response. 

To see the new methods in action, extend the command-line parsing at the bottom of the application with new `add` and `get` options:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py
```python
    elif sys.argv[1] == 'add':
        db.add_document({
            'title': 'Work From Home Policy',
            'category': 'teams',
            'content': 'The purpose of this full-time work-from-home policy is...',
        }, id='1')
    elif sys.argv[1] == 'get':
        response = db.get_document(sys.argv[2])
        print(response['_source'])
    # add more commands before this line
```
::::

::::{tab-item} JavaScript
:sync: js

```js
  else if (process.argv[2] == 'add') {
    await db.addDocument({
      title: 'Work From Home Policy',
      category: 'teams',
      content: 'The purpose of this full-time work-from-home policy is...',
    }, '1');
  }
  else if (process.argv[2] == 'get') {
    const response = await db.getDocument(process.argv[3]);
    console.log(response._source);
  }
  // add more commands before this line
```
::::

::::{tab-item} Go
:sync: go
```go
    } else if os.Args[1] == "add" {
        err = db.AddDocument(context.Background(), `{
            "title": "Work From Home Policy",
            "category": "teams",
            "content": "The purpose of this full-time work-from-home policy is..."
        }`, "1")
    } else if os.Args[1] == "get" {
        response, err := db.GetDocument(context.Background(), os.Args[2])
        if err == nil {
            fmt.Println(string(response.Source_))
        }
    // add more commands before this line
```
::::

:::::

The new `add` command inserts a test document into the index, identified as `"1"`. The `get` command retrieves the document with the identifier given in the command and prints it to the terminal. Try these commands as follows:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

::::{tab-item} Go
:sync: go

```bash
# insert a test document with id="1"
go run ./main.go add

# retrieve document with id="1"
go run ./main.go get 1
```

::::

:::::

The `get` command should print the following information:

```js
{
  title: 'Work From Home Policy',
  category: 'teams',
  content: 'The purpose of this full-time work-from-home policy is...',
}
```

## Ingesting documents in bulk

When setting up a new Elasticsearch index for a real project, you are likely going to need to import a large number of documents. You could ingest all these documents by iterating over them and calling the client's {lang-id}`index,go:Index` {lang-text}`method,go:function` for each, but this could take a long time for large datasets. To make this process more efficient, Elasticsearch provides a *bulk* feature that allows you to send multiple operations in a single call.

Now you are going to implement a bulk ingest option using an example dataset in [NDJSON](https://github.com/ndjson/ndjson-spec) format (Newline Delimited JSON), a format derived from JSON in which each line is a complete JSON object. Download the example dataset to the project directory using `curl`:

```bash
curl -L -o data.ndjson https://gist.githubusercontent.com/miguelgrinberg/4aa9a1f046238ed4a4c478078d2387f8/raw/3fd8a29087e1f4b140c06f4f8604f8890af57657/data.ndjson
```

The new ingest solution will read and parse documents from this file one by one and feed them to the bulk helper provided by the Elasticsearch client. The bulk helper will then assemble bulk requests and send them to Elasticsearch.

The {lang-id}`addManyDocuments,py:add_many_documents,go:AddManyDocuments` {lang-text}`method,go:function` shown below implements the bulk ingest solution.

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

    # add more methods before this line
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

  // add more methods before this line
```

Let's start to analyze this method from the `helpers.bulk` method of the client. This method takes the a list of actions to perform in the `datasource` argument, and a document processing function in `onDocument`. The return value of this method is an object with several details about the bulk operation, in particular how many documents were processed successfully and how many failed. For this application an excecption is raised if there is at least one error. On success, the method returns the number of documents that were inserted into the index.

The ingest process is fed by the `datasource` argument, which in this case is the `getNextDocument` generator function. The function opens the data file and reads it one line at a time. Each line is parsed as a JSON object and returned it.

As the bulk helper receives each document from the generator function, it calls the `onDocument` function with it as an argument. This function returns the operation that needs to be performed with this document. By returning an object with an `index` key it indicates that the document is to be stored in the index. The `_index` and `_id` provide the name of the index and the unique identifier respectively.

The identifiers are generated from a numeric incrementing counter in this case. This is just one of many alternatives to provide identifiers, it is not necessary for these identifiers to be numbers. It is also possible to omit the `_id` key to have Elasticsearch generate random identifiers.
::::

::::{tab-item} Go
:sync: go

```go
func (db DB) AddManyDocuments(ctx context.Context, dataFile string) (int, error) {
    indexer, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
        Client: db.Client,
        Index:  db.Index,
    })
    defer indexer.Close(ctx)

    file, err := os.Open(dataFile)
    if err != nil {
        return 0, err
    }
    defer file.Close()

    count := 0
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        count++
        if err := indexer.Add(ctx, esutil.BulkIndexerItem{
            Action:     "index",
            DocumentID: strconv.Itoa(count),
            Body:       strings.NewReader(scanner.Text()),
        }); err != nil {
            return 0, err
        }
    }
    if err := scanner.Err(); err != nil {
        return 0, err
    }
    return count, nil
}

// add more functions before this line
```

This code requires a few new imports, which you need to add at the top of the file:

```go
import (
    // ...
    "bufio"
    "strconv"
    "github.com/elastic/go-elasticsearch/v9/esutil"
)
```

This function starts by creating a `BulkIndexer`. This is a specialized helper that accepts Elasticsearch operations and packages them into chunks before they are submitted. The indexer is configured with the instance of the Elasticsearch client and the index name. There are additional arguments that can be passed to control how the chunking logic works, but for this example the defaults are sufficient. The indexer has a `Close` function, so that is added as a deferred call.

Next, file referenced by the `dataFile` argument is opened, and read line by line. For each line, the indexer's `Add` function is called with a `BulkIndexerItem` argument. This structure defines an action, which in this case is always `"index"`. The `DocumentId` attribute sets the unique identifier for each document, which is generated from a counter that is incremented before each line is processed. The `Body` attribute is set to the document data, given as a `Reader` instance.

If no errors occur during the ingest, then the function returns the number of ingested documents.
::::

:::::

Let's now add a new `bulk` command that calls the new {lang-text}`method,go:function`:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py
```python
    elif sys.argv[1] == 'bulk':
        count = db.add_many_documents(sys.argv[2])
        print(f'Ingested {count} documents.')
    # add more commands before this line
```
::::

::::{tab-item} JavaScript
:sync: js
```js
  else if (process.argv[2] == 'bulk') {
    const count = await db.addManyDocuments(process.argv[3]);
    console.log(`Ingested ${count} documents.`);
  }
  // add more commands before this line
```
::::

::::{tab-item} Go
:sync: go
```go
    } else if os.Args[1] == "bulk" {
        count, err := db.AddManyDocuments(context.Background(), os.Args[2])
        if err == nil {
            fmt.Printf("Ingested %d documents.\n", count)
        }
    // add more commands before this line
```
::::

:::::

This new `bulk` command takes an argument that is the filename of the NDJSON data file to ingest. Make sure you have downloaded the *data.ndjson* file as instructed above, and then run the ingest as follows:

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

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

::::{tab-item} Go
:sync: go
```bash
go run ./main.go bulk data.ndjson
```
::::

:::::

The output of this command should indicate that 15 documents were ingested.

:::{hint}
While this tutorial uses a small example dataset, the bulk ingest solution presented here is very robust and is able to scale to very large amounts of data. Thanks to the use of chunking, it is possible to ingest datasets that are larger than the amount of memory available to the process, since one one chunk is held in memory at a given time.
:::
