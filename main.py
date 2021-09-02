import discord
import logging
import asyncio
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
        await self.every_five_minutes()

    def check_if_it_is_me(self, message: discord.Message) -> None:
        return message.author.id == int(owner)

    async def send_results(self, embed: discord.Embed, content) -> None:
        for message in self.copyList:  # type:discord.Message
            if len(content) == 0:
                await message.edit(embed=embed, content="")
            else:
                await message.edit(embed=embed, content=content)

    async def set_flag_copy(self, message: discord.Message):
        newMessage = await message.channel.send("Will update next time a mvp is sent here")
        self.copyList.append(newMessage)

    # Checks if I called for a placed flag
    async def on_message(self, message: discord.Message):
        if message.content.startswith(command + "placeFlag") and self.check_if_it_is_me(message):
            await self.set_flag_copy(message)

    # async def on_raw_message_edit(self, after: discord.Message):
    #     print("message change detected")
    #
    #     mvp_id = 872901421417246800
    #     if after.message_id == mvp_id:
    #         message = await self.get_channel(838492366121861150).fetch_message(872901421417246800)
    #         if len(message.embeds) != 0:
    #             await self.send_results(message.embeds[0], message.content)
    #         await self.send_results(None, message.content)

    # After called, will update all the messages in copyList to the current MVP message
    async def every_five_minutes(self):
        message = await self.get_channel(838492366121861150).fetch_message(872901421417246800)
        # message = await self.get_channel(875050700852310045).fetch_message(883071638193725471)
        if len(message.embeds) != 0:
            await self.send_results(message.embeds[0], message.content)
        else:
            await self.send_results(None, message.content)
        await asyncio.sleep(5*60)
        task = asyncio.create_task(self.every_five_minutes())
        await task


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.messages = True
    client = MyClient(intents=intents)
    client.run(token)
