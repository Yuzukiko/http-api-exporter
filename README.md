# http-api-exporter
[![Docker Image CI](https://github.com/Yuzukiko/http-api-exporter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Yuzukiko/http-api-exporter/actions/workflows/docker-image.yml)

Prometheus exporter for results of http api requests\
Metrics are exported on port 5000 (default) on endpoint /metrics

[Docker Hub](https://hub.docker.com/repository/docker/yuzukiko/http-api-exporter)

## env list
| env      | value                                                             | default | mandatory |
|----------|-------------------------------------------------------------------|---------|-----------|
| API_LIST | [{"name": "", "description":"", "url":"", "request_interval":10}] |         | yes       |
| PORT     | Number                                                            | 5000    | no        |
| DEBUG    | True/False                                                        | False   | no        |

Request_interval is in seconds
