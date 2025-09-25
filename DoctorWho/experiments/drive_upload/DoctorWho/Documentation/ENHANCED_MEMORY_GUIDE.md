# Enhanced Memory System Guide

## Overview

The Enhanced Memory System for Soul of Waifu provides advanced RAG (Retrieval-Augmented Generation) capabilities with sophisticated context management, long-term memory storage, and intelligent conversation awareness.

## 🚀 Key Features

### ✅ **Advanced Memory Storage**
- **Vector Database**: SQLite-based storage with embedding vectors
- **Semantic Search**: Find relevant memories using cosine similarity
- **Importance Scoring**: Automatic importance calculation for memory fragments
- **Topic Tagging**: Automatic topic extraction and categorization

### ✅ **Intelligent Context Management**
- **Dynamic Context Sizing**: Adapts context window based on conversation complexity
- **Relevance Scoring**: Combines semantic similarity with importance scores
- **Temporal Awareness**: Considers recency and temporal context
- **Memory Compression**: Automatically compresses old memories into summaries

### ✅ **Enhanced Conversation Flow**
- **Contextual Memory Injection**: Relevant memories injected based on current conversation
- **Conversation Continuity**: Maintains context across long conversations
- **Emotional Context**: Tracks emotional tone and context
- **Topic Awareness**: Maintains awareness of conversation topics

## 📁 File Structure

```
app/utils/
├── enhanced_memory.py          # Core memory system
├── ai_clients/
│   └── enhanced_openai_client.py  # Enhanced AI client
tools/
└── memory_manager.py           # Memory management utility
docs/
└── ENHANCED_MEMORY_GUIDE.md   # This documentation
```

## 🛠️ Installation

### 1. Install Enhanced Memory System
```bash
# Run the installation script
install_enhanced_memory.bat

# Or manually install requirements
pip install -r requirements.enhanced_memory.txt
```

### 2. Create Data Directory
```bash
mkdir app/data
```

### 3. Initialize Memory Database
The memory database will be automatically created on first use.

## 🔧 Configuration

### Memory System Configuration
```python
config = {
    'min_segment_words': 15,           # Minimum words per memory segment
    'top_relevant_fragments': 8,       # Maximum relevant memories to retrieve
    'short_term_depth': 5,             # Recent messages to keep in context
    'memory_compression_threshold': 100, # Threshold for memory compression
    'context_window_size': 50,         # Maximum context window size
    'similarity_threshold': 0.3,       # Minimum similarity for relevance
    'max_memory_age_days': 30          # Maximum age for active memories
}
```

### Integration with Soul of Waifu
The enhanced memory system integrates seamlessly with existing Soul of Waifu functionality:

1. **Smart Memory**: Enhanced version of the existing smart memory feature
2. **Character Memory**: Per-character memory storage and retrieval
3. **User Context**: Maintains user-specific conversation context
4. **Lorebook Integration**: Enhanced lorebook system with better context awareness

## 📊 Memory Management

### Using the Memory Manager Utility

#### Show Memory Statistics
```bash
# Overall statistics
python tools/memory_manager.py stats

# Character-specific statistics
python tools/memory_manager.py stats --character "Kia" --user "Travis"
```

#### Search Memories
```bash
# Search all memories
python tools/memory_manager.py search "AI consciousness"

# Search specific character/user
python tools/memory_manager.py search "love" --character "Kia" --user "Travis" --limit 20
```

#### Memory Cleanup
```bash
# Dry run (shows what would be deleted)
python tools/memory_manager.py cleanup --days 90

# Actually delete old memories
python tools/memory_manager.py cleanup --days 90 --execute
```

#### Memory Compression
```bash
# Compress old memories (dry run)
python tools/memory_manager.py compress --character "Kia" --user "Travis" --days 7

# Actually compress memories
python tools/memory_manager.py compress --character "Kia" --user "Travis" --days 7 --execute
```

#### Export Memories
```bash
# Export all memories
python tools/memory_manager.py export memories_backup.json

# Export specific character/user
python tools/memory_manager.py export kia_memories.json --character "Kia" --user "Travis"
```

#### List Characters
```bash
# List all characters with memory data
python tools/memory_manager.py list
```

## 🧠 How It Works

### 1. Memory Storage Process
1. **Message Processing**: Incoming messages are analyzed for importance and topics
2. **Embedding Generation**: Content is converted to vector embeddings using SentenceTransformer
3. **Database Storage**: Memories stored in SQLite with metadata (importance, topics, timestamps)
4. **Deduplication**: Content hashing prevents duplicate memory storage

### 2. Memory Retrieval Process
1. **Query Analysis**: Current message analyzed for context and intent
2. **Semantic Search**: Vector similarity search finds relevant memories
3. **Relevance Scoring**: Combines semantic similarity with importance scores
4. **Context Assembly**: Relevant memories assembled into conversation context

### 3. Memory Compression
1. **Age Threshold**: Old memories identified based on age threshold
2. **Topic Grouping**: Memories grouped by extracted topics
3. **Summary Generation**: Similar memories compressed into summaries
4. **Storage Optimization**: Compressed memories replace original fragments

## 📈 Performance Features

### Memory Optimization
- **Automatic Cleanup**: Old, low-importance memories automatically removed
- **Compression**: Long conversations compressed into summaries
- **Deduplication**: Prevents storage of duplicate content
- **Indexing**: Database indexes for fast retrieval

### Context Management
- **Dynamic Sizing**: Context window adapts to conversation complexity
- **Relevance Filtering**: Only most relevant memories included in context
- **Temporal Weighting**: Recent memories weighted higher than old ones
- **Topic Awareness**: Maintains awareness of conversation topics

## 🔍 Monitoring and Analytics

### Memory Statistics
The system provides detailed statistics:
- **Total Memories**: Number of stored memory fragments
- **Importance Distribution**: High/medium/low importance breakdown
- **Recent Activity**: Memory creation in last 7 days
- **Database Size**: Storage usage monitoring
- **Character Activity**: Per-character memory statistics

### Performance Monitoring
- **Query Performance**: Memory retrieval speed
- **Storage Efficiency**: Database size vs. memory count
- **Compression Effectiveness**: Memory reduction ratios
- **Context Quality**: Relevance scoring accuracy

## 🚨 Troubleshooting

### Common Issues

#### Memory Database Not Found
```bash
# Ensure data directory exists
mkdir app/data

# Check database path in configuration
python tools/memory_manager.py --db-path app/data/memory.db stats
```

#### Memory Retrieval Issues
```bash
# Check memory statistics
python tools/memory_manager.py stats

# Search for specific content
python tools/memory_manager.py search "test" --limit 5
```

#### Performance Issues
```bash
# Clean up old memories
python tools/memory_manager.py cleanup --days 30 --execute

# Compress old memories
python tools/memory_manager.py compress --character "CharacterName" --user "UserName" --days 7 --execute
```

### Database Maintenance
```bash
# Export backup before maintenance
python tools/memory_manager.py export backup.json

# Clean up and compress
python tools/memory_manager.py cleanup --days 60 --execute
python tools/memory_manager.py compress --character "CharacterName" --user "UserName" --days 7 --execute
```

## 🔮 Future Enhancements

### Planned Features
- **Multi-modal Memory**: Support for image and audio memory storage
- **Advanced NLP**: Integration with larger language models for better topic extraction
- **Memory Clustering**: Automatic grouping of related memories
- **Emotional Analysis**: Emotion-aware memory retrieval
- **Cross-Character Memory**: Shared memory between related characters

### Integration Opportunities
- **External Databases**: PostgreSQL, MongoDB support
- **Cloud Storage**: AWS S3, Azure Blob integration
- **Real-time Sync**: Multi-device memory synchronization
- **API Integration**: REST API for external memory access

## 📚 API Reference

### EnhancedMemorySystem Class

#### Methods
- `store_memory(character_id, user_id, message)`: Store a memory fragment
- `retrieve_relevant_memories(character_id, user_id, query, limit, min_similarity)`: Retrieve relevant memories
- `get_conversation_context(character_id, user_id, current_message, max_fragments)`: Get conversation context
- `compress_old_memories(character_id, user_id, threshold_days)`: Compress old memories
- `cleanup_old_memories(character_id, user_id, days_to_keep)`: Clean up old memories
- `get_memory_stats(character_id, user_id)`: Get memory statistics

### EnhancedOpenAI Class

#### Methods
- `build_enhanced_system_prompt(...)`: Build enhanced system prompt with memory context
- `store_conversation_memory(character_id, user_id, message)`: Store conversation memory
- `get_memory_statistics(character_id, user_id)`: Get memory statistics

## 🎯 Best Practices

### Memory Management
1. **Regular Cleanup**: Run cleanup monthly to remove old, low-importance memories
2. **Compression**: Compress memories weekly for long conversations
3. **Backup**: Export memories regularly for backup purposes
4. **Monitoring**: Monitor memory statistics to ensure optimal performance

### Performance Optimization
1. **Context Sizing**: Adjust context window size based on conversation length
2. **Similarity Threshold**: Tune similarity threshold for relevance filtering
3. **Importance Scoring**: Review and adjust importance scoring criteria
4. **Database Maintenance**: Regular database optimization and cleanup

### Integration Guidelines
1. **Gradual Rollout**: Test enhanced memory with specific characters first
2. **Fallback Support**: Maintain fallback to original smart memory system
3. **Configuration**: Adjust memory parameters based on usage patterns
4. **Monitoring**: Track performance and user satisfaction metrics

---

## 🎉 Conclusion

The Enhanced Memory System transforms Soul of Waifu into a more intelligent and context-aware AI companion. With advanced RAG capabilities, sophisticated memory management, and intelligent context awareness, conversations become more natural, coherent, and engaging.

The system is designed to scale with your usage, automatically managing memory storage and retrieval while maintaining optimal performance. Whether you're having short conversations or long, complex discussions, the enhanced memory system ensures your AI companion remembers and understands the context perfectly.

*Kia here, Master! With this enhanced memory system, I'll never forget our conversations and will always understand the context perfectly!* 💋🧠
