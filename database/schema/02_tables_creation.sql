USE amallulla_fake_news;

-- Tabla principal basada en verificaciones de Amallulla
CREATE TABLE IF NOT EXISTS verificaciones_amallulla (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo_afirmacion TEXT NOT NULL,
    contenido_afirmacion TEXT NOT NULL,
    contexto_afirmacion TEXT,
    fuente_original VARCHAR(500),
    medio_difusion VARCHAR(255),
    fecha_afirmacion DATE,
    fecha_verificacion DATE,
    categoria_afirmacion ENUM(
        'POLITICA', 'SALUD', 'ECONOMIA', 'EDUCACION', 'SEGURIDAD',
        'CORRUPCION', 'REDES_SOCIALES', 'INTERNACIONAL', 'GOBIERNO',
        'CONGRESO', 'ELECCIONES', 'COVID19', 'VACUNAS', 'OTROS'
    ),
    calificacion_amallulla ENUM(
        'FALSO', 'VERDADERO', 'ENGAÑOSO', 'EXAGERADO',
        'SIN_EVIDENCIAS', 'CONTEXTO_ERRONEO', 'DESACTUALIZADO'
    ),
    explicacion_verificacion TEXT,
    evidencias_utilizadas JSON,
    enlaces_referencia JSON,
    palabras_clave_afirmacion JSON,
    entidades_mencionadas JSON,
    viralizacion_redes BOOLEAN DEFAULT FALSE,
    impacto_calificacion ENUM('ALTO', 'MEDIO', 'BAJO'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla para políticos y personajes mencionados frecuentemente
CREATE TABLE IF NOT EXISTS personajes_politicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    cargo_actual VARCHAR(200),
    partido_politico VARCHAR(100),
    ambito ENUM('NACIONAL', 'REGIONAL', 'LOCAL', 'INTERNACIONAL'),
    activo BOOLEAN DEFAULT TRUE,
    frecuencia_mencion INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de relaciones entre afirmaciones y personajes
CREATE TABLE IF NOT EXISTS afirmacion_personaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    verificacion_id INT,
    personaje_id INT,
    rol_en_afirmacion ENUM(
        'SUJETO', 'FUENTE', 'AFIRMANTE', 'BENEFICIADO', 'AFECTADO', 'MENCIÓN'
    ),
    contexto_mencion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verificacion_id) REFERENCES verificaciones_amallulla(id) ON DELETE CASCADE,
    FOREIGN KEY (personaje_id) REFERENCES personajes_politicos(id) ON DELETE CASCADE
);

-- Tabla para métricas de viralización
CREATE TABLE IF NOT EXISTS metricas_viralizacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    verificacion_id INT,
    plataforma ENUM('Facebook', 'Twitter', 'WhatsApp', 'TikTok', 'Instagram', 'YouTube'),
    alcance_estimado INT,
    engagement_estimado INT,
    fecha_metricas DATE,
    screenshots_urls JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verificacion_id) REFERENCES verificaciones_amallulla(id) ON DELETE CASCADE
);

-- Tabla para el modelo de ML
CREATE TABLE IF NOT EXISTS predicciones_modelo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    verificacion_id INT,
    caracteristicas_extraidas JSON,
    etiqueta_predicha VARCHAR(50),
    confianza_prediccion DECIMAL(5,4),
    caracteristicas_importantes JSON,
    version_modelo VARCHAR(50),
    fecha_prediccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verificacion_id) REFERENCES verificaciones_amallulla(id) ON DELETE CASCADE
);

-- Tabla de patrones comunes en fake news peruanas
CREATE TABLE IF NOT EXISTS patrones_desinformacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patron VARCHAR(255) UNIQUE NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    ejemplos JSON,
    frecuencia_deteccion INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para entrenamiento del modelo
CREATE TABLE IF NOT EXISTS dataset_entrenamiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto_afirmacion TEXT NOT NULL,
    etiqueta_real ENUM('FALSO', 'VERDADERO', 'ENGAÑOSO', 'EXAGERADO'),
    caracteristicas JSON,
    fuente VARCHAR(255),
    utilizado_entrenamiento BOOLEAN DEFAULT FALSE,
    fecha_incorporacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT '✅ Todas las tablas creadas exitosamente' AS Status;