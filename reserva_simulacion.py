import psycopg2
import threading
import time
import csv
import os
from datetime import datetime

# Configuración de conexión (debes ingresar tus datos)
DB_CONFIG = {
    'dbname': 'eventos',
    'user': '',
    'password': '',  
    'host': 'localhost',
    'port': '5432'
}

# Niveles de aislamiento disponibles
NIVELES = {
    'read_committed': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    'repeatable_read': psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
    'serializable': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
}

def exportar_eventos_a_csv(nombre_archivo='eventos.csv'):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Consultar los eventos
        cur.execute("SELECT * FROM eventos;")
        eventos = cur.fetchall()
        
        # Obtener los nombres de las columnas
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='eventos';")
        columnas = [col[0] for col in cur.fetchall()]
        
        # Escribir a CSV
        with open(nombre_archivo, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(columnas)  # Escribir encabezados
            writer.writerows(eventos)  # Escribir datos
        
        print(f"Datos de eventos exportados a {nombre_archivo}")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al exportar eventos: {e}")
        return False

def intentar_reservar(id_asiento, usuario, nivel_aislamiento):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(nivel_aislamiento)
        cur = conn.cursor()
        cur.execute("BEGIN;")

        cur.execute("SELECT disponible FROM asientos WHERE id_asiento = %s FOR UPDATE;", (id_asiento,))
        disponible = cur.fetchone()

        if disponible and disponible[0]:
            cur.execute("""
                INSERT INTO reservas (id_evento, id_asiento, usuario)
                SELECT id_evento, %s, %s
                FROM asientos
                WHERE id_asiento = %s;
            """, (id_asiento, usuario, id_asiento))

            cur.execute("UPDATE asientos SET disponible = FALSE WHERE id_asiento = %s;", (id_asiento,))
            conn.commit()
            print(f"[✓] {usuario} reservó el asiento {id_asiento}")
        else:
            conn.rollback()
            print(f"[X] {usuario} no pudo reservar el asiento {id_asiento} (no disponible)")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] Error en reserva de {usuario}: {e}")

def simular_reservas_concurrentes(num_usuarios, asientos_ids, nivel_aislamiento):
    threads = []
    for i in range(num_usuarios):
        usuario = f"usuario_{i+1}"
        id_asiento = asientos_ids[i % len(asientos_ids)]
        t = threading.Thread(target=intentar_reservar, args=(id_asiento, usuario, nivel_aislamiento))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    print("=== Simulador de Reservas Concurrentes ===")

    try:
        num_usuarios = int(input(" ¿Cuántos usuarios quieres simular? "))
        asientos_input = input(" Ingresa los ID de asientos separados por coma (ej: 3,4,5): ")
        asientos_ids = [int(a.strip()) for a in asientos_input.split(",")]

        print("\nNiveles de aislamiento disponibles:")
        for key in NIVELES:
            print(f" - {key}")
        aislamiento_str = input("Selecciona el nivel de aislamiento: ").strip().lower()

        if aislamiento_str not in NIVELES:
            raise ValueError("Nivel de aislamiento inválido.")

        nivel_aislamiento = NIVELES[aislamiento_str]

        inicio = time.time()
        simular_reservas_concurrentes(num_usuarios, asientos_ids, nivel_aislamiento)
        duracion = round((time.time() - inicio) * 1000, 2)
        print(f"\n Simulación completada en {duracion} ms")
    except Exception as e:
        print(f"\n[!] Error: {e}")
