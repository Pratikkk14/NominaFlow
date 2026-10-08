# Week 12 Deliverable Report — Multi-Container Topology & Continuous Deployment with Docker Compose

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Week 12 — Docker Compose Topology (FastAPI Backend + PostgreSQL 16 + Nginx Reverse Proxy) & One-Command Deployment  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

In **Week 12**, we implemented and verified the **Multi-Container Production Topology** and Continuous Deployment configuration for **NominaFlow**.

This milestone delivers:
1. **Multi-Service Docker Compose Architecture (`docker-compose.yml`)**:
   - `backend`: Containerized FastAPI application running via Uvicorn.
   - `db`: Dedicated PostgreSQL 16 Alpine container with database health checks and named persistent volume (`postgres_data`).
   - `proxy`: Nginx reverse proxy routing port 80 traffic to the internal backend service on port 8000.
2. **Persistent Volumes**: Independent persistence for database records (`postgres_data`) and user-uploaded nomination documents (`app_uploads`).
3. **Automated Service Dependencies**: `backend` waits for `db` to be completely healthy before accepting traffic (`depends_on: { db: { condition: service_healthy } }`).

---

## 2. Multi-Container Service Topology

```text
                               Client Browser
                                     │
                                     │ HTTP (Port 80)
                                     ▼
                      ┌──────────────────────────────┐
                      │    nominaflow_proxy (Nginx)   │
                      └──────────────┬───────────────┘
                                     │
                                     │ Reverse Proxy (Port 8000)
                                     ▼
                      ┌──────────────────────────────┐
                      │  nominaflow_backend (FastAPI) │
                      └──────────────┬───────────────┘
                                     │
                                     │ SQL Queries (Port 5432)
                                     ▼
                      ┌──────────────────────────────┐
                      │    nominaflow_db (PostgreSQL)│
                      └──────────────────────────────┘
```

---

## 3. One-Command Continuous Deployment Verification

| Step | Command | Action & Outcome |
|---|---|---|
| **1. Deploy Stack** | `docker compose up -d` | Builds backend image, starts PostgreSQL, waits for health check, and spins up Nginx |
| **2. Check Status** | `docker compose ps` | All 3 containers show `Up` and `healthy` |
| **3. Stream Logs** | `docker compose logs -f` | Real-time unified logging across all services |
| **4. Teardown** | `docker compose down -v` | Graceful stop and cleanup of containers and networks |

---

## 4. Key Verification Metrics

| Service Component | Port Mapping | Health Strategy | Status |
|---|---|---|---|
| **`nominaflow_proxy`** | `80:80` | Automatic restart policy | ✅ **Verified** |
| **`nominaflow_backend`** | `8000` (Internal) | HTTP `/health` probe | ✅ **Verified** |
| **`nominaflow_db`** | `5432:5432` | `pg_isready -U nominaflow` | ✅ **Verified** |
| **Persistent Volumes** | Named Volumes | Data survives container restarts | ✅ **Verified** |

---

## 5. Summary & Next Milestone
Weeks 11 & 12 complete the Docker containerization and Compose deployment milestones. Next, **Weeks 13 & 14** introduce **Ansible Configuration Management, Infrastructure Automation, and Systemd Service Provisioning**.
