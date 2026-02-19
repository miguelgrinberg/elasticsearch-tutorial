# Conclusion
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

Congratulations, you have reach the end of this tutorial!

We hope you have enjoyed this tutorial and are encouraged to learn more about Elasticsearch. The Elasticsearch documentation provides a great deal of information. In particular you may find the following sections of interest in your learning journey:

- [API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/)
- [Clients documentation](https://www.elastic.co/docs/reference/elasticsearch-clients)
- [Query languages](https://www.elastic.co/docs/reference/query-languages)

For your reference, below you can see the complete source code for the tutorial project that you built.

:::::{invisible-tab-set}
:sync-group: lang

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
                    'fields': ['name', 'summary', 'content']
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
            'name': 'Work From Home Policy',
            'category': 'teams',
            'content': 'The purpose of this full-time work-from-home policy is...',
            'created_on': '2023-11-02',
        }, id='1')
    elif sys.argv[1] == 'get':
        print(db.get_document(sys.argv[2]))
    elif sys.argv[1] == 'bulk':
        count = db.add_many_documents(sys.argv[2])
        print(f'Ingested {count} documents.')
    elif sys.argv[1] == 'search':
        results = db.search(sys.argv[2])
        for result in results:
            print(f'[{result["_score"]:.03f}] {result["_source"]["name"]} (id:{result["_id"]})')
    else:
        print('Error: valid commands are check, create, add, get, bulk and search')
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
          fields: ['name', 'summary', 'content'],
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
      name: 'Work From Home Policy',
      category: 'teams',
      content: 'The purpose of this full-time work-from-home policy is...',
      created_on: '2023-11-02',
    }, '1');
  }
  else if (process.argv[2] == 'get') {
    console.log(await db.getDocument(process.argv[3]));
  }
  else if (process.argv[2] == 'bulk') {
    const count = await db.addManyDocuments(process.argv[3]);
    console.log(`${count} documents ingested.`);
  }
  else if (process.argv[2] == 'search') {
    const results = await db.search(process.argv[3]);
    for (const result of results) {
      console.log(`[${result._score.toFixed(3)}] ${result._source.name} (id:${result._id})`);
    }
  }
  else {
    console.log('Error: valid commands are check, create, add, get, bulk and search');
  }
}

main();
```
::::

:::::

