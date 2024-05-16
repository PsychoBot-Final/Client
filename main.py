import sys
from util import init
from discord_app import DiscordApp



if __name__ == '__main__':
    init()
    app = DiscordApp(sys.argv)
    app.run()