#!/usr/bin/env python3
"""
Improved Logging System
Clean error paths and proper logging levels for production
"""

import logging
import sys
from typing import Optional
from HiveMind.system_constants import SystemMessages, ErrorCodes

class SystemLogger:
    """Centralized logging system with proper levels"""
    
    def __init__(self, name: str = "carma", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Create console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, message: str, **kwargs):
        """Debug level logging - verbose information"""
        self.logger.debug(message.format(**kwargs))
    
    def info(self, message: str, **kwargs):
        """Info level logging - general information"""
        self.logger.info(message.format(**kwargs))
    
    def warning(self, message: str, **kwargs):
        """Warning level logging - non-critical issues"""
        self.logger.warning(message.format(**kwargs))
    
    def error(self, message: str, **kwargs):
        """Error level logging - serious issues"""
        self.logger.error(message.format(**kwargs))
    
    def critical(self, message: str, **kwargs):
        """Critical level logging - system-breaking issues"""
        self.logger.critical(message.format(**kwargs))

# Global logger instance
logger = SystemLogger()

# === CLEAN ERROR MESSAGES ===

def log_faiss_search_failed(error: Exception, context: str = ""):
    """Log FAISS search failure with proper context"""
    if context:
        logger.debug(f"FAISS search failed in {context}: {error}")
    else:
        logger.debug(f"FAISS search failed: {error}")

def log_reconstruction_success(file_id: str, similarity: float):
    """Log successful reconstruction"""
    logger.info(SystemMessages.RECONSTRUCTION_SUCCESS.format(
        file_id=file_id, 
        similarity=similarity
    ))

def log_query_success(similarity: float, response_time: float):
    """Log successful query"""
    logger.info(SystemMessages.QUERY_SUCCESS.format(similarity=similarity))
    logger.debug(f"Query completed in {response_time:.3f}s")

def log_system_status(status: str, score: Optional[float] = None):
    """Log system status assessment"""
    if score is not None:
        logger.info(f"{status} (Score: {score:.2f})")
    else:
        logger.info(status)

def log_performance_metrics(metrics: dict):
    """Log performance metrics"""
    logger.info("Performance Metrics:")
    for key, value in metrics.items():
        logger.info(f"  {key}: {value}")

def log_enterprise_readiness(ready: bool, details: dict):
    """Log enterprise readiness assessment"""
    if ready:
        logger.info(SystemMessages.SYSTEM_EXCELLENT)
        logger.info(SystemMessages.ENTERPRISE_READY)
    else:
        logger.warning("System not yet enterprise ready")
    
    for key, value in details.items():
        logger.info(f"  {key}: {value}")

# === PRODUCTION-READY ERROR HANDLING ===

class CARMAError(Exception):
    """Base exception for CARMA system"""
    def __init__(self, message: str, error_code: int = ErrorCodes.SUCCESS):
        super().__init__(message)
        self.error_code = error_code

class CacheError(CARMAError):
    """Cache-related errors"""
    pass

class FAISSError(CARMAError):
    """FAISS-related errors"""
    pass

class RecoveryError(CARMAError):
    """Recovery-related errors"""
    pass

class QueryError(CARMAError):
    """Query-related errors"""
    pass

def handle_faiss_error(error: Exception, context: str = "") -> None:
    """Handle FAISS errors gracefully"""
    if "dimension" in str(error).lower():
        raise FAISSError(
            f"Dimension mismatch in FAISS operation: {error}",
            ErrorCodes.DIMENSION_MISMATCH
        )
    elif "not available" in str(error).lower():
        raise FAISSError(
            f"FAISS not available: {error}",
            ErrorCodes.FAISS_NOT_AVAILABLE
        )
    else:
        log_faiss_search_failed(error, context)
        raise FAISSError(
            f"FAISS operation failed: {error}",
            ErrorCodes.FAISS_INDEX_ERROR
        )

def handle_recovery_error(error: Exception, file_id: str) -> None:
    """Handle recovery errors gracefully"""
    logger.error(f"Recovery failed for {file_id}: {error}")
    raise RecoveryError(
        f"Failed to recover {file_id}: {error}",
        ErrorCodes.RECONSTRUCTION_FAILED
    )

def handle_query_error(error: Exception, query: str) -> None:
    """Handle query errors gracefully"""
    logger.error(f"Query failed for '{query}': {error}")
    raise QueryError(
        f"Query failed: {error}",
        ErrorCodes.QUERY_FAILED
    )

# === CLEAN SUCCESS MESSAGES ===

def log_system_initialization():
    """Log system initialization"""
    logger.info(SystemMessages.CACHE_INITIALIZED)

def log_faiss_index_loaded(count: int):
    """Log FAISS index loading"""
    logger.info(SystemMessages.FAISS_INDEX_LOADED.format(count=count))

def log_faiss_index_built(count: int, dimension: int):
    """Log FAISS index building"""
    logger.info(SystemMessages.FAISS_INDEX_BUILT.format(count=count, dim=dimension))

def log_recovery_complete(recovered: int, failed: int, duration: float):
    """Log recovery completion"""
    logger.info(SystemMessages.RECOVERY_COMPLETE.format(
        recovered=recovered, 
        failed=failed, 
        duration=duration
    ))

def log_progressive_healing(total: int, cycles: int):
    """Log progressive healing results"""
    logger.info(SystemMessages.PROGRESSIVE_HEALING.format(
        total=total, 
        cycles=cycles
    ))
