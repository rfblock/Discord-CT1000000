import discord
from dotenv import dotenv_values


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
config = { **dotenv_values('.env') }

@client.event
async def on_read():
	print(f'Logged in as {client.user}')

with open('data.txt') as f:
	last_num = int(f.readline())
	last_user = f.readline()

@client.event
async def on_message(message):
	global last_num, last_user
	
	if message.author == client.user:
		return
	if str(message.channel) != 'count-test':
		return

	try:
		new_num = int(message.content.split(' -')[0])
		if new_num == last_num + 1 and str(message.author) != last_user:
			last_num = new_num
			last_user = str(message.author)
			with open('data.txt', 'w') as f:
				f.write(str(new_num) + '\n' + last_user)
		else:
			raise ValueError
	except ValueError:
		print(f'{message.author}: {message.content}')
		await message.delete()

if __name__ == '__main__':
	client.run(config['BOT_TOKEN'])