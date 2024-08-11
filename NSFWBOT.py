from discord import File
from discord.ext import commands
import io
import requests
import random
from bs4 import BeautifulSoup
from utilites import ban_check


class NSFWBot(commands.Cog):
	"""Хентый комманды"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='genshin_porn', aliases=['genshin_p'])
	@commands.is_nsfw()
	@commands.check(ban_check)
	async def _genshin_porn(self, ctx):
		headers = {'Referer': 'http://thatpervert.com/'}
		hentai_list = requests.get(r"http://thatpervert.com/tag/Genshin+Impact+porn", headers=headers)
		soup = BeautifulSoup(hentai_list.text, "lxml")
		page_last = int(soup.find('div', class_='pagination_expanded').find('span', class_='current').text)
		random_page = random.randint(0, page_last)
		hentai_page = requests.get(rf"http://thatpervert.com/tag/Genshin+Impact+porn/{random_page}", headers=headers)
		image = BeautifulSoup(hentai_page.text, "lxml")
		list_image = image.find_all('a', class_='prettyPhotoLink')
		request_image = requests.get(random.choice(list_image).get('href'), headers=headers).content
		await ctx.send("Рандом Хентыч Гашиш", file=File(io.BytesIO(request_image), filename='genshin.png'))


def setup(bot):
	bot.add_cog(NSFWBot(bot))
