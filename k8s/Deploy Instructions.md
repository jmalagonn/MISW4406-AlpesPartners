# 🚀 Instrucciones de Despliegue - AlpesPartners en GCP GKE

## 📋 Prerrequisitos

### 1. Herramientas necesarias
```bash
# Instalar Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Instalar kubectl
# https://kubernetes.io/docs/tasks/tools/

# Instalar Docker
# https://docs.docker.com/get-docker/

# Verificar instalaciones
gcloud version
kubectl version --client
docker --version
```

### 2. Configuración inicial de GCP
```bash
# Autenticarse en GCP
gcloud auth login

# Configurar proyecto
export PROJECT_ID="desarrolloswcloud"
gcloud config set project $PROJECT_ID

# Habilitar APIs necesarias
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable compute.googleapis.com
```

---

## 🏗️ Paso 1: Crear Cluster de GKE

### 1.1 Crear cluster con configuración optimizada
```cmd
# ⏱️ TIEMPO ESTIMADO: 5-8 minutos
gcloud container clusters create alpes-experiment --zone=us-central1-a --machine-type=e2-standard-2 --num-nodes=2 --enable-autoscaling --min-nodes=1 --max-nodes=5 --disk-size=20GB --disk-type=pd-standard --enable-network-policy --enable-autorepair --enable-autoupgrade

# Verificar que el cluster esté listo
gcloud container clusters list
```

### 1.2 Configurar kubectl
```cmd
gcloud container clusters get-credentials alpes-experiment --zone=us-central1-a
kubectl get nodes
```

---

## 🐳 Paso 2: Construir y Subir Imágenes Docker

### 2.1 Configurar Docker para GCR
```bash
# Configurar Docker para usar gcloud como helper
gcloud auth configure-docker
```

### 2.2 Construir y subir imágenes
```cmd


# Construir y subir BFF (2-3 min)
docker build -t gcr.io/desarrolloswcloud/bff ./client/bff && docker push gcr.io/desarrolloswcloud/bff

# Construir y subir Tracking (2-3 min)
docker build -t gcr.io/desarrolloswcloud/tracking ./tracking && docker push gcr.io/desarrolloswcloud/tracking

# Construir y subir Affiliates (2-3 min)
docker build -t gcr.io/desarrolloswcloud/affiliates ./affiliates && docker push gcr.io/desarrolloswcloud/affiliates

# Construir y subir Alliances (2-3 min)
docker build -t gcr.io/desarrolloswcloud/alliances ./alliances && docker push gcr.io/desarrolloswcloud/alliances

# Verificar que las imágenes se subieron correctamente
gcloud container images list
```

---

## ☸️ Paso 3: Desplegar en Kubernetes

### 3.1 Aplicar configuración con Kustomize
```cmd
cd k8s
kubectl apply -k .

# Verificar que los pods se estén creando (algunos tardarán más)
kubectl get pods -n alpes-experiment

# Verificar servicios
kubectl get services -n alpes-experiment

# Monitorear el progreso
kubectl get pods -n alpes-experiment -w
```

### 3.2 Verificar despliegue
```cmd

# Verificar estado de pods (esperar hasta que todos estén "Running")
kubectl get pods -n alpes-experiment

# Verificar logs de servicios específicos si hay problemas
kubectl logs deployment/bff -n alpes-experiment
kubectl logs deployment/tracking -n alpes-experiment -c tracking-api
kubectl logs deployment/tracking -n alpes-experiment -c tracking-worker

```

---

## 🌐 Paso 4: Configurar Acceso Externo

### 4.1 Obtener IP externa del LoadBalancer
```cmd

# Verificar servicios
kubectl get services -n alpes-experiment

# Verificar ingress (la IP aparecerá en el campo ADDRESS)
kubectl get ingress -n alpes-experiment

# Si no aparece IP, verificar eventos del ingress
kubectl describe ingress bff-ingress -n alpes-experiment

```
---

## Paso 5: Verificación y Testing

### 5.1 Health Checks
```cmd
# Obtener IP externa (puede tomar 2-5 minutos)
set EXTERNAL_IP=%kubectl get ingress -n alpes-experiment -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"%

# Verificar que la IP esté asignada
kubectl get ingress -n alpes-experiment

# Health checks - IMPORTANTE: Usar prefijo /api/v1/
curl http://%EXTERNAL_IP%/
curl http://%EXTERNAL_IP%/health
curl http://%EXTERNAL_IP%/api/v1/tracking/health
curl http://%EXTERNAL_IP%/api/v1/affiliates/health
curl http://%EXTERNAL_IP%/api/v1/alliances/health
```

### 5.2 Testing de funcionalidad
```cmd
# Test BFF (debe retornar: {"status":"ok","message":"BFF Service is running"})
curl http://%EXTERNAL_IP%/

# Test Tracking Health (debe retornar: {"status":"Tracking health serivce ok"})
curl http://%EXTERNAL_IP%/api/v1/tracking/health

# Test Tracking Stats (debe retornar: {"items":[]})
curl http://%EXTERNAL_IP%/api/v1/tracking/stats/daily

# Test Tracking Interactions (debe retornar: {"items":[]})
curl http://%EXTERNAL_IP%/api/v1/tracking/interactions

# Test Alliances (debe retornar lista de marcas)
curl http://%EXTERNAL_IP%/api/v1/alliances/brands
```

---

### Monitoreo
```cmd
kubectl get all -n alpes-experiment
kubectl logs -f deployment/SERVICE_NAME -n alpes-experiment
kubectl describe pod POD_NAME -n alpes-experiment
kubectl get events -n alpes-experiment --sort-by='.lastTimestamp'
```

### Escalado
```cmd
kubectl scale deployment tracking --replicas=3 -n alpes-experiment
kubectl autoscale deployment tracking --cpu-percent=70 --min=2 --max=10 -n alpes-experiment
```

---

### Limpieza de recursos
```cmd
gcloud container clusters delete alpes-experiment --zone=us-central1-a
gcloud container images delete gcr.io/desarrolloswcloud/bff --force-delete-tags
gcloud container images delete gcr.io/desarrolloswcloud/tracking --force-delete-tags
gcloud container images delete gcr.io/desarrolloswcloud/affiliates --force-delete-tags
gcloud container images delete gcr.io/desarrolloswcloud/alliances --force-delete-tags
```
