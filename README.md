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

## Escenario de Escalabilidad - Tracking (Sergio Perez)
<img  alt="image" src="https://github.com/user-attachments/assets/2459862c-2474-404a-9471-089c4471dfe1" />

**Flujo:** Pulsar (comandos) - Worker de tracking - CQRS - API `/tracking/interactions`.

### Paso a paso para ejecutar el escenario de CQRS en Tracking (Creación de Interacción)

1. **Levantar los servicios necesarios**  
   Asegúrase de tener los servicios de Pulsar, la base de datos, el servicio de tracking y el worker de tracking corriendo.  
   ```bash
   docker compose up -d tracking_db pulsar tracking tracking_worker
   ```

2. **Verificar la salud del servicio de tracking**  
   Compruebe que el servicio de tracking está disponible:  
   ```bash
   curl -s http://localhost:8010/tracking/health
   ```

3. **Publicar un comando para crear una interacción**  
   Envíe un mensaje al tópico de comandos de tracking simulando la creación de una interacción. Por ejemplo:  
   ```bash
   docker compose exec pulsar bin/pulsar-client produce -m '{"type":"create_interaction","user_id":123,"interaction":"like","timestamp":"2024-06-01T12:00:00Z"}' -k test commands.tracking
   ```

4. **Consultar la API de CQRS para verificar la interacción**  
   Una vez procesado el comando, consulte la API para ver si la interacción fue registrada correctamente:  
   ```bash
   curl -s http://localhost:8010/tracking/interactions
   ```

5. **(Opcional) Revisar los logs del worker de tracking**  
   Verificar el procesamiento revisando los logs:  
   ```bash
   docker compose logs -f tracking_worker
   ```

### Modelo de datos
En este escenario, implementamos un modelo basado en Event Sourcing en la capa de datos. Esto significa que, en lugar de almacenar únicamente el estado actual de las entidades, registramos cada cambio como un evento inmutable en un log de eventos. Por ejemplo, en el servicio de tracking, cada interacción del usuario (como "like", "view", etc.) se almacena como un evento individual. Posteriormente, estos eventos pueden ser consultados o proyectados para reconstruir el estado actual o generar vistas materializadas (como estadísticas diarias).

Este enfoque nos permite auditar fácilmente todas las acciones realizadas, facilita la escalabilidad y la integración con otros sistemas mediante la publicación de eventos.

## Tipos de Eventos Utilizados

### Eventos de Carga de Estado

El servicio de tracking utiliza **eventos de carga de estado** (`InteractionTracked`), justificado por:

- **Simplicidad del dominio**: Las interacciones son eventos atómicos sin transiciones complejas
- **Auditoría completa**: Trazabilidad de todas las interacciones
- **Performance**: Optimizado para alta frecuencia de escritura
- **Autocontenido**: Cada evento contiene toda la información necesaria

#### Evolución del Esquema
- **Backward Compatibility**: Nuevos campos como opcionales
- **Versionado**: Sistema de versiones para evolución controlada
- **Migración Gradual**: Compatibilidad con versiones anteriores

### Beneficios de la Implementación
1. **Simplicidad**: Eventos autocontenidos y fáciles de entender
2. **Auditabilidad**: Trazabilidad completa de interacciones
3. **Escalabilidad**: Proyecciones optimizadas para consultas
4. **Mantenibilidad**: Esquemas claros y bien definidos
5. **Flexibilidad**: Fácil evolución del esquema


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


 ## Descripción de actividades realizada por cada miembro

 * Arquitectura general de servicios y BFF: Nicolas Malagon
 * Escenario de Escalabilidad: Sergio Perez
 * Escenario de Rendimiento: Manuel Sanchez
 * Escenario de Disponibilidad: Mariana Diaz
 * Despliegue: Trabajo en Conjunto

