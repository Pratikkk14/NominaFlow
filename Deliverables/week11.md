# Week 11 Deliverable Report — Docker Multi-Stage Image & Container Lifecycle Management

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Week 11 — Production Multi-Stage Dockerfile, Minimal Image Footprint, Container Lifecycle Verification, and Healthcheck Probes  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

In **Week 11**, we implemented the **Multi-Stage Production Containerization** for **NominaFlow**.

This milestone delivers:
1. **Multi-Stage `Dockerfile`**: Two-stage build process separating compiler build tools from the minimal runtime image, reducing image attack surface and artifact weight.
2. **Security Hardening**: Runs as an unprivileged non-root user (`appuser:appgroup` / UID: 1001).
3. **Container Healthcheck Probe**: Built-in HTTP liveness probe monitoring `http://localhost:8000/health` every 15 seconds.
4. **Verified Container Lifecycle**: Documented build, tag, run, logs, inspect, stop, and clean lifecycle operations.

---

## 2. Multi-Stage Docker Architecture (`Dockerfile`)

```dockerfile
# Stage 1: Build & Wheel Compilation
FROM python:3.12-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Hardened Runtime
FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PATH=/home/appuser/.local/bin:$PATH
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 curl && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup -s /bin/bash -m appuser && mkdir -p /app/uploads && chown -R appuser:appgroup /app
WORKDIR /app
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup pyproject.toml requirements.txt ./
USER appuser
RUN pip install --no-cache-dir --no-deps -e .
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "training_nomination.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 3. Container Lifecycle Verification Commands

| Action | Command | Purpose |
|---|---|---|
| **Build & Tag** | `docker build -t nominaflow-app:1.0.0 .` | Compiles image with semantic version tag |
| **Run Container** | `docker run -d -p 8000:8000 --name nominaflow_test nominaflow-app:1.0.0` | Starts background container mapping port 8000 |
| **Inspect Logs** | `docker logs -f nominaflow_test` | Streams Uvicorn startup logs |
| **Health Probe** | `docker inspect --format='{{json .State.Health.Status}}' nominaflow_test` | Confirms `"healthy"` status |
| **Stop & Remove**| `docker stop nominaflow_test && docker rm nominaflow_test` | Graceful shutdown and container cleanup |

---

## 4. Key Verification Metrics

| Verification Area | Expected Result | Observed Result | Status |
|---|---|---|---|
| **Multi-Stage Build** | Compiler tools excluded from final image | Final image size minimized | ✅ **Passed** |
| **Non-Root Execution** | Container runs as `UID 1001` (`appuser`) | Confirmed via `whoami` / `id` | ✅ **Passed** |
| **Healthcheck** | HTTP probe checks `/health` | Container state transitions to `healthy` | ✅ **Passed** |
| **Lifecycle Ops** | Start, stop, restart, inspect, delete verified | All Docker commands execute cleanly | ✅ **Passed** |

---

## 5. Summary & Next Milestone
Week 11 successfully delivers production containerization. Week 12 orchestrates the full stack using **Docker Compose (FastAPI + PostgreSQL + Nginx)**.
