#!/bin/bash

# ========= CONFIGURACIÓN =========
NAMESPACE="press-any-key"
REPO_NAME="celery-cloud-runner"
DISPLAY_NAME="Press Any Key namespace"
AWS_PROFILE="pak"
REGION="us-east-1"
# =================================

# 1. Obtener ID de cuenta
ACCOUNT_ID=$(aws sts get-caller-identity --profile "$AWS_PROFILE" --query Account --output text)

# 2. Verificar si ya hay un namespace creado
echo "⏳ Verificando namespace..."
EXISTING_NAMESPACE=$(aws ecr-public describe-registries \
  --region "$REGION" \
  --profile "$AWS_PROFILE" \
  --query 'registries[0].registryName' \
  --output text 2>/dev/null)

if [ "$EXISTING_NAMESPACE" == "None" ] || [ -z "$EXISTING_NAMESPACE" ]; then
  echo "🚀 Creando namespace público: $DISPLAY_NAME"
  aws ecr-public put-registry-catalog-data \
    --region "$REGION" \
    --profile "$AWS_PROFILE" \
    --catalog-data "{\"displayName\": \"$DISPLAY_NAME\"}"
else
  echo "✅ Namespace ya existe: $EXISTING_NAMESPACE"
fi

# 3. Crear el repositorio
echo "📦 Creando repositorio público: $REPO_NAME"
aws ecr-public create-repository \
  --repository-name "$REPO_NAME" \
  --region "$REGION" \
  --profile "$AWS_PROFILE"

# 4. Mostrar URI del repositorio
REPO_URI=$(aws ecr-public describe-repositories \
  --repository-names "$REPO_NAME" \
  --region "$REGION" \
  --profile "$AWS_PROFILE" \
  --query 'repositories[0].repositoryUri' \
  --output text)

echo "🎯 Repositorio creado con éxito:"
echo "    URI: $REPO_URI"

# 5. Instrucciones opcionales
echo ""
echo "📤 Para subir una imagen:"
echo "    docker tag <tu-imagen> $REPO_URI:latest"
echo "    docker push $REPO_URI:latest"
