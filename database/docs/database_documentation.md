
### **9. `database/docs/database_documentation.md`**
```markdown
# Documentación Técnica - Base de Datos

## Diagrama Entidad-Relación

## Descripción de Tablas

### verificaciones_amallulla
Tabla principal que almacena todas las verificaciones de Amallulla.

**Campos importantes:**
- `categoria_afirmacion`: Categoría temática (POLITICA, SALUD, etc.)
- `calificacion_amallulla`: Resultado de verificación (FALSO, VERDADERO, etc.)
- `viralizacion_redes`: Indicador si fue viral en redes
- `impacto_calificacion`: Nivel de impacto (ALTO, MEDIO, BAJO)

### personajes_politicos
Catálogo de políticos y figuras públicas mencionadas.

### afirmacion_personaje
Tabla de relación many-to-many entre verificaciones y personajes.

## Índices de Optimización
- Índices en campos de búsqueda frecuente
- Índices únicos para evitar duplicados
- Índices compuestos para consultas complejas

## Seguridad
- Usar variables de entorno para credenciales
- No incluir datos sensibles en los scripts
- Backup regular de la base de datos