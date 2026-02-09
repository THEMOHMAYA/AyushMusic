import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch

from config import YOUTUBE_IMG_URL


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    try:
        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)

        for r in (await results.next())["result"]:
            duration = r.get("duration", "0:00")
            thumb = r["thumbnails"][0]["url"].split("?")[0]

        # ===== Download thumbnail =====
        async with aiohttp.ClientSession() as session:
            async with session.get(thumb) as resp:
                f = await aiofiles.open(f"cache/raw_{videoid}.jpg", "wb")
                await f.write(await resp.read())
                await f.close()

        yt = Image.open(f"cache/raw_{videoid}.jpg").convert("RGBA")
        yt = yt.resize((1280, 720))

        # ===== BLUR BACKGROUND =====
        bg = yt.filter(ImageFilter.GaussianBlur(25))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        # ===== WHITE CARD =====
        card_w, card_h = 900, 460
        card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 255))

        mask = Image.new("L", (card_w, card_h), 0)
        m = ImageDraw.Draw(mask)
        m.rounded_rectangle((0, 0, card_w, card_h), 35, fill=255)

        # ===== INNER THUMBNAIL =====
        inner_thumb = yt.resize((860, 300))
        card.paste(inner_thumb, (20, 20))

        draw = ImageDraw.Draw(card)

        # ===== FONTS =====
        font = ImageFont.truetype("AyushMusic/assets/font.ttf", 26)

        # ===== PLAYER LINE =====
        line_y = 350
        draw.line((60, line_y, 840, line_y), fill=(180, 180, 180), width=4)
        draw.ellipse((250, line_y - 7, 266, line_y + 7), fill="black")

        draw.text((60, 370), "00:00", fill="black", font=font)
        draw.text((780, 370), duration, fill="black", font=font)

        # ===== COMPOSE =====
        bg.paste(card, (190, 110), mask)

        # ===== POWERED BY TEXT =====
        final_draw = ImageDraw.Draw(bg)
        power_font = ImageFont.truetype("AyushMusic/assets/font.ttf", 28)
        final_draw.text(
            (640, 610),
            "Powered by AYUSH",
            fill=(220, 220, 220),
            anchor="mm",
            font=power_font,
        )

        bg.save(f"cache/{videoid}.png")
        os.remove(f"cache/raw_{videoid}.jpg")

        return f"cache/{videoid}.png"

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
