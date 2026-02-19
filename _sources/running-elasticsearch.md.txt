# Running Elasticsearch
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

This section will show you how to run Elasticsearch on your computer.

There are many different ways to install Elasticsearch, ranging from simple, local installs intended for development and testing to production-grade multi-node clusters. For this tutorial you are going to take a simple approach based on Elastic's [start-local](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/local-development-installation-quickstart) project.

To use `start-local`, you need to have Docker and Docker Compose installed on your computer. The easiest way to get these tools is by installing [Docker Desktop](https://www.docker.com/products/docker-desktop/).

:::{tip}
You can make sure that you are ready to run the `start-local` installer by typing the command `docker compose` on your shell prompt. If successful, the command should print a help message. You can review the [start-local prerequisites](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/local-development-installation-quickstart#local-dev-prerequisites) for additional details.
:::

While having the *elasticsearch-tutorial* directory you created earlier as your current directory, run the `start-local` installer:

```bash
cd ~/Documents/elasticsearch-tutorial
curl -fsSL https://elastic.co/start-local | sh
```

The installer will run for a few minutes. The output should look similar to the following:

```bash
  ______ _           _   _
 |  ____| |         | | (_)
 | |__  | | __ _ ___| |_ _  ___
 |  __| | |/ _` / __| __| |/ __|
 | |____| | (_| \__ \ |_| | (__
 |______|_|\__,_|___/\__|_|\___|
-------------------------------------------------
🚀 Run Elasticsearch and Kibana for local testing
-------------------------------------------------

ℹ️  Do not use this script in a production environment

⌛️ Setting up Elasticsearch and Kibana v9.3.0-arm64...

- Generated random passwords
- Created the /Users/miguelgrinberg/Documents/elastic-start-local folder containing the files:
  - .env, with settings
  - configuration files for Kibana and EDOT (if selected)
  - start/stop/uninstall commands
- Initializing and starting containers...

Creating network 'es-local-dev-net' ... done (created).
Creating container 'es-local-dev' from image 'docker.elastic.co/elasticsearch/elasticsearch:9.3.0-arm64' ... done (created).
Creating container 'kibana-local-dev' from image 'docker.elastic.co/kibana/kibana:9.3.0-arm64' ... done (created).
Starting container 'es-local-dev' ... done.
Waiting for 'es-local-dev' ... healthy.
Creating Elasticsearch API key ... done.
Setting up 'kibana_system' user password ... done.
Starting container 'kibana-local-dev' ... done.
Waiting for 'kibana-local-dev' ... healthy.

🎉 Congrats, Elasticsearch and Kibana are installed and running!

🌐 Open your browser at http://localhost:5601

   Username: elastic
   Password: XXXXXXX

🔌 Elasticsearch API endpoint: http://localhost:9200
🔑 API key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Learn more at https://github.com/elastic/start-local
```

Your local instance of Elasticsearch should now be up and running, and you should have a *elastic-start-local* sub-directory in your project.

:::{tip}
You will find scripts to stop, restart or uninstall start-local in the *elastic-start-local* sub-directory.
:::

Near the bottom of the `start-local` output you have the credentials that you will use to access your Elasticsearch instance. To make it convenient to use these credentials, it is a good idea to save them in a configuration file.

Open your favorite code editor and create a new file named *.env* (that is a dot, followed by the letters `env`) in the *elasticsearch-tutorial* directory. Write the following configuration variables on this file, replacing the Xs with the information that `start-local` printed to your console:

```bash
ELASTICSEARCH_URL=http://localhost:9200
KIBANA_URL=http://localhost:5601
ELASTIC_USERNAME=elastic
ELASTIC_PASSWORD=XXXXXXX
ELASTIC_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

:::{hint}
The `start-local` installer script also installs and runs and instance of Kibana, a web-based administration environment for Elasticsearch. You will not need Kibana for this tutorial, but you are welcome to explore by navigating to *http://localhost:5601* in your browser and logging in with your assigned username and password.
:::
