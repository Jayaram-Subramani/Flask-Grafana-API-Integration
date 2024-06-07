from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

GRAFANA_URL = "URL"
GRAFANA_USERNAME = "Username"
GRAFANA_PASSWORD = "Password1"

common_headers = {
    "Content-Type": "application/json",
    "X-Disable-Provenance": "true"
}

def get_alert_rules():
    url = f"{GRAFANA_URL}/api/v1/provisioning/alert-rules"
    try:
        response = requests.get(url, auth=(GRAFANA_USERNAME, GRAFANA_PASSWORD))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/get_alert_rules', methods=['GET'])
def get_alert_rules_route():
    alert_rules = get_alert_rules()
    return jsonify(alert_rules)

@app.route('/create_alert', methods=['POST'])
def create_alert():
    data = request.get_json()
    
    summary = data['summary']
    title = data['title']
    threshold = data['threshold']
    
    alert_payload ={
        "annotations": {
            "__dashboardUid__": "tmsOtSxZk",
            "__panelId__": "37",
            "summary": summary
        },
        "condition": "C",
        "data": [
            {
                "datasourceUid": "a0984061-310d-4940-8aab-f2885d04ecb4",
                "model": {
                    "datasource": {
                        "type": "cloudwatch",
                        "uid": "a0984061-310d-4940-8aab-f2885d04ecb4"
                    },
                    "dimensions": {},
                    "expression": "",
                    "hide": False,
                    "id": "",
                    "intervalMs": 20000,
                    "label": "",
                    "logGroups": [],
                    "matchExact": True,
                    "maxDataPoints": 932,
                    "metricEditorMode": 0,
                    "metricName": "CPUUtilization",
                    "metricQueryType": 0,
                    "namespace": "AWS/EC2",
                    "period": "60",
                    "queryMode": "Metrics",
                    "refId": "B",
                    "region": "default",
                    "sqlExpression": "",
                    "statistic": "Average"
                },
                "queryType": "",
                "refId": "B",
                "relativeTimeRange": {
                    "from": 600,
                    "to": 0
                }
            },
            {
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [
                        {
                            "evaluator": {
                                "params": [],
                                "type": "gt"
                            },
                            "operator": {
                                "type": "and"
                            },
                            "query": {
                                "params": [
                                    "A"
                                ]
                            },
                            "reducer": {
                                "params": [],
                                "type": "last"
                            },
                            "type": "query"
                        }
                    ],
                    "datasource": {
                        "type": "__expr__",
                        "uid": "__expr__"
                    },
                    "expression": "B",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "reducer": "last",
                    "refId": "A",
                    "type": "reduce"
                },
                "queryType": "",
                "refId": "A",
                "relativeTimeRange": {
                    "from": 600,
                    "to": 0
                }
            },
            {
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [
                        {
                            "evaluator": {
                                "params": [
                                    threshold
                                ],
                                "type": "gt"
                            },
                            "operator": {
                                "type": "and"
                            },
                            "query": {
                                "params": [
                                    "C"
                                ]
                            },
                            "reducer": {
                                "params": [],
                                "type": "last"
                            },
                            "type": "query"
                        }
                    ],
                    "datasource": {
                        "type": "__expr__",
                        "uid": "__expr__"
                    },
                    "expression": "A",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "C",
                    "type": "threshold"
                },
                "queryType": "",
                "refId": "C",
                "relativeTimeRange": {
                    "from": 600,
                    "to": 0
                }
            }
        ],
        "execErrState": "Error",
        "folderUID": "b4fe6dad-bf98-4c09-bb1a-659dc093a68d",
        "for": "5m",
        "id": 1383,
        "isPaused": False,
        "labels": {
            "CPU": "threshold"
        },
        "noDataState": "NoData",
        "orgID": 1,
        "ruleGroup": title,
        "title": title
    }
    base_url = f"{GRAFANA_URL}/api/v1/provisioning/alert-rules"
    try:
        response = requests.post(base_url, auth=(GRAFANA_USERNAME, GRAFANA_PASSWORD), headers=common_headers, data=json.dumps(alert_payload))
        print(response)
        return jsonify("message : alert created successfully")
    except Exception as e:
        return jsonify({"message": str(e)})


def get_dashboard(api_url):
    url = f"{api_url}/api/search"
    try:
        response = requests.get(url, headers=common_headers, auth=(GRAFANA_USERNAME, GRAFANA_PASSWORD))

        if response.status_code == 200:
            dashboard_data = response.json()
            return dashboard_data
        else:
            return {"error": f"Failed to fetch dashboard. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@app.route('/api/dashboard/uid/<dashboard_uid>', methods=['GET'])
def fetch_dashboard(dashboard_uid):
    if not dashboard_uid:
        return jsonify({"error": "Dashboard UID is required. Please provide 'dashboard_uid' as a query parameter."})

    dashboard_data = get_dashboard(GRAFANA_URL)

    if "error" in dashboard_data:
        return jsonify({"error": dashboard_data["error"]})
    else:
        return jsonify(dashboard_data)


@app.route('/get_all_folders', methods=['GET'])
def get_all_folders():
    url = f"{GRAFANA_URL}/api/folders"
    try:
        response = requests.get(url, headers=common_headers, auth=(GRAFANA_USERNAME, GRAFANA_PASSWORD))

        if response.status_code == 200:
            folders = response.json()
            return jsonify(folders)
        else:
            return jsonify({"error": f"Failed to get folders. Status code: {response.status_code}"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})


@app.route('/uid/<dashboard_uid>', methods=['GET'])
def fetch_all_panels(dashboard_uid):
    try:
        url = f"{GRAFANA_URL}/api/dashboards/uid/{dashboard_uid}"
        response = requests.get(url, headers=common_headers, auth=(GRAFANA_USERNAME, GRAFANA_PASSWORD))

        if response.status_code == 200:
            panels = response.json()

            if "dashboard" in panels:
                dashboard_data = panels['dashboard']
                panels = dashboard_data['panels']
                data = []

                for panel in panels:
                    panel_id = panel['id']
                    panel_title = panel['title']
                    result = {"panel_id": panel_id, "panel_title": panel_title}
                    data.append(result)
                return jsonify(data), 200
            else:
                return jsonify({"error": "Failed to fetch panels from dashboard data."})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)
