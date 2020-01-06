# PsswdLckr
Manager de contraseñas, almacenadas en un archivo de texto oculto en una carpeta privada. 

Las contraseñas se almacenan encriptadas usando encriptación simétrica (módulo Fernet), y la respectiva llave se guarda en otro archivo de texto oculto.

La principal función del script es poder copiar la contraseña de una determinada cuenta al clipboard para facilitar el inicio de sesión, sin necesidad de tener que ver o acordarse de la contraseña. Para ello, el script se encarga de desencriptar la contraseña almacenada y copiarla al clipboard. También se puede copiar el nombre de usuario.
El script permite también agregar cuentas (nombre de usuario y contraseña), ver las cuentas existentes y borrar cuentas.
