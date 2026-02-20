# Project Set Up
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

In this section you will create a new project and add all the dependencies to it, including the official Elasticsearch client for your chosen programming language.

Find a suitable parent directory for the project such as your *Documents* directory, and create a project directory named *elasticsearch-tutorial* in it:

```bash
cd ~/Documents
mkdir elasticsearch-tutorial
cd elasticsearch-tutorial
```

:::::{tab-set}
:sync-group: lang
:class: invisible-tabs

::::{tab-item} Python
:sync: py

Following Python best practices, the next step is to create a *virtual environment*, which is a private copy of the Python interpreter dedicated to this project.

:::{tip}
Python supports many different ways to create virtual environments. Feel free to use your favorite method, if you have one.
:::

Make sure your current directory is the *elasticsearch-tutorial* directory you created above, and then enter the following commands to create the virtual environment:

```bash
python -m venv .venv
```

This command creates a Python virtual environment in the **.venv** (dot-venv) directory. You can replace `.venv` in this command with any name that you like. Note that in some installations of Python, you may need to use `python3` instead of `python` to invoke the Python interpreter.

Once the virtual environment is created, the next step is to *activate* it. Activating a virtual environment makes it the active Python environment for the shell session you are in. The activation command is as follows:

```bash
source .venv/bin/activate
```

After the virtual environment is activated, the command-line prompt changes to show the name of the environment:

```bash
(.venv) $ _
```

:::{tip}
If you haven't used Python virtual environments before, you should keep in mind that the activation command is not permanent and only applies to the terminal session in which the command is entered. When you open another terminal window, you have to repeat the activation command.
:::

The last step to configure the Python environment is to install the Python packages that you will need to use in this tutorial. Make sure that the virtual environment was activated in the previous step, and then run the following command to install these packages:

```bash
pip install elasticsearch python-dotenv
```

The command adds two dependencies to the project:

- `elasticsearch`: the official Elasticsearch Python client
- `python-dotenv`: a package that reads configuration variables from a file. You will use it to import your Elasticsearch credentials from a configuration file.

::::

::::{tab-item} JavaScript
:sync: js

The next step is to create a JavaScript project in this directory. Make sure your current directory is the *elasticsearch-tutorial* directory you created above, and then enter the following commands to initialize the project:

```bash
npm init -y
```

To complete the project creation, you will install the package dependencies that you will need to use in this tutorial. Run the following command to install these packages:

```bash
npm install @elastic/elasticsearch dotenv
```

The command adds two dependencies to the project:

- `@elastic/elasticsearch`: the official Elasticsearch JavaScript client
- `dotenv`: a package that reads configuration variables from a file. You will use it to import your Elasticsearch credentials from a configuration file.

::::

:::::
