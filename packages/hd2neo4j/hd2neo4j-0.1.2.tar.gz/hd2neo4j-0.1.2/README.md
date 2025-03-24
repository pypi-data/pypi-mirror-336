# hd2neo4j

`hd2neo4j` tool to transform heterogeneous data into a knowledge graph stored in Neo4j.

## Installation
```bash
pip install hd2neo4j
```

## Usage

### 1. Import Necessary Services
Import `RepositoryService` and `MapperService` from `hd2neo4j.services`, which handle the connection to Neo4j and data mapping, respectively.

```python
from hd2neo4j.services import RepositoryService, MapperService
```

### 2. Connect to Neo4j
Stablish a connection to the Neo4j database  using `RepositoryService`. 

```python
r_service: RepositoryService = RepositoryService(
    "neo4j://connection-uri:port", "user", "Neo4j_password", "database_name"
)
```

### 3. Load Configuration and Data
Two things are needed to start the mapping process:
- The mapping configuration JSON file.
- A data array to transform into a Neo4j graph. For large amounts of data, using a Python iterator is recommended.

### 4. Execute the Mapping Process
 initialize `MapperService` with the loaded configuration and data, and then the mapping process is executed by calling `start_mapping()`.

```python
m_service: MapperService = MapperService(
    mapping_config=config, 
    repository_service=r_service, 
    data_to_map=data
)

m_service.start_mapping()
```

### 5. (Optional) Clean the Database
If you want to clear the database before performing a new mapping, you can use:

```python
r_service.clean_graph_db()
```
