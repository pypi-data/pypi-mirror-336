import os
import importlib.util

def load_functions():
    folder = "Amisynth/Functions"
    # Usamos os.walk() para recorrer todos los subdirectorios
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(".py"):
                # Obtenemos el nombre del módulo sin `.py`
                module_name = filename[:-3]
                # Obtenemos la ruta completa del archivo
                module_path = os.path.join(root, filename)

                # Cargamos y ejecutamos el módulo
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
