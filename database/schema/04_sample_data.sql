USE amallulla_fake_news;

-- Insertar personajes políticos comunes en verificaciones de Amallulla
INSERT INTO personajes_politicos (nombre_completo, cargo_actual, partido_politico, ambito) VALUES
('Pedro Castillo', 'Expresidente de la República', 'Perú Libre', 'NACIONAL'),
('Dina Boluarte', 'Presidenta de la República', 'Independiente', 'NACIONAL'),
('Keiko Fujimori', 'Lideresa de Fuerza Popular', 'Fuerza Popular', 'NACIONAL'),
('Rafael López Aliaga', 'Alcalde de Lima', 'Renovación Popular', 'NACIONAL'),
('Antauro Humala', 'Líder de ETAC', 'ETAC', 'NACIONAL'),
('César Acuña', 'Líder de Alianza para el Progreso', 'Alianza para el Progreso', 'NACIONAL'),
('Aníbal Torres', 'Ex Primer Ministro', 'Perú Libre', 'NACIONAL'),
('Betsy Chávez', 'Expresidenta del Consejo de Ministros', 'Perú Libre', 'NACIONAL');

-- Insertar verificaciones de ejemplo basadas en Amallulla
INSERT INTO verificaciones_amallulla (
    titulo_afirmacion, 
    contenido_afirmacion, 
    fuente_original,
    categoria_afirmacion,
    calificacion_amallulla,
    explicacion_verificacion,
    palabras_clave_afirmacion,
    viralizacion_redes,
    impacto_calificacion
) VALUES
(
    'Gobierno planea eliminar las AFP y confiscar los fondos de pensiones',
    'Se afirma que el gobierno de Dina Boluarte planea eliminar el sistema de AFP y confiscar los fondos de los trabajadores para financiar gasto público',
    'Cadena de WhatsApp',
    'ECONOMIA',
    'FALSO',
    'No existe ningún proyecto de ley ni declaración oficial que sustente esta afirmación. El MEF ha desmentido categóricamente esta información en comunicados oficiales.',
    '["AFP", "fondos", "pensiones", "confiscación", "gobierno", "Dina Boluarte"]',
    TRUE,
    'ALTO'
),
(
    'Vacuna contra COVID-19 contiene chip de rastreo de Bill Gates',
    'Circula en redes que las vacunas contra el COVID-19 contienen microchips financiados por Bill Gates para controlar a la población mundial',
    'Facebook e Instagram',
    'SALUD',
    'FALSO',
    'Expertos en salud y tecnología han desmentido esta teoría conspirativa. Las vacunas no contienen dispositivos de rastreo y Bill Gates no tiene relación con su desarrollo.',
    '["vacuna", "COVID", "chip", "rastreo", "Bill Gates", "control"]',
    TRUE,
    'ALTO'
);

-- Insertar relaciones con personajes
INSERT INTO afirmacion_personaje (verificacion_id, personaje_id, rol_en_afirmacion) VALUES
(1, 2, 'SUJETO'),  -- Dina Boluarte en afirmación 1
(2, 2, 'MENCIÓN'); -- Dina Boluarte en afirmación 2

-- Insertar patrones comunes de desinformación
INSERT INTO patrones_desinformacion (patron, descripcion, categoria, ejemplos) VALUES
(
    'Supuesta ley o decreto inexistente',
    'Afirman la existencia de leyes, decretos o proyectos de ley que no existen o son falsos',
    'POLITICA',
    '["Ley que elimina AFP", "Decreto para confiscar propiedades", "Proyecto para eliminar moneda nacional"]'
),
(
    'Teorías conspirativas de salud',
    'Desinformación sobre vacunas, enfermedades o tratamientos médicos con teorías sin fundamento',
    'SALUD',
    '["Vacunas con chips", "Remedios milagrosos", "Enfermedades inventadas para control poblacional"]'
);

SELECT '✅ Datos de ejemplo insertados exitosamente' AS Status;