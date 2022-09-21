# 使用prometheus数据
from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)


@app.route('/api/health')
def check_health():
    return "API is working well!"


@app.route('/api/graph/fields')
def fetch_graph_fields():
    nodes_fields = [{"field_name": "id", "type": "string"},
                    {"field_name": "title", "type": "string"},
                    {"field_name": "subTitle", "type": "string"},
                    {"field_name": "mainStat", "type": "string"},
                    {"field_name": "secondaryStat", "type": "number"},
                    {"field_name": "arc__failed", "type": "number", "color": "red", "displayName": "Failed"},
                    {"field_name": "arc__passed", "type": "number", "color": "green", "displayName": "Passed"},
                    {"field_name": "detail__role", "type": "string", "displayName": "Role"}]
    edges_fields = [
        {"field_name": "id", "type": "string"},
        {"field_name": "source", "type": "string"},
        {"field_name": "target", "type": "string"},
        {"field_name": "mainStat", "type": "number"},
    ]
    result = {"nodes_fields": nodes_fields,
              "edges_fields": edges_fields}
    return jsonify(result)


@app.route('/api/graph/data')
def fetch_graph_data():
    # 点
    # 线
    # traces_service_graph_request_total 客户端->服务端请求数量
    nodes = {}
    edges = {}
    url = 'http://10.10.30.32:9090/api/v1'
    r = requests.get(url + '/query?query=traces_service_graph_request_total')
    prom_result_set_json = r.json()['data']['result']
    for prom_result_json in prom_result_set_json:
        metric_label_json = prom_result_json['metric']  # label
        metric_value = int(prom_result_json['value'][1])  # 具体的值
        metric_label_client = metric_label_json['client']
        metric_label_server = metric_label_json['server']
        # 添加节点
        if metric_label_client not in nodes.keys():
            node_id = len(nodes.keys()) + 1
            nodes[metric_label_client] = Node(node_id, metric_label_client)
        nodes[metric_label_client].mainStat += metric_value
        nodes[metric_label_client].client_passed += metric_value

        if metric_label_server not in nodes.keys():
            node_id = len(nodes.keys()) + 1
            nodes[metric_label_server] = Node(node_id, metric_label_server)
        nodes[metric_label_server].mainStat += metric_value
        nodes[metric_label_server].server_passed += metric_value

        tracing_relation = (metric_label_client, metric_label_server)
        # 添加边
        if tracing_relation not in edges.keys():
            edge_id = len(edges.keys()) + 1
            edges[tracing_relation] = Edge(edge_id,
                                           nodes[metric_label_client].id,
                                           nodes[metric_label_server].id)
        edges[tracing_relation].mainStat += metric_value

    nodes_json = json.loads(json.dumps(list(nodes.values()), default=node_to_dict))
    edges_json = json.loads(json.dumps(list(edges.values()), default=edge_to_dict))
    result = {"nodes": nodes_json, "edges": edges_json}
    return jsonify(result)


def node_to_dict(node):
    return {
        'id': node.id,
        'title': node.title,
        'mainStat': node.f_main_stat(),
        # 'secondaryStat': node.f_secondary_stat(),
        'arc__failed': node.arc__failed,
        'arc__passed': node.arc__passed,
        'detail__role': node.detail__role
    }


def edge_to_dict(edge):
    return {
        'id': edge.id,
        'source': edge.source,
        'target': edge.target,
        'mainStat': edge.mainStat
    }


class Node:
    """
    id
    title
    subTitle
    mainStat
    secondaryStat
    arc__failed
    arc__passed
    detail__role
    """

    def __init__(self, id, title, detail__role="service"):
        self.id = id
        self.title = title
        self.mainStat = 0
        self.arc__failed = 0.0
        self.arc__passed = 1.0
        self.detail__role = detail__role
        self.client_passed = 0
        self.client_failed = 0
        self.server_passed = 0
        self.server_failed = 0

    def f_main_stat(self):
        return str(self.server_passed)

    def f_secondary_stat(self):
        return str(self.server_passed)


class Edge:
    """
    id
    source
    target
    mainStat
    """

    def __init__(self, id, source, target, mainStat=0):
        self.id = id
        self.source = source
        self.target = target
        self.mainStat = mainStat


app.run(host='0.0.0.0', port=5000)
