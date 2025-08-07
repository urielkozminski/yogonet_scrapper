#!/bin/bash

# Parámetros
PROJECT_ID="yogonet-468217"
REGION="us-central1"
REPO_NAME="yogonet-artifacts"
IMAGE_NAME="yogonet-scraper"
JOB_NAME="yogonet-job"

# Asegurarse que el usuario esté logueado
gcloud auth configure-docker $REGION-docker.pkg.dev
gcloud config set project $PROJECT_ID

# Build de la imagen
echo "🔨 Building Docker image..."
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME .

# Push al Artifact Registry
echo "📦 Subiendo la imagen al Artifact Registry..."
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME

# Crear o actualizar el Cloud Run Job
echo "🚀 Desplegando job a Cloud Run..."
gcloud run jobs describe $JOB_NAME --region $REGION > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "🔁 Job ya existe. Actualizando..."
  gcloud run jobs update $JOB_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME \
    --region $REGION \
    --set-env-vars "GCP_PROJECT_ID=$PROJECT_ID,BIGQUERY_DATASET=yogonet_scraper,BIGQUERY_TABLE=yogonet_scraper_results"
else
  echo "🆕 Creando nuevo job..."
  gcloud run jobs create $JOB_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME \
    --region $REGION \
    --set-env-vars "GCP_PROJECT_ID=$PROJECT_ID,BIGQUERY_DATASET=yogonet_scraper,BIGQUERY_TABLE=yogonet_scraper_results"
fi

# Ejecutar el job
echo "▶️ Ejecutando el job..."
gcloud run jobs execute $JOB_NAME --region $REGION