import discord
import re
from discord import app_commands

# Lista global de embeds
embeds = []  # Esta lista se puede actualizar desde otros archivos, como 'image.py' o 'thumbnail.py'

buttons = []  # Si también necesitas manejar botones, puedes añadir la lógica aquí

choices_slash = {}




async def utils():
    nuevos_embeds = []  # Usamos una lista nueva para los embeds procesados

    # Iterar sobre cada item en la lista de embeds

    for item in embeds:
        embed = discord.Embed()  # Crear el embed sin título y descripción por defecto

        if "color" in item and item["color"]:
            embed.color = item["color"]

        # Verificar si el título está presente y agregarlo
        if 'title' in item and item['title']:
            embed.title = item['title']

        if "title_url" in item and item["title_url"]:
            embed.url = ensure_double_slash(item["title_url"] or "")

        # Verificar si la descripción está presente y agregarla
        if 'description' in item and item['description']:
            embed.description = item['description']

        # Verificar si hay imagen y añadirla, asegurando que la URL esté bien formada
        if "image" in item and item["image"]:
            n = ensure_double_slash(item["image"])
            embed.set_image(url=n)

        if "thumbnail_icon" in item and item["thumbnail_icon"]:
            n = ensure_double_slash(item["thumbnail_icon"])
            embed.set_thumbnail(url=n)

        if "footer" in item and item["footer"]:
            icon = item["footer_icon"] if "footer_icon" in item and item["footer_icon"] else None
            embed.set_footer(text=item["footer"], icon_url=icon)
        

        author_name = item.get("author")
        author_icon = ensure_double_slash(item.get("author_icon", ""))
        author_url = ensure_double_slash(item.get("author_url", ""))

        if author_name or author_icon or author_url:
            embed.set_author(name=author_name or "", icon_url=author_icon, url=author_url)
        # Agregar el embed procesado a la lista

        if "fields" in item and isinstance(item["fields"], list):
            for field in item["fields"]:
                embed.add_field(
                    name=field.get("name"),
                    value=field.get("value"),
                    inline=field.get("inline"))


        nuevos_embeds.append(embed)

    # Retornar los nuevos embeds procesados y los botones
    return buttons, nuevos_embeds


def ensure_double_slash(text: str) -> str:
    return re.sub(r"https:(?!//)", "https://", text)



