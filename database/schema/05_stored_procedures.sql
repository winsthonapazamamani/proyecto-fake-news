USE amallulla_fake_news;

-- Procedimiento para registrar nueva verificación
DELIMITER //
CREATE PROCEDURE sp_registrar_verificacion(
    IN p_titulo TEXT,
    IN p_contenido TEXT,
    IN p_fuente VARCHAR(500),
    IN p_categoria VARCHAR(50),
    IN p_calificacion VARCHAR(50),
    IN p_explicacion TEXT,
    IN p_palabras_clave JSON
)
BEGIN
    INSERT INTO verificaciones_amallulla (
        titulo_afirmacion, contenido_afirmacion, fuente_original, 
        categoria_afirmacion, calificacion_amallulla, explicacion_verificacion,
        palabras_clave_afirmacion, fecha_verificacion
    ) VALUES (
        p_titulo, p_contenido, p_fuente, p_categoria, p_calificacion,
        p_explicacion, p_palabras_clave, CURDATE()
    );
    
    SELECT LAST_INSERT_ID() as nuevo_id;
END//
DELIMITER ;

-- Función para obtener estadísticas por categoría
DELIMITER //
CREATE PROCEDURE sp_estadisticas_categoria(IN p_categoria VARCHAR(50))
BEGIN
    SELECT 
        calificacion_amallulla,
        COUNT(*) as total,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM verificaciones_amallulla WHERE categoria_afirmacion = p_categoria)), 2) as porcentaje
    FROM verificaciones_amallulla 
    WHERE categoria_afirmacion = p_categoria
    GROUP BY calificacion_amallulla
    ORDER BY total DESC;
END//
DELIMITER ;

-- Vista para análisis frecuente
CREATE VIEW vista_analisis_desinformacion AS
SELECT 
    va.calificacion_amallulla,
    va.categoria_afirmacion,
    COUNT(*) as total_afirmaciones,
    AVG(CASE WHEN va.viralizacion_redes THEN 1 ELSE 0 END) as tasa_viralizacion,
    GROUP_CONCAT(DISTINCT pp.nombre_completo) as personajes_frecuentes
FROM verificaciones_amallulla va
LEFT JOIN afirmacion_personaje ap ON va.id = ap.verificacion_id
LEFT JOIN personajes_politicos pp ON ap.personaje_id = pp.id
GROUP BY va.calificacion_amallulla, va.categoria_afirmacion;

SELECT '✅ Procedimientos almacenados creados exitosamente' AS Status;