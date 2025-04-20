import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv('MTM2MzY0NzEwNDQxNjc0Nzc0MQ.GgRc2_.UD3LDNQP-Mf9fb9YMihJJKRa2HSXACPiGrOr30')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

# Хранилище "био" для пользователя (пока просто в словаре)
user_data = {}

class ModerationView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.button(label="Мут", style=discord.ButtonStyle.gray, custom_id="mute")
    async def mute(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data[self.member.id]['muted'] = True
        await interaction.response.send_message(f"✅ {self.member.mention} замучен!", ephemeral=True)

    @discord.ui.button(label="Варн", style=discord.ButtonStyle.blurple, custom_id="warn")
    async def warn(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data[self.member.id]['warns'] += 1
        await interaction.response.send_message(f"⚠️ {self.member.mention} получил варн!", ephemeral=True)

    @discord.ui.button(label="Бан", style=discord.ButtonStyle.danger, custom_id="ban")
    async def ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data[self.member.id]['banned'] = True
        await interaction.response.send_message(f"⛔ {self.member.mention} забанен!", ephemeral=True)

    @discord.ui.button(label="Обновить", style=discord.ButtonStyle.green, custom_id="refresh")
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_embed(self.member)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Снять мут", style=discord.ButtonStyle.secondary, row=1)
    async def unmute(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data[self.member.id]['muted'] = False
        await interaction.response.send_message(f"🔊 Снят мут с {self.member.mention}", ephemeral=True)

    @discord.ui.button(label="Снять варн", style=discord.ButtonStyle.secondary, row=1)
    async def unwarn(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data[self.member.id]['warns'] = 0
        await interaction.response.send_message(f"🧼 Варны очищены у {self.member.mention}", ephemeral=True)

    @discord.ui.button(label="Снять бан", style=discord.ButtonStyle.secondary, row=1)
    async def unban(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data[self.member.id]['banned'] = False
        await interaction.response.send_message(f"🔓 {self.member.mention} разбанен", ephemeral=True)

def create_embed(member: discord.Member):
    data = user_data.get(member.id, {
        'warns': 0,
        'muted': False,
        'banned': False
    })
    embed = discord.Embed(
        title="Выбери нужную тебе команду модерации",
        color=discord.Color.dark_gray()
    )
    embed.add_field(name="Пользователь", value=member.mention)
    embed.add_field(name="Варны", value=str(data['warns']))
    embed.add_field(name="В муте", value="Да" if data['muted'] else "Нет")
    embed.add_field(name="В бане", value="Да" if data['banned'] else "Нет")
    embed.add_field(name="Наказания", value="Пусто" if data['warns'] == 0 else "Имеются")
    embed.set_thumbnail(url=member.display_avatar.url)
    return embed

@tree.command(name="action", description="Открыть модерацию для участника")
@app_commands.describe(member="Участник для модерации")
async def action(interaction: discord.Interaction, member: discord.Member):
    if member.id not in user_data:
        user_data[member.id] = {'warns': 0, 'muted': False, 'banned': False}
    embed = create_embed(member)
    view = ModerationView(member)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Chromchik запущен как {bot.user}")

bot.run(MTM2MzY0NzEwNDQxNjc0Nzc0MQ.GgRc2_.UD3LDNQP-Mf9fb9YMihJJKRa2HSXACPiGrOr30)
