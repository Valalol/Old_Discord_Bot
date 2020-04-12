import discord
from discord.ext import commands

class Commandes_Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clean','removemsg'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int, author : discord.Member = None):
        """Supprime un certain nombre de messages"""
        await ctx.message.delete()
        if author == None:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'I have deleted {amount} messages. :unicorn:', delete_after=4)
        else:
            def author_check(m):
                return m.author == author
            await ctx.channel.purge(limit=amount+1, check = author_check)
            await ctx.send(f'I have deleted {amount} messages of {author}. :unicorn:', delete_after=4)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f"Veuillez spécifier le nombre de message à supprimer.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help clear.")
    
    @commands.command()
    @commands.has_permissions(kick_members=True) 
    async def kick(self, ctx, user : discord.Member, *, reason=None):
        """Expulse un membre du serveur"""
        await user.kick(reason=reason)
        try :
            embed=discord.Embed(title=f'{user} a été expulsé du serveur', color=0x00ff00)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            embed.add_field(name=f"Raison", value=reason)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{user} a été expulsé du serveur par {ctx.message.author}.\nLa raison de cette explusion est la suivante : {reason}')
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xff0000)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help kick.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à expulser.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help kick.")
        else:
            print(error)

    @commands.command()
    @commands.has_permissions(ban_members=True) 
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        """Bannit un membre du serveur"""
        await user.ban(reason=reason)
        try :
            embed=discord.Embed(title=f'{user} a été banni du serveur', color=0x00ff00)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            embed.add_field(name=f"Raison", value=reason)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{user} a été banni du serveur par {ctx.message.author}.\nLa raison de ce bannissement est la suivante : {reason}')
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xff0000)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help ban.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à bannir.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help ban.")
        else:
            print(error)


def setup(client):
    client.add_cog(Commandes_Admin(client))