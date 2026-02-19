# Searching
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

In this section you are going to learn how to run full-text searches on the index you have built.

Elasticsearch provides several options to conduct searchs. For this tutorial you are going to use the [Query DSL](https://www.elastic.co/docs/explore-analyze/query-filter/languages/querydsl), a JSON-style query language.

## Searching an index field

The most basic way to search an index is to look for a specific word or sequence of words in a text field of the index. In the Query DSL this is called a [Match](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query) query.

Here is an example of a match query:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
client.search(
    index='documents',
    query={
        'match': {
            'content': 'work from home',
        }
    }
)
```
::::

::::{tab-item} JavaScript
:sync: js
```js
await self.client.search({
  index: 'documents',
  query: {
    match: {
      content: 'work from home',
    }
  }
});
```
::::

:::::

In this example, the `content` field of the 'documents' index is searched for the words `work from home`. The return value from the `search` method includes the documents that were found, each with a relevance score.

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
    def search(self, search_query):
        results = self.client.search(
            index=self.index,
            query={
               'match': {
                    'content': search_query,
                }
            }
        )
        return results['hits']['hits']
```

The expresion `results['hits']['hits']` returns the list of documents that were found.

::::

::::{tab-item} JavaScript
:sync: js
```js
  async search(searchQuery) {
    const results = await this.client.search({
      index: this.index,
      query: {
        match: {
          content: searchQuery,
        }
      }
    });
    return results.hits.hits;
  }
```

The expresion `results.hits.hits` returns the list of documents that were found.
::::

:::::

:::{hint}
The response from a search includes a lot of useful information beyond the list of documents. Review all of its fields in the [documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-responses).
:::

To use the search feature, add a `search` command-line argument that runs a search and prints the results:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
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
  else if (process.argv[2] == 'search') {
    const results = await db.search(process.argv[3]);
    for (const result of results) {
      console.log(`[${result._score.toFixed(3)}] ${result._source.name} (id:${result._id})`);
    }
  }
  else {
    console.log('Error: valid commands are check, create, add, get, bulk and search');
  }
```
::::

:::::

You can see that each result includes a `_score` attribute. This is the relevance score, with higher values meaning higher relevance. The `_source` field includes the document data, and `_id` includes the unique identifier of the document, both seen already.

You are now ready to search the index:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```bash
python main.py search "work from home"
```
::::

::::{tab-item} JavaScript
:sync: js
```bash
node main.js search "work from home"
```
::::

:::::

The result is the list of documents that were found with the given words. The `search` command in this application prints the relevance score, the title and the identifier of each returned document.

```
[6.235] Work From Home Policy (id:1)
[1.436] Wfh Policy Update May 2023 (id:3)
[1.302] Company Vacation Policy (id:5)
[1.300] Code Of Conduct (id:9)
[1.282] Office Pet Policy (id:10)
[1.107] New Employee Onboarding Guide (id:15)
[0.994] Sales Engineering Collaboration (id:7)
[0.820] Updating Your Tax Elections Forms (id:14)
[0.803] Performance Management Policy (id:11)
[0.522] April Work From Home Update (id:2)
```

Feel free to try other search terms to see different results. If you want to see any of the returned documents in more detail, you can use the `get` command to retrieve it by its `id` and see its contents.

## Searching multiple fields at once

The search from the previous section is configured to look at the `content` field of the index. In some cases this is sufficient, but many indexes (including the one in this tutorial) have more than one text field. When there are multiple text fields, it could be useful to run a search across all of the fields, and not just one.

To run a search on multiple fields, the [Multi-match](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-multi-match-query) query can be used.

Instead of adding yet another method, this time update the existing `search` method to use multi-match instead of the simple match:

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
```python
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
```
::::

::::{tab-item} JavaScript
:sync: js
```js
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
```
::::

:::::

The multi-match query uses a slightly different format that makes it possible to provide a list of fields to search. If you repeat a search with the updated search you will likely notice that the ranking of results is different, because now the three text fields in the index are used instead of just one.

Below you can see the results for the "work for home" search used above. Note how there are some documents were rated higher than before due to having the words in the query in the additional fields added to the search:

```
[6.235] Work From Home Policy (id:1)
[4.890] April Work From Home Update (id:2)
[3.225] Wfh Policy Update May 2023 (id:3)
[2.230] Company Vacation Policy (id:5)
[1.387] Intellectual Property Policy (id:8)
[1.300] Code Of Conduct (id:9)
[1.282] Office Pet Policy (id:10)
[1.168] Updating Your Tax Elections Forms (id:14)
[1.107] New Employee Onboarding Guide (id:15)
[0.994] Sales Engineering Collaboration (id:7)
```

:::::{invisible-tab-set}
:sync-group: lang

::::{tab-item} Python
:sync: py
&nbsp;
::::

::::{tab-item} JavaScript
:sync: js
&nbsp;
::::

:::::

