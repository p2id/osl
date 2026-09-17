# Zero-Cost Architecture

## Objective

Run the core development and automation workflow without mandatory paid APIs, paid hosting, or paid infrastructure.

## Local-First Stack

- Linux
- Git
- Docker
- Python
- FastAPI
- PostgreSQL
- Redis
- Ollama or llama.cpp
- local open-weight models
- pytest
- Ruff
- mypy where useful
- MkDocs
- Prometheus
- Grafana
- Caddy

## External Services

External services are optional accelerators, not architectural requirements.

The system should continue to function when an external AI provider, cloud service, or hosted database is unavailable.

## Resource Strategy

Prefer:

- CPU inference for small workloads;
- GPU inference when hardware is available;
- small models for classification and routing;
- larger models only for difficult tasks;
- caching for repeated work;
- queues for controlled concurrency;
- local storage before object storage;
- public repositories and free CI where appropriate.

## Scaling Path

`One Workstation → Multiple Local Workers → Optional VPS → Optional GPU Worker Pool → Hybrid Infrastructure`

Scaling should be triggered by measurable workload requirements rather than assumed capacity.
