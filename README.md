Money‑Transfer Starter

A production‑ready skeleton implementing:

FastAPI API Gateway (REST + GraphQL), load‑balancing, JWT auth, Casbin RBAC, rate‑limit, circuit‑break, Prometheus metrics.

Two gRPC micro‑services (userprofile_service, banktransaction_service) with PostgreSQL, Redis cache, Kafka event bus, Prom‑ready metrics, automatic Alembic migration.

Shared libs in common/ (DB, cache, events, observability).

Dev & CI – Docker Compose stack, GitHub Actions, quick‑start bash script, multi‑arch image builds.

./quick-start.sh  #  installs, builds, starts stack

Swagger → https://localhost/docs
GraphiQL → https://localhost/graphql
Grafana → http://localhost:3000


| Service             | gRPC Port | Metrics Port      | Exposed Ports (Compose)      | Notes                |
|---------------------|-----------|-------------------|------------------------------|----------------------|
| user_service        | 50051     | 9100              | 50051:50051, 9100:9100       | OK                   |
| transaction_service | 50052     | 9101 (→ 9100)     | 50052:50052, 9101:9100       | Slight inconsistency |
| gateway             | 8000      | –                 | 8000:8000                    | OK                   |
| keycloak            | 8080      | –                 | 8080:8080                    | OK                   |
| prometheus          | 9090      | –                 | 9090:9090                    | OK                   |
| grafana             | 3000      | –                 | 3000:3000                    | OK                   |

