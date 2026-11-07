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
