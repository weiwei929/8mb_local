# Docker Compose Files Overview

This project includes multiple Docker Compose configurations for different deployment scenarios.

## File Naming Convention

- **`.single.yml`** - Single container deployment (pull from Docker Hub)
- **`.multi.yml`** - Multi-container deployment (pull from Docker Hub)
- **`.single-build.yml`** - Single container (build locally)
- **`.multi-build.yml`** - Multi-container (build locally)

## Files

### Production (Docker Hub Images)

#### `docker-compose.single.yml` ⭐ **RECOMMENDED**
- **What**: ONE container with everything (Redis + Backend + Worker + Frontend)
- **Use when**: You want the simplest deployment
- **Containers**: 1 (8mblocal-app)
- **Ports**: 8000 only
- **Access**: http://localhost:8000

```bash
docker compose -f docker-compose.single.yml up -d
```

#### `docker-compose.multi.yml`
- **What**: Original 3-container setup
- **Use when**: You need separate services or debugging
- **Containers**: 4 (redis, backend, worker, frontend)
- **Ports**: 5173 (frontend), 8000 (backend), 6379 (redis)
- **Access**: Frontend at http://localhost:5173

```bash
docker compose -f docker-compose.multi.yml up -d
```

### Development (Local Builds)

#### `docker-compose.single-build.yml`
- Builds the unified single container from Dockerfile
- Takes ~20-30 minutes (FFmpeg compilation)

```bash
docker compose -f docker-compose.single-build.yml build
docker compose -f docker-compose.single-build.yml up -d
```

#### `docker-compose.multi-build.yml`
- Builds all 3 containers separately from their individual Dockerfiles
- Faster parallel builds

```bash
docker compose -f docker-compose.multi-build.yml up --build -d
```

## Quick Reference

| File | Containers | Build Time | Best For |
|------|-----------|------------|----------|
| `docker-compose.single.yml` | 1 | None (pulls image) | **Production, simplest** |
| `docker-compose.multi.yml` | 4 | None (pulls images) | Debugging, separate services |
| `docker-compose.single-build.yml` | 1 | ~25 mins | Local single-container dev |
| `docker-compose.multi-build.yml` | 4 | ~15 mins | Local multi-container dev |

## GPU Support

All configurations support GPU acceleration with `--gpus all` or the deploy.resources syntax. The system auto-detects NVIDIA/Intel/AMD GPUs or falls back to CPU.

## Environment Variables

All configurations respect `.env` file. Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key variables:
- `AUTH_ENABLED` - Enable/disable basic auth
- `AUTH_USER` / `AUTH_PASS` - Credentials if auth enabled
- `FILE_RETENTION_HOURS` - How long to keep uploaded/output files
