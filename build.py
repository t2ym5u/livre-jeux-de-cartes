#!/usr/bin/env python3
"""Assemble chapter Markdown files, add game anchors, check links, generate the index
chapter and the cover, then build the EPUB with pandoc."""
import glob
import os
import re
import shutil
import subprocess
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
CHAP = os.path.join(ROOT, "src")
BUILD = os.path.join(ROOT, "build")
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "Le-grand-livre-des-jeux-de-cartes.epub")
OUT_MD = os.path.join(DIST, "Le-grand-livre-des-jeux-de-cartes.md")
ASSETS = os.path.join(ROOT, "assets")
FIELD = re.compile(r"^- \*\*(Joueurs|Fun|Challenge|Âge conseillé|Diffusion) ?:\*\* *(.*)")


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return "jeu-" + re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def is_game_file(path):
    return re.match(r"0[1-9]-", os.path.basename(path)) is not None


def chapter_files():
    return sorted(glob.glob(os.path.join(CHAP, "*.md")))


def parse_games(files):
    games, chapter, cur = [], None, None
    for f in files:
        if not is_game_file(f):
            continue
        for line in open(f, encoding="utf-8"):
            if line.startswith("# "):
                chapter = line[2:].strip()
            elif line.startswith("## "):
                cur = {"name": line[3:].strip(), "chapter": chapter}
                games.append(cur)
            elif cur is not None:
                m = FIELD.match(line)
                if m:
                    cur[m.group(1)] = m.group(2).strip()
    return [g for g in games if "Joueurs" in g and "Challenge" in g]


def score(text):
    m = re.match(r"(\d(?:[.,]5)?)\s*/\s*5", text or "")
    return float(m.group(1).replace(",", ".")) if m else None


def player_range(text):
    head = text.lower().split("(")[0]
    nums = [int(n) for n in re.findall(r"\d+", head)]
    if not nums:
        return None
    lo, hi = min(nums), max(nums)
    if "et plus" in head or "ou plus" in head or "+" in head or "illimit" in head:
        hi = max(hi, 99)
    return lo, hi


def age(text):
    m = re.search(r"(\d+)", text or "")
    return int(m.group(1)) if m else None


def link(g):
    return f"[{g['name']}](#{slug(g['name'])})"


def note(g, key):
    return (g.get(key) or "?").split(" ")[0]


def line(g):
    return f"- **{link(g)}** : {g['Joueurs']} ; fun {note(g, 'Fun')}, challenge {note(g, 'Challenge')}"


def index_md(games):
    by_name = lambda g: g["name"].lower()
    out = ["# Index pratiques", "",
           "Ces listes sont générées à partir des fiches. Pour chaque jeu : le nombre de joueurs, "
           "puis les notes de fun et de challenge. Les noms renvoient aux fiches.", ""]
    out += ["## Jeux classés par nombre de joueurs", ""]
    for label, lo, hi in [("Seul", 1, 1), ("À deux", 2, 2), ("À trois", 3, 3), ("À quatre", 4, 4),
                          ("À cinq ou six", 5, 6), ("À sept et plus", 7, 99)]:
        sel = [g for g in games if (r := player_range(g["Joueurs"])) and r[0] <= hi and r[1] >= lo
               and not (hi == 1 and re.search(r"croupier|banquier", g["Joueurs"]))]
        out += [f"**{label}** ({len(sel)} jeux)", ""] + [line(g) for g in sorted(sel, key=by_name)] + [""]
    out += ["## Les jeux les plus stimulants (challenge 4/5 et plus)", ""]
    sel = [g for g in games if (score(g["Challenge"]) or 0) >= 4]
    out += [line(g) for g in sorted(sel, key=lambda g: (-score(g["Challenge"]), by_name(g)))] + [""]
    out += ["## Les jeux les plus amusants (fun 4/5 et plus)", ""]
    sel = [g for g in games if (score(g.get("Fun")) or 0) >= 4]
    out += [line(g) for g in sorted(sel, key=lambda g: (-score(g["Fun"]), by_name(g)))] + [""]
    out += ["## Pour jouer avec des enfants (dès 8 ans ou moins)", ""]
    sel = [g for g in games if (age(g.get("Âge conseillé")) or 99) <= 8]
    out += [f"- **{link(g)}** : {g['Âge conseillé']} ; {g['Joueurs']}"
            for g in sorted(sel, key=lambda g: (age(g["Âge conseillé"]), by_name(g)))] + [""]
    out += ["## Les jeux régionaux et de niche à découvrir", ""]
    sel = [g for g in games if g.get("Diffusion", "").lower().startswith(("niche", "régional"))]
    out += [f"- **{link(g)}** : {g['Diffusion']}" for g in sorted(sel, key=by_name)] + [""]
    out += ["## Tous les jeux par ordre alphabétique", ""]
    out += [f"- **{link(g)}** ({g['chapter']})" for g in sorted(games, key=by_name)]
    return "\n".join(out) + "\n"


def stage(files):
    """Copy sources to build/, adding {#jeu-...} anchors to game headings."""
    shutil.rmtree(BUILD, ignore_errors=True)
    os.makedirs(BUILD)
    staged, anchors = [], set()
    for f in files:
        text = open(f, encoding="utf-8").read()
        # [[Nom]] or [[Nom|texte]] -> link to the game's fiche
        text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]",
                      lambda m: f"[{m.group(2) or m.group(1)}](#{slug(m.group(1))})", text)
        # French typography: no-break space before : ; ! ? and inside guillemets
        text = re.sub(r" ([:;!?»])", "\u00a0\\1", text)
        text = text.replace("« ", "«\u00a0")
        if is_game_file(f):
            def add_id(m):
                anchors.add(slug(m.group(1)))
                return f"## {m.group(1)} {{#{slug(m.group(1))}}}"
            text = re.sub(r"^## (.+?)\s*$", add_id, text, flags=re.M)
        dst = os.path.join(BUILD, os.path.basename(f))
        open(dst, "w", encoding="utf-8").write(text)
        staged.append(dst)
    return staged, anchors


def check_links(files, anchors):
    bad = []
    for f in files:
        for n, l in enumerate(open(f, encoding="utf-8"), 1):
            for target in re.findall(r"\]\(#([^)]+)\)", l):
                if target not in anchors:
                    bad.append(f"{os.path.basename(f)}:{n}: #{target}")
    return bad


def cover(count):
    svg = open(os.path.join(ASSETS, "cover.svg"), encoding="utf-8").read().replace("GAMES_COUNT", str(count))
    src = os.path.join(BUILD, "cover.svg")
    open(src, "w", encoding="utf-8").write(svg)
    png = os.path.join(BUILD, "cover.png")
    subprocess.run(["rsvg-convert", "-w", "1200", "-o", png, src], check=True)
    return png


def main():
    files = chapter_files()
    games = parse_games(files)
    os.makedirs(DIST, exist_ok=True)
    staged, anchors = stage(files)
    idx = os.path.join(BUILD, "99-index-1.md")
    open(idx, "w", encoding="utf-8").write(index_md(games))
    staged.append(idx)
    bad = check_links(staged, anchors)
    for b in bad:
        print("LIEN CASSÉ", b)
    png = cover(len(games))
    print(f"{len(games)} fiches de jeu, {len(files)} fichiers, {len(bad)} liens cassés")
    cmd = ["pandoc", "--from", "markdown-smart", "--to", "epub3",
           "--metadata-file", os.path.join(ASSETS, "metadata.yaml"),
           "--metadata", f"subtitle=Règles, histoire, stratégie et variantes de {len(games)} jeux",
           "--epub-cover-image", png,
           "--css", os.path.join(ASSETS, "style.css"),
           "--toc", "--toc-depth=2", "--split-level=2",
           "-o", OUT] + staged
    subprocess.run(cmd, check=True)
    # Single-file Markdown edition, with the same anchors and links
    with open(OUT_MD, "w", encoding="utf-8") as out:
        out.write("% Le grand livre des jeux de cartes\n\n")
        out.write("\n\n".join(open(f, encoding="utf-8").read().strip() for f in staged) + "\n")
    print(OUT)
    print(OUT_MD)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
