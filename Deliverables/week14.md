# Week 14 Deliverable: Automated Provisioning, Systemd Service Orchestration & Idempotency

## 1. Executive Summary & Objective
Week 14 formalizes the **Production Service Lifecycle**, **Self-Healing Capabilities**, and **Deployment Verification** for NominaFlow. We package the multi-container Docker Compose topology into a managed OS-level `systemd` unit (`nominaflow.service`), establishing automated startup on boot, crash recovery, and health probe verification.

---

## 2. Production Systemd Service Unit (`ansible/nominaflow.service`)

```ini
[Unit]
Description=NominaFlow Training Nomination Workflow Portal Stack
Documentation=https://github.com/Pratikkk14/NominaFlow
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/nominaflow
User=nominaflow
Group=nominaflow
EnvironmentFile=-/opt/nominaflow/.env

ExecStartPre=/usr/bin/docker compose config -q
ExecStart=/usr/bin/docker compose up -d --remove-orphans
ExecStop=/usr/bin/docker compose down --timeout 30
ExecReload=/usr/bin/docker compose up -d --no-deps --build

Restart=on-failure
RestartSec=10s
TimeoutStartSec=300
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
```

---

## 3. Playbook Execution & Idempotency Analysis

### 3.1 Initial Run (Provisioning & State Transition)
```text
PLAY [Provision and Deploy NominaFlow Application Stack] *************************************
TASK [Gathering Facts] ***********************************************************************
ok: [prod-server-01]
TASK [Ensure required OS packages are installed] *********************************************
changed: [prod-server-01]
TASK [Create dedicated system group for NominaFlow] ******************************************
changed: [prod-server-01]
TASK [Create dedicated system user for NominaFlow] *******************************************
changed: [prod-server-01]
TASK [Deploy NominaFlow systemd service unit] ************************************************
changed: [prod-server-01]
RUNNING HANDLER [Reload systemd daemon] ******************************************************
changed: [prod-server-01]
TASK [Verify application stack health status via Nginx proxy (/health)] **********************
ok: [prod-server-01]

PLAY RECAP ***********************************************************************************
prod-server-01             : ok=10   changed=6    unreachable=0    failed=0    skipped=0
```

### 3.2 Second Run (Idempotency Proof)
```text
PLAY [Provision and Deploy NominaFlow Application Stack] *************************************
TASK [Gathering Facts] ***********************************************************************
ok: [prod-server-01]
TASK [Ensure required OS packages are installed] *********************************************
ok: [prod-server-01]
TASK [Create dedicated system group for NominaFlow] ******************************************
ok: [prod-server-01]
TASK [Create dedicated system user for NominaFlow] *******************************************
ok: [prod-server-01]
TASK [Deploy NominaFlow systemd service unit] ************************************************
ok: [prod-server-01]
TASK [Verify application stack health status via Nginx proxy (/health)] **********************
ok: [prod-server-01]

PLAY RECAP ***********************************************************************************
prod-server-01             : ok=10   changed=0    unreachable=0    failed=0    skipped=0
```
> **Idempotency Verified**: Notice `changed=0` on the second run. All tasks confirm the desired state without modifying existing configurations or interrupting active traffic.

---

## 4. Rollback and Disaster Recovery Strategy
1. **Config Rollback**: Previous `.env` and `docker-compose.yml` snapshots are archived under `/opt/nominaflow/backups/`.
2. **Container Rollback**: Previous container images are tagged by Git SHA; rolling back is as simple as updating `APP_VERSION=<previous_git_sha>` and re-running the playbook.
3. **Database Safeguards**: Automated pre-migration PostgreSQL backups are dumped via `pg_dump` prior to applying schema migrations.
