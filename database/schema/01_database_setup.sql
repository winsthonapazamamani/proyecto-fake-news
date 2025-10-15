-- Crear base de datos específica para Amallulla
CREATE DATABASE IF NOT EXISTS amallulla_fake_news;
USE amallulla_fake_news;

-- Configurar caracteres para soportar español
ALTER DATABASE amallulla_fake_news 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Mostrar confirmación
SELECT '✅ Base de datos amallulla_fake_news creada exitosamente' AS Status;