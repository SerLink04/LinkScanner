# -*- coding: utf-8 -*-

from rainbow import *
import os
from colorama import *
from threading import Thread
from shodan import Shodan
from check_mc_info import *
import ctypes
from datetime import datetime
import re

# Coded by SerLink04 (discord.gg/comunidad)

name_cmd = "LinkScanner | discord.gg/comunidad | Coded by SerLink04"

try:
    ctypes.windll.kernel32.SetConsoleTitleW(name_cmd)
except:
    pass
def fix_motd(motd):
    return re.sub(r'&[0-9A-Za-z]|§[0-9A-Za-z]|\n|\r|\\n', '', motd)
    
def scan_mc(ip, puerto, scan_save, file_name, timeout):
    mcinfo = StatusPing(ip.strip(),puerto, timeout)
    if not mcinfo:
        return
    else:
        try:
            status = mcinfo.get_status()
            version = status["version"]["name"]
            players_on = status["players"]["online"]
            players_max = status["players"]["max"]
            try:
                motd = fix_motd(status["description"]["text"])
                if motd.strip() == '':
                    motd = fix_motd(status["description"]["extra"]["text"])
            except:
                try:
                    motd = fix_motd(status["description"]["extra"]["text"])
                except:
                    try:
                        motd = fix_motd(status["description"])
                    except:
                        motd = "A Minecraft Server"
            forge = [i.lower() for i in status]
            if "modinfo" in forge and not status["modinfo"]["modList"]:
                mods = "N/A"
            else:
                resultado = "forgedata" in forge or "modinfo" in forge
                if resultado:
                    mods = "Yes"
                else:
                    mods = "N/A"
            #rainbow(f"Server found: {ip}:{puerto} | version: {version} | players: {players_on}/{players_max} | motd: {motd} | server of mods: {mods}")
            print(Fore.WHITE + "Server found: " + Fore.LIGHTRED_EX + ip + ":" + str(puerto) + Fore.CYAN + " >> " + Fore.WHITE + "version: " + Fore.LIGHTRED_EX + str(version) + Fore.CYAN +
                " || " + Fore.WHITE + "players: " + Fore.LIGHTRED_EX + str(players_on) +"/" + str(players_max) + Fore.CYAN + " ||" +
                Fore.WHITE + " motd: " + Fore.LIGHTRED_EX + str(motd) + Fore.CYAN + " ||" + Fore.WHITE +" server of mods: " + Fore.LIGHTRED_EX + str(mods))
            print("\n")
            if scan_save:
                file = open(file_name, 'a')
                file.write(f"Server found: {ip}:{puerto} | version: {version} | players: {players_on}/{players_max} | motd: {motd} | server of mods: {mods}" + '\n')
                file.close()
        except:
            return
    
def is_a_semirange(ip):
    if not "." in ip or not "*" in ip:
        return False
    count = ip.count(".")
    count2 = ip.count("*")
    if count != 3 or count2 != 1:
        return False
    splited = ip.split(".")
    rangos_permitidos = [1,2,3]
    if len(splited) == 4 and splited[0].isdigit() and splited[1].isdigit() and splited[2].isdigit() and splited[3] == "*":
        if len(splited[0]) in rangos_permitidos and len(splited[1]) in rangos_permitidos and len(splited[2]) in rangos_permitidos:
            if int(splited[0]) < 0 or int(splited[0]) > 255 or int(splited[1]) < 0 or int(splited[1]) > 255 or int(splited[2]) < 0 or int(splited[2]) > 255:
                return False
            else:
                return True
        else:
            return False
    else:
        return False
        
def is_an_ip(ip):
    if not "." in ip:
        return False
    count = ip.count(".")
    if count != 3:
        return False
    splited = ip.split(".")
    rangos_permitidos = [1,2,3]
    if len(splited) == 4 and splited[0].isdigit() and splited[1].isdigit() and splited[2].isdigit() and splited[3].isdigit():
        if len(splited[0]) in rangos_permitidos and len(splited[1]) in rangos_permitidos and len(splited[2]) in rangos_permitidos and len(splited[3]) in rangos_permitidos:
            if int(splited[0]) < 0 or int(splited[0]) > 255 or int(splited[1]) < 0 or int(splited[1]) > 255 or int(splited[2]) < 0 or int(splited[2]) > 255 or int(splited[3]) < 0 or int(splited[3]) > 255:
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def fix_ip(semirango, ip, rango1, rango2, save_filee, name_file_, timeout):
    semirange_real = semirango.replace("*","") + str(ip)
    hilo_scan = Thread(target=range_scan_2, args=(semirange_real, rango1, rango2, save_filee, name_file_, timeout))
    hilo_scan.start()
    
def scanning(semirange, rango1, rango2, save_filee, name_file_, timeout):
    for i in range(1,256):
        scan_thread = Thread(target=fix_ip, args=(semirange, i, rango1, rango2, save_filee, name_file_, timeout))
        scan_thread.start()
    
def range_scan(semiranges, rango1, rango2, save_filee, name_file_, timeout):
    t1 = datetime.now()
    for semirange in semiranges:
        if type(rango1) == list:
            for ports_range in rango1:
                rango1 = int(ports_range.split("-")[0])
                rango2 = int(ports_range.split("-")[1])
                scan_thread2 = Thread(target=scanning, args=(semirange, rango1, rango2, save_filee, name_file_, timeout))
                scan_thread2.start()
        else:
            scan_thread2 = Thread(target=scanning, args=(semirange, rango1, rango2, save_filee, name_file_, timeout))
            scan_thread2.start()
    
    while scan_thread2.is_alive():
        pass
    time.sleep(4)
    t2 = datetime.now()
    total =  t2 - t1
    rainbow("Escaneo finalizado en " + str(total).split(".")[0] + "s")
    print("\n")
    salida = input(str(rainbow("[LinkScanner] Escaneo finalizado... Presiona enter para volver al menú")).replace("None", "")).split("-")
    print("\n")
    clear()
    main()

def range_scan_2(ip, rango1, rango2, save_filee, name_file_, timeout):
    for puerto in range(rango1,rango2+1):
        try:
            checked2 = Thread(target=scan_mc, args=(ip,puerto, save_filee, name_file_, timeout))
            checked2.start()
        except:
            scan_mc(ip,puerto,save_filee,name_file_,timeout)
            
def scan(ips, rango1, rango2, scan_save2, name_file, timeout):
    t1 = datetime.now()
    if type(rango1) == list:
        for ip in ips:
            for port_range in rango1:
                rango_1 = port_range.split("-")[0]
                rango_2 = port_range.split("-")[1]
                for puerto in range(int(rango_1),int(rango_2)+1):
                    scanning_mc = Thread(target=scan_mc, args=(ip,puerto, scan_save2, name_file, timeout))
                    scanning_mc.start()   
    else:
        for ip in ips:
            for puerto in range(rango1,rango2+1):
                scanning_mc = Thread(target=scan_mc, args=(ip,puerto, scan_save2, name_file, timeout))
                scanning_mc.start()
    time.sleep(1)
    scanning_mc.join()
    time.sleep(1)
    t2 = datetime.now()
    total =  t2 - t1
    rainbow("Escaneo finalizado en " + str(total).split(".")[0] + "s")
    print("\n")
    salida = input(str(rainbow("[LinkScanner] Escaneo finalizado... Presiona enter para volver al menú")).replace("None", "")).split("-")
    print("\n")
    clear()
    main()
    
def clear():
    os.system("cls" if os.name == 'nt' else 'clear')    
    
def getIpList(file):
    with open(file,"r") as f:
        file = f.readlines()
        files = [f.strip() for f in file]
        files = [x for x in files if x != '']
        return files
    
def is_a_timeout(timeout):
    if not timeout.isdigit():
        return False
    if int(timeout) < 0:
        return False
    return True
    
def is_a_port_range(port_range):
    if "." in port_range:
        ips = port_range.split(".")
        for ip in ips:
            if not "-" in ip:
                return False
        for ip in ips:
            ip_splited = ip.split("-")
            if len(ip_splited) != 2:
                return False
            if not ip_splited[0].isdigit() or not ip_splited[1].isdigit():
                return False
            if int(ip_splited[0]) < 1 or int(ip_splited[0]) > 65535 or int(ip_splited[1]) < 1 or int(ip_splited[1]) > 65535:
                return False
            if int(ip_splited[0]) >= int(ip_splited[1]):
                return False
        return True
        
    else:
        if not "-" in port_range:
            return False
        port_range_splited = port_range.split("-")
        if len(port_range_splited) != 2:
            return False
        if not port_range_splited[0].isdigit() or not port_range_splited[1].isdigit():
            return False
        if int(port_range_splited[0]) < 1 or int(port_range_splited[0]) > 65534 or int(port_range_splited[1]) < 1 or int(port_range_splited[1]) > 65535:
            return False
        if int(port_range_splited[0]) >= int(port_range_splited[1]):
            return False
        return True
    
def main():
    banner = """

                 _     _       _     ____                                  
                | |   (_)_ __ | | __/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
                | |   | | '_ \| |/ /\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
                | |___| | | | |   <  ___) | (_| (_| | | | | | | |  __/ |   
                |_____|_|_| |_|_|\_\|____/ \___\__,_|_| |_|_| |_|\___|_| v1.0  
                                                                        

    """

    rainbow(banner)
    rainbow("                Coded by SerLink04 #LinkSquad (discord.gg/comunidad)")
    print()
    print() 
    rainbow("                                 (1) Escanear ips")
    print("\n")
    rainbow("                                 (2) Escanear list ip")
    print("\n")
    rainbow("                                 (3) Escanear semirangos")
    print("\n\n")
    opt = input(str(rainbow("                        [LinkScanner] Selecciona una opción: ")).replace("None", ""))
    if opt == "1":
        print()
        ips = input(str(rainbow("[LinkScanner] Escribe las ips a escanear separadas por espacios: ")).replace("None", "")).split()
        if len(ips) == 0:
            print("No has introducido ninguna ip para escanear")
            salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
            clear()
            main()
        for ip in ips:
            if not is_an_ip(ip):
                print("Has introducido una o unas ips erróneas")
                salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                clear()
                main()
        print()
        opt_2 = input(str(rainbow("[LinkScanner] ¿Deseas guardar los resultados en un txt? s/n: ")).replace("None", "")).lower().strip()
        print()
        sis = ["y","yes","yup","yeah","s","si","sip"]
        if opt_2 in sis:
            scan_save_2 = True
            name_file = input(str(rainbow("[LinkScanner] Introduce el nombre al archivo (result_ip_scan.txt by default): ")).replace("None", "")).strip()
            if name_file == "":
                name_file = 'result_ip_scan.txt'
            else:
                if not name_file.endswith('.txt'):
                    name_file = name_file + '.txt'
                if " " in name_file:
                    name_file =  name_file.split()
                    name_file = "_".join(name_file)
            print()
        else:
            scan_save_2 = False
            name_file = False
        timeout = input(str(rainbow("[LinkScanner] Introduce un timeout (3 seconds by default): ")).replace("None", ""))
        if timeout.strip() == "":
            timeout = 3
        else:
            if not is_a_timeout(timeout):
                print("Has introducido un timeout incorrecto...")
                salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                clear()
                main()
            
        print()
        rangos = input(str(rainbow("[LinkScanner] Introduce el rango de puertos a escanear (Ej: 25530-25580): ")).replace("None", ""))
        if not is_a_port_range(rangos):
            print("Has introducido un rango de puertos incorrecto... Uso correcto: 25530-25580 o 25530-25580.25600-25650")
            salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
            clear()
            main()       
        print("Esto demorará unos momentos...")
        t1 = datetime.now()
        if "." in rangos:
            rango1 = rangos.split(".")
            rango2 = rango1
        else:    
            rangos = rangos.split("-")
            rango1 = int(rangos[0])
            rango2 = int(rangos[1])
        try:
            hilo = Thread(target=scan, args=(ips, rango1, rango2, scan_save_2, name_file, timeout))
            hilo.start()
        except:
            hilo = Thread(target=scan, args=(ips, rango1, rango2, scan_save_2, name_file, timeout))
            hilo.start()
        hilo.join()

    elif opt == "2":
        print()
        ips = input(str(rainbow("[LinkScanner] Introduce el directorio del archivo a escanear (ips.txt by default): ")).replace("None", "")).strip()
        if ips == "":
            file = "ips.txt"
        else:
            file = ips
            if not file.endswith('.txt'):
                file = file + '.txt'
            if " " in file:
                file =  file.split()
                file = "_".join(file)
        filee = open(file, "a")
        filee.close()
        lines = open(file, "r+")
        archivo = lines.readlines()
        archivo_striped = [x.strip() for x in archivo]
        if len(archivo_striped) == 0:
            print()
            rainbow("No hay ninguna ip establecida en el archivo")
            print()
            ips = input(str(rainbow("[LinkScanner] ¿Deseas establecer ips para escanear? y/n: ")).replace("None", "")).strip()
            sis = ["y","yes","yup","yeah","s","si","sip"]
            if ips.lower() in sis:
                print()
                versions = input(str(rainbow("[LinkScanner] Escribe las versiones para escanear entre comillas ('spigot 1.8.8' 'paperspigot'): ")).replace("None", "")).strip().split("'")
                versions = [x.strip() for x in versions]
                versions = [x for x in versions if x != '']
                versions = [x.replace(" ","-") for x in versions]
                print("Buscando ips relacionadas a esos parámetros y añadiéndolas a la lista...")
                api = Shodan('76uWNv0clygVHb8IzwYoPfWCw8MqCF8W')
                ips_to_scan = [] 
                count = 0
                for version in versions:
                    results = api.search(version)
                    for result in results['matches']:
                        ip = str(result['ip_str'])
                        ips_to_scan.append(ip)
                        count += 1
                for ip in ips_to_scan:
                    lines.write(f"\n{ip}")
                lines.close()
                print(Fore.CYAN +  f"Han sido agregadas {count} ips a la lista.")
                salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                clear()
                main()
                
            else:
                print()
                rainbow("Volviendo al menú...")
                time.sleep(1)
                lines.close()
                clear()
                main()
        else:
            print()
            sis = ["y","yes","yup","yeah","s","si","sip"]
            opt2 = input(str(rainbow("[LinkScanner] Se han detectado ips en el txt ¿Deseas revisar las ips antes del escaneo? s/n: ")).replace("None", "")).strip()
            if opt2.lower() in sis:
                ips = getIpList(file)
                count = 0
                for ip in ips:
                    rainbow("IP in the txt: " + ip + "\n")
                    count += 1
                print(Fore.CYAN + "IPS totales: " + Fore.LIGHTBLUE_EX + str(count))
            print()
            opt_2 = input(str(rainbow("[LinkScanner] ¿Deseas guardar los resultados en un txt? s/n: ")).replace("None", "")).strip()
            print()
            if opt_2 in sis:
                scan_save = True
                name_file = input(str(rainbow("[LinkScanner] Introduce el nombre al archivo (result.txt by default): ")).replace("None", "")).strip()
                print()
                if name_file.strip() == "":
                    name_file = 'result.txt'
                else:
                    if not name_file.endswith('.txt'):
                        name_file = name_file + '.txt'
                    if " " in name_file:
                        name_file = name_file.split()
                        name_file = "_".join(name_file)
            else:
                scan_save = False
                name_file = False
            sis = ["y","yes","yup","yeah","s","si","sip"]
            opt3 = input(str(rainbow("[LinkScanner] ¿Te gustaría agregar más ips para escanearlas? s/n: ")).replace("None", "")).strip()
            if opt3.lower() in sis:
                print()
                versions = input(str(rainbow("[LinkScanner] Escribe las versiones para escanear entre comillas ('spigot 1.8.8' 'paperspigot'): ")).replace("None", "")).strip().split("'")
                versions = [x.strip() for x in versions]
                versions = [x for x in versions if x != '']
                versions = [x.replace(" ","-") for x in versions]
                print("Buscando ips relacionadas a esos parámetros y añadiéndolas a la lista...")
                api = Shodan('76uWNv0clygVHb8IzwYoPfWCw8MqCF8W')
                ips_to_scan = [] 
                count = 0
                for version in versions:
                    results = api.search(version)
                    for result in results['matches']:
                        ip = str(result['ip_str'])
                        ips_to_scan.append(ip)
                        count += 1
                for ip in ips_to_scan:
                    lines.write(f"\n{ip}")
                lines.close()
                print(Fore.CYAN +  f"Han sido agregadas {count} ips a la lista.")
            print()
            timeout = input(str(rainbow("[LinkScanner] Introduce un timeout (3 seconds by default): ")).replace("None", ""))
            if timeout.strip() == "":
                timeout = 3
            else:
                if not is_a_timeout(timeout):
                    print("Has introducido un timeout incorrecto...")
                    salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                    clear()
                    main()
            print()
            rangos = input(str(rainbow("[LinkScanner] Introduce el rango de puertos a escanear (Ej: 25530-25580): ")).replace("None", ""))
            if not is_a_port_range(rangos):
                print("Has introducido un rango de puertos incorrecto... Uso correcto: 25530-25580 o 25530-25580.25600-25650")
                salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                clear()
                main()
            if "." in rangos:
                rango1 = rangos.split(".")
                rango2 = rango1
            else:    
                rangos = rangos.split("-")
                rango1 = int(rangos[0])
                rango2 = int(rangos[1])
            print()
            starting_scan = input(str(rainbow("[LinkScanner] ¿Deseas iniciar el escaneo? s/n: ")).replace("None", "")).strip()
            if starting_scan.lower() in sis:
                print("Esto demorará unos momentos...")
                try:
                    hilo = Thread(target=scan, args=(getIpList(file), rango1, rango2, scan_save, name_file, timeout))
                    hilo.start()
                except:
                    scan(getIpList(file), rango1, rango2, scan_save, name_file, timeout)
                hilo.join()
            else:
                print()
                print("Volviendo al menú principal...")
                time.sleep(1)
                clear()
                main()
                
    elif opt == "3":
        print()
        sies = ["y","yes","yup","yeah","s","si","sip"]
        rangos_to_scan = input(str(rainbow("[LinkScanner] Introduce los semirangos a escanear (Ej: 142.44.143.* 66.70.180.*): ")).replace("None", "")).split()
        if len(rangos_to_scan) == 0:
            print("No has introducido ningún semirango para escanear")
            salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
            clear()
            main()
        for semirangoo in rangos_to_scan:
            if is_a_semirange(semirangoo):
                pass
            else:
                print("Has introducido un o unos semirangos inválidos... (Uso correcto: 142.44.143.* 66.70.180.*)")
                salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                clear()
                main()
        print()
        option_2 = input(str(rainbow("[LinkScanner] ¿Deseas guardar los resultados en un txt? s/n: ")).replace("None", "")).lower().strip()
        print()
        if option_2 in sies:
            scan_save = True
            name_file = input(str(rainbow("[LinkScanner] Introduce el nombre al archivo (result_linkscanner.txt by default): ")).replace("None", "")).strip()
            print()
            if name_file == "":
                name_file = 'result_linkscanner.txt'
            else:
                if not name_file.endswith('.txt'):
                    name_file = name_file + '.txt'
                if " " in name_file:
                    name_file = name_file.split()
                    name_file = "_".join(name_file)
        else:
            scan_save = False
            name_file = False
        timeout = input(str(rainbow("[LinkScanner] Introduce un timeout (3 seconds by default): ")).replace("None", ""))
        if timeout.strip() == "":
            timeout = 3
        else:
            if not is_a_timeout(timeout):
                print("Has introducido un timeout incorrecto...")
                salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
                clear()
                main()
        print()
        ports_range = input(str(rainbow("[LinkScanner] Introduce un rango de puertos (Ej: 25530-25580): ")).replace("None", ""))
        if not is_a_port_range(ports_range):
            print("Has introducido un rango de puertos incorrecto... Uso correcto: 25530-25580 o 25530-25580.25600-25650")
            salida = input(str(rainbow("Presiona enter para volver al menú...")).replace("None", ""))
            clear()
            main()
        if "." in ports_range:
            rango1 = ports_range.split(".")
            rango2 = rango1
        else:    
            rangos = ports_range.split("-")
            rango1 = int(rangos[0])
            rango2 = int(rangos[1])
        print("Esto demorará unos momentos...")
        range_scan(rangos_to_scan, rango1, rango2, scan_save, name_file, timeout)

    else:
        print("\n")
        rainbow("                        [LinkScanner] Esa opción no existe...")
        print("\n")
        menu = input(Fore.WHITE + "                         Pulsa intro para volver al menú...")
        clear()
        main()
clear()
main()
