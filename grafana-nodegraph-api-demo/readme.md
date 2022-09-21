### 说明

为Grafana插件`nodegraph-api-plugin`提供REST api数据。

插件：https://github.com/hoptical/nodegraph-api-plugin

The REST API application should handle three requests: `fields`, `data`, and `health`. They are described below.

#### Fetch Graph Fields
This route returns the nodes and edges fields defined in the parameter tables. It would help the plugin to create desired parameters for the graph. For nodes, id and for edges, id, source, and target fields are required. Other fields are optional.

endpoint: /api/graph/fields

method: GET

content type: application/json

content format example:

```json
{
  "edges_fields": [
    {
      "field_name": "id",
      "type": "string"
    },
    {
      "field_name": "source",
      "type": "string"
    },
    {
      "field_name": "target",
      "type": "string"
    },
    {
      "field_name": "mainStat",
      "type": "number"
    }
  ],
  "nodes_fields": [
    {
      "field_name": "id",
      "type": "string"
    },
    {
      "field_name": "title",
      "type": "string"
    },
    {
      "field_name": "mainStat",
      "type": "string"
    },
    {
      "field_name": "secondaryStat",
      "type": "number"
    },
    {
      "color": "red",
      "field_name": "arc__failed",
      "type": "number"
    },
    {
      "color": "green",
      "field_name": "arc__passed",
      "type": "number"
    },
    {
      "displayName": "Role",
      "field_name": "detail__role",
      "type": "string"
    }
  ]
}
```

#### Fetch Graph Data

This route returns the graph data, which is intended to visualize.

endpoint: /api/graph/data

method: GET

content type: application/json

Data Format example:

```json
{
    "edges": [
        {
            "id": "1",
            "mainStat": "53/s",
            "source": "1",
            "target": "2"
        }
    ],
    "nodes": [
        {
            "arc__failed": 0.7,
            "arc__passed": 0.3,
            "detail__zone": "load",
            "id": "1",
            "subTitle": "instance:#2",
            "title": "Service1"
        },
        {
            "arc__failed": 0.5,
            "arc__passed": 0.5,
            "detail__zone": "transform",
            "id": "2",
            "subTitle": "instance:#3",
            "title": "Service2"
        }
    ]
}
```
For more detail of the variables, please visit here.

#### Health
This route is for testing the health of the API, which is used by the Save & Test action while adding the plugin.(Part 2 of the Getting Started Section). Currently, it only needs to return the 200 status code in case of a successful connection.

endpoint: /api/health

method: GET

success status code: 200