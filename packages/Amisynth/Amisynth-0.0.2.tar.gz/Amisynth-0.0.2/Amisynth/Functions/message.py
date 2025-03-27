import xfox

@xfox.addfunc(xfox.funcs)
async def message(num, *args, **kwargs):
    # Filtrar kwargs para ignorar 'ctx_slash_env'
    filtered_kwargs = {k: v for k, v in kwargs.items() if k != "ctx_slash_env"}

    # Obtener el contexto adecuado
    ctx_message_env = kwargs.get("ctx_message_env")
    ctx_command = kwargs.get("ctx_command")

    if ctx_message_env:
        message_content = ctx_message_env.content  # Mensaje del evento
        palabras = message_content.split()  # Obtener palabras
    elif ctx_command:
        message_content = ctx_command.message.content  # Mensaje del comando
        palabras = message_content.split()[1:]  # Excluir el nombre del comando
        

    # Si se proporciona un número, tratarlo como índice de palabras
    if num.isdigit():
        index = int(num) - 1  # Ajuste para empezar en 1
        palabra = palabras[index] if 0 <= index < len(palabras) else ""

        # Si hay argumentos extra, buscar en kwargs si la palabra no existe
        if args:
            for clave in args:
                if clave in filtered_kwargs:
                    return palabra if palabra else filtered_kwargs[clave]
        
        return palabra
    
    # Si num no es número, asumir que es una clave de kwargs
    return filtered_kwargs.get(num, "")
