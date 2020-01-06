#!/bin/python3

import os
import sys
import pyperclip as pc
from cryptography.fernet import Fernet

def opcion1(key):
    os.system("clear")
    flag = False
    account = input("Ingrese nombre de cuenta: ")
    PSSWD = open('.passwd.txt')
    for line in PSSWD:
        line = line.strip().split()
        if account == line[0]:
            print("Error: cuenta existente.")
            flag = True
            break
    PSSWD.close()
    if flag != True:
        user = input("Ingrese nombre de usuario de la cuenta: ")
        PSSWD = open('.passwd.txt', 'a')
        passwd = input("Ingrese password: ")
        passwd = passwd.encode()
        f = Fernet(key)
        passwd = f.encrypt(passwd)
        passwd = passwd.decode()
        newLine = account + ' ' + user + ' ' + passwd + '\n'
        PSSWD.write(newLine)
        PSSWD.close()
    input("Pulsa enter para continuar.")
    inicio(key)

def opcion2(key):
    os.system("clear")
    print("Mostrando cuentas: ")
    PSSWD = open('.passwd.txt')
    for line in PSSWD:
        line = line.strip().split()
        print(line[0])
    input("Pulsa enter para continuar.")
    inicio(key)

def opcion3(key):
    #opcion de copiar usuario o password
    #opcion de seguir en la misma funcion o volver a inicio()
    os.system("clear")
    flag = False
    account = input("Cuenta: ")
    PSSWD = open('.passwd.txt')
    for line in PSSWD:
        line = line.strip().split()
        if account == line[0]:
            opcion = -1
            opcion = int(input("Copiar usuario (1) o password (2)? "))
            if opcion == 1:
                pc.copy(line[1])
                print("Usuario para cuenta " + account + " copiada al clipboard.")
                flag = True
            elif opcion == 2:
                passwd = line[2]
                passwd = passwd.encode()
                f = Fernet(key)
                passwd = f.decrypt(passwd)
                passwd = passwd.decode()
                pc.copy(passwd)
                print("Password para cuenta " + account + " copiada al clipboard.")
                flag = True
            else:
                input("Error: opcion incorrecta. Intente de nuevo...")
                opcion3(key)
    if flag != True:
        print("No existe la cuenta " + account)
    input("Pulsa enter para continuar.")
    inicio(key)

def opcion4(key):
    os.system("clear")
    account = input("Cuenta a eliminar: ")
    #TODO: verificar password de cuenta antes de eliminarla
    #passwd = input("Ingrese la password de esa cuenta: ")
    with open('.passwd.txt', 'r+') as PSSWD:
        new_PSSWD = PSSWD.readlines()
        PSSWD.seek(0)
        for line in new_PSSWD:
            line2 = line
            line2 = line.strip().split()
            if account != line2[0]:
                PSSWD.write(line)
        PSSWD.truncate()
        print("Cuenta " + account + " eliminada con exito.")
    input("Pulsa enter para continuar.")
    inicio(key)

def opcion5():
    os.system("clear")
    sys.exit()

def inicio(key):
    os.system("clear")
    print("Inicio.")
    print("Selecciona una opcion:")
    print("1: agregar cuenta.")
    print("2: ver cuentas.")
    print("3: copiar password.")
    print("4: borrar cuenta.")
    print("5: salir.")
    opcion = input("Opcion: ")

    if opcion == '1':
        opcion1(key)

    elif opcion == '2':
        opcion2(key)

    elif opcion == '3':
        opcion3(key)

    elif opcion == '4':
        opcion4(key)

    elif opcion == '5':
        opcion5()
    
    else:
        inicio(key)


if __name__ == "__main__":
    if os.stat('.keys.key').st_size == 0:
        KEY = Fernet.generate_key()
        file = open('.keys.key', 'wb')
        file.write(KEY)
        file.close()
        inicio(KEY)
    else:
        file = open('.keys.key', 'rb')
        KEY = file.read()
        file.close()
        inicio(KEY)
        
