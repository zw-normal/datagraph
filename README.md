# Datagraph

The core of datagraph builds a simple graph structure for expressing how to reading, calculating and outputting data based on popular Python Data Analysis Library pandas. On the top of core, it uses Django to build the backend engine and Typescript, Bootstrap, D3 and Vega-Lite to build the frontend for storing and rendering data from customizable data source.

A deployed site can be accessed at http://104.225.140.184/.

## Frontend

![Alt text](doc/Workbench.png?raw=true "Workbench")

![Alt text](doc/Browser.png?raw=true "Workbench")

## Graph Engine

The core `graph` and `engine` Django apps together allow defining unlimited data `reader`, `calculator`, `aggregator` and `writer` by following the convention of module and function name.

### Data Reader

Data Reader acts as data source, defines the data source, mostly about how to read and interpret them into pandas Dataframe. A manual data reader is also supported. 

### Data Calculator

Data Calculator defines how to transform data from upstream data nodes, such as drop nan data or selecting special columns etc.

### Data Aggregator

Data Aggregator combines data from upstream data nodes, like combines columns etc.

### Data Writer

Data Writer allows output upstream data in different formats, for example, generating vega-lite chart specification for displaying on the frontend.
