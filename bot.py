from discord.ext import commands, tasks
from discord import Intents
import discord
import os
import json
from threading import Lock

# Armazenamento em memória para dados do usuário
user_data = {}
data_lock = Lock()
data_file = 'user_data.json'

# Função para carregar dados do arquivo
def load_data():
    global user_data
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                user_data = json.load(f)
            except json.JSONDecodeError:
                print("Erro ao carregar dados: arquivo JSON corrompido")
                user_data = {}
    else:
        user_data = {}

# Função para salvar dados no arquivo com bloqueio
def save_data():
    with data_lock:
        with open(data_file, 'w') as f:
            json.dump(user_data, f, indent=4)

# Função para assegurar a integridade dos dados de um usuário
def ensure_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"saldo": 0}

# Carregar dados na inicialização
load_data()

intents = Intents.default()
intents.message_content = True  # Habilite intents adicionais conforme necessário

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    auto_save_task.start()

@bot.event
async def on_disconnect():
    print('Bot desconectado')

@bot.command(name="iniciar_banner")
@commands.has_permissions(administrator=True)
async def init_banner(ctx, banner_name: str, description: str):
    await ctx.send(f"Banner {banner_name} iniciado com a descrição: {description}")

@tasks.loop(minutes=5)
async def auto_save_task():
    save_data()

class SelectMenuView(discord.ui.View):
    @discord.ui.select(
        placeholder="Escolha o banner...",
        options=[
            discord.SelectOption(label="Banner Personagem Ilimitado", description="Banner de personagem ilimitado"),
            discord.SelectOption(label="Banner Arma Ilimitado", description="Banner de arma ilimitado"),
        ]
    )
    async def select_callback(self, select, interaction):
        user_id = str(interaction.user.id)
        ensure_user_data(user_id)
        if select.values[0] == "Banner Personagem Limitado":
            await interaction.response.send_message("Banner Personagem Limitado")
            await interaction.followup.send("[Imagem](URL_IMAGEM_BANNER_PERSONAGEM_LIMITADO)")
        elif select.values[0] == "Banner Arma Limitado":
            await interaction.response.send_message("Banner Arma Limitado")
            await interaction.followup.send("[Imagem](URL_IMAGEM_BANNER_ARMA_LIMITADO)")
        elif select.values[0] == "Banner Personagem Ilimitado":
            await interaction.response.send_message("Banner Personagem Ilimitado")
            await interaction.followup.send("[Imagem](URL_IMAGEM_BANNER_PERSONAGEM_ILIMITADO)")
        elif select.values[0] == "Banner Arma Ilimitado":
            await interaction.response.send_message("Banner Arma Ilimitado")
            await interaction.followup.send("[Imagem](URL_IMAGEM_BANNER_ARMA_ILIMITADO)")
        save_data()

@bot.command(name="menu_banner")
async def menu_banner(ctx):
    view = SelectMenuView()
    await ctx.send("Selecione o banner que você deseja ver:", view=view)

# Inicie o bot
bot.run('SEU_TOKEN_DO_BOT')