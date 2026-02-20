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

::::{tab-item} Go
:sync: go
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

The `DB` class is where all the database logic for the project will be defined. In the constructor, an instance of the Elasticsearch client is created. The Elasticsearch URL and the API key are read from the environment and passed as configuration arguments, to allow the client to authenticate.

The `check` method calls the `info` method of the client and returns its response. Calling the `info` method is often done as a way to test that a connection to the Elasticsearch server can be established. If the call succeeds, some basic information about the Elasticsearch instance is returned.

The last three lines of the application define the code that will run when the script is started. In this first version, the application creates an instance of the `DB` class, and prints the result of calling its `check` method.

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

The `DB` class is where all the database logic for the project will be defined. In the constructor, an instance of the Elasticsearch client is created. The Elasticsearch URL and the API key are read from the environment and passed as configuration arguments, to allow the client to authenticate.

The `check` method calls the `info` method of the client and returns its response. Calling the `info` method is often done as a way to test that a connection to the Elasticsearch server can be established. If the call succeeds, some basic information about the Elasticsearch instance is returned.

:::{hint}
The methods of the Elasticsearch client for JavaScript return promises. They can be invoked with async/await or promise syntax.
:::

The `main` function defines the code that will run when the script is started. In this first, version, the application creates an instance of the `DB` class, and prints the result of calling its `check` method.

::::

::::{tab-item} Go
:sync: go

Copy the following code into a file named *main.go* in your project directory:

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

type DB struct {
	Client *elasticsearch.TypedClient
}

func NewDB() (*DB, error) {
	client, err := elasticsearch.NewTypedClient(
		elasticsearch.Config{
			Addresses: []string{os.Getenv("ELASTICSEARCH_URL")},
			APIKey:    os.Getenv("ELASTIC_API_KEY"),
		},
	)
	if err != nil {
		return nil, err
	}
	return &DB{Client: client}, nil
}

func (db DB) Close(ctx context.Context) error {
	return db.Client.Close(ctx)
}

func (db DB) Check(ctx context.Context) (*info.Response, error) {
	return db.Client.Info().Do(ctx)
}

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	db, err := NewDB()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close(context.Background())

	response, err := db.Check(context.Background())
	if err != nil {
		log.Fatal(err)
	}
	r, _ := json.Marshal(response)
	fmt.Println(string(r))
}
```

The `DB` struct is where all the database logic for the project will be defined. In the `NewDB` function, an instance of the Elasticsearch client is created. The Elasticsearch URL and the API key are read from the environment and passed as configuration arguments, to allow the client to authenticate. Notice that the first line in the `main` function calls `Load` from the `godotenv` package. This will read the variables that you stored in the *.env* file into the environment.

The `Close` function performs cleanup, by closing the Elasticearch client.

The `Check` function calls the `Info` method of the client and returns its response. Calling the `info` method is often done as a way to test that a connection to the Elasticsearch server can be established. If the call succeeds, some basic information about the Elasticsearch instance is returned.

In the `main` function, after importing the environment variables, an instance of `NewDB` is created, with a deferred call to `Close`. Then it calls the `Check` function and prints the result to the terminal. To print the response in a format that is easy to understand, it is marshaled as a JSON object.

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
