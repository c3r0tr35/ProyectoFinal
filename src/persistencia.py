import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_INVENTARIO = os.path.join(BASE, "data", "inventario.txt")
RUTA_VENTAS = os.path.join(BASE, "data", "ventas.txt")


def cargar_inventario():
    inventario = {}
    try:
        with open(RUTA_INVENTARIO, "r", encoding="utf-8") as f:
            for numero, linea in enumerate(f, 1):
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    partes = linea.split("|")
                    if len(partes) != 7:
                        raise ValueError
                    codigo, nombre, categoria, precio, stock, minimo, proveedor = partes
                    precio = float(precio)
                    stock = int(stock)
                    minimo = int(minimo)
                    if not codigo or precio <= 0 or stock < 0 or minimo < 0:
                        raise ValueError
                    if codigo in inventario:
                        raise ValueError
                except ValueError:
                    print(f"Advertencia: la linea {numero} de inventario.txt esta corrupta y se omite.")
                    continue
                inventario[codigo] = {
                    "nombre": nombre,
                    "categoria": categoria,
                    "precio": precio,
                    "stock": stock,
                    "stock_minimo": minimo,
                    "proveedor": proveedor,
                }
    except FileNotFoundError:
        print("No se encontro inventario.txt, se inicia con un inventario vacio.")
    return inventario


def guardar_inventario(inventario):
    os.makedirs(os.path.dirname(RUTA_INVENTARIO), exist_ok=True)
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as f:
        for codigo, p in inventario.items():
            f.write(f"{codigo}|{p['nombre']}|{p['categoria']}|{p['precio']}|{p['stock']}|{p['stock_minimo']}|{p['proveedor']}\n")


def registrar_venta(fecha, total, carrito):
    os.makedirs(os.path.dirname(RUTA_VENTAS), exist_ok=True)
    detalle = ";".join(f"{codigo}:{cantidad}" for codigo, cantidad in carrito.items())
    with open(RUTA_VENTAS, "a", encoding="utf-8") as f:
        f.write(f"{fecha}|{total}|{detalle}\n")


def cargar_ventas():
    ventas = []
    try:
        with open(RUTA_VENTAS, "r", encoding="utf-8") as f:
            for numero, linea in enumerate(f, 1):
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    fecha, total, detalle = linea.split("|")
                    items = {}
                    for par in detalle.split(";"):
                        codigo, cantidad = par.split(":")
                        items[codigo] = int(cantidad)
                    ventas.append({"fecha": fecha, "total": float(total), "items": items})
                except ValueError:
                    print(f"Advertencia: la linea {numero} de ventas.txt esta corrupta y se omite.")
    except FileNotFoundError:
        pass
    return ventas
