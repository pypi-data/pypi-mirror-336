import xfox
from Amisynth.utils import embeds  # Asegúrate de que 'embeds' sea la lista global que deseas modificar

@xfox.addfunc(xfox.funcs)
async def thumbnail(url: str, indice: int = 1, *args, **kwargs):
    """
    Guarda un thumbnail en la lista de embeds, con una URL de imagen específica y un índice opcional.
    Si se especifica el índice, se inserta o actualiza en esa posición. Si no, se agrega en la posición 1.
    """
    embed = {
        "thumbnail_icon": url,  # URL de la imagen como thumbnail
        "index": indice    # Añadir el índice para identificar la posición
    }

    # Buscar si ya existe un embed con ese índice y actualizar solo el thumbnail
    found = False
    for i, item in enumerate(embeds):
        if item.get("index") == indice:
            # Mantener los otros atributos del embed y solo actualizar el thumbnail
            embeds[i]["thumbnail_icon"] = url
            found = True
            break
    if not found:
        # Si no se encontró, agregar uno nuevo
        embeds.append(embed)

    return ""
