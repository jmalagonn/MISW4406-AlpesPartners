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

## Escenario de rendimiento — Tracking (Manuel Sánchez)
<img width="1737" height="1058" alt="image" src="https://github.com/user-attachments/assets/3239ae13-09c6-4811-8f57-45c6657cf1f6" />

**Flujo:** Pulsar (comandos) - Worker de tracking - DB propia - API `/tracking/stats/daily`.

### Paso a paso para ejecutar el escenario de rendimiento en Tracking

1. **Levantar los servicios necesarios**  
   Asegúrate de tener Pulsar, la base de datos, el servicio de tracking y el worker de tracking corriendo:  
   ```bash
   docker compose up -d tracking_db pulsar tracking tracking_worker```

2. **Verificar la salud del servicio de tracking**
   Comprueba que el servicio responde correctamente:
     ```bash
     curl -s http://34.8.61.71/api/v1/tracking/health```

3. **Smoke test (opcional en local)**
Publica un par de mensajes de prueba y valida que la proyección se actualiza:

```bash
# publicar 2 mensajes de prueba
docker compose exec pulsar bin/pulsar-client produce -m '{"demo":true}' -n 2 -k test commands.tracking

# vista materializada (esperado: incremento de count en el día actual)
curl -s http://34.8.61.71/api/v1/tracking/stats/daily
```

3. **Prueba de capacidad (≥80k/min)**
Configura paralelismo y ejecuta carga sostenida:
```bash
# (una sola vez) retención infinita
docker compose exec pulsar bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1

# crear tópico particionado (si ya existe, ignorar)
docker compose exec pulsar bin/pulsar-admin topics create-partitioned-topic commands.tracking --partitions 8 || true

# escalar consumidores en paralelo
docker compose up -d --scale tracking_worker=6

# enviar 90k mensajes/min (~1500 msg/s por 60s)
docker compose exec pulsar bin/pulsar-perf produce \
  -r 1500 -time 60 \
  persistent://public/default/commands.tracking
```

4. **Validación final**
Consulta la proyección para confirmar que el contador refleja la carga procesada:
```bash
curl -s http://34.8.61.71/api/v1/tracking/stats/daily
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


## Escenario de Disponibilidad (Mariana Díaz)

<img width="1382" height="825" alt="image" src="https://github.com/user-attachments/assets/1dacd120-f6ca-48bd-824a-b48a6c222bd8" />

### Ejecución de una interacción para probar la HA

Revisar la siguiente sección donde se referencia detalladamente como realizar una interacción al servicio 

[Paso a Paso Ejecución](https://github.com/jmalagonn/MISW4406-AlpesPartners/wiki/Escenario-Escalabilidad#paso-a-paso-para-ejecutar-el-escenario-de-cqrs-en-tracking-creaci%C3%B3n-de-interacci%C3%B3n)

### Decisiones Arquitecturales

#### Kubernetes con Autoescalado Horizontal (HPA)

* Configurado con minReplicas: 2, maxReplicas: 10.
* Escalado basado en CPU > 70% y Memoria > 70%.
* Permite escalado automático y auto-healing, aunque introduce overhead de orquestación y se debe considerar el tiempo de warm-up de los pods.
* Riesgo: una configuración inadecuada puede causar escalado excesivo y desperdicio de recursos.


#### Health Checks y Graceful Shutdown
* Configurados con un periodo de gracia de 30 segundos.
* Ante SIGTERM o SIGINT, los contenedores:
     1. Dejan de recibir nuevos mensajes.
     2. Procesan los mensajes actuales.
     3. Cierran la conexión con Pulsar.
     4. Terminan de forma segura, evitando pérdida de eventos.
     5. Garantizan resiliencia y reinicios seguros, aunque un mal ajuste podría generar overhead o falsos positivos en la detección de fallos.


#### Workers resilientes con Pulsar KeyShared
* Configuración: consumer_type=pulsar.ConsumerType.KeyShared.
* Permite que múltiples workers procesen eventos en paralelo de forma balanceada, manteniendo entrega ordenada por clave.
* Asegura que no haya duplicación de eventos y que se mantenga continuidad durante fallos o escalados.
* Riesgo: una mala configuración puede derivar en pérdida o duplicación de mensajes.


### Justificación

Estas decisiones garantizan que el servicio de tracking pueda mantener una disponibilidad mayor a 99.99% en escenarios de alta demanda.

* El HPA permite absorber picos de tráfico con escalado automático.
* Los health checks y graceful shutdown aseguran resiliencia y reinicios sin interrupciones.
* La configuración de los workers con KeyShared mantiene continuidad en el consumo de eventos sin pérdidas durante fallos o escalados.

### Experimentación del Escenario

[Resultados de Prueba](https://github.com/jmalagonn/MISW4406-AlpesPartners/wiki/Experimento-Disponibilidad)


 ## Descripción de actividades realizada por cada miembro

 * Arquitectura general de servicios y BFF: Nicolas Malagon
 * Escenario de Escalabilidad: Sergio Perez
 * Escenario de Rendimiento: Manuel Sanchez
 * Escenario de Disponibilidad: Mariana Diaz
 * Despliegue: Trabajo en Conjunto

