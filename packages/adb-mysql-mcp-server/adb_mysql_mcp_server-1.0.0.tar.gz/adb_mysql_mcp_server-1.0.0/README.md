# Adb MySQL MCP Server
Adb MySQL MCP Server serves as a universal interface between AI Agents and Adb MySQL databases. It enables seamless communication between AI Agents and Adb MySQL, helping AI Agents retrieve Adb MySQL database metadata and execute SQL operations.

## Configuration
### Mode 1: Using Local File
#### MCP Integration
Add the following configuration to the MCP client configuration file:
```json
"mcpServers": {
  "adb-mysql-mcp-server": {
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/alibabacloud-adb-mysql-mcp-server",
      "run",
      "adb-mysql-mcp-server"
    ],
    "env": {
      "ADB_MYSQL_HOST": "host",
      "ADB_MYSQL_PORT": "port",
      "ADB_MYSQL_USER": "database_user",
      "ADB_MYSQL_PASSWORD": "database_password",
      "ADB_MYSQL_DATABASE": "database"
    }
  }
}
```

### Mode 2: Using PIP Mode
#### Installation
Install MCP Server using the following package:
```bash
pip install adb-mysql-mcp-server
```

#### MCP Integration
Add the following configuration to the MCP client configuration file:
```json
  "mcpServers": {
    "adb-mysql-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "adb-mysql-mcp-server",
        "adb-mysql-mcp-server"
      ],
      "env": {
        "ADB_MYSQL_HOST": "host",
        "ADB_MYSQL_PORT": "port",
        "ADB_MYSQL_USER": "database_user",
        "ADB_MYSQL_PASSWORD": "database_password",
        "ADB_MYSQL_DATABASE": "database"
      }
    }
  }
```

## Components
### Tools
* `execute_sql`: Execute a SQL query in the Adb MySQL Cluster

* `get_query_plan`: Get the query plan for a SQL query

* `get_execution_plan`: Get the actual execution plan with runtime statistics for a SQL query

### Resources
#### Built-in Resources
* `adbmysql:///databases`: Get all the databases in the adb mysql cluster

#### Resource Templates
* `adbmysql:///{schema}/tables`: Get all the tables in a specific database

* `adbmysql:///{database}/{table}/ddl`: Get the DDL script of a table in a specific database

* `adbmysql:///{config}/{key}/value`: Get the value for a config key in the cluster

### Prompts
None at this time