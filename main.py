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
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction,
               member: discord.Member,
               reason: Optional[str]):
        
        kick_embed = discord.Embed(
                color=0xFF0000,
                title=f"Kicked user {str(member)}",
                description=reason
        )

        if discord.Permissions.administrator in member.guild_permissions:
                kick_embed.title = "Error while kicking user:"
                kick_embed.description = "User is administrator."
                await interaction.response.send_message(embed=kick_embed)
                return
        
        await interaction.guild.kick(member, reason=reason)
        await interaction.response.send_message(embed=kick_embed)

@kick.error
async def kick_error(interaction: discord.Interaction, 
                     err: app_commands.AppCommandError):
        kick_embed = discord.Embed(
                color=0xFF0000,
                title="Error"
        )
        if isinstance(err, app_commands.errors.MissingPermissions):
                kick_embed.description = "You do not have the nessecary permisions."
                await interaction.response.send_message(embed=kick_embed, ephemeral=True)
        


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
