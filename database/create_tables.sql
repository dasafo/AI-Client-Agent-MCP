-- Creación de las tablas (si no existen)
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    issued_at DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    status TEXT DEFAULT 'pending' -- 'pending', 'completed', 'canceled'
);

CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    client_id INTEGER,                -- Puede ser NULL para informes globales
    client_name TEXT,                 -- Puede ser NULL o 'All clients' para informes globales
    period TEXT,                      -- Puede ser NULL para informes globales
    manager_email TEXT NOT NULL,
    manager_name TEXT NOT NULL,
    report_type TEXT NOT NULL,
    report_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Inserción de Clientes y sus Facturas Intercaladas

-- Cliente 1 (ID asumido: 1)
INSERT INTO clients (name, city, email) VALUES ('Tammy Cruz', 'Málaga', 'tammy.cruz@example.com');
-- Facturas para Tammy Cruz (client_id = 1) - 5 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (1, 150.75, '2023-10-01', '2023-10-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (1, 75.00, '2024-01-15', '2024-02-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (1, 220.50, '2023-05-12', '2023-06-11', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (1, 30.99, '2022-11-22', '2022-12-22', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (1, 450.00, '2023-08-03', '2023-09-02', 'completed');

-- Cliente 2 (ID asumido: 2)
INSERT INTO clients (name, city, email) VALUES ('Elba Salcedo', 'East Lee', 'elba.salcedo@example.com');
-- Facturas para Elba Salcedo (client_id = 2) - 3 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (2, 299.99, '2023-11-05', '2023-12-05', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (2, 120.00, '2023-02-19', '2023-03-21', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (2, 85.60, '2022-09-03', '2022-10-03', 'canceled');

-- Cliente 3 (ID asumido: 3)
INSERT INTO clients (name, city, email) VALUES ('Erika Martin', 'Garciatown', 'erika.martin@example.com');
-- Facturas para Erika Martin (client_id = 3) - 18 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 50.00, '2023-09-20', '2023-10-20', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 120.00, '2024-02-10', '2024-03-11', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 75.50, '2023-01-01', '2023-01-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 250.00, '2022-07-15', '2022-08-14', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 90.80, '2023-04-05', '2023-05-05', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 15.00, '2022-03-10', '2022-04-09', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 300.00, '2023-10-25', '2023-11-24', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 42.20, '2024-01-02', '2024-02-01', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 110.00, '2022-12-01', '2022-12-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 65.00, '2023-06-12', '2023-07-12', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 199.99, '2022-01-20', '2022-02-19', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 88.00, '2023-11-30', '2023-12-30', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 275.00, '2022-09-05', '2022-10-05', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 55.60, '2023-03-15', '2023-04-14', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 140.00, '2022-05-22', '2022-06-21', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 23.45, '2023-07-01', '2023-07-31', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 160.00, '2022-10-10', '2022-11-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (3, 99.00, '2024-03-01', '2024-03-31', 'pending');


-- Cliente 4 (ID asumido: 4)
INSERT INTO clients (name, city, email) VALUES ('Nicole Watson', 'Teruel', 'nicole.watson@example.com');
-- Facturas para Nicole Watson (client_id = 4) - 1 factura
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (4, 450.20, '2023-12-01', '2023-12-31', 'pending');

-- Cliente 5 (ID asumido: 5)
INSERT INTO clients (name, city, email) VALUES ('Ezequiel Sarabia', 'Jenniferfort', 'ezequiel.sarabia@example.com');
-- Facturas para Ezequiel Sarabia (client_id = 5) - 24 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 88.50, '2024-01-05', '2024-02-04', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 123.45, '2023-03-10', '2023-04-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 56.78, '2022-08-15', '2022-09-14', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 200.00, '2023-10-01', '2023-10-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 75.20, '2024-02-20', '2024-03-21', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 300.50, '2022-01-25', '2022-02-24', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 99.00, '2023-06-05', '2023-07-05', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 150.75, '2022-11-11', '2022-12-11', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 45.90, '2023-09-12', '2023-10-12', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 180.00, '2024-03-01', '2024-03-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 62.30, '2022-04-07', '2022-05-07', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 220.00, '2023-01-18', '2023-02-17', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 80.00, '2022-07-22', '2022-08-21', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 135.60, '2023-12-03', '2024-01-02', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 92.15, '2022-02-14', '2022-03-16', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 260.80, '2023-07-09', '2023-08-08', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 70.00, '2022-05-29', '2022-06-28', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 115.40, '2023-02-28', '2023-03-30', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 205.00, '2022-10-16', '2022-11-15', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 53.25, '2023-05-02', '2023-06-01', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 170.00, '2022-06-19', '2022-07-19', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 100.00, '2023-04-24', '2023-05-24', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 33.80, '2022-12-28', '2023-01-27', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (5, 290.10, '2023-08-11', '2023-09-10', 'completed');


-- Cliente 6 (ID asumido: 6)
INSERT INTO clients (name, city, email) VALUES ('Kike Rolón', 'San Claudia los bajos', 'kike.rolón@example.com');
-- Facturas para Kike Rolón (client_id = 6) - 7 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 199.00, '2023-08-15', '2023-09-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 25.00, '2024-03-01', '2024-03-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 350.70, '2022-10-10', '2022-11-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 80.20, '2023-04-20', '2023-05-20', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 150.00, '2022-06-05', '2022-07-05', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 60.00, '2023-12-12', '2024-01-11', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (6, 210.50, '2022-02-02', '2022-03-04', 'completed');

-- Cliente 7 (ID asumido: 7)
INSERT INTO clients (name, city, email) VALUES ('Andrea Robinson', 'San Amalia de la Montaña', 'andrea.robinson@example.com');
-- Facturas para Andrea Robinson (client_id = 7) - 2 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (7, 320.00, '2023-07-10', '2023-08-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (7, 95.50, '2022-12-05', '2023-01-04', 'pending');

-- Cliente 8 (ID asumido: 8)
INSERT INTO clients (name, city, email) VALUES ('Daniel Pelayo', 'North Alison', 'daniel.pelayo@example.com');
-- Facturas para Daniel Pelayo (client_id = 8) - 10 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 65.90, '2024-02-20', '2024-03-21', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 120.00, '2023-01-15', '2023-02-14', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 200.00, '2022-05-01', '2022-05-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 45.75, '2023-09-10', '2023-10-10', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 180.00, '2022-11-25', '2022-12-25', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 90.50, '2024-01-03', '2024-02-02', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 300.00, '2023-06-18', '2023-07-18', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 77.00, '2022-02-10', '2022-03-12', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 130.20, '2023-12-08', '2024-01-07', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (8, 50.00, '2022-08-01', '2022-08-31', 'canceled');

-- Cliente 9 (ID asumido: 9)
INSERT INTO clients (name, city, email) VALUES ('Elodia Tamayo', 'Marissaville', 'elodia.tamayo@example.com');
-- Facturas para Elodia Tamayo (client_id = 9) - 4 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (9, 500.00, '2023-06-01', '2023-06-30', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (9, 150.00, '2024-01-20', '2024-02-19', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (9, 220.80, '2022-09-15', '2022-10-15', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (9, 70.00, '2023-03-05', '2023-04-04', 'completed');

-- Cliente 10 (ID asumido: 10)
INSERT INTO clients (name, city, email) VALUES ('Josep Holland', 'Nueva Dinamarca', 'josep.holland@example.com');
-- Facturas para Josep Holland (client_id = 10) - 6 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (10, 770.40, '2023-05-05', '2023-06-04', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (10, 120.00, '2022-01-10', '2022-02-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (10, 300.00, '2023-11-10', '2023-12-10', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (10, 55.90, '2022-07-20', '2022-08-19', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (10, 400.00, '2024-02-01', '2024-03-02', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (10, 90.00, '2023-02-25', '2023-03-27', 'pending');

-- Cliente 11 (ID asumido: 11)
INSERT INTO clients (name, city, email) VALUES ('Ciríaco Hernández', 'San Amanda los bajos', 'ciríaco.hernández@example.com');
-- Facturas para Ciríaco Hernández (client_id = 11) - 21 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 99.99, '2024-03-05', '2024-04-04', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 145.50, '2023-01-12', '2023-02-11', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 210.75, '2022-04-18', '2022-05-18', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 60.20, '2023-08-02', '2023-09-01', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 320.00, '2022-11-22', '2022-12-22', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 88.00, '2024-01-08', '2024-02-07', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 175.00, '2023-05-14', '2023-06-13', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 40.90, '2022-02-03', '2022-03-05', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 250.60, '2023-10-27', '2023-11-26', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 105.00, '2022-07-01', '2022-07-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 70.30, '2023-03-09', '2023-04-08', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 190.00, '2022-09-13', '2022-10-13', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 15.55, '2023-12-07', '2024-01-06', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 125.00, '2022-06-25', '2022-07-25', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 280.10, '2024-02-15', '2024-03-16', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 95.00, '2023-07-19', '2023-08-18', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 50.00, '2022-03-28', '2022-04-27', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 300.00, '2023-09-03', '2023-10-03', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 160.80, '2022-12-30', '2023-01-29', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 220.00, '2023-06-11', '2023-07-11', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (11, 35.70, '2022-08-08', '2022-09-07', 'pending');

-- Cliente 12 (ID asumido: 12)
INSERT INTO clients (name, city, email) VALUES ('Jose Francisco Lerma', 'East Shirleymouth', 'jose francisco.lerma@example.com');
-- Facturas para Jose Francisco Lerma (client_id = 12) - 3 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (12, 210.00, '2023-04-10', '2023-05-10', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (12, 105.50, '2023-10-11', '2023-11-10', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (12, 75.00, '2022-03-01', '2022-03-31', 'pending');

-- Cliente 13 (ID asumido: 13)
INSERT INTO clients (name, city, email) VALUES ('Dana Ramón', 'Perkinston', 'dana.ramón@example.com');
-- Facturas para Dana Ramón (client_id = 13) - 1 factura
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (13, 333.33, '2023-03-15', '2023-04-14', 'completed');

-- Cliente 14 (ID asumido: 14)
INSERT INTO clients (name, city, email) VALUES ('Michael Tenorio', 'Castellón', 'michael.tenorio@example.com');
-- Facturas para Michael Tenorio (client_id = 14) - 8 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 123.45, '2024-02-01', '2024-03-02', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 400.00, '2023-07-07', '2023-08-06', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 60.80, '2022-10-14', '2022-11-13', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 250.00, '2023-01-20', '2023-02-19', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 110.50, '2022-04-28', '2022-05-28', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 180.00, '2023-09-05', '2023-10-05', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 77.25, '2022-12-12', '2023-01-11', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (14, 300.00, '2024-03-10', '2024-04-09', 'pending');

-- Cliente 15 (ID asumido: 15)
INSERT INTO clients (name, city, email) VALUES ('Carolina Padilla', 'Vanessashire', 'carolina.padilla@example.com');
-- Facturas para Carolina Padilla (client_id = 15) - 12 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 600.00, '2023-02-20', '2023-03-22', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 50.25, '2023-09-01', '2023-10-01', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 125.00, '2022-01-05', '2022-02-04', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 320.70, '2023-05-18', '2023-06-17', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 80.00, '2022-08-10', '2022-09-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 190.90, '2023-11-25', '2023-12-25', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 260.00, '2022-03-15', '2022-04-14', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 45.50, '2024-01-10', '2024-02-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 500.00, '2022-06-01', '2022-06-30', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 150.00, '2023-10-07', '2023-11-06', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 95.30, '2022-12-19', '2023-01-18', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (15, 210.00, '2023-07-22', '2023-08-21', 'completed');

-- Cliente 16 (ID asumido: 16)
INSERT INTO clients (name, city, email) VALUES ('Susana Merino', 'Robertview', 'susana.merino@example.com');
-- Facturas para Susana Merino (client_id = 16) - 1 factura
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (16, 95.80, '2023-01-25', '2023-02-24', 'canceled');

-- Cliente 17 (ID asumido: 17)
INSERT INTO clients (name, city, email) VALUES ('Lilia Yáñez', 'Cáceres', 'lilia.yáñez@example.com');
-- Facturas para Lilia Yáñez (client_id = 17) - 3 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (17, 275.00, '2024-01-10', '2024-02-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (17, 85.40, '2023-06-15', '2023-07-15', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (17, 199.99, '2022-11-01', '2022-11-30', 'pending');

-- Cliente 18 (ID asumido: 18)
INSERT INTO clients (name, city, email) VALUES ('Salvador Summers', 'Nueva Saint Kitts y Nevis', 'salvador.summers@example.com');
-- Facturas para Salvador Summers (client_id = 18) - 4 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (18, 42.00, '2023-12-15', '2024-01-14', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (18, 180.00, '2024-03-10', '2024-04-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (18, 67.50, '2023-02-05', '2023-03-07', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (18, 240.00, '2022-08-20', '2022-09-19', 'completed');

-- Cliente 19 (ID asumido: 19)
INSERT INTO clients (name, city, email) VALUES ('Margarita Hawkins', 'Marieburgh', 'margarita.hawkins@example.com');
-- Facturas para Margarita Hawkins (client_id = 19) - 2 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (19, 310.60, '2023-11-20', '2023-12-20', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (19, 115.00, '2022-05-10', '2022-06-09', 'pending');

-- Cliente 20 (ID asumido: 20)
INSERT INTO clients (name, city, email) VALUES ('Ruben Ortiz', 'Navarra', 'ruben.ortiz@example.com');
-- Facturas para Ruben Ortiz (client_id = 20) - 5 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (20, 160.25, '2024-02-05', '2024-03-06', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (20, 280.00, '2023-08-01', '2023-08-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (20, 50.00, '2022-02-15', '2022-03-17', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (20, 400.00, '2023-10-10', '2023-11-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (20, 75.90, '2022-07-25', '2022-08-24', 'completed');

-- Continuar este patrón para los clientes restantes (21 a 39)
-- Ajustando el número de facturas entre 1 y 25 para cada uno.
-- Por brevedad, solo completaré unos pocos más, pero el patrón es el mismo.

-- Cliente 21 (ID asumido: 21)
INSERT INTO clients (name, city, email) VALUES ('Sheri Griffin', 'Barcelona', 'sheri.griffin@example.com');
-- Facturas para Sheri Griffin (client_id = 21) - 2 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (21, 850.00, '2023-10-25', '2023-11-24', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (21, 125.50, '2024-01-01', '2024-01-31', 'completed');

-- Cliente 22 (ID asumido: 22)
INSERT INTO clients (name, city, email) VALUES ('Joseph Rogers', 'Lake Bonnie', 'joseph.rogers@example.com');
-- Facturas para Joseph Rogers (client_id = 22) - 1 factura
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (22, 75.99, '2023-09-30', '2023-10-30', 'pending');

-- Cliente 23 (ID asumido: 23)
INSERT INTO clients (name, city, email) VALUES ('Christopher Vicens', 'Vieja Brasil', 'christopher.vicens@example.com');
-- Facturas para Christopher Vicens (client_id = 23) - 25 facturas
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 200.00, '2024-03-12', '2024-04-11', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 45.50, '2023-01-05', '2023-02-04', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 112.75, '2022-06-18', '2022-07-18', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 300.00, '2023-09-22', '2023-10-22', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 88.20, '2024-02-01', '2024-03-02', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 175.00, '2022-03-10', '2022-04-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 50.00, '2023-07-14', '2023-08-13', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 220.90, '2022-11-28', '2022-12-28', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 130.00, '2023-04-02', '2023-05-02', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 95.60, '2022-09-07', '2022-10-07', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 15.25, '2024-01-15', '2024-02-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 400.00, '2023-05-19', '2023-06-18', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 67.00, '2022-01-23', '2022-02-22', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 180.40, '2023-12-04', '2024-01-03', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 270.00, '2022-08-11', '2022-09-10', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 33.00, '2023-02-26', '2023-03-28', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 101.50, '2022-10-30', '2022-11-29', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 255.00, '2023-06-08', '2023-07-08', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 79.80, '2022-04-14', '2022-05-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 140.00, '2023-11-17', '2023-12-17', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 205.20, '2022-07-03', '2022-08-02', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 190.00, '2024-03-03', '2024-04-02', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 25.00, '2023-08-20', '2023-09-19', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 310.00, '2022-12-25', '2023-01-24', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (23, 60.00, '2023-10-09', '2023-11-08', 'completed');


-- Cliente 24 (ID asumido: 24)
INSERT INTO clients (name, city, email) VALUES ('Elena Thomas', 'New Vincent', 'elena.thomas@example.com');
-- Facturas para Elena Thomas (client_id = 24)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (24, 530.10, '2023-08-01', '2023-08-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (24, 90.00, '2024-02-15', '2024-03-16', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (24, 125.50, '2022-11-10', '2022-12-10', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (24, 70.20, '2023-03-05', '2023-04-04', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (24, 300.00, '2024-01-02', '2024-02-01', 'pending');

-- Cliente 25 (ID asumido: 25)
INSERT INTO clients (name, city, email) VALUES ('Bernardino Barrett', 'Vizcaya', 'bernardino.barrett@example.com');
-- Facturas para Bernardino Barrett (client_id = 25)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (25, 110.00, '2023-07-05', '2023-08-04', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (25, 45.90, '2022-09-15', '2022-10-15', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (25, 260.00, '2023-12-01', '2023-12-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (25, 88.00, '2024-03-03', '2024-04-02', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (25, 150.25, '2023-01-20', '2023-02-19', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (25, 500.00, '2022-05-01', '2022-05-31', 'completed');

-- Cliente 26 (ID asumido: 26)
INSERT INTO clients (name, city, email) VALUES ('Adalberto Cantero', 'San Rufino los altos', 'adalberto.cantero@example.com');
-- Facturas para Adalberto Cantero (client_id = 26)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (26, 40.50, '2024-01-22', '2024-02-21', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (26, 199.00, '2023-06-11', '2023-07-11', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (26, 75.00, '2022-08-01', '2022-08-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (26, 310.80, '2023-10-25', '2023-11-24', 'pending');

-- Cliente 27 (ID asumido: 27)
INSERT INTO clients (name, city, email) VALUES ('Taylor Peláez', 'Barcelona', 'taylor.peláez@example.com');
-- Facturas para Taylor Peláez (client_id = 27)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 700.00, '2023-06-10', '2023-07-10', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 140.70, '2023-12-01', '2023-12-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 55.00, '2022-04-01', '2022-04-30', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 230.25, '2024-02-20', '2024-03-21', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 99.99, '2023-03-15', '2023-04-14', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 450.00, '2022-10-05', '2022-11-04', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 120.00, '2023-09-18', '2023-10-18', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 65.80, '2022-01-10', '2022-02-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (27, 315.50, '2024-01-07', '2024-02-06', 'pending');

-- Cliente 28 (ID asumido: 28)
INSERT INTO clients (name, city, email) VALUES ('Isaías Puerta', 'Cuenca', 'isaías.puerta@example.com');
-- Facturas para Isaías Puerta (client_id = 28)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (28, 222.22, '2023-05-15', '2023-06-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (28, 80.00, '2022-07-01', '2022-07-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (28, 175.60, '2023-11-20', '2023-12-20', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (28, 30.50, '2024-03-01', '2024-03-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (28, 400.00, '2022-12-05', '2023-01-04', 'completed');

-- Cliente 29 (ID asumido: 29)
INSERT INTO clients (name, city, email) VALUES ('Jessica Montez', 'Taylorville', 'jessica.montez@example.com');
-- Facturas para Jessica Montez (client_id = 29)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (29, 30.00, '2024-02-28', '2024-03-29', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (29, 155.75, '2023-07-10', '2023-08-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (29, 92.00, '2022-10-01', '2022-10-31', 'completed');

-- Cliente 30 (ID asumido: 30)
INSERT INTO clients (name, city, email) VALUES ('Natasha Collins', 'East Kristin', 'natasha.collins@example.com');
-- Facturas para Natasha Collins (client_id = 30)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 135.00, '2023-04-20', '2023-05-20', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 68.40, '2023-11-11', '2023-12-11', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 220.00, '2022-02-05', '2022-03-07', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 77.77, '2024-01-15', '2024-02-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 310.50, '2022-09-20', '2022-10-20', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 49.90, '2023-06-01', '2023-06-30', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (30, 180.00, '2024-03-10', '2024-04-09', 'pending');

-- Cliente 31 (ID asumido: 31)
INSERT INTO clients (name, city, email) VALUES ('Jerónimo Stevens', 'Valencia', 'jerónimo.stevens@example.com');
-- Facturas para Jerónimo Stevens (client_id = 31)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 480.90, '2023-03-25', '2023-04-24', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 120.00, '2022-06-15', '2022-07-15', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 35.50, '2023-10-01', '2023-10-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 250.75, '2024-02-05', '2024-03-06', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 90.00, '2022-11-10', '2022-12-10', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 600.00, '2023-07-20', '2023-08-19', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 155.00, '2024-01-01', '2024-01-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 72.30, '2022-03-03', '2022-04-02', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 199.99, '2023-09-05', '2023-10-05', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (31, 40.00, '2022-01-20', '2022-02-19', 'canceled');

-- Cliente 32 (ID asumido: 32)
INSERT INTO clients (name, city, email) VALUES ('Emilio Mateo', 'Boydburgh', 'emilio.mateo@example.com');
-- Facturas para Emilio Mateo (client_id = 32)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (32, 80.00, '2024-01-08', '2024-02-07', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (32, 215.50, '2023-05-10', '2023-06-09', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (32, 99.00, '2022-08-22', '2022-09-21', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (32, 45.25, '2023-11-01', '2023-11-30', 'pending');

-- Cliente 33 (ID asumido: 33)
INSERT INTO clients (name, city, email) VALUES ('Cándida Chavarría', 'Vieja Países Bajos', 'cándida.chavarría@example.com');
-- Facturas para Cándida Chavarría (client_id = 33)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (33, 250.00, '2023-02-01', '2023-03-03', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (33, 175.20, '2023-08-08', '2023-09-07', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (33, 60.00, '2022-05-25', '2022-06-24', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (33, 330.90, '2024-01-12', '2024-02-11', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (33, 105.00, '2022-12-18', '2023-01-17', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (33, 200.00, '2023-06-05', '2023-07-05', 'pending');

-- Cliente 34 (ID asumido: 34)
INSERT INTO clients (name, city, email) VALUES ('Soraya Tomas', 'Bowersmouth', 'soraya.tomas@example.com');
-- Facturas para Soraya Tomas (client_id = 34)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (34, 100.00, '2023-01-12', '2023-02-11', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (34, 275.80, '2022-07-19', '2022-08-18', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (34, 50.20, '2023-09-03', '2023-10-03', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (34, 140.00, '2024-02-20', '2024-03-21', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (34, 300.00, '2022-04-01', '2022-04-30', 'completed');

-- Cliente 35 (ID asumido: 35)
INSERT INTO clients (name, city, email) VALUES ('Susana Lopez', 'Baleares', 'susana.lopez@example.com');
-- Facturas para Susana Lopez (client_id = 35)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 375.50, '2024-03-15', '2024-04-14', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 88.00, '2023-04-10', '2023-05-10', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 190.20, '2022-09-01', '2022-09-30', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 45.99, '2023-12-05', '2024-01-04', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 260.00, '2022-02-18', '2022-03-20', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 112.75, '2024-01-22', '2024-02-21', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (35, 500.00, '2023-08-14', '2023-09-13', 'completed');

-- Cliente 36 (ID asumido: 36)
INSERT INTO clients (name, city, email) VALUES ('Nélida Aragón', 'Nueva Omán', 'nélida.aragón@example.com');
-- Facturas para Nélida Aragón (client_id = 36)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (36, 55.55, '2023-12-20', '2024-01-19', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (36, 220.00, '2024-02-12', '2024-03-13', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (36, 95.30, '2023-03-01', '2023-03-31', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (36, 140.60, '2022-07-07', '2022-08-06', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (36, 30.00, '2023-10-10', '2023-11-09', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (36, 410.00, '2022-01-05', '2022-02-04', 'completed');

-- Cliente 37 (ID asumido: 37)
INSERT INTO clients (name, city, email) VALUES ('George Calzada', 'San Celia los altos', 'george.calzada@example.com');
-- Facturas para George Calzada (client_id = 37)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (37, 190.80, '2023-11-25', '2023-12-25', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (37, 65.00, '2024-03-01', '2024-03-31', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (37, 240.25, '2022-06-10', '2022-07-10', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (37, 77.90, '2023-02-15', '2023-03-17', 'completed');

-- Cliente 38 (ID asumido: 38)
INSERT INTO clients (name, city, email) VALUES ('Inmaculada Brown', 'Ceuta', 'inmaculada.brown@example.com');
-- Facturas para Inmaculada Brown (client_id = 38)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 400.00, '2024-01-29', '2024-02-28', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 123.40, '2023-05-05', '2023-06-04', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 88.88, '2022-10-12', '2022-11-11', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 210.00, '2023-07-18', '2023-08-17', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 55.50, '2024-03-05', '2024-04-04', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 305.00, '2022-01-20', '2022-02-19', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 160.70, '2023-09-22', '2023-10-22', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 70.00, '2022-04-08', '2022-05-08', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (38, 290.15, '2023-12-11', '2024-01-10', 'canceled');

-- Cliente 39 (ID asumido: 39)
INSERT INTO clients (name, city, email) VALUES ('Ibán Nazario', 'Asturias', 'ibán.nazario@example.com');
-- Facturas para Ibán Nazario (client_id = 39)
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 620.00, '2023-10-30', '2023-11-29', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 35.75, '2024-03-03', '2024-04-02', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 180.90, '2023-01-10', '2023-02-09', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 99.00, '2022-06-20', '2022-07-20', 'completed');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 275.00, '2023-08-05', '2023-09-04', 'pending');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 40.50, '2022-11-15', '2022-12-15', 'canceled');
INSERT INTO invoices (client_id, amount, issued_at, due_date, status) VALUES (39, 500.00, '2024-02-01', '2024-03-02', 'completed');