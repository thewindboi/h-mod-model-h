import discord
from discord import app_commands
from typing import Any, Union, Optional
from datetime import datetime, timedelta
import os
import random

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
               await self.tree.sync(guild=None)    # Global commands take a while to register with discord.
               await self.tree.sync(guild=TEST_GUILD)
               print("synced commands")


intents = discord.Intents.default()
intents.message_content = True
client = modbot(intents=intents)


@client.event
async def on_ready():
        print(f'logged in as {client.user} (ID: {client.user.id})')

        
''' MODERATOR UTILITIES '''

#----------
# Kick command 
#----------
@client.tree.command(description="Kicks a member out of the server.")
@app_commands.describe(member="The member of the server to kick out.",
                       reason="The reason you kicked them.")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction,
               member: discord.Member,
               reason: Optional[str] = None):
        
        if member == interaction.user or member.top_role >= interaction.user.top_role:
                raise discord.Forbidden
        
        kick_embed = discord.Embed(
                color=0xFF0000,
                title=f"Kicked user {str(member)}",
                description=reason
        )
        
        await interaction.guild.kick(member, reason=reason)
        await interaction.response.send_message(embed=kick_embed)

#----------
# Kick command error handling
#----------
@kick.error
async def kick_error(interaction: discord.Interaction, 
                     err: app_commands.AppCommandError):
        kick_embed = discord.Embed(
                color=0xFF0000,
                title="Error"
        )
        if isinstance(err, app_commands.errors.MissingPermissions):
                kick_embed.description = "You do not have the nessecary permissions."
                await interaction.response.send_message(embed=kick_embed, ephemeral=True)
        elif isinstance(err, discord.Forbidden):
                kick_embed.description = "You are unable to kick this person."
                await interaction.response.send_message(embed=kick_embed, ephemeral=True)
        else:
                kick_embed.description = "Unable to kick user."
                await interaction.response.send_message(embed=kick_embed, ephemeral=True)

#----------
# Ban command 
#----------
@client.tree.command(description="Bans a member from the server.")
@app_commands.describe(member="The member of the server to ban.",
                       reason="The reason you banned them.")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction,
               member: discord.Member,
               reason: Optional[str] = None):
        
        if member == interaction.user or member.top_role >= interaction.user.top_role:
                raise discord.Forbidden
        
        ban_embed = discord.Embed(
                color=0xFF0000,
                title=f"Banned user {str(member)}",
                description=reason
        )

        await interaction.guild.ban(member, reason=reason)
        await interaction.response.send_message(embed=ban_embed)

#----------
# Ban command error handling
#----------
@ban.error
async def ban_error(interaction: discord.Interaction, 
                     err: app_commands.AppCommandError):
        ban_embed = discord.Embed(
                color=0xFF0000,
                title="Error"
        )
        if isinstance(err, app_commands.errors.MissingPermissions):
                ban_embed.description = "You do not have the nessecary permissions."
                await interaction.response.send_message(embed=ban_embed, ephemeral=True)
        elif isinstance(err, discord.Forbidden):
                ban_embed.description = "You are unable to ban this person."
                await interaction.response.send_message(embed=ban_embed, ephemeral=True)
        else:
                ban_embed.description = "Unable to ban user."
                await interaction.response.send_message(embed=ban_embed, ephemeral=True)
                print(err)     


#----------
# Timeout command 
#----------
@client.tree.command(description="Timeouts a user.")
@app_commands.describe(time="The number of hours to time them out for (0 to remove timeout).")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction,
                   member: discord.Member,
                   time: int,
                   reason: Optional[str]):
        
        if member == interaction.user or member.top_role >= interaction.user.top_role:
                raise discord.Forbidden
        
        timeout_embed = discord.Embed(
                color=0xFF0000,
                title=f"Timed out user {str(member)} for {time} hours.",
                description=reason
        )
        
        deltatime = timedelta(hours=time)

        if not time:
                timeout_embed.title = f"Removed timeout from {str(member)}."
                
        await member.timeout(deltatime, reason=reason)
        await interaction.response.send_message(embed=timeout_embed)

#----------
# Timeout command error handling
#----------
@timeout.error
async def timeout_error(interaction: discord.Interaction, 
                        err: app_commands.AppCommandError):
        timeout_embed = discord.Embed(
                color=0xFF0000,
                title="Error"
        )
        if isinstance(err, app_commands.errors.MissingPermissions):
                timeout_embed.description = "You do not have the nessecary permissions."
                await interaction.response.send_message(embed=timeout_embed, ephemeral=True)
        elif isinstance(err, discord.Forbidden):
                timeout_embed.description = "You are unable to timeout this user."
                await interaction.response.send_message(embed=timeout_embed, ephemeral=True)
        else:
                timeout_embed.description = "Unable to timeout user."
                await interaction.response.send_message(embed=timeout_embed, ephemeral=True)
                print(err)

''' MISCELLANEOUS'''

@client.tree.command(description="Sends the time between a HEARTBEAT and a HEARTBEAT_ACK.")
async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f'Ping! Latency is {client.latency} seconds.', ephemeral=True)

@client.tree.command(description="H")
async def h(interaction: discord.Interaction):
        h_responses = ["H",
                       "H is gud",
                       "h",
                       "ver rare h message"]
        h_weights = [0.45,
                     0.25,
                     0.25,
                     0.05]
        await interaction.response.send_message(random.choice(h_responses, h_weights), ephemeral=True)



TOKEN = os.environ['TOKEN']
client.run(TOKEN)
