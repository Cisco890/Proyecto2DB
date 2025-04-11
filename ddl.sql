-- Crear tabla de eventos
CREATE TABLE eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL
);

-- Crear tabla de asientos
CREATE TABLE asientos (
    id_asiento SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL,
    numero_asiento VARCHAR(10) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE,
    UNIQUE (id_evento, numero_asiento)
);

-- Crear tabla de reservas
CREATE TABLE reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL,
    id_asiento INTEGER NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE,
    FOREIGN KEY (id_asiento) REFERENCES asientos(id_asiento) ON DELETE CASCADE,
    UNIQUE (id_asiento) -- Cada asiento solo puede ser reservado una vez
);
