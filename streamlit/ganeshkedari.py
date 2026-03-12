"""
Ganesh Kedari — Interactive Resume (Streamlit App)
===================================================
A single-page, highly interactive resume application built with Streamlit.
Theme mirrors the portfolio site: dark background (#000000), accent blue (#1387c1),
Roboto / Raleway / Poppins fonts.

Run:  streamlit run ganeshkedari.py
"""

import base64
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────
# 0. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Ganesh Kedari | Resume",
    page_icon="assets/r2d2.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
# 1. HELPER: encode local image → base64 data-URI
# ─────────────────────────────────────────────
def img_to_base64(path: str) -> str:
    """Return base64-encoded string of a local image file."""
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode()


def get_pdf_bytes(path: str) -> bytes:
    """Return raw bytes of a file (used for download button)."""
    return Path(path).read_bytes()


# ─────────────────────────────────────────────
# 2. GLOBAL CSS INJECTION
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ── */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Raleway:wght@400;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

        /* ── CSS Variables (mirror index.html) ── */
        :root {
            --bg:       #000000;
            --surface:  #141f26;
            --text:     #e7f2f7;
            --heading:  #ffffff;
            --accent:   #1387c1;
            --contrast: #ffffff;
        }

        /* ── Global overrides ── */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: var(--bg) !important;
            color: var(--text) !important;
            font-family: 'Roboto', sans-serif !important;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            font-family: 'Raleway', sans-serif !important;
            color: var(--heading) !important;
        }

        /* ── Sidebar styling ── */
        section[data-testid="stSidebar"] {
            background-color: var(--surface) !important;
            font-family: 'Poppins', sans-serif !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] a {
            color: var(--text) !important;
        }

        /* ── Hide Streamlit chrome ── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}

        /* ── Accent links ── */
        a { color: var(--accent) !important; text-decoration: none; }
        a:hover { color: #15a3e6 !important; text-decoration: underline; }

        /* ── Streamlit buttons accent ── */
        .stButton > button,
        .stDownloadButton > button {
            background-color: var(--accent) !important;
            color: var(--contrast) !important;
            border: none !important;
            border-radius: 6px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500 !important;
            padding: 0.5rem 1.6rem !important;
            transition: background 0.3s ease;
        }
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background-color: #15a3e6 !important;
        }

        /* ── Outline button variant (via custom HTML) ── */
        .btn-outline-custom {
            display: inline-block;
            padding: 0.5rem 1.6rem;
            border: 2px solid var(--accent);
            color: var(--accent) !important;
            border-radius: 6px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            text-decoration: none !important;
            transition: all 0.3s ease;
            margin-left: 0.5rem;
        }
        .btn-outline-custom:hover {
            background-color: var(--accent);
            color: var(--contrast) !important;
        }
        .btn-primary-custom {
            display: inline-block;
            padding: 0.5rem 1.6rem;
            background-color: var(--accent);
            color: var(--contrast) !important;
            border-radius: 6px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            text-decoration: none !important;
            transition: background 0.3s ease;
        }
        .btn-primary-custom:hover { background-color: #15a3e6; }

        /* ── Section dividers ── */
        .section-divider {
            width: 60px; height: 4px;
            background: var(--accent);
            border: none; margin: 0.5rem 0 1.5rem 0;
            border-radius: 2px;
        }

        /* ── Skill bars ── */
        .skill-bar-container { margin-bottom: 1.2rem; }
        .skill-bar-label {
            display: flex; justify-content: space-between;
            font-family: 'Poppins', sans-serif;
            font-size: 0.95rem; margin-bottom: 0.3rem;
            color: var(--text);
        }
        .skill-bar-track {
            background: rgba(255,255,255,0.08);
            border-radius: 8px; height: 12px;
            overflow: hidden;
        }
        .skill-bar-fill {
            height: 100%; border-radius: 8px;
            background: linear-gradient(90deg, var(--accent), #15a3e6);
            transition: width 1.2s ease-in-out;
        }

        /* ── Timeline ── */
        .timeline { position: relative; padding-left: 28px; }
        .timeline::before {
            content: ''; position: absolute; left: 8px; top: 0; bottom: 0;
            width: 2px; background: var(--accent);
        }
        .timeline-item {
            position: relative; margin-bottom: 2rem;
            padding: 1.2rem 1.4rem;
            background: var(--surface);
            border-radius: 10px;
            border-left: 3px solid var(--accent);
        }
        .timeline-item::before {
            content: ''; position: absolute;
            left: -33px; top: 1.5rem;
            width: 12px; height: 12px;
            background: var(--accent); border-radius: 50%;
            border: 2px solid var(--bg);
        }
        .timeline-item h4 {
            margin: 0 0 0.2rem 0; font-size: 1.15rem;
            color: var(--heading) !important;
        }
        .timeline-item .period {
            display: inline-block;
            background: var(--accent); color: var(--contrast);
            padding: 2px 10px; border-radius: 4px;
            font-size: 0.8rem; font-weight: 600;
            margin-bottom: 0.4rem; font-family: 'Poppins', sans-serif;
        }
        .timeline-item .org {
            font-style: italic; color: #9db8c7;
            font-size: 0.92rem; margin-bottom: 0.6rem;
        }
        .timeline-item ul { padding-left: 1.1rem; margin-top: 0.5rem; }
        .timeline-item li {
            font-size: 0.9rem; line-height: 1.55;
            margin-bottom: 0.35rem; color: var(--text);
        }

        /* ── Profile image ── */
        .profile-img {
            border-radius: 50%; border: 4px solid var(--accent);
            width: 160px; height: 160px; object-fit: cover;
            transition: transform 0.4s ease;
        }
        .profile-img:hover { transform: scale(1.05); }

        /* ── Hero profile image ── */
        .hero-profile-img {
            border-radius: 16px; border: none;
            max-width: 100%; height: auto;
            transition: transform 0.4s ease;
            box-shadow: none;
        }
        .hero-profile-img:hover { transform: scale(1.03); }

        /* ── About image ── */
        .about-img {
            border-radius: 14px; max-width: 100%; height: auto;
            box-shadow: 0 6px 24px rgba(19,135,193,0.15);
        }

        /* ── Social icons row ── */
        .social-row { display: flex; gap: 1rem; margin-top: 0.8rem; flex-wrap: wrap; }
        .social-icon {
            display: inline-flex; align-items: center; justify-content: center;
            width: 42px; height: 42px; border-radius: 50%;
            background: var(--surface); color: var(--accent) !important;
            font-size: 1.2rem; text-decoration: none !important;
            transition: all 0.3s ease; border: 1px solid rgba(19,135,193,0.3);
        }
        .social-icon:hover {
            background: var(--accent); color: var(--contrast) !important;
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(19,135,193,0.4);
        }

        /* ── Word cloud ── */
        .word-cloud { border-radius: 12px; max-width: 100%; }

        /* ── Typed animation ── */
        .typed-text {
            color: var(--accent);
            font-family: 'Raleway', sans-serif;
            font-weight: 700;
            font-size: 1.6rem;
        }
        .typed-cursor {
            color: var(--accent);
            font-size: 1.6rem;
            animation: blink 0.7s infinite;
        }
        @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }

        /* ── Quote ── */
        .newton-quote {
            font-style: italic; color: #9db8c7;
            font-size: 1.05rem; line-height: 1.65;
            border-left: 3px solid var(--accent);
            padding-left: 1rem; margin: 1.2rem 0;
        }
        .newton-quote .attribution {
            display: block; text-align: right;
            font-style: normal; font-weight: 600;
            color: var(--accent); margin-top: 0.5rem;
        }

        /* ── Section anchor scroll-margin ── */
        [id] { scroll-margin-top: 2rem; }

        /* ── Footer ── */
        .footer-container {
            text-align: center; padding: 2rem 0 1rem 0;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin-top: 3rem; color: #9db8c7;
        }

        /* ── Expander styling ── */
        details summary {
            font-family: 'Poppins', sans-serif;
            font-weight: 500; cursor: pointer;
            color: var(--accent) !important;
        }

        /* ── Tabs override ── */
        .stTabs [data-baseweb="tab-list"] button {
            font-family: 'Poppins', sans-serif !important;
            color: var(--text) !important;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 3. TYPED.JS ANIMATION (pure HTML/CSS/JS)
# ─────────────────────────────────────────────
def typed_animation():
    """Render a typed.js-style typewriter animation using st.components.v1.html (iframe with JS)."""
    import streamlit.components.v1 as components
    components.html(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap');
            body { margin: 0; padding: 0; background: transparent; overflow: hidden; }
            .typed-wrap {
                font-family: 'Raleway', sans-serif;
                display: flex; align-items: center;
            }
            .prefix {
                font-size: 1.6rem; color: #e7f2f7; white-space: nowrap;
            }
            .typed-output {
                color: #1387c1; font-weight: 700; font-size: 1.6rem;
                white-space: nowrap;
            }
            .cursor {
                color: #1387c1; font-size: 1.6rem; font-weight: 400;
                animation: blink 0.7s infinite;
            }
            @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }
        </style>
        <div class="typed-wrap">
            <span class="prefix">I am a&nbsp;</span>
            <span id="typed-output" class="typed-output"></span>
            <span class="cursor">|</span>
        </div>
        <script>
        (function(){
            const words = ["Coder", "Data Mercenary", "Geek"];
            let wordIdx = 0, charIdx = 0, deleting = false;
            const el = document.getElementById("typed-output");
            if (!el) return;
            function tick() {
                const word = words[wordIdx];
                if (deleting) {
                    el.textContent = word.substring(0, charIdx--);
                    if (charIdx < 0) { deleting = false; wordIdx = (wordIdx + 1) % words.length; }
                    setTimeout(tick, 50);
                } else {
                    el.textContent = word.substring(0, charIdx++);
                    if (charIdx > word.length) { deleting = true; setTimeout(tick, 1200); }
                    else { setTimeout(tick, 100); }
                }
            }
            tick();
        })();
        </script>
        """,
        height=50,
    )


# ─────────────────────────────────────────────
# 4. SKILL BAR COMPONENT
# ─────────────────────────────────────────────
def skill_bar(label: str, pct: int):
    st.markdown(
        f"""
        <div class="skill-bar-container">
            <div class="skill-bar-label"><span>{label}</span><span>{pct}%</span></div>
            <div class="skill-bar-track">
                <div class="skill-bar-fill" style="width:{pct}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 5. TIMELINE ITEM COMPONENT
# ─────────────────────────────────────────────
def timeline_item(title: str, period: str, org: str, desc: str, bullets: list[str] | None = None):
    bullets_html = ""
    if bullets:
        items = "".join(f"<li>{b}</li>" for b in bullets)
        bullets_html = f"<ul>{items}</ul>"
    st.markdown(
        f"""
        <div class="timeline-item">
            <h4>{title}</h4>
            <span class="period">{period}</span>
            <div class="org">{org}</div>
            <div style="font-size:0.92rem; color:var(--text); line-height:1.6;">{desc}</div>
            {bullets_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 6. SOCIAL LINKS ROW
# ─────────────────────────────────────────────
SOCIAL_LINKS = {
    "LinkedIn": ("https://www.linkedin.com/in/ganeshkedari", "🔗"),
    "GitHub": ("https://github.com/ganeshkedari/", "💻"),
    "X / Twitter": ("https://x.com/ganesh_kedari", "𝕏"),
    "Facebook": ("https://www.facebook.com/ganeshkedari", "📘"),
    "Instagram": ("https://instagram.com/ganeshkedari", "📷"),
}


def social_links_html(size: str = "42px") -> str:
    icons = {
        "LinkedIn": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/></svg>',
        "GitHub": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>',
        "X / Twitter": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865l8.875 11.633Z"/></svg>',
        "Facebook": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0 0 3.603 0 8.05 0 12.067 2.928 15.396 6.75 16v-5.624H4.718V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258V8.05h2.218l-.354 2.326H9.25V16c3.822-.604 6.75-3.934 6.75-7.951z"/></svg>',
        "Instagram": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/></svg>',
    }
    items = ""
    for name, (url, _) in SOCIAL_LINKS.items():
        svg = icons.get(name, "🔗")
        items += f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="social-icon" title="{name}">{svg}</a>'
    return f'<div class="social-row">{items}</div>'


# ═════════════════════════════════════════════
# MAIN APP
# ═════════════════════════════════════════════
def main():
    inject_css()

    # ── Sidebar ──────────────────────────────
    with st.sidebar:
        profile_b64 = img_to_base64("assets/profile.PNG")
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem 0;">
                <img src="data:image/png;base64,{profile_b64}" class="profile-img" alt="Ganesh Kedari">
                <h2 style="margin:0.8rem 0 0.1rem 0; font-size:1.4rem;">Ganesh Kedari</h2>
                <p style="color:#9db8c7; font-size:0.9rem; margin:0;">Solution Architect &bull; Data &amp; Analytics</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Sidebar navigation links (HTML anchors)
        st.markdown(
            """
            <style>
            .sidebar-nav a {
                display: block; padding: 0.45rem 0.8rem; margin-bottom: 0.3rem;
                border-radius: 6px; font-family: 'Poppins', sans-serif;
                font-size: 0.95rem; font-weight: 500;
                color: var(--text) !important; text-decoration: none !important;
                transition: all 0.25s ease;
            }
            .sidebar-nav a:hover {
                background: rgba(19,135,193,0.15);
                color: var(--accent) !important;
                padding-left: 1.1rem;
            }
            </style>
            <nav class="sidebar-nav">
                <a href="#home">🏠&ensp;Home</a>
                <a href="#experience">💼&ensp;Experience</a>
                <a href="#education">🎓&ensp;Education</a>
                <a href="#contact">📬&ensp;Contact</a>
            </nav>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Download Resume in sidebar
        pdf_bytes = get_pdf_bytes("assets/Ganesh_Kedari_Visual_CV.pdf")
        st.download_button(
            label="📥  Download Resume",
            data=pdf_bytes,
            file_name="Ganesh_Kedari_Visual_CV.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        st.markdown("---")

        # Social icons in sidebar
        st.markdown(social_links_html(), unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION: HOME / HERO
    # ─────────────────────────────────────────
    st.markdown('<div id="home"></div>', unsafe_allow_html=True)

    hero_left, hero_right = st.columns([3, 2], gap="large")

    with hero_left:
        st.markdown(
            """
            <h1 style="font-size:2.8rem; margin-bottom:0.2rem;">
                Hello, I'm <span style="color:var(--accent);">Ganesh Kedari</span>
            </h1>
            """,
            unsafe_allow_html=True,
        )

        typed_animation()

        st.markdown(
            """
            <div class="newton-quote">
                I do not know what I may appear to the world; but to myself I seem to have been only
                like a boy playing on the sea-shore, and diverting myself in now and then finding a
                smoother pebble or a prettier shell than ordinary, whilst the great ocean of truth
                lay all undiscovered before me.
                <span class="attribution">&mdash; Sir Isaac Newton</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="margin-top:1.2rem;">
                <a href="#experience" class="btn-primary-custom">View My Work</a>
                <a href="https://topmate.io/ganeshkedari/" target="_blank" rel="noopener noreferrer"
                   class="btn-outline-custom">Get In Touch</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        hero_b64 = img_to_base64("assets/profile.PNG")
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem;">
                <img src="data:image/png;base64,{hero_b64}" class="hero-profile-img" alt="Ganesh Kedari">
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION: EXPERIENCE
    # ─────────────────────────────────────────
    st.markdown('<div id="experience"></div>', unsafe_allow_html=True)
    st.markdown("## Professional Experience")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    timeline_item(
        title="Staff Architect",
        period="Nov 2019 – Present",
        org="IQVIA, Pune, India",
        desc=(
            "At IQVIA, I help Life Sciences organizations unlock the power of AI-powered, "
            "conversational analytics. Instead of just building tools, I focus on designing "
            "solutions that change the way business users interact with data and make decisions."
        ),
        bullets=[
            "Architected and deployed AI-driven analytics solutions that enabled pharma clients to ask questions in natural language and receive instant insights, improving decision-making speed.",
            "Built a scalable analytics framework for managing data pipelines and model training, reducing deployment time and boosting model accuracy.",
            "Integrated diverse data sources (SAP HANA, Snowflake, AWS Redshift, Azure CosmosDB, Databricks, Salesforce, VEEVA CRM) into unified analytics platforms, enhancing data accessibility and reporting precision.",
            "Developed and operationalized machine learning models for NLP, anomaly detection, and predictive insights, helping clients identify risks and opportunities earlier.",
            "Partnered with product teams and business stakeholders to co-create solutions that delivered measurable ROI and stronger adoption across global user bases.",
            "Streamlined DevOps integration using Kubernetes, Helm, and Grafana, improving reliability, scalability, and system monitoring.",
            "Created a reusable analytics artifacts library, cutting development effort by 20% across multiple projects.",
        ],
    )

    timeline_item(
        title="Solution Architect",
        period="2008 – 2019",
        org="IBM, Pune, India",
        desc=(
            "Progressed from Entry Level Engineer to System Scientist to Solution Architect, "
            "driving the evolution of IBM's analytics capabilities through client-focused innovation "
            "and scalable BI solutions. Designed and delivered enterprise-grade analytics architectures "
            "across global teams, integrating AI, DevOps, and big data technologies."
        ),
        bullets=[
            "Spearheaded end-to-end analytics solution design and delivery, progressing from System Scientist to Solution Architect within IBM's global Data & Analytics practice.",
            "Drove customer-centric product innovation by aligning real-world use cases with IBM Business Analytics roadmap, enhancing product relevance and adoption.",
            "Designed and implemented scalable BI architectures for global clients, using tools like Cognos, Power BI, and ELK to unify insights across complex data ecosystems.",
            "Architected AI-powered analytics frameworks on big data lakes, enabling procurement teams to improve operational efficiency and decision-making by 20%.",
            "Integrated analytics solutions with modern DevOps pipelines (Docker, Kubernetes, Jenkins), reducing deployment cycles and improving release reliability.",
            "Delivered strategic proofs-of-concept in data quality, automation, and mobile BI, directly influencing IBM Procurement's product development priorities.",
            "Collaborated cross-functionally with global clients to translate business needs into technical solutions, strengthening IBM's consulting and delivery capabilities.",
        ],
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION: EDUCATION
    # ─────────────────────────────────────────
    st.markdown('<div id="education"></div>', unsafe_allow_html=True)
    st.markdown("## Education")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    timeline_item(
        title="Master of Science — Scientific Computing",
        period="2006 – 2008",
        org="Savitribai Phule University, Pune, India",
        desc=(
            "Majoring in Scientific Computing with a concentration in High Performance Computing, "
            "Optimization Techniques, Unix Programming and Java, I have been exposed to all facets "
            "of software development life cycle. Throughout my collegiate career, I attempted to stay "
            "well-rounded combining academic excellence with leadership and work experience."
        ),
    )

    timeline_item(
        title="Bachelor of Computer Science",
        period="2003 – 2005",
        org="Savitribai Phule University, Pune, India",
        desc=(
            "Activities and societies: Represented College at various Technical Events, Member of "
            "National Service Scheme, Participated in National Level Republic Day Camp. "
            'Completed B.Sc. in Computer Science with "First class with Distinction".'
        ),
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION: CONTACT / FOOTER
    # ─────────────────────────────────────────
    st.markdown('<div id="contact"></div>', unsafe_allow_html=True)
    st.markdown("## Get In Touch")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <p style="font-size:1.05rem; max-width:600px;">
            I'm always open to discussing data architecture, AI strategy, or new opportunities.
            Feel free to reach out!
        </p>
        <div style="margin:1rem 0;">
            <a href="https://topmate.io/ganeshkedari/" target="_blank" rel="noopener noreferrer"
               class="btn-primary-custom" style="font-size:1.05rem; padding:0.65rem 2rem;">
               💬&ensp;Book a Conversation
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(social_links_html(), unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <div class="footer-container">
            <p>© Copyright <strong>Ganesh Kedari</strong> — All Rights Reserved</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
