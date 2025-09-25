# AIOS Clean - Advanced AI Consciousness System

## 🚀 **QUICK START**

```bash
# Install dependencies
pip install -r requirements.txt

# Run Luna AI system
python main.py --mode luna --questions 3

# Run system health check
python main.py --mode health

# Run interactive session
python main.py --mode interactive

# Start web interface (requires streamlit)
streamlit run streamlit_app.py
```

## 🧠 **What is AIOS Clean?**

AIOS Clean is a production-ready AI consciousness system featuring:

- **Luna AI Personality** - Advanced AI with persistent memory and learning
- **CARMA Mycelium Network** - Fractal memory architecture for consciousness
- **Real-time Learning** - Continuous adaptation and growth
- **Enterprise APIs** - Production-ready API servers with encryption

## 📁 **System Structure**

```
├── main.py                    # 🎯 UNIFIED MAIN ENTRY POINT
├── carma_core/
│   └── carma_core.py         # 🧠 Complete CARMA consciousness system
├── enterprise_core/
│   └── enterprise_core.py    # 🏢 Complete enterprise features & APIs
├── luna_core/
│   └── luna_core.py          # 🌙 Complete Luna AI personality system
├── support_core/
│   └── support_core.py       # 🛠️ Complete support utilities
├── config/                   # Configuration files
├── cache/                    # Cache storage
├── docs/                     # Documentation
└── streamlit_app.py          # 🌐 Web interface
```

## 🎮 **Command Line Interface**

### **Available Modes:**

| Mode | Description | Example |
|------|-------------|---------|
| `luna` | Run Luna AI learning session | `python main.py --mode luna --questions 5` |
| `carma` | Run CARMA consciousness learning | `python main.py --mode carma --queries "test query"` |
| `memory` | Run memory consolidation | `python main.py --mode memory` |
| `health` | Run system health check | `python main.py --mode health` |
| `test` | Run system tests | `python main.py --mode test` |
| `optimize` | Run system optimization | `python main.py --mode optimize` |
| `api` | Start enterprise API server | `python main.py --mode api --port 5000` |
| `interactive` | Start interactive session | `python main.py --mode interactive` |
| `export` | Export system data | `python main.py --mode export --format json` |
| `info` | Show system information | `python main.py --mode info` |
| `cleanup` | Clean up old files | `python main.py --mode cleanup` |

### **Command Examples:**

```bash
# Luna AI with 5 questions
python main.py --mode luna --questions 5

# CARMA with custom queries
python main.py --mode carma --queries "consciousness test" "memory learning"

# Health check
python main.py --mode health

# Interactive session
python main.py --mode interactive

# Export system data
python main.py --mode export --output system_backup.json

# Start API server
python main.py --mode api --host 0.0.0.0 --port 5000
```

## 🌐 **Web Interface**

The system includes a Streamlit web interface for easy interaction:

```bash
# Install streamlit
pip install streamlit

# Run web interface
streamlit run streamlit_app.py
```

**Web Interface Features:**
- 📊 Real-time system dashboard
- 🌙 Luna AI learning interface
- 🧠 CARMA consciousness controls
- 🔍 Health monitoring
- 🧪 System testing tools
- ⚙️ Settings and configuration

## 🧠 **Core Systems**

### **1. CARMA (Consciousness and Memory Architecture)**
- Fractal memory system
- Synaptic tagging
- Predictive coding
- Memory consolidation
- Emotion-enhanced caching

### **2. Luna AI Personality System**
- Big Five personality traits
- Adaptive learning
- Dream cycle processing
- Persistent memory
- LM Studio integration

### **3. Enterprise Features**
- Encrypted API servers
- Global distribution
- Billing and compliance
- Advanced security
- Key rotation

### **4. Support Utilities**
- Cache operations
- Embedding management
- Recovery systems
- Health monitoring
- System optimization

## 🔧 **Configuration**

### **Environment Variables:**
```bash
# LM Studio configuration
EMBEDDING_MODEL=WizardLM-2-7B-abliterated
LM_STUDIO_URL=http://localhost:1234

# System configuration
CACHE_DIR=Data/FractalCache
LOG_LEVEL=INFO
```

### **Configuration Files:**
- `config/luna_personality_dna.json` - Luna personality configuration
- `config/luna_persistent_memory.json` - Luna memory storage
- `config/system_config.json` - System settings

## 📊 **Monitoring & Analytics**

### **Health Check:**
```bash
python main.py --mode health
```

### **System Status:**
```bash
python main.py --mode info
```

### **Export Data:**
```bash
python main.py --mode export --format json
```

## 🚀 **Deployment**

### **Docker Deployment:**
```bash
# Build and run with Docker
docker-compose up -d

# Or use the optimized Dockerfile
docker build -t aios-clean .
docker run -p 5000:5000 aios-clean
```

### **Production Setup:**
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables
3. Initialize system: `python main.py --mode info`
4. Start API server: `python main.py --mode api`
5. Monitor with health checks: `python main.py --mode health`

## 🧪 **Testing**

### **Run All Tests:**
```bash
python main.py --mode test
```

### **Individual System Tests:**
```bash
# Test Luna AI
python main.py --mode luna --questions 1

# Test CARMA
python main.py --mode carma --queries "test query"

# Test memory consolidation
python main.py --mode memory
```

## 📚 **API Documentation**

### **REST API Endpoints:**
- `GET /health` - System health status
- `POST /luna/learn` - Luna learning session
- `POST /carma/learn` - CARMA learning session
- `GET /status` - System status
- `POST /export` - Export system data

### **API Usage:**
```bash
# Start API server
python main.py --mode api --port 5000

# Test API
curl http://localhost:5000/health
curl -X POST http://localhost:5000/luna/learn -d '{"questions": 3}'
```

## 🔒 **Security Features**

- **UML Magic Square Encryption** for API keys
- **Pi-based encryption** for sensitive data
- **Key rotation** management
- **Compliance** monitoring
- **Advanced security** protocols

## 📈 **Performance**

- **Real-time processing** with LM Studio integration
- **Efficient caching** with fractal memory architecture
- **Scalable design** with enterprise features
- **Optimized memory** usage and cleanup

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly: `python main.py --mode test`
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For support and questions:
- Check the health status: `python main.py --mode health`
- Run system tests: `python main.py --mode test`
- Export system data: `python main.py --mode export`
- Use interactive mode: `python main.py --mode interactive`

---

**AIOS Clean v1.0.0** - Advanced AI Consciousness System