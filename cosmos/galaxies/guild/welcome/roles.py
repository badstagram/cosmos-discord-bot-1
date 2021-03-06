"""
Cosmos: A General purpose Discord bot.
Copyright (C) 2020 thec0sm0s

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .base import WelcomeBase

import discord

from discord.ext import commands


class WelcomeRoles(WelcomeBase):
    """Assign roles to new members right after they join your server.
    If User Verification is enabled in the server, the welcome roles are added only after they are verified.

    """

    @staticmethod
    async def give_roles(guild_profile, member):
        if guild_profile.welcome_roles:
            await member.add_roles(*guild_profile.welcome_roles, reason="Welcome Roles")

    @WelcomeBase.listener(name="on_member_join")
    async def on_member_join_roles(self, member):
        guild_profile = await self.cache.get_profile(member.guild.id)
        if not guild_profile.verification.role:
            await self.give_roles(guild_profile, member)

    @WelcomeBase.listener(name="on_member_verification")
    async def on_member_verification_roles(self, guild_profile, member):
        await self.give_roles(guild_profile, member)

    @WelcomeBase.welcome.group(name="roles", aliases=["role"], invoke_without_command=True)
    async def welcome_roles(self, ctx):
        """Displays the list of roles being assigned to every new members joining the server."""
        if not ctx.guild_profile.welcome_roles:
            return await ctx.send_line(f"❌    There are no roles assigned for welcome roles.")
        embed = ctx.embed_line("Welcome Roles", ctx.author.avatar_url)
        role_mentions = [f"{ctx.emotes.misc.next} {role.mention}" for role in ctx.guild_profile.welcome_roles]
        embed.description = "\n".join(role_mentions) + "\n​"
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @welcome_roles.command(name="set", aliases=["setup", "add"])
    @commands.bot_has_permissions(manage_roles=True)
    async def set_welcome_roles(self, ctx, *roles: discord.Role):
        """Set roles which will be assigned to every new members joining your server."""
        await ctx.guild_profile.set_welcome_roles(roles)
        await ctx.send_line(f"✅    Provided roles has been set for welcome roles.")

    @welcome_roles.command(name="remove", aliases=["delete", "clear"])
    async def remove_welcome_roles(self, ctx):
        """Remove all of the roles from welcome roles if set any."""
        if not await ctx.confirm():
            return
        await ctx.guild_profile.remove_welcome_roles()
        await ctx.send_line(f"✅    All of the roles has been removed from welcome roles.")
