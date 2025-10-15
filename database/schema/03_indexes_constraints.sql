USE amallulla_fake_news;

-- Crear índices para mejor performance
CREATE INDEX idx_amallulla_calificacion ON verificaciones_amallulla(calificacion_amallulla);
CREATE INDEX idx_amallulla_categoria ON verificaciones_amallulla(categoria_afirmacion);
CREATE INDEX idx_amallulla_fecha ON verificaciones_amallulla(fecha_afirmacion);
CREATE INDEX idx_amallulla_viralizacion ON verificaciones_amallulla(viralizacion_redes);
CREATE INDEX idx_personajes_nombre ON personajes_politicos(nombre_completo);
CREATE INDEX idx_afirmacion_personaje ON afirmacion_personaje(verificacion_id, personaje_id);
CREATE INDEX idx_metricas_plataforma ON metricas_viralizacion(plataforma);
CREATE INDEX idx_predicciones_confianza ON predicciones_modelo(confianza_prediccion);
CREATE INDEX idx_dataset_etiqueta ON dataset_entrenamiento(etiqueta_real);

-- Índice único para evitar duplicados en personajes
CREATE UNIQUE INDEX idx_personajes_unique ON personajes_politicos(nombre_completo);

SELECT '✅ Índices creados exitosamente' AS Status;