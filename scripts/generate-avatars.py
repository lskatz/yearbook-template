#!/usr/bin/env python3
"""
Generate illustrated SVG portrait avatars for yearbook example characters.
Each avatar reflects physical traits of the corresponding Malcolm in the Middle character.

Hair functions return (back, front) tuples:
  back  — drawn before the head circle (panels that hang behind the face)
  front — drawn after  the head circle (cap that sits on top)

Run from repo root:
    python3 scripts/generate-avatars.py
"""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "people")

BACKDROP = "#b8cce8"   # classic school-photo light blue


# ---------------------------------------------------------------------------
# Hair shape builders  — return (back_svg, front_svg)
# ---------------------------------------------------------------------------

def hair_short_male(color):
    front = (
        f'<ellipse cx="150" cy="138" rx="74" ry="54" fill="{color}"/>'
        f'<path d="M 76 170 Q 90 126 150 118 Q 210 126 224 170" fill="{color}"/>'
    )
    return ("", front)


def hair_short_neat(color):
    front = (
        f'<ellipse cx="150" cy="140" rx="74" ry="52" fill="{color}"/>'
        f'<path d="M 76 168 Q 100 122 150 116 Q 200 122 224 168" fill="{color}"/>'
    )
    return ("", front)


def hair_long_female(color):
    back = (
        f'<rect x="72" y="156" width="23" height="112" rx="11" fill="{color}"/>'
        f'<rect x="205" y="156" width="23" height="112" rx="11" fill="{color}"/>'
    )
    front = f'<ellipse cx="150" cy="140" rx="74" ry="52" fill="{color}"/>'
    return (back, front)


def hair_medium_female(color):
    back = (
        f'<rect x="74" y="156" width="21" height="72" rx="10" fill="{color}"/>'
        f'<rect x="205" y="156" width="21" height="72" rx="10" fill="{color}"/>'
    )
    front = f'<ellipse cx="150" cy="140" rx="74" ry="52" fill="{color}"/>'
    return (back, front)


def hair_bun(color):
    front = (
        f'<ellipse cx="150" cy="144" rx="74" ry="52" fill="{color}"/>'
        f'<rect x="140" y="116" width="20" height="30" fill="{color}"/>'
        f'<circle cx="150" cy="102" r="22" fill="{color}"/>'
    )
    return ("", front)


def hair_bald(_color):
    return ("", "")


# ---------------------------------------------------------------------------
# Glasses overlay
# ---------------------------------------------------------------------------

def _glasses():
    return (
        '<rect x="102" y="176" width="36" height="24" rx="6"'
        ' fill="rgba(200,230,255,0.25)" stroke="#444" stroke-width="2.5"/>'
        '<rect x="162" y="176" width="36" height="24" rx="6"'
        ' fill="rgba(200,230,255,0.25)" stroke="#444" stroke-width="2.5"/>'
        '<line x1="138" y1="188" x2="162" y2="188" stroke="#444" stroke-width="2.5"/>'
        '<line x1="75"  y1="188" x2="102" y2="188" stroke="#444" stroke-width="2"/>'
        '<line x1="198" y1="188" x2="225" y2="188" stroke="#444" stroke-width="2"/>'
    )


# ---------------------------------------------------------------------------
# Master avatar builder
# ---------------------------------------------------------------------------

def make_avatar(char_id, skin, hair_color, hair_fn,
                has_glasses, clothes, eye_color="#2a1a0a", bg=BACKDROP):
    hair_back, hair_front = hair_fn(hair_color)
    gl = _glasses() if has_glasses else ""

    return f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400"
     role="img" aria-label="{char_id} portrait">

  <!-- Backdrop -->
  <rect width="300" height="400" fill="{bg}"/>

  <!-- Long/medium hair panels — sit in front of clothes but behind head -->
  {hair_back}

  <!-- Clothes / body silhouette -->
  <path d="M 46 400 L 64 322 Q 102 294 150 290 Q 198 294 236 322 L 254 400 Z"
        fill="{clothes}"/>

  <!-- Neck -->
  <rect x="133" y="246" width="34" height="46" rx="6" fill="{skin}"/>

  <!-- Ears — behind head circle so face cleanly overlaps -->
  <ellipse cx="76"  cy="192" rx="12" ry="16" fill="{skin}"/>
  <ellipse cx="224" cy="192" rx="12" ry="16" fill="{skin}"/>

  <!-- Head -->
  <circle cx="150" cy="186" r="74" fill="{skin}"/>

  <!-- Hair cap — on top of head -->
  {hair_front}

  <!-- Eyes — whites -->
  <ellipse cx="121" cy="188" rx="10" ry="8" fill="white"/>
  <ellipse cx="179" cy="188" rx="10" ry="8" fill="white"/>
  <!-- Irises -->
  <circle cx="122" cy="189" r="5.5" fill="{eye_color}"/>
  <circle cx="180" cy="189" r="5.5" fill="{eye_color}"/>
  <!-- Specular highlights -->
  <circle cx="124" cy="187" r="2" fill="white"/>
  <circle cx="182" cy="187" r="2" fill="white"/>

  <!-- Eyebrows -->
  <path d="M 107 172 Q 121 165 135 172"
        stroke="{hair_color}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M 165 172 Q 179 165 193 172"
        stroke="{hair_color}" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Nose (soft shadow nostrils) -->
  <ellipse cx="143" cy="212" rx="5" ry="3.5" fill="rgba(0,0,0,0.10)"/>
  <ellipse cx="157" cy="212" rx="5" ry="3.5" fill="rgba(0,0,0,0.10)"/>

  <!-- Mouth -->
  <path d="M 132 226 Q 150 237 168 226"
        stroke="#b06060" stroke-width="3" fill="none" stroke-linecap="round"/>

  <!-- Glasses -->
  {gl}

</svg>
"""


# ---------------------------------------------------------------------------
# Character roster
# (id, skin, hair_color, hair_fn, glasses, clothes, eye_color, backdrop)
#
# Traits sourced from Malcolm in the Middle character descriptions.
# ---------------------------------------------------------------------------

characters = [
    # ---- STUDENTS ----

    # Malcolm Wilkerson — ~10 yo white male, dark brown messy hair, brown eyes
    ("malcolm-wilkerson",
     "#f5d5a8", "#4e2b12", hair_short_male,   False, "#2e6db0", "#4e2b12", BACKDROP),

    # Reese Wilkerson — ~12 yo white male, dirty-blonde hair, stocky build
    ("reese-wilkerson",
     "#f5d5a8", "#c4a03a", hair_short_male,   False, "#a04c18", "#5a3a10", BACKDROP),

    # Dewey Wilkerson — ~8 yo white male, brown hair, small / younger-looking
    ("dewey-wilkerson",
     "#f5d5a8", "#6a3a1a", hair_short_neat,   False, "#2e8040", "#3a2010", BACKDROP),

    # Francis Wilkerson — ~17 yo white male, dark brown hair (older teen)
    ("francis-wilkerson",
     "#f5d5a8", "#4e2b12", hair_short_neat,   False, "#7a2a10", "#3a2010", BACKDROP),

    # Stevie Kenarban — ~10 yo Black male, very close-cropped black hair
    ("stevie-kenarban",
     "#4a2808", "#1a0e06", hair_short_male,   False, "#1c3e7a", "#1a0e06", "#b0c8e4"),

    # Cynthia Sanders — ~10 yo white female, bright red hair, tall
    ("cynthia-sanders",
     "#fce8d4", "#b82010", hair_long_female,  False, "#6a1a9a", "#3a2010", BACKDROP),

    # Dabney Hooper — ~10 yo white male, light brown hair, thick glasses, nerdy
    ("dabney-hooper",
     "#f5d5a8", "#a07830", hair_short_neat,   True,  "#1a4a90", "#4a3010", BACKDROP),

    # Lloyd Cornwall — ~10 yo white male, dark hair, thick-framed glasses
    ("lloyd",
     "#f5d5a8", "#1e1410", hair_short_neat,   True,  "#1a6a30", "#1e1410", BACKDROP),

    # Kevin Ainsley — ~10 yo, medium brown skin, dark brown hair
    ("kevin",
     "#d4956a", "#2c1a0a", hair_short_male,   False, "#c05018", "#2c1a0a", BACKDROP),

    # Julie Houlerman — ~11 yo female, golden blonde hair
    ("julie-houlerman",
     "#fce8d4", "#c89c38", hair_long_female,  False, "#c41860", "#3a2c10", BACKDROP),

    # Jessica Barton — ~13 yo female, medium brown skin, dark brown hair
    ("jessica",
     "#d4956a", "#2c1a0a", hair_long_female,  False, "#6a1080", "#2c1a0a", BACKDROP),

    # ---- TEACHERS ----

    # Ms. Caroline Miller — white woman ~40s, auburn hair, glasses
    ("caroline-miller",
     "#f5d5a8", "#7a3010", hair_medium_female, True,  "#1a307a", "#3a1808", BACKDROP),

    # Mr. Herkabe — white male ~50s, receding/bald black hair, pompous
    ("mr-herkabe",
     "#f0e0c8", "#1a1414", hair_bald,          False, "#282828", "#1a1414", "#c8c8cc"),

    # Mr. Woodward — adult male, medium brown skin, dark brown hair
    ("mr-woodward",
     "#d4956a", "#2c1a0a", hair_short_neat,    False, "#1a4010", "#2c1a0a", BACKDROP),

    # Ms. Old — elderly white woman, silver-gray bun, glasses
    ("ms-old",
     "#f2dac8", "#b0b0b0", hair_bun,           True,  "#5a1070", "#606060", "#d8d0e4"),

    # ---- STAFF ----

    # Principal Block — white male ~50s, dark hair, navy suit
    ("principal-block",
     "#f5d5a8", "#2a1a0a", hair_short_neat,    False, "#0e1a52", "#2a1a0a", BACKDROP),

    # Nurse Craig — white woman, blonde hair, white/pale uniform
    ("nurse-craig",
     "#f5d5a8", "#c8a030", hair_medium_female, False, "#e8eeff", "#3a2c10", BACKDROP),

    # Counselor Fenton — adult male, olive skin, brown hair
    ("counselor-fenton",
     "#c8845a", "#4a2810", hair_short_neat,    False, "#1a4010", "#4a2810", BACKDROP),
]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for row in characters:
        char_id, skin, hair_color, hair_fn, has_glasses, clothes, eye_color, bg = row
        svg = make_avatar(char_id, skin, hair_color, hair_fn,
                          has_glasses, clothes, eye_color, bg)
        path = os.path.join(OUTPUT_DIR, f"{char_id}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  wrote {os.path.relpath(path)}")
    print(f"\nDone — {len(characters)} avatars in assets/images/people/")


if __name__ == "__main__":
    main()
