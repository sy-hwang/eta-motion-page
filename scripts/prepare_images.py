"""Export the supplied paper figures for the project page. Requires Poppler and Pillow."""
from pathlib import Path
import subprocess
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "Topology_Agnostic_Motion_Generation" / "figures"
OUT = ROOT / "site" / "assets" / "images"
TEMP = ROOT / "tmp" / "previews"
OUT.mkdir(parents=True, exist_ok=True)
TEMP.mkdir(parents=True, exist_ok=True)

figures = {
    "teaser": "teaser_round2_v2.pdf",
    "overview": "overview_v4.pdf",
    "comparison": "Qualitative_v3.pdf",
    "sparse": "sparse_joint.pdf",
    "joint-budget": "k_budget_coverage_compact.pdf",
}
for name, source in figures.items():
    target = TEMP / name
    subprocess.run(["pdftoppm", "-scale-to", "2800", "-png", "-singlefile", str(FIGURES / source), str(target)], check=True)
    picture = Image.open(target.with_suffix(".png")).convert("RGB")
    if name == "overview":
        # overview_v4 has a second, unused diagram below the main architecture.
        # Keep the complete main architecture panel, including all of its labels.
        picture = picture.crop((0, int(picture.height * .42), picture.width, int(picture.height * .75)))
    difference = ImageChops.difference(picture, Image.new("RGB", picture.size, "white"))
    bbox = difference.convert("L").point(lambda x: 255 if x > 20 else 0).getbbox()
    if bbox:
        left, top, right, bottom = bbox
        picture = picture.crop((max(0, left - 16), max(0, top - 16), min(picture.width, right + 16), min(picture.height, bottom + 16)))
    picture.save(OUT / f"{name}.webp", quality=93, method=6)
    print(f"{name}: {picture.width} x {picture.height}")
