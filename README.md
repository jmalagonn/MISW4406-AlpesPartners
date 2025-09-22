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

## Escenario de Rendimiento — Tracking (Manuel Sánchez)

<img width="1737" height="1058" alt="image" src="https://github.com/user-attachments/assets/3239ae13-09c6-4811-8f57-45c6657cf1f6" />

### Ejecución de una interacción para probar el rendimiento

Revisar la siguiente sección donde se referencia detalladamente cómo ejecutar el escenario de rendimiento en Tracking:

[Paso a Paso Ejecución](https://github.com/jmalagonn/MISW4406-AlpesPartners/wiki/Escenario-Rendimiento#paso-a-paso-para-ejecutar-el-escenario-de-rendimiento-en-tracking)

### Decisiones Arquitecturales

#### Kubernetes con Autoescalado Horizontal (HPA)
* Configurado con minReplicas: 2, maxReplicas: 10.  
* Escalado basado en CPU > 70% y Memoria > 70%.  
* Políticas configuradas: escalado agresivo (200% cada 15s) y reducción moderada (50% cada 30s).  
* Riesgo: la latencia en la reacción del escalado puede generar pérdida temporal de capacidad.

#### Recursos por Pod
* Requests: CPU 250m, Memoria 256Mi.  
* Limits: CPU 500m, Memoria 512Mi.  
* Garantizan un mínimo de rendimiento por instancia, pero también limitan la capacidad máxima antes de escalar.

#### Workers resilientes con Pulsar KeyShared
* Configuración: consumer_type=pulsar.ConsumerType.KeyShared.  
* Permite que múltiples workers procesen eventos en paralelo balanceando carga por clave.  
* Asegura orden en el consumo de mensajes y evita duplicados, aunque requiere un ajuste cuidadoso de particiones y concurrencia.

### Justificación

Estas decisiones buscan garantizar que el servicio de tracking pueda procesar entre **400 y 800 transacciones por minuto**, manteniendo resiliencia ante picos de carga.

* El HPA permite absorber picos de tráfico con escalado automático.  
* La asignación de recursos asegura un balance entre costo y rendimiento por pod.  
* La configuración de Pulsar distribuye la carga de forma equitativa, evitando pérdida de mensajes bajo alta demanda.  

### Experimentación del Escenario

[Resultados de Prueba](https://github.com/jmalagonn/MISW4406-AlpesPartners/wiki/Experimento-Rendimiento)

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

