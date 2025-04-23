import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from datetime import timedelta

TOKEN = "MTM2MzYzNjM2MTUxMjM1MzgzNA.GxHebf.0fSWDNOpCKx1wbUUuH1iq59QeLwPwckIhTke14"
GUILD_ID = 1332279312195260446

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Временное хранилище данных
user_data = {}

class ModerationView(View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

        # Верхний ряд кнопок
        self.add_item(Button(label="Мут", style=discord.ButtonStyle.red, row=0))
        self.add_item(Button(label="Варн", style=discord.ButtonStyle.blurple, row=0))
        self.add_item(Button(label="Бан", style=discord.ButtonStyle.red, row=0))
        self.add_item(Button(label="Обновить", style=discord.ButtonStyle.green, row=0))

        # Нижний ряд кнопок
        self.add_item(Button(label="Снять мут", style=discord.ButtonStyle.gray, row=1))
        self.add_item(Button(label="Снять варн", style=discord.ButtonStyle.gray, row=1))
        self.add_item(Button(label="Снять бан", style=discord.ButtonStyle.gray, row=1))

    async def update_message(self, interaction: discord.Interaction):
        data = user_data.get(self.member.id, {"warns": 0, "muted": False, "banned": False})

        embed = discord.Embed(
            title="Выбери нужную тебе команду модерации",
            color=discord.Color.dark_grey()
        )
        embed.add_field(name="Пользователь", value=self.member.mention, inline=True)
        embed.add_field(name="Варны", value=str(data["warns"]), inline=True)
        embed.add_field(name="В муте", value="Да" if data["muted"] else "Нет", inline=True)
        embed.add_field(name="В бане", value="Да" if data["banned"] else "Нет", inline=True)
        embed.add_field(name="Наказания", value="Пусто" if data["warns"] == 0 else "Имеются", inline=True)
        embed.set_thumbnail(url=self.member.display_avatar.url)

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Мут", style=discord.ButtonStyle.red, row=0)
    async def mute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id not in user_data:
            user_data[self.member.id] = {"warns": 0, "muted": False, "banned": False}
        user_data[self.member.id]["muted"] = True
        await interaction.response.send_message(f"🔇 {self.member.mention} замьючен", ephemeral=True)
        await self.update_message(interaction)

    @discord.ui.button(label="Варн", style=discord.ButtonStyle.blurple, row=0)
    async def warn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id not in user_data:
            user_data[self.member.id] = {"warns": 0, "muted": False, "banned": False}
        user_data[self.member.id]["warns"] += 1
        await interaction.response.send_message(f"⚠️ Варн выдан {self.member.mention}", ephemeral=True)
        await self.update_message(interaction)

    @discord.ui.button(label="Бан", style=discord.ButtonStyle.red, row=0)
    async def ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id not in user_data:
            user_data[self.member.id] = {"warns": 0, "muted": False, "banned": False}
        user_data[self.member.id]["banned"] = True
        await interaction.response.send_message(f"⛔ {self.member.mention} забанен", ephemeral=True)
        await self.update_message(interaction)

    @discord.ui.button(label="Обновить", style=discord.ButtonStyle.green, row=0)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_message(interaction)

    @discord.ui.button(label="Снять мут", style=discord.ButtonStyle.gray, row=1)
    async def unmute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id in user_data:
            user_data[self.member.id]["muted"] = False
            await interaction.response.send_message(f"🔊 С {self.member.mention} снят мут", ephemeral=True)
            await self.update_message(interaction)

    @discord.ui.button(label="Снять варн", style=discord.ButtonStyle.gray, row=1)
    async def unwarn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id in user_data:
            user_data[self.member.id]["warns"] = 0
            await interaction.response.send_message(f"⚠️ Варны сняты у {self.member.mention}", ephemeral=True)
            await self.update_message(interaction)

    @discord.ui.button(label="Снять бан", style=discord.ButtonStyle.gray, row=1)
    async def unban(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id in user_data:
            user_data[self.member.id]["banned"] = False
            await interaction.response.send_message(f"✅ {self.member.mention} разбанен", ephemeral=True)
            await self.update_message(interaction)

@bot.tree.command(name="action", description="Меню модерации")
@app_commands.describe(member="Участник для модерации")
async def action(interaction: discord.Interaction, member: discord.Member):
    if member.id not in user_data:
        user_data[member.id] = {"warns": 0, "muted": False, "banned": False}

    data = user_data[member.id]
    embed = discord.Embed(
        title="Выбери нужную тебе команду модерации",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Пользователь", value=member.mention, inline=True)
    embed.add_field(name="Варны", value=str(data["warns"]), inline=True)
    embed.add_field(name="В муте", value="Да" if data["muted"] else "Нет", inline=True)
    embed.add_field(name="В бане", value="Да" if data["banned"] else "Нет", inline=True)
    embed.add_field(name="Наказания", value="Пусто" if data["warns"] == 0 else "Имеются", inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)

    await interaction.response.send_message(embed=embed, view=ModerationView(member), ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Бот {bot.user} готов к работе!")

bot.run(TOKEN)
