import streamlit as st
import os
from pathlib import Path

st.set_page_config(
    page_title="Travis Miner — AI Systems Architect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO and Social Preview
st.markdown("""
<meta property="og:title" content="Travis Miner — AI Systems Architect">
<meta property="og:description" content="Modular AI systems, evaluation infrastructure, production dashboards. Proven track record with closed-loop evaluation and enterprise-grade monitoring.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://dj9k9jkcrqvbshyp4qdpfz.streamlit.app/">
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .project-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .skill-badge {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .contact-box {
        background-color: #e8f4fd;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 Travis Miner</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666;">AI Systems Architect</h2>', unsafe_allow_html=True)

# Trust Signals
st.markdown("""
<div style="text-align: center; margin: 1rem 0; padding: 1rem; background-color: #f0f8ff; border-radius: 8px;">
    <strong>Proven Results:</strong> 10/10 golden tests · p95 17.7s · recall@5 100% · Production-ready infrastructure
</div>
""", unsafe_allow_html=True)

# Hero CTAs
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.link_button("📞 Book a Call", "mailto:travis@example.com", use_container_width=True)
with col2:
    st.link_button("🧠 View AIOS", "https://github.com/Nemeca99/AIOS", use_container_width=True)

# Navigation Tabs
st.markdown("---")
about, projects, services, contact = st.tabs(["About", "Projects", "Services", "Contact"])

with about:
    st.markdown("## About Me")
    st.markdown("""
    **Neurodivergent AI Systems Architect with 6+ months of intensive learning and production deployments.**

    I specialize in building modular AI systems, custom chatbots, and automation solutions. 
    My approach combines technical innovation with practical business solutions.

    **Key Strengths:**
    - 🧠 **Systems Thinking**: Design modular, maintainable architectures
    - 🔧 **Problem Solving**: Turn complex requirements into working solutions  
    - 🚀 **Fast Execution**: Hyperfocus-driven development cycles
    - 📊 **Data-Driven**: Built-in monitoring, testing, and adaptation systems
    """)

    # Skills
    st.markdown("### Technical Skills")
    skills = [
        "Python", "Streamlit", "AI/LLM Integration", "System Architecture",
        "API Development", "Data Analysis", "Automation", "Git/GitHub",
        "Project Management", "Documentation", "Testing", "Deployment"
    ]

    skill_html = '<div style="text-align: center;">'
    for skill in skills:
        skill_html += f'<span class="skill-badge">{skill}</span>'
    skill_html += '</div>'
    st.markdown(skill_html, unsafe_allow_html=True)

with projects:
    st.markdown("## Featured Projects")

    # AIOS Project
    with st.container(border=True):
        st.subheader("🤖 AIOS — Modular AI Operating System")
        st.markdown("Production-ready modular AI system with closed-loop evaluation infrastructure.")
        st.markdown("**Key Features:** Language-first routing, CARMA memory, hypothesis-driven adaptation, CI/CD, GDPR-aligned data handling.")
        st.markdown("**Stack:** Python · Streamlit · LM Studio · Git · CI/CD")
        st.link_button("View AIOS Repository", "https://github.com/Nemeca99/AIOS")

    # Custom LLM Project
    with st.container(border=True):
        st.subheader("🧠 Custom LLM Training System")
        st.markdown("Personal AI model training and management system with configuration pipelines.")
        st.markdown("**Stack:** Python · AI/ML libraries · Local LLM integration")
        st.link_button("View Portfolio", "#")

    # Extension Converter Project
    with st.container(border=True):
        st.subheader("🔄 All-in-One Extension Converter")
        st.markdown("Comprehensive file conversion and data processing tool with Discord integration.")
        st.markdown("**Stack:** Python · Discord.py · File processing libraries")
        st.link_button("View Portfolio", "#")

with services:
    st.markdown("## Services Offered")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 AI Development")
        st.markdown("""
        - **Custom Chatbots**: Business-specific AI assistants
        - **RAG Systems**: Document search and retrieval
        - **AI Integration**: OpenAI, LM Studio, local models
        - **Automation**: AI-powered workflow automation
        """)
        
        st.markdown("### 🌐 Web Development")
        st.markdown("""
        - **Streamlit Dashboards**: Data visualization and monitoring
        - **API Development**: RESTful services and integrations
        - **Database Design**: Data architecture and optimization
        - **Deployment**: Cloud hosting and CI/CD setup
        """)

    with col2:
        st.markdown("### 🛠️ Business Solutions")
        st.markdown("""
        - **Process Automation**: Workflow optimization
        - **Data Analysis**: Insights and reporting
        - **System Architecture**: Modular, scalable design
        - **Technical Consulting**: AI strategy and implementation
        """)
        
        st.markdown("### 📊 Portfolio Highlights")
        st.markdown("""
        - **Production Systems**: Real-world deployment experience
        - **Comprehensive Testing**: QA infrastructure and monitoring
        - **Documentation**: Complete runbooks and guides
        - **Security**: GDPR-aligned data handling
        """)

    # Pricing
    st.markdown("## Project Pricing")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🚀 Quick Projects")
        st.markdown("**$200–$500** · 2–5 days · 1 revision")
        st.markdown("""
        - Simple chatbot setup
        - Data dashboard
        - Automation script
        """)

    with col2:
        st.markdown("### 💼 Custom Solutions")
        st.markdown("**$500–$2000** · 1–3 weeks · 2 revisions")
        st.markdown("""
        - Complex AI systems
        - Multi-component apps
        - Integration projects
        """)

    with col3:
        st.markdown("### 🏢 Enterprise")
        st.markdown("**$2000+** · Custom timeline · Ongoing support")
        st.markdown("""
        - Full system architecture
        - Team training
        - Dedicated support
        """)

with contact:
    st.markdown('<div class="contact-box">', unsafe_allow_html=True)
    st.markdown("## 📞 Let's Work Together")
    st.markdown("""
    **Ready to build something amazing?**

    I specialize in turning complex ideas into working systems. 
    Whether you need a simple chatbot or a full AI infrastructure, 
    I can help you get it done quickly and professionally.

    **Contact me today for a free consultation!**
    """)

    st.markdown("### 📧 Get In Touch")
    st.markdown("**GitHub:** [Nemeca99](https://github.com/Nemeca99)")
    st.markdown("**Portfolio:** [This Streamlit App](https://dj9k9jkcrqvbshyp4qdpfz.streamlit.app/)")
    st.markdown("**Projects:** [AIOS Repository](https://github.com/Nemeca99/AIOS)")

    # Contact Form
    with st.form("contact_form"):
        st.markdown("### Send a Message")
        name = st.text_input("Name")
        email = st.text_input("Email")
        project_type = st.selectbox("Project Type", [
            "Custom Chatbot",
            "Data Dashboard", 
            "AI Integration",
            "Automation Script",
            "Full System Development",
            "Consulting",
            "Other"
        ])
        message = st.text_area("Project Details", height=100)
        submitted = st.form_submit_button("Send Message")
        
        if submitted:
            st.success("✅ Thanks. I'll reply soon.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>Built with Streamlit | Deployed on Streamlit Cloud</p>
    <p>© 2025 Travis Miner — AI Systems Architect</p>
</div>
""", unsafe_allow_html=True)
