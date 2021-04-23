# /usr/bin/python3
# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# Please read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

# Standalone file for facilitating local deploys.

import os

a = r"""
  _    _ _ _             _     _
 | |  | | | |           (_)   | |
 | |  | | | |_ _ __ ___  _  __| |
 | |  | | | __| '__/ _ \| |/ _  |
 | |__| | | |_| | | (_) | | (_| |
  \____/|_|\__|_|  \___/|_|\__,_|
"""


def start():

    clear_screen()
    check_for_py()

    print(f"{a}\n\n")
    print("Bienvenido a SayuOgiwaraBot, ¡comencemos a configurar!\n\n")
    print("Clonando el repositorio...\n\n")
    try:
        os.system("git clone https://github.com/TaprisSugarbell/Ultroid && cd Ultroid")
    except Exception as e:
        print(f"ERROR\n{str(e)}")
    print("\n\nDone")
    os.system("cd Ultroid")
    clear_screen()
    print(a)
    print("\n\nLet's start!\n")

    # generate session if needed.
    sessionisneeded = input(
        "¿Desea generar una nueva sesion o tener el antiguo sesion string? [generate/skip]",
    )
    if sessionisneeded == "generate":
        gen_session()
    elif sessionisneeded == "skip":
        pass
    else:
        print(
            'Por favor, elija " generate " para generar un strin sesion, o " skip " para pasarla.\n\nPor favor, ejecute el script de nuevo.',
        )
        exit(0)

    # start bleck megik
    print("\n\nEmpecemos a introducir las variables.\n\n")
    varrs = [
        "API_ID",
        "API_HASH",
        "SESSION",
        "BOT_USERNAME",
        "BOT_TOKEN",
        "REDIS_URI",
        "REDIS_PASSWORD",
        "LOG_CHANNEL",
    ]
    all_done = "# Variables de Entorno de SayuOgiwaraBot.\n# No borres este archivo.\n\n"
    for i in varrs:
        all_done += do_input(i)
    clear_screen()
    print(a)
    print("\n\nAquí están las cosas que has introducido.\nPor favor, revisa.")
    print(all_done)
    isitdone = input("\n\n¿Está todo correcto? [y/n]")
    if isitdone == "y":
        # https://github.com/TaprisSugarbell/Ultroid/blob/31b9eb1f4f8059e0ae66adb74cb6e8174df12eac/resources/startup/locals.py#L35
        f = open(".env", "w")
        f.write(all_done)
        f.close
    elif isitdone == "n":
        print("Oh, vamos a rehacer estos entonces -_-")
        start()
    else:
        # https://github.com/TaprisSugarbell/Ultroid/blob/31b9eb1f4f8059e0ae66adb74cb6e8174df12eac/resources/startup/locals.py#L35
        f = open(".env", "w")
        f.write(all_done)
        f.close
    clear_screen()
    print("\nFelicidades. ¡Todo está hecho!\n¡Es hora de iniciar el bot!")
    print("\nInstalling requirements... This might take a while...")
    os.system("pip3 install -r ./resources/extras/local-requirements.txt")
    clear_screen()
    print(a)
    print("\nIniciar SayuOgiwaraBot...")
    os.system("python3 -m pyUltroid")


def do_input(var):
    val = input(f"Ingresa tu {var}: ")
    to_write = f"{var}={val}\n"
    return to_write


def clear_screen():
    # clear screen
    if os.name == "posix":
        _ = os.system("clear")
    else:
        # for windows platfrom
        _ = os.system("cls")


def check_for_py():
    print(
        "Por favor, asegúrese de que tiene python instalado. \nConsíguelo en http://python.org/\n\n",
    )
    try:
        ch = int(
            input(
                "Ingrese la opción:\n1. Continúa, python está instalado.\n2. Salir e instalar python.\n",
            ),
        )
    except BaseException:
        print("¡¡Por favor, ejecute el script de nuevo, e introduzca la elección como un número!!")
        exit(0)
    if ch == 1:
        pass
    elif ch == 2:
        print("Por favor, instale python y continúe.")
        exit(0)
    else:
        print("¿No te enseñaron a leer? ¡¡Ingresa una opción!!")
        return


def gen_session():
    print("\nProcesando...")
    # https://github.com/TeamUltroid/Ultroid/blob/31b9eb1f4f8059e0ae66adb74cb6e8174df12eac/resources/startup/locals.py#L35
    os.system("python3 resources/session/ssgen.py")
    return


start()
