"""
CARMA Chain Logic for Serial API Processing
Ensures all API calls are processed in serial order, not parallel
"""

import time
import threading
import queue
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

class ChainStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ChainOperation:
    """Represents a single operation in the chain"""
    operation_id: str
    user_id: str
    operation_type: str
    data: Dict[str, Any]
    timestamp: float
    status: ChainStatus = ChainStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

class CARMAChainProcessor:
    """Serial chain processor for CARMA API operations"""
    
    def __init__(self, max_chain_length: int = 1000):
        self.max_chain_length = max_chain_length
        self.chain_queue = queue.Queue(maxsize=max_chain_length)
        self.processing_lock = threading.Lock()
        self.chain_history = []
        self.active_operations = {}
        self.operation_handlers = {}
        self.is_processing = False
        self.processing_thread = None
        
        # Chain statistics
        self.stats = {
            "total_operations": 0,
            "completed_operations": 0,
            "failed_operations": 0,
            "cancelled_operations": 0,
            "average_processing_time": 0.0,
            "chain_length": 0
        }
    
    def register_operation_handler(self, operation_type: str, handler: Callable):
        """Register a handler for a specific operation type"""
        self.operation_handlers[operation_type] = handler
    
    def add_operation(self, user_id: str, operation_type: str, data: Dict[str, Any]) -> str:
        """Add an operation to the chain"""
        operation_id = f"{user_id}_{operation_type}_{int(time.time() * 1000)}"
        
        operation = ChainOperation(
            operation_id=operation_id,
            user_id=user_id,
            operation_type=operation_type,
            data=data,
            timestamp=time.time()
        )
        
        try:
            self.chain_queue.put(operation, timeout=1.0)
            self.active_operations[operation_id] = operation
            self.stats["total_operations"] += 1
            self.stats["chain_length"] = self.chain_queue.qsize()
            
            # Start processing if not already running
            if not self.is_processing:
                self.start_processing()
            
            return operation_id
            
        except queue.Full:
            raise Exception("Chain queue is full - system overloaded")
    
    def start_processing(self):
        """Start the chain processing thread"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.processing_thread = threading.Thread(target=self._process_chain, daemon=True)
        self.processing_thread.start()
    
    def stop_processing(self):
        """Stop the chain processing thread"""
        self.is_processing = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5.0)
    
    def _process_chain(self):
        """Main chain processing loop - SERIAL ONLY"""
        while self.is_processing:
            try:
                # Get next operation from queue (blocks until available)
                operation = self.chain_queue.get(timeout=1.0)
                
                # Process the operation
                self._process_operation(operation)
                
                # Mark task as done
                self.chain_queue.task_done()
                
            except queue.Empty:
                # No operations in queue, continue
                continue
            except Exception as e:
                print(f"Error in chain processing: {e}")
                continue
    
    def _process_operation(self, operation: ChainOperation):
        """Process a single operation in the chain"""
        start_time = time.time()
        
        try:
            # Update operation status
            operation.status = ChainStatus.PROCESSING
            
            # Get handler for operation type
            handler = self.operation_handlers.get(operation.operation_type)
            if not handler:
                raise Exception(f"No handler registered for operation type: {operation.operation_type}")
            
            # Execute the operation
            result = handler(operation.user_id, operation.data)
            
            # Update operation with result
            operation.result = result
            operation.status = ChainStatus.COMPLETED
            self.stats["completed_operations"] += 1
            
        except Exception as e:
            # Handle operation failure
            operation.error = str(e)
            operation.retry_count += 1
            
            if operation.retry_count < operation.max_retries:
                # Retry the operation
                operation.status = ChainStatus.PENDING
                self.chain_queue.put(operation)
            else:
                # Max retries exceeded
                operation.status = ChainStatus.FAILED
                self.stats["failed_operations"] += 1
        
        finally:
            # Update processing time
            processing_time = time.time() - start_time
            self._update_average_processing_time(processing_time)
            
            # Remove from active operations
            if operation.operation_id in self.active_operations:
                del self.active_operations[operation.operation_id]
            
            # Add to history
            self.chain_history.append(operation)
            
            # Keep history size manageable
            if len(self.chain_history) > self.max_chain_length * 2:
                self.chain_history = self.chain_history[-self.max_chain_length:]
    
    def _update_average_processing_time(self, processing_time: float):
        """Update average processing time"""
        total_ops = self.stats["completed_operations"] + self.stats["failed_operations"]
        if total_ops > 0:
            current_avg = self.stats["average_processing_time"]
            self.stats["average_processing_time"] = ((current_avg * (total_ops - 1)) + processing_time) / total_ops
    
    def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific operation"""
        if operation_id in self.active_operations:
            operation = self.active_operations[operation_id]
        else:
            # Look in history
            operation = next((op for op in self.chain_history if op.operation_id == operation_id), None)
        
        if not operation:
            return None
        
        return {
            "operation_id": operation.operation_id,
            "user_id": operation.user_id,
            "operation_type": operation.operation_type,
            "status": operation.status.value,
            "timestamp": operation.timestamp,
            "result": operation.result,
            "error": operation.error,
            "retry_count": operation.retry_count
        }
    
    def cancel_operation(self, operation_id: str) -> bool:
        """Cancel a pending operation"""
        if operation_id in self.active_operations:
            operation = self.active_operations[operation_id]
            if operation.status == ChainStatus.PENDING:
                operation.status = ChainStatus.CANCELLED
                self.stats["cancelled_operations"] += 1
                return True
        return False
    
    def get_chain_status(self) -> Dict[str, Any]:
        """Get current chain status"""
        return {
            "is_processing": self.is_processing,
            "queue_size": self.chain_queue.qsize(),
            "active_operations": len(self.active_operations),
            "stats": self.stats.copy()
        }
    
    def get_user_operations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all operations for a specific user"""
        user_ops = []
        
        # Check active operations
        for operation in self.active_operations.values():
            if operation.user_id == user_id:
                user_ops.append(self.get_operation_status(operation.operation_id))
        
        # Check history
        for operation in self.chain_history:
            if operation.user_id == user_id:
                user_ops.append(self.get_operation_status(operation.operation_id))
        
        return user_ops
    
    def clear_chain(self):
        """Clear the chain queue and history"""
        with self.processing_lock:
            # Clear queue
            while not self.chain_queue.empty():
                try:
                    self.chain_queue.get_nowait()
                except queue.Empty:
                    break
            
            # Clear active operations
            self.active_operations.clear()
            
            # Clear history
            self.chain_history.clear()
            
            # Reset stats
            self.stats = {
                "total_operations": 0,
                "completed_operations": 0,
                "failed_operations": 0,
                "cancelled_operations": 0,
                "average_processing_time": 0.0,
                "chain_length": 0
            }

def test_carma_chain_logic():
    """Test the CARMA chain logic"""
    print("🔗 Testing CARMA Chain Logic")
    print("=" * 50)
    
    # Create chain processor
    chain = CARMAChainProcessor(max_chain_length=100)
    
    # Register operation handlers
    def generate_key_handler(user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for generate_key operations"""
        time.sleep(0.1)  # Simulate processing time
        return {
            "success": True,
            "api_key": f"carma_{user_id}_{int(time.time())}",
            "user_id": user_id
        }
    
    def validate_key_handler(user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for validate_key operations"""
        time.sleep(0.05)  # Simulate processing time
        api_key = data.get("api_key", "")
        return {
            "success": True,
            "valid": api_key.startswith("carma_"),
            "user_id": user_id
        }
    
    chain.register_operation_handler("generate_key", generate_key_handler)
    chain.register_operation_handler("validate_key", validate_key_handler)
    
    # Test 1: Add operations
    print("\n📝 Adding Operations to Chain:")
    operation_ids = []
    
    for i in range(5):
        op_id = chain.add_operation(f"user_{i}", "generate_key", {"permissions": "admin"})
        operation_ids.append(op_id)
        print(f"   Added operation {i+1}: {op_id}")
    
    # Test 2: Check chain status
    print("\n📊 Chain Status:")
    status = chain.get_chain_status()
    for key, value in status.items():
        if key != "stats":
            print(f"   {key}: {value}")
    
    # Test 3: Wait for processing
    print("\n⏳ Waiting for Processing...")
    time.sleep(2)  # Wait for operations to complete
    
    # Test 4: Check operation statuses
    print("\n✅ Operation Statuses:")
    for op_id in operation_ids:
        op_status = chain.get_operation_status(op_id)
        if op_status:
            print(f"   {op_id}: {op_status['status']} - {op_status.get('result', {}).get('api_key', 'N/A')}")
    
    # Test 5: Add more operations
    print("\n📝 Adding More Operations:")
    for i in range(3):
        op_id = chain.add_operation(f"user_{i+5}", "validate_key", {"api_key": f"carma_user_{i+5}_{int(time.time())}"})
        operation_ids.append(op_id)
        print(f"   Added validation operation {i+1}: {op_id}")
    
    # Test 6: Final status
    print("\n📊 Final Chain Status:")
    final_status = chain.get_chain_status()
    for key, value in final_status.items():
        if key != "stats":
            print(f"   {key}: {value}")
    
    print("\n   Statistics:")
    for key, value in final_status["stats"].items():
        print(f"      {key}: {value}")
    
    # Test 7: User operations
    print("\n👤 User Operations:")
    user_ops = chain.get_user_operations("user_0")
    print(f"   user_0 operations: {len(user_ops)}")
    for op in user_ops:
        print(f"      {op['operation_type']}: {op['status']}")
    
    # Stop processing
    chain.stop_processing()
    
    print("\n🎯 CARMA Chain Logic Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_carma_chain_logic()
