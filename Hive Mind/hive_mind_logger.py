#!/usr/bin/env python3
"""
HIVE MIND LOGGING & ERROR HANDLING SYSTEM
Comprehensive logging, debugging, and robust error handling for AIOS
"""

import logging
import traceback
import json
import os
import sys
import time
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import functools
import threading
import queue
import signal
import atexit

class HiveMindLogger:
    """Centralized logging and error handling system"""
    
    def __init__(self, log_dir: str = "../log/hive_mind"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create temp directory for recovery files
        self.temp_dir = Path(tempfile.gettempdir()) / "hive_mind_recovery"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Error recovery queue
        self.error_queue = queue.Queue()
        self.recovery_thread = None
        self.shutdown_flag = threading.Event()
        
        # Setup logging
        self._setup_logging()
        
        # Register cleanup handlers
        atexit.register(self._cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Start recovery thread
        self._start_recovery_thread()
        
        self.log("SYSTEM", "HiveMindLogger initialized", "INFO")
    
    def _setup_logging(self):
        """Setup comprehensive logging system"""
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(component)-15s | %(function)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Main logger
        self.logger = logging.getLogger('hive_mind')
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler (simple)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (detailed)
        log_file = self.log_dir / f"hive_mind_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)
        
        # Error handler (critical errors only)
        error_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(error_handler)
        
        # Debug handler (very detailed)
        debug_file = self.log_dir / f"debug_{datetime.now().strftime('%Y%m%d')}.log"
        debug_handler = logging.FileHandler(debug_file, encoding='utf-8')
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(debug_handler)
    
    def _start_recovery_thread(self):
        """Start background recovery thread"""
        self.recovery_thread = threading.Thread(target=self._recovery_worker, daemon=True)
        self.recovery_thread.start()
    
    def _recovery_worker(self):
        """Background worker for error recovery"""
        while not self.shutdown_flag.is_set():
            try:
                error_data = self.error_queue.get(timeout=1.0)
                self._process_error_recovery(error_data)
            except queue.Empty:
                continue
            except Exception as e:
                self.log("RECOVERY", f"Recovery worker error: {e}", "CRITICAL")
    
    def _process_error_recovery(self, error_data: Dict[str, Any]):
        """Process error recovery actions"""
        try:
            component = error_data.get('component', 'UNKNOWN')
            error_type = error_data.get('error_type', 'UNKNOWN')
            recovery_action = error_data.get('recovery_action', 'LOG_ONLY')
            
            self.log("RECOVERY", f"Processing {error_type} error in {component}", "INFO")
            
            if recovery_action == 'RESTART_COMPONENT':
                self._restart_component(component, error_data)
            elif recovery_action == 'CLEAR_CACHE':
                self._clear_component_cache(component, error_data)
            elif recovery_action == 'FALLBACK_MODE':
                self._enable_fallback_mode(component, error_data)
            elif recovery_action == 'SAVE_STATE':
                self._save_recovery_state(component, error_data)
            
            self.log("RECOVERY", f"Recovery completed for {component}", "INFO")
            
        except Exception as e:
            self.log("RECOVERY", f"Recovery processing failed: {e}", "CRITICAL")
    
    def _restart_component(self, component: str, error_data: Dict[str, Any]):
        """Restart a component after error"""
        self.log("RECOVERY", f"Restarting component: {component}", "WARNING")
        # Implementation would depend on component type
        pass
    
    def _clear_component_cache(self, component: str, error_data: Dict[str, Any]):
        """Clear component cache after error"""
        self.log("RECOVERY", f"Clearing cache for component: {component}", "WARNING")
        # Implementation would clear relevant caches
        pass
    
    def _enable_fallback_mode(self, component: str, error_data: Dict[str, Any]):
        """Enable fallback mode for component"""
        self.log("RECOVERY", f"Enabling fallback mode for component: {component}", "WARNING")
        # Implementation would enable simplified mode
        pass
    
    def _save_recovery_state(self, component: str, error_data: Dict[str, Any]):
        """Save recovery state to temp file"""
        recovery_file = self.temp_dir / f"{component}_recovery_{int(time.time())}.json"
        try:
            with open(recovery_file, 'w') as f:
                json.dump(error_data, f, indent=2, default=str)
            self.log("RECOVERY", f"Recovery state saved: {recovery_file}", "INFO")
        except Exception as e:
            self.log("RECOVERY", f"Failed to save recovery state: {e}", "ERROR")
    
    def log(self, component: str, message: str, level: str = "INFO", extra_data: Optional[Dict] = None):
        """Centralized logging method"""
        try:
            # Add extra data to message if provided
            if extra_data:
                message += f" | Extra: {json.dumps(extra_data, default=str)}"
            
            # Log with component info
            extra = {'component': component, 'function': self._get_caller_function()}
            
            if level.upper() == "DEBUG":
                self.logger.debug(message, extra=extra)
            elif level.upper() == "INFO":
                self.logger.info(message, extra=extra)
            elif level.upper() == "WARNING":
                self.logger.warning(message, extra=extra)
            elif level.upper() == "ERROR":
                self.logger.error(message, extra=extra)
            elif level.upper() == "CRITICAL":
                self.logger.critical(message, extra=extra)
            else:
                self.logger.info(message, extra=extra)
                
        except Exception as e:
            # Fallback logging if main system fails
            print(f"LOGGING ERROR: {e} | Original: {message}")
    
    def _get_caller_function(self) -> str:
        """Get the calling function name"""
        try:
            return traceback.extract_stack()[-3].name
        except:
            return "UNKNOWN"
    
    def error_handler(self, component: str, error_type: str = "GENERAL", 
                     recovery_action: str = "LOG_ONLY", auto_recover: bool = True):
        """Decorator for comprehensive error handling"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                self.log(component, f"Starting {func.__name__}", "DEBUG")
                
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    self.log(component, f"Completed {func.__name__} in {duration:.3f}s", "DEBUG")
                    return result
                    
                except Exception as e:
                    duration = time.time() - start_time
                    error_data = {
                        'component': component,
                        'function': func.__name__,
                        'error_type': error_type,
                        'error_message': str(e),
                        'traceback': traceback.format_exc(),
                        'args': str(args)[:200],  # Truncate long args
                        'kwargs': str(kwargs)[:200],
                        'duration': duration,
                        'timestamp': datetime.now().isoformat(),
                        'recovery_action': recovery_action
                    }
                    
                    self.log(component, f"ERROR in {func.__name__}: {e}", "ERROR", error_data)
                    
                    if auto_recover:
                        self.error_queue.put(error_data)
                    
                    # Return safe fallback based on error type
                    return self._get_fallback_result(func.__name__, error_type, e)
            
            return wrapper
        return decorator
    
    def _get_fallback_result(self, function_name: str, error_type: str, error: Exception):
        """Get safe fallback result based on function type"""
        if "test" in function_name.lower():
            return {"error": True, "message": str(error), "fallback": True}
        elif "query" in function_name.lower() or "response" in function_name.lower():
            return None
        elif "cache" in function_name.lower():
            return {}
        elif "save" in function_name.lower() or "load" in function_name.lower():
            return False
        else:
            return None
    
    def safe_execute(self, func, *args, component: str = "UNKNOWN", 
                    max_retries: int = 3, **kwargs):
        """Safely execute a function with retries"""
        for attempt in range(max_retries):
            try:
                self.log(component, f"Attempt {attempt + 1}/{max_retries}: {func.__name__}", "DEBUG")
                result = func(*args, **kwargs)
                if attempt > 0:
                    self.log(component, f"Success on attempt {attempt + 1}", "INFO")
                return result
            except Exception as e:
                self.log(component, f"Attempt {attempt + 1} failed: {e}", "WARNING")
                if attempt == max_retries - 1:
                    self.log(component, f"All {max_retries} attempts failed", "ERROR")
                    return self._get_fallback_result(func.__name__, "RETRY_EXHAUSTED", e)
                time.sleep(0.5 * (attempt + 1))  # Exponential backoff
    
    def create_temp_file(self, prefix: str = "hive_mind", suffix: str = ".tmp") -> Path:
        """Create a temporary file for recovery"""
        temp_file = self.temp_dir / f"{prefix}_{int(time.time())}{suffix}"
        self.log("TEMP", f"Created temp file: {temp_file}", "DEBUG")
        return temp_file
    
    def save_critical_state(self, component: str, state_data: Dict[str, Any]) -> Path:
        """Save critical state for recovery"""
        state_file = self.create_temp_file(f"{component}_state", ".json")
        try:
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=2, default=str)
            self.log("STATE", f"Critical state saved: {state_file}", "INFO")
            return state_file
        except Exception as e:
            self.log("STATE", f"Failed to save critical state: {e}", "ERROR")
            return None
    
    def load_critical_state(self, state_file: Path) -> Optional[Dict[str, Any]]:
        """Load critical state for recovery"""
        try:
            if state_file.exists():
                with open(state_file, 'r') as f:
                    state_data = json.load(f)
                self.log("STATE", f"Critical state loaded: {state_file}", "INFO")
                return state_data
        except Exception as e:
            self.log("STATE", f"Failed to load critical state: {e}", "ERROR")
        return None
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.log("SYSTEM", f"Received signal {signum}, initiating graceful shutdown", "WARNING")
        self.shutdown_flag.set()
        self._cleanup()
        sys.exit(0)
    
    def _cleanup(self):
        """Cleanup resources on shutdown"""
        try:
            self.log("SYSTEM", "Starting cleanup process", "INFO")
            self.shutdown_flag.set()
            
            # Wait for recovery thread to finish
            if self.recovery_thread and self.recovery_thread.is_alive():
                self.recovery_thread.join(timeout=5.0)
            
            # Clean up old temp files (older than 24 hours)
            self._cleanup_old_temp_files()
            
            self.log("SYSTEM", "Cleanup completed", "INFO")
        except Exception as e:
            print(f"CLEANUP ERROR: {e}")
    
    def _cleanup_old_temp_files(self):
        """Clean up old temporary files"""
        try:
            current_time = time.time()
            for temp_file in self.temp_dir.glob("*"):
                if temp_file.is_file():
                    file_age = current_time - temp_file.stat().st_mtime
                    if file_age > 86400:  # 24 hours
                        temp_file.unlink()
                        self.log("CLEANUP", f"Removed old temp file: {temp_file}", "DEBUG")
        except Exception as e:
            self.log("CLEANUP", f"Error cleaning temp files: {e}", "WARNING")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "log_directory": str(self.log_dir),
            "temp_directory": str(self.temp_dir),
            "recovery_queue_size": self.error_queue.qsize(),
            "recovery_thread_alive": self.recovery_thread.is_alive() if self.recovery_thread else False,
            "shutdown_flag_set": self.shutdown_flag.is_set(),
            "temp_files_count": len(list(self.temp_dir.glob("*"))),
            "log_files": [str(f) for f in self.log_dir.glob("*.log")]
        }

# Global logger instance
hive_logger = HiveMindLogger()

# Convenience functions
def log(component: str, message: str, level: str = "INFO", extra_data: Optional[Dict] = None):
    """Convenience function for logging"""
    hive_logger.log(component, message, level, extra_data)

def error_handler(component: str, error_type: str = "GENERAL", 
                recovery_action: str = "LOG_ONLY", auto_recover: bool = True):
    """Convenience function for error handling decorator"""
    return hive_logger.error_handler(component, error_type, recovery_action, auto_recover)

def safe_execute(func, *args, component: str = "UNKNOWN", max_retries: int = 3, **kwargs):
    """Convenience function for safe execution"""
    return hive_logger.safe_execute(func, *args, component=component, max_retries=max_retries, **kwargs)
