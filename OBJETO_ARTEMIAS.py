from time import sleep
import time
import numpy as np
import RPi.GPIO as GPIO

#def movimiento(distancia, sentido_giro, fin_pos, PUL, DIR, fin_carr, pasos_vuelta, modo_fun):

class motor:
    pass
    def __init__(self, PUL, DIR, fin_carr, pasos_vuelta, fin_pos):
        self.PUL = PUL
        self.DIR = DIR
        self.fin_carr = fin_carr
        self.pasos_vuelta = 2*pasos_vuelta #correccion por como funiona el codigo
        self.fin_pos = fin_pos
        
        self.cont_pasos_global = 0
        self.pos_actual = 0
        
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(fin_carr, GPIO.IN)
        GPIO.setup(PUL, GPIO.OUT)
        GPIO.setup(DIR, GPIO.OUT)
            
    def set_vel_max(self,velocidad):
        self.velocidad = velocidad * self.pasos_vuelta / 0.8;
        
    def set_acel(self,aceleracion):
        self.aceleracion = aceleracion * self.pasos_vuelta / 0.8;
        
    def set_rango(self,pos_min,pos_max):
        self.pos_min = pos_min
        self.pos_max = pos_max
    
    def run_distance(self,distancia):
        
        posicion = self.pos_actual + distancia
        print("valor de nueva posicion: ", posicion)     
        if posicion > self.pos_max or posicion < self.pos_min:
            print("movimiento invalido: fuera de rango...")
            return
        
        if distancia < 0:
            aux_sentido = -1
            GPIO.output(self.DIR, GPIO.HIGH)
        else:
            GPIO.output(self.DIR, GPIO.LOW)
            aux_sentido = 1
        distancia = abs(distancia)
        
        Pasos_totales = round(distancia*self.pasos_vuelta/0.8) # Se obtiene a partir de la posicion a la que se quiere llevar el carro (mas tarde lo acomodo asi too bonito :"v# )
        paso_corte = round(self.velocidad * self.velocidad / (2 * self.aceleracion))#paso en el cual debe cesar la self.aceleracioneración
        t_min = np.sqrt(2000000000000 * (paso_corte) / self.aceleracion) - np.sqrt(2000000000000 * (paso_corte - 1) / self.aceleracion)
        t_min = t_min*1000 #delay en etapa de self.velocidadocidad constante
        delay = np.zeros(paso_corte)#definicion del array del tamaño adecuado. 
        i=1
        
        while i < paso_corte:#calculo de los tiempos para cada paso en self.aceleracioneración.
            delay [i] = 1000000000*(np.sqrt(2 * i / self.aceleracion) - np.sqrt(2 * (i-1) / self.aceleracion))
            i=i+1
        i=0
        while i < paso_corte-1:#acomodo del array
            delay [i] = delay [i+1]
            i=i+1

        delay [paso_corte-1] = t_min
        #MOVIMIENTO DEL SISTEMA:
        i = 0
        pin_step = True # estado que generara la onda cuadrada necesaria para mover el motor
        #modo de valor de posicion final fijo       
        if paso_corte > Pasos_totales/2:
            paso_corte = (Pasos_totales/2)
            print("paso corte cambiado")  
        tiempo_siguiente = 0
        tiempo_inicio = time.time_ns()
        while True:        
            delta_tiempo = time.time_ns()
            delta_tiempo = delta_tiempo - tiempo_inicio        
            if delta_tiempo >= tiempo_siguiente:
                if paso_corte > i:
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    tiempo_siguiente = tiempo_siguiente + delay[i]
                    i = i + 1
                elif Pasos_totales - paso_corte < i:
                    #print(Pasos_totales + paso_corte - i)
                    tiempo_siguiente = tiempo_siguiente + delay[Pasos_totales - i]
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    i = i + 1
                else:
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    tiempo_siguiente = tiempo_siguiente + t_min
                    i = i + 1
            if i >= Pasos_totales:
                modo_fun = 2
                print("pasos totales: ",Pasos_totales)
                print("pasos efectados: ",i)
                self.cont_pasos_global = self.cont_pasos_global + aux_sentido*i
                
                self.pos_actual = 0.8*self.cont_pasos_global/self.pasos_vuelta
                print("posicion actual: ", self.pos_actual)
                i = 0
                Pasos_totales = -1
                break
    
    def run_position(self,posicion):
        
        distancia = posicion - self.pos_actual
        #print("valor de nueva posicion: ", posicion)  
        if posicion > self.pos_max or posicion < self.pos_min:
            print("movimiento invalido: fuera de rango...")
            return
        
        if distancia < 0:
            aux_sentido = -1
            GPIO.output(self.DIR, GPIO.HIGH)
        else:
            GPIO.output(self.DIR, GPIO.LOW)
            aux_sentido = 1  
        distancia = abs(distancia)
     
        Pasos_totales = round(distancia*self.pasos_vuelta/0.8) # Se obtiene a partir de la posicion a la que se quiere llevar el carro (mas tarde lo acomodo asi too bonito :"v# )
        paso_corte = round(self.velocidad * self.velocidad / (2 * self.aceleracion))#paso en el cual debe cesar la self.aceleracioneración
        t_min = np.sqrt(2000000000000 * (paso_corte) / self.aceleracion) - np.sqrt(2000000000000 * (paso_corte - 1) / self.aceleracion)
        t_min = t_min*1000 #delay en etapa de self.velocidadocidad constante
        delay = np.zeros(paso_corte)#definicion del array del tamaño adecuado. 
        i=1
        
        while i < paso_corte:#calculo de los tiempos para cada paso en self.aceleracioneración.
            delay [i] = 1000000000*(np.sqrt(2 * i / self.aceleracion) - np.sqrt(2 * (i-1) / self.aceleracion))
            i=i+1
        i=0
        while i < paso_corte-1:#acomodo del array
            delay [i] = delay [i+1]
            i=i+1
        delay [paso_corte-1] = t_min
        #MOVIMIENTO DEL SISTEMA:
        i = 0
        pin_step = True # estado que generara la onda cuadrada necesaria para mover el motor
        #modo de valor de posicion final fijo       
        if paso_corte > Pasos_totales/2:
            paso_corte = (Pasos_totales/2)
            print("paso corte cambiado")  
        tiempo_siguiente = 0
        tiempo_inicio = time.time_ns()
        while True:        
            delta_tiempo = time.time_ns()
            delta_tiempo = delta_tiempo - tiempo_inicio        
            if delta_tiempo >= tiempo_siguiente:
                if paso_corte > i:
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    tiempo_siguiente = tiempo_siguiente + delay[i]
                    i = i + 1
                elif Pasos_totales - paso_corte < i:
                    #print(Pasos_totales + paso_corte - i)
                    tiempo_siguiente = tiempo_siguiente + delay[Pasos_totales - i]
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    i = i + 1
                else:
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    tiempo_siguiente = tiempo_siguiente + t_min
                    i = i + 1
            if i >= Pasos_totales:
                modo_fun = 2
                self.cont_pasos_global = self.cont_pasos_global + aux_sentido*i
                self.pos_actual = 0.8*self.cont_pasos_global/self.pasos_vuelta
                """
                print("pasos totales: ",Pasos_totales)
                print("pasos efectados: ",i)
                print("posicion actual: ", self.pos_actual)
                """
                
                i = 0
                Pasos_totales = -1
                break
    
    
    def set_motor(self):
        
        paso_corte = round(self.velocidad * self.velocidad / (2 * self.aceleracion))#paso en el cual debe cesar la self.aceleracioneración
        t_min = np.sqrt(2000000000000 * (paso_corte) / self.aceleracion) - np.sqrt(2000000000000 * (paso_corte - 1) / self.aceleracion)
        t_min = t_min*1000 #delay en etapa de self.velocidadocidad constante
        delay = np.zeros(paso_corte)#definicion del array del tamaño adecuado.  
        i=1
        while i < paso_corte:#calculo de los tiempos para cada paso en self.aceleracioneración.
            delay [i] = 1000000000*(np.sqrt(2 * i / self.aceleracion) - np.sqrt(2 * (i-1) / self.aceleracion))
            i=i+1
        i=0
        while i < paso_corte-1:#acomodo del array
            delay [i] = delay [i+1]
            i=i+1
        delay [paso_corte-1] = t_min
        #MOVIMIENTO DEL SISTEMA:
        i = 0
        pin_step = True # estado que generara la onda cuadrada necesaria para mover el motor
        #crea una variable booleana, luego definela como true o false para luego simplemente sura var or !var, y arreglao
        pos_final_carr = True
        if self.fin_pos == 1:
            pos_final_carr = True
        elif self.fin_pos == 0:
            pos_final_carr = False  
        GPIO.output(self.DIR, pos_final_carr)#low indica ATRAS
        tiempo_siguiente = 0
        tiempo_inicio = time.time_ns()
        #ETAPA DE 1ER ACERCAMIENTO AL FINAL DE CARRERA
        while True:
            delta_tiempo = time.time_ns()
            delta_tiempo = delta_tiempo - tiempo_inicio
            
            if delta_tiempo >= tiempo_siguiente:
                if paso_corte > i:
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    tiempo_siguiente = tiempo_siguiente + delay[i]
                    i = i + 1
                else:
                    GPIO.output(self.PUL, pin_step)
                    pin_step = not pin_step
                    tiempo_siguiente = tiempo_siguiente + t_min
                    i = i + 1
            if GPIO.input(self.fin_carr) == 1:
                break
        #alejamiento del final de carrera
        GPIO.output(self.DIR, not pos_final_carr) # NOS ALEJAMOS DEL FINAL DE CARRERA
        i = 0
        tiempo_siguiente = 0
        tiempo_inicio = time.time_ns()    
        while i <= self.pasos_vuelta:
            delta_tiempo = time.time_ns()
            delta_tiempo = delta_tiempo - tiempo_inicio        
            if delta_tiempo >= tiempo_siguiente:
                GPIO.output(self.PUL, pin_step)
                pin_step = not pin_step
                tiempo_siguiente = tiempo_siguiente + 2*t_min
                i = i + 1
        #ACERCAMIOENTOLENTO Y PRECISO HACIA EL FINAL DE CARRERA
        GPIO.output(self.DIR, pos_final_carr)
        i = 0
        tiempo_siguiente = 0
        tiempo_inicio = time.time_ns()
        while True:
            delta_tiempo = time.time_ns()
            delta_tiempo = delta_tiempo - tiempo_inicio        
            if delta_tiempo >= tiempo_siguiente:
                GPIO.output(self.PUL, pin_step)
                pin_step = not pin_step
                tiempo_siguiente = tiempo_siguiente + 4*t_min
                i = i + 1
            if GPIO.input(self.fin_carr) == 1:
                break
        self.cont_pasos_global = 0
        self.pos_actual = 0
        #print("fin del seteo")
    