
from AyushMusic.core.bot import Aru
from AyushMusic.core.dir import dirr
from AyushMusic.core.git import git
from AyushMusic.core.userbot import Userbot
from AyushMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Aru()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()


