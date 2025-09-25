@echo off
REM CARMA Encrypted API Server Runner
REM Uses Travis Miner's UML Magic Square Encryption

echo 🚀 Starting CARMA Encrypted API Server
echo 🔮 Using UML Magic Square Encryption
echo ==================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install docker-compose first.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "Data\FractalCache" mkdir "Data\FractalCache"
if not exist "experiments" mkdir "experiments"
if not exist "logs" mkdir "logs"

REM Build and run the encrypted API server
echo 🐳 Building and running CARMA Encrypted API Server...
docker-compose -f docker-compose.encrypted.yml up --build -d

REM Wait for the service to be ready
echo ⏳ Waiting for service to be ready...
timeout /t 10 /nobreak >nul

REM Check if the service is running
echo 🔍 Checking service status...
curl -f http://localhost:5000/v2/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ CARMA Encrypted API Server is running!
    echo 🌐 API available at: http://localhost:5000
    echo 📚 Health check: http://localhost:5000/v2/health
    echo 🔑 Master API key will be generated automatically
    echo.
    echo 🔮 UML Magic Square Encryption Features:
    echo   • Recursive compression for key generation
    echo   • Magic square validation for security
    echo   • Meta-stability checking
    echo   • Permission-based access control
    echo   • Time-based entropy
    echo.
    echo 📋 Available endpoints:
    echo   • POST /v2/keys/generate - Generate new API key
    echo   • POST /v2/keys/validate - Validate API key
    echo   • GET /v2/keys/list - List active keys (admin only)
    echo   • POST /v2/fragments - Store fragment
    echo   • GET /v2/fragments/{id} - Retrieve fragment
    echo   • GET /v2/fragments - List fragments
    echo   • POST /v2/search - Search fragments
    echo   • GET /v2/health - System health
    echo   • GET /v2/system/status - System status
    echo   • GET /v2/system/metrics - Performance metrics
    echo   • GET /v2/system/config - System configuration
    echo   • GET /v2/analytics/topology - Memory topology
    echo   • GET /v2/analytics/performance - Performance analytics
    echo   • POST /v2/recovery/scan - Scan blank fragments
    echo   • POST /v2/recovery/heal - Heal fragments
    echo.
    echo 🎉 CARMA Encrypted API Server is ready for enterprise use!
) else (
    echo ❌ Failed to start CARMA Encrypted API Server
    echo 📋 Checking logs...
    docker-compose -f docker-compose.encrypted.yml logs carma-encrypted-api
    pause
    exit /b 1
)

pause
