import os
import re
import aiofiles
import aiohttp
import textwrap
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from AyushMusic import app
from config import YOUTUBE_IMG_URL

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / float(image.size[0])
    heightRatio = maxHeight / float(image.size[1])
    newSize = int(image.size[0] * widthRatio), int(image.size[1] * heightRatio)
    image = image.resize(newSize, Image.LANCZOS)
    return image

async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        
        # Background Processing
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.filter(ImageFilter.GaussianBlur(radius=40))
        image3 = ImageEnhance.Brightness(image2)
        image3.enhance(0.5).save(f"cache/temp{videoid}.png")
        background = Image.open(f"cache/temp{videoid}.png")
        draw = ImageDraw.Draw(background)
        
        # Font Paths (Check if they exist in assets)
        font = ImageFont.truetype("assets/font.ttf", 30)
        font2 = ImageFont.truetype("assets/font2.ttf", 70)
        font3 = ImageFont.truetype("assets/font2.ttf", 40)

        # Circular Thumbnail Logic
        circle_thumbnail = image1.resize((450, 450), Image.LANCZOS)
        mask = Image.new("L", (450, 450), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 450, 450), fill=255)
        
        # Paste Circular Image
        background.paste(circle_thumbnail, (120, 135), mask)
        
        # --- NEW: Paste your circle.png frame ---
        # Assuming circle.png is in your main directory or assets/
        if os.path.exists("assets/circle.png"):
            circle_frame = Image.open("assets/circle.png")
        elif os.path.exists("circle.png"):
            circle_frame = Image.open("circle.png")
        else:
            circle_frame = None
            
        if circle_frame:
            circle_frame = circle_frame.resize((480, 480), Image.LANCZOS)
            background.paste(circle_frame, (105, 120), circle_frame.convert("RGBA"))
        # ----------------------------------------

        # Text Drawing
        para = textwrap.wrap(title, width=32)
        if para:
            draw.text((630, 200), para[0], fill="white", font=font2)
            if len(para) > 1:
                draw.text((630, 280), para[1], fill="white", font=font2)

        draw.text((630, 410), f"Views : {views}", fill="white", font=font3)
        draw.text((630, 470), f"Duration : {duration}", fill="white", font=font3)
        draw.text((630, 530), f"Channel : {channel}", fill="white", font=font3)

        background.save(f"cache/{videoid}.png")
        
        # Cleanup
        try:
            os.remove(f"cache/temp{videoid}.png")
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        return f"cache/{videoid}.png"
    except Exception as e:
        print(f"Error in thumbnail: {e}")
        return YOUTUBE_IMG_URL
