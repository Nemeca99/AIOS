#!/bin/bash
# CARMA Encrypted API Server Runner
# Uses Travis Miner's UML Magic Square Encryption

echo "🚀 Starting CARMA Encrypted API Server"
echo "🔮 Using UML Magic Square Encryption"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p Data/FractalCache
mkdir -p experiments
mkdir -p logs

# Set permissions
echo "🔧 Setting permissions..."
chmod +x HiveMind/carma_encrypted_api_server.py

# Build and run the encrypted API server
echo "🐳 Building and running CARMA Encrypted API Server..."
docker-compose -f docker-compose.encrypted.yml up --build -d

# Wait for the service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if the service is running
echo "🔍 Checking service status..."
if curl -f http://localhost:5000/v2/health > /dev/null 2>&1; then
    echo "✅ CARMA Encrypted API Server is running!"
    echo "🌐 API available at: http://localhost:5000"
    echo "📚 Health check: http://localhost:5000/v2/health"
    echo "🔑 Master API key will be generated automatically"
    echo ""
    echo "🔮 UML Magic Square Encryption Features:"
    echo "  • Recursive compression for key generation"
    echo "  • Magic square validation for security"
    echo "  • Meta-stability checking"
    echo "  • Permission-based access control"
    echo "  • Time-based entropy"
    echo ""
    echo "📋 Available endpoints:"
    echo "  • POST /v2/keys/generate - Generate new API key"
    echo "  • POST /v2/keys/validate - Validate API key"
    echo "  • GET /v2/keys/list - List active keys (admin only)"
    echo "  • POST /v2/fragments - Store fragment"
    echo "  • GET /v2/fragments/{id} - Retrieve fragment"
    echo "  • GET /v2/fragments - List fragments"
    echo "  • POST /v2/search - Search fragments"
    echo "  • GET /v2/health - System health"
    echo "  • GET /v2/system/status - System status"
    echo "  • GET /v2/system/metrics - Performance metrics"
    echo "  • GET /v2/system/config - System configuration"
    echo "  • GET /v2/analytics/topology - Memory topology"
    echo "  • GET /v2/analytics/performance - Performance analytics"
    echo "  • POST /v2/recovery/scan - Scan blank fragments"
    echo "  • POST /v2/recovery/heal - Heal fragments"
    echo ""
    echo "🎉 CARMA Encrypted API Server is ready for enterprise use!"
else
    echo "❌ Failed to start CARMA Encrypted API Server"
    echo "📋 Checking logs..."
    docker-compose -f docker-compose.encrypted.yml logs carma-encrypted-api
    exit 1
fi
