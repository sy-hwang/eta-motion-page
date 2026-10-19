"""Cut each mesh-result slide into an independent web-ready MP4.

Usage: python scripts/export_mesh_clips.py --ffmpeg /path/to/ffmpeg
Requires the original recording and Pillow. No PowerPoint installation needed.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--ffmpeg", default=shutil.which("ffmpeg"))
args = parser.parse_args()
if not args.ffmpeg:
    parser.error("Provide --ffmpeg or install FFmpeg on PATH.")

manifest = json.loads((ROOT / "scripts/mesh_clips.json").read_text(encoding="utf-8"))
source = ROOT / manifest["source"]
output = ROOT / "site/assets/video/mesh"
posters = ROOT / "site/assets/images/mesh"
review = ROOT / "tmp/mesh-review"
for folder in [output, posters, review]:
    folder.mkdir(parents=True, exist_ok=True)

def ffmpeg(*arguments):
    subprocess.run([args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *map(str, arguments)], check=True)

for clip in manifest["clips"]:
    duration = clip["end"] - clip["start"]
    target = output / (clip["slug"] + ".mp4")
    # Trim before constant-frame-rate conversion so the next slide cannot enter
    # the output through frame duplication or an imprecise keyframe seek.
    filters = f"trim=duration={duration - .001:.6f},setpts=PTS-STARTPTS,fps=30,setsar=1"
    ffmpeg("-ss", f'{clip["start"]:.6f}', "-i", source, "-vf", filters,
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", target)
    still = review / (clip["slug"] + "-poster.png")
    ffmpeg("-ss", min(1, duration / 3), "-i", target, "-frames:v", "1", "-vf", "scale=1280:-2", still)
    Image.open(still).save(posters / (clip["slug"] + ".webp"), quality=90, method=6)
    # Decode the complete output, then retain endpoint frames for visual QA.
    ffmpeg("-i", target, "-f", "null", "-")
    ffmpeg("-i", target, "-frames:v", "1", "-vf", "scale=640:-2", review / (clip["slug"] + "-first.png"))
    ffmpeg("-sseof", "-0.06", "-i", target, "-frames:v", "1", "-vf", "scale=640:-2", review / (clip["slug"] + "-last.png"))
    print(f'{clip["slug"]}: {duration:.3f}s, {target.stat().st_size / 1024 / 1024:.2f} MiB', flush=True)
