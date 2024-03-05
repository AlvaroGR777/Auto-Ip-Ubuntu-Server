import subprocess
import yaml

def obtener_adaptadores_red():
    # Analiza el contenido del archivo netplan para obtener los adaptadores de red
    try:
        with open('/etc/netplan/00-installer-config.yaml', 'r') as file:
            netplan_config = yaml.safe_load(file)
            adaptadores_red = netplan_config.get('network', {}).get('ethernets', {})
            return adaptadores_red.keys()
    except Exception as e:
        print("Error al analizar el archivo netplan:", e)
        return []

def solicitar_parametros(adaptador):
    while True:
        ip = input(f"Introduce la dirección IP para {adaptador}: ")
        if validar_ip(ip):
            break
        else:
            print("Dirección IP no válida. Por favor, inténtalo de nuevo.")

    while True:
        mascara = input(f"Introduce la máscara de red para {adaptador} (ejemplo: 255.255.255.0): ")
        if validar_mascara(mascara):
            break
        else:
            print("Máscara de red no válida. Por favor, inténtalo de nuevo.")

    while True:
        gateway = input(f"Introduce la dirección del gateway para {adaptador}: ")
        if validar_ip(gateway):
            break
        else:
            print("Dirección de gateway no válida. Por favor, inténtalo de nuevo.")

    return ip, mascara, gateway

def validar_ip(ip):
    partes = ip.split('.')
    if len(partes) != 4:
        return False
    for parte in partes:
        if not 0 <= int(parte) <= 255:
            return False
    return True

def validar_mascara(mascara):
    partes = mascara.split('.')
    if len(partes) != 4:
        return False
    for parte in partes:
        if not (int(parte) == 255 or int(parte) == 0):
            return False
    return True

def modificar_archivo_netplan(adaptadores_red, parametros_red):
    try:
        with open('/etc/netplan/00-installer-config.yaml', 'r') as file:
            netplan_config = yaml.safe_load(file)

        for adaptador in adaptadores_red:
            netplan_config['network']['ethernets'][adaptador]['addresses'] = [parametros_red[adaptador]['ip']]
            netplan_config['network']['ethernets'][adaptador]['gateway4'] = parametros_red[adaptador]['gateway']

            # Verificar si el campo 'nameservers' existe antes de modificarlo
            if 'nameservers' in netplan_config['network']['ethernets'][adaptador]:
                netplan_config['network']['ethernets'][adaptador]['nameservers']['addresses'] = [parametros_red[adaptador]['gateway']]

        with open('/etc/netplan/00-installer-config.yaml', 'w') as file:
            yaml.dump(netplan_config, file, default_flow_style=False)

        print("Archivo netplan modificado correctamente.")
    except Exception as e:
        print("Error al modificar el archivo netplan:", e)

def aplicar_cambios_red():
    try:
        subprocess.run(['sudo', 'netplan', 'apply'])
        print("Cambios de red aplicados correctamente.")
    except Exception as e:
        print("Error al aplicar cambios de red:", e)

if __name__ == "__main__":
    adaptadores_red = obtener_adaptadores_red()
    if adaptadores_red:
        parametros_red = {}
        for adaptador in adaptadores_red:
            parametros_red[adaptador] = {}
            parametros_red[adaptador]['ip'], parametros_red[adaptador]['mascara'], parametros_red[adaptador]['gateway'] = solicitar_parametros(adaptador)
        modificar_archivo_netplan(adaptadores_red, parametros_red)
        aplicar_cambios_red()