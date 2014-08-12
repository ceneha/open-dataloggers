import serial
from datetime import*
import time
import equipos
import sys
import logging


class Datalogger():

     #defino elemento de loggeo de python
    logging.basicConfig(filename='/../log/syslog.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    comandoRt=" "
    comandoDatos=" "

    # Metodo llamado despues de crear el objeto para realizar tareas de inicializacion
    def __init__(self, port, baudrate, parity, rtscts, xonxoff, tipo):
        try:
            # define los parametros para la conexion, los parametros los recibe cuando se crea el objeto
            self.serial = serial.Serial(port, baudrate, parity=parity, rtscts=rtscts, xonxoff=xonxoff)
            # bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE por defecto en la libreria serial
            # el parametro tipo se utiliza para elegir el tipo de datalogger con el que se quiere trabajar
            # ver equipos.py para ver los equipos cargados
        except serial.serialutil.SerialException:
            logging.error("No se pudo crear instancia clase datalogger")
            #sys.stderr.write("No se pudo crear instancia clase datalogger")
            sys.exit(1)
        lista=equipos.obtenerComandos(tipo)
        global comandoRt
        global comandoDatos
        comandoRt=lista[0]
        comandoDatos=lista[1]
        #print 'comando tiempo real'+' '+comandoRt
        #print 'comando todos los datos'+' '+comandoDatos

    # Inicia la comunicacion a traves del puerto serie
    def start_conexion(self):
        try:
            self.serial.open()
        except self.serial.SerialException, e:
            logging.error("No se puedo abrir el puerto %s: %s\n" % (self.serial.portstr, e))
            #sys.stderr.write("No se puedo abrir el puerto %s: %s\n" % (self.serial.portstr, e))
            sys.exit(1)
        logging.info("Comunicacion Iniciada")

    # Finaliza la comunicacion
    def close_conexion(self):
        self.serial.close()
        logging.info("Comunicacion Finalizada")

    # Permite cambiar el puerto y la velocidad de la comunicacion
    def set_parameters(self,port, baudrate):
        self.serial = serial.Serial(port, baudrate)
        logging.info("Cambio de los parametros de la comunicacion")


    # Devuelve por pantalla los datos en tiempo real de equipo
    def get_data_rt(self):
        logging.info("Inicio Obtencion tiempo real")
        # mientras el otro extremo de la conexion no responda mandamos ENTER
        while self.serial.inWaiting() == 0:
            self.serial.write('\r\n')
            time.sleep(1)
        # enviamos en numero 7 para que el datalogger nos devuelva los datos actuales
        self.serial.write(comandoRt+'\r\n')
        out = ''
        # se espera un segundo antes de leer la salida
        time.sleep(1)
        while self.serial.inWaiting() > 0:
            out += self.serial.read(1)
        if out != '':
            print ">>  Datos en tiempo real:"
            print ">>" + out
       #self.serial.write('\r\n')


    ## Realiza la interregacion del datalogger cada TIEMPO y lo va almacenando en archivos
    ## Campo muestraspseg es la cantidad de muestras por segundo
    ## 1 =1/seg 2=2/seg 3=3/seg 4=4/seg 5=5/seg 6=6/seg 7=7/seg 8=8/seg(maximo posible)
    ## luego se le pasan D,M,H los cuales indican la duracion de la funcion
    ## por ultimo se le pasa los minutos, que indican cada cuanto se cambia de archivo

    def get_auto_data_rt(self,dias,horas,minutos,muestraspseg,minDuraFile,pathFile):
       # dependiendo la cantidad de muestras saco el tiempo de espera
        logging.info("Inicio Captura tiempo real")
        muestraspseg=float(muestraspseg)
        dias=int(dias)
        horas=int(horas)
        minutos=int(minutos)
        minDuraFile=int(minDuraFile)
        tiempo = round(1.0/muestraspseg,3) # // division con resultado redondeado
        while self.serial.inWaiting() == 0:
            self.serial.write('\r\n')
            time.sleep(1)
        # tomo la fecha y hora de arranque
        fhInicio=(datetime.today())
        restaDias=0
        restaHoras=0
        restaMinutos=0
        # este ciclo es el que controla la cantidad de tiempo que dura la ejecucion de la funcion
        while not((restaDias == dias) and (restaHoras == horas) and (restaMinutos == minutos)):
            # tomo fecha y hora actual para controlar la duracion de la funcion
            fhActual=(datetime.today())
            # se crea el archivo
            nombreArchi=str(fhActual)
            try:
                 f = open(pathFile+nombreArchi+".raw", "w")
            except IOError:
                logging.error("No se pudo crear el archivo Metodo Captura Tiempo Real")
            # pone en cero la variable
            restaMinutos2=0
            out=''
            while self.serial.inWaiting() == 0:
                self.serial.write('\r\n')
                time.sleep(1)
            # este segundo ciclo controla la duracion de cada archivo de consulta(mediante tiempo)
            while not(restaMinutos2 == minDuraFile):
                # tomo fecha y hora actual para controlar la duracion del archivo
                fhActual2=(datetime.today())
                # -------se realiza la consulta al datalogger--------
                self.serial.write(comandoRt+'\r\n')
                # se espera- tiempo- antes de leer la salida
                time.sleep(tiempo)
                # devuelve la cantidad de chars en el buffer
                # lee esa cantidad de caracteres
                cantChar=int(self.serial.inWaiting())
                if (cantChar > 0):
                    out = self.serial.read(cantChar)
                    #print out
                # cada consulta se agrega al archivo
                if out != '':
                    f.write("Fecha_y_Hora:" + str(fhActual2))
                    f.write(out)
               # se limpian los buffer de la comunicacion serie
                self.serial.flush()
                self.serial.flushInput()
                self.serial.flushOutput()
                #--------------        --------------------
                # control segundo ciclo
                # realizo la resta de la fecha actual y la inicial, devuelve un objeto timedelta
                resta2=fhActual2-fhActual
                restaMinutos2 = int(resta2.seconds // 60 % 60)
            # cuando se cumple el tiempo de duracion del archivo se cierra
            f.close()
            # control primer ciclo
            # realizo la resta de la fecha actual y la inicial, devuelve un objeto timedelta
            fhActual3=(datetime.today())
            resta=fhActual3-fhInicio
            # del objeto saco los dias, las horas y los minutos, estos se encuentran en segundos
            restaDias= int(resta.days)
            restaHoras=int(resta.seconds // 3600)
            restaMinutos=int(resta.seconds // 60 % 60)

    def get_datalogger_data(self,pathFile): 
	logging.info("Inicio Obtencion Flux")                                                                                           
        while self.serial.inWaiting() == 0:                                                                                             
            self.serial.write('\r\n')                                                                                                   
            time.sleep(1)                                                                                                               
        # se crea el archivo con la fecha y hora                                                                                        
        fhActual=(str(datetime.today()))                                                                     
        # le manda el caracter 8 para obtener las talbas almacenadas en el datalogger                    
        self.serial.write(comandoDatos+'\r\n')                                                           
        out= ''                                                                                       
        # se espera un segundo antes de leer la salida                  
        time.sleep(1)                                                                   
        # luego almacena en out todo lo que le devuelve el datalogger                       

        # devuelve la cantidad de chars en el buffer                                        
        # lee esa cantidad de caracteres                                                    
        cantChar=int(self.serial.inWaiting())                                               
        if (cantChar > 0):                                                                  
            out = self.serial.read(cantChar)        
        if (out != '') & ("flux" in out ):
	    try:                                                                                                                                                  
               f = open(pathFile+"flux"+fhActual+".raw", "w")                                                                                                    
            except IOError:                                                                                                                                       
               logging.error("No se pudo crear el archivo Metodo Obtencion Flux")   
            while (out != ''):                                                                                         
                if("ts_data" in out):
                    f.write(out) 
                    logging.info("Llego un ts_data")   
                    break
                else:
                    f.write(out)
                # se envian un par de enter para obtener respuesta del datalogger                                
                while self.serial.inWaiting() == 0:                                                              
                    self.serial.write('\r\n')                                                                    
                    time.sleep(1)                                                                             
                #le manda el caracter 8 para obtener las talbas almacenadas en el datalogger                    
                self.serial.write(comandoDatos+'\r\n')                                                           
                #se espera un segundo antes de leer la salida                  
                time.sleep(1)                                                                   
                # luego almacena en out todo lo que le devuelve el datalogger                       
                # devuelve la cantidad de chars en el buffer                                        
                # lee esa cantidad de caracteres                                                    
                cantChar=int(self.serial.inWaiting())                                               
                if (cantChar > 0):                                                                  
                    out = self.serial.read(cantChar)          
            self.serial.flush()                                                                 
            self.serial.flushInput()                                                            
            self.serial.flushOutput()                     
            f.close()   
        else:
            logging.info("No hay flux para extraer") 
