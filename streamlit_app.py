#!/usr/bin/env python3
"""
AIOS Clean - Streamlit Web Interface
Web interface for the AIOS Clean system using the unified main.py as foundation.
"""

import streamlit as st
import json
import time
from datetime import datetime
from main import AIOSClean, SystemMode

# Page configuration
st.set_page_config(
    page_title="AIOS Clean",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'aios_system' not in st.session_state:
    st.session_state.aios_system = None
    st.session_state.initialized = False

# Sidebar
st.sidebar.title("🧠 AIOS Clean")
st.sidebar.markdown("Advanced AI Performance System")

# Initialize system button
if st.sidebar.button("🚀 Initialize System", type="primary"):
    with st.spinner("Initializing AIOS Clean System..."):
        st.session_state.aios_system = AIOSClean()
        st.session_state.initialized = True
    st.success("System initialized successfully!")

# Main interface
if st.session_state.initialized and st.session_state.aios_system:
    
    # System status
    st.title("📊 System Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = st.session_state.aios_system.get_quick_status()
        st.metric("System Status", status['status'].title())
    
    with col2:
        st.metric("CARMA Fragments", status['carma_fragments'])
    
    with col3:
        st.metric("Luna Interactions", status['luna_interactions'])
    
    with col4:
        st.metric("Support Fragments", status['support_fragments'])
    
    # Tabs for different functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌙 Luna AI", 
        "🧠 CARMA", 
        "🔍 Health", 
        "🧪 Testing", 
        "⚙️ Settings"
    ])
    
    with tab1:
        st.header("🌙 Luna AI Personality System")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            questions = st.slider("Number of Questions", 1, 10, 3)
            if st.button("Run Luna Learning Session", type="primary"):
                with st.spinner("Running Luna learning session..."):
                    results = st.session_state.aios_system.run_luna_learning(questions)
                
                st.success("Luna learning session completed!")
                st.json(results)
        
        with col2:
            st.info("""
            **Luna AI Features:**
            - Big Five personality assessment
            - Adaptive learning system
            - Dream cycle processing
            - Memory consolidation
            """)
    
    with tab2:
        st.header("🧠 CARMA Performance System")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            queries = st.text_area(
                "Enter CARMA Learning Queries (one per line):",
                value="I am learning about artificial intelligence\nThis is a test query\nMemory consolidation is important",
                height=100
            )
            
            if st.button("Run CARMA Learning Session", type="primary"):
                query_list = [q.strip() for q in queries.split('\n') if q.strip()]
                with st.spinner("Running CARMA learning session..."):
                    results = st.session_state.aios_system.run_carma_learning(query_list)
                
                st.success("CARMA learning session completed!")
                st.json(results)
        
        with col2:
            st.info("""
            **CARMA Features:**
            - Performance architecture
            - Memory consolidation
            - Synaptic tagging
            - Predictive coding
            """)
    
    with tab3:
        st.header("🔍 System Health Check")
        
        if st.button("Run Health Check", type="primary"):
            with st.spinner("Running system health check..."):
                health_results = st.session_state.aios_system.run_system_health_check()
            
            st.success("Health check completed!")
            
            # Display health score
            health_score = health_results.get('health_score', 0)
            st.metric("Health Score", f"{health_score:.2f}/1.0")
            
            # Display detailed results
            st.json(health_results)
    
    with tab4:
        st.header("🧪 System Testing")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Run System Tests", type="primary"):
                with st.spinner("Running system tests..."):
                    test_results = st.session_state.aios_system.run_system_tests()
                
                st.success("System tests completed!")
                
                # Display test results
                success_rate = (test_results['passed'] / test_results['total'] * 100)
                st.metric("Success Rate", f"{success_rate:.1f}%")
                st.metric("Tests Passed", f"{test_results['passed']}/{test_results['total']}")
                
                # Display individual test results
                for test in test_results['tests']:
                    status_emoji = "✅" if test['status'] == 'passed' else "❌"
                    st.write(f"{status_emoji} {test['name']}: {test['message']}")
        
        with col2:
            st.info("""
            **Test Coverage:**
            - Import tests
            - System initialization
            - Basic functionality
            - Error handling
            """)
    
    with tab5:
        st.header("⚙️ System Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("System Information")
            info = st.session_state.aios_system.get_system_info()
            st.json(info)
        
        with col2:
            st.subheader("Export Data")
            if st.button("Export System Data"):
                filename = st.session_state.aios_system.export_system_data()
                st.success(f"Data exported to: {filename}")
                st.download_button(
                    label="Download Export",
                    data=json.dumps(st.session_state.aios_system.get_system_status(), indent=2),
                    file_name=filename,
                    mime="application/json"
                )

else:
    # Welcome screen
    st.title("🧠 Welcome to AIOS Clean")
    st.markdown("### Advanced AI Performance System")
    
    st.markdown("""
    **AIOS Clean** is a unified AI performance system featuring:
    
    - **🌙 Luna AI** - Advanced personality system with learning capabilities
    - **🧠 CARMA** - Cached Aided Retrieval Mycelium Architecture
    - **🏢 Enterprise** - API and business features
    - **🛠️ Support** - Utilities and operations
    
    Click the "Initialize System" button in the sidebar to get started!
    """)
    
    # System architecture diagram
    st.subheader("System Architecture")
    st.code("""
    main.py (Unified Entry Point)
    ├── carma_core/carma_core.py
    ├── luna_core/luna_core.py  
    ├── enterprise_core/enterprise_core.py
    └── support_core/support_core.py
    """, language="text")

# Footer
st.markdown("---")
st.markdown("**AIOS Clean v1.0.0** - Advanced AI Performance System")
