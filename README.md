# AlpesParners

## Servicios
Servicio de afiliados:
-  carpeta raíz: affiliates

## Requerimientos:
- Docker

## Ejecución local
En una terminal situada en la raíz del proyecto, ejecuta el siguiente comando:

```bash
docker-compose up --build
```


## Escenario de rendimiento — Tracking

## Escenario de rendimiento — Tracking (Manuel Sánchez)

**Flujo:** Pulsar (comandos) - Worker de tracking - DB propia - API `/tracking/stats/daily`.

### Variables (.env junto a `docker-compose.yml`)
```env
PULSAR_URL=pulsar://pulsar:6650
DATABASE_URL=postgresql+psycopg2://app:app@tracking_db:5432/app
TOPIC_COMMANDS_TRACKING=commands.tracking
SUBSCRIPTION_NAME=tracking-svc
```

### Smoke test (opcional en local)
```bash
# levantar mínimos
docker compose up -d tracking_db pulsar tracking tracking_worker

# (una sola vez) retención
docker compose exec pulsar bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1

# health
curl -s http://localhost:8010/tracking/health

# publicar 2 mensajes de prueba
docker compose exec pulsar bin/pulsar-client produce -m '{"demo":true}' -n 2 -k test commands.tracking

# vista materializada (esperado: count=2)
curl -s http://localhost:8010/tracking/stats/daily
```

### Prueba de capacidad (GCP)
```bash
# paralelismo del tópico + escalar consumidores
docker compose exec pulsar bin/pulsar-admin topics create-partitioned-topic commands.tracking --partitions X
docker compose up -d --scale tracking_worker=6

# 60s @ 1500 msg/s ≈ 90k/min (>80k objetivo 80k)
docker compose exec pulsar bin/pulsar-perf produce -r 1500 -time 60 -m 256 commands.tracking
```