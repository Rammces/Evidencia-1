import random as rd
import sys
import datetime
import sqlite3
from sqlite3 import Error
from datetime import datetime
import openpyxl

# Crear tablas para AFIs
def crear_tablas_afi():
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Estudiantes (matricula INTEGER PRIMARY KEY, nombre TEXT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS CategoriasAFI (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, descripcion TEXT);")
            cursor.execute("CREATE TABLE IF NOT EXISTS ActividadesAFI (folio INTEGER PRIMARY KEY, matricula INTEGER, actividad TEXT NOT NULL, categoria TEXT NOT NULL, fecha TIMESTAMP);")
            print("Tablas creadas exitosamente.")
    except Error as e:
        print(e)

crear_tablas_afi()

# Registrar nueva AFI
def registrar_afi():
    while True:
        matricula = int(input("Ingresa tu matrícula: "))
        try:
            with sqlite3.connect("AFI.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Estudiantes WHERE matricula = ?", (matricula,))
                estudiante = cursor.fetchone()
                if estudiante:
                    print(f"Estudiante encontrado: {estudiante[1]}")
                else:
                    print("No se encontró estudiante con esa matrícula.")
                    continue
        except Exception as e:
            print(f"Error: {e}")
            continue

        actividad = input("Nombre de la actividad AFI (Escribe SALIR para regresar): ")
        if actividad.upper() == "SALIR":
            return

        categoria = input("Categoría de la actividad (Deportiva, Cultural, Académica, etc.): ")
        fecha_ingresada = input("Fecha de realización (dd/mm/aaaa): ")

        try:
            fecha_dt = datetime.strptime(fecha_ingresada, "%d/%m/%Y")
        except ValueError:
            print("Formato de fecha incorrecto.")
            continue

        folio = rd.randint(1000, 9999)
        try:
            with sqlite3.connect("AFI.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ActividadesAFI VALUES (?, ?, ?, ?, ?)", (folio, matricula, actividad, categoria, fecha_dt))
                conn.commit()
                print("AFI registrada exitosamente.")
        except Exception as e:
            print(f"Error al registrar: {e}")

# Modificar actividad AFI
def modificar_afi():
    nombre_actividad = input("Nombre de la actividad que deseas modificar: ")
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ActividadesAFI WHERE actividad = ?", (nombre_actividad,))
            registro = cursor.fetchone()
            if registro:
                print(f"Folio: {registro[0]}, Actividad: {registro[2]}, Categoría: {registro[3]}, Fecha: {registro[4]}")
            else:
                print("No se encontró la actividad.")
                return
    except Exception as e:
        print(f"Error: {e}")
        return

    nuevo_nombre = input("Nuevo nombre para la actividad: ")
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE ActividadesAFI SET actividad = ? WHERE folio = ?", (nuevo_nombre, registro[0]))
            conn.commit()
            print("Actividad modificada exitosamente.")
    except Exception as e:
        print(f"Error al modificar: {e}")

# Consultar si una fecha tiene AFIs registradas
def consultar_fecha_afi():
    fecha = input("Fecha a consultar (dd/mm/aaaa): ")
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha incorrecto.")
        return

    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ActividadesAFI WHERE fecha = ?", (fecha_dt,))
            registros = cursor.fetchall()
            if registros:
                print(f"Ya hay actividades registradas en {fecha_dt.strftime('%d/%m/%Y')}.")
            else:
                print("La fecha está libre para registrar una AFI.")
    except Exception as e:
        print(f"Error: {e}")

# Reporte de AFIs por fecha
def reporte_afi_por_fecha():
    fecha = input("Fecha a consultar (dd/mm/aaaa): ")
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha incorrecto.")
        return

    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ActividadesAFI WHERE fecha = ?", (fecha_dt,))
            registros = cursor.fetchall()
            if registros:
                print(f"Actividades registradas en {fecha_dt.strftime('%d/%m/%Y')}:")
                for r in registros:
                    print(f"Folio: {r[0]}, Matrícula: {r[1]}, Actividad: {r[2]}, Categoría: {r[3]}")
            else:
                print("No hay actividades registradas en esa fecha.")
    except Exception as e:
        print(f"Error: {e}")

# Registrar nueva categoría de AFI
def registrar_categoria_afi():
    nombre = input("Nombre de la categoría: ")
    descripcion = input("Descripción breve: ")
    id_cat = rd.randint(100, 999)
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CategoriasAFI VALUES (?, ?, ?)", (id_cat, nombre, descripcion))
            conn.commit()
            print("Categoría registrada exitosamente.")
    except Exception as e:
        print(f"Error: {e}")

# Registrar estudiante
def registrar_estudiante():
    nombre = input("Nombre del estudiante: ")
    matricula = rd.randint(100000, 999999)
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Estudiantes VALUES (?, ?)", (matricula, nombre))
            conn.commit()
            print(f"Estudiante registrado con matrícula: {matricula}")
    except Exception as e:
        print(f"Error: {e}")

# Eliminar actividad AFI
def eliminar_afi():
    folio = int(input("Folio de la actividad a eliminar: "))
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ActividadesAFI WHERE folio = ?", (folio,))
            conn.commit()
            print("Actividad eliminada exitosamente.")
    except Exception as e:
        print(f"Error: {e}")

# Exportar AFIs a Excel
def exportar_afi_excel():
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ActividadesAFI")
            actividades = cursor.fetchall()

        workbook = openpyxl.Workbook()
        hoja = workbook.active
        hoja.title = "AFIs"

        hoja.append(['Folio', 'Matrícula', 'Actividad', 'Categoría', 'Fecha'])
        for act in actividades:
            hoja.append(act)

        workbook.save("Reporte_AFIs.xlsx")
        print("Datos exportados exitosamente a 'Reporte_AFIs.xlsx'")
    except Exception as e:
        print(f"Error: {e}")

# Menú principal
def menu():
    while True:
        print("\n--- MENÚ DE ACTIVIDADES DE FORMACIÓN INTEGRAL ---")
        print("1. Registrar nueva AFI")
        print("2. Modificar actividad AFI")
        print("3. Consultar disponibilidad por fecha")
        print("4. Reporte de AFIs por fecha")
        print("5. Registrar categoría de AFI")
        print("6. Registrar estudiante")
        print("7. Eliminar actividad AFI")
        print("8. Exportar AFIs a Excel")
        print("9. Salir")
        try:
            opcion = int(input("Selecciona una opción (1-9): "))
            if opcion == 1:
                registrar_afi()
            elif opcion == 2:
                modificar_afi()
            elif opcion == 3:
                consultar_fecha_afi()
            elif opcion == 4:
                reporte_afi_por_fecha()
            elif opcion == 5:
                registrar_categoria_afi()
            elif opcion == 6:
                registrar_estudiante()
            elif opcion == 7:
                eliminar_afi()
            elif opcion == 8:
                exportar_afi_excel()
            elif opcion == 9:
                print("Saliendo del programa...")
                sys.exit()
            else:
                print("Opción inválida.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entre 1 y 10.")


def mostrar_tablas():
    try:
        with sqlite3.connect("AFI.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()
            print("\nTablas en la base de datos:")
            for tabla in tablas:
                print(f"- {tabla[0]}")
    except Exception as e:
        print(f"Error al mostrar tablas: {e}")

menu()