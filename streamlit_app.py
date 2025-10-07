import streamlit as st
import os
from pathlib import Path

st.set_page_config(
    page_title="Travis Miner - AI Developer Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
st.markdown('<h2 style="text-align: center; color: #666;">AI Developer & Systems Architect</h2>', unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 📋 [About](#about)")
with col2:
    st.markdown("### 🛠️ [Projects](#projects)")
with col3:
    st.markdown("### 💼 [Services](#services)")
with col4:
    st.markdown("### 📞 [Contact](#contact)")

# About Section
st.markdown("---")
st.markdown("## About Me")
st.markdown("""
**Neurodivergent AI Developer with 6+ months of intensive learning and project development.**

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

# Projects Section
st.markdown("---")
st.markdown("## Featured Projects")

# AIOS Project
st.markdown('<div class="project-card">', unsafe_allow_html=True)
st.markdown("### 🤖 AIOS - Modular AI Operating System")
st.markdown("""
**A production-ready modular AI system with closed-loop evaluation infrastructure.**

**Key Features:**
- ✅ Language-first mathematical refinement routing (60/40 main/embedder split)
- ✅ Modular architecture with proven component swappability (92% independence)
- ✅ CARMA cognitive memory system with decay/freshness policies
- ✅ Hypothesis-driven adaptation with provenance logging
- ✅ Complete CI/CD infrastructure with SLO monitoring
- ✅ Production security (PII redaction, GDPR compliance)

**Technical Stack:** Python, Streamlit, LM Studio, Git, CI/CD
**Status:** Production-ready with comprehensive documentation
""")
st.markdown("**🔗 [GitHub Repository](https://github.com/Nemeca99/AIOS)**")
st.markdown("**📊 [Documentation](https://github.com/Nemeca99/AIOS/blob/main/README.md)**")
st.markdown('</div>', unsafe_allow_html=True)

# Custom LLM Project
st.markdown('<div class="project-card">', unsafe_allow_html=True)
st.markdown("### 🧠 Custom LLM Training System")
st.markdown("""
**Personal AI model training and management system.**

**Features:**
- Model configuration and training pipeline
- Data preprocessing and validation
- Training progress monitoring
- Model deployment and testing

**Technical Stack:** Python, AI/ML libraries, Local LLM integration
""")
st.markdown('</div>', unsafe_allow_html=True)

# Extension Converter Project
st.markdown('<div class="project-card">', unsafe_allow_html=True)
st.markdown("### 🔄 All-in-One Extension Converter")
st.markdown("""
**Comprehensive file conversion and data processing tool.**

**Features:**
- Multi-format file conversion
- Data collection and processing
- AI training data preparation
- Discord bot integration
- Automated workflows

**Technical Stack:** Python, Discord.py, File processing libraries
""")
st.markdown('</div>', unsafe_allow_html=True)

# Services Section
st.markdown("---")
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
    - **Security**: GDPR compliance and data protection
    """)

# Pricing
st.markdown("---")
st.markdown("## Project Pricing")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚀 Quick Projects")
    st.markdown("""
    **$200 - $500**
    - Simple chatbot setup
    - Data dashboard
    - Automation script
    - 2-5 days delivery
    """)

with col2:
    st.markdown("### 💼 Custom Solutions")
    st.markdown("""
    **$500 - $2000**
    - Complex AI systems
    - Multi-component apps
    - Integration projects
    - 1-3 weeks delivery
    """)

with col3:
    st.markdown("### 🏢 Enterprise")
    st.markdown("""
    **$2000+**
    - Full system architecture
    - Ongoing support
    - Team training
    - Custom timeline
    """)

# Contact Section
st.markdown("---")
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
st.markdown("**Portfolio:** [This Streamlit App](https://share.streamlit.io/)")
st.markdown("**Projects:** [AIOS Repository](https://github.com/Nemeca99/AIOS)")

# Contact Form
with st.form("contact_form"):
    st.markdown("### Send a Message")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
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
        st.success("✅ Message sent! I'll get back to you within 24 hours.")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>Built with Streamlit | Deployed on Streamlit Cloud</p>
    <p>© 2025 Travis Miner - AI Developer & Systems Architect</p>
</div>
""", unsafe_allow_html=True)
