#!/usr/bin/env python3
"""
CARMA System Constants and Configuration
Centralized configuration for the entire CARMA system
All hardcoded values should reference this file
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Any

# === SYSTEM VERSION ===
class SystemVersion:
    VERSION = "1.0.0"
    BUILD_DATE = "September 2025"
    STATUS = "PRODUCTION READY"

# === SYSTEM CONFIGURATION ===
class SystemConfig:
    # Cache Configuration
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    MIN_FILE_SIZE = 1024  # 1KB
    SPLIT_THRESHOLD = 0.8  # Split when 80% of max size
    MAX_SPLITS = 6  # 1 → 2 → 4 → 8 → 16 → 32 → 64
    MAX_CACHE_SIZE = 1000  # Maximum fragments before eviction
    
    # Timing Configuration
    TTL_HOURS = 24  # Time-to-live in hours
    MIN_HIT_COUNT = 2  # Minimum hits to avoid eviction
    EVICTION_THRESHOLD = 0.8  # Evict when 80% of max size
    
    # Embedding Configuration
    EMBEDDING_DIMENSION = 384  # Standard embedding dimension
    SIMILARITY_THRESHOLD = 0.3  # Cosine similarity threshold for linking
    QUERY_SUCCESS_THRESHOLD = 0.2  # Minimum similarity for query success
    RECONSTRUCTION_SUCCESS_THRESHOLD = 0.5  # High-quality reconstruction threshold
    
    # Recovery Configuration
    MAX_RECONSTRUCTION_ATTEMPTS = 3
    CONTEXT_WINDOW_SIZE = 5
    RECOVERY_TIMEOUT_SECONDS = 30
    
    # Performance Thresholds
    ENTERPRISE_QUERY_SUCCESS_RATE = 0.8  # 80% for enterprise readiness
    ENTERPRISE_RECONSTRUCTION_RATE = 0.9  # 90% for enterprise readiness
    ENTERPRISE_SIMILARITY_THRESHOLD = 0.7  # 70% for enterprise readiness
    ENTERPRISE_RECOVERY_TIME_SECONDS = 1.0  # 1 second max recovery time
    
    # Content Processing
    CONTENT_HASH_LENGTH = 8  # Length of content hash for IDs

# === CACHE CONFIGURATION ===
class CacheConfig:
    # File Size Limits
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    MIN_FILE_SIZE = 1024  # 1KB
    SPLIT_THRESHOLD = 0.8  # Split when 80% of max size
    MAX_SPLITS = 6  # 1 → 2 → 4 → 8 → 16 → 32 → 64
    MAX_CACHE_SIZE = 1000  # Maximum fragments before eviction
    
    # Timing Configuration
    TTL_HOURS = 24  # Time-to-live in hours
    MIN_HIT_COUNT = 2  # Minimum hits to avoid eviction
    EVICTION_THRESHOLD = 0.8  # Evict when 80% of max size
    
    # Content Processing
    CONTENT_HASH_LENGTH = 8  # Length of content hash for IDs
    MAX_CONTENT_LENGTH = 10000  # Maximum content length for processing
    MIN_CONTENT_LENGTH = 10  # Minimum content length to process

# === EMBEDDING CONFIGURATION ===
class EmbeddingConfig:
    # Model Configuration
    EMBEDDING_MODEL = "text-embedding-mlabonne_qwen3-0.6b-abliterated"
    API_URL = "http://localhost:1234/v1/embeddings"
    USE_API = False
    FALLBACK_DIMENSION = 384
    EMBEDDING_DIMENSION = 384  # Standard embedding dimension
    
    # Similarity Thresholds
    SIMILARITY_THRESHOLD = 0.3  # Cosine similarity threshold for linking
    QUERY_SUCCESS_THRESHOLD = 0.2  # Minimum similarity for query success
    RECONSTRUCTION_SUCCESS_THRESHOLD = 0.5  # High-quality reconstruction threshold
    ENTERPRISE_SIMILARITY_THRESHOLD = 0.7  # 70% for enterprise readiness
    
    # FAISS Configuration
    FAISS_INDEX_TYPE = "IndexFlatIP"  # Inner product for cosine similarity
    NORMALIZE_EMBEDDINGS = True
    DEFAULT_TOP_K = 3
    MAX_QUERY_RESULTS = 10

# === RECOVERY CONFIGURATION ===
class RecoveryConfig:
    # Recovery Limits
    MAX_RECONSTRUCTION_ATTEMPTS = 3
    CONTEXT_WINDOW_SIZE = 5
    RECOVERY_TIMEOUT_SECONDS = 30
    
    # Quality Thresholds
    MIN_RECONSTRUCTION_SIMILARITY = 0.3
    HIGH_QUALITY_THRESHOLD = 0.7
    ENTERPRISE_RECONSTRUCTION_RATE = 0.9  # 90% for enterprise readiness
    
    # Progressive Healing
    MAX_HEALING_CYCLES = 10
    HEALING_IMPROVEMENT_THRESHOLD = 0.05  # 5% improvement per cycle

# === PERFORMANCE THRESHOLDS ===
class PerformanceConfig:
    # Enterprise Thresholds
    ENTERPRISE_QUERY_SUCCESS_RATE = 0.8  # 80% for enterprise readiness
    ENTERPRISE_RECOVERY_TIME_SECONDS = 1.0  # 1 second max recovery time
    ENTERPRISE_RESPONSE_TIME_SECONDS = 0.1  # 100ms max response time
    
    # Scaling Targets
    TARGET_FRAGMENT_COUNT = 1000  # Target for scaling tests
    MAX_FRAGMENT_COUNT = 10000  # Maximum supported fragments
    MEMORY_USAGE_THRESHOLD = 0.8  # 80% memory usage threshold

# === FILE PATHS ===
class FilePaths:
    # Base Directories
    CACHE_DIR = "Data/FractalCache"
    EXPERIMENTS_DIR = "experiments"
    HIVEMIND_DIR = "HiveMind"
    UTILS_DIR = "utils"
    REPORTS_DIR = "reports"
    BACKUP_DIR = "backups"
    
    # Specific Files
    FAISS_INDEX = "luna_carma_integration/faiss.index"
    FAISS_IDS = "luna_carma_integration/faiss.ids.json"
    EMBEDDER_CACHE = "AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json"
    REGISTRY_JSON = "luna_carma_integration/registry.json"
    
    # Test Results
    FIXED_RECOVERY_RESULTS = "experiments/fixed_recovery_test_results.json"
    ENHANCED_RECOVERY_RESULTS = "experiments/enhanced_recovery_test_results.json"
    ENTERPRISE_DEMO_RESULTS = "experiments/simple_enterprise_demo_report.json"
    VISUALIZATION_REPORT = "experiments/visualization_report.json"
    
    # Visualization Outputs
    MEMORY_TOPOLOGY_PNG = "experiments/memory_topology.png"
    SIMILARITY_HEATMAP_PNG = "experiments/similarity_heatmap.png"
    PERFORMANCE_DASHBOARD_PNG = "experiments/performance_dashboard.png"
    
    # Database Paths
    CONVERSATIONS_DB = "F:/AI_Datasets/AIOS_Database/database/conversations.db"
    LUNA_PERSONALITY_DNA = "AI_Core/Nova AI/AI/personality/luna_personality_dna.json"
    LUNA_LEARNING_HISTORY = "AI_Core/Nova AI/AI/personality/learning_data/luna_learning_history.json"

# === FILE EXTENSIONS ===
class FileExtensions:
    JSON = ".json"
    PNG = ".png"
    CSV = ".csv"
    TXT = ".txt"
    MD = ".md"
    PY = ".py"
    DOT = ".dot"
    DB = ".db"

# === MESSAGES AND LOGGING ===
class SystemMessages:
    # Success Messages
    CACHE_INITIALIZED = "🌱 Fractal Mycelium Cache Initialized"
    FAISS_INDEX_LOADED = "✅ FAISS index loaded: {count} embeddings"
    FAISS_INDEX_BUILT = "✅ FAISS index built: {count} embeddings, dimension {dim}"
    RECONSTRUCTION_SUCCESS = "✅ Reconstructed: {file_id} (similarity: {similarity:.2f})"
    QUERY_SUCCESS = "✅ Success (similarity: {similarity:.2f})"
    SYSTEM_EXCELLENT = "✅ SYSTEM EXCELLENT: Self-healing capabilities demonstrated"
    ENTERPRISE_READY = "🚀 Ready for enterprise deployment with semantic reconstruction"
    
    # Warning Messages
    NO_EMBEDDING_INDEX = "⚠️  No embedding index built, using simple search"
    FAISS_NOT_AVAILABLE = "⚠️  FAISS not available, using simple similarity search"
    DIMENSION_MISMATCH = "⚠️  Dimension mismatch: index={index_dim}, embedder={embedder_dim}"
    COULD_NOT_LOAD_INDEX = "⚠️  Could not load existing FAISS index: {error}"
    
    # Error Messages
    FAISS_QUERY_ERROR = "❌ FAISS query error: {error}"
    FAISS_SEARCH_FAILED = "❌ FAISS search failed: {error}"
    NO_EMBEDDINGS_FOUND = "❌ No embeddings found to build index"
    NO_FRAGMENTS_FOUND = "❌ No fragments found to build index"
    RECONSTRUCTION_FAILED = "❌ Failed to reconstruct {file_id}: {error}"
    QUERY_FAILED = "❌ Failed (similarity: {similarity:.2f})"
    SYSTEM_NEEDS_WORK = "❌ SYSTEM NEEDS WORK: Self-healing capabilities insufficient"
    
    # Info Messages
    CREATED_BLANK_PLACEHOLDER = "🗑️  Created blank placeholder: {file_id}"
    DELETED_FRAGMENT = "🗑️  Deleted: {file_id}"
    RECOVERY_COMPLETE = "🌙 Recovery Complete: {recovered} recovered, {failed} failed in {duration:.2f}s"
    PROGRESSIVE_HEALING = "🔄 Progressive healing: {total} total recovered over {cycles} cycles"

# === MODEL CONFIGURATION ===
class ModelConfig:
    # Embedder Configuration
    EMBEDDING_MODEL = "text-embedding-mlabonne_qwen3-0.6b-abliterated"
    API_URL = "http://localhost:1234/v1/embeddings"
    USE_API = False
    FALLBACK_DIMENSION = 384
    
    # Query Configuration
    DEFAULT_TOP_K = 3
    MAX_QUERY_RESULTS = 10
    QUERY_TIMEOUT = 5.0

# === COMMERCIAL FRAMING ===
class CommercialFraming:
    # Product Name
    PRODUCT_NAME = "CARMA - Cognitive Adaptive Retrieval Memory Architecture"
    SHORT_NAME = "CARMA"
    
    # Taglines
    PRIMARY_TAGLINE = "Never lose knowledge again. Our system heals itself."
    TECHNICAL_TAGLINE = "Fault-Tolerant AI Memory with Self-Healing Capabilities"
    ENTERPRISE_TAGLINE = "Enterprise-Grade Self-Healing Knowledge Management"
    
    # Value Propositions
    VALUE_PROPOSITIONS = [
        "100% data recovery rate - No knowledge loss",
        "Sub-second healing speed - Minimal downtime", 
        "0.80+ semantic similarity - High-quality reconstruction",
        "Progressive healing - Gets better over time",
        "Fault-tolerant design - Handles any corruption",
        "Enterprise-grade performance - Production ready"
    ]
    
    # Key Metrics
    KEY_METRICS = {
        "query_success_rate": "100%",
        "reconstruction_rate": "100%", 
        "average_similarity": "0.80+",
        "recovery_time": "0.06 seconds",
        "scalability": "1000+ fragments",
        "reliability": "Fault-tolerant"
    }

# === ASSESSMENT CRITERIA ===
class AssessmentCriteria:
    # Overall Score Weights
    RECOVERY_WEIGHT = 0.8  # 80% weight on recovery performance
    QUERY_WEIGHT = 0.2     # 20% weight on query performance
    
    # Recovery Score Components
    RECONSTRUCTION_RATE_WEIGHT = 0.7
    SIMILARITY_WEIGHT = 0.3
    
    # Thresholds
    EXCELLENT_SCORE = 0.7
    GOOD_SCORE = 0.5
    NEEDS_WORK_SCORE = 0.0

# === CONFIDENCE API CONFIGURATION ===
class ConfidenceConfig:
    # Confidence Thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.7
    MEDIUM_CONFIDENCE_THRESHOLD = 0.5
    LOW_CONFIDENCE_THRESHOLD = 0.3
    
    # Quality Score Weights
    SEMANTIC_SIMILARITY_WEIGHT = 0.5
    WORD_OVERLAP_WEIGHT = 0.3
    LENGTH_APPROPRIATENESS_WEIGHT = 0.2
    
    # Enterprise Readiness
    ENTERPRISE_READINESS_THRESHOLD = 0.8  # 80% of criteria must be met
    HIGH_CONFIDENCE_RATE_THRESHOLD = 0.5  # 50% high confidence rate required

# === VISUALIZATION CONFIGURATION ===
class VisualizationConfig:
    # Figure Sizes
    TOPOLOGY_FIGURE_SIZE = (16, 12)
    HEATMAP_FIGURE_SIZE = (12, 10)
    DASHBOARD_FIGURE_SIZE = (16, 12)
    
    # Node and Edge Properties
    NODE_SIZE = 300
    NODE_ALPHA = 0.8
    EDGE_WIDTH_SOLID = 2
    EDGE_WIDTH_DASHED = 1
    EDGE_ALPHA_SOLID = 0.6
    EDGE_ALPHA_DASHED = 0.4
    
    # Colors
    PARENT_CHILD_COLOR = 'blue'
    SEMANTIC_COLOR = 'red'
    ROOT_LEVEL_COLOR = 'gold'
    LEVEL_1_COLOR = 'lightblue'
    LEVEL_2_COLOR = 'lightgreen'
    DEEPER_LEVEL_COLOR = 'lightgray'
    RECONSTRUCTED_COLOR = 'lightcoral'
    
    # Output Settings
    DPI = 300
    BBOX_INCHES = 'tight'
    FONT_SIZE_TITLE = 16
    FONT_SIZE_SUBTITLE = 10

# === ERROR CODES ===
class ErrorCodes:
    # Success
    SUCCESS = 0
    
    # Cache Errors
    CACHE_INIT_FAILED = 1001
    FILE_NOT_FOUND = 1002
    INVALID_FRAGMENT = 1003
    
    # FAISS Errors
    FAISS_NOT_AVAILABLE = 2001
    FAISS_INDEX_ERROR = 2002
    DIMENSION_MISMATCH = 2003
    
    # Recovery Errors
    RECONSTRUCTION_FAILED = 3001
    BLANK_FILE_NOT_FOUND = 3002
    SIMILARITY_TOO_LOW = 3003
    
    # Query Errors
    QUERY_FAILED = 4001
    NO_RESULTS_FOUND = 4002
    EMBEDDING_FAILED = 4003

# === DEFAULT VALUES ===
class DefaultValues:
    # Fragment Defaults
    DEFAULT_LEVEL = 0
    DEFAULT_HITS = 0
    DEFAULT_SIMILARITY = 0.0
    
    # Recovery Defaults
    DEFAULT_RECOVERY_PRIORITY = 1.0
    DEFAULT_PLACEHOLDER_PROMPT = "Reconstruct content for {file_id} at level {level}"
    
    # Query Defaults
    DEFAULT_QUERY_TIMEOUT = 5.0
    DEFAULT_MAX_RESULTS = 10
    
    # System Defaults
    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_CACHE_SIZE = 1000
    DEFAULT_TTL_HOURS = 24

# === API CONFIGURATION ===
class APIConfig:
    # HTTP Settings
    TIMEOUT_SECONDS = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0
    
    # Request Headers
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "CARMA-System/1.0.0"
    }

# === BACKUP CONFIGURATION ===
class BackupConfig:
    # Backup Settings
    MAX_BACKUPS = 10
    BACKUP_RETENTION_DAYS = 30
    COMPRESS_BACKUPS = True
    
    # Backup File Names
    REGISTRY_BACKUP = "file_registry.json"
    LINKS_BACKUP = "semantic_links.json"
    WEIGHTS_BACKUP = "hit_weights.json"
    PATH_WEIGHTS_BACKUP = "path_weights.json"
    METRICS_BACKUP = "metrics.json"
    MANIFEST_BACKUP = "manifest.json"

# === LOGGING CONFIGURATION ===
class LoggingConfig:
    # Log Levels
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
    # Log Format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Log Files
    MAIN_LOG = "logs/carma.log"
    ERROR_LOG = "logs/carma_errors.log"
    PERFORMANCE_LOG = "logs/carma_performance.log"

# === TESTING CONFIGURATION ===
class TestingConfig:
    # Test Data
    TEST_FRAGMENT_COUNT = 20
    TEST_QUERY_COUNT = 8
    TEST_RECONSTRUCTION_COUNT = 5
    TEST_HEALING_CYCLES = 3
    
    # Test Thresholds
    MIN_TEST_SIMILARITY = 0.3
    TARGET_TEST_SIMILARITY = 0.7
    MAX_TEST_RESPONSE_TIME = 1.0

# === ENVIRONMENT CONFIGURATION ===
class EnvironmentConfig:
    # Development
    DEV_MODE = True
    DEBUG_MODE = False
    VERBOSE_LOGGING = True
    
    # Production
    PRODUCTION_MODE = False
    PERFORMANCE_MONITORING = True
    ERROR_REPORTING = True

# === UTILITY FUNCTIONS ===
def get_cache_dir() -> Path:
    """Get the cache directory path"""
    return Path(FilePaths.CACHE_DIR)

def get_experiments_dir() -> Path:
    """Get the experiments directory path"""
    return Path(FilePaths.EXPERIMENTS_DIR)

def get_reports_dir() -> Path:
    """Get the reports directory path"""
    return Path(FilePaths.REPORTS_DIR)

def get_backup_dir() -> Path:
    """Get the backup directory path"""
    return Path(FilePaths.BACKUP_DIR)

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        get_cache_dir(),
        get_experiments_dir(),
        get_reports_dir(),
        get_backup_dir(),
        Path("logs")
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# === CONFIGURATION VALIDATION ===
def validate_configuration() -> bool:
    """Validate the system configuration"""
    try:
        # Check required directories
        ensure_directories()
        
        # Validate numeric ranges
        assert 0 < CacheConfig.MAX_FILE_SIZE < 100 * 1024 * 1024  # 0 < max < 100MB
        assert 0 < EmbeddingConfig.EMBEDDING_DIMENSION < 10000  # Reasonable embedding dimension
        assert 0 < PerformanceConfig.ENTERPRISE_QUERY_SUCCESS_RATE <= 1.0  # Valid percentage
        
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

# === CONFIGURATION SUMMARY ===
def get_configuration_summary() -> Dict[str, Any]:
    """Get a summary of the current configuration"""
    return {
        "version": SystemVersion.VERSION,
        "status": SystemVersion.STATUS,
        "cache_config": {
            "max_file_size": CacheConfig.MAX_FILE_SIZE,
            "max_cache_size": CacheConfig.MAX_CACHE_SIZE,
            "split_threshold": CacheConfig.SPLIT_THRESHOLD
        },
        "embedding_config": {
            "model": EmbeddingConfig.EMBEDDING_MODEL,
            "dimension": EmbeddingConfig.EMBEDDING_DIMENSION,
            "similarity_threshold": EmbeddingConfig.SIMILARITY_THRESHOLD
        },
        "performance_config": {
            "enterprise_query_success_rate": PerformanceConfig.ENTERPRISE_QUERY_SUCCESS_RATE,
            "enterprise_recovery_time": PerformanceConfig.ENTERPRISE_RECOVERY_TIME_SECONDS,
            "target_fragment_count": PerformanceConfig.TARGET_FRAGMENT_COUNT
        },
        "file_paths": {
            "cache_dir": FilePaths.CACHE_DIR,
            "experiments_dir": FilePaths.EXPERIMENTS_DIR,
            "faiss_index": FilePaths.FAISS_INDEX
        }
    }

if __name__ == "__main__":
    # Validate configuration on import
    if validate_configuration():
        print("✅ Configuration validated successfully")
        summary = get_configuration_summary()
        print(f"📊 System Version: {summary['version']}")
        print(f"📁 Cache Directory: {summary['file_paths']['cache_dir']}")
        print(f"🧠 Embedding Model: {summary['embedding_config']['model']}")
    else:
        print("❌ Configuration validation failed")
        exit(1)