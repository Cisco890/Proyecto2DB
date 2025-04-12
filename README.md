# Simulador de Reservas Concurrentes

Este proyecto simula múltiples usuarios intentando reservar asientos para un evento de forma concurrente, utilizando **transacciones** y diferentes **niveles de aislamiento** en PostgreSQL. El objetivo es analizar el comportamiento de la base de datos bajo condiciones de concurrencia real.

---

##  Requisitos

- Python 3.8+
- PostgreSQL (ya instalado y configurado)
- Biblioteca `psycopg2`  
  Instalar con:

  ```bash
  pip install psycopg2-binary
  ```

---

##  Configuración

Edita el archivo `reserva_simulacion.py` y actualiza la variable `DB_CONFIG` con tus datos de conexión:

```python
DB_CONFIG = {
    'dbname': 'eventos',
    'user': '', #tu usuario
    'password': '',  # tu contraseña
    'host': 'localhost',
    'port': '5432'
}
```

---

##  Cómo ejecutar

Desde la terminal:

```bash
python reserva_simulacion.py
```

Luego se te pedirá:

1. Número de usuarios a simular
2. IDs de los asientos que se desean probar (separados por coma) [1,2,3,4, etcétera]
3. Nivel de aislamiento a utilizar

---

##  Niveles de aislamiento disponibles

| Nivel              | Descripción |
|--------------------|-------------|
| `read_committed`   | Nivel por defecto en PostgreSQL. Permite lecturas de datos confirmados por otras transacciones, pero puede sufrir de lecturas no repetibles. |
| `repeatable_read`  | Asegura que las filas leídas no cambien durante la transacción. Puede generar bloqueos y evitar lecturas no repetibles, pero permite phantom reads. |
| `serializable`     | El más estricto. Ejecuta las transacciones como si fueran completamente secuenciales. Previene todos los problemas de concurrencia, pero puede fallar si detecta conflictos. |

---

## Exportación de datos a CSV

El script incluye funciones para exportar las tablas `eventos`, `asientos` y `reservas` a archivos `.csv`:

```python
exportar_eventos_a_csv()
exportar_asientos_a_csv()
exportar_reservas_a_csv()
```

Esto generará los archivos `eventos.csv`, `asientos.csv` y `reservas.csv` en el directorio actual.

---

##  Estructura del Proyecto

```
 proyecto_simulador/
├── reserva_simulacion.py
├── eventos.csv (opcional)
├── asientos.csv (opcional)
├── reservas.csv (opcional)
├── importar_csv.sql (opcional)
└── README.md
```

---

## 📌 Notas

- Cada hilo simula un usuario.
- Las reservas se hacen con `BEGIN`, `SELECT ... FOR UPDATE`, `INSERT` y `UPDATE`.
- El programa garantiza que solo un usuario pueda reservar un asiento si está disponible.
- Los resultados pueden variar según el nivel de aislamiento y el número de hilos.

---
Luis Pedro Lira - 23669, Juan Francisco Martínez - 23617 

