def calcular_descuento(subtotal):
    if subtotal >= 100000:
        return subtotal * 0.10
    if subtotal >= 50000:
        return subtotal * 0.05
    return 0.0


def agregar_al_carrito(inventario, carrito, codigo, cantidad):
    if codigo not in inventario:
        raise ValueError(f"El codigo {codigo} no existe.")
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")
    nueva_cantidad = carrito.get(codigo, 0) + cantidad
    disponible = inventario[codigo]["stock"]
    if nueva_cantidad > disponible:
        raise ValueError(f"Stock insuficiente. Disponible: {disponible}.")
    carrito[codigo] = nueva_cantidad


def calcular_subtotal(inventario, carrito):
    return sum(inventario[codigo]["precio"] * cantidad for codigo, cantidad in carrito.items())


def calcular_cambio(total, pago):
    if pago < total:
        raise ValueError(f"El pago es insuficiente. Faltan ${total - pago:,.0f}.")
    return pago - total


def confirmar_venta(inventario, carrito):
    for codigo, cantidad in carrito.items():
        if codigo not in inventario or cantidad > inventario[codigo]["stock"]:
            raise ValueError(f"No hay stock suficiente de {codigo}.")
    for codigo, cantidad in carrito.items():
        inventario[codigo]["stock"] -= cantidad
