def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El campo no puede estar vacio.")


def pedir_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Debe ingresar un numero entero.")
            continue
        if valor <= 0:
            print("El valor debe ser mayor que cero.")
            continue
        return valor


def pedir_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("Debe ingresar un numero valido.")
            continue
        if valor <= 0:
            print("El valor debe ser mayor que cero.")
            continue
        return valor


def pedir_opcion(mensaje, opciones):
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print("Opcion no valida.")


def pedir_de_lista(titulo, lista):
    print(titulo)
    for i, elemento in enumerate(lista, 1):
        print(f"  {i}. {elemento}")
    while True:
        try:
            numero = int(input("Elija una opcion: "))
        except ValueError:
            print("Debe ingresar un numero.")
            continue
        if 1 <= numero <= len(lista):
            return lista[numero - 1]
        print("Opcion fuera de rango.")


def pedir_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Responda s o n.")
