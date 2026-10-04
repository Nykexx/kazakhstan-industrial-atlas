# -*- coding: utf-8 -*-
"""
Updater for Site 1: KAZAKHSTAN INDUSTRIAL ATLAS 3D
Adds True 3D Interactive Map, 23 Nature Reserves & National Parks,
and 3D Animal Hologram Showcase in Cyber-Industrial (Cyan/Emerald/Blue) design.
"""
import json
import os

with open("full_regions_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

with open("nature_reserves_db.json", "r", encoding="utf-8") as f:
    parks_db = json.load(f)

# Generate SVG elements for regions and cities
svg_regions_paths = []
svg_city_pins = []

for rid, r in db.items():
    path_d = r["svg_path"]
    rtype = r["type"]
    name = r["name"]
    lx = r.get("label_x", 500)
    ly = r.get("label_y", 300)
    
    svg_regions_paths.append(f'''    <path id="region-{rid}" class="kz-region" data-id="{rid}" d="{path_d}">
      <title>{name}</title>
    </path>''')
    
    if rtype == "city":
        svg_city_pins.append(f'''    <g id="city-{rid}" class="city-hub-pin" data-id="{rid}" transform="translate({lx:.1f}, {ly:.1f})">
      <circle class="pin-hit-circle" r="22" />
      <circle class="pin-pulse-wave" r="14" />
      <circle class="pin-base" r="7" />
      <circle class="pin-core" r="3" />
      <g class="pin-badge" transform="translate(12, -9)">
        <rect class="badge-bg" x="0" y="0" width="{len(name)*7.5 + 14}" height="18" rx="4" />
        <text class="badge-txt" x="7" y="13">{name}</text>
      </g>
    </g>''')

# Generate 23 National Parks & Nature Reserves Pins
svg_parks_pins = []
for p in parks_db:
    pid = p["id"]
    pname = p["name"]
    ptype = p["type"]
    px = p["x"]
    py = p["y"]
    is_park = (ptype == "park")
    color = "#10b981" if is_park else "#f59e0b"
    icon = "M0 -6 L4 1 L-4 1 Z M0 0 L0 4" if is_park else "M-5 3 L0 -5 L5 3 Z"
    
    svg_parks_pins.append(f'''    <g id="park-{pid}" class="cyber-nature-pin {ptype}" data-park-id="{pid}" transform="translate({px:.1f}, {py:.1f})">
      <circle class="park-hit-circle" r="20" />
      <circle class="park-radar-wave" r="13" stroke="{color}" />
      <circle class="park-base-disc" r="7.5" fill="#0b1120" stroke="{color}" stroke-width="1.8" />
      <path class="park-glyph" d="{icon}" stroke="{color}" stroke-width="1.3" fill="none" />
      <circle class="park-core-dot" r="2.2" fill="{color}" />
    </g>''')

svg_regions_html = "\n".join(svg_regions_paths)
svg_cities_html = "\n".join(svg_city_pins)
svg_parks_html = "\n".join(svg_parks_pins)

db_embedded = json.dumps(db, ensure_ascii=False)
parks_embedded = json.dumps(parks_db, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="no-referrer">
  <title>ИНДУСТРИАЛЬНЫЙ АТЛАС КАЗАХСТАНА 3D // 2026</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  
  <!-- Three.js CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <style>
    /* ==========================================================================
       CYBER-INDUSTRIAL DESIGN SYSTEM: SLATE & NEON CYAN / EMERALD
       ========================================================================== */
    :root {{
      --bg-base: #070b14;
      --bg-panel: #0d1527;
      --bg-card: rgba(15, 23, 42, 0.75);
      --border-line: rgba(56, 189, 248, 0.2);
      --border-glow: rgba(6, 182, 212, 0.5);
      --cyan-bright: #06b6d4;
      --cyan-light: #67e8f9;
      --cyan-glow: rgba(6, 182, 212, 0.3);
      --emerald-accent: #10b981;
      --emerald-glow: rgba(16, 185, 129, 0.3);
      --amber-accent: #f59e0b;
      --text-pri: #f8fafc;
      --text-sec: #94a3b8;
      --text-dim: #64748b;
      --font-main: 'Inter', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100%;
      height: 100%;
      background-color: var(--bg-base);
      color: var(--text-pri);
      font-family: var(--font-main);
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* Cyber Tech Grid Background */
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      background-image: 
        radial-gradient(circle at 50% 15%, rgba(6, 182, 212, 0.08) 0%, transparent 65%),
        linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 36px 36px, 36px 36px;
      pointer-events: none;
      z-index: 0;
    }}

    .app-root {{
      position: relative;
      z-index: 1;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}

    /* HEADER */
    .cyber-header {{
      background: rgba(13, 21, 39, 0.92);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-line);
      position: sticky;
      top: 0;
      z-index: 50;
    }}

    .cyber-header-main {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 24px;
      gap: 20px;
      flex-wrap: wrap;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-icon {{
      width: 42px;
      height: 42px;
      border: 1px solid var(--cyan-bright);
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(15, 23, 42, 0.9));
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--cyan-bright);
      box-shadow: 0 0 15px var(--cyan-glow);
    }}

    .brand-titles h1 {{
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 0.03em;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-titles h1 span {{
      color: var(--cyan-bright);
    }}

    .brand-titles p {{
      font-size: 11px;
      color: var(--text-sec);
    }}

    .header-controls {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex: 1;
      max-width: 520px;
      justify-content: flex-end;
    }}

    .search-wrap {{
      position: relative;
      flex: 1;
      max-width: 320px;
    }}

    .search-input {{
      width: 100%;
      height: 38px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-line);
      border-radius: var(--radius-md);
      padding: 0 36px 0 14px;
      color: #ffffff;
      font-size: 13px;
      outline: none;
      transition: var(--transition);
    }}

    .search-input:focus {{
      border-color: var(--cyan-bright);
      box-shadow: 0 0 14px var(--cyan-glow);
    }}

    .search-dropdown {{
      position: absolute;
      top: calc(100% + 6px);
      left: 0;
      right: 0;
      background: #0f172a;
      border: 1px solid var(--cyan-bright);
      border-radius: var(--radius-md);
      box-shadow: 0 15px 35px rgba(0,0,0,0.8);
      max-height: 280px;
      overflow-y: auto;
      display: none;
      z-index: 100;
    }}

    .search-item {{
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .search-item:hover {{
      background: rgba(6, 182, 212, 0.15);
    }}

    /* SECTOR FILTER TABS */
    .filter-tabs-bar {{
      padding: 8px 24px;
      background: rgba(8, 14, 26, 0.95);
      border-bottom: 1px solid var(--border-line);
      display: flex;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .filter-tabs-bar::-webkit-scrollbar {{ display: none; }}

    .filter-btn {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(56, 189, 248, 0.15);
      border-radius: var(--radius-sm);
      color: var(--text-sec);
      padding: 6px 14px;
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
      white-space: nowrap;
    }}

    .filter-btn:hover {{
      color: #ffffff;
      border-color: var(--cyan-bright);
      background: rgba(6, 182, 212, 0.1);
    }}

    .filter-btn.active {{
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(15, 23, 42, 0.9));
      border-color: var(--cyan-bright);
      color: var(--cyan-light);
      box-shadow: 0 0 12px var(--cyan-glow);
      font-weight: 600;
    }}

    /* ==========================================================================
       TRUE 3D MAP WORKSPACE
       ========================================================================== */
    .workspace-wrapper {{
      position: relative;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    .map-3d-stage-wrapper {{
      position: relative;
      flex: 1;
      min-height: calc(100vh - 120px);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      perspective: 1400px;
      cursor: grab;
      user-select: none;
      padding: 20px;
    }}

    .map-3d-stage-wrapper:active {{
      cursor: grabbing;
    }}

    .map-3d-plane {{
      position: relative;
      width: 1000px;
      max-width: 95vw;
      height: 650px;
      max-height: 80vh;
      transform-style: preserve-3d;
      transition: transform 0.12s cubic-bezier(0.1, 0.9, 0.2, 1);
      will-change: transform;
    }}

    /* Grid Base on 3D Plane Floor */
    .map-3d-plane::before {{
      content: "";
      position: absolute;
      inset: -40px;
      border: 1px dashed rgba(6, 182, 212, 0.25);
      border-radius: 20px;
      background: radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 75%);
      transform: translateZ(-25px);
      pointer-events: none;
      box-shadow: 0 35px 70px rgba(0,0,0,0.9);
    }}

    .svg-atlas-viewport {{
      width: 100%;
      height: 100%;
      filter: drop-shadow(0 25px 40px rgba(0, 0, 0, 0.9));
      transform: translateZ(15px);
      transform-style: preserve-3d;
    }}

    /* REGIONS */
    .kz-region {{
      fill: #0f172a;
      stroke: var(--cyan-bright);
      stroke-width: 1.15;
      stroke-opacity: 0.45;
      vector-effect: non-scaling-stroke;
      cursor: pointer;
      transition: fill 0.25s ease, stroke 0.25s ease, stroke-width 0.25s ease, filter 0.25s ease;
    }}

    .kz-region:hover {{
      fill: rgba(6, 182, 212, 0.32);
      stroke: var(--cyan-light);
      stroke-width: 2.2;
      stroke-opacity: 1;
      filter: drop-shadow(0 0 14px rgba(6, 182, 212, 0.7));
    }}

    .kz-region.dimmed {{
      opacity: 0.2;
      fill: #060a12;
      stroke-opacity: 0.15;
    }}

    .kz-region.highlighted {{
      fill: rgba(6, 182, 212, 0.4);
      stroke: #ffffff;
      stroke-width: 2.4;
      stroke-opacity: 1;
      filter: drop-shadow(0 0 16px rgba(6, 182, 212, 0.8));
    }}

    /* CITY HUBS */
    .city-hub-pin {{
      cursor: pointer;
    }}
    .pin-hit-circle {{
      fill: transparent;
      pointer-events: all;
    }}
    .pin-pulse-wave {{
      fill: none;
      stroke: var(--cyan-bright);
      stroke-width: 1.2;
      opacity: 0.6;
      animation: pinWave 2.8s infinite ease-out;
      pointer-events: none;
    }}
    @keyframes pinWave {{
      0% {{ transform: scale(0.5); opacity: 1; }}
      100% {{ transform: scale(2.0); opacity: 0; }}
    }}
    .pin-base {{
      fill: #0b1120;
      stroke: var(--cyan-bright);
      stroke-width: 2;
      pointer-events: none;
      transition: fill 0.2s, stroke 0.2s;
    }}
    .pin-core {{
      fill: #ffffff;
      pointer-events: none;
    }}
    .pin-badge {{
      pointer-events: none;
    }}
    .badge-bg {{
      fill: rgba(15, 23, 42, 0.9);
      stroke: var(--border-glow);
      stroke-width: 1;
    }}
    .badge-txt {{
      fill: #ffffff;
      font-size: 11px;
      font-weight: 600;
    }}
    .city-hub-pin:hover .pin-base {{
      fill: var(--cyan-bright);
      stroke: #ffffff;
    }}
    .city-hub-pin:hover .badge-bg {{
      fill: var(--cyan-bright);
    }}
    .city-hub-pin:hover .badge-txt {{
      fill: #000000;
    }}

    /* ==========================================================================
       CYBER NATURE PINS (23 PARKS & RESERVES)
       ========================================================================== */
    .cyber-nature-pin {{
      cursor: pointer;
    }}
    .park-hit-circle {{
      fill: transparent;
      pointer-events: all;
    }}
    .park-radar-wave {{
      fill: none;
      stroke-width: 1.2;
      opacity: 0.7;
      animation: parkWave 2.6s infinite ease-out;
      pointer-events: none;
    }}
    @keyframes parkWave {{
      0% {{ transform: scale(0.5); opacity: 1; }}
      100% {{ transform: scale(2.2); opacity: 0; }}
    }}
    .park-base-disc {{
      pointer-events: none;
      transition: fill 0.2s, stroke 0.2s;
    }}
    .park-glyph {{
      pointer-events: none;
    }}
    .park-core-dot {{
      pointer-events: none;
    }}
    .cyber-nature-pin:hover .park-base-disc {{
      fill: var(--emerald-accent);
      stroke: #ffffff;
    }}
    .cyber-nature-pin:hover .park-glyph {{
      stroke: #000000;
    }}

    /* 3D CONTROLS TOOLBAR */
    .map-3d-toolbar {{
      position: absolute;
      top: 20px;
      right: 24px;
      display: flex;
      gap: 8px;
      background: rgba(13, 21, 39, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-line);
      border-radius: var(--radius-md);
      padding: 6px;
      z-index: 20;
    }}

    .map-3d-btn {{
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(56, 189, 248, 0.2);
      color: var(--text-sec);
      border-radius: var(--radius-sm);
      padding: 6px 12px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
      white-space: nowrap;
    }}

    .map-3d-btn:hover {{
      color: #ffffff;
      border-color: var(--cyan-bright);
      background: rgba(6, 182, 212, 0.15);
    }}

    .map-3d-btn.active {{
      background: var(--cyan-bright);
      color: #000000;
      border-color: var(--cyan-bright);
      box-shadow: 0 0 10px var(--cyan-glow);
    }}

    /* FLOATING TELEMETRY HUD */
    .map-telemetry-hud {{
      position: absolute;
      bottom: 24px;
      left: 24px;
      width: 320px;
      background: rgba(13, 21, 39, 0.9);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-glow);
      border-radius: var(--radius-md);
      padding: 16px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.8);
      pointer-events: none;
      z-index: 10;
    }}

    .hud-title {{
      font-size: 14px;
      font-weight: 700;
      color: #ffffff;
    }}

    .hud-stat-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .hud-stat-val {{
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--cyan-light);
      font-weight: 600;
    }}

    /* ZOOM CONTROLS */
    .map-zoom-panel {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 10;
    }}

    .zoom-btn {{
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-glow);
      color: var(--cyan-bright);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      transition: var(--transition);
    }}

    .zoom-btn:hover {{
      background: var(--cyan-bright);
      color: #000000;
      box-shadow: 0 0 12px var(--cyan-glow);
    }}

    /* ==========================================================================
       3D ANIMAL SHOWCASE (HOLOGRAPHIC INSPECTOR)
       ========================================================================== */
    .animal-hologram-card {{
      position: fixed;
      pointer-events: none;
      background: rgba(11, 17, 32, 0.95);
      backdrop-filter: blur(20px);
      border: 1px solid var(--emerald-accent);
      border-radius: var(--radius-lg);
      padding: 16px;
      width: 360px;
      box-shadow: 0 25px 50px rgba(0,0,0,0.85), 0 0 35px var(--emerald-glow);
      z-index: 1200;
      opacity: 0;
      transform: translate(-50%, -105%) scale(0.95);
      transition: opacity 0.25s ease, transform 0.25s ease;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .animal-hologram-card.visible {{
      opacity: 1;
      transform: translate(-50%, -105%) scale(1);
      pointer-events: all;
    }}

    .animal-card-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
      border-bottom: 1px solid rgba(16, 185, 129, 0.2);
      padding-bottom: 8px;
    }}

    .animal-park-name {{
      font-size: 13px;
      font-weight: 700;
      color: var(--emerald-accent);
    }}

    .animal-park-region {{
      font-size: 11px;
      color: var(--text-sec);
    }}

    .animal-type-badge {{
      font-size: 9.5px;
      padding: 3px 7px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: var(--emerald-accent);
      white-space: nowrap;
    }}

    .animal-visual-stage {{
      position: relative;
      width: 100%;
      height: 190px;
      border-radius: var(--radius-md);
      overflow: hidden;
      background: radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.95), #06090e);
      border: 1px solid var(--border-line);
    }}

    .animal-3d-canvas-wrap {{
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      cursor: grab;
    }}

    .animal-photo-view {{
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      object-fit: cover;
      display: none;
    }}

    .visual-toggle-bar {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      display: flex;
      gap: 4px;
      z-index: 10;
    }}

    .visual-toggle-btn {{
      background: rgba(7, 11, 20, 0.85);
      border: 1px solid var(--border-glow);
      color: var(--cyan-light);
      font-size: 10px;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
      transition: var(--transition);
    }}

    .visual-toggle-btn.active {{
      background: var(--emerald-accent);
      color: #000000;
      font-weight: 700;
      border-color: var(--emerald-accent);
    }}

    .animal-bio-info {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .animal-name-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
    }}

    .animal-latin {{
      font-size: 11px;
      font-style: italic;
      color: var(--cyan-light);
    }}

    .animal-redbook {{
      font-size: 11px;
      color: #f87171;
      font-weight: 600;
      background: rgba(248, 113, 113, 0.1);
      border: 1px solid rgba(248, 113, 113, 0.25);
      padding: 3px 8px;
      border-radius: 4px;
      margin-top: 4px;
    }}

    .animal-fact {{
      font-size: 11.5px;
      color: var(--text-sec);
      line-height: 1.45;
      margin-top: 4px;
    }}

    .animal-card-actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .animal-link-btn {{
      font-size: 11px;
      font-weight: 600;
      color: var(--cyan-light);
      background: none;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    .animal-link-btn:hover {{
      text-decoration: underline;
    }}

    /* MODAL POPUP */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(7, 11, 20, 0.85);
      backdrop-filter: blur(14px);
      z-index: 1500;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}

    .modal-overlay.active {{
      opacity: 1;
      pointer-events: all;
    }}

    .modal-window {{
      background: #0d1527;
      border: 1px solid var(--border-glow);
      border-radius: var(--radius-xl);
      box-shadow: 0 25px 60px rgba(0,0,0,0.85), 0 0 35px var(--cyan-glow);
      width: 100%;
      max-width: 1140px;
      height: 90vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .modal-top {{
      padding: 16px 24px;
      background: rgba(15, 23, 42, 0.95);
      border-bottom: 1px solid var(--border-line);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .modal-close-btn {{
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-line);
      color: #ffffff;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }}

    .modal-body {{
      flex: 1;
      overflow-y: auto;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }}

    /* TOOLTIP */
    .geo-tooltip {{
      position: fixed;
      pointer-events: none;
      background: rgba(13, 21, 39, 0.95);
      backdrop-filter: blur(12px);
      border: 1px solid var(--cyan-bright);
      border-radius: var(--radius-md);
      padding: 10px 16px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.8);
      z-index: 500;
      opacity: 0;
      transform: translate(-50%, -120%);
      transition: opacity 0.15s ease;
      white-space: nowrap;
    }}

    .geo-tooltip.visible {{
      opacity: 1;
    }}

    @media (max-width: 900px) {{
      .map-3d-toolbar {{
        top: 10px; right: 10px; flex-wrap: wrap; max-width: 240px;
      }}
      .map-telemetry-hud {{ display: none; }}
      .animal-hologram-card {{ width: 320px; }}
    }}
  </style>
</head>
<body>
  <div class="app-root">
    <header class="cyber-header">
      <div class="cyber-header-main">
        <div class="brand-wrap">
          <div class="brand-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
          </div>
          <div class="brand-titles">
            <h1>ИНДУСТРИАЛЬНЫЙ АТЛАС <span>// 3D КАЗАХСТАН</span></h1>
            <p>20 субъектов РК • 23 нацпарка и заповедника с 3D фауной • Актуальные границы 2026</p>
          </div>
        </div>

        <div class="header-controls">
          <div class="search-wrap">
            <input type="text" id="searchInput" class="search-input" placeholder="Поиск субъекта, города или нацпарка..." autocomplete="off">
            <div id="searchDropdown" class="search-dropdown"></div>
          </div>
        </div>
      </div>

      <nav class="filter-tabs-bar">
        <button class="filter-btn active" data-filter="all">Все регионы (20)</button>
        <button class="filter-btn" data-filter="parks" style="color: var(--emerald-accent); border-color: rgba(16,185,129,0.4);">🌲 Заповедники & Парки (23)</button>
        <button class="filter-btn" data-filter="oilgas">Нефть и газ</button>
        <button class="filter-btn" data-filter="metallurgy">Металлургия</button>
        <button class="filter-btn" data-filter="uranium">Уран & Атомпром</button>
        <button class="filter-btn" data-filter="agro">Агропром</button>
        <button class="filter-btn" data-filter="coal">Уголь & Энергетика</button>
        <button class="filter-btn" data-filter="machinery">Машиностроение</button>
      </nav>
    </header>

    <main class="workspace-wrapper">
      <div id="map3DStageWrapper" class="map-3d-stage-wrapper">
        <div class="map-3d-toolbar">
          <button id="btn3DPerspective" class="map-3d-btn active">⟲ 3D Перспектива</button>
          <button id="btn3DIsometric" class="map-3d-btn">◰ Изометрия</button>
          <button id="btn3DTopDown" class="map-3d-btn">⧈ 2D План</button>
          <button id="btn3DAutoOrbit" class="map-3d-btn">✦ Авто-облёт</button>
          <button id="btnToggleParks" class="map-3d-btn" style="color: var(--emerald-accent);">🌲 Фауна (23)</button>
        </div>

        <div id="map3DPlane" class="map-3d-plane">
          <svg id="svgAtlas" class="svg-atlas-viewport" viewBox="0 0 1000 650">
            <g id="regionsLayer">
{svg_regions_html}
            </g>
            <g id="citiesLayer">
{svg_cities_html}
            </g>
            <g id="parksLayer">
{svg_parks_html}
            </g>
          </svg>
        </div>

        <div id="telemetryHud" class="map-telemetry-hud">
          <div class="hud-title" id="hudTitle">Карагандинская область</div>
          <div style="font-size: 11.5px; color: var(--text-sec); margin-top: 2px;" id="hudFocus">Чёрная металлургия и уголь</div>
          <div class="hud-stat-row">
            <div>
              <div style="font-size: 10px; color: var(--text-dim); text-transform: uppercase;">Центр</div>
              <div id="hudCenter" class="hud-stat-val">г. Караганда</div>
            </div>
            <div>
              <div style="font-size: 10px; color: var(--text-dim); text-transform: uppercase;">Пром. доля</div>
              <div id="hudShare" class="hud-stat-val">~9.5%</div>
            </div>
          </div>
        </div>

        <div class="map-zoom-panel">
          <button id="zoomInBtn" class="zoom-btn">+</button>
          <button id="zoomOutBtn" class="zoom-btn">−</button>
          <button id="zoomResetBtn" class="zoom-btn" style="font-size: 11px;">100%</button>
        </div>
      </div>
    </main>
  </div>

  <!-- TOOLTIP -->
  <div id="geoTooltip" class="geo-tooltip">
    <div id="tooltipName" style="font-weight: 700; color: #fff;"></div>
    <div id="tooltipCenter" style="font-size: 11px; color: var(--text-sec);"></div>
    <div id="tooltipFocus" style="font-size: 11px; color: var(--cyan-light); margin-top: 2px;"></div>
  </div>

  <!-- 3D ANIMAL SHOWCASE -->
  <div id="animalHologramCard" class="animal-hologram-card">
    <div class="animal-card-header">
      <div>
        <div id="animalParkName" class="animal-park-name">Иле-Алатауский национальный парк</div>
        <div id="animalParkRegion" class="animal-park-region">Алматинская область • Основан в 1996 г.</div>
      </div>
      <div id="animalTypeBadge" class="animal-type-badge">ГНПП</div>
    </div>

    <div class="animal-visual-stage">
      <div id="animal3DCanvasWrap" class="animal-3d-canvas-wrap"></div>
      <img id="animalPhotoView" class="animal-photo-view" src="" alt="Fauna" referrerpolicy="no-referrer">
      <div class="visual-toggle-bar">
        <button id="btnView3D" class="visual-toggle-btn active">3D Модель</button>
        <button id="btnViewPhoto" class="visual-toggle-btn">Фото</button>
      </div>
    </div>

    <div class="animal-bio-info">
      <div class="animal-name-title">
        <span id="animalName">Снежный барс (Ирбис)</span>
      </div>
      <div id="animalLatin" class="animal-latin">Panthera uncia</div>
      <div id="animalRedBook" class="animal-redbook">Красная книга РК: I категория (исчезающий вид)</div>
      <div id="animalFact" class="animal-fact">Обитает на альпийских хребтах Тянь-Шаня...</div>
    </div>

    <div class="animal-card-actions">
      <button id="animalOpenRegionBtn" class="animal-link-btn">Открыть досье региона →</button>
      <span style="font-size: 10px; color: var(--text-dim); font-family: var(--font-mono);">3D FAUNA LAB</span>
    </div>
  </div>

  <!-- MODAL POPUP -->
  <div id="modalOverlay" class="modal-overlay">
    <div class="modal-window">
      <div class="modal-top">
        <div>
          <h2 id="modalTitle" style="font-size: 20px; font-weight: 700; color: #fff;">Карагандинская область</h2>
          <div id="modalSub" style="font-size: 12px; color: var(--cyan-light);">Qaraǵandy oblysy • Центр: Караганда</div>
        </div>
        <button id="modalCloseBtn" class="modal-close-btn">&times;</button>
      </div>

      <div class="modal-body">
        <div id="modalStatsGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px;"></div>
        <div id="modalSummary" style="background: rgba(6, 182, 212, 0.05); border-left: 3px solid var(--cyan-bright); padding: 16px; border-radius: var(--radius-sm); font-size: 13.5px; line-height: 1.6;"></div>
        <div id="modalEnterprises" style="display: flex; flex-direction: column; gap: 12px;"></div>
        <div id="modalNature" style="display: flex; flex-direction: column; gap: 12px;"></div>
        <div id="modalGallery" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px;"></div>
      </div>
    </div>
  </div>

  <script>
    const REGIONS_DATA = {db_embedded};
    const PARKS_DATA = {parks_embedded};

    class CyberIndustrialAtlas3D {{
      constructor() {{
        this.db = REGIONS_DATA;
        this.parks = PARKS_DATA;
        this.parksVisible = true;

        // 3D Orbit
        this.rotX = 35;
        this.rotZ = -10;
        this.zoom = 1;
        this.isDragging = false;
        this.startX = 0;
        this.startY = 0;
        this.autoOrbit = false;

        // Three.js
        this.threeScene = null;
        this.threeCamera = null;
        this.threeRenderer = null;
        this.threeMesh = null;
        this.activeAnimal = null;

        this.initDOM();
        this.init3DOrbit();
        this.initThreeJS();
        this.initEvents();
        this.updateHUD('karaganda');
        this.apply3DTransform();
      }}

      initDOM() {{
        this.map3DStageWrapper = document.getElementById('map3DStageWrapper');
        this.map3DPlane = document.getElementById('map3DPlane');
        this.tooltip = document.getElementById('geoTooltip');
        this.tooltipName = document.getElementById('tooltipName');
        this.tooltipCenter = document.getElementById('tooltipCenter');
        this.tooltipFocus = document.getElementById('tooltipFocus');

        this.hudTitle = document.getElementById('hudTitle');
        this.hudFocus = document.getElementById('hudFocus');
        this.hudCenter = document.getElementById('hudCenter');
        this.hudShare = document.getElementById('hudShare');

        this.animalCard = document.getElementById('animalHologramCard');
        this.animalParkName = document.getElementById('animalParkName');
        this.animalParkRegion = document.getElementById('animalParkRegion');
        this.animalTypeBadge = document.getElementById('animalTypeBadge');
        this.animalName = document.getElementById('animalName');
        this.animalLatin = document.getElementById('animalLatin');
        this.animalRedBook = document.getElementById('animalRedBook');
        this.animalFact = document.getElementById('animalFact');
        this.animalPhotoView = document.getElementById('animalPhotoView');
        this.animal3DCanvasWrap = document.getElementById('animal3DCanvasWrap');
        this.btnView3D = document.getElementById('btnView3D');
        this.btnViewPhoto = document.getElementById('btnViewPhoto');
        this.animalOpenRegionBtn = document.getElementById('animalOpenRegionBtn');

        this.modalOverlay = document.getElementById('modalOverlay');
        this.modalCloseBtn = document.getElementById('modalCloseBtn');
        this.searchInput = document.getElementById('searchInput');
        this.searchDropdown = document.getElementById('searchDropdown');
      }}

      init3DOrbit() {{
        const wrapper = this.map3DStageWrapper;

        wrapper.addEventListener('pointerdown', (e) => {{
          if (e.target.closest('.map-3d-toolbar, .map-zoom-panel, .map-telemetry-hud, .animal-hologram-card')) return;
          this.isDragging = true;
          this.startX = e.clientX;
          this.startY = e.clientY;
          wrapper.setPointerCapture(e.pointerId);
        }});

        wrapper.addEventListener('pointermove', (e) => {{
          if (!this.isDragging) return;
          const dx = e.clientX - this.startX;
          const dy = e.clientY - this.startY;
          this.startX = e.clientX;
          this.startY = e.clientY;
          this.rotZ += dx * 0.28;
          this.rotX = Math.max(0, Math.min(65, this.rotX - dy * 0.28));
          this.autoOrbit = false;
          this.apply3DTransform();
        }});

        const endDrag = (e) => {{
          if (this.isDragging) {{
            this.isDragging = false;
            try {{ wrapper.releasePointerCapture(e.pointerId); }} catch(_) {{}}
          }}
        }};
        wrapper.addEventListener('pointerup', endDrag);
        wrapper.addEventListener('pointercancel', endDrag);

        wrapper.addEventListener('wheel', (e) => {{
          e.preventDefault();
          const delta = e.deltaY > 0 ? -0.1 : 0.1;
          this.zoom = Math.max(0.7, Math.min(2.2, this.zoom + delta));
          this.apply3DTransform();
        }}, {{ passive: false }});

        document.getElementById('btn3DPerspective').addEventListener('click', () => {{
          this.rotX = 35; this.rotZ = -10; this.autoOrbit = false; this.apply3DTransform();
        }});
        document.getElementById('btn3DIsometric').addEventListener('click', () => {{
          this.rotX = 55; this.rotZ = -28; this.autoOrbit = false; this.apply3DTransform();
        }});
        document.getElementById('btn3DTopDown').addEventListener('click', () => {{
          this.rotX = 0; this.rotZ = 0; this.autoOrbit = false; this.apply3DTransform();
        }});
        document.getElementById('btn3DAutoOrbit').addEventListener('click', () => {{
          this.autoOrbit = !this.autoOrbit;
          if (this.autoOrbit) this.runOrbitLoop();
        }});
        document.getElementById('btnToggleParks').addEventListener('click', (e) => {{
          this.parksVisible = !this.parksVisible;
          document.getElementById('parksLayer').style.display = this.parksVisible ? 'block' : 'none';
          e.currentTarget.style.opacity = this.parksVisible ? '1' : '0.4';
        }});
      }}

      runOrbitLoop() {{
        if (!this.autoOrbit) return;
        this.rotZ += 0.15;
        this.apply3DTransform();
        requestAnimationFrame(() => this.runOrbitLoop());
      }}

      apply3DTransform() {{
        this.map3DPlane.style.transform = `rotateX(${{this.rotX.toFixed(1)}}deg) rotateZ(${{this.rotZ.toFixed(1)}}deg) scale(${{this.zoom.toFixed(2)}})`;
      }}

      initThreeJS() {{
        if (typeof THREE === 'undefined') return;
        const width = 328;
        const height = 190;
        this.threeScene = new THREE.Scene();
        this.threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
        this.threeCamera.position.set(0, 1.2, 3.8);

        this.threeRenderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        this.threeRenderer.setSize(width, height);
        this.threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.animal3DCanvasWrap.appendChild(this.threeRenderer.domElement);

        this.threeScene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const pl = new THREE.PointLight(0x06b6d4, 1.8, 20);
        pl.position.set(2, 4, 3);
        this.threeScene.add(pl);
        const fl = new THREE.PointLight(0x10b981, 1.2, 20);
        fl.position.set(-3, -1, -2);
        this.threeScene.add(fl);

        let isModelDragging = false;
        let prevX = 0;
        this.threeRenderer.domElement.addEventListener('pointerdown', (e) => {{
          isModelDragging = true;
          prevX = e.clientX;
        }});
        window.addEventListener('pointermove', (e) => {{
          if (!isModelDragging || !this.threeMesh) return;
          const dx = e.clientX - prevX;
          prevX = e.clientX;
          this.threeMesh.rotation.y += dx * 0.02;
        }});
        window.addEventListener('pointerup', () => isModelDragging = false);

        const loop = () => {{
          requestAnimationFrame(loop);
          if (this.threeMesh && !isModelDragging) {{
            this.threeMesh.rotation.y += 0.012;
          }}
          this.threeRenderer.render(this.threeScene, this.threeCamera);
        }};
        loop();
      }}

      buildModel(modelType, colorHex) {{
        const root = new THREE.Group();
        const mat = new THREE.MeshStandardMaterial({{
          color: new THREE.Color(colorHex || 0x06b6d4),
          metalness: 0.7,
          roughness: 0.2,
          flatShading: true
        }});
        const wire = new THREE.MeshBasicMaterial({{
          color: 0xffffff,
          wireframe: true,
          transparent: true,
          opacity: 0.25
        }});

        const part = (geom, x=0, y=0, z=0, rx=0, ry=0, rz=0) => {{
          const g = new THREE.Group();
          g.add(new THREE.Mesh(geom, mat));
          g.add(new THREE.Mesh(geom, wire));
          g.position.set(x, y, z);
          g.rotation.set(rx, ry, rz);
          root.add(g);
        }};

        if (modelType === 'feline') {{
          part(new THREE.CylinderGeometry(0.35, 0.45, 1.4, 8), 0, 0, 0, 1.57);
          part(new THREE.ConeGeometry(0.3, 0.5, 6), 0, 0.35, 0.75, 0.4);
          part(new THREE.DodecahedronGeometry(0.38), 0, 0.6, 0.95);
          part(new THREE.CylinderGeometry(0.1, 0.08, 0.8, 6), -0.28, -0.5, 0.5);
          part(new THREE.CylinderGeometry(0.1, 0.08, 0.8, 6), 0.28, -0.5, 0.5);
          part(new THREE.CylinderGeometry(0.12, 0.09, 0.8, 6), -0.3, -0.5, -0.5);
          part(new THREE.CylinderGeometry(0.12, 0.09, 0.8, 6), 0.3, -0.5, -0.5);
          part(new THREE.CylinderGeometry(0.08, 0.05, 1.2, 6), 0, 0.2, -0.9, -0.8);
        }} else if (modelType === 'bird') {{
          part(new THREE.SphereGeometry(0.4, 8, 6), 0, 0, 0);
          part(new THREE.CylinderGeometry(0.08, 0.12, 0.8, 6), 0, 0.45, 0.25, 0.3);
          part(new THREE.ConeGeometry(0.18, 0.45, 6), 0, 0.85, 0.45, -1.4);
          part(new THREE.BoxGeometry(1.6, 0.06, 0.5), -0.9, 0.1, 0, 0, 0, 0.15);
          part(new THREE.BoxGeometry(1.6, 0.06, 0.5), 0.9, 0.1, 0, 0, 0, -0.15);
        }} else if (modelType === 'ungulate') {{
          part(new THREE.CylinderGeometry(0.4, 0.45, 1.5, 8), 0, 0, 0, 1.57);
          part(new THREE.CylinderGeometry(0.18, 0.25, 0.75, 6), 0, 0.45, 0.65, 0.5);
          part(new THREE.BoxGeometry(0.35, 0.4, 0.55), 0, 0.85, 0.85);
          part(new THREE.TorusGeometry(0.45, 0.08, 6, 12, Math.PI), -0.3, 1.15, 0.7, 0, 1.2, 0.8);
          part(new THREE.TorusGeometry(0.45, 0.08, 6, 12, Math.PI), 0.3, 1.15, 0.7, 0, -1.2, -0.8);
          part(new THREE.CylinderGeometry(0.09, 0.07, 1.0, 6), -0.25, -0.6, 0.55);
          part(new THREE.CylinderGeometry(0.09, 0.07, 1.0, 6), 0.25, -0.6, 0.55);
          part(new THREE.CylinderGeometry(0.1, 0.08, 1.0, 6), -0.27, -0.6, -0.55);
          part(new THREE.CylinderGeometry(0.1, 0.08, 1.0, 6), 0.27, -0.6, -0.55);
        }} else if (modelType === 'bear') {{
          part(new THREE.SphereGeometry(0.65, 8, 8), 0, 0, 0);
          part(new THREE.SphereGeometry(0.55, 8, 8), 0, 0.25, 0.55);
          part(new THREE.DodecahedronGeometry(0.4), 0, 0.45, 0.95);
          part(new THREE.CylinderGeometry(0.2, 0.16, 0.75, 6), -0.35, -0.45, 0.45);
          part(new THREE.CylinderGeometry(0.2, 0.16, 0.75, 6), 0.35, -0.45, 0.45);
        }} else {{
          part(new THREE.CylinderGeometry(0.35, 0.5, 0.9, 8), 0, 0, 0);
          part(new THREE.SphereGeometry(0.32, 8, 8), 0, 0.55, 0.05);
          part(new THREE.BoxGeometry(0.15, 0.35, 0.12), -0.25, 0.2, 0.25, -0.6);
          part(new THREE.BoxGeometry(0.15, 0.35, 0.12), 0.25, 0.2, 0.25, -0.6);
        }}

        root.position.y = -0.2;
        return root;
      }}

      showAnimal(parkId, event) {{
        const park = this.parks.find(p => p.id === parkId);
        if (!park) return;
        this.activeAnimal = park;

        this.animalParkName.textContent = park.name;
        this.animalParkRegion.textContent = park.regionName + ' • ' + park.areaKm2;
        this.animalTypeBadge.textContent = park.type === 'park' ? 'ГНПП' : 'ЗАПОВЕДНИК';

        const a = park.animal;
        this.animalName.textContent = a.name;
        this.animalLatin.textContent = a.latin;
        this.animalRedBook.textContent = a.category;
        this.animalFact.textContent = a.population;
        this.animalPhotoView.src = a.imageUrl;

        if (this.threeScene) {{
          if (this.threeMesh) this.threeScene.remove(this.threeMesh);
          this.threeMesh = this.buildModel(a.modelType, a.modelColor);
          this.threeScene.add(this.threeMesh);
        }}

        let x = event ? event.clientX : window.innerWidth / 2;
        let y = event ? event.clientY : window.innerHeight / 2;
        x = Math.max(190, Math.min(window.innerWidth - 190, x));
        y = Math.max(340, Math.min(window.innerHeight - 30, y));

        this.animalCard.style.left = x + 'px';
        this.animalCard.style.top = y + 'px';
        this.animalCard.classList.add('visible');

        this.switchVisualTab('3d');
      }}

      switchVisualTab(tab) {{
        if (tab === '3d') {{
          this.animal3DCanvasWrap.style.display = 'block';
          this.animalPhotoView.style.display = 'none';
          this.btnView3D.classList.add('active');
          this.btnViewPhoto.classList.remove('active');
        }} else {{
          this.animal3DCanvasWrap.style.display = 'none';
          this.animalPhotoView.style.display = 'block';
          this.btnViewPhoto.classList.add('active');
          this.btnView3D.classList.remove('active');
        }}
      }}

      initEvents() {{
        // Regions
        document.querySelectorAll('.kz-region').forEach(el => {{
          el.addEventListener('mouseenter', (e) => this.onRegionHover(e, el.dataset.id));
          el.addEventListener('mousemove', (e) => this.moveTooltip(e));
          el.addEventListener('mouseleave', () => this.hideTooltip());
          el.addEventListener('click', () => this.openModal(el.dataset.id));
        }});

        // Cities
        document.querySelectorAll('.city-hub-pin').forEach(pin => {{
          pin.addEventListener('mouseenter', (e) => this.onRegionHover(e, pin.dataset.id));
          pin.addEventListener('mousemove', (e) => this.moveTooltip(e));
          pin.addEventListener('mouseleave', () => this.hideTooltip());
          pin.addEventListener('click', () => this.openModal(pin.dataset.id));
        }});

        // 23 Nature Pins
        document.querySelectorAll('.cyber-nature-pin').forEach(np => {{
          np.addEventListener('mouseenter', (e) => this.showAnimal(np.dataset.parkId, e));
          np.addEventListener('click', (e) => {{
            e.stopPropagation();
            this.showAnimal(np.dataset.parkId, e);
          }});
        }});

        document.addEventListener('click', (e) => {{
          if (!this.animalCard.contains(e.target) && !e.target.closest('.cyber-nature-pin')) {{
            this.animalCard.classList.remove('visible');
          }}
        }});

        this.btnView3D.addEventListener('click', (e) => {{
          e.stopPropagation(); this.switchVisualTab('3d');
        }});
        this.btnViewPhoto.addEventListener('click', (e) => {{
          e.stopPropagation(); this.switchVisualTab('photo');
        }});

        this.animalOpenRegionBtn.addEventListener('click', () => {{
          if (this.activeAnimal) {{
            this.animalCard.classList.remove('visible');
            this.openModal(this.activeAnimal.regionId);
          }}
        }});

        // Filters
        document.querySelectorAll('.filter-btn').forEach(btn => {{
          btn.addEventListener('click', () => {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            this.applyFilter(btn.dataset.filter);
          }});
        }});

        // Modal
        this.modalCloseBtn.addEventListener('click', () => this.modalOverlay.classList.remove('active'));
        this.modalOverlay.addEventListener('click', (e) => {{
          if (e.target === this.modalOverlay) this.modalOverlay.classList.remove('active');
        }});
        window.addEventListener('keydown', (e) => {{
          if (e.key === 'Escape') {{
            this.modalOverlay.classList.remove('active');
            this.animalCard.classList.remove('visible');
            this.searchDropdown.style.display = 'none';
          }}
        }});

        // Search
        this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        document.addEventListener('click', (e) => {{
          if (!this.searchInput.contains(e.target) && !this.searchDropdown.contains(e.target)) {{
            this.searchDropdown.style.display = 'none';
          }}
        }});

        // Zoom
        document.getElementById('zoomInBtn').addEventListener('click', () => {{
          this.zoom = Math.min(2.2, this.zoom + 0.15); this.apply3DTransform();
        }});
        document.getElementById('zoomOutBtn').addEventListener('click', () => {{
          this.zoom = Math.max(0.7, this.zoom - 0.15); this.apply3DTransform();
        }});
        document.getElementById('zoomResetBtn').addEventListener('click', () => {{
          this.zoom = 1; this.rotX = 35; this.rotZ = -10; this.autoOrbit = false; this.apply3DTransform();
        }});
      }}

      onRegionHover(e, id) {{
        const d = this.db[id];
        if (!d) return;
        this.tooltipName.textContent = d.name;
        this.tooltipCenter.textContent = 'Центр: г. ' + d.center;
        this.tooltipFocus.textContent = d.focus || 'Индустриальный центр';
        this.tooltip.classList.add('visible');
        this.moveTooltip(e);
        this.updateHUD(id);
      }}

      moveTooltip(e) {{
        this.tooltip.style.left = e.clientX + 'px';
        this.tooltip.style.top = (e.clientY - 12) + 'px';
      }}

      hideTooltip() {{
        this.tooltip.classList.remove('visible');
      }}

      updateHUD(id) {{
        const d = this.db[id];
        if (!d) return;
        this.hudTitle.textContent = d.name;
        this.hudFocus.textContent = d.focus || 'Индустриальный комплекс';
        this.hudCenter.textContent = 'г. ' + d.center;
        this.hudShare.textContent = d.indShare || '—';
      }}

      applyFilter(cat) {{
        const regions = document.querySelectorAll('.kz-region');
        const pins = document.querySelectorAll('.city-hub-pin');
        const parksLayer = document.getElementById('parksLayer');

        if (cat === 'parks') {{
          parksLayer.style.display = 'block';
          regions.forEach(r => r.classList.remove('dimmed', 'highlighted'));
          pins.forEach(p => p.style.opacity = '0.3');
          return;
        }}

        if (cat === 'all') {{
          regions.forEach(r => r.classList.remove('dimmed', 'highlighted'));
          pins.forEach(p => p.style.opacity = '1');
        }} else {{
          regions.forEach(r => {{
            const d = this.db[r.dataset.id];
            const tags = (d && d.filterTags) ? d.filterTags : [];
            if (tags.includes(cat)) {{
              r.classList.remove('dimmed');
              r.classList.add('highlighted');
            }} else {{
              r.classList.remove('highlighted');
              r.classList.add('dimmed');
            }}
          }});
          pins.forEach(p => {{
            const d = this.db[p.dataset.id];
            const tags = (d && d.filterTags) ? d.filterTags : [];
            p.style.opacity = tags.includes(cat) ? '1' : '0.2';
          }});
        }}
      }}

      handleSearch(q) {{
        q = q.trim().toLowerCase();
        if (!q) {{
          this.searchDropdown.style.display = 'none';
          return;
        }}

        const rMatches = Object.values(this.db).filter(d => 
          d.name.toLowerCase().includes(q) || d.center.toLowerCase().includes(q)
        ).slice(0, 4);

        const pMatches = this.parks.filter(p =>
          p.name.toLowerCase().includes(q) || p.animal.name.toLowerCase().includes(q)
        ).slice(0, 3);

        let html = '';
        rMatches.forEach(m => {{
          html += `
            <div class="search-item" onclick="atlasApp.openModal('${{m.id}}')">
              <div>
                <div style="font-weight: 600; color: #fff;">${{m.name}}</div>
                <div style="font-size: 11px; color: var(--text-sec);">Центр: г. ${{m.center}}</div>
              </div>
              <div style="font-size: 11px; color: var(--cyan-bright);">${{m.indShare || ''}}</div>
            </div>
          `;
        }});

        pMatches.forEach(p => {{
          html += `
            <div class="search-item" onclick="atlasApp.showAnimal('${{p.id}}')">
              <div>
                <div style="font-weight: 600; color: var(--emerald-accent);">🌲 ${{p.name}}</div>
                <div style="font-size: 11px; color: var(--text-sec);">${{p.animal.name}}</div>
              </div>
              <div style="font-size: 10px; color: var(--emerald-accent);">3D ФАУНА</div>
            </div>
          `;
        }});

        this.searchDropdown.innerHTML = html || '<div style="padding: 12px; color: var(--text-dim); text-align: center;">Не найдено</div>';
        this.searchDropdown.style.display = 'block';
      }}

      openModal(id) {{
        const d = this.db[id];
        if (!d) return;

        this.searchDropdown.style.display = 'none';
        this.animalCard.classList.remove('visible');

        document.getElementById('modalTitle').textContent = d.name;
        document.getElementById('modalSub').textContent = `${{d.nameKz}} • Административный центр: г. ${{d.center}}`;

        // Stats
        document.getElementById('modalStatsGrid').innerHTML = `
          <div style="background: rgba(15,23,42,0.8); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
            <div style="font-size: 11px; color: var(--text-dim); text-transform: uppercase;">Площадь</div>
            <div style="font-size: 18px; font-weight: 700; color: #fff; margin-top: 4px;">${{d.area}}</div>
            <div style="font-size: 11px; color: var(--cyan-light);">${{d.areaCmp || ''}}</div>
          </div>
          <div style="background: rgba(15,23,42,0.8); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
            <div style="font-size: 11px; color: var(--text-dim); text-transform: uppercase;">Население</div>
            <div style="font-size: 18px; font-weight: 700; color: #fff; margin-top: 4px;">${{d.population}}</div>
            <div style="font-size: 11px; color: var(--cyan-light);">Плотность: ${{d.density || ''}}</div>
          </div>
          <div style="background: rgba(15,23,42,0.8); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
            <div style="font-size: 11px; color: var(--text-dim); text-transform: uppercase;">Урбанизация</div>
            <div style="font-size: 18px; font-weight: 700; color: #fff; margin-top: 4px;">${{d.urbanRate || '70%'}}</div>
          </div>
          <div style="background: rgba(15,23,42,0.8); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
            <div style="font-size: 11px; color: var(--text-dim); text-transform: uppercase;">Вклад в пром. РК</div>
            <div style="font-size: 18px; font-weight: 700; color: #fff; margin-top: 4px;">${{d.indShare || '—'}}</div>
          </div>
        `;

        document.getElementById('modalSummary').textContent = d.summary || '';

        // Enterprises
        const entDiv = document.getElementById('modalEnterprises');
        entDiv.innerHTML = '<h3 style="font-size: 15px; font-weight: 700; color: #fff;">Ключевые предприятия</h3>' +
          (d.enterprises || []).map(e => `
            <div style="background: rgba(15,23,42,0.6); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 700; color: #fff;">${{e.title}}</div>
                <span style="font-size: 10px; color: var(--cyan-bright); background: rgba(6,182,212,0.15); padding: 2px 8px; border-radius: 4px;">${{e.tag || ''}}</span>
              </div>
              <div style="font-size: 12px; color: var(--text-sec); margin-top: 6px;">${{e.role}}</div>
            </div>
          `).join('');

        // Nature
        const nat = d.nature || {{}};
        document.getElementById('modalNature').innerHTML = `
          <h3 style="font-size: 15px; font-weight: 700; color: #fff;">Природно-экологический каркас</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
            <div style="background: rgba(15,23,42,0.6); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
              <div style="font-size: 12px; font-weight: 700; color: var(--emerald-accent);">Заповедники & Парки</div>
              <ul style="margin-top: 8px; font-size: 12px; color: var(--text-sec); list-style: inside;">
                ${{(nat.reserves || []).map(r => `<li>${{r}}</li>`).join('')}}
              </ul>
            </div>
            <div style="background: rgba(15,23,42,0.6); border: 1px solid var(--border-line); padding: 14px; border-radius: var(--radius-sm);">
              <div style="font-size: 12px; font-weight: 700; color: var(--emerald-accent);">Редкая фауна</div>
              <ul style="margin-top: 8px; font-size: 12px; color: var(--text-sec); list-style: inside;">
                ${{(nat.fauna || []).map(f => `<li>${{f}}</li>`).join('')}}
              </ul>
            </div>
          </div>
        `;

        // Gallery
        const gal = document.getElementById('modalGallery');
        gal.innerHTML = (d.images || []).map(img => `
          <div style="border-radius: var(--radius-sm); overflow: hidden; background: #000; height: 160px; position: relative;">
            <img src="${{img.url}}" alt="${{img.caption}}" referrerpolicy="no-referrer" style="width: 100%; height: 100%; object-fit: cover;">
            <div style="position: absolute; bottom: 0; inset-inline: 0; background: linear-gradient(transparent, rgba(0,0,0,0.9)); padding: 12px 8px 6px; font-size: 11px; color: #fff;">${{img.caption}}</div>
          </div>
        `).join('');

        this.modalOverlay.classList.add('active');
      }}
    }}

    let atlasApp;
    window.addEventListener('DOMContentLoaded', () => {{
      atlasApp = new CyberIndustrialAtlas3D();
    }});
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Site 1 (Industrial Atlas 3D) index.html updated successfully! Size:", os.path.getsize("index.html"), "bytes")
