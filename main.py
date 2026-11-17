
# main.py

import discord
from discord.ext import commands
from discord import app_commands

import config


# --------------------------------------------------
# BOT AYARLARI
# --------------------------------------------------

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# --------------------------------------------------
# DERS PROGRAMI EMBED TASARIMI
# --------------------------------------------------

def create_schedule_embed():

    embed = discord.Embed(
        title="📚 Haftalık Ders Programı",
        description=(
            f"**{config.SCHOOL_NAME}**\n\n"
            "Aşağıda haftalık ders programını "
            "görüntüleyebilirsin.\n"
            "Ders saatlerini takip etmeyi unutma! 🚀"
        ),
        color=discord.Color.from_rgb(190, 255, 90)
    )

    for day, lessons in config.WEEKLY_SCHEDULE.items():

        lesson_text = "\n".join(
            f"• {lesson}" for lesson in lessons
        )

        # Discord alan sınırını aşmamak için kontrol.
        if len(lesson_text) > 1024:
            lesson_text = lesson_text[:1010] + "\n..."

        embed.add_field(
            name=f"📅 {day}",
            value=lesson_text or "Ders bulunmuyor.",
            inline=False
        )

    embed.set_footer(
        text="Online Eğitim Akademisi | İyi dersler!"
    )

    return embed


# --------------------------------------------------
# ÖĞRENCİ DERS PROGRAMI BUTONU
# --------------------------------------------------

class ScheduleView(discord.ui.View):

    def __init__(self):

        # timeout=None sayesinde buton kalıcı olur.
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Ders Programımı Görüntüle",
        emoji="📚",
        style=discord.ButtonStyle.success,
        custom_id="school_schedule_button"
    )
    async def schedule_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = create_schedule_embed()

        # Program sadece butona tıklayan öğrenciye gönderilir.
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


# --------------------------------------------------
# BOT BAŞLATILIRKEN ÇALIŞACAK İŞLEMLER
# --------------------------------------------------

class SchoolBot(commands.Bot):

    async def setup_hook(self):

        # Kalıcı buton kaydı.
        self.add_view(ScheduleView())

        # Slash komutlarını Discord'a kaydet.
        await self.tree.sync()

        print("Slash komutları senkronize edildi.")


bot = SchoolBot(
    command_prefix="!",
    intents=intents
)


# --------------------------------------------------
# BOT DURUMU
# --------------------------------------------------

@bot.event
async def on_ready():

    print("--------------------------------")
    print(f"Bot aktif: {bot.user}")
    print(f"Sunucu sayısı: {len(bot.guilds)}")
    print("--------------------------------")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Öğrencilerin ders programını 📚"
        )
    )


# --------------------------------------------------
# YÖNETİCİ KOMUTU: PROGRAM PANELİ
# --------------------------------------------------

@bot.tree.command(
    name="program_paneli",
    description="Öğrenciler için ders programı paneli oluşturur."
)
@app_commands.checks.has_permissions(administrator=True)
async def program_paneli(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎓 Okul Ders Programı",
        description=(
            "Merhaba sevgili öğrenciler! 👋\n\n"
            "Haftalık ders programınıza ulaşmak için "
            "aşağıdaki butona tıklayabilirsiniz.\n\n"
            "📚 **Ders Programımı Görüntüle**\n\n"
            "Derslerinizi takip edin ve eğitim "
            "sürecinizi aksatmayın!\n\n"
            "✨ Hepinize başarılı bir eğitim dönemi dileriz."
        ),
        color=discord.Color.from_rgb(190, 255, 90)
    )

    embed.set_footer(
        text=config.SCHOOL_NAME
    )

    await interaction.response.send_message(
        content="✅ Ders programı paneli oluşturuldu!",
        ephemeral=True
    )

    await interaction.channel.send(
        embed=embed,
        view=ScheduleView()
    )


# --------------------------------------------------
# YETKİ HATA YÖNETİMİ
# --------------------------------------------------

@program_paneli.error
async def program_paneli_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    if isinstance(
        error,
        app_commands.errors.MissingPermissions
    ):

        message = (
            "⛔ Bu komutu kullanabilmek için "
            "yönetici yetkisine sahip olmalısın."
        )

    else:

        message = (
            "❌ Bir hata oluştu. "
            "Lütfen daha sonra tekrar dene."
        )

        print(f"Komut hatası: {error}")

    if interaction.response.is_done():

        await interaction.followup.send(
            message,
            ephemeral=True
        )

    else:

        await interaction.response.send_message(
            message,
            ephemeral=True
        )


# --------------------------------------------------
# BOTU BAŞLAT
# --------------------------------------------------

if __name__ == "__main__":

    if (
        not config.TOKEN
        or config.TOKEN == "BURAYA_DISCORD_BOT_TOKENINI_YAZ"
    ):

        raise ValueError(
            "config.py dosyasına Discord bot tokenini eklemelisin!"
        )

    bot.run(config.TOKEN)
