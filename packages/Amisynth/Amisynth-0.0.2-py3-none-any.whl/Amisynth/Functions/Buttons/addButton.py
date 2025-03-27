import xfox
import discord
from Amisynth.utils import buttons

@xfox.addfunc(xfox.funcs)
async def addButton(new_row: str, button_id: str, label: str, style: str, *args, **kwargs):
    """Crea múltiples botones interactivos y devuelve una lista de objetos de botones creados."""
    
    # Estilos disponibles
    estilos = {
        "Primary": discord.ButtonStyle.primary,
        "Secondary": discord.ButtonStyle.secondary,
        "Success": discord.ButtonStyle.success,
        "Danger": discord.ButtonStyle.danger,
        "Link": discord.ButtonStyle.link
    }
    
    
    # Manejar múltiples botones
    for i in range(0, len(args), 3):  # Se asume que cada botón tiene 3 argumentos adicionales
        button_args = args[i:i+3]
        disabled = button_args[0].lower() == "true" if len(button_args) > 0 else False
        emoji = button_args[1] if len(button_args) > 1 else None
        message_id = button_args[2] if len(button_args) > 2 else None
        
        button_style = estilos.get(style, discord.ButtonStyle.primary)
        
        button = discord.ui.Button(
            label=label,
            custom_id=button_id if button_style != discord.ButtonStyle.link else None,
            style=button_style,
            emoji=emoji,
            disabled=disabled,
            url=button_id if button_style == discord.ButtonStyle.link else None
        )
        
        buttons.append(button)
    
    return ""
