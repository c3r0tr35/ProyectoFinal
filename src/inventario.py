from tabulate import tabulate

CATEGORIAS = ["Lacteos", "Bebidas", "Aseo", "Abarrotes", "Snacks"]


def registrar_producto(inventario, codigo, nombre, categoria, precio, stock, stock_minimo, proveedor):
    if codigo in inventario:
        raise ValueError(f"El codigo {codigo} ya existe.")
    if precio <= 0 or stock <= 0 or stock_minimo <= 0:
        raise ValueError("Precio, stock y stock minimo deben ser mayores que cero.")
    inventario[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "proveedor": proveedor,
    }


def buscar_por_codigo(inventario, codigo):
    return inventario.get(codigo)


def buscar_por_categoria(inventario, categoria):
    return {c: p for c, p in inventario.items() if p["categoria"] == categoria}


def modificar_producto(inventario, codigo, precio, stock):
    if codigo not in inventario:
        raise ValueError(f"El codigo {codigo} no existe.")
    if precio <= 0 or stock <= 0:
        raise ValueError("Precio y stock deben ser mayores que cero.")
    inventario[codigo]["precio"] = precio
    inventario[codigo]["stock"] = stock


def eliminar_producto(inventario, codigo):
    if codigo not in inventario:
        raise ValueError(f"El codigo {codigo} no existe.")
    del inventario[codigo]


def mostrar_productos(productos):
    filas = []
    for codigo, p in productos.items():
        filas.append([
            codigo,
            p["nombre"],
            p["categoria"],
            f"${p['precio']:,.0f}",
            p["stock"],
            p["stock_minimo"],
            p["proveedor"],
        ])
    encabezados = ["Codigo", "Nombre", "Categoria", "Precio", "Stock", "Minimo", "Proveedor"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))
