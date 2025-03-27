#!/bin/bash

# Declare variables
PROFILE="pak"
DOMAIN="celery-cloud"
AWS_REGION="us-east-1"
REGISTRY_URI="public.ecr.aws/e2b2x4l7"
REPOSITORY_NAME="lambda-runner"
PLATFORM="linux/amd64"
# PLATFORM="linux/amd64,linux/arm64"
BUILDER_NAME="mybuilder"


while [[ "$#" -gt 0 ]]; do
    case $1 in
        --repository_name) REPOSITORY_NAME="$2"; shift ;;
        --base_version) BASE_VERSION="$2"; shift ;;
        --platform) PLATFORM="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "Bumping version ..."
v=$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)
# bump patch version
part="patch"
uvx --from bump2version bumpversion --allow-dirty --current-version "$v" "$part" pyproject.toml

BASE_VERSION=$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)
echo "✅ Bumped version to $BASE_VERSION"

# Verify if builder exists
if docker buildx ls | grep -q "^$BUILDER_NAME "; then
    echo "✅ Builder '$BUILDER_NAME' exists. Activating ..."
    docker buildx use "$BUILDER_NAME"
    echo "✅ Builder '$BUILDER_NAME' active."

else
    echo "⚠️  Builder '$BUILDER_NAME' not found. Creating..."
    docker buildx create --name "$BUILDER_NAME" --use
    echo "✅ Builder '$BUILDER_NAME' created and active."
fi


set -e

docker buildx inspect $BUILDER_NAME --bootstrap

echo "Authorizing in repo"
aws --profile $PROFILE ecr-public get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY_URI

echo "$REGISTRY_URI/$DOMAIN/$REPOSITORY_NAME:$BASE_VERSION"

echo "Installing QEMU for multi-architecture support"
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

echo "Building the image for multiple platforms"
docker buildx build --provenance=false --progress=plain --platform $PLATFORM -t $REGISTRY_URI/$DOMAIN/$REPOSITORY_NAME:$BASE_VERSION -f Dockerfile --push .

# docker buildx imagetools create -t $REGISTRY_URI/$REPOSITORY_NAME:$BASE_VERSION

echo "✅ Image building finished: $REGISTRY_URI/$DOMAIN/$REPOSITORY_NAME:$BASE_VERSION"
