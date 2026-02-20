# Conclusion
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

Congratulations, you have reach the end of this tutorial!

We hope you have enjoyed this tutorial and are encouraged to learn more about Elasticsearch. The Elasticsearch documentation provides a great deal of information. In particular you may find the following sections of interest in your learning journey:

- [API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/)
- [Clients documentation](https://www.elastic.co/docs/reference/elasticsearch-clients)
- [Query languages](https://www.elastic.co/docs/reference/query-languages)

For your reference, below you can see the complete source code for the tutorial project that you built.

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py
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

    def add_document(self, document: dict[str, Any], id: str | None = None):
        self.client.index(index=self.index, id=id, document=document)

    def get_document(self, id: str):
        return self.client.get(index=self.index, id=id)

    def add_many_documents(self, data_file: str):
        def get_next_action() -> Iterator[dict[str, Any]]:
            id = 0
            with open(data_file, 'r') as f:
                for line in f:
                    document = json.loads(line)
                    id += 1
                    yield {'_index': self.index, '_id': str(id), '_source': document}

        response = bulk(client=self.client, actions=get_next_action(), stats_only=True)
        if response[1] != 0:
            raise RuntimeError('Bulk ingest failure')
        return response[0]

    def search(self, search_query):
        results = self.client.search(
            index=self.index,
            query={
                'multi_match': {
                    'query': search_query,
                    'fields': ['title', 'summary', 'content']
                }
            }
        )
        return results['hits']['hits']


if __name__ == '__main__':
    db = DB('documents')
    if sys.argv[1] == 'check':
        print(db.check())
    elif sys.argv[1] == 'create':
        db.create_index()
    elif sys.argv[1] == 'add':
        db.add_document({
            'title': 'Work From Home Policy',
            'category': 'teams',
            'content': 'The purpose of this full-time work-from-home policy is...',
        }, id='1')
    elif sys.argv[1] == 'get':
        response = db.get_document(sys.argv[2])
        print(response['_source'])
    elif sys.argv[1] == 'bulk':
        count = db.add_many_documents(sys.argv[2])
        print(f'Ingested {count} documents.')
    elif sys.argv[1] == 'search':
        results = db.search(sys.argv[2])
        for result in results:
            print(f'[{result["_score"]:.03f}] {result["_source"]["title"]} (id:{result["_id"]})')
    else:
        print('Error: unknown command')
```
::::

::::{tab-item} JavaScript
:sync: js
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

  async addDocument(document, id) {
    await this.client.index({ index: this.index, id: id, document: document });
  }

  async getDocument(id) {
    return await this.client.get({ index: this.index, id: id });
  }

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

  async search(searchQuery) {
    const results = await this.client.search({
      index: this.index,
      query: {
        multi_match: {
          query: searchQuery,
          fields: ['title', 'summary', 'content'],
        }
      }
    });
    return results.hits.hits;
  }
}

async function main() {
  const db = new DB('documents');
  if (process.argv[2] == 'check') {
    console.log(await db.check());
  }
  else if (process.argv[2] == 'create') {
    await db.createIndex('documents');
  }
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
  else if (process.argv[2] == 'bulk') {
    const count = await db.addManyDocuments(process.argv[3]);
    console.log(`${count} documents ingested.`);
  }
  else if (process.argv[2] == 'search') {
    const results = await db.search(process.argv[3]);
    for (const result of results) {
      console.log(`[${result._score.toFixed(3)}] ${result._source.title} (id:${result._id})`);
    }
  }
  else {
    console.log('Error: unknown command');
  }
}

main();
```
::::

::::{tab-item} Go
:sync: go

```go
package main

import (
    "bufio"
    "strconv"
    "github.com/elastic/go-elasticsearch/v9/esutil"
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"
    "strings"

    "github.com/elastic/go-elasticsearch/v9"
    "github.com/elastic/go-elasticsearch/v9/typedapi/core/get"
    "github.com/elastic/go-elasticsearch/v9/typedapi/core/info"
    "github.com/elastic/go-elasticsearch/v9/typedapi/core/search"
    "github.com/elastic/go-elasticsearch/v9/typedapi/types"
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

func (db DB) AddDocument(ctx context.Context, document string, id string) error {
    _, err := db.Client.Index(db.Index).Id(id).Raw(
        strings.NewReader(document),
    ).Do(context.Background())
    return err
}

func (db DB) GetDocument(ctx context.Context, id string) (*get.Response, error) {
    return db.Client.Get(db.Index, id).Do(ctx)
}

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

func (db DB) Search(ctx context.Context, searchQuery string) ([]types.Hit, error) {
    response, err := db.Client.Search().Index(db.Index).Request(&search.Request{
        Query: &types.Query{
            MultiMatch: &types.MultiMatchQuery{
                Query:  searchQuery,
                Fields: []string{"title", "summary", "content"},
            },
        },
    }).Do(ctx)
    if err != nil {
        return nil, err
    }
    return response.Hits.Hits, nil
}

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
    } else if os.Args[1] == "bulk" {
        count, err := db.AddManyDocuments(context.Background(), os.Args[2])
        if err == nil {
            fmt.Printf("Ingested %d documents.\n", count)
        }
    } else if os.Args[1] == "search" {
        results, err := db.Search(context.Background(), os.Args[2])
        if err == nil {
            for _, result := range results {
                var doc Document
                json.Unmarshal(result.Source_, &doc)
                fmt.Printf("[%.3f] %s (id:%s)\n", *result.Score_, doc.Title, *result.Id_)
            }
        }
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

