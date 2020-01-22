#!/bin/python3

"""
Script para almacenar cuentas.
Opcion de copiar nombre de cuenta y clave al clipboard.

TODO: crear una GUI.

"""

import os
import sys
import pyperclip as pc
from cryptography.fernet import Fernet
from getpass import getpass

def opcion1(key):
    os.system("clear")
    flag = False
    psFlag = False
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
        passwd = getpass("Ingrese password:")
        passwd2 = getpass("Ingrese de nuevo su password:")
        if passwd == passwd2:
            passwd = passwd.encode()
            f = Fernet(key)
            passwd = f.encrypt(passwd)
            passwd = passwd.decode()
            psFlag = True
        else:
            input("Error: passwords no coinciden. Intente de nuevo...")
            opcion1(key)
        if psFlag:
            newLine = account + ' ' + user + ' ' + passwd + '\n'
            PSSWD.write(newLine)
        PSSWD.close()
        print(f'Cuenta {account} creada con exito.')
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
                print(f'Usuario para cuenta {account} copiada al clipboard.')
                flag = True
            elif opcion == 2:
                passwd = line[2]
                passwd = passwd.encode()
                f = Fernet(key)
                passwd = f.decrypt(passwd)
                passwd = passwd.decode()
                pc.copy(passwd)
                print(f'Password para cuenta {account} copiada al clipboard.')
                flag = True
            else:
                input("Error: opcion incorrecta. Intente de nuevo...")
                opcion3(key)
    if flag != True:
        print(f'Error: no existe la cuenta {account}')
    input("Pulsa enter para continuar.")
    inicio(key)

def opcion4(key):
    os.system("clear")
    flag = False
    account = input("Cuenta a eliminar: ")
    verification = input(f'Seguro que quiere eliminar la cuenta {account}? [y/n]: ')
    if verification == 'n':
        input("Pulse enter para continuar.")
        inicio(key)
    #TODO: verificar password de cuenta antes de eliminarla
    passwdInput = getpass("Ingrese la password de esa cuenta:")
    with open('.passwd.txt', 'r+') as PSSWD:
        new_PSSWD = PSSWD.readlines()
        PSSWD.seek(0)
        for line in new_PSSWD:
            line2 = line.strip().split()
            if line2[0] == account:
                passwdAc = line2[2]
                passwdAc = passwdAc.encode()
                f = Fernet(key)
                passwdAc = f.decrypt(passwdAc)
                passwdAc = passwdAc.decode()
                if (passwdInput == passwdAc):
                    flag = True
                    break
                else:
                    break
        PSSWD.close()
        if flag and verification == 'y':
            with open('.passwd.txt', 'r+') as PSSWD:
                new_PSSWD2 = PSSWD.readlines()
                PSSWD.seek(0)
                for line in new_PSSWD2:
                    line2 = line.strip().split()
                    if account != line2[0]:
                        PSSWD.write(line)
                PSSWD.truncate()
                print(f'Cuenta {account} eliminada con exito.')
        else:
            print("Error: password incorrecta. Intente de nuevo...")
    input("Pulsa enter para continuar.")
    inicio(key)

def opcion5():
    os.system("clear")
    sys.exit()

def inicio(key):
    os.system("clear")
    print("Inicio.")
    print("Seleccione una opcion:")
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
        