# TiendaPy

Aplicacion de consola en Python para controlar el inventario y las ventas de la tienda Don Aurelio.

## Funciones

- Gestion de inventario: registrar, consultar, modificar y eliminar productos
- Ventas con carrito, descuentos (5 % desde $50.000, 10 % desde $100.000) y cambio
- Alertas de stock agrupadas por proveedor
- Cierre del dia
- Persistencia en archivos de texto plano

## Instalacion

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```
python src/main.py
```

## Estructura

```
tiendapy/
|-- data/
|   |-- inventario.txt
|   `-- ventas.txt
`-- src/
    |-- main.py
    |-- inventario.py
    |-- ventas.py
    |-- reportes.py
    |-- persistencia.py
    `-- validaciones.py
```

## Formato de los archivos

inventario.txt: `codigo|nombre|categoria|precio|stock|stock_minimo|proveedor`

ventas.txt: `fecha|total|codigo:cantidad;codigo:cantidad`

## Decisiones de diseño

- Los productos son diccionarios y el inventario es un diccionario por codigo.
- Las reglas de negocio lanzan `ValueError` con `raise` y se capturan en `main.py`.
- Se usa `tabulate` para mostrar las tablas.
