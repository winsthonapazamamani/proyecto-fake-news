import mysql.connector
import os
import sys

def execute_sql_file(cursor, file_path):
    """Ejecutar archivo SQL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()
            
        # Dividir por punto y coma y ejecutar cada comando
        for command in sql_commands.split(';'):
            command = command.strip()
            if command and not command.startswith('--'):
                cursor.execute(command)
                
        print(f"✅ Ejecutado: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error en {file_path}: {e}")
        return False

def setup_database():
    """Configurar la base de datos completa"""
    try:
        # Conexión inicial sin base de datos
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # ⚠️ Cambiar según tu configuración
        )
        
        cursor = conn.cursor()
        
        # Archivos SQL en orden de ejecución
        sql_files = [
            'database/schema/01_database_setup.sql',
            'database/schema/02_tables_creation.sql',
            'database/schema/03_indexes_constraints.sql',
            'database/schema/04_sample_data.sql',
            'database/schema/05_stored_procedures.sql'
        ]
        
        # Ejecutar cada archivo
        for sql_file in sql_files:
            if os.path.exists(sql_file):
                if execute_sql_file(cursor, sql_file):
                    conn.commit()
                else:
                    print(f"❌ Falló la ejecución de {sql_file}")
                    return False
            else:
                print(f"⚠️ Archivo no encontrado: {sql_file}")
        
        cursor.close()
        conn.close()
        
        print("🎉 Base de datos configurada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando configuración de base de datos...")
    if setup_database():
        print("✅ Configuración completada exitosamente")
    else:
        print("❌ Configuración falló")
        sys.exit(1)