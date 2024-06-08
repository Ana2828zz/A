import discord
from discord import app_commands
from discord.ui import Select, View
from discord.ext import commands
import asyncio
from db.statusdb import membstat, CreateProfile, AddSaldo, ConvenePerLim, ConvenePerIlim



class Status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='resgistrar-se', description='Se registe para liberar sua conta!')
    async def register(self, interaction:discord.Interaction):
        CreateProfile(interaction.user, 0, 0, 0, 'Não há nada aqui!')
        await interaction.response.send_message(f'{interaction.user.display_name} se registrou!')

    @app_commands.command(name='saldo', description='Mostra seu saldo no Bot')
    async def balance(self, interaction:discord.Interaction, membro: discord.Member = None):
        if membro is None:
            membro = interaction.user
        check = membstat.find_one({'_id': membro.id})
        if check is None:
            await interaction.response.send_message(f'{membro.display_name} não tem registro')
        e = discord.Embed(title=f'Saldo de: {membro.display_name}')
        e.add_field(name='<:astrite:1245636166275825695> Astrites', value=membstat.find_one({"_id": membro.id})['astrite'])
        e.add_field(name='<:brilhante:1245636242906021920> Maré Brilhante', value=membstat.find_one({"_id": membro.id})['lustrous'])
        e.add_field(name='<:radiante:1245636213189251092> Maré Radiante', value=membstat.find_one({"_id": membro.id})['radiant'])
        e.add_field(name='Ressonadores e Itens', value=membstat.find_one({"_id": membro.id})['resona'])
        await interaction.response.send_message(embed=e)

    @app_commands.command(name='editar_saldo', description='Adicione ou remova saldo da conta de um membro')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(add_remove=[
        app_commands.Choice(name=f"[ ✅ ] Adicionar", value='+'),
        app_commands.Choice(name="[ ❌ ] Remover", value='-')
        ])
    @app_commands.choices(item=[
        app_commands.Choice(name=f"[ ⚪ ] Astrite", value='astrite'),
        app_commands.Choice(name="[ 🔵 ] Maré Brilhante", value='lustrous'),
        app_commands.Choice(name="[ 🟡 ] Maré Radiante", value='radiant')
        ])
    async def add_saldo(self, interaction:discord.Interaction, add_remove: app_commands.Choice[str], valor: int, item: app_commands.Choice[str], membro: discord.Member):
        check = membstat.find_one({'_id': membro.id})
        if check is None:
            await interaction.response.send_message(f'{membro.display_name} não tem registro')
        AddSaldo(membro, add_remove.value , item.value, valor)
        if item.value == 'astrite':
            item_name = '[ <:astrite:1245636166275825695> ] Astrite'
        elif item.value == 'lustrous':
            item_name = '[ <:brilhante:1245636242906021920> ] Maré Brilhante'
        elif item.value == 'radiant':
            item_name = '[ <:radiante:1245636213189251092> ] Maré Radiante'
        await interaction.response.send_message(f'{item_name} {add_remove.value}{valor} para {membro.display_name}')

    @app_commands.command(name='convene', description='Visualize e atire no banner')
    async def convene(self, interaction: discord.Interaction):
        author = interaction.user
        class Dropdown(discord.ui.Select):
            def __init__(self):
                options = [
            discord.SelectOption(label='Banner Personagem Limitado', value='https://i.ibb.co/ByVYZHS/174-Sem-T-tulo-20240601033931.png', description='Banner de personagem de evento limitado!', emoji='<:radiante:1245636213189251092>'),
            discord.SelectOption(label='Banner Arma Limitado', value='https://i.ibb.co/fn364QL/IMG-3326.jpg', description='Banner de arma de evento limitado!', emoji='<:radiante:1245636213189251092>'),
            discord.SelectOption(label='Banner Personagem Ilimitado', value='https://i.ibb.co/XXfdnQj/IMG-3327.jpg', description='Banner de personagem de evento ilimitado', emoji='<:brilhante:1245636242906021920>'),
            discord.SelectOption(label='Banner Arma Ilimitado', description='Banner de arma de evento ilimitado', emoji='<:brilhante:1245636242906021920>')
        ]
                super().__init__(placeholder='Escolha o banner...', min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                authorcmd = author
                selected_value = self.values[0]
                selected_option = next(option for option in self.options if option.value == selected_value)
                label = selected_option.label
                value = selected_option.value
                emojis = selected_option.emoji
                class ConveneAction(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                    @discord.ui.button(label="1x  Convene x1", style=discord.ButtonStyle.blurple, emoji=emojis)
                    async def convene_1(self, interaction: discord.Interaction, button: discord.ui.Button):
                        banner = 'perlim1'
                        conveneperlim = ConvenePerLim(interaction.user, banner)
                        conveneperilim = ConvenePerIlim(interaction.user, banner)
                        if label == 'Banner Personagem Limitado':
                            tiro = 'radiant'
                            result, resultados, categoria, url_imagem, url_imagem10 = conveneperlim
                        elif label == 'Banner Arma Limitado':
                            tiro = 'radiant'
                        elif label == 'Banner Personagem Ilimitado':
                            tiro = 'lustrous'
                            result, resultados, categoria, url_imagem, url_imagem10 = conveneperilim
                        elif label == 'Banner Arma Ilimitado':
                            tiro = 'lustrous'
                        checkbal = membstat.find_one({"_id": interaction.user.id})[tiro]
                        if interaction.user == author and checkbal >= 1:
                            membstat.update_one({'_id': interaction.user.id},{'$inc':{tiro: -1}})
                            e = discord.Embed(title=f'__***{interaction.user.display_name} ATIROU 1x EM {label} !!!***__')
                            e.set_image(url=url_imagem)
                            
                            await interaction.response.edit_message(embed=e, view=None)
                            await asyncio.sleep(7)
                            await interaction.channel.send(result)
                        else:
                            await interaction.response.send_message('Você não tem tiros o suficiente!', ephemeral=True)
                             
                    @discord.ui.button(label="10x  Convene x10", style=discord.ButtonStyle.blurple, emoji=emojis)
                    async def convene_10(self, interaction: discord.Interaction, button: discord.ui.Button):
                        banner = 'perlim10'
                        conveneperlim = ConvenePerLim(interaction.user, banner)
                        conveneperilim = ConvenePerIlim(interaction.user, banner)
                        if label == 'Banner Personagem Limitado':
                            tiro = 'radiant'
                            result, resultados, categoria, url_imagem, url_imagem10 = conveneperlim
                        elif label == 'Banner Arma Limitado':
                            tiro = 'radiant'
                        elif label == 'Banner Personagem Ilimitado':
                            tiro = 'lustrous'
                            result, resultados, categoria, url_imagem, url_imagem10 = conveneperilim
                        elif label == 'Banner Arma Ilimitado':
                            tiro = 'lustrous'
                        class ConvenePull(discord.ui.View):
                            def __init__(self):
                                super().__init__()
                            @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji='⏩')
                            async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                                e.add_field(name=f'{resultados[f'tiro{n+1}']}')
                                n = n+1

                        checkbal = membstat.find_one({"_id": interaction.user.id})[tiro]
                        if interaction.user == author and checkbal >= 10:
                            membstat.update_one({'_id': interaction.user.id},{'$inc':{tiro: -10}})
                            e = discord.Embed(title=f'__***{interaction.user.display_name} ATIROU 10x EM {label} !!!***__')
                            e.set_image(url=url_imagem10)
                            await interaction.response.edit_message(embed=e, view=None)
                            await asyncio.sleep(7)
                            e = discord.Embed(title=f'***{interaction.user.display_name}***')
                            e.add_field(name=f'1 - {resultados[f'tiro1']}', value='')
                            num = 2
                            class ConvenePull(discord.ui.View):
                                def __init__(self):
                                    super().__init__()
                                    self.num = 2
                                @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji='▶️')
                                async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                                            e.add_field(name=f'{self.num} - {resultados[f'tiro{self.num}']}', value='')
                                            if self.num <= 9:
                                                await interaction.response.edit_message(embed=e)
                                                self.num = self.num+1
                                            else:
                                                await interaction.response.edit_message(embed=e, view=None)
                                    
                                @discord.ui.button(label="SKIP", style=discord.ButtonStyle.gray, emoji='⏩')
                                async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
                                    for _ in range(self.num,11):
                                        e.add_field(name=f'{self.num} - {resultados[f'tiro{self.num}']}', value='')
                                        self.num = self.num+1
                                    await interaction.response.edit_message(embed=e, view=None)

                            await interaction.channel.send(embed=e, view=ConvenePull())
                        else:
                            await interaction.response.send_message('Você não tem tiros o suficiente!', ephemeral=True)
                    @discord.ui.button(label="Pity", style=discord.ButtonStyle.gray, emoji='❕')
                    async def pity_view(self, interaction: discord.Interaction, button: discord.ui.Button):
                        if label == 'Banner Personagem Limitado':
                            rpity4 = 'pity4perlim'
                            rpity5 = 'pity5perlim'
                        elif label == 'Banner Arma Limitado':
                            rpity4 = 'pity4armlim'
                            rpity5 = 'pity5armlim'
                        elif label == 'Banner Personagem Ilimitado':
                            rpity4 = 'pity4perilim'
                            rpity5 = 'pity5perilim'
                        elif label == 'Banner Arma Ilimitado':
                            rpity4 = 'pity4armilim'
                            rpity5 = 'pity5armilim'
                        pity4 = membstat.find_one({"_id": interaction.user.id})[rpity4]
                        pity5 = membstat.find_one({"_id": interaction.user.id})[rpity5]
                        e = discord.Embed(title=f'**Pity de:** __***{interaction.user.display_name}***__', description=f'Banner: ***{label}***')
                        e.add_field(name='[⭐] 4 Estrelas: ', value=pity4)
                        e.add_field(name='[⭐] 5 Estrelas: ', value=pity5)
                        if label == 'Banner Personagem Limitado':
                            garantido = membstat.find_one({"_id": interaction.user.id})['garantido']
                            if garantido == 'nao':
                                rgaran = '❌'
                            else:
                                rgaran = '✅'
                            e.add_field(name='[⭐] Garantido: ', value=rgaran)
                        await interaction.response.edit_message(embed=e, view=ConveneAction())
                if interaction.user == authorcmd:
                    e = discord.Embed(title=f'__***{label}***__')
                    e.set_image(url=value)
                    await interaction.response.edit_message(embed=e, view=ConveneAction())

        class DropdownView(discord.ui.View):
            def __init__(self):
                super().__init__()

                self.add_item(Dropdown())
        await interaction.response.send_message('Selecione o banner que queira ver:', view=DropdownView())


async def setup(client):
    await client.add_cog(Status(client))