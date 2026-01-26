import os
import re
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from youtubesearchpython.__future__ import VideosSearch

WIDTH, HEIGHT = 1280, 720
CACHE = "cache"
ASSETS = "AyushMusic/assets"


def circle_crop(img, mask):
    img = img.resize(mask.size, Image.Resampling.LANCZOS).convert("RGBA")
    out = Image.new("RGBA", mask.size)
    out.paste(img, (0, 0), mask)
    return out


async def download(url, path):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            if r.status != 200:
                return False
            async with aiofiles.open(path, "wb") as f:
                await f.write(await r.read())
    return True


async def get_yt(videoid):
    search = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
    data = (await search.next())["result"][0]
    title = re.sub(r"\s+", " ", data["title"])
    duration = data["duration"]
    thumb = data["thumbnails"][0]["url"].split("?")[0]
    return title, duration, thumb


async def gen_thumbnail(videoid, user_photo):
    os.makedirs(CACHE, exist_ok=True)
    output = f"{CACHE}/{videoid}.png"

    title, duration, yt_thumb = await get_yt(videoid)

    yt_path = f"{CACHE}/yt.png"
    user_path = f"{CACHE}/user.png"

    await download(yt_thumb, yt_path)
    await download(user_photo, user_path)

    # Load images
    yt = Image.open(yt_path).convert("RGBA")
    user = Image.open(user_path).convert("RGBA")
    circle = Image.open(f"{ASSETS}/circle.png").convert("L")

    # Background
    bg = yt.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(35))
    bg = ImageEnhance.Color(bg).enhance(0.8)
    bg = ImageEnhance.Brightness(bg).enhance(0.6)

    # Blue overlay
    overlay = Image.new("RGBA", bg.size, (30, 60, 160, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    # Big circle (YT thumb)
    big_mask = circle.resize((360, 360))
    big = circle_crop(yt, big_mask)
    bg.paste(big, (460, 160), big)

    # Small circle (user)
    small_mask = circle.resize((120, 120))
    small = circle_crop(user, small_mask)
    bg.paste(small, (650, 380), small)

    draw = ImageDraw.Draw(bg)

    font_head = ImageFont.truetype(f"{ASSETS}/font2.ttf", 44)
    font_title = ImageFont.truetype(f"{ASSETS}/font.ttf", 36)
    font_small = ImageFont.truetype(f"{ASSETS}/font2.ttf", 26)

    # Texts
    draw.text((WIDTH//2, 70), "STARTED PLAYING",
              font=font_head, fill="white", anchor="mm")

    draw.text((WIDTH//2, 550), title,
              font=font_title, fill="white", anchor="mm")

    draw.text((WIDTH//2, 600), f"Duration : {duration}",
              font=font_small, fill="#dddddd", anchor="mm")

    bg.save(output)

    os.remove(yt_path)
    os.remove(user_path)

    return output
