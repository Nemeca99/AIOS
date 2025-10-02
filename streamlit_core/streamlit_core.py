#!/usr/bin/env python3
"""
STREAMLIT CORE SYSTEM
Self-contained UI system for AIOS Clean
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

import streamlit as st
import json
import pickle
from datetime import datetime
from typing import Dict, List, Optional, Any

class StreamlitCore:
    """
    Self-contained Streamlit UI system for AIOS Clean.
    Handles all UI components and user interactions.
    """
    
    def __init__(self):
        """Initialize the Streamlit core system."""
        self.state_file = Path("streamlit_state.pkl")
        self.heartbeat_file = Path("meditation_heartbeat.json")
        self.session_file = Path("meditation_session.json")
        
        print(f"🎨 Streamlit Core System Initialized")
        print(f"   State File: {self.state_file}")
        print(f"   Heartbeat File: {self.heartbeat_file}")
    
    def load_persistent_state(self) -> Dict[str, Any]:
        """Load persistent state from file with memory leak protection."""
        if not self.state_file.exists():
            return {}
        
        try:
            # Check file size to prevent loading huge files
            file_size = self.state_file.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                print(f"⚠️ State file too large ({file_size} bytes), clearing it")
                self.state_file.unlink()
                return {}

            with open(self.state_file, 'rb') as f:
                state = pickle.load(f)

            # Validate state is a dictionary and not too large
            if not isinstance(state, dict):
                print("⚠️ Invalid state format, clearing")
                self.state_file.unlink()
                return {}

            # Limit number of keys to prevent memory bloat
            if len(state) > 1000:
                print(f"⚠️ Too many state keys ({len(state)}), clearing old state")
                self.state_file.unlink()
                return {}

            return state

        except (pickle.PickleError, EOFError, OSError) as e:
            print(f"⚠️ Error loading state: {e}, clearing corrupted file")
            try:
                self.state_file.unlink()
            except:
                pass
            return {}
    
    def save_persistent_state(self, state: Dict[str, Any]):
        """Save persistent state to file with memory leak protection."""
        try:
            # Validate state before saving
            if not isinstance(state, dict):
                print("⚠️ State must be a dictionary")
                return

            # Limit state size
            if len(state) > 1000:
                print("⚠️ Too many state keys, not saving")
                return

            # Create backup before overwriting
            if self.state_file.exists():
                backup_file = self.state_file.with_suffix('.bak')
                try:
                    self.state_file.rename(backup_file)
                except:
                    pass

            # Write new state
            with open(self.state_file, 'wb') as f:
                pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

            # Remove backup if successful
            backup_file = self.state_file.with_suffix('.bak')
            if backup_file.exists():
                backup_file.unlink()

        except Exception as e:
            print(f"⚠️ Error saving state: {e}")
            # Restore backup if save failed
            backup_file = self.state_file.with_suffix('.bak')
            if backup_file.exists():
                try:
                    backup_file.rename(self.state_file)
                except:
                    pass
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value, with persistent fallback and memory protection."""
        # Limit key length to prevent memory issues
        if not isinstance(key, str) or len(key) > 100:
            print(f"⚠️ Invalid state key: {key}")
            return default

        if key not in st.session_state:
            persistent_state = self.load_persistent_state()
            if key in persistent_state:
                value = persistent_state[key]
                # Validate value size
                try:
                    import sys
                    value_size = sys.getsizeof(value)
                    if value_size > 1024 * 1024:  # 1MB limit per value
                        print(f"⚠️ State value too large ({value_size} bytes), using default")
                        st.session_state[key] = default
                        return default
                except:
                    pass
                st.session_state[key] = value
            else:
                st.session_state[key] = default
        return st.session_state[key]
    
    def set_state(self, key: str, value: Any, persistent: bool = True):
        """Set a state value with memory leak protection."""
        # Validate key
        if not isinstance(key, str) or len(key) > 100:
            print(f"⚠️ Invalid state key: {key}")
            return

        # Validate value size
        try:
            import sys
            value_size = sys.getsizeof(value)
            if value_size > 1024 * 1024:  # 1MB limit per value
                print(f"⚠️ State value too large ({value_size} bytes), not setting")
                return
        except:
            pass

        st.session_state[key] = value
        if persistent:
            persistent_state = self.load_persistent_state()
            persistent_state[key] = value
            self.save_persistent_state(persistent_state)
    
    def clear_persistent_state(self):
        """Clear all persistent state with cleanup."""
        try:
            # Clear session state
            st.session_state.clear()

            # Remove state file and backup
            if self.state_file.exists():
                self.state_file.unlink()
            backup_file = self.state_file.with_suffix('.bak')
            if backup_file.exists():
                backup_file.unlink()

        except Exception as e:
            print(f"⚠️ Error clearing state: {e}")
    
    def update_heartbeat(self):
        """Update the heartbeat file to indicate browser is active."""
        try:
            heartbeat_data = {
                'last_heartbeat': datetime.now().timestamp(),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.heartbeat_file, 'w') as f:
                json.dump(heartbeat_data, f)
                
        except Exception as e:
            print(f"⚠️ Error updating heartbeat: {e}")
    
    def check_browser_active(self, max_idle_seconds: int = 30) -> bool:
        """Check if browser is still active based on heartbeat."""
        if not self.heartbeat_file.exists():
            return True  # Allow if no heartbeat file exists yet

        try:
            with open(self.heartbeat_file, 'r') as f:
                heartbeat_data = json.load(f)

            last_heartbeat = heartbeat_data.get('last_heartbeat', 0)
            time_since_heartbeat = datetime.now().timestamp() - last_heartbeat

            return time_since_heartbeat < max_idle_seconds

        except Exception as e:
            print(f"⚠️ Error checking heartbeat: {e}")
            return True  # Allow if we can't read the file
    
    def get_meditation_session_info(self) -> Dict[str, Any]:
        """Get current meditation session information."""
        if not self.session_file.exists():
            return {
                'active': False,
                'start_time': None,
                'total_meditations': 0,
                'current_state': 'idle'
            }
        
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            return {
                'active': session_data.get('active', False),
                'start_time': session_data.get('start_time'),
                'total_meditations': session_data.get('meditation_count', 0),
                'current_state': session_data.get('current_state', 'idle'),
                'karma_gained': session_data.get('karma_gained', 0.0),
                'efficiency_scores': session_data.get('efficiency_scores', [])
            }
            
        except Exception as e:
            print(f"⚠️ Error reading session file: {e}")
            return {
                'active': False,
                'start_time': None,
                'total_meditations': 0,
                'current_state': 'idle'
            }
    
    def render_sidebar(self):
        """Render the sidebar with persistent state management."""
        st.sidebar.title("🔧 System Controls")
        
        # Persistent State Management
        st.sidebar.subheader("💾 Persistent State")
        
        if st.sidebar.button("🗑️ Clear All State", type="secondary"):
            self.clear_persistent_state()
            st.sidebar.success("State cleared!")
            st.rerun()
        
        # State Information
        persistent_state = self.load_persistent_state()
        st.sidebar.write(f"**State Keys:** {len(persistent_state)}")
        
        if persistent_state:
            state_size = sum(sys.getsizeof(str(v)) for v in persistent_state.values()) / 1024
            st.sidebar.write(f"**State Size:** {state_size:.1f} KB")
        
        # Meditation Session Info
        session_info = self.get_meditation_session_info()
        if session_info['active']:
            st.sidebar.subheader("🧘 Meditation Session")
            st.sidebar.write(f"**Status:** Active")
            st.sidebar.write(f"**Meditations:** {session_info['total_meditations']}")
            st.sidebar.write(f"**Karma:** {session_info['karma_gained']:.1f}")
        else:
            st.sidebar.subheader("🧘 Meditation Session")
            st.sidebar.write("**Status:** Inactive")
    
    def render_main_interface(self):
        """Render the main interface."""
        st.title("🌙 AIOS Clean - Luna Learning System")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🧠 Learning", "📊 Analytics", "🔧 Settings"])
        
        with tab1:
            self._render_chat_interface()
        
        with tab2:
            self._render_learning_interface()
        
        with tab3:
            self._render_analytics_interface()
        
        with tab4:
            self._render_settings_interface()
    
    def _render_chat_interface(self):
        """Render the chat interface."""
        st.header("💬 Chat with Luna")
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask Luna anything..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response (placeholder)
            with st.chat_message("assistant"):
                response = "Hello! I'm Luna, your AI learning companion. How can I help you today?"
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    def _render_learning_interface(self):
        """Render the learning interface."""
        st.header("🧠 Luna Learning System")
        
        # Meditation Engine
        st.subheader("🧘 Meditation Engine")
        
        meditation_confirm = self.get_state('meditation_confirm', False)
        
        if not meditation_confirm:
            st.info("Click below to start Luna's autonomous self-reflection mode")
            
            if st.button("🌙 Enter Meditation Mode (Self-Query Loop)", type="primary"):
                self.set_state('meditation_confirm', True)
                st.rerun()
        else:
            st.warning("⚠️ Meditation mode requires confirmation")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ YES, Start Autonomous Reflection", type="primary"):
                    # Start meditation process
                    st.success("🧘 Meditation mode started!")
                    self.update_heartbeat()
            
            with col2:
                if st.button("❌ Cancel", type="secondary"):
                    self.set_state('meditation_confirm', False)
                    st.rerun()
        
        # Meditation Dashboard
        session_info = self.get_meditation_session_info()
        if session_info['active']:
            st.subheader("📊 Meditation Dashboard")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Session Duration", f"{session_info['total_meditations']} cycles")
            with col2:
                st.metric("Karma Gained", f"{session_info['karma_gained']:.1f}")
            with col3:
                st.metric("Current State", session_info['current_state'])
    
    def _render_analytics_interface(self):
        """Render the analytics interface."""
        st.header("📊 System Analytics")
        
        # Placeholder for analytics
        st.info("Analytics interface coming soon...")
    
    def _render_settings_interface(self):
        """Render the settings interface."""
        st.header("🔧 System Settings")
        
        # System configuration options
        st.subheader("System Configuration")
        
        # Placeholder for settings
        st.info("Settings interface coming soon...")

# Main entry point for Streamlit app
def main():
    """Main Streamlit application entry point."""
    # Initialize Streamlit core
    streamlit_core = StreamlitCore()
    
    # Update heartbeat
    streamlit_core.update_heartbeat()
    
    # Render sidebar
    streamlit_core.render_sidebar()
    
    # Render main interface
    streamlit_core.render_main_interface()

if __name__ == "__main__":
    main()
