import subprocess

def solicitar_parametros():
    while True:
        ip = input("Introduce la dirección IP: ")
        if validar_ip(ip):
            break
        else:
            print("Dirección IP no válida. Por favor, inténtalo de nuevo.")

    while True:
        mascara = input("Introduce la máscara de red (ejemplo: 255.255.255.0): ")
        if validar_mascara(mascara):
            break
        else:
            print("Máscara de red no válida. Por favor, inténtalo de nuevo.")

    while True:
        gateway = input("Introduce la dirección del gateway: ")
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

def cambiar_parametros_red(ip, mascara, gateway):
    try:
        # Desactivar interfaz de red
        subprocess.run(['sudo', 'ifconfig', 'eth0', 'down'])

        # Cambiar la configuración de red
        subprocess.run(['sudo', 'ifconfig', 'eth0', ip, 'netmask', mascara])
        subprocess.run(['sudo', 'route', 'add', 'default', 'gw', gateway])

        # Activar interfaz de red
        subprocess.run(['sudo', 'ifconfig', 'eth0', 'up'])

        print("Configuración de red cambiada correctamente.")
    except Exception as e:
        print("Error al cambiar la configuración de red:", e)

if __name__ == "__main__":
    ip, mascara, gateway = solicitar_parametros()
    cambiar_parametros_red(ip, mascara, gateway)
