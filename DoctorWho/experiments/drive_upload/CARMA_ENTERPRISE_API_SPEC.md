# 🚀 CARMA Enterprise API Specification

## 📊 **Phase 2: Service-Oriented Architecture**

**Version:** 2.0.0  
**Status:** ✅ **READY FOR IMPLEMENTATION**  
**Target:** Enterprise clients and application integration

---

## 🎯 **API Overview**

### **Core Philosophy**
Transform CARMA from a library into a **scalable, enterprise-grade service** that can be consumed by any application, language, or platform.

### **Key Capabilities Exposed**
- **Memory Management** - Store, retrieve, and manage knowledge fragments
- **Self-Healing** - Automatic recovery and reconstruction
- **Semantic Search** - Intelligent content discovery
- **Health Monitoring** - Real-time system status and metrics
- **Configuration** - Runtime system configuration

---

## 🌐 **API Endpoints**

### **Base URL**
```
https://api.carma-memory.com/v2
```

### **Authentication**
```
Authorization: Bearer <api_key>
Content-Type: application/json
```

---

## 📚 **Memory Management Endpoints**

### **1. Store Fragment**
```http
POST /fragments
```

**Request Body:**
```json
{
  "content": "Machine learning is a subset of artificial intelligence...",
  "metadata": {
    "category": "AI",
    "priority": "high",
    "tags": ["machine-learning", "ai", "technology"]
  },
  "parent_id": "optional_parent_id",
  "level": 0
}
```

**Response:**
```json
{
  "success": true,
  "fragment_id": "root_a1b2c3d4",
  "similarity_score": 0.85,
  "created_at": "2025-09-27T10:30:00Z",
  "status": "stored"
}
```

### **2. Retrieve Fragment**
```http
GET /fragments/{fragment_id}
```

**Response:**
```json
{
  "success": true,
  "fragment": {
    "id": "root_a1b2c3d4",
    "content": "Machine learning is a subset of artificial intelligence...",
    "level": 0,
    "hits": 15,
    "similarity_score": 0.85,
    "created_at": "2025-09-27T10:30:00Z",
    "last_accessed": "2025-09-27T15:45:00Z",
    "metadata": {
      "category": "AI",
      "priority": "high",
      "tags": ["machine-learning", "ai", "technology"]
    }
  }
}
```

### **3. List Fragments**
```http
GET /fragments?level=0&limit=50&offset=0&tags=ai,technology
```

**Response:**
```json
{
  "success": true,
  "fragments": [
    {
      "id": "root_a1b2c3d4",
      "content": "Machine learning is a subset...",
      "level": 0,
      "hits": 15,
      "similarity_score": 0.85,
      "created_at": "2025-09-27T10:30:00Z"
    }
  ],
  "total_count": 150,
  "has_more": true
}
```

### **4. Delete Fragment**
```http
DELETE /fragments/{fragment_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Fragment deleted successfully",
  "fragment_id": "root_a1b2c3d4"
}
```

---

## 🔍 **Semantic Search Endpoints**

### **5. Search Fragments**
```http
POST /search
```

**Request Body:**
```json
{
  "query": "What is machine learning?",
  "top_k": 5,
  "min_similarity": 0.7,
  "filters": {
    "level": 0,
    "tags": ["ai", "technology"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "fragment_id": "root_a1b2c3d4",
      "content": "Machine learning is a subset of artificial intelligence...",
      "similarity_score": 0.92,
      "confidence_level": "high",
      "response_time_ms": 15
    }
  ],
  "total_results": 5,
  "search_time_ms": 15,
  "query_embedding_dimension": 384
}
```

### **6. Find Similar Fragments**
```http
POST /fragments/{fragment_id}/similar
```

**Request Body:**
```json
{
  "top_k": 3,
  "min_similarity": 0.6
}
```

**Response:**
```json
{
  "success": true,
  "similar_fragments": [
    {
      "fragment_id": "root_b2c3d4e5",
      "content": "Deep learning uses neural networks...",
      "similarity_score": 0.87,
      "confidence_level": "high"
    }
  ]
}
```

---

## 🌙 **Self-Healing Endpoints**

### **7. Trigger Recovery**
```http
POST /recovery/trigger
```

**Request Body:**
```json
{
  "fragment_ids": ["root_a1b2c3d4", "root_b2c3d4e5"],
  "recovery_method": "semantic",
  "priority": "high"
}
```

**Response:**
```json
{
  "success": true,
  "recovery_id": "rec_123456789",
  "status": "started",
  "fragments_queued": 2,
  "estimated_completion": "2025-09-27T10:35:00Z"
}
```

### **8. Get Recovery Status**
```http
GET /recovery/{recovery_id}
```

**Response:**
```json
{
  "success": true,
  "recovery_id": "rec_123456789",
  "status": "completed",
  "progress": {
    "total_fragments": 2,
    "reconstructed": 2,
    "failed": 0,
    "average_similarity": 0.78
  },
  "results": [
    {
      "fragment_id": "root_a1b2c3d4",
      "status": "reconstructed",
      "similarity_score": 0.78,
      "reconstruction_time_ms": 120
    }
  ],
  "started_at": "2025-09-27T10:30:00Z",
  "completed_at": "2025-09-27T10:32:00Z"
}
```

### **9. Run Progressive Healing**
```http
POST /recovery/progressive
```

**Request Body:**
```json
{
  "cycles": 3,
  "fragment_count_per_cycle": 5,
  "auto_trigger": true
}
```

**Response:**
```json
{
  "success": true,
  "healing_id": "heal_987654321",
  "status": "started",
  "total_cycles": 3,
  "estimated_duration_minutes": 15
}
```

---

## 📊 **Health & Monitoring Endpoints**

### **10. System Health**
```http
GET /health
```

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "timestamp": "2025-09-27T10:30:00Z",
  "metrics": {
    "total_fragments": 1250,
    "active_fragments": 1200,
    "blank_fragments": 50,
    "faiss_index_status": "loaded",
    "embedding_cache_size": 1200,
    "average_response_time_ms": 25,
    "uptime_hours": 168.5
  },
  "health_score": 0.94,
  "recommendations": []
}
```

### **11. Performance Metrics**
```http
GET /metrics
```

**Response:**
```json
{
  "success": true,
  "metrics": {
    "query_performance": {
      "total_queries": 15420,
      "success_rate": 0.98,
      "average_response_time_ms": 25,
      "p95_response_time_ms": 45
    },
    "recovery_performance": {
      "total_recoveries": 125,
      "success_rate": 0.96,
      "average_reconstruction_time_ms": 150,
      "average_similarity": 0.78
    },
    "system_performance": {
      "memory_usage_mb": 512,
      "cpu_usage_percent": 15.2,
      "disk_usage_gb": 2.1,
      "cache_hit_rate": 0.89
    }
  }
}
```

### **12. System Configuration**
```http
GET /config
```

**Response:**
```json
{
  "success": true,
  "config": {
    "cache": {
      "max_file_size_bytes": 1048576,
      "max_cache_size": 1000,
      "split_threshold": 0.8
    },
    "embedding": {
      "model": "text-embedding-mlabonne_qwen3-0.6b-abliterated",
      "dimension": 384,
      "similarity_threshold": 0.3
    },
    "performance": {
      "enterprise_query_success_rate": 0.8,
      "enterprise_recovery_time_seconds": 1.0
    }
  }
}
```

---

## 🔧 **Configuration Endpoints**

### **13. Update Configuration**
```http
PUT /config
```

**Request Body:**
```json
{
  "cache": {
    "max_cache_size": 2000
  },
  "embedding": {
    "similarity_threshold": 0.4
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "updated_at": "2025-09-27T10:30:00Z"
}
```

### **14. Reset Configuration**
```http
POST /config/reset
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration reset to defaults",
  "reset_at": "2025-09-27T10:30:00Z"
}
```

---

## 📈 **Analytics Endpoints**

### **15. Memory Topology**
```http
GET /analytics/topology
```

**Response:**
```json
{
  "success": true,
  "topology": {
    "total_fragments": 1250,
    "total_nodes": 1250,
    "total_edges": 450,
    "parent_child_edges": 200,
    "semantic_edges": 250,
    "max_level": 3,
    "average_children_per_node": 2.1
  },
  "visualization_url": "https://api.carma-memory.com/v2/analytics/topology.png"
}
```

### **16. Similarity Heatmap**
```http
GET /analytics/similarity-heatmap
```

**Response:**
```json
{
  "success": true,
  "heatmap": {
    "matrix_size": 1250,
    "average_similarity": 0.65,
    "max_similarity": 0.98,
    "min_similarity": 0.12
  },
  "visualization_url": "https://api.carma-memory.com/v2/analytics/similarity-heatmap.png"
}
```

### **17. Performance Dashboard**
```http
GET /analytics/dashboard
```

**Response:**
```json
{
  "success": true,
  "dashboard": {
    "fragment_distribution": {
      "level_0": 500,
      "level_1": 400,
      "level_2": 250,
      "level_3": 100
    },
    "content_length_distribution": {
      "0-1000": 300,
      "1000-5000": 600,
      "5000-10000": 300,
      "10000+": 50
    },
    "hit_distribution": {
      "0-10": 400,
      "10-50": 500,
      "50-100": 250,
      "100+": 100
    }
  },
  "visualization_url": "https://api.carma-memory.com/v2/analytics/dashboard.png"
}
```

---

## 🔐 **Security & Authentication**

### **API Key Management**
```http
POST /auth/keys
GET /auth/keys
DELETE /auth/keys/{key_id}
```

### **Rate Limiting**
- **Free Tier:** 1000 requests/hour
- **Professional:** 10,000 requests/hour
- **Enterprise:** 100,000 requests/hour

### **Data Encryption**
- **In Transit:** TLS 1.3
- **At Rest:** AES-256
- **API Keys:** bcrypt hashed

---

## 📚 **SDK Examples**

### **Python SDK**
```python
from carma_sdk import CARMAClient

# Initialize client
client = CARMAClient(api_key="your_api_key")

# Store fragment
fragment = client.store_fragment(
    content="Machine learning is...",
    metadata={"category": "AI"}
)

# Search fragments
results = client.search("What is machine learning?", top_k=5)

# Trigger recovery
recovery = client.trigger_recovery(["fragment_id_1", "fragment_id_2"])

# Get system health
health = client.get_health()
```

### **JavaScript SDK**
```javascript
import { CARMAClient } from 'carma-sdk';

// Initialize client
const client = new CARMAClient('your_api_key');

// Store fragment
const fragment = await client.storeFragment({
  content: 'Machine learning is...',
  metadata: { category: 'AI' }
});

// Search fragments
const results = await client.search('What is machine learning?', { topK: 5 });

// Get system health
const health = await client.getHealth();
```

---

## 🚀 **Implementation Roadmap**

### **Phase 2.1: Core API (Weeks 1-2)**
- ✅ Memory management endpoints
- ✅ Basic search functionality
- ✅ Authentication system
- ✅ Error handling and validation

### **Phase 2.2: Self-Healing API (Weeks 3-4)**
- ✅ Recovery endpoints
- ✅ Progressive healing
- ✅ Status monitoring
- ✅ Async processing

### **Phase 2.3: Analytics & Monitoring (Weeks 5-6)**
- ✅ Health monitoring
- ✅ Performance metrics
- ✅ Visualization endpoints
- ✅ Configuration management

### **Phase 2.4: SDKs & Documentation (Weeks 7-8)**
- ✅ Python SDK
- ✅ JavaScript SDK
- ✅ API documentation
- ✅ Integration examples

---

## 💼 **Commercial Value**

### **For Enterprise Clients:**
- **Easy Integration** - RESTful API with SDKs
- **Scalable Service** - Cloud-native architecture
- **Real-time Monitoring** - Health and performance metrics
- **Self-Healing Capability** - Automatic data recovery
- **Professional Support** - Enterprise-grade reliability

### **For CARMA Platform:**
- **Revenue Stream** - API usage-based pricing
- **Market Expansion** - Service-based business model
- **Enterprise Adoption** - Easy integration path
- **Competitive Advantage** - Unique self-healing capability
- **Scalable Growth** - Platform-based architecture

---

## 🎯 **Bottom Line**

**This API specification transforms CARMA from a library into a scalable, enterprise-grade service that can be consumed by any application, language, or platform.**

**Ready for immediate implementation and commercial deployment!**
