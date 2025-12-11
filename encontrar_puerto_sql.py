"""
Script para encontrar el puerto de tu instancia de SQL Server
Ejecuta: python encontrar_puerto_sql.py
"""
import subprocess
import re

def encontrar_puerto_sql():
    """Intenta encontrar el puerto de SQL Server usando diferentes métodos"""
    
    print("=== Buscando puerto de SQL Server SQLEXPRESS01 ===\n")
    
    # Método 1: Usar netstat para encontrar conexiones SQL Server
    print("Metodo 1: Buscando con netstat...")
    try:
        result = subprocess.run(
            ['netstat', '-an'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Buscar líneas que contengan SQL Server (puertos comunes)
        sql_ports = []
        for line in result.stdout.split('\n'):
            if 'LISTENING' in line and ('1433' in line or '1434' in line or '49152' in line or '49153' in line):
                # Extraer el puerto
                match = re.search(r':(\d+)\s', line)
                if match:
                    port = match.group(1)
                    if port not in sql_ports:
                        sql_ports.append(port)
                        print(f"  [ENCONTRADO] Puerto posible: {port}")
        
        if sql_ports:
            print(f"\n  Puertos encontrados: {', '.join(sql_ports)}")
            print(f"  Prueba usar el primero: PORT = '{sql_ports[0]}'")
        else:
            print("  No se encontraron puertos obvios")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "="*50)
    print("\nINSTRUCCIONES MANUALES:")
    print("\n1. Abre SQL Server Configuration Manager")
    print("2. Ve a: SQL Server Network Configuration > Protocols for SQLEXPRESS01")
    print("3. Haz clic derecho en TCP/IP > Properties")
    print("4. Ve a la pestaña IP Addresses")
    print("5. Desplazate hasta IPAll")
    print("6. Busca 'TCP Dynamic Ports' o 'TCP Port'")
    print("7. Anota el numero que encuentres")
    print("8. Actualiza settings.py con ese puerto:")
    print("   'PORT': 'EL_NUMERO_QUE_ENCONTRASTE',")
    print("\nSi TCP Dynamic Ports esta vacio:")
    print("- Configura TCP Port con un numero (ej: 1433)")
    print("- Reinicia SQL Server")
    print("- Usa ese numero en settings.py")
    print("\n" + "="*50)

if __name__ == '__main__':
    encontrar_puerto_sql()


