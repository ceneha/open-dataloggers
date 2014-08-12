# Este documento esta pensado para colocar en el los diferentes dataloggers
# junto con los comandos que se utiliza para obtener los datos
# Para esto se creara una lista con los diferentes comandos empezando por:
# comando para obtener datos en tiempo real
# comando para obtener todos los datos registrados(contenido del datalogger)

# LISTA DE EQUIPOS

#-----------------------------------------------------------------------
# Tipo = 1
# Campbell Scientific
# Datalogger CR1000
#-----------------------------------------------------------------------
# Comando '7' obtiene los datos en tiempo real
# Comando '8' obtiene los datos almacenados FLUX

def Uno():
    print 'Campbell CR1000'
    lista=["7","8"]
    return lista


#-----------------------------------------------------------------------
# Tipo = 2
# Stevens
# DOT Logger
#-----------------------------------------------------------------------

def Dos():
    print 'Stevens'
    lista=["CD", "DB"]
    return lista

#-----------------------------------------------------------------------

# FIN DE LISTA DE EQUIPOS

#-----------------------------------------------------------------------
# Funcion principal
#-----------------------------------------------------------------------

def obtenerComandos(tipo):
    if tipo == 1:
        l =Uno()
        return l
    elif tipo == 2:
        l=Dos()
        return l



