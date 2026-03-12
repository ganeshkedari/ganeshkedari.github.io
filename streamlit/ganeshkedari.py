"""
ganeshkedari.py — Streamlit Interactive Resume Application
===========================================================

ENTRY POINT for the Streamlit app.

This is a single-page, dark-themed interactive resume for Ganesh Kedari.
It mirrors the look and feel of the original portfolio website
(ganeshkedari.github.io) using custom CSS and reusable components.

Architecture
------------
The app is split into four files for maintainability:

  ganeshkedari.py   ← YOU ARE HERE (layout & page orchestration)
  components.py     ← Reusable UI widgets (typed animation, timeline, etc.)
  data.py           ← All resume content & personal details
  style.css         ← External stylesheet (injected at runtime)

How to run
----------
    cd streamlit
    # activate virtual environment first (venv/Scripts/activate on Windows)
    streamlit run ganeshkedari.py

Folder structure
----------------
    streamlit/
    ├── .streamlit/config.toml   # Streamlit theme (dark palette)
    ├── ganeshkedari.py          # ← this file
    ├── components.py            # reusable UI components
    ├── data.py                  # resume content / data
    ├── style.css                # external CSS stylesheet
    ├── requirements.txt         # Python dependencies
    ├── assets/                  # images & documents (self-contained)
    │   ├── profile.PNG
    │   ├── r2d2.png
    │   └── Ganesh_Kedari_Visual_CV.pdf
    └── venv/                    # Python virtual environment (git-ignored)
"""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

# ── Local modules ────────────────────────────────────────────────────────────
from components import typed_animation, timeline_item, social_links_html
from data import PERSONAL, SOCIAL_LINKS, EXPERIENCE, EDUCATION, ASSET_PATHS


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# Resolve the directory that contains this script.
# All asset paths are relative to this directory, which ensures the app
# works correctly regardless of the working directory (local dev vs.
# Streamlit Cloud where cwd is the repository root).
BASE_DIR = Path(__file__).resolve().parent


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION  (must be the first Streamlit command)
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=f"{PERSONAL['name']} | Resume",
    page_icon=str(BASE_DIR / ASSET_PATHS["favicon"]),
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def _asset(relative_path: str) -> Path:
    """Resolve an asset path relative to the script directory."""
    return BASE_DIR / relative_path


def img_to_base64(relative_path: str) -> str:
    """
    Read an image file and return its contents as a base64-encoded string.

    This is used to embed images directly into HTML via data-URIs,
    avoiding cross-origin or path-resolution issues in Streamlit.
    """
    return base64.b64encode(_asset(relative_path).read_bytes()).decode()


def get_pdf_bytes(relative_path: str) -> bytes:
    """Read a file and return its raw bytes (for st.download_button)."""
    return _asset(relative_path).read_bytes()


def load_css(css_file: str = "style.css") -> None:
    """
    Read an external CSS file and inject it into the Streamlit app via
    st.markdown with unsafe_allow_html=True.

    This keeps all styling in a dedicated .css file for easier editing.
    """
    css_text = _asset(css_file).read_text(encoding="utf-8")
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE SECTIONS
# Each section is a standalone function that renders one part of the page.
# They are called sequentially in main() to compose the full layout.
# ═════════════════════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar() -> None:
    """
    Render the left sidebar containing:
      - Profile photo (circular, accent-bordered)
      - Name and short title
      - Navigation anchor links
      - Resume download button
      - Social media icons
    """
    with st.sidebar:

        # -- Profile card --------------------------------------------------
        # Encode the profile image as base64 so it can be embedded directly
        # in an <img> tag without relying on Streamlit's static file serving.
        profile_b64 = img_to_base64(ASSET_PATHS["profile_img"])
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem 0;">
                <img src="data:image/png;base64,{profile_b64}"
                     class="profile-img" alt="{PERSONAL['name']}">
                <h2 style="margin:0.8rem 0 0.1rem 0; font-size:1.4rem;">
                    {PERSONAL['name']}
                </h2>
                <p style="color:#9db8c7; font-size:0.9rem; margin:0;">
                    {PERSONAL['title']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # -- Navigation links ----------------------------------------------
        # Uses plain HTML anchor links (<a href="#section">) that scroll the
        # main content area to the corresponding section.  The sidebar-nav
        # CSS class is defined in style.css.
        st.markdown(
            """
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

        # -- Resume PDF download -------------------------------------------
        # st.download_button serves the file directly from memory.
        pdf_bytes = get_pdf_bytes(ASSET_PATHS["resume_pdf"])
        st.download_button(
            label="📥  Download Resume",
            data=pdf_bytes,
            file_name="Ganesh_Kedari_Visual_CV.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        st.markdown("---")

        # -- Social media icons --------------------------------------------
        # Rendered as inline SVGs wrapped in circular <a> links.
        st.markdown(social_links_html(SOCIAL_LINKS), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────────────────────────────────────

def render_hero() -> None:
    """
    Render the hero / landing area:
      - Large greeting with name highlighted in accent colour
      - Typewriter animation cycling through tagline words
      - Inspirational quote
      - CTA buttons ("View My Work", "Get In Touch")
      - Profile image on the right
    """
    # Anchor for sidebar navigation
    st.markdown('<div id="home"></div>', unsafe_allow_html=True)

    # Two-column layout: text (60%) | image (40%)
    hero_left, hero_right = st.columns([3, 2], gap="large")

    with hero_left:
        # -- Greeting ------------------------------------------------------
        st.markdown(
            f"""
            <h1 style="font-size:2.8rem; margin-bottom:0.2rem;">
                Hello, I'm
                <span style="color:var(--accent);">{PERSONAL['name']}</span>
            </h1>
            """,
            unsafe_allow_html=True,
        )

        # -- Typewriter animation ------------------------------------------
        # Renders inside an iframe (st.components.v1.html) because
        # st.markdown strips <script> tags.  See components.py.
        typed_animation(words=PERSONAL["typed_words"])

        # -- Quote ---------------------------------------------------------
        st.markdown(
            f"""
            <div class="newton-quote">
                {PERSONAL['quote']}
                <span class="attribution">
                    &mdash; {PERSONAL['quote_author']}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -- Call-to-action buttons ----------------------------------------
        st.markdown(
            f"""
            <div style="margin-top:1.2rem;">
                <a href="#experience" class="btn-primary-custom">
                    View My Work
                </a>
                <a href="{PERSONAL['contact_url']}"
                   target="_blank" rel="noopener noreferrer"
                   class="btn-outline-custom">
                    Get In Touch
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        # -- Profile image (rounded rectangle, no border) ------------------
        hero_b64 = img_to_base64(ASSET_PATHS["profile_img"])
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem;">
                <img src="data:image/png;base64,{hero_b64}"
                     class="hero-profile-img"
                     alt="{PERSONAL['name']}">
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# EXPERIENCE SECTION
# ─────────────────────────────────────────────────────────────────────────────

def render_experience() -> None:
    """
    Render the Professional Experience section.

    Each role is displayed as a timeline card with a coloured dot,
    date badge, description, and bullet-point achievements.
    Data is sourced from data.EXPERIENCE (list of dicts).
    """
    # Anchor for sidebar navigation
    st.markdown('<div id="experience"></div>', unsafe_allow_html=True)
    st.markdown("## Professional Experience")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Open the timeline wrapper (applies the vertical line via CSS)
    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    # Iterate over experience entries defined in data.py
    for entry in EXPERIENCE:
        timeline_item(
            title=entry["title"],
            period=entry["period"],
            org=entry["org"],
            desc=entry["desc"],
            bullets=entry.get("bullets"),
        )

    # Close the timeline wrapper
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# EDUCATION SECTION
# ─────────────────────────────────────────────────────────────────────────────

def render_education() -> None:
    """
    Render the Education section.

    Each qualification is displayed as a timeline card.
    Data is sourced from data.EDUCATION (list of dicts).
    """
    # Anchor for sidebar navigation
    st.markdown('<div id="education"></div>', unsafe_allow_html=True)
    st.markdown("## Education")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for entry in EDUCATION:
        timeline_item(
            title=entry["title"],
            period=entry["period"],
            org=entry["org"],
            desc=entry["desc"],
            bullets=entry.get("bullets"),
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT / FOOTER SECTION
# ─────────────────────────────────────────────────────────────────────────────

def render_contact() -> None:
    """
    Render the contact call-to-action and footer:
      - Brief blurb inviting conversation
      - "Book a Conversation" button (links to topmate.io)
      - Social media icon row
      - Copyright line
    """
    st.markdown('<div id="contact"></div>', unsafe_allow_html=True)
    st.markdown("## Get In Touch")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -- Contact blurb & CTA button ----------------------------------------
    st.markdown(
        f"""
        <p style="font-size:1.05rem; max-width:600px;">
            {PERSONAL['contact_blurb']}
        </p>
        <div style="margin:1rem 0;">
            <a href="{PERSONAL['contact_url']}"
               target="_blank" rel="noopener noreferrer"
               class="btn-primary-custom"
               style="font-size:1.05rem; padding:0.65rem 2rem;">
               💬&ensp;Book a Conversation
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -- Social icons (same row as used in sidebar) ------------------------
    st.markdown(social_links_html(SOCIAL_LINKS), unsafe_allow_html=True)

    # -- Footer / copyright ------------------------------------------------
    st.markdown(
        f"""
        <div class="footer-container">
            <p>{PERSONAL['copyright']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# MAIN — Orchestrate the full page
# ═════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Compose the full single-page resume by calling each section renderer
    in order.  The CSS is loaded first to ensure styles are available
    before any HTML is rendered.

    Execution flow:
      1. load_css()          → inject style.css
      2. render_sidebar()    → navigation + download + social links
      3. render_hero()       → greeting, typed animation, quote, CTA
      4. render_experience() → professional timeline
      5. render_education()  → academic timeline
      6. render_contact()    → contact CTA + footer
    """
    # 1. Inject the external stylesheet
    load_css("style.css")

    # 2. Render sidebar (navigation, download, social links)
    render_sidebar()

    # 3. Render main-content sections top-to-bottom
    render_hero()
    render_experience()
    render_education()
    render_contact()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point — run only when executed directly by Streamlit
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
