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

## Escenario de Disponibilidad — Tracking (Mariana)

Para este escenario buscabamos asegurar disponibilidad del servicio de Tracking al tener una situación de alto tráfico por parte de los usuarios (más de 10,000 interacciones) donde el servicio pudiese manejarlo correctamente y procesarlo acorde a ello.

Para ello, se implementó un nginx que nos permitiera balancear las peticiones HTTP entre tres diferentes instancias del servicio de tracking para manejar la carga apropiadamente. Para hacer una simulación de la carga se puede levantar el proyecto como se menciona al inicio de este README y posteriormente hacer una prueba de 10,000 peticiones con el siguiente comando de manera local.

```bash
# Peticiones al servicio de tracking
for i in {1..10000}; do
  RESPONSE=$(curl -s -X POST http://localhost:8040/tracking/interactions \
    -H "Content-Type: application/json" \
    -d '{"interaction_type":"click","target_element_id":"123","target_element_type":"button","campaign_id":"123"}')
  echo "Request $i: $RESPONSE"
done
```
Para verificar que se ha recibido correctamente las 10000 peticiones en el nginx se puede verificar la cantidad de peticiones que se reciben al ejecutar este comando

```bash
docker logs misw4406-alpespartners-tracking_nginx-1 2>&1 | grep '/tracking/interactions' | wc -l
```

Así mismo, los workers se configuraron para ser resilientes en caso de fallo con la siguiente configuración

```bash
consumer_type=pulsar.ConsumerType.KeyShared
```

Y tambien se implementó graceful shutdown, donde si un contenedor necesita reiniciarse o escalarse, recibe la señal SIGTERM o SIGINT, deja de recibir nuevos mensajes, procesa los mensajes actuales, cierra la conexión con Pulsar y termina de forma segura. Esto evita la pérdida de eventos y permite reinicios seguros sin interrumpir el flujo de trabajo.