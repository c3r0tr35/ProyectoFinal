import validaciones as val
import persistencia as per
import inventario as inv


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
def main():
    inventario = per.cargar_inventario()
    print(f"Inventario cargado: {len(inventario)} productos.")

    while True:
        print("\n   TiendaPy - Don Aurelio   ")
        print("1. Inventario")
        print("4. Guardar inventario")
        print("0. Salir")
        opcion = val.pedir_opcion("Opcion: ", ["0", "1", "4"])

        if opcion == "1":
            menu_inventario(inventario)
        elif opcion == "4":
            per.guardar_inventario(inventario)
            print("Inventario guardado.")
        elif opcion == "0":
            per.guardar_inventario(inventario)
            print("Inventario guardado. Hasta luego.")
            break


if __name__ == "__main__":
    main()
