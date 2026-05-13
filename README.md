# Platform Engineer Demo – Compliance-as-Code, Traceable Reasoning, Governed Memory

A complete platform engineering showcase that bakes security, auditability, and privacy directly into the application code. This project implements three core principles required by modern regulated environments:

- **Compliance-as-Code**: Every significant action emits an immutable audit event. Access policies are versioned and tested in CI.
- **Traceable Reasoning**: Automated decisions (e.g., loan approval) record the full reasoning chain so that any outcome can be explained to a human auditor.
- **Governed Memory**: Context is stored without personally identifiable information (PII), supports right‑to‑be‑forgotten, and enforces data residency / consent.

The demo consists of a containerised FastAPI backend serving a React frontend, a GitHub Actions CI/CD pipeline, Terraform for infrastructure, and Kubernetes manifests with Prometheus monitoring – all following the above principles.

## Architecture

```
[User] → React UI → FastAPI backend → (audit logs, memory store)
                 ↓ CI/CD
[GitHub] → GitHub Actions → Terraform → AKS/EKS → K8s (Deployment, NetworkPolicy)
                 ↓ Monitoring
[Prometheus + Grafana] ← AlertManager
```

## Tech Stack

| Layer              | Technology                           |
|--------------------|--------------------------------------|
| Backend            | Python 3.10, FastAPI, Uvicorn        |
| Frontend           | React (served as static files)       |
| Containerisation   | Docker, Docker Compose               |
| CI/CD              | GitHub Actions (lint, test, OPA, Trivy) |
| Infrastructure     | Terraform (Azure / AWS)              |
| Orchestration      | Kubernetes (AKS/EKS/Kind)            |
| Monitoring         | Prometheus, Grafana, Alertmanager    |
| Policy as Code     | Open Policy Agent (Rego)             |
| Security Scanning  | Trivy                                |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/) and Docker Compose
- Python 3.10+ (for local development)
- Node.js 18+ (to rebuild the frontend)
- Git

### Run with Docker Compose (recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd platform-demo-principles

# Build and start the backend (includes the frontend)
docker-compose up -d --build
```

The application will be available at:
- **Frontend**: [http://localhost:8000](http://localhost:8000) (served by FastAPI)
- **API health**: [http://localhost:8000/health](http://localhost:8000/health)

### Run locally (without Docker)

```bash
cd app
pip install -r requirements.txt

# Build frontend
cd ../frontend
npm install && npm run build
mkdir -p ../app/static
cp -r build/* ../app/static/

# Run backend
cd ../app
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testing

Tests verify that the Compliance-as-Code (audit logger) and Governed Memory (PII filtering, right‑to‑be‑forgotten) are working correctly.

```bash
cd app
python -m pytest tests/ -v
```

You should see **4 tests passing**.

## CI/CD Pipeline

The pipeline is defined in `.github/workflows/`:

- **CI** (on push/PR): linting, unit tests, Trivy security scan, OPA policy check on Kubernetes manifests.
- **CD** (on merge to main): Terraform apply to provision an AKS cluster, deploy K8s manifests, install Prometheus monitoring.

To see it in action, simply push to GitHub and navigate to the **Actions** tab.

## Project Structure (auto-generated)
platform-demo-principles/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── audit_logger.py
│   ├── memory_governor.py
│   ├── items_storage.py
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── test_audit.py
│       ├── test_compliance.py
│       └── test_memory.py
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── network-policy.yaml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── compliance_test.feature
├── policies/
│   ├── access.rego
│   └── compliance_test.rego
├── monitoring/
│   └── alert-rules.yaml
├── Dockerfile
├── docker-compose.yml
├── generate_readme.sh
├── README.md
└── .gitignore

### Demonstrating the Principles

### 1. Compliance-as-Code
- **Audit Logging**: Every call to `/api/loan-decision` generates an immutable JSON audit event (traceId, action, status, reasoning). Check logs with:
  ```bash
  docker-compose logs backend | grep audit
  ```
- **OPA Policies**: `policies/compliance_test.rego` checks that Kubernetes deployments use `readOnlyRootFilesystem` and `runAsNonRoot`.  
- **CI Enforcement**: Trivy scans for vulnerabilities; OPA checks block non‑compliant deployments.

### 2. Traceable Reasoning
- **Loan Decision API**: `/api/loan-decision` returns an `approved` boolean plus a `reasoning` list that traces every applied policy rule.  
- **Audit Event**: The reasoning chain is also logged in the audit stream for full traceability.  

Try it from the frontend form or using `curl`:
```bash
curl -X POST http://localhost:8000/api/loan-decision \
  -H "Content-Type: application/json" \
  -d '{"income":3000,"debt":2500,"employment_years":1}'
```

### 3. Governed Memory
- **PII Filtering**: The `/api/remember` endpoint accepts a user context but strips any field like `email`, `phone`, `name`.  
- **Pseudonymisation**: Users are identified by a token derived from their original ID, never stored directly.  
- **Right to Erasure**: `/api/forget/{token}` permanently deletes the stored context.  

Test via the UI (Memory section) or with `curl`:
```bash
# Store context (email will be removed)
curl -X POST http://localhost:8000/api/remember \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","context":{"preference":"dark","email":"user@example.com"}}'

# Recall context (no email)
curl http://localhost:8000/api/recall/<token>

# Forget the user
curl -X DELETE http://localhost:8000/api/forget/<token>
```

## Deploying to Kubernetes (optional)

1. Start a local cluster (Kind/Minikube) or use an AKS cluster created by Terraform.
2. Apply the manifests:
   ```bash
   kubectl apply -f k8s/
   ```
3. Install the monitoring stack:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
     --namespace monitoring --create-namespace
   kubectl apply -f monitoring/alert-rules.yaml -n monitoring
   ```
4. Access Grafana and inspect the pre‑configured alerts for high error rates and unauthorised access attempts.

## Next Steps

- Push the repo to GitHub and watch the CI/CD pipelines run.
- Customise the Terraform variables to deploy to your own cloud account.
- Add a production database (e.g., PostgreSQL) and replace the in‑memory stores.
- Integrate a vector database for more advanced Governed Memory (e.g., Pinecone, pgvector).

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
