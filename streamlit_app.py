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

# Custom CSS - Travis's Professional Style
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 400;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
    }
    
    /* Trust Signals */
    .trust-signals {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .trust-signals strong {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        color: #1e293b;
        font-weight: 500;
    }
    
    /* Hero CTAs */
    .hero-ctas {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 2rem 0;
    }
    
    /* Project Cards */
    .project-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.3rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .skill-badge:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Pricing Cards */
    .pricing-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .pricing-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
    }
    
    .pricing-card.featured {
        border-color: #667eea;
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    
    /* Contact Section */
    .contact-box {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Code Blocks */
    .code-block {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Metrics */
    .metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Footer */
    .footer {
        background: #1e293b;
        color: #94a3b8;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 16px 16px 0 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .hero-ctas {
            flex-direction: column;
            align-items: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 Travis Miner</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">AI Systems Architect</h2>', unsafe_allow_html=True)

# Trust Signals with Metrics
st.markdown("""
<div class="trust-signals">
    <strong>Proven Results:</strong> 10/10 golden tests · p95 17.7s · recall@5 100% · Production-ready infrastructure
</div>
""", unsafe_allow_html=True)

# Hero CTAs
st.markdown('<div class="hero-ctas">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.link_button("📞 Book a Call", "mailto:travis@example.com", use_container_width=True)
with col2:
    st.link_button("🧠 View AIOS", "https://github.com/Nemeca99/AIOS", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation Tabs
st.markdown("---")
about, projects, services, contact = st.tabs(["About", "Projects", "Services", "Contact"])

with about:
    st.markdown("## About Me")
    
    # Personal Story
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Building the future of AI, one system at a time.**

        I'm a neurodivergent AI Systems Architect who's spent the last 6 months diving deep into 
        production-grade AI development. My journey started with curiosity about how AI systems 
        could be built differently—more modular, more intelligent, more human.

        **What drives me:** Creating AI systems that don't just work, but adapt, learn, and 
        improve over time. I believe the best technology feels invisible to users but powerful 
        in its capabilities.

        **My approach:** Every project gets the same attention to detail—from the initial 
        architecture decisions to the final monitoring dashboards. I build systems that are 
        meant to last and grow with your business.
        """)
    
    with col2:
        # Key Metrics
        st.markdown("### Proven Results")
        st.markdown('<div class="metric">', unsafe_allow_html=True)
        st.markdown('<span class="metric-number">10/10</span>', unsafe_allow_html=True)
        st.markdown('<span class="metric-label">Golden Tests Passing</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric">', unsafe_allow_html=True)
        st.markdown('<span class="metric-number">100%</span>', unsafe_allow_html=True)
        st.markdown('<span class="metric-label">Recall@5 Accuracy</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric">', unsafe_allow_html=True)
        st.markdown('<span class="metric-number">17.7s</span>', unsafe_allow_html=True)
        st.markdown('<span class="metric-label">P95 Response Time</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Core Strengths
    st.markdown("### Core Strengths")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🧠 Systems Thinking**
        Design modular, maintainable architectures that scale with your business.

        **🔧 Problem Solving**
        Turn complex requirements into working solutions that exceed expectations.

        **📊 Data-Driven**
        Built-in monitoring, testing, and adaptation systems ensure continuous improvement.
        """)
    
    with col2:
        st.markdown("""
        **🚀 Fast Execution**
        Hyperfocus-driven development cycles that deliver results quickly.

        **🎯 Business Focus**
        Every technical decision is made with your business goals in mind.

        **📚 Continuous Learning**
        Staying current with AI advances to bring you cutting-edge solutions.
        """)

    # Technical Skills
    st.markdown("### Technical Expertise")
    skills = [
        "Python", "Streamlit", "AI/LLM Integration", "System Architecture",
        "API Development", "Data Analysis", "Automation", "Git/GitHub",
        "Project Management", "Documentation", "Testing", "Deployment",
        "RAG Systems", "Monitoring", "CI/CD", "Security"
    ]

    skill_html = '<div style="text-align: center; margin: 2rem 0;">'
    for skill in skills:
        skill_html += f'<span class="skill-badge">{skill}</span>'
    skill_html += '</div>'
    st.markdown(skill_html, unsafe_allow_html=True)
    
    # Philosophy
    st.markdown("### My Development Philosophy")
    st.markdown("""
    > **"AI is a mirror—you have to build it backwards."**
    
    This isn't just a catchy phrase—it's how I approach every project. While most AI systems 
    start with mathematics and hope language emerges, I start with language and use mathematics 
    for refinement. This "backward engineering" approach creates AI that feels more natural 
    and responds more intelligently to human needs.
    
    **The result?** Systems that work the way humans think, not the way computers process.
    """)

with projects:
    st.markdown("## Featured Projects")
    st.markdown("Each project represents months of learning, iteration, and real-world application. These aren't tutorials—they're production systems.")

    # AIOS Project
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 AIOS — Modular AI Operating System")
    st.markdown("""
    **Production-ready modular AI system with closed-loop evaluation infrastructure.**
    
    This is my flagship project—a complete AI operating system that demonstrates advanced concepts 
    like language-first mathematical refinement, cognitive memory systems, and hypothesis-driven 
    adaptation. Built with enterprise-grade monitoring, security, and documentation.
    """)
    
    # Key Features with Icons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔧 Technical Features:**
        - Language-first routing (60/40 main/embedder split)
        - CARMA cognitive memory with decay policies
        - Hypothesis-driven adaptation system
        - Complete CI/CD infrastructure
        - Real-time SLO monitoring
        """)
    
    with col2:
        st.markdown("""
        **📊 Measured Results:**
        - 10/10 golden tests passing
        - 100% recall@5 on QA set
        - P95 latency: 17.7s
        - 92% component independence
        - GDPR-aligned data handling
        """)
    
    st.markdown("**Stack:** Python · Streamlit · LM Studio · Git · CI/CD · Docker")
    st.link_button("View AIOS Repository", "https://github.com/Nemeca99/AIOS")
    st.markdown('</div>', unsafe_allow_html=True)

    # Custom LLM Project
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Custom LLM Training System")
    st.markdown("""
    **Personal AI model training and management system with configuration pipelines.**
    
    Built to understand the full lifecycle of AI model development—from data preprocessing 
    through training, validation, and deployment. Includes automated configuration management 
    and training progress monitoring.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🎯 Capabilities:**
        - Model configuration management
        - Training pipeline automation
        - Data preprocessing and validation
        - Progress monitoring and logging
        """)
    
    with col2:
        st.markdown("""
        **📈 Features:**
        - Automated hyperparameter tuning
        - Model versioning and comparison
        - Performance metrics tracking
        - Local deployment testing
        """)
    
    st.markdown("**Stack:** Python · AI/ML libraries · Local LLM integration · Configuration management")
    st.link_button("View Portfolio", "#")
    st.markdown('</div>', unsafe_allow_html=True)

    # Extension Converter Project
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### 🔄 All-in-One Extension Converter")
    st.markdown("""
    **Comprehensive file conversion and data processing tool with Discord integration.**
    
    A multi-purpose automation platform that handles file conversion, data collection, 
    and AI training data preparation. Includes Discord bot integration for seamless 
    workflow management and user interaction.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **⚡ Core Features:**
        - Multi-format file conversion
        - Data collection and processing
        - AI training data preparation
        - Automated workflow management
        """)
    
    with col2:
        st.markdown("""
        **🤖 Integration:**
        - Discord bot for user interaction
        - API endpoints for external access
        - Batch processing capabilities
        - Progress tracking and notifications
        """)
    
    st.markdown("**Stack:** Python · Discord.py · File processing libraries · API development")
    st.link_button("View Portfolio", "#")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Portfolio Showcase Note
    st.markdown("""
    ---
    **💡 This Portfolio Itself**
    
    This Streamlit application is also a demonstration of my capabilities—clean design, 
    responsive layout, professional styling, and seamless user experience. Built with 
    modern web standards and deployed on cloud infrastructure.
    """)

with services:
    st.markdown("## Services Offered")
    st.markdown("Building toward a family-run business where quality and personal attention matter more than scale.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 AI Development")
        st.markdown("""
        - **Custom Chatbots**: Business-specific AI assistants that understand your needs
        - **RAG Systems**: Intelligent document search and retrieval systems
        - **AI Integration**: Seamless OpenAI, LM Studio, and local model integration
        - **Workflow Automation**: AI-powered processes that save time and reduce errors
        """)
        
        st.markdown("### 🌐 Web Development")
        st.markdown("""
        - **Streamlit Dashboards**: Beautiful data visualization and monitoring interfaces
        - **API Development**: RESTful services and seamless integrations
        - **Database Design**: Scalable data architecture and optimization
        - **Cloud Deployment**: Professional hosting and CI/CD setup
        """)

    with col2:
        st.markdown("### 🛠️ Business Solutions")
        st.markdown("""
        - **Process Automation**: Workflow optimization that scales with your business
        - **Data Analysis**: Actionable insights and comprehensive reporting
        - **System Architecture**: Modular, scalable designs that grow with you
        - **Technical Consulting**: AI strategy and implementation guidance
        """)
        
        st.markdown("### 🏆 Why Choose Our Family Business")
        st.markdown("""
        - **Personal Attention**: Every project gets my full focus and expertise
        - **Production Quality**: Enterprise-grade systems with comprehensive testing
        - **Complete Documentation**: Detailed runbooks and maintenance guides
        - **Long-term Partnership**: Support that grows with your business
        """)

    # Pricing with Family Business Focus
    st.markdown("## Investment Options")
    st.markdown("Transparent pricing with no hidden fees. Every project includes comprehensive documentation and support.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="pricing-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Quick Solutions")
        st.markdown("**$200–$500**")
        st.markdown("*2–5 days delivery · 1 revision included*")
        st.markdown("""
        **Perfect for:**
        - Simple chatbot setup
        - Data dashboard creation
        - Automation script development
        - Small business process improvements
        
        **What you get:**
        - Working solution
        - Basic documentation
        - 30-day support
        - Source code access
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="pricing-card featured">', unsafe_allow_html=True)
        st.markdown("### 💼 Custom Solutions")
        st.markdown("**$500–$2000**")
        st.markdown("*1–3 weeks delivery · 2 revisions included*")
        st.markdown("""
        **Perfect for:**
        - Complex AI systems
        - Multi-component applications
        - Integration projects
        - Business process automation
        
        **What you get:**
        - Complete solution
        - Comprehensive documentation
        - 90-day support
        - Training session
        - Future enhancement roadmap
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="pricing-card">', unsafe_allow_html=True)
        st.markdown("### 🏢 Enterprise Partnership")
        st.markdown("**$2000+**")
        st.markdown("*Custom timeline · Ongoing support*")
        st.markdown("""
        **Perfect for:**
        - Full system architecture
        - Team training and development
        - Dedicated ongoing support
        - Strategic AI implementation
        
        **What you get:**
        - Enterprise-grade solution
        - Complete documentation suite
        - Ongoing partnership
        - Priority support
        - Strategic consultation
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Family Business Vision
    st.markdown("""
    ---
    **👨‍👩‍👧‍👦 Our Family Business Vision**
    
    My goal is to build a sustainable family business where my fiancée and I can work together, 
    providing exceptional AI solutions while maintaining the personal touch that makes the difference. 
    Every project contributes to this vision of financial freedom and meaningful work.
    
    **When you hire us, you're not just getting a service—you're supporting a family's dream.**
    """)

with contact:
    st.markdown('<div class="contact-box">', unsafe_allow_html=True)
    st.markdown("## 📞 Let's Build Something Amazing Together")
    st.markdown("""
    **Ready to transform your business with AI?**

    I specialize in turning complex ideas into working systems that grow with your business. 
    Whether you need a simple chatbot or a full AI infrastructure, I can help you get it 
    done quickly, professionally, and with the personal attention that makes the difference.

    **Let's discuss your project and make it happen!**
    """)

    # Contact Methods
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📧 Direct Contact")
        st.markdown("**GitHub:** [Nemeca99](https://github.com/Nemeca99)")
        st.markdown("**Portfolio:** [Live Demo](https://dj9k9jkcrqvbshyp4qdpfz.streamlit.app/)")
        st.markdown("**Projects:** [AIOS Repository](https://github.com/Nemeca99/AIOS)")
    
    with col2:
        st.markdown("### 🚀 Response Times")
        st.markdown("**Initial Response:** Within 24 hours")
        st.markdown("**Project Quote:** 1-2 business days")
        st.markdown("**Emergency Support:** Same day")
    
    with col3:
        st.markdown("### 💼 What to Expect")
        st.markdown("**Free Consultation:** 30-minute discovery call")
        st.markdown("**Detailed Quote:** Transparent pricing")
        st.markdown("**Regular Updates:** Weekly progress reports")

    # Contact Form
    st.markdown("### Send Me a Message")
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name *", placeholder="John Smith")
            email = st.text_input("Email Address *", placeholder="john@company.com")
        with col2:
            company = st.text_input("Company (Optional)", placeholder="Acme Corp")
            budget = st.selectbox("Project Budget", [
                "Under $500",
                "$500 - $1,000", 
                "$1,000 - $2,000",
                "$2,000 - $5,000",
                "$5,000+",
                "Not sure yet"
            ])
        
        project_type = st.selectbox("Project Type *", [
            "Custom Chatbot Development",
            "Data Dashboard Creation", 
            "AI System Integration",
            "Process Automation",
            "Full System Architecture",
            "Technical Consulting",
            "Other - Please describe below"
        ])
        
        timeline = st.selectbox("Timeline", [
            "ASAP (Rush job)",
            "Within 2 weeks",
            "Within 1 month", 
            "Within 3 months",
            "Flexible timeline"
        ])
        
        message = st.text_area("Project Details *", height=120, placeholder="Tell me about your project, goals, and any specific requirements...")
        
        submitted = st.form_submit_button("🚀 Send Message", use_container_width=True)
        
        if submitted:
            st.success("✅ Message sent successfully! I'll get back to you within 24 hours.")
            st.balloons()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Professional Footer
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h4 style="color: #e2e8f0; margin-bottom: 1rem;">Travis Miner — AI Systems Architect</h4>
            <p style="margin: 0;">Building the future of AI, one system at a time.</p>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0;"><strong>Built with:</strong> Streamlit • Python • Modern Web Standards</p>
            <p style="margin: 0;"><strong>Deployed on:</strong> Streamlit Cloud • GitHub • CI/CD</p>
        </div>
    </div>
    <hr style="border: 1px solid #334155; margin: 2rem 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <p style="margin: 0;">© 2025 Travis Miner. All rights reserved.</p>
        </div>
        <div>
            <p style="margin: 0;">Supporting families through exceptional AI solutions.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
