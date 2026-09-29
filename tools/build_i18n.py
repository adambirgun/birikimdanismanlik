# -*- coding: utf-8 -*-
"""Generate multilingual static pages for Birikim Danışmanlık."""
from __future__ import annotations

import html
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://birikimedu.com"
PAGES = ["index.html", "hakkimizda.html", "hizmetlerimiz.html", "iletisim.html", "404.html"]
LANGS = ["tr", "en", "es", "de", "fr", "ru"]
OG_LOCALES = {
    "tr": "tr_TR",
    "en": "en_US",
    "es": "es_ES",
    "de": "de_DE",
    "fr": "fr_FR",
    "ru": "ru_RU",
}
AVAILABLE_LANGS = ["Turkish", "English", "Spanish", "German", "French", "Russian"]

ICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' fill='%230a65db'/%3E"
    "%3Ccircle cx='16' cy='16' r='7' fill='%23fff9f0'/%3E"
    "%3Ccircle cx='16' cy='16' r='3' fill='%23000609'/%3E%3C/svg%3E"
)

BAUHAUS = {
    "a": """<div class="bauhaus">
                <div class="bh-blue-sq"></div><div class="bh-eye"></div><div class="bh-red-circle"></div>
                <div class="bh-checker"></div><div class="bh-pink-rect"></div><div class="bh-yellow-semi"></div>
                <div class="bh-blue-tri"></div><div class="bh-yellow-sq"></div><div class="bh-red-sq"></div>
                <div class="bh-starburst"></div></div>""",
    "b": """<div class="bauhaus bauhaus-b">
                <div class="bh-pink-rect"></div><div class="bh-red-circle"></div><div class="bh-checker"></div>
                <div class="bh-blue-sq"></div><div class="bh-yellow-sq"></div><div class="bh-starburst"></div></div>""",
    "c": """<div class="bauhaus bauhaus-c">
                <div class="bh-yellow-sq"></div><div class="bh-blue-sq"></div><div class="bh-red-circle"></div>
                <div class="bh-checker"></div><div class="bh-pink-rect"></div><div class="bh-eye"></div></div>""",
}

ERROR_STYLE = """
  <style>
    .error-page { padding: 48px 0 96px; }
    .error-grid { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: clamp(32px,6vw,80px); align-items: center; }
    .error-code { font-family: var(--font-display); font-weight: 600; font-size: clamp(72px,16vw,140px); line-height: 0.95; letter-spacing: -0.03em; color: var(--color-signal-blue); margin-bottom: 8px; }
    .error-links { display: flex; flex-direction: column; gap: 10px; margin-top: 28px; max-width: 420px; }
    .error-links a { font-weight: 600; padding: 10px 0; border-bottom: 1px solid rgba(26,28,30,0.12); }
    .error-links a:hover { color: var(--color-signal-blue); }
    @media (max-width: 860px) { .error-grid { grid-template-columns: minmax(0,1fr); } }
  </style>"""


def e(s: str) -> str:
    return html.escape(s, quote=True)


def asset(lang: str) -> str:
    return "../assets" if lang != "tr" else "assets"


def page_url(lang: str, page: str) -> str:
    if lang == "tr":
        return f"{BASE}/" if page == "index.html" else f"{BASE}/{page}"
    return f"{BASE}/{lang}/" if page == "index.html" else f"{BASE}/{lang}/{page}"


def href_to(target_lang: str, page: str, from_lang: str) -> str:
    """Relative URL to the same logical page in another language."""
    if page == "index.html":
        if from_lang == "tr":
            return "./" if target_lang == "tr" else f"{target_lang}/"
        return "../" if target_lang == "tr" else f"../{target_lang}/"
    if from_lang == "tr":
        return page if target_lang == "tr" else f"{target_lang}/{page}"
    if target_lang == "tr":
        return f"../{page}"
    return f"../{target_lang}/{page}"


def hreflang(page: str) -> str:
    lines = [f'  <link rel="alternate" hreflang="{lang}" href="{page_url(lang, page)}">' for lang in LANGS]
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{page_url("tr", page)}">')
    return "\n".join(lines)


def lang_switch(lang: str, page: str, label: str) -> str:
    """Nav-style language links (no <select>) — matches Earlydog header, works without JS."""
    parts = []
    for code, name in [("tr", "TR"), ("en", "EN"), ("es", "ES"), ("de", "DE"), ("fr", "FR"), ("ru", "RU")]:
        href = href_to(code, page, lang)
        active = ' class="is-active" aria-current="true"' if code == lang else ""
        parts.append(
            f'<a href="{href}" hreflang="{code}" lang="{code}" data-lang="{code}"{active}>{name}</a>'
        )
    return (
        f'<nav class="lang-switch" aria-label="{e(label)}">'
        + "".join(parts)
        + "</nav>"
    )


def header(t: dict, lang: str, page: str, active: str, ghost_href: str | None = None, ghost_text: str | None = None) -> str:
    a = asset(lang)
    gh = ghost_href or "iletisim.html"
    gt = ghost_text or t["nav_cta"]
    return f"""  <div class="nav-backdrop" id="nav-backdrop"></div>
  <header class="site-header">
    <div class="header-inner">
      <a href="index.html" class="logo" aria-label="{e(t['logo_aria'])}">
        <img class="logo-img" src="{a}/images/brand/logo.png" width="96" height="96" alt="Birikim Danışmanlık">
      </a>
      <nav class="main-nav" id="main-nav" aria-label="{e(t['nav_aria'])}">
        <a href="index.html"{' class="active"' if active == 'home' else ''}>{e(t['nav_home'])}</a>
        <a href="hakkimizda.html"{' class="active"' if active == 'about' else ''}>{e(t['nav_about'])}</a>
        <a href="hizmetlerimiz.html"{' class="active"' if active == 'services' else ''}>{e(t['nav_services'])}</a>
        <a href="iletisim.html"{' class="active"' if active == 'contact' else ''}>{e(t['nav_contact'])}</a>
        <a class="nav-cta" href="iletisim.html">{e(t['nav_cta'])}</a>
      </nav>
      {lang_switch(lang, page, t['lang_label'])}
      <a class="ghost-link" href="{gh}">{e(gt)}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="{e(t['menu_open'])}">
        <span></span><span></span>
      </button>
    </div>
  </header>"""


def footer(t: dict, lang: str, short: bool = False) -> str:
    a = asset(lang)
    blurb = t["footer_blurb_short"] if short else t["footer_blurb"]
    return f"""  <footer class="site-footer">
    <div class="site-shell">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="index.html" class="logo">
            <img class="logo-img" src="{a}/images/brand/logo.png" width="72" height="72" alt="Birikim Danışmanlık">
          </a>
          <p class="fit-text">{e(blurb)}</p>
        </div>
        <div class="footer-col">
          <h3>{e(t['footer_pages'])}</h3>
          <a href="index.html">{e(t['nav_home'])}</a>
          <a href="hakkimizda.html">{e(t['nav_about'])}</a>
          <a href="hizmetlerimiz.html">{e(t['nav_services'])}</a>
          <a href="iletisim.html">{e(t['nav_contact'])}</a>
        </div>
        <div class="footer-col">
          <h3>{e(t['footer_contact'])}</h3>
          <p>Alanya, Antalya</p>
          <a href="mailto:info@birikimedu.com">info@birikimedu.com</a>
          <p>{e(t['footer_hours'])}</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Birikim Danışmanlık</p>
        <p>birikimedu.com</p>
      </div>
    </div>
  </footer>"""


def cookie(t: dict) -> str:
    return f"""  <div class="cookie-bar" id="cookie-bar" role="dialog" aria-label="{e(t['cookie_aria'])}">
    <p class="fit-text">{e(t['cookie_text'])}</p>
    <div class="cookie-actions">
      <button type="button" class="btn" id="cookie-essential">{e(t['cookie_essential'])}</button>
      <button type="button" class="btn" id="cookie-accept">{e(t['cookie_accept'])}</button>
    </div>
  </div>"""


def head_common(lang: str, page: str, title: str, description: str, a: str, extra: str = "", robots: str | None = None) -> str:
    rob = robots or "index, follow"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{page_url(lang, page)}">
  <meta name="robots" content="{rob}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#fff9f0">
{hreflang(page)}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{OG_LOCALES[lang]}">
  <meta property="og:site_name" content="Birikim Danışmanlık">
  <meta property="og:image" content="{BASE}/assets/images/og/og-image.png">
  <link rel="icon" href="{ICON}">
  <link rel="stylesheet" href="{a}/css/style.css">
{extra}</head>"""


def render_index(T: dict, lang: str) -> str:
    t = T[lang]
    p = t["index"]
    a = asset(lang)
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
            for q, ans in p["faq_ld"]
        ],
    }
    org_ld = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "Birikim Danışmanlık",
        "alternateName": "Birikim Büyükgebiz",
        "url": BASE,
        "logo": f"{BASE}/assets/images/brand/logo.png",
        "image": f"{BASE}/assets/images/og/og-image.png",
        "description": p["org_description"],
        "email": "info@birikimedu.com",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Alanya",
            "addressRegion": "Antalya",
            "addressCountry": "TR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 36.5438, "longitude": 31.9998},
        "areaServed": [
            {"@type": "City", "name": "Alanya"},
            {"@type": "Country", "name": "Turkey"},
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "email": "info@birikimedu.com",
            "availableLanguage": AVAILABLE_LANGS,
            "areaServed": "TR",
        },
        "founder": {"@type": "Person", "name": "Birikim Büyükgebiz"},
    }
    import json

    extra = f"""  <meta property="og:title" content="{e(p['og_title'])}">
  <meta property="og:description" content="{e(p['og_description'])}">
  <meta property="og:url" content="{page_url(lang, 'index.html')}">
  <script type="application/ld+json">
{json.dumps(org_ld, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False, indent=2)}
  </script>
"""
    faqs = "\n".join(
        f"""              <details class="faq-item">
                <summary class="fit-text">{e(q)}</summary>
                <p class="fit-text">{e(ans)}</p>
              </details>"""
        for q, ans in p["faq"]
    )
    body = f"""<body>
{header(t, lang, 'index.html', 'home')}
<main>
        <section class="hero">
          <div class="site-shell hero-grid">
            <div class="hero-copy">
              <h1 class="display fit-text">
                {e(p['hero_h1_a'])}
                <span class="accent">{e(p['hero_h1_b'])}</span>
              </h1>
              <p class="lede fit-text">{e(p['hero_lede'])}</p>
              <div class="btn-row">
                <a href="iletisim.html" class="btn">{e(p['btn_eval'])}</a>
                <a href="hizmetlerimiz.html" class="btn">{e(p['btn_services'])}</a>
              </div>
            </div>
            <div class="feature-visual" aria-hidden="true">{BAUHAUS['a']}</div>
          </div>
        </section>
        <section class="feature" aria-labelledby="uni-title">
          <div class="site-shell feature-grid">
            <div class="feature-copy">
              <span class="eyebrow">{e(p['uni_eye'])}</span>
              <h2 id="uni-title" class="heading fit-text">{e(p['uni_h2'])}</h2>
              <p class="lede fit-text">{e(p['uni_p'])}</p>
              <div class="btn-row"><a href="hizmetlerimiz.html" class="btn">{e(p['uni_btn'])}</a></div>
            </div>
            <div class="feature-visual" aria-hidden="true">{BAUHAUS['b']}</div>
          </div>
        </section>
        <section class="feature" aria-labelledby="lang-title">
          <div class="site-shell feature-grid is-reverse">
            <div class="feature-copy">
              <span class="eyebrow">{e(p['lang_eye'])}</span>
              <h2 id="lang-title" class="heading fit-text">{e(p['lang_h2'])}</h2>
              <p class="lede fit-text">{e(p['lang_p'])}</p>
              <div class="btn-row"><a href="hizmetlerimiz.html" class="btn">{e(p['lang_btn'])}</a></div>
            </div>
            <div class="feature-visual" aria-hidden="true">{BAUHAUS['c']}</div>
          </div>
        </section>
        <section class="feature" aria-labelledby="why-title">
          <div class="site-shell feature-grid">
            <div class="feature-copy">
              <span class="eyebrow">{e(p['why_eye'])}</span>
              <h2 id="why-title" class="heading fit-text">{e(p['why_h2'])}</h2>
              <p class="lede fit-text">{e(p['why_p'])}</p>
              <div class="btn-row"><a href="hakkimizda.html" class="btn">{e(p['why_btn'])}</a></div>
            </div>
            <div class="feature-visual" aria-hidden="true">{BAUHAUS['a']}</div>
          </div>
        </section>
        <section class="section" aria-labelledby="countries-title">
          <div class="site-shell">
            <div class="section-intro">
              <span class="eyebrow">{e(p['countries_eye'])}</span>
              <h2 id="countries-title" class="heading fit-text">{e(p['countries_h2'])}</h2>
              <p class="lede fit-text">{e(p['countries_p'])}</p>
            </div>
            <div class="country-row">
              <article class="country-item"><span class="meta">{e(p['es_meta'])}</span><h3 class="fit-text">{e(p['es_h3'])}</h3><p class="fit-text">{e(p['es_p'])}</p></article>
              <article class="country-item"><span class="meta">{e(p['fr_meta'])}</span><h3 class="fit-text">{e(p['fr_h3'])}</h3><p class="fit-text">{e(p['fr_p'])}</p></article>
              <article class="country-item"><span class="meta">{e(p['uk_meta'])}</span><h3 class="fit-text">{e(p['uk_h3'])}</h3><p class="fit-text">{e(p['uk_p'])}</p></article>
            </div>
          </div>
        </section>
        <section class="section" aria-labelledby="faq-title">
          <div class="site-shell">
            <div class="section-intro">
              <span class="eyebrow">{e(p['faq_eye'])}</span>
              <h2 id="faq-title" class="heading fit-text">{e(p['faq_h2'])}</h2>
            </div>
            <div class="faq-list">{faqs}</div>
          </div>
        </section>
        <section class="cta-band" aria-labelledby="cta-title">
          <div class="site-shell">
            <div class="cta-panel">
              <div>
                <h2 id="cta-title" class="heading fit-text">{e(p['cta_h2'])}</h2>
                <p class="lede fit-text">{e(p['cta_p'])}</p>
                <div class="btn-row">
                  <a href="iletisim.html" class="btn">{e(p['cta_form'])}</a>
                  <a href="mailto:info@birikimedu.com" class="ghost-link">{e(p['cta_mail'])}</a>
                </div>
              </div>
              <div class="cta-art" aria-hidden="true"><div class="bauhaus bauhaus-b" style="max-width:280px">
                <div class="bh-blue-sq"></div><div class="bh-red-circle"></div><div class="bh-checker"></div>
                <div class="bh-yellow-sq"></div><div class="bh-pink-rect"></div></div></div>
            </div>
          </div>
        </section>
</main>
{footer(t, lang)}
{cookie(t)}
  <script src="{a}/js/script.js" defer></script>
</body>
</html>"""
    return head_common(lang, "index.html", p["title"], p["description"], a, extra) + "\n" + body


def render_about(T: dict, lang: str) -> str:
    t = T[lang]
    p = t["about"]
    a = asset(lang)
    extra = f"""  <meta property="og:title" content="{e(p['og_title'])}">
  <meta property="og:description" content="{e(p['og_description'])}">
  <meta property="og:url" content="{page_url(lang, 'hakkimizda.html')}">
"""
    body = f"""<body>
{header(t, lang, 'hakkimizda.html', 'about')}
<main>
        <section class="page-hero">
          <div class="site-shell">
            <span class="eyebrow">{e(p['eye'])}</span>
            <h1 class="heading fit-text">{e(p['h1'])}</h1>
            <p class="lede fit-text">{e(p['lede'])}</p>
          </div>
        </section>
        <section class="section" style="padding-top:0">
          <div class="site-shell">
            <div class="feature-grid">
              <div class="content-copy">
                <p class="fit-text">{e(p['p1'])}</p>
                <p class="fit-text">{e(p['p2'])}</p>
              </div>
              <div class="feature-visual" aria-hidden="true">{BAUHAUS['c']}</div>
            </div>
            <div class="mission-grid">
              <article class="mission-card"><h3 class="fit-text">{e(p['promise_h'])}</h3><p class="fit-text">{e(p['promise_p'])}</p></article>
              <article class="mission-card"><h3 class="fit-text">{e(p['not_h'])}</h3><p class="fit-text">{e(p['not_p'])}</p></article>
            </div>
            <div class="content-copy" style="margin-top:64px">
              <h2 class="fit-text">{e(p['process_h'])}</h2>
              <p class="fit-text">{e(p['process_p'])}</p>
              <p class="fit-text">{e(p['process_p2'])}</p>
            </div>
          </div>
        </section>
        <section class="cta-band">
          <div class="site-shell">
            <div class="cta-panel">
              <div>
                <h2 class="heading fit-text">{e(p['cta_h'])}</h2>
                <p class="lede fit-text">{e(p['cta_p'])}</p>
                <div class="btn-row"><a href="iletisim.html" class="btn">{e(p['cta_btn'])}</a></div>
              </div>
              <div class="cta-art" aria-hidden="true"><div class="bauhaus" style="max-width:280px">
                <div class="bh-blue-sq"></div><div class="bh-red-circle"></div><div class="bh-checker"></div><div class="bh-yellow-sq"></div></div></div>
            </div>
          </div>
        </section>
</main>
{footer(t, lang, short=True)}
{cookie(t)}
  <script src="{a}/js/script.js" defer></script>
</body>
</html>"""
    return head_common(lang, "hakkimizda.html", p["title"], p["description"], a, extra) + "\n" + body


def render_services(T: dict, lang: str) -> str:
    t = T[lang]
    p = t["services"]
    a = asset(lang)
    extra = f"""  <meta property="og:title" content="{e(p['og_title'])}">
  <meta property="og:description" content="{e(p['og_description'])}">
  <meta property="og:url" content="{page_url(lang, 'hizmetlerimiz.html')}">
"""
    blocks = []
    for title, para, items in p["blocks"]:
        lis = "\n".join(f'<li class="fit-text">{e(i)}</li>' for i in items)
        blocks.append(
            f"""            <article class="service-block">
              <h2 class="fit-text">{e(title)}</h2>
              <div>
                <p class="fit-text">{e(para)}</p>
                <ul>{lis}</ul>
              </div>
            </article>"""
        )
    body = f"""<body>
{header(t, lang, 'hizmetlerimiz.html', 'services')}
<main>
        <section class="page-hero">
          <div class="site-shell">
            <span class="eyebrow">{e(p['eye'])}</span>
            <h1 class="heading fit-text">{e(p['h1'])}</h1>
            <p class="lede fit-text">{e(p['lede'])}</p>
          </div>
        </section>
        <section class="section" style="padding-top:0">
          <div class="site-shell">
{chr(10).join(blocks)}
          </div>
        </section>
        <section class="cta-band">
          <div class="site-shell">
            <div class="cta-panel">
              <div>
                <h2 class="heading fit-text">{e(p['cta_h'])}</h2>
                <p class="lede fit-text">{e(p['cta_p'])}</p>
                <div class="btn-row"><a href="iletisim.html" class="btn">{e(p['cta_btn'])}</a></div>
              </div>
              <div class="cta-art" aria-hidden="true"><div class="bauhaus bauhaus-b" style="max-width:280px">
                <div class="bh-pink-rect"></div><div class="bh-red-circle"></div><div class="bh-blue-sq"></div><div class="bh-checker"></div></div></div>
            </div>
          </div>
        </section>
</main>
{footer(t, lang, short=True)}
{cookie(t)}
  <script src="{a}/js/script.js" defer></script>
</body>
</html>"""
    return head_common(lang, "hizmetlerimiz.html", p["title"], p["description"], a, extra) + "\n" + body


def render_contact(T: dict, lang: str) -> str:
    t = T[lang]
    p = t["contact"]
    a = asset(lang)
    import json

    ld = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": p["ld_name"],
        "url": page_url(lang, "iletisim.html"),
        "mainEntity": {
            "@type": "EducationalOrganization",
            "name": "Birikim Danışmanlık",
            "email": "info@birikimedu.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Alanya",
                "addressRegion": "Antalya",
                "addressCountry": "TR",
            },
        },
    }
    extra = f"""  <meta property="og:title" content="{e(p['og_title'])}">
  <meta property="og:description" content="{e(p['og_description'])}">
  <meta property="og:url" content="{page_url(lang, 'iletisim.html')}">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
"""
    body = f"""<body>
{header(t, lang, 'iletisim.html', 'contact', ghost_href='mailto:info@birikimedu.com', ghost_text=p['ghost'])}
<main>
        <section class="page-hero">
          <div class="site-shell">
            <span class="eyebrow">{e(p['eye'])}</span>
            <h1 class="heading fit-text">{e(p['h1'])}</h1>
            <p class="lede fit-text">{e(p['lede'])}</p>
          </div>
        </section>
        <section class="section" style="padding-top:0">
          <div class="site-shell contact-grid">
            <div>
              <h2 class="heading fit-text" style="font-size:clamp(28px,4vw,40px)">{e(p['what_h'])}</h2>
              <p class="lede fit-text">{e(p['what_p'])}</p>
              <div class="contact-facts">
                <div class="contact-fact">
                  <div class="icon" aria-hidden="true"><svg viewBox="0 0 122.88 88.86" xmlns="http://www.w3.org/2000/svg"><path d="M7.05,0H115.83a7.07,7.07,0,0,1,7,7.05V81.81a7,7,0,0,1-1.22,4,2.78,2.78,0,0,1-.66,1,2.62,2.62,0,0,1-.66.46,7,7,0,0,1-4.51,1.65H7.05a7.07,7.07,0,0,1-7-7V7.05A7.07,7.07,0,0,1,7.05,0Zm-.3,78.84L43.53,40.62,6.75,9.54v69.3ZM49.07,45.39,9.77,83.45h103L75.22,45.39l-11,9.21h0a2.7,2.7,0,0,1-3.45,0L49.07,45.39Zm31.6-4.84,35.46,38.6V9.2L80.67,40.55ZM10.21,5.41,62.39,47.7,112.27,5.41Z"/></svg></div>
                  <div><strong class="fit-text">{e(p['email_l'])}</strong><a class="fit-text" href="mailto:info@birikimedu.com">info@birikimedu.com</a></div>
                </div>
                <div class="contact-fact">
                  <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#fff9f0" d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg></div>
                  <div><strong class="fit-text">{e(p['loc_l'])}</strong><span class="fit-text">{e(p['loc_v'])}</span></div>
                </div>
                <div class="contact-fact">
                  <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#fff9f0" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4V7h-2v7h6v-2h-4z"/></svg></div>
                  <div><strong class="fit-text">{e(p['time_l'])}</strong><span class="fit-text">{e(p['time_v'])}</span></div>
                </div>
                <div class="contact-fact">
                  <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#fff9f0" d="M6 2h9l5 5v15H6V2zm8 1.5V8h4.5L14 3.5zM8 12h8v1.5H8V12zm0 4h8v1.5H8V16z"/></svg></div>
                  <div><strong class="fit-text">{e(p['apt_l'])}</strong><span class="fit-text">{e(p['apt_v'])}</span></div>
                </div>
              </div>
            </div>
            <div class="form-panel">
              <form id="contact-form" action="#" method="get" novalidate>
                <div class="form-group"><label for="name">{e(p['label_name'])}</label>
                  <input type="text" id="name" name="name" required maxlength="120" autocomplete="name" placeholder="{e(p['ph_name'])}"></div>
                <div class="form-group"><label for="email">{e(p['label_email'])}</label>
                  <input type="email" id="email" name="email" required maxlength="160" autocomplete="email" placeholder="{e(p['ph_email'])}"></div>
                <div class="form-group"><label for="service">{e(p['label_service'])}</label>
                  <select id="service" name="service" required>
                    <option value="">{e(p['opt_empty'])}</option>
                    <option value="universite">{e(p['opt_uni'])}</option>
                    <option value="dil-okulu">{e(p['opt_lang'])}</option>
                    <option value="vize">{e(p['opt_visa'])}</option>
                    <option value="diger">{e(p['opt_other'])}</option>
                  </select></div>
                <div class="form-group"><label for="message">{e(p['label_msg'])}</label>
                  <textarea id="message" name="message" required maxlength="4000" placeholder="{e(p['ph_msg'])}"></textarea></div>
                <button type="submit" class="btn btn-full">{e(p['submit'])}</button>
                <p class="form-note fit-text">{e(p['note'])}</p>
                <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
              </form>
            </div>
          </div>
        </section>
</main>
{footer(t, lang, short=True)}
{cookie(t)}
  <script src="{a}/js/script.js" defer></script>
</body>
</html>"""
    return head_common(lang, "iletisim.html", p["title"], p["description"], a, extra) + "\n" + body


def render_404(T: dict, lang: str) -> str:
    t = T[lang]
    p = t["error"]
    a = asset(lang)
    body = f"""<body>
{header(t, lang, '404.html', '')}
  <main class="error-page">
    <div class="site-shell error-grid">
      <div>
        <p class="error-code" aria-hidden="true">404</p>
        <span class="eyebrow">{e(p['eye'])}</span>
        <h1 class="heading fit-text">{e(p['h1'])}</h1>
        <p class="lede fit-text">{e(p['lede'])}</p>
        <div class="btn-row">
          <a href="index.html" class="btn">{e(p['btn_home'])}</a>
          <a href="iletisim.html" class="btn">{e(p['btn_contact'])}</a>
        </div>
        <div class="error-links">
          <a href="hakkimizda.html">{e(p['link_about'])}</a>
          <a href="hizmetlerimiz.html">{e(p['link_services'])}</a>
          <a href="mailto:info@birikimedu.com">{e(p['link_mail'])}</a>
        </div>
      </div>
      <div class="feature-visual" aria-hidden="true">{BAUHAUS['c'].replace('bh-eye', 'bh-starburst')}</div>
    </div>
  </main>
{footer(t, lang, short=True)}
  <script src="{a}/js/script.js" defer></script>
</body>
</html>"""
    head = head_common(lang, "404.html", p["title"], p["description"], a, ERROR_STYLE, robots="noindex, follow")
    # 404 has no useful hreflang to self across langs for missing pages — keep anyway for consistency
    return head + "\n" + body


def write_sitemap() -> None:
    urls = []
    for lang in LANGS:
        for page in ["index.html", "hakkimizda.html", "hizmetlerimiz.html", "iletisim.html"]:
            pri = "1.0" if page == "index.html" and lang == "tr" else ("0.9" if page == "index.html" else "0.8")
            urls.append(
                f"""  <url>
    <loc>{page_url(lang, page)}</loc>
    <changefreq>{"weekly" if page == "index.html" else "monthly"}</changefreq>
    <priority>{pri}</priority>
  </url>"""
            )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )


def load_T() -> dict:
    # Turkish base from this module's companion — import merge
    spec = importlib.util.spec_from_file_location("i18n_extra", ROOT / "tools" / "_i18n_extra.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)

    # Load TR from embedded minimal file or from _i18n_tr
    tr_path = ROOT / "tools" / "_i18n_tr.py"
    if tr_path.exists():
        spec2 = importlib.util.spec_from_file_location("i18n_tr", tr_path)
        mod2 = importlib.util.module_from_spec(spec2)
        assert spec2.loader
        spec2.loader.exec_module(mod2)
        T = {"tr": mod2.TR}
    else:
        raise SystemExit("Missing _i18n_tr.py")

    mod.merge(T)
    return T


def main() -> None:
    T = load_T()
    for lang in LANGS:
        missing = [k for k in ("index", "about", "services", "contact", "error") if k not in T[lang]]
        if missing:
            raise SystemExit(f"{lang} missing keys: {missing}")

    renderers = {
        "index.html": render_index,
        "hakkimizda.html": render_about,
        "hizmetlerimiz.html": render_services,
        "iletisim.html": render_contact,
        "404.html": render_404,
    }
    for lang in LANGS:
        out_dir = ROOT if lang == "tr" else ROOT / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        for page, fn in renderers.items():
            path = out_dir / page
            path.write_text(fn(T, lang), encoding="utf-8")
            print("wrote", path.relative_to(ROOT))
    write_sitemap()
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
