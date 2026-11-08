def alertas_stock(inventario):
    por_proveedor = {}
    for codigo, p in inventario.items():
        if p["stock"] <= p["stock_minimo"]:
            estado = "AGOTADO" if p["stock"] == 0 else "Stock bajo"
            fila = [codigo, p["nombre"], p["stock"], p["stock_minimo"], estado]
            por_proveedor.setdefault(p["proveedor"], []).append(fila)
    return por_proveedor


def cierre_dia(inventario, ventas, fecha):
    ventas_dia = [v for v in ventas if v["fecha"] == fecha]
    total = sum(v["total"] for v in ventas_dia)
    cantidad = len(ventas_dia)
    promedio = total / cantidad if cantidad > 0 else 0.0

    unidades = {}
    for v in ventas_dia:
        for codigo, cant in v["items"].items():
            unidades[codigo] = unidades.get(codigo, 0) + cant

    mas_vendido = None
    if unidades:
        codigo_top = max(unidades, key=unidades.get)
        nombre = inventario[codigo_top]["nombre"] if codigo_top in inventario else codigo_top
        mas_vendido = (nombre, unidades[codigo_top])

    sin_ventas = [p["nombre"] for c, p in inventario.items() if c not in unidades]
    categorias = sorted({inventario[c]["categoria"] for c in unidades if c in inventario})

    return {
        "total": total,
        "ventas": cantidad,
        "promedio": promedio,
        "mas_vendido": mas_vendido,
        "sin_ventas": sin_ventas,
        "categorias": categorias,
    }
