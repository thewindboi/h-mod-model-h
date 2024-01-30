import discord
from discord import app_commands
from typing import Any, Coroutine, Optional
import os

TEST_GUILD = discord.Object(id=os.environ['GUILD'])

class modbot(discord.Client):
        def __init__(self, *, 
                     intents: discord.Intents):
                # Call discord.Client's constructor
                super().__init__(intents=intents)

                self.tree = app_commands.CommandTree(self)
        
        async def setup_hook(self):

                # Copies over to testing server
               self.tree.copy_global_to(guild=TEST_GUILD)
               
               # Syncs all commands
               await self.tree.sync()    # Global commands take a while to register with discord.
               await self.tree.sync(guild=TEST_GUILD)
               print("synced commands")


intents = discord.Intents.default()
intents.message_content = True
client = modbot(intents=intents)


@client.event
async def on_ready():
        print(f'logged in as {client.user} (ID: {client.user.id})')

        
        ''' MODERATOR UTILITIES '''

@client.tree.command(description="Kicks a member out of the server.")
@app_commands.describe(member="The member of the server to kick out.",
                       reason="The reason you kicked them.")
async def kick(interaction: discord.Interaction,
               member: discord.Member,
               reason: Optional[str]):
        await interaction.guild.kick(member, reason=reason)
        kick_embed = discord.Embed(
                color=0xFF0000,
                title=f"Kicked user {str(member)}",
                description=reason
        )
        await interaction.response.send_message(embed=kick_embed)


        ''' MISCELLANEOUS'''

@client.tree.command(description="Sends the time between a HEARTBEAT and a HEARTBEAT_ACK.")
async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f'Ping! Latency is {client.latency} seconds.', ephemeral=True)

@client.tree.command()
async def embed_test(interaction: discord.Interaction,
                     member: discord.Member):
        embed = discord.Embed(
                color=0xFF0000,
                title="Kick embed",
                description=f"Kicked {str(member)}."
        )
        embed.add_field(
                name="Reason",
                value=f"Reason: {str(member)} isnt h :("
        )
        await interaction.response.send_message("h", embed=embed)


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
