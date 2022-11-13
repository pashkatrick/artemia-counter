from OBJETO_ARTEMIAS import motor    
from time import sleep
import time

def matrix_motion (tipo_pozo,tiempo_foto,check_pozo):
    
    # check_pozo:
    # array de bools de los pozos
    # 0: no seleccionado (no se toma foto)
    # 1: seleccionado (sí se toma foto)
    
    mot_y = motor(19,26,17,3200,0)
    mot_x = motor(12,21,23,3200,1)
    
    mot_x.set_vel_max(2)
    mot_x.set_acel(15)
    mot_x.set_rango(0,11.8)
    mot_y.set_vel_max(2)
    mot_y.set_acel(15)
    mot_y.set_rango(-10.5,0)
    
    if tipo_pozo == 1:
        dis_init_x = 1.75
        dis_init_y = -1
        num_x = 2
        num_y = 3
        dist_pozos = 3.75
    elif tipo_pozo == 2:
        dis_init_x = 0.5
        dis_init_y = -0.3
        num_x = 4
        num_y = 6
        dist_pozos = 1.93
    elif tipo_pozo == 3:
        dis_init_x = 0.5
        dis_init_y = -0.275
        num_x = 4
        num_y = 6
        dist_pozos = 1.93


    mot_x.set_motor()
    mot_y.set_motor()

    
    """
    
    mot_x.run_distance(5)
    mot_x.run_distance(10)
    mot_x.run_distance(1)
    mot_x.run_position(2)
    
    mot_y.run_distance(-5)
    mot_y.run_distance(7)
    mot_y.run_distance(-1)
    mot_y.run_position(-2)
    """
    #mot_x.run_distance(dis_init_x)
    #mot_y.run_distance(dis_init_y)
    
    i = 0
    j = 0
    
    while j < num_y:
        mot_y.run_position(-j*dist_pozos + dis_init_y)
        
        while i < num_x:
            # (i+1)-1=i so it starts in 0
            if check_pozo[2*(j)+i] == True:   
                mot_x.run_position(i*dist_pozos + dis_init_x)
                
                # viewed from the front
                # yellow strip looking north
                # from top to botoom, left to right (no U shape)
                # in normal coords (3x4):
                # A4, B4, C4, A3, B3, C3, A2, etc
                # i+1: column
                # j+1: row
                print("tomando foto: ",i+1," ",j+1)
                
                # cmd: take picture
                
                time.sleep(tiempo_foto)
            i = i + 1
            
        j = j + 1
        i = 0
    
    mot_x.set_motor()
    mot_y.set_motor()

#matrix = [1,0,0,0,0,0] 
#matrix_motion(1,5,matrix)