import os
import csv
import re

# Es el nombre del archivo para la persistencia de datos
ARCHIVO_DB = "inventario_productos.csv"
#Aqui estas las funciones para registrar , añadir y actualizar valores guardado 
def cargar_inventario():
    """Carga los productos desde el archivo CSV al iniciar el programa."""
    inventario = {}
    if not os.path.exists(ARCHIVO_DB):
        return inventario
    try:
        with open(ARCHIVO_DB, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                codigo = row['codigo']
                inventario[codigo] = {
                    'nombre': row['nombre'],
                    'precio': float(row['precio']),
                    'cantidad': int(row['cantidad'])
                }
    except (IOError, ValueError) as e:
        print(f"Error al cargar el archivo de persistencia: {e}")
        print("Se iniciará con un inventario vacío.")
    return inventario

def guardar_inventario(inventario):
    """Guarda el estado actual del inventario en el archivo CSV."""
    try:
        with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['codigo', 'nombre', 'precio', 'cantidad']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for codigo, datos in inventario.items():
                writer.writerow({
                    'codigo': codigo,
                    'nombre': datos['nombre'],
                    'precio': datos['precio'],
                    'cantidad': datos['cantidad']
                })
    except IOError as e:
        print(f"Error crítico: No se pudo guardar la información en el archivo. {e}")

def validar_codigo(codigo, inventario):
    """Valida el formato del código (PROD-XXX) y que no sea duplicado."""
    codigo = codigo.strip().upper()
    if not codigo:
        print("El código del producto no puede estar vacío.")
        return None
    
    # Es el formato requerido: PROD- seguido de un número para registrar su id del producto 
    patron = r"^PROD-\d+$"
    if not re.match(patron, codigo):
        print("Formato de código inválido. Debe usar la estructura 'PROD-001'.")
        return None
        
    if codigo in inventario:
        print(f"El código '{codigo}' ya está registrado para otro producto.")
        return None
        
    return codigo

def registrar_producto(inventario):
    """Permite el registro controlado de un nuevo producto."""
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    
    cod_input = input("Ingrese el código del producto (Ej: PROD-001): ")
    codigo = validar_codigo(cod_input, inventario)
    if not codigo:
        return

    nombre = input("Ingrese el nombre/descripción del producto: ").strip()
    if not nombre:
        print("El nombre del producto no puede estar vacío.")
        return

    try:
        precio = float(input("Ingrese el precio unitario (mayor a 0): "))
        if precio <= 0:
            print("El precio debe ser un número estrictamente mayor que cero.")
            return
            
        cantidad = int(input("Ingrese la cantidad disponible (0 o mayor): "))
        if cantidad < 0:
            print("La cantidad inicial no puede ser negativa.")
            return
            
    except ValueError:
        print("Error de datos: El precio debe ser decimal y la cantidad un número entero.")
        return

    # Inserción segura en el diccionario para evitar errores en el regsitro y mostrar todo lo registrado
    inventario[codigo] = {
        'nombre': nombre,
        'precio': precio,
        'cantidad': cantidad
    }
    guardar_inventario(inventario)
    print(f"Producto '{nombre}' [{codigo}] registrado con éxito.")

def consultar_productos(inventario):
    """Muestra de manera formateada todos los productos en el sistema."""
    print("\n--- CONSULTA DE INVENTARIO GENERAL ---")
    if not inventario:
        print("El inventario se encuentra actualmente vacío.")
        return

    # Cabecera de la tabla en consola o imagen de la consola 
    print(f"{'Código':<12} | {'Nombre / Descripción':<25} | {'Precio (Bs.)':<12} | {'Cantidad':<10}")
    print("-" * 68)
    
    for codigo, d in inventario.items():
        print(f"{codigo:<12} | {d['nombre']:<25} | {d['precio']:<12.2f} | {d['cantidad']:<10}")
    print("-" * 68)

def actualizar_existencias(inventario):
    """Modifica la cantidad disponible de un artículo ya existente."""
    print("\n--- ACTUALIZACIÓN DE EXISTENCIAS (STOCK) ---")
    codigo = input("Ingrese el código del producto a actualizar: ").strip().upper()
    
    if codigo not in inventario:
        print("El producto especificado no existe en el sistema legado.")
        return
        
    producto = inventario[codigo]
    print(f"Producto seleccionado: {producto['nombre']} | Stock actual: {producto['cantidad']}")
    
    try:
        print("Seleccione una operación:")
        print("1. Adicionar stock (+)")
        print("2. Reducir stock (-)")
        op_stock = input("Opción: ").strip()
        
        cantidad_cambio = int(input("Ingrese la cantidad de unidades: "))
        if cantidad_cambio <= 0:
            print("La cantidad del cambio debe ser un número entero mayor a cero.")
            return

        if op_stock == "1":
            producto['cantidad'] += cantidad_cambio
        elif op_stock == "2":
            if producto['cantidad'] - cantidad_cambio < 0:
                print(f"Operación inválida. No se puede reducir a cantidades negativas. Stock disponible: {producto['cantidad']}")
                return
            producto['cantidad'] -= cantidad_cambio
        else:
            print("Opción de operación no válida.")
            return
            
    except ValueError:
        print("Error de datos: La cantidad de stock debe ser exclusivamente un número entero.")
        return

    guardar_inventario(inventario)
    print(f"Stock actualizado correctamente. Nuevo stock de [{codigo}]: {producto['cantidad']} unidades.")

def main():
    """Función principal que gestiona el ciclo del menú de usuario."""
    # Inicialización y recuperación desde persistencia 
    inventario_sistema = cargar_inventario()
    
    while True:
        print("\n========================================")
        print("  SISTEMA DE GESTIÓN COMERCIAL - MENU   ")
        print("========================================")
        print("1. Registrar un nuevo producto")
        print("2. Consultar los productos registrados")
        print("3. Actualizar la cantidad disponible")
        print("4. Salir del programa")
        print("========================================")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            registrar_producto(inventario_sistema)
        elif opcion == "2":
            consultar_productos(inventario_sistema)
        elif opcion == "3":
            actualizar_existencias(inventario_sistema)
        elif opcion == "4":
            print("\nGuardando cambios finales y terminando el programa de manera segura.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo seleccionando un número del 1 al 4.")

if __name__ == "__main__":
    main()