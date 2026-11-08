import datetime
from tabulate import tabulate

import validaciones as val
import persistencia as per
import inventario as inv
import ventas as ven
import reportes as rep


####
def menu_inventario(inventario):
    while True:
        print("\n   Gestion de inventario   ")
        print("1. Registrar producto")
        print("2. Consultar por codigo")
        print("3. Consultar por categoria")
        print("4. Modificar precio y stock")
        print("5. Eliminar producto")
        print("6. Listar todo")
        print("0. Volver")
        opcion = val.pedir_opcion("Opcion: ", ["0", "1", "2", "3", "4", "5", "6"])

        if opcion == "0":
            return

        elif opcion == "1":
            codigo = val.pedir_texto("Codigo: ").upper()
            if codigo in inventario:
                print(f"Error: el codigo {codigo} ya existe.")
                continue
            nombre = val.pedir_texto("Nombre: ")
            categoria = val.pedir_de_lista("Categoria:", inv.CATEGORIAS)
            precio = val.pedir_float("Precio: ")
            stock = val.pedir_entero("Stock: ")
            minimo = val.pedir_entero("Stock minimo: ")
            proveedor = val.pedir_texto("Proveedor: ")
            try:
                inv.registrar_producto(inventario, codigo, nombre, categoria, precio, stock, minimo, proveedor)
                print("Producto registrado.")
            except ValueError as e:
                print("Error:", e)

        elif opcion == "2":
            codigo = val.pedir_texto("Codigo: ").upper()
            producto = inv.buscar_por_codigo(inventario, codigo)
            if producto is None:
                print("No existe un producto con ese codigo.")
            else:
                inv.mostrar_productos({codigo: producto})

        elif opcion == "3":
            categoria = val.pedir_de_lista("Categoria:", inv.CATEGORIAS)
            encontrados = inv.buscar_por_categoria(inventario, categoria)
            if not encontrados:
                print("No hay productos en esa categoria.")
            else:
                inv.mostrar_productos(encontrados)

        elif opcion == "4":
            codigo = val.pedir_texto("Codigo: ").upper()
            if codigo not in inventario:
                print("No existe un producto con ese codigo.")
                continue
            precio = val.pedir_float("Nuevo precio: ")
            stock = val.pedir_entero("Nuevo stock: ")
            try:
                inv.modificar_producto(inventario, codigo, precio, stock)
                print("Producto modificado.")
            except ValueError as e:
                print("Error:", e)

        elif opcion == "5":
            codigo = val.pedir_texto("Codigo: ").upper()
            if codigo not in inventario:
                print("No existe un producto con ese codigo.")
                continue
            if val.pedir_si_no(f"Eliminar {inventario[codigo]['nombre']}? (s/n): "):
                try:
                    inv.eliminar_producto(inventario, codigo)
                    print("Producto eliminado.")
                except ValueError as e:
                    print("Error:", e)

        elif opcion == "6":
            if not inventario:
                print("El inventario esta vacio.")
            else:
                inv.mostrar_productos(inventario)


####
def mostrar_carrito(inventario, carrito):
    filas = []
    for codigo, cantidad in carrito.items():
        p = inventario[codigo]
        filas.append([p["nombre"], cantidad, f"${p['precio'] * cantidad:,.0f}"])
    print(tabulate(filas, headers=["Producto", "Cantidad", "Valor"], tablefmt="grid"))


def nueva_venta(inventario):
    if not inventario:
        print("No hay productos en el inventario.")
        return

    carrito = {}
    print("\n   Nueva venta   (deje el codigo vacio para terminar)")
    while True:
        codigo = input("Codigo: ").strip().upper()
        if codigo == "":
            break
        if codigo not in inventario:
            print("No existe un producto con ese codigo.")
            continue
        print(f"{inventario[codigo]['nombre']} - ${inventario[codigo]['precio']:,.0f} - disponibles: {inventario[codigo]['stock']}")
        cantidad = val.pedir_entero("Cantidad: ")
        try:
            ven.agregar_al_carrito(inventario, carrito, codigo, cantidad)
        except ValueError as e:
            print("Error:", e)

    if not carrito:
        print("Venta cancelada, el carrito esta vacio.")
        return

    subtotal = ven.calcular_subtotal(inventario, carrito)
    descuento = ven.calcular_descuento(subtotal)
    total = subtotal - descuento

    print()
    mostrar_carrito(inventario, carrito)
    print(f"Subtotal:  ${subtotal:,.0f}")
    print(f"Descuento: ${descuento:,.0f}")
    print(f"Total:     ${total:,.0f}")

    if not val.pedir_si_no("Confirmar venta? (s/n): "):
        print("Venta cancelada.")
        return

    while True:
        pago = val.pedir_float("Pago recibido: ")
        try:
            cambio = ven.calcular_cambio(total, pago)
            break
        except ValueError as e:
            print("Error:", e)
            if not val.pedir_si_no("Reintentar? (s/n): "):
                print("Venta cancelada.")
                return

    try:
        ven.confirmar_venta(inventario, carrito)
    except ValueError as e:
        print("Error:", e)
        return

    fecha = str(datetime.date.today())
    per.registrar_venta(fecha, total, carrito)
    per.guardar_inventario(inventario)
    print(f"Venta registrada. Cambio: ${cambio:,.0f}")


####
def mostrar_alertas(inventario):
    por_proveedor = rep.alertas_stock(inventario)
    print("\n   Alertas de stock   ")
    if not por_proveedor:
        print("No hay productos por reabastecer.")
        return
    for proveedor, filas in por_proveedor.items():
        print(f"\nProveedor: {proveedor}")
        print(tabulate(filas, headers=["Codigo", "Producto", "Stock", "Minimo", "Estado"], tablefmt="grid"))


def mostrar_cierre(inventario):
    fecha = str(datetime.date.today())
    ventas = per.cargar_ventas()
    r = rep.cierre_dia(inventario, ventas, fecha)

    print(f"\n   Cierre del dia {fecha}   ")
    if r["ventas"] == 0:
        print("Hoy no se han registrado ventas.")
    else:
        print(f"Total vendido: ${r['total']:,.0f}")
        print(f"Numero de ventas: {r['ventas']}")
        print(f"Ticket promedio: ${r['promedio']:,.0f}")
        print(f"Producto mas vendido: {r['mas_vendido'][0]} ({r['mas_vendido'][1]} unidades)")
        print(f"Categorias con movimiento: {', '.join(r['categorias'])}")
    if r["sin_ventas"]:
        print("Productos sin ventas:")
        for nombre in r["sin_ventas"]:
            print(f"- {nombre}")
    else:
        print("Todos los productos tuvieron ventas.")


def menu_reportes(inventario):
    while True:
        print("\n   Reportes   ")
        print("1. Alertas de stock")
        print("2. Cierre del dia")
        print("0. Volver")
        opcion = val.pedir_opcion("Opcion: ", ["0", "1", "2"])
        if opcion == "0":
            return
        elif opcion == "1":
            mostrar_alertas(inventario)
        elif opcion == "2":
            mostrar_cierre(inventario)


####
def main():
    inventario = per.cargar_inventario()
    print(f"Inventario cargado: {len(inventario)} productos.")

    while True:
        print("\n   TiendaPy - Don Aurelio   ")
        print("1. Inventario")
        print("2. Nueva venta")
        print("3. Reportes")
        print("4. Guardar inventario")
        print("0. Salir")
        opcion = val.pedir_opcion("Opcion: ", ["0", "1", "2", "3", "4"])

        if opcion == "1":
            menu_inventario(inventario)
        elif opcion == "2":
            nueva_venta(inventario)
        elif opcion == "3":
            menu_reportes(inventario)
        elif opcion == "4":
            per.guardar_inventario(inventario)
            print("Inventario guardado.")
        elif opcion == "0":
            per.guardar_inventario(inventario)
            print("Inventario guardado. Hasta luego.")
            break


if __name__ == "__main__":
    main()
