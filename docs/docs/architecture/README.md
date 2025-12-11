# Architecture Documentation Index

> **[Home](../../README.md)** | **Architecture Docs**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

Index of architecture documentation for Cloud Scale Analytics.

---

## Overview

This section provides architecture documentation for:

- Reference architectures
- Design patterns
- Integration patterns
- Security architecture

---

## Reference Architectures

| Architecture | Description | Use Case |
|-------------|-------------|----------|
| [Delta Lakehouse](../../architecture/delta-lakehouse/README.md) | Medallion architecture with Delta Lake | General analytics |
| [Serverless SQL](../../architecture/serverless-sql/README.md) | Serverless data warehouse | Ad-hoc analytics |
| [Streaming Analytics](../../03-architecture-patterns/streaming-architectures/README.md) | Real-time processing | Event-driven apps |
| [Feature Store](../../architecture/feature-store/README.md) | ML feature management | MLOps |

---

## Architecture Patterns

### Data Processing

- **Batch Processing**: Large-scale ETL with Spark
- **Stream Processing**: Real-time with Event Hubs + Stream Analytics
- **Lambda Architecture**: Combined batch and speed layers
- **Kappa Architecture**: Streaming-only processing

### Data Storage

- **Data Lake**: Raw data storage in ADLS Gen2
- **Delta Lake**: ACID transactions on data lake
- **Data Warehouse**: Dedicated SQL pools
- **Lakehouse**: Combined lake + warehouse

---

## Quick Links

- [Architecture Patterns](../../03-architecture-patterns/README.md)
- [Implementation Guides](../../04-implementation-guides/README.md)
- [Best Practices](../../best-practices/README.md)

---

*Last Updated: January 2025*
