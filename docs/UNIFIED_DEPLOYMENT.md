# Unified Container Deployment

## Overview

The 8mb.local project now supports two deployment modes:

1. **Multi-container** (original): Separate containers for backend API, worker, and frontend
2. **Unified container** (new): Single container running all services via supervisord

## Unified Container Architecture

The unified container includes:
- **FastAPI backend** (uvicorn on port 8000)
- **Celery worker** (video compression with NVENC)
- **Pre-built frontend** (served as static files by FastAPI)
- **Supervisord** (process manager)

All services run in a single container, simplifying deployment and reducing resource overhead.

## Deployment Options

### Option 1: Docker Hub (Recommended for Quick Start)

```bash
# Pull and run the unified image
docker compose -f docker-compose.hub-unified.yml up -d

# View logs
docker compose -f docker-compose.hub-unified.yml logs -f

# Stop
docker compose -f docker-compose.hub-unified.yml down
```

The unified image is published to Docker Hub as `jms1717/8mblocal:latest`.

### Option 2: Build Locally

```bash
# Build the unified container
docker compose -f docker-compose.unified.yml build

# Run
docker compose -f docker-compose.unified.yml up -d

# View logs
docker compose -f docker-compose.unified.yml logs -f

# Stop
docker compose -f docker-compose.unified.yml down
```

### Option 3: Original Multi-Container Setup

The original multi-container setup is still supported:

```bash
# From Docker Hub
docker compose -f docker-compose.hub.yml up -d

# Or build locally
docker compose up -d
```

## Files

- `Dockerfile` - Unified multi-stage build
- `supervisord.conf` - Process manager configuration
- `docker-compose.unified.yml` - Local build compose file
- `docker-compose.hub-unified.yml` - Pull from Docker Hub
- `docker-compose.yml` - Original multi-container local build
- `docker-compose.hub.yml` - Original multi-container from Hub

## Technical Details

### Unified Dockerfile Stages

1. **ffmpeg-build**: Compiles FFmpeg 7.0 with NVENC support on CUDA 12.1
2. **frontend-build**: Builds SvelteKit frontend with empty `PUBLIC_BACKEND_URL` (same-origin)
3. **runtime**: Combines Python backend, Celery worker, FFmpeg, and pre-built frontend

### Supervisord Configuration

The supervisord configuration runs two programs:
- `backend`: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- `worker`: `celery -A worker.celery_app worker --loglevel=info -n 8mblocal@%h --concurrency=1`

### Static File Serving

The FastAPI backend serves the pre-built frontend when the unified container detects `/app/frontend-build`:
- Static assets mounted at `/_app`
- SPA fallback routing for all non-API paths
- API routes remain at `/api/*`

## Benefits of Unified Container

✅ **Simpler deployment**: One image instead of three  
✅ **Lower resource usage**: Shared base image layers  
✅ **Faster startup**: No inter-container dependencies  
✅ **Easier networking**: No CORS issues (same-origin)  
✅ **Single port**: Only expose 8000 (plus Redis internally)

## GitHub Actions

The `.github/workflows/docker-publish-unified.yml` workflow builds and publishes the unified image to Docker Hub on push to main or version tags.

## Migration

To migrate from multi-container to unified:

1. Stop the old stack: `docker compose down`
2. Pull the new unified image: `docker compose -f docker-compose.hub-unified.yml pull`
3. Start the unified stack: `docker compose -f docker-compose.hub-unified.yml up -d`

Your uploads and outputs volumes are preserved.

## Troubleshooting

**Check process status:**
```bash
docker exec -it 8mblocal-app supervisorctl status
```

**View individual process logs:**
```bash
docker exec -it 8mblocal-app supervisorctl tail backend
docker exec -it 8mblocal-app supervisorctl tail worker
```

**Restart a process:**
```bash
docker exec -it 8mblocal-app supervisorctl restart backend
docker exec -it 8mblocal-app supervisorctl restart worker
```
