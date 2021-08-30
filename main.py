import discord
import logging
import pickle
import os

logging.basicConfig(level=logging.INFO)
command = "."
owner = "219905033876013058"
token = os.getenv("DISC_TOKEN0")


class MyClient(discord.Client):
    async def on_ready(self):

        print('Logged on as {0}!'.format(self.user))
        self.copyList = []

    def check_if_it_is_me(self, message: discord.Message) -> None:
        return message.author.id == int(owner)

    async def send_results(self, embed: discord.Embed, content) -> None:
        for message in self.copyList:  # type:discord.Message
            await message.edit(embed=embed, content=content)

    async def set_flag_copy(self, message: discord.Message):
        newMessage = await message.channel.send("Will update next time a mvp is sent here")
        self.copyList.append(newMessage)

    async def on_message(self, message: discord.Message):
        if message.content.startswith(command + "placeFlag") and message.author.guild_permissions.administrator:
            await self.set_flag_copy(message)

    async def on_raw_message_edit(self, after: discord.Message):
        print("message change detected")

        mvp_id = 881722819237539911
        if after.message_id == mvp_id:
            message = await self.get_channel(875050700852310042).fetch_message(881722819237539911)
            if (len(message.embeds) != 0):
                await self.send_results(message.embeds[0], message.content)
            await self.send_results(None, message.content)


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.messages = True
    client = MyClient(intents=intents)
    client.run(token)
