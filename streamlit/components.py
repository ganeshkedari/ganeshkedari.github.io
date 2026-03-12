"""
components.py — Reusable UI Components for the Streamlit Resume App
====================================================================

This module provides self-contained, reusable UI building blocks that
are used by the main application (ganeshkedari.py).  Each function
renders a specific visual component using `st.markdown` (for HTML/CSS)
or `st.components.v1.html` (when JavaScript execution is required).

Components
----------
- typed_animation()   : Typewriter text effect ("Coder", "Data Mercenary", "Geek")
- skill_bar()         : Horizontal progress bar with label and percentage
- timeline_item()     : Card used in Experience / Education timelines
- social_links_html() : Row of circular social-media icon links

Dependencies
------------
- streamlit
- streamlit.components.v1  (for the typed animation iframe)
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


# ─────────────────────────────────────────────────────────────────────────────
# TYPED.JS-STYLE ANIMATION
# ─────────────────────────────────────────────────────────────────────────────
# Streamlit's st.markdown() strips <script> tags, so JavaScript-based
# animations must be rendered inside an iframe via st.components.v1.html().
# The component is fully self-contained: fonts, styles, and JS are all
# inlined inside the iframe document.
# ─────────────────────────────────────────────────────────────────────────────

def typed_animation(words: list[str] | None = None, height: int = 50) -> None:
    """
    Render a typewriter animation that cycles through a list of words.

    Parameters
    ----------
    words : list[str], optional
        Words to cycle through.  Defaults to ["Coder", "Data Mercenary", "Geek"].
    height : int
        Pixel height of the iframe.  50 px works well for a single line.
    """
    if words is None:
        words = ["Coder", "Data Mercenary", "Geek"]

    # Build a JS array literal from the Python list
    js_words = ", ".join(f'"{w}"' for w in words)

    components.html(
        f"""
        <style>
            /* Load Raleway inside the iframe so the font matches the main page */
            @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap');

            body {{
                margin: 0; padding: 0;
                background: transparent;   /* inherit dark bg from parent */
                overflow: hidden;           /* no scrollbars inside iframe */
            }}

            .typed-wrap {{
                font-family: 'Raleway', sans-serif;
                display: flex;
                align-items: center;
            }}

            /* Static prefix text */
            .prefix {{
                font-size: 1.6rem;
                color: #e7f2f7;              /* --text */
                white-space: nowrap;
            }}

            /* Dynamically typed text */
            .typed-output {{
                color: #1387c1;              /* --accent */
                font-weight: 700;
                font-size: 1.6rem;
                white-space: nowrap;
            }}

            /* Blinking cursor pipe */
            .cursor {{
                color: #1387c1;
                font-size: 1.6rem;
                font-weight: 400;
                animation: blink 0.7s infinite;
            }}

            @keyframes blink {{
                0%, 100% {{ opacity: 1; }}
                50%      {{ opacity: 0; }}
            }}
        </style>

        <div class="typed-wrap">
            <span class="prefix">I am a&nbsp;</span>
            <span id="typed-output" class="typed-output"></span>
            <span class="cursor">|</span>
        </div>

        <script>
        (function() {{
            // ── Configuration ──
            const words    = [{js_words}];
            const typeMs   = 100;   // milliseconds per character (typing)
            const deleteMs = 50;    // milliseconds per character (deleting)
            const pauseMs  = 1200;  // pause before deleting

            // ── State ──
            let wordIdx  = 0;
            let charIdx  = 0;
            let deleting = false;
            const el = document.getElementById("typed-output");
            if (!el) return;

            function tick() {{
                const word = words[wordIdx];

                if (deleting) {{
                    // Remove one character
                    el.textContent = word.substring(0, charIdx--);
                    if (charIdx < 0) {{
                        deleting = false;
                        wordIdx  = (wordIdx + 1) % words.length;
                    }}
                    setTimeout(tick, deleteMs);
                }} else {{
                    // Add one character
                    el.textContent = word.substring(0, charIdx++);
                    if (charIdx > word.length) {{
                        deleting = true;
                        setTimeout(tick, pauseMs);
                    }} else {{
                        setTimeout(tick, typeMs);
                    }}
                }}
            }}

            tick();  // start the animation loop
        }})();
        </script>
        """,
        height=height,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SKILL BAR
# ─────────────────────────────────────────────────────────────────────────────

def skill_bar(label: str, pct: int) -> None:
    """
    Render a horizontal progress bar with a label on the left and
    percentage on the right.

    Parameters
    ----------
    label : str   – Skill name (e.g. "Python | Databases").
    pct   : int   – Fill percentage (0–100).
    """
    st.markdown(
        f"""
        <div class="skill-bar-container">
            <div class="skill-bar-label">
                <span>{label}</span>
                <span>{pct}%</span>
            </div>
            <div class="skill-bar-track">
                <div class="skill-bar-fill" style="width:{pct}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# TIMELINE ITEM
# ─────────────────────────────────────────────────────────────────────────────

def timeline_item(
    title: str,
    period: str,
    org: str,
    desc: str,
    bullets: list[str] | None = None,
) -> None:
    """
    Render a single card in a vertical timeline (experience or education).

    Parameters
    ----------
    title   : str        – Job title or degree name.
    period  : str        – Date range shown as an accent-coloured badge.
    org     : str        – Company or institution name (shown in italics).
    desc    : str        – Paragraph describing the role.
    bullets : list[str]  – Optional list of achievement bullet points.
    """
    # Build the <ul> block only if bullets are provided
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
            <div style="font-size:0.92rem; color:var(--text); line-height:1.6;">
                {desc}
            </div>
            {bullets_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SOCIAL LINKS
# ─────────────────────────────────────────────────────────────────────────────

# SVG icons for each social platform (Bootstrap Icons style, 16×16/18×18)
_SOCIAL_SVGS: dict[str, str] = {
    "LinkedIn": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" '
        'fill="currentColor" viewBox="0 0 16 16"><path d="M0 1.146C0 .513.526 '
        "0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 "
        "1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 "
        "12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 "
        "1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 "
        "0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 "
        "8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 "
        "1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-"
        "1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 "
        "1.193v.025h-.016a5.54 5.54 0 0 1 "
        '.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/></svg>'
    ),
    "GitHub": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" '
        'fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 '
        "3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 "
        "0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-"
        ".82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 "
        "1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 "
        "0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 "
        ".67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 "
        ".27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 "
        "2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 "
        "3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 "
        ".21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"
        '"/></svg>'
    ),
    "X / Twitter": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
        'fill="currentColor" viewBox="0 0 16 16"><path d="M12.6.75h2.454l-'
        "5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-"
        "6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 "
        '2.145H2.865l8.875 11.633Z"/></svg>'
    ),
    "Facebook": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" '
        'fill="currentColor" viewBox="0 0 16 16"><path d="M16 8.049c0-4.446-'
        "3.582-8.05-8-8.05C3.58 0 0 3.603 0 8.05 0 12.067 2.928 15.396 "
        "6.75 16v-5.624H4.718V8.05H6.75V6.275c0-2.017 1.195-3.131 "
        "3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 "
        "0-1.303.621-1.303 1.258V8.05h2.218l-.354 2.326H9.25V16c3.822-"
        '.604 6.75-3.934 6.75-7.951z"/></svg>'
    ),
    "Instagram": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" '
        'fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C5.829 0 '
        "5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 "
        "0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 "
        "4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852"
        ".174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 "
        "1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 "
        "16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 "
        "3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509"
        ".332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-"
        ".048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 "
        "0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-"
        "1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c"
        "2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145"
        ".64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 "
        "1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035"
        ".78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-"
        ".546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-"
        "3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a"
        "2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-"
        ".24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136"
        ".008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-"
        ".64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276"
        ".738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 "
        "0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 "
        "8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 "
        '5.334 2.667 2.667 0 0 1 0-5.334z"/></svg>'
    ),
}


def social_links_html(links: dict[str, str] | None = None) -> str:
    """
    Build an HTML string containing a row of circular social-media icons.

    Parameters
    ----------
    links : dict[str, str], optional
        Mapping of platform name → URL.  Defaults to Ganesh's profiles.

    Returns
    -------
    str – HTML ready for st.markdown(…, unsafe_allow_html=True).
    """
    if links is None:
        links = {
            "LinkedIn":    "https://www.linkedin.com/in/ganeshkedari",
            "GitHub":      "https://github.com/ganeshkedari/",
            "X / Twitter": "https://x.com/ganesh_kedari",
            "Facebook":    "https://www.facebook.com/ganeshkedari",
            "Instagram":   "https://instagram.com/ganeshkedari",
        }

    items = ""
    for name, url in links.items():
        svg = _SOCIAL_SVGS.get(name, "🔗")
        items += (
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            f'class="social-icon" title="{name}">{svg}</a>'
        )
    return f'<div class="social-row">{items}</div>'
