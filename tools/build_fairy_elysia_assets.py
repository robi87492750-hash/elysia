"""Build maid Elysia's transparent desktop-pet clips from project artwork."""

from __future__ import annotations

import json
import math
from pathlib import Path

import imageio_ffmpeg
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "characters" / "elysia"
VIDEOS = CHARACTER / "videos"
SIZE = (640, 360)
FEET_Y = 330
FPS = 24


def canvas_for(source: Image.Image, max_width: int = 350) -> Image.Image:
    source = source.convert("RGBA")
    alpha = source.getchannel("A").point(lambda value: 255 if value >= 96 else 0)
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError("Artwork has no visible pixels")
    source = source.crop(bounds)
    scale = min(max_width / source.width, 300 / source.height)
    source = source.resize(
        (round(source.width * scale), round(source.height * scale)),
        Image.Resampling.LANCZOS,
    )
    result = Image.new("RGBA", SIZE)
    result.alpha_composite(source, ((SIZE[0] - source.width) // 2, FEET_Y - source.height))
    return result


def transform(image: Image.Image, scale_x: float = 1, scale_y: float = 1,
              x: int = 0, y: int = 0, angle: float = 0) -> Image.Image:
    width = round(SIZE[0] * scale_x)
    height = round(SIZE[1] * scale_y)
    changed = image.resize((width, height), Image.Resampling.LANCZOS)
    result = Image.new("RGBA", SIZE)
    result.alpha_composite(changed, ((SIZE[0] - width) // 2 + x,
                                     FEET_Y - round(FEET_Y * scale_y) + y))
    if angle:
        result = result.rotate(angle, Image.Resampling.BICUBIC, center=(SIZE[0] // 2, FEET_Y))
    return result


def encode(path: Path, frames: list[Image.Image]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = imageio_ffmpeg.write_frames(
        str(path), SIZE, fps=FPS, codec="libvpx-vp9", pix_fmt_in="rgba",
        pix_fmt_out="yuva420p", macro_block_size=1,
        output_params=["-auto-alt-ref", "0", "-metadata:s:v:0", "alpha_mode=1",
                       "-deadline", "realtime", "-cpu-used", "4", "-crf", "32", "-b:v", "0"],
    )
    writer.send(None)
    try:
        for frame in frames:
            writer.send(frame.tobytes())
    finally:
        writer.close()


def main() -> None:
    static = canvas_for(Image.open(CHARACTER / "女仆爱莉原画.png"))
    static.save(CHARACTER / "Q版女仆爱莉希雅.png")

    sheet = Image.open(CHARACTER / "女仆爱莉跑步四帧.png").convert("RGBA")
    run_poses = [canvas_for(sheet.crop((round(i * sheet.width / 4), 0,
                                       round((i + 1) * sheet.width / 4), sheet.height)), 360)
                 for i in range(4)]

    idle = [transform(static, 1 - 0.004 * math.sin(2 * math.pi * i / 48),
                      1 + 0.007 * math.sin(2 * math.pi * i / 48)) for i in range(48)]
    encode(VIDEOS / "idle" / "Q版待机呼吸.webm", idle)

    move = []
    for i in range(24):
        phase = (i / 24) * 4
        pose = int(phase)
        blend = (phase - pose) * 0.3
        frame = Image.blend(run_poses[pose], run_poses[(pose + 1) % 4], blend)
        move.append(transform(frame, y=-round(2 * math.sin(4 * math.pi * i / 24))))
    encode(VIDEOS / "move" / "轻快行走.webm", move)

    actions = [
        ("turn", "轻盈转身.webm", 36),
        ("click", "开心回应.webm", 36),
        ("drag", "悬空反馈.webm", 36),
        ("random", "挥手互动.webm", 48),
    ]
    for folder, name, count in actions:
        frames = []
        for i in range(count):
            phase = 2 * math.pi * i / count
            if folder == "turn":
                frame = transform(static, scale_x=1 - 0.10 * (math.sin(phase / 2) ** 2),
                                  x=round(3 * math.sin(phase)))
            elif folder == "click":
                frame = transform(static, scale_x=1 + 0.025 * math.sin(phase),
                                  scale_y=1 - 0.03 * math.sin(phase),
                                  y=-round(6 * max(0, math.sin(phase))))
            elif folder == "drag":
                frame = transform(static, y=-round(4 + 3 * math.sin(phase)),
                                  angle=2 * math.sin(phase))
            else:
                frame = transform(static, angle=2.5 * math.sin(phase),
                                  y=-round(2 * math.sin(phase)))
            frames.append(frame)
        encode(VIDEOS / folder / name, frames)

    manifest_path = CHARACTER / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    alpha = static.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    left, top, right, bottom = alpha.getbbox()
    manifest.update({
        "name": "女仆爱莉希雅 / Elysia",
        "body_box": [left, top, right, bottom],
        "head_box": [left, top, right, min(bottom, top + round((bottom - top) * 0.55))],
        "static": "Q版女仆爱莉希雅.png",
    })
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    (VIDEOS / "move_strides.json").write_text(
        json.dumps({"轻快行走.webm": {"stride": 90}}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    icon = static.copy()
    icon.thumbnail((256, 256), Image.Resampling.LANCZOS)
    icon.save(CHARACTER / "爱莉希雅桌宠.ico", format="ICO",
              sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])


if __name__ == "__main__":
    main()
