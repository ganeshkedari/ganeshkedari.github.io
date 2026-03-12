"""
data.py — Resume Content & Configuration Data
===============================================

This module is the **single source of truth** for all text content,
personal details, experience entries, education entries, and social
links displayed in the Streamlit resume application.

Why separate data from rendering?
---------------------------------
1. Easy to update content without touching layout / component code.
2. Makes the main app file (ganeshkedari.py) short and readable.
3. Enables potential future features (e.g. loading data from a YAML
   file or database) with minimal refactoring.

Data Structures
---------------
- PERSONAL      : dict  – Name, title, tagline, quote, contact URL.
- SOCIAL_LINKS  : dict  – Platform name → URL.
- EXPERIENCE    : list  – Professional experience entries (newest first).
- EDUCATION     : list  – Academic qualifications (newest first).
- ASSET_PATHS   : dict  – Logical name → relative path under streamlit/.

All paths are relative to the project root (the streamlit/ folder).
They are resolved at runtime using BASE_DIR in the main app.
"""

from __future__ import annotations


# ─────────────────────────────────────────────────────────────────────────────
# PERSONAL DETAILS
# ─────────────────────────────────────────────────────────────────────────────

PERSONAL: dict[str, str | list[str]] = {
    # Display name
    "name": "Ganesh Kedari",

    # One-line role description (shown below profile image in sidebar)
    "title": "Solution Architect • Data & Analytics",

    # Words cycled by the typewriter animation in the hero section
    "typed_words": ["Coder", "Data Mercenary", "Geek"],

    # Inspirational quote in the hero section
    "quote": (
        "I do not know what I may appear to the world; but to myself I seem "
        "to have been only like a boy playing on the sea-shore, and diverting "
        "myself in now and then finding a smoother pebble or a prettier shell "
        "than ordinary, whilst the great ocean of truth lay all undiscovered "
        "before me."
    ),
    "quote_author": "Sir Isaac Newton",

    # Contact / booking link
    "contact_url": "https://topmate.io/ganeshkedari/",

    # Brief contact blurb (shown in the Contact section)
    "contact_blurb": (
        "I'm always open to discussing data architecture, AI strategy, "
        "or new opportunities. Feel free to reach out!"
    ),

    # Copyright text
    "copyright": "© Copyright Ganesh Kedari — All Rights Reserved",
}


# ─────────────────────────────────────────────────────────────────────────────
# SOCIAL LINKS
# Platform name → URL.  Order determines display order.
# ─────────────────────────────────────────────────────────────────────────────

SOCIAL_LINKS: dict[str, str] = {
    "LinkedIn":    "https://www.linkedin.com/in/ganeshkedari",
    "GitHub":      "https://github.com/ganeshkedari/",
    "X / Twitter": "https://x.com/ganesh_kedari",
    "Facebook":    "https://www.facebook.com/ganeshkedari",
    "Instagram":   "https://instagram.com/ganeshkedari",
}


# ─────────────────────────────────────────────────────────────────────────────
# PROFESSIONAL EXPERIENCE
# Each entry is a dict with keys: title, period, org, desc, bullets.
# Listed newest-first (matches the visual order on the page).
# ─────────────────────────────────────────────────────────────────────────────

EXPERIENCE: list[dict] = [
    {
        "title": "Staff Architect",
        "period": "Nov 2019 – Present",
        "org": "IQVIA, Pune, India",
        "desc": (
            "At IQVIA, I help Life Sciences organizations unlock the power of "
            "AI-powered, conversational analytics. Instead of just building "
            "tools, I focus on designing solutions that change the way business "
            "users interact with data and make decisions."
        ),
        "bullets": [
            "Architected and deployed AI-driven analytics solutions that "
            "enabled pharma clients to ask questions in natural language and "
            "receive instant insights, improving decision-making speed.",

            "Built a scalable analytics framework for managing data pipelines "
            "and model training, reducing deployment time and boosting model "
            "accuracy.",

            "Integrated diverse data sources (SAP HANA, Snowflake, AWS "
            "Redshift, Azure CosmosDB, Databricks, Salesforce, VEEVA CRM) "
            "into unified analytics platforms, enhancing data accessibility "
            "and reporting precision.",

            "Developed and operationalized machine learning models for NLP, "
            "anomaly detection, and predictive insights, helping clients "
            "identify risks and opportunities earlier.",

            "Partnered with product teams and business stakeholders to "
            "co-create solutions that delivered measurable ROI and stronger "
            "adoption across global user bases.",

            "Streamlined DevOps integration using Kubernetes, Helm, and "
            "Grafana, improving reliability, scalability, and system "
            "monitoring.",

            "Created a reusable analytics artifacts library, cutting "
            "development effort by 20% across multiple projects.",
        ],
    },
    {
        "title": "Solution Architect",
        "period": "2008 – 2019",
        "org": "IBM, Pune, India",
        "desc": (
            "Progressed from Entry Level Engineer to System Scientist to "
            "Solution Architect, driving the evolution of IBM's analytics "
            "capabilities through client-focused innovation and scalable BI "
            "solutions. Designed and delivered enterprise-grade analytics "
            "architectures across global teams, integrating AI, DevOps, and "
            "big data technologies."
        ),
        "bullets": [
            "Spearheaded end-to-end analytics solution design and delivery, "
            "progressing from System Scientist to Solution Architect within "
            "IBM's global Data & Analytics practice.",

            "Drove customer-centric product innovation by aligning real-world "
            "use cases with IBM Business Analytics roadmap, enhancing product "
            "relevance and adoption.",

            "Designed and implemented scalable BI architectures for global "
            "clients, using tools like Cognos, Power BI, and ELK to unify "
            "insights across complex data ecosystems.",

            "Architected AI-powered analytics frameworks on big data lakes, "
            "enabling procurement teams to improve operational efficiency and "
            "decision-making by 20%.",

            "Integrated analytics solutions with modern DevOps pipelines "
            "(Docker, Kubernetes, Jenkins), reducing deployment cycles and "
            "improving release reliability.",

            "Delivered strategic proofs-of-concept in data quality, "
            "automation, and mobile BI, directly influencing IBM Procurement's "
            "product development priorities.",

            "Collaborated cross-functionally with global clients to translate "
            "business needs into technical solutions, strengthening IBM's "
            "consulting and delivery capabilities.",
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# EDUCATION
# Each entry is a dict with keys: title, period, org, desc.
# Listed newest-first.
# ─────────────────────────────────────────────────────────────────────────────

EDUCATION: list[dict] = [
    {
        "title": "Master of Science — Scientific Computing",
        "period": "2006 – 2008",
        "org": "Savitribai Phule University, Pune, India",
        "desc": (
            "Majoring in Scientific Computing with a concentration in High "
            "Performance Computing, Optimization Techniques, Unix Programming "
            "and Java, I have been exposed to all facets of software "
            "development life cycle. Throughout my collegiate career, I "
            "attempted to stay well-rounded combining academic excellence "
            "with leadership and work experience."
        ),
    },
    {
        "title": "Bachelor of Computer Science",
        "period": "2003 – 2005",
        "org": "Savitribai Phule University, Pune, India",
        "desc": (
            "Activities and societies: Represented College at various "
            "Technical Events, Member of National Service Scheme, "
            "Participated in National Level Republic Day Camp. "
            'Completed B.Sc. in Computer Science with "First class with '
            'Distinction".'
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# ASSET PATHS (relative to the streamlit/ folder — resolved at runtime)
# ─────────────────────────────────────────────────────────────────────────────

ASSET_PATHS: dict[str, str] = {
    "profile_img":  "assets/profile.PNG",        # Sidebar & hero profile photo
    "favicon":      "assets/r2d2.png",           # Browser tab icon
    "resume_pdf":   "assets/Ganesh_Kedari_Visual_CV.pdf",  # Downloadable CV
}
