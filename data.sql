-- Insertar eventos
INSERT INTO eventos (nombre, fecha)
VALUES 
('Concierto Rock Fest', '2025-05-15 20:00:00'),
('Conferencia Tech', '2025-06-01 10:00:00'),
('Festival de Jazz', '2025-06-20 18:00:00');

-- Insertar asientos para cada evento (10 por evento)
-- Evento 1: Rock Fest
INSERT INTO asientos (id_evento, numero_asiento) VALUES 
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
(1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5');

-- Evento 2: Tech
INSERT INTO asientos (id_evento, numero_asiento) VALUES 
(2, 'C1'), (2, 'C2'), (2, 'C3'), (2, 'C4'), (2, 'C5'),
(2, 'D1'), (2, 'D2'), (2, 'D3'), (2, 'D4'), (2, 'D5');

-- Evento 3: Jazz
INSERT INTO asientos (id_evento, numero_asiento) VALUES 
(3, 'E1'), (3, 'E2'), (3, 'E3'), (3, 'E4'), (3, 'E5'),
(3, 'F1'), (3, 'F2'), (3, 'F3'), (3, 'F4'), (3, 'F5');

-- Insertar reservas iniciales
-- Rock Fest: A1, A2, B1 ya reservados
INSERT INTO reservas (id_evento, id_asiento, usuario)
VALUES 
(1, 1, 'juan'), 
(1, 2, 'ana'), 
(1, 6, 'carlos');

-- Tech: C1, D5 reservados
INSERT INTO reservas (id_evento, id_asiento, usuario)
VALUES 
(2, 11, 'laura'), 
(2, 20, 'marco');

-- Jazz: E1, F1, F2 reservados
INSERT INTO reservas (id_evento, id_asiento, usuario)
VALUES 
(3, 21, 'sofia'), 
(3, 26, 'andres'), 
(3, 27, 'diana');

-- Actualizar disponibilidad de asientos reservados
UPDATE asientos SET disponible = FALSE WHERE id_asiento IN (
    1, 2, 6,     -- Rock Fest
    11, 20,      -- Tech
    21, 26, 27   -- Jazz
);
