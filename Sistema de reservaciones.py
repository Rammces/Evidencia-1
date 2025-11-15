import sqlite3
import pandas as pd
from datetime import datetime

# Conexión a la base de datos
conn = sqlite3.connect("reservaciones.db")
cursor = conn.cursor()

# Crear tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Salas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    capacidad INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Reservaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_sala INTEGER,
    fecha TEXT,
    hora TEXT,
    FOREIGN KEY(id_cliente) REFERENCES Clientes(id),
    FOREIGN KEY(id_sala) REFERENCES Salas(id)
)
""")

conn.commit()

# Funciones del sistema
def registrar_sala():
    nombre = input("Nombre de la sala: ")
    capacidad = int(input("Capacidad de la sala: "))
    cursor.execute("INSERT INTO Salas (nombre, capacidad) VALUES (?, ?)", (nombre, capacidad))
    conn.commit()
    print("Sala registrada correctamente.")

def registrar_cliente():
    nombre = input("Nombre del cliente: ")
    correo = input("Correo del cliente: ")
    cursor.execute("INSERT INTO Clientes (nombre, correo) VALUES (?, ?)", (nombre, correo))
    conn.commit()
    print("Cliente registrado correctamente.")

def registrar_reservacion():
    id_cliente = int(input("ID del cliente: "))
    id_sala = int(input("ID de la sala: "))
    fecha = input("Fecha de la reservación (YYYY-MM-DD): ")
    hora = input("Hora de la reservación (HH:MM): ")
    
    # Verificar si la sala ya está ocupada
    cursor.execute("""
    SELECT * FROM Reservaciones 
    WHERE id_sala=? AND fecha=? AND hora=?
    """, (id_sala, fecha, hora))
    if cursor.fetchone():
        print("La sala ya está reservada en esa fecha y hora.")
        return
    
    cursor.execute("INSERT INTO Reservaciones (id_cliente, id_sala, fecha, hora) VALUES (?, ?, ?, ?)",
                   (id_cliente, id_sala, fecha, hora))
    conn.commit()
    print("Reservación registrada correctamente.")

def modificar_reservacion():
    id_reserva = int(input("ID de la reservación a modificar: "))
    fecha = input("Nueva fecha (YYYY-MM-DD): ")
    hora = input("Nueva hora (HH:MM): ")
    cursor.execute("UPDATE Reservaciones SET fecha=?, hora=? WHERE id=?", (fecha, hora, id_reserva))
    conn.commit()
    print("Reservación modificada correctamente.")

def consultar_fecha_disponible():
    fecha = input("Ingrese la fecha a consultar (YYYY-MM-DD): ")
    cursor.execute("""
    SELECT s.nombre, r.hora FROM Reservaciones r
    JOIN Salas s ON r.id_sala = s.id
    WHERE r.fecha=?
    """, (fecha,))
    reservas = cursor.fetchall()
    if reservas:
        print("Reservas en esa fecha:")
        for sala, hora in reservas:
            print(f"Sala: {sala} - Hora: {hora}")
    else:
        print("No hay reservaciones en esa fecha.")

def reporte_por_fecha():
    fecha = input("Ingrese la fecha del reporte (YYYY-MM-DD): ")
    cursor.execute("""
    SELECT r.id, c.nombre, s.nombre, r.fecha, r.hora 
    FROM Reservaciones r
    JOIN Clientes c ON r.id_cliente = c.id
    JOIN Salas s ON r.id_sala = s.id
    WHERE r.fecha=?
    """, (fecha,))
    reservas = cursor.fetchall()
    if reservas:
        df = pd.DataFrame(reservas, columns=["ID", "Cliente", "Sala", "Fecha", "Hora"])
        print(df)
        return df
    else:
        print("No hay reservaciones en esa fecha.")
        return pd.DataFrame()

def eliminar_reservacion():
    id_reserva = int(input("ID de la reservación a eliminar: "))
    cursor.execute("DELETE FROM Reservaciones WHERE id=?", (id_reserva,))
    conn.commit()
    print("Reservación eliminada.")

def exportar_excel(df):
    if df.empty:
        print("No hay datos para exportar.")
        return
    archivo = f"reservaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(archivo, index=False)
    print(f"Datos exportados a Excel en el archivo {archivo}.")

# Menú principal
def menu():
    while True:
        print("\n--- Sistema de Reservaciones ---")
        print("1. Registrar sala")
        print("2. Registrar cliente")
        print("3. Registrar reservación")
        print("4. Modificar reservación")
        print("5. Consultar fecha disponible")
        print("6. Reporte de reservaciones por fecha")
        print("7. Eliminar reservación")
        print("8. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_sala()
        elif opcion == "2":
            registrar_cliente()
        elif opcion == "3":
            registrar_reservacion()
        elif opcion == "4":
            modificar_reservacion()
        elif opcion == "5":
            consultar_fecha_disponible()
        elif opcion == "6":
            df = reporte_por_fecha()
            exportar_excel(df)
        elif opcion == "7":
            eliminar_reservacion()
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
    conn.close()