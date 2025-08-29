# ☸️ Kubernetes Deployment Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **🚀 [Deployment](../README.md)**

---

## 📋 Overview

This directory contains scripts and manifests for deploying the Cloud Scale Analytics (CSA) in-a-Box documentation to Kubernetes clusters. These scripts enable enterprise-grade deployment with high availability, auto-scaling, and robust monitoring capabilities.

## 🎯 Purpose

The Kubernetes deployment scripts are designed to:

- **Deploy documentation to Kubernetes clusters** for enterprise environments
- **Configure auto-scaling and load balancing** for high availability
- **Set up ingress controllers and SSL termination** for secure access
- **Implement monitoring and observability** with Prometheus and Grafana
- **Manage multi-environment deployments** (dev, staging, production)

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts and manifests listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Dependencies |
|--------|---------|----------|--------------|
| `deploy-k8s.sh` | Deploy documentation to Kubernetes cluster | **MEDIUM** | kubectl, Kubernetes cluster |
| `setup-ingress.sh` | Configure ingress controller and SSL | **MEDIUM** | kubectl, cert-manager |
| `setup-monitoring.sh` | Deploy Prometheus and Grafana monitoring | **LOW** | kubectl, Helm |
| `scale-deployment.sh` | Scale deployment up/down | **LOW** | kubectl |
| `update-configmap.sh` | Update configuration without restart | **LOW** | kubectl |
| `backup-persistent-data.sh` | Backup persistent volumes | **LOW** | kubectl, backup tools |

### Planned Manifests (To Be Created)

| Manifest | Purpose | Priority |
|----------|---------|----------|
| `deployment.yaml` | Main application deployment | **MEDIUM** |
| `service.yaml` | Service configuration | **MEDIUM** |
| `ingress.yaml` | Ingress routing configuration | **MEDIUM** |
| `configmap.yaml` | Application configuration | **MEDIUM** |
| `hpa.yaml` | Horizontal Pod Autoscaler | **LOW** |
| `networkpolicy.yaml` | Network security policies | **LOW** |

## 🚀 Planned Script Details

### `deploy-k8s.sh` (Priority: MEDIUM)

**Purpose:** Deploy documentation application to Kubernetes cluster

**Features:**
- Deploy using kubectl or Helm
- Support for multiple environments
- Rolling updates with zero downtime
- Health checks and readiness probes
- Automatic rollback on failure

**Planned Usage:**
```bash
./deploy-k8s.sh [--namespace namespace] [--env environment] [--replicas count]

# Examples
./deploy-k8s.sh --namespace csa-docs --env production
./deploy-k8s.sh --replicas 3 --env staging
./deploy-k8s.sh --dry-run  # Validate without deploying
```

### `setup-ingress.sh` (Priority: MEDIUM)

**Purpose:** Configure ingress controller and SSL certificates

**Features:**
- Install and configure NGINX ingress controller
- Set up cert-manager for automatic SSL certificates
- Configure custom domains and routing
- Enable rate limiting and security headers

**Planned Usage:**
```bash
./setup-ingress.sh --domain docs.contoso.com [--email admin@contoso.com]

# Examples
./setup-ingress.sh --domain docs.contoso.com --email admin@contoso.com
./setup-ingress.sh --internal-only  # Internal cluster access only
```

### `setup-monitoring.sh` (Priority: LOW)

**Purpose:** Deploy comprehensive monitoring stack

**Features:**
- Install Prometheus for metrics collection
- Deploy Grafana for visualization
- Configure alerting rules and notifications
- Set up log aggregation with Fluentd/ELK
- Create documentation-specific dashboards

**Planned Usage:**
```bash
./setup-monitoring.sh [--namespace monitoring] [--storage-class class]

# Examples
./setup-monitoring.sh --namespace kube-prometheus
./setup-monitoring.sh --storage-class premium-ssd
```

## ☸️ Kubernetes Architecture

### Deployment Strategy

**Architecture Components:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Load Balancer │────│  Ingress         │────│  Service        │
│   (Cloud LB)    │    │  Controller      │    │  (ClusterIP)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                          │
                       ┌─────────────────────────────────┼─────────────────────────────────┐
                       │                                 │                                 │
                ┌──────▼──────┐                   ┌──────▼──────┐                   ┌──────▼──────┐
                │    Pod 1    │                   │    Pod 2    │                   │    Pod 3    │
                │             │                   │             │                   │             │
                │  nginx:80   │                   │  nginx:80   │                   │  nginx:80   │
                │  docs site  │                   │  docs site  │                   │  docs site  │
                └─────────────┘                   └─────────────┘                   └─────────────┘
```

### Resource Allocation

**Recommended Resources:**
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "50m"
  limits:
    memory: "128Mi" 
    cpu: "100m"
```

**Scaling Configuration:**
- **Minimum replicas:** 2 (high availability)
- **Maximum replicas:** 10 (burst capacity)
- **Target CPU utilization:** 70%
- **Target memory utilization:** 80%

## 📄 Planned Kubernetes Manifests

### `deployment.yaml` (Priority: MEDIUM)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: csa-docs
  namespace: csa-docs
  labels:
    app: csa-docs
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: csa-docs
  template:
    metadata:
      labels:
        app: csa-docs
    spec:
      containers:
      - name: docs
        image: csa-docs:latest
        ports:
        - containerPort: 80
          name: http
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DOCS_BASE_URL
          value: "https://docs.contoso.com"
```

### `service.yaml` (Priority: MEDIUM)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: csa-docs-service
  namespace: csa-docs
  labels:
    app: csa-docs
spec:
  selector:
    app: csa-docs
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  type: ClusterIP
```

### `ingress.yaml` (Priority: MEDIUM)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: csa-docs-ingress
  namespace: csa-docs
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - docs.contoso.com
    secretName: csa-docs-tls
  rules:
  - host: docs.contoso.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: csa-docs-service
            port:
              number: 80
```

### `hpa.yaml` (Priority: LOW)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: csa-docs-hpa
  namespace: csa-docs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: csa-docs
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 🔧 Cluster Requirements

### Minimum Cluster Specifications

**Node Requirements:**
- **CPU:** 2 vCPUs per node minimum
- **Memory:** 4GB RAM per node minimum  
- **Storage:** 20GB disk per node minimum
- **Network:** CNI plugin (Calico, Flannel, etc.)

**Kubernetes Version:**
- **Minimum:** v1.24+
- **Recommended:** v1.28+
- **Features:** Ingress Controller, CSI drivers, RBAC

### Prerequisites

**Required Components:**
```bash
# Core components
- kubectl (matching cluster version)
- Ingress Controller (NGINX recommended)
- cert-manager (for SSL certificates)
- Metrics Server (for HPA)

# Optional components  
- Helm v3+ (for package management)
- Prometheus Operator (for monitoring)
- External DNS (for automatic DNS management)
```

### Cloud Provider Support

**Supported Kubernetes Services:**
- **Azure Kubernetes Service (AKS)** - Native Azure integration
- **Amazon Elastic Kubernetes Service (EKS)** - AWS integration
- **Google Kubernetes Engine (GKE)** - Google Cloud integration
- **On-premises clusters** - Generic Kubernetes support

## 📊 Monitoring and Observability

### Metrics Collection

**Application Metrics:**
- **HTTP request metrics** - Request rate, latency, errors
- **Resource utilization** - CPU, memory, network usage
- **Custom metrics** - Documentation-specific metrics
- **Business metrics** - Page views, user engagement

**Infrastructure Metrics:**
- **Pod metrics** - Pod status, restarts, resource usage
- **Node metrics** - Node health, capacity, network
- **Cluster metrics** - Cluster health, API server metrics

### Logging Strategy

**Log Aggregation:**
```yaml
# Fluentd DaemonSet for log collection
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  # Fluentd configuration for centralized logging
```

**Log Destinations:**
- **ElasticSearch** - Full-text search and analytics
- **Azure Monitor Logs** - Cloud-native logging
- **Prometheus Loki** - Label-based log aggregation
- **Splunk** - Enterprise log management

### Alerting Rules

**Critical Alerts:**
- **Pod crash loops** - Pods failing to start repeatedly
- **High error rates** - HTTP 5xx errors > 5%
- **Resource exhaustion** - CPU/Memory usage > 90%
- **Certificate expiration** - SSL certificates expiring < 30 days

## 🔒 Security Considerations

### Pod Security

**Security Context:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
```

### Network Security

**Network Policies:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: csa-docs-netpol
spec:
  podSelector:
    matchLabels:
      app: csa-docs
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
```

### RBAC Configuration

**Service Account:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: csa-docs-sa
  namespace: csa-docs
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: csa-docs-role
  namespace: csa-docs
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
```

## 🔍 Troubleshooting

### Common Kubernetes Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **Pods not starting** | Resource constraints | Check resource requests/limits |
| **ImagePullBackOff** | Image not accessible | Verify image registry and credentials |
| **Service unreachable** | Network/firewall issues | Check service and ingress configuration |
| **SSL certificate issues** | cert-manager problems | Check cert-manager logs and configuration |
| **High latency** | Resource contention | Scale up pods or increase resources |

### Debugging Commands

```bash
# Check pod status and logs
kubectl get pods -n csa-docs
kubectl logs -f deployment/csa-docs -n csa-docs

# Check service and ingress
kubectl get svc,ingress -n csa-docs
kubectl describe ingress csa-docs-ingress -n csa-docs

# Check resource usage
kubectl top pods -n csa-docs
kubectl top nodes

# Check events
kubectl get events -n csa-docs --sort-by=.metadata.creationTimestamp

# Debug networking
kubectl exec -it pod/csa-docs-xxx -n csa-docs -- /bin/sh
```

### Performance Optimization

**Optimization Strategies:**
- **Resource tuning** - Optimize CPU/memory requests and limits
- **Image optimization** - Use multi-stage Docker builds
- **Caching** - Implement Redis/Memcached for content caching
- **CDN integration** - Use cloud CDN for static assets
- **Horizontal scaling** - Scale pods based on load

## 💰 Cost Considerations

### Cloud Provider Costs

**Azure Kubernetes Service (AKS):**
- **Control plane:** Free
- **Nodes:** Standard_B2s (~$30/month per node)
- **Load balancer:** ~$20/month
- **Storage:** Premium SSD ~$0.17/GB/month

**Estimated monthly cost for 3-node cluster:** ~$110-150/month

### Cost Optimization

- **Use burstable instances** - B-series VMs for variable workloads
- **Right-size resources** - Monitor and adjust resource requests
- **Use spot instances** - For non-production environments
- **Implement auto-scaling** - Scale down during low usage periods
- **Optimize storage** - Use appropriate storage classes

## 📚 Related Documentation

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Docker Deployment Guide](../docker/README.md)

## 🤝 Contributing

### Adding New Kubernetes Resources

1. **Follow Kubernetes best practices** - Use labels, annotations, resource limits
2. **Include security context** - Run as non-root, read-only filesystem
3. **Add health checks** - Implement liveness and readiness probes
4. **Support multiple environments** - Use configurable values
5. **Include monitoring** - Add Prometheus metrics and alerts
6. **Test thoroughly** - Test deployment, scaling, and failure scenarios

### Manifest Requirements

- [ ] Follows Kubernetes API conventions
- [ ] Includes proper labels and annotations
- [ ] Has resource requests and limits
- [ ] Implements security best practices
- [ ] Includes health checks
- [ ] Supports configuration via ConfigMaps/Secrets
- [ ] Is validated with `kubectl --dry-run=client`
- [ ] Is tested in actual Kubernetes cluster

## 📞 Support

For Kubernetes deployment issues:

- **GitHub Issues:** [Create Kubernetes Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=kubernetes,deployment)
- **Kubernetes Documentation:** Check official Kubernetes docs
- **kubectl Help:** `kubectl --help` or `kubectl command --help`
- **Community:** Kubernetes Slack, Stack Overflow
- **Cloud Support:** Use cloud provider support for managed Kubernetes
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team