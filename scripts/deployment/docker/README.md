# 🐳 Docker Deployment Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **🚀 [Deployment](../README.md)**

---

## 📋 Overview

This directory contains scripts for containerizing and deploying the Cloud Scale Analytics (CSA) in-a-Box documentation using Docker. These scripts enable portable, scalable deployment of the documentation site across different environments and container orchestration platforms.

## 🎯 Purpose

The Docker deployment scripts are designed to:

- **Containerize documentation site** for portable deployment
- **Build optimized container images** for production use
- **Deploy containers** to various container platforms
- **Configure load balancing and scaling** for high-availability deployment
- **Integrate with container registries** for image management

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Dependencies |
|--------|---------|----------|--------------|
| `build-container.sh` | Build documentation container image | **HIGH** | Docker, MkDocs |
| `deploy-container.sh` | Deploy container to runtime environment | **HIGH** | Docker, Container runtime |
| `push-to-registry.sh` | Push images to container registry | **MEDIUM** | Docker, Registry access |
| `run-local.sh` | Run documentation container locally | **MEDIUM** | Docker |
| `build-multi-arch.sh` | Build multi-architecture container images | **LOW** | Docker Buildx |
| `health-check.sh` | Container health check utilities | **LOW** | Docker, curl |

## 🚀 Planned Script Details

### `build-container.sh` (Priority: HIGH)

**Purpose:** Build optimized Docker container image for documentation

**Features:**
- Multi-stage Docker build for minimal image size
- Build documentation using MkDocs
- Serve documentation using nginx
- Include health check endpoints
- Support for build-time configuration

**Planned Usage:**
```bash
./build-container.sh [--tag tag] [--registry registry] [--build-arg key=value]

# Examples
./build-container.sh --tag csa-docs:latest
./build-container.sh --tag myregistry.azurecr.io/csa-docs:v1.0.0
./build-container.sh --build-arg ENVIRONMENT=production
```

**Dockerfile Structure:**
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdocs build --clean --strict

# Production stage  
FROM nginx:alpine
COPY --from=builder /app/site /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

### `deploy-container.sh` (Priority: HIGH)

**Purpose:** Deploy containerized documentation to various platforms

**Features:**
- Deploy to Docker Compose environments
- Deploy to Docker Swarm clusters
- Configure environment variables and secrets
- Set up load balancing and scaling
- Monitor deployment status

**Planned Usage:**
```bash
./deploy-container.sh [--platform platform] [--replicas count] [--port port]

# Examples
./deploy-container.sh --platform docker-compose
./deploy-container.sh --platform swarm --replicas 3
./deploy-container.sh --port 8080 --env production
```

### `push-to-registry.sh` (Priority: MEDIUM)

**Purpose:** Push container images to container registries

**Features:**
- Support for multiple registry providers (Docker Hub, ACR, ECR)
- Multi-architecture image pushing
- Image tagging strategies (latest, semantic versioning)
- Registry authentication handling
- Build and push in single operation

**Planned Usage:**
```bash
./push-to-registry.sh --registry registry.url --image image:tag

# Examples
./push-to-registry.sh --registry docker.io --image csa-docs:latest
./push-to-registry.sh --registry myregistry.azurecr.io --image csa-docs:v1.0.0
```

### `run-local.sh` (Priority: MEDIUM)

**Purpose:** Run documentation container locally for development and testing

**Features:**
- Mount local directories for development
- Configure port mapping
- Set up environment variables
- Enable live reload for development
- Provide easy access to logs

**Planned Usage:**
```bash
./run-local.sh [--port port] [--dev] [--mount-source]

# Examples  
./run-local.sh --port 3000
./run-local.sh --dev --mount-source  # Development mode with live reload
```

## 🐳 Container Specifications

### Base Image Strategy

**Production Image:**
- **Base:** `nginx:alpine` (< 50MB)
- **Purpose:** Serve static documentation files
- **Features:** Optimized nginx configuration, security headers
- **Size Goal:** < 100MB total

**Development Image:**
- **Base:** `python:3.11-slim`
- **Purpose:** Live development with MkDocs serve
- **Features:** Hot reload, development tools
- **Size:** ~200MB (development tools included)

### Multi-Architecture Support

Support for multiple architectures:
- **linux/amd64** - x86_64 servers and development machines
- **linux/arm64** - ARM-based servers and Apple Silicon
- **linux/arm/v7** - Raspberry Pi and ARM devices

### Container Configuration

**Environment Variables:**
```bash
# Server configuration
NGINX_PORT=80
NGINX_WORKER_PROCESSES=auto
NGINX_WORKER_CONNECTIONS=1024

# Documentation configuration  
DOCS_TITLE="CSA Documentation"
DOCS_BASE_URL="https://docs.contoso.com"
DOCS_VERSION="1.0.0"

# Security configuration
SECURITY_HEADERS=true
CSP_POLICY="default-src 'self'"
HTTPS_REDIRECT=false

# Monitoring configuration
ENABLE_METRICS=true
METRICS_PORT=9090
HEALTH_CHECK_PATH="/health"
```

**Port Mapping:**
- **80:** Main documentation site
- **443:** HTTPS (when SSL configured)
- **9090:** Prometheus metrics (optional)
- **8080:** Alternative HTTP port

## 🔧 Container Orchestration

### Docker Compose

**Basic Deployment:**
```yaml
version: '3.8'
services:
  csa-docs:
    image: csa-docs:latest
    ports:
      - "80:80"
    environment:
      - DOCS_BASE_URL=http://localhost
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
```

**Production Deployment with Load Balancer:**
```yaml
version: '3.8'
services:
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-proxy.conf:/etc/nginx/nginx.conf
    depends_on:
      - csa-docs-1
      - csa-docs-2

  csa-docs-1:
    image: csa-docs:latest
    environment:
      - INSTANCE_ID=1
    
  csa-docs-2:
    image: csa-docs:latest
    environment:
      - INSTANCE_ID=2
```

### Docker Swarm

**Swarm Service Definition:**
```bash
docker service create \
  --name csa-docs \
  --replicas 3 \
  --port published=80,target=80 \
  --env DOCS_BASE_URL=https://docs.contoso.com \
  --health-cmd "curl -f http://localhost/" \
  --health-interval 30s \
  csa-docs:latest
```

## 📊 Monitoring and Logging

### Container Health Checks

Built-in health checks monitor:
- **HTTP endpoint availability** - Main documentation site responsiveness
- **Disk space** - Available storage for logs and cache
- **Memory usage** - Container memory consumption
- **Process status** - Nginx/serving process health

### Logging Configuration

**Log Output:**
```bash
# Structured JSON logging
{
  "timestamp": "2025-01-28T10:30:00Z",
  "level": "INFO", 
  "service": "csa-docs",
  "message": "Request processed",
  "method": "GET",
  "path": "/architecture/overview/",
  "status": 200,
  "duration": "45ms",
  "user_agent": "Mozilla/5.0..."
}
```

**Log Destinations:**
- **stdout/stderr** - Docker logs (default)
- **File logs** - Persistent logging (optional)
- **Syslog** - Centralized logging (production)
- **Azure Monitor** - Cloud logging integration

### Metrics Collection

**Prometheus Metrics:**
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration
- `nginx_connections_active` - Active connections
- `container_memory_usage_bytes` - Memory usage

## 🔒 Security Considerations

### Container Security

**Security Features:**
- **Non-root user** - Run nginx as non-root user
- **Read-only filesystem** - Immutable container filesystem
- **Security headers** - CSP, HSTS, X-Frame-Options
- **Minimal attack surface** - Alpine Linux base image
- **No shell access** - Remove shell and unnecessary tools

**Security Scanning:**
```bash
# Container vulnerability scanning (planned)
./security-scan.sh --image csa-docs:latest

# Docker Bench security checks (planned)  
./docker-bench-security.sh
```

### Network Security

**Network Configuration:**
- **Internal networks** - Isolate containers from external access
- **TLS termination** - HTTPS/SSL support
- **Rate limiting** - Protect against DDoS
- **IP whitelisting** - Restrict access by IP ranges

## 🔍 Troubleshooting

### Common Container Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **Container won't start** | Invalid configuration | Check logs with `docker logs container-id` |
| **Port already in use** | Port conflict | Use different port mapping |
| **Build fails** | Missing dependencies | Check Dockerfile and base image |
| **Health check fails** | Service not responding | Check nginx configuration and logs |
| **High memory usage** | Memory leak or large content | Monitor metrics and optimize content |

### Debugging Commands

```bash
# View container logs
docker logs csa-docs --follow

# Execute shell in running container
docker exec -it csa-docs /bin/sh

# Inspect container configuration
docker inspect csa-docs

# View container resource usage
docker stats csa-docs

# Test container health check
docker exec csa-docs curl -f http://localhost/
```

### Performance Optimization

**Container Performance:**
- **Multi-stage builds** - Minimize image size
- **Layer caching** - Optimize Docker layer caching
- **Resource limits** - Set appropriate CPU/memory limits
- **Nginx tuning** - Optimize nginx configuration for static content
- **Compression** - Enable gzip compression for text content

## 💰 Cost Considerations

### Container Hosting Costs

**Azure Container Instances (ACI):**
- **Small (1 vCPU, 1GB RAM):** ~$15/month
- **Medium (2 vCPU, 4GB RAM):** ~$60/month

**Azure Container Apps:**
- **Consumption:** $0.000024/vCPU-second + $0.0000025/GB-second
- **Estimated:** $10-30/month for typical documentation site

**Docker Hub:**
- **Free tier:** 1 private repository
- **Pro:** $5/month for unlimited private repositories

### Cost Optimization

- **Use Alpine Linux** - Smaller images reduce storage costs
- **Multi-stage builds** - Minimize final image size
- **Resource limits** - Set appropriate CPU/memory limits
- **Auto-scaling** - Scale based on actual usage

## 📚 Related Documentation

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [nginx Configuration Guide](https://nginx.org/en/docs/)
- [Container Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Kubernetes Deployment Guide](../kubernetes/README.md)

## 🤝 Contributing

### Adding New Container Scripts

1. **Follow Docker best practices** - Use multi-stage builds, minimal base images
2. **Include security considerations** - Non-root users, read-only filesystems
3. **Support multiple architectures** - Use Docker Buildx for multi-arch builds
4. **Add comprehensive testing** - Test container startup, health checks, scaling
5. **Document resource requirements** - CPU, memory, storage needs
6. **Include monitoring** - Health checks, metrics, logging

### Script Requirements

- [ ] Uses multi-stage Dockerfile for optimization
- [ ] Supports configurable environment variables
- [ ] Includes health check implementation
- [ ] Has proper error handling and logging
- [ ] Supports both development and production modes
- [ ] Is tested with different container runtimes
- [ ] Documents resource requirements and costs
- [ ] Includes security scanning integration

## 📞 Support

For Docker deployment issues:

- **GitHub Issues:** [Create Docker Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=docker,deployment)
- **Docker Documentation:** Check official Docker documentation
- **Container Logs:** Use `docker logs` for troubleshooting
- **Community:** Docker Community Forums and Stack Overflow
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team