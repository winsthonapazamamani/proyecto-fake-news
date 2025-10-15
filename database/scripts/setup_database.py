import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """Clase para manejar conexiones a la base de datos"""
    
    @staticmethod
    def get_connection():
        """Obtener conexión a la base de datos"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='amallulla_fake_news',
                user='root',
                password='',  # ⚠️ Usar variables de entorno en producción
                auth_plugin='mysql_native_password'
            )
            
            if connection.is_connected():
                print("✅ Conexión a MySQL exitosa")
                return connection
                
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    @staticmethod
    def test_connection():
        """Probar la conexión y mostrar información"""
        conn = DatabaseConnection.get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Obtener versión de MySQL
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"🔧 Versión MySQL: {version[0]}")
            
            # Obtener información de la base de datos
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"🗃️ Base de datos: {db_name[0]}")
            
            # Contar tablas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'amallulla_fake_news'
            """)
            table_count = cursor.fetchone()
            print(f"📊 Tablas en la base de datos: {table_count[0]}")
            
            cursor.close()
            conn.close()
            return True
        return False

if __name__ == "__main__":
    print("🧪 Probando conexión a la base de datos...")
    DatabaseConnection.test_connection()