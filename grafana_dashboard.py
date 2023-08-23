#!/usr/bin/env python3.7

"""Module for creating data source and dashboard in Grafana"""

import requests
import json
import os
from dotenv import load_dotenv

from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT
)
from grafanalib._gen import DashboardEncoder

grafana_url = 'http://localhost:3000'

def send_post_request(uri, body):
    load_dotenv()
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': "Bearer " + os.getenv('TOKEN')
    }
    resp = requests.post(grafana_url + uri, data=body, headers=headers)
    return resp.json()

def create_data_source():
    body = {
      "name":"prometheus",
      "type":"prometheus",
      "url":"http://docker.for.mac.localhost:9090",
      "access":"proxy",
      "basicAuth":False
    }
    response = send_post_request("/api/datasources", json.dumps(body))
    print(response)

def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    return json.dumps(
        {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite,
            "message": message
        }, sort_keys=True, indent=2, cls=DashboardEncoder)

def create_dashboard():
    dashboard = Dashboard(
    title="Python generated example dashboard",
    timezone="browser",
    panels=[
        TimeSeries(
            title="CPU load",
            dataSource='prometheus',
            targets=[
                Target(
                    expr='java_lang_OperatingSystem_CpuLoad',
                    legendFormat="{{ handler }}",
                    refId='A',
                ),
            ],
            unit=OPS_FORMAT,
            gridPos=GridPos(h=20, w=20, x=0, y=0),
        ),
      ],
    ).auto_panel_ids()
    body = get_dashboard_json(dashboard)
    response = send_post_request("/api/dashboards/db", body)
    print(response)

#create_data_source()
create_dashboard()