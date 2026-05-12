from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from api.catalog import MOVIE_BLUEPRINTS, THEATER_PHOTOS, normalize_catalog_key


PUBLIC_DIR = ROOT / "frontend" / "public" / "assets"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def svg_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")


def poster_svg(title: str, genres: list[str], tagline: str, palette: dict[str, str]) -> str:
    chips = " • ".join(genres[:3])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1350">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{palette['secondary']}" />
      <stop offset="55%" stop-color="{palette['primary']}" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <radialGradient id="glow" cx="35%" cy="20%" r="65%">
      <stop offset="0%" stop-color="{palette['accent']}" stop-opacity="0.9" />
      <stop offset="100%" stop-color="{palette['accent']}" stop-opacity="0" />
    </radialGradient>
  </defs>
  <rect width="900" height="1350" fill="url(#bg)" />
  <rect width="900" height="1350" fill="url(#glow)" />
  <rect x="46" y="46" width="808" height="1258" rx="36" fill="none" stroke="rgba(255,255,255,0.22)" />
  <circle cx="710" cy="240" r="182" fill="rgba(255,255,255,0.08)" />
  <path d="M0 990 C250 860 540 860 900 1120 L900 1350 L0 1350 Z" fill="rgba(2,6,23,0.62)" />
  <text x="84" y="140" fill="rgba(255,255,255,0.82)" font-size="30" font-family="Helvetica,Arial,sans-serif" letter-spacing="8">CINEVERSE CURATED ASSET</text>
  <text x="84" y="1050" fill="white" font-size="96" font-weight="700" font-family="Helvetica,Arial,sans-serif">{title}</text>
  <text x="84" y="1110" fill="{palette['accent']}" font-size="34" font-family="Helvetica,Arial,sans-serif">{chips}</text>
  <foreignObject x="84" y="1144" width="720" height="110">
    <div xmlns="http://www.w3.org/1999/xhtml" style="color: rgba(255,255,255,0.8); font-family: Helvetica,Arial,sans-serif; font-size: 30px; line-height: 1.4;">
      {tagline}
    </div>
  </foreignObject>
</svg>"""


def backdrop_svg(title: str, genres: list[str], mood: str, palette: dict[str, str]) -> str:
    chips = " • ".join(genres[:3])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">
  <defs>
    <linearGradient id="sky" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617" />
      <stop offset="40%" stop-color="{palette['secondary']}" />
      <stop offset="100%" stop-color="{palette['primary']}" />
    </linearGradient>
    <radialGradient id="spot" cx="72%" cy="28%" r="45%">
      <stop offset="0%" stop-color="{palette['accent']}" stop-opacity="0.95" />
      <stop offset="100%" stop-color="{palette['accent']}" stop-opacity="0" />
    </radialGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#sky)" />
  <rect width="1920" height="1080" fill="url(#spot)" />
  <path d="M0 760 C300 640 620 660 920 740 C1210 818 1490 930 1920 760 L1920 1080 L0 1080 Z" fill="rgba(2,6,23,0.72)" />
  <path d="M0 890 C360 760 820 760 1220 860 C1450 916 1700 960 1920 900" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="4" />
  <text x="112" y="140" fill="rgba(255,255,255,0.74)" font-size="34" font-family="Helvetica,Arial,sans-serif" letter-spacing="10">FEATURED CINEMATIC BANNER</text>
  <text x="112" y="760" fill="white" font-size="122" font-weight="700" font-family="Helvetica,Arial,sans-serif">{title}</text>
  <text x="116" y="828" fill="{palette['accent']}" font-size="34" font-family="Helvetica,Arial,sans-serif">{chips}</text>
  <foreignObject x="112" y="858" width="760" height="120">
    <div xmlns="http://www.w3.org/1999/xhtml" style="color: rgba(255,255,255,0.82); font-family: Helvetica,Arial,sans-serif; font-size: 30px; line-height: 1.35;">
      {mood}
    </div>
  </foreignObject>
</svg>"""


def logo_svg(title: str, palette: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360">
  <defs>
    <linearGradient id="logo" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{palette['accent']}" />
      <stop offset="100%" stop-color="{palette['primary']}" />
    </linearGradient>
  </defs>
  <rect width="1200" height="360" rx="48" fill="rgba(2,6,23,0.18)" />
  <text x="60" y="220" fill="url(#logo)" font-size="138" font-weight="700" font-family="Helvetica,Arial,sans-serif">{title}</text>
</svg>"""


def gallery_svg(title: str, label: str, palette: dict[str, str], index: int) -> str:
    opacity = 0.18 + index * 0.08
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{palette['secondary']}" />
      <stop offset="100%" stop-color="{palette['primary']}" />
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#g)" />
  <circle cx="{320 + index * 160}" cy="{200 + index * 70}" r="190" fill="rgba(255,255,255,{opacity})" />
  <path d="M0 620 C240 540 400 560 600 610 C840 670 1050 710 1280 540 L1280 720 L0 720 Z" fill="rgba(2,6,23,0.54)" />
  <text x="60" y="100" fill="rgba(255,255,255,0.7)" font-size="30" font-family="Helvetica,Arial,sans-serif" letter-spacing="6">{label}</text>
  <text x="60" y="620" fill="white" font-size="84" font-weight="700" font-family="Helvetica,Arial,sans-serif">{title}</text>
</svg>"""


def cast_svg(name: str) -> str:
    initials = " ".join(part[0] for part in name.split()[:2]).upper()
    tone = ["#0f172a", "#1d4ed8", "#7c3aed", "#be123c"][len(name) % 4]
    accent = ["#93c5fd", "#f9a8d4", "#a7f3d0", "#fde68a"][len(name) % 4]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{tone}" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="256" fill="url(#bg)" />
  <circle cx="256" cy="192" r="92" fill="{accent}" fill-opacity="0.34" />
  <path d="M126 422 C152 334 210 286 256 286 C302 286 360 334 386 422" fill="{accent}" fill-opacity="0.42" />
  <text x="256" y="472" text-anchor="middle" fill="white" font-size="108" font-weight="700" font-family="Helvetica,Arial,sans-serif">{initials}</text>
</svg>"""


def theater_svg(label: str, accent: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720">
  <rect width="1200" height="720" fill="#050816" />
  <rect x="72" y="72" width="1056" height="576" rx="38" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)" />
  <path d="M126 530 C270 442 430 410 604 410 C784 410 938 446 1080 530" fill="none" stroke="{accent}" stroke-width="10" stroke-linecap="round" />
  <text x="100" y="180" fill="{accent}" font-size="40" font-family="Helvetica,Arial,sans-serif" letter-spacing="8">PREMIUM CINEMA NETWORK</text>
  <text x="100" y="340" fill="white" font-size="120" font-weight="700" font-family="Helvetica,Arial,sans-serif">{label}</text>
  <text x="100" y="414" fill="rgba(255,255,255,0.74)" font-size="32" font-family="Helvetica,Arial,sans-serif">IMAX • Laser Projection • Recliners • Dolby Atmos</text>
</svg>"""


def main():
    ensure_dir(PUBLIC_DIR / "movies")
    ensure_dir(PUBLIC_DIR / "cast")
    ensure_dir(PUBLIC_DIR / "theaters")

    for item in MOVIE_BLUEPRINTS:
        movie_dir = PUBLIC_DIR / "movies" / item["slug"]
        gallery_dir = movie_dir / "gallery"
        ensure_dir(gallery_dir)
        svg_file(movie_dir / "poster.svg", poster_svg(item["title"], item["genre"], item["heroTag"], item["palette"]))
        svg_file(movie_dir / "backdrop.svg", backdrop_svg(item["title"], item["genre"], item["mood"], item["palette"]))
        svg_file(movie_dir / "logo.svg", logo_svg(item["title"], item["palette"]))
        for index, label in enumerate(["Still 01", "Still 02", "Still 03"], start=1):
            svg_file(gallery_dir / f"scene-{index}.svg", gallery_svg(item["title"], label, item["palette"], index))
        for name, _role in item["cast"]:
            svg_file(PUBLIC_DIR / "cast" / f"{normalize_catalog_key(name)}.svg", cast_svg(name))

    theater_accents = {
        "pvr.svg": "#fbbf24",
        "inox.svg": "#38bdf8",
        "cinepolis.svg": "#34d399",
        "miraj.svg": "#f472b6",
        "carnival.svg": "#fb7185",
        "asian-cinemas.svg": "#a78bfa",
    }
    for file_name in THEATER_PHOTOS.values():
        svg_file(PUBLIC_DIR / file_name.replace("/assets/", ""), theater_svg(Path(file_name).stem.replace("-", " ").title(), theater_accents[Path(file_name).name]))


if __name__ == "__main__":
    main()
