# OpenTelemetry Integration for xGitGuard

This document describes the OpenTelemetry integration added to xGitGuard for comprehensive observability.

## Overview

The integration provides:
- **Traces**: GitHub API calls, secret detection workflows
- **Metrics**: Request durations, detection counts, error rates  
- **Logs**: Structured application logs with correlation

## Architecture

```
xGitGuard App → OTLP → OpenTelemetry Collector → Backends
                                ├── Jaeger (traces)
                                ├── Prometheus (metrics)
                                └── File logs (logs)
```

## Quick Start

1. **Start the observability stack:**
   ```bash
   docker-compose up -d
   ```

2. **Set environment variables:**
   ```bash
   export GITHUB_API_KEY="your_github_token"
   export OTEL_SERVICE_NAME="xgitguard"
   export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run xGitGuard with telemetry:**
   ```bash
   cd xgitguard/github-public
   python public_cred_detections.py --help
   ```

## Access Dashboards

- **Jaeger UI**: http://localhost:16686 (traces)
- **Prometheus**: http://localhost:9090 (metrics)
- **Grafana**: http://localhost:3000 (dashboards, admin/admin)

## Configuration

### Environment Variables

- `OTEL_SERVICE_NAME`: Service name for telemetry (default: "xgitguard")
- `OTEL_EXPORTER_OTLP_ENDPOINT`: Collector endpoint (default: "http://localhost:4317")
- `GITHUB_API_KEY`: GitHub API token for testing

### Collector Configuration

The collector is configured in `otel-collector-config.yaml` to:
- Receive OTLP data on ports 4317 (gRPC) and 4318 (HTTP)
- Process with batching and memory limiting
- Export to Jaeger, Prometheus, and file logs

## Instrumented Components

1. **GitHub API Calls** (`github_calls.py`):
   - HTTP request tracing
   - Response time metrics
   - Error tracking

2. **Detection Workflows** (`*_cred_detections.py`):
   - End-to-end trace spans
   - Detection result metrics

3. **Logging** (`logger.py`):
   - Structured log correlation
   - OpenTelemetry log integration

## Testing

Run a simple detection to generate telemetry:
```bash
cd xgitguard/github-public
GITHUB_TOKEN=$GITHUB_API_KEY python public_cred_detections.py --search_query "password" --extension "py" --org "octocat"
```

Check the dashboards to see traces, metrics, and logs flowing through the system.
