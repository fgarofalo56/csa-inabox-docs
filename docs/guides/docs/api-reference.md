# API Reference Template

> **Home [Home](../../../README.md)** | **Documentation** | **Guides [Guides](../README.md)** | **Templates**

---

## Overview

This template provides a standardized format for documenting APIs in the CSA-in-a-Box documentation project. Use this template when creating API reference documentation.

## Table of Contents

- [API Overview](#api-overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## API Overview

### Base URL

```text
Production: https://api.csa-docs.azurewebsites.net/v1
Staging: https://api-staging.csa-docs.azurewebsites.net/v1
Development: http://localhost:8000/api/v1
```

### API Versioning

This API uses URL-based versioning. The current version is `v1`.

### Content Types

| Request | Response | Description |
|---------|----------|-------------|
| `application/json` | `application/json` | Standard JSON API |
| `application/x-www-form-urlencoded` | `application/json` | Form submissions |

---

## Authentication

### API Key Authentication

Include your API key in the request header:

```http
GET /api/v1/resource HTTP/1.1
Host: api.csa-docs.azurewebsites.net
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### OAuth 2.0

For user-specific operations, use OAuth 2.0 authentication:

```http
GET /api/v1/resource HTTP/1.1
Host: api.csa-docs.azurewebsites.net
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json
```

---

## Endpoints

### Resource Collection

#### List Resources

Retrieve a list of resources.

**Endpoint:** `GET /api/v1/resources`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1) |
| `limit` | integer | No | Items per page (default: 20, max: 100) |
| `sort` | string | No | Sort field (default: `created_at`) |
| `order` | string | No | Sort order: `asc` or `desc` (default: `desc`) |
| `filter` | string | No | Filter criteria |

**Request Example:**

```bash
curl -X GET "https://api.csa-docs.azurewebsites.net/v1/resources?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**Response Example:**

```json
{
  "data": [
    {
      "id": "res_123456",
      "name": "Example Resource",
      "description": "Resource description",
      "status": "active",
      "created_at": "2025-12-09T10:30:00Z",
      "updated_at": "2025-12-09T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 500 | Internal Server Error |

#### Get Resource

Retrieve a specific resource by ID.

**Endpoint:** `GET /api/v1/resources/{id}`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Resource identifier |

**Request Example:**

```bash
curl -X GET "https://api.csa-docs.azurewebsites.net/v1/resources/res_123456" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**Response Example:**

```json
{
  "id": "res_123456",
  "name": "Example Resource",
  "description": "Resource description",
  "status": "active",
  "metadata": {
    "tags": ["analytics", "synapse"],
    "category": "data-platform"
  },
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T10:30:00Z"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 404 | Resource not found |
| 401 | Unauthorized |
| 500 | Internal Server Error |

#### Create Resource

Create a new resource.

**Endpoint:** `POST /api/v1/resources`

**Request Body:**

```json
{
  "name": "New Resource",
  "description": "Resource description",
  "status": "active",
  "metadata": {
    "tags": ["analytics"],
    "category": "data-platform"
  }
}
```

**Response Example:**

```json
{
  "id": "res_789012",
  "name": "New Resource",
  "description": "Resource description",
  "status": "active",
  "metadata": {
    "tags": ["analytics"],
    "category": "data-platform"
  },
  "created_at": "2025-12-09T11:00:00Z",
  "updated_at": "2025-12-09T11:00:00Z"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 409 | Conflict |
| 500 | Internal Server Error |

#### Update Resource

Update an existing resource.

**Endpoint:** `PATCH /api/v1/resources/{id}`

**Request Body:**

```json
{
  "name": "Updated Resource Name",
  "status": "inactive"
}
```

**Response Example:**

```json
{
  "id": "res_123456",
  "name": "Updated Resource Name",
  "description": "Resource description",
  "status": "inactive",
  "metadata": {
    "tags": ["analytics", "synapse"],
    "category": "data-platform"
  },
  "created_at": "2025-12-09T10:30:00Z",
  "updated_at": "2025-12-09T11:15:00Z"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Resource not found |
| 500 | Internal Server Error |

#### Delete Resource

Delete a resource.

**Endpoint:** `DELETE /api/v1/resources/{id}`

**Response Example:**

```json
{
  "message": "Resource deleted successfully",
  "id": "res_123456"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Resource not found |
| 500 | Internal Server Error |

---

## Data Models

### Resource Model

```typescript
interface Resource {
  id: string;                    // Unique identifier
  name: string;                  // Resource name
  description: string;           // Resource description
  status: 'active' | 'inactive'; // Resource status
  metadata: {
    tags: string[];              // Resource tags
    category: string;            // Resource category
  };
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
}
```

### Pagination Model

```typescript
interface Pagination {
  total: number;    // Total number of items
  page: number;     // Current page number
  limit: number;    // Items per page
  pages: number;    // Total number of pages
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "details": {
      "resource_id": "res_123456"
    },
    "timestamp": "2025-12-09T12:00:00Z"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request validation failed |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Resource does not exist |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limiting

### Rate Limits

| Tier | Requests per Minute | Requests per Hour |
|------|---------------------|-------------------|
| **Free** | 60 | 1,000 |
| **Standard** | 600 | 10,000 |
| **Premium** | 6,000 | 100,000 |

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1638360000
```

---

## Examples

### Python Example

```python
import requests

# Configuration
API_BASE_URL = "https://api.csa-docs.azurewebsites.net/v1"
API_KEY = "your_api_key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# List resources
response = requests.get(
    f"{API_BASE_URL}/resources",
    headers=headers,
    params={"page": 1, "limit": 20}
)

if response.status_code == 200:
    data = response.json()
    print(f"Total resources: {data['pagination']['total']}")
    for resource in data['data']:
        print(f"- {resource['name']}")
```

### JavaScript Example

```javascript
const API_BASE_URL = 'https://api.csa-docs.azurewebsites.net/v1';
const API_KEY = 'your_api_key';

// List resources
async function listResources() {
  const response = await fetch(`${API_BASE_URL}/resources?page=1&limit=20`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    }
  });

  if (response.ok) {
    const data = await response.json();
    console.log(`Total resources: ${data.pagination.total}`);
    data.data.forEach(resource => {
      console.log(`- ${resource.name}`);
    });
  }
}

listResources();
```

---

## Additional Resources

- [API Authentication Guide](./authentication.md)
- [API Best Practices](./best-practices.md)
- [SDKs and Client Libraries](./sdks.md)

---

**Last Updated:** December 9, 2025
**Version:** 1.0.0
**API Version:** v1
