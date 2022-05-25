import discord
import wordle
import SQLmanager

game = wordle.Word()
class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        if message.author == self.user and message.content == '🟩🟩🟩🟩🟩':
            await message.channel.send('You win!')
            
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '!newuser':
            await message.channel.send(SQLmanager.db.NewUser(message.author))

        if message.content == '!leaderboard':
            await message.channel.send(SQLmanager.db.ShowLeaderboard())
        
        if message.content == '!wordle':
            game.generate()
            print(game.keyword)
            await message.channel.send('⬜⬜⬜⬜⬜')

        if len(message.content) == 5 and game.complete == False:
            await message.channel.send(game.guess(message.content.lower()))
            if game.complete:
                SQLmanager.db.AddWin(message.author)

        if message.content == '!letters':
            await message.channel.send(''.join(game.invalid_letters))
          
client = MyClient()
client.run('your token here')
