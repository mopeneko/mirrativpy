from mirrativpy.main import Mirrativ
import json


cookiess = {}
bot = Mirrativ()
bot.create_account(random=True)
bot.follow("id")
cookiess[bot.user_id] = bot.session.cookies.get_dict()
json.dump(cookiess, open("cookies.json", "w"), indent=4, ensure_ascii=False)
