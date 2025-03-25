# celery-cloud

Implementation of celery services using public cloud services.

- AWS: Lambda, SQS, SNS, DynamoDB.

## Launch test Project

Launch server

```powershell
$env:AWS_PROFILE="pak"; uv run celery-worker
```

Test client

```powershell
$env:AWS_PROFILE="pak"; uv run celery-worker
```

## Development notes

### Start project (uv)

```bash
uv init --no-readme
```

### Configure project as package

```ini
[project.scripts]
# Execute function "main" from package and main.py file
celery-cloud = "celery_cloud.main:main"
# Execute function "hello" from __init__.py
celery-cloud-hello = "celery_cloud:hello"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Version management

#### Set a specific version

```bash
VERSION="0.5.0"
uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $VERSION
```

#### Retrieve version

```bash
uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version
```

Works in a Dockerfile, makefile, etc.

#### Bump project version

If you need to bump the version by using specifiers like patch, minor, or major:

```bash
v=$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)

# bump patch version
part="patch"
uvx --from bump2version bumpversion --allow-dirty --current-version "$v" "$part" pyproject.toml
```

### Launch project

```bash
uv run celery-cloud
```

### Get python local path

```bash
uv run python -c "import sys; print(sys.executable)"
```

## Step 1: Celery local worker

TODO

## Test: debug local lambda

Fastapi will be used as an interface to lambda. debugpy will be used to connect to VSCode.

Add dependencies using uv.

```bash
uv add --group dev fastapi uvicorn debugpy ruff
```

Create launch.json to connect to the debugger

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to FastAPI (uv)",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5890
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "${workspaceFolder}"
        }
      ]
    }
  ]
}
```

Launch uvicorn with the fastapi project

```bash
uv run uvicorn celery_cloud.debug_server:app
```

From VSCode launch debugger "Attach to FastAPI (uv)".

Test the application.

```bash
curl -X POST "http://127.0.0.1:8000/lambda" -H "Content-Type: application/json" -d @sqs_event.json
```

```powershell
$body = Get-Content -Raw -Path "sqs_event.json"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/lambda" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body

# If UTF-8 required on server
$body = Get-Content -Raw -Path "sqs_event.json" | Out-String
Invoke-RestMethod -Uri "http://127.0.0.1:8000/lambda" -Method Post -Headers @{"Content-Type"="application/json"} -Body ([System.Text.Encoding]::UTF8.GetBytes($body))

```
