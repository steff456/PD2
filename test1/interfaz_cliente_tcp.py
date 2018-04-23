import tkinter as tk
# from cliente_tcp import *
import threading
import math
import sys
"""
Interfaz del cliente para manejar las interacciones del usuario.
"""
class Application(tk.Frame):
    """
    Esta clase genera una interfaz
    """
    def __init__(self, master=None):
        """
        Constructor
        """
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Crea todos los elementos de la ventana
        """
        self.descargando = 0
        self.conexion = 0

        self.lbip = tk.Label(self, text="Hoja")
        self.lbip.grid(row=0, column=0)

        self.txip = tk.Entry(self)
        self.txip.grid(row=0, column=1)

        self.lbport = tk.Label(self, text="PORT")
        self.lbport.grid(row=0, column=2)

        self.txport = tk.Entry(self)
        self.txport.grid(row=0, column=3)

        self.btpleth = tk.Button(self, text="Pleth", command=self.let_the_magic_work_pleth)
        self.btpleth.grid(row=0, column=4)

        self.btSpO2 = tk.Button(self, text="SpO2", command=self.let_the_magic_work_SO2)
        self.btSpO2.grid(row = 1, column=4)

        self.listBoxLista = tk.Listbox(self, selectmode="SINGLE")
        self.listBoxLista.grid(row=2,column=1, columnspan=2,  sticky=tk.W+tk.E)

        self.btdescargar = tk.Button(self, text="Descargar", command=self.descargarArchivo)
        self.btdescargar.grid(row = 2, column=3, sticky = tk.S)

        self.sdetener = tk.StringVar()
        self.sdetener.set("-")
        self.btdetener = tk.Button(self, textvariable=self.sdetener, command=self.cambiarDescarga)
        self.btdetener.grid(row = 2, column=4, sticky = tk.S)

        self.sconexion = tk.StringVar()
        self.sconexion.set("No conectado")
        self.lbconexion = tk.Label(self,textvariable=self.sconexion)
        self.lbconexion.grid(row=3, column=3, columnspan = 2, sticky = tk.W+tk.E)

        self.s = tk.StringVar()
        self.lbporcentaje = tk.Label(self, textvariable=self.s)
        self.lbporcentaje.grid(row = 3, column=1, columnspan=2, sticky=tk.W+tk.E)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.terminar)
        self.quit.grid(row=4, column=2)

    
    # Calculate the Pleth
    def let_the_magic_work_pleth(self):
        import scipy.io as sio
        import matplotlib.pyplot as plt
        import numpy as np
        import csv
        file = csv.DictReader(open(self), delimiter=",")
        v_pleth = []
        for row in file:
            if row[file.fieldnames[1]]=='MDC_PULS_OXIM_PLETH':
                n_value = row[file.fieldnames[4]]
                v_pleth.append(float(n_value))

        # return v_pleth
        plt.plot(v_pleth)
        plt.show()

    def let_the_magic_work_SO2(self):
        import scipy.io as sio
        import matplotlib.pyplot as plt
        import numpy as np
        import csv
    
        file = csv.DictReader(open(self), delimiter=",")
        # lets do this for Heart Rate
        # 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
        v_SO2 = []
        for row in file:
            if row[file.fieldnames[1]]=='NONIN_SPO2_8BEAT':
                n_value = row[file.fieldnames[4]]
                v_SO2.append(float(n_value))

        plt.plot(v_pleth)
        plt.show()
        # return v_SO2
    def conectar(self):
        """
        Llama la funcion conectar del cliente. Inicia el estado de la conexion.
        """
        conexion_con_servidor(self, self.txip.get(), int(self.txport.get()))
        self.mostrarConexion()
        thread_timeout=threading.Thread(target=timeoutCliente, args=(self,))
        thread_timeout.start()

    def actualizarLista(self, lista):
        """
        Actualiza la lista de archivos.
        """
        self.lista = lista
        self.listBoxLista.delete(0,tk.END)
        for l in self.lista:
            self.listBoxLista.insert(tk.END, l[1:-1])

    def descargarArchivo(self):
        """
        Llama la funcion descargar del cliente. Inicia el estado "descargando"
        """
        seleccionado = self.listBoxLista.get(self.listBoxLista.curselection())
        thread_archivo=threading.Thread(target=pedir_archivo, args=(self,seleccionado,))
        thread_archivo.start()
        self.cambiarDescarga()

    def mostrarConexion(self):
        """
        Cambia el estado de la conexion y lo muestra.
        """
        if self.conexion:
            self.conexion = 0
            self.sconexion.set("Desconectado")
        else:
            self.conexion =  1
            self.sconexion.set("Conectado")

    def estaConectado(self):
        """
        Retorna el estado de la conexion.
        """
        return self.conexion

    def actualizarProgreso(self,progreso):
        """
        Actualiza el porcentaje de progreso de la descarga.
        """
        self.s.set('Progreso: {}%'.format(math.ceil(progreso)))

    def cambiarDescarga(self):
        """
        Detiene la descarga cambiando el estado y mostrandolo.
        """
        if self.descargando:
            self.sdetener.set("Reanudar")
            self.descargando=0
        else:
            self.sdetener.set("Detener")
            self.descargando=1

    def estaDescargando(self):
        """
        Retorna si se esta descargando actualmente o no.
        """
        return self.descargando

    def mensajeEmergente(self, mensaje):
        win = tk.Toplevel()
        win.wm_title("Tiempo transcurrido")
        lbtiempo = tk.Label(win,text=mensaje)
        lbtiempo.grid(row=0, column=0)
        quit = tk.Button(win, text="Close", fg="red",
                              command=win.destroy)
        quit.grid(row=2, column=0)

    def terminar(self):
        cerrarConexion(self)
        root.destroy()

    def finalizarDescarga(self):
        self.sdetener.set("-")
        self.descargando=0

if __name__ == '__main__':
    """
    Si se llama este metodo, se crea la interfaz con la clase Application y se inicia
    """
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    threading.join(1)

# Calculate the Pleth
def let_the_magic_work_pleth(my_file):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import csv
    file = csv.DictReader(open(my_file), delimiter=",")
    v_pleth = []
    for row in file:
        if row[file.fieldnames[1]]=='MDC_PULS_OXIM_PLETH':
            n_value = row[file.fieldnames[4]]
            v_pleth.append(float(n_value))

    return v_pleth

# Calculate the Heart Rate
def let_the_magic_work_HR(my_file):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import csv
    file = csv.DictReader(open(my_file), delimiter=",")
    # lets do this for Heart Rate
    # 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
    v_heartrate = []
    for row in file:
        if row[file.fieldnames[1]]=='NONIN_HR_8BEAT_FOR_DISPLAY':
            n_value = row[file.fieldnames[4]]
            v_heartrate.append(float(n_value))

    return v_heartrate

# Calculate the Cardiac Output
def let_the_magic_work_CO(my_file, v_heartrate):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import csv
    from detect_peaks import detect_peaks
    from findpeaks import compute_peak_prominence

    Z_ao = 0.14

    file = csv.DictReader(open(my_file), delimiter=",")
    v_values = []
    for row in file:
        if row[file.fieldnames[1]]=='MDC_PULS_OXIM_PLETH':
            n_value = row[file.fieldnames[4]]
            v_values.append(float(n_value))

    v_values = list(map(lambda k: k - min(v_values), v_values))
    x = np.array(range(0,len(v_values)))
    ind = detect_peaks(v_values)
    prominence = compute_peak_prominence(v_values, ind)

    lk_high = []
    lk_down = []

    for kk in range(len(prominence)):
        p = prominence[kk]
        if p > 0.1:
            lk_high.append(ind[kk])
        elif p < 0.1:
            lk_down.append(ind[kk])

    cardiacO = []
    n_area = []
    HR = np.mean(v_heartrate)

    for idw in range(len(lk_down)-1):
        if lk_down[idw] < lk_high[idw]:
            aux = min(v_values[lk_down[idw]:lk_high[idw]])
            x_ind = list(map(lambda k1: k1 == aux, v_values[lk_down[idw]:lk_high[idw]]))
            x_aux1 = x[lk_down[idw]:lk_high[idw]]
            x_start = x_aux1[x_ind]
            aux_2 = min(v_values[lk_down[idw+1]:lk_high[idw+1]])
            x_ind_2 = list(map(lambda k2: k2 == aux_2, v_values[lk_down[idw+1]:lk_high[idw+1]]))
            x_aux2 = x[lk_down[idw+1]:lk_high[idw+1]]
            x_b = x_aux2[x_ind_2]
        else:
            aux = min(v_values[lk_high[idw]:lk_down[idw]])
            x_ind = list(map(lambda k1: k1 == aux, v_values[lk_high[idw]:lk_down[idw]]))
            x_aux1 = x[lk_high[idw]:lk_down[idw]]
            x_start = x_aux1[x_ind]
            aux_2 = min(v_values[lk_high[idw+1]:lk_down[idw+1]])
            x_ind_2 = list(map(lambda k2: k2 == aux_2, v_values[lk_high[idw+1]:lk_down[idw+1]]))
            x_aux2 = x[lk_high[idw+1]:lk_down[idw+1]]
            x_b = x_aux2[x_ind_2]
        n_area.append(np.trapz(v_values[x_start[0]:x_b[0]]))
        cardiacO.append((n_area[idw]*HR)/(Z_ao*1000))

    # SV=area / 0.14 cm³
    # cardiaO=(SV*HR)/1000 L
    # Heart Rate Variability

    # plt.plot(v_values)
    # plt.show()
    return cardiacO

# Calculate the Saturation
def let_the_magic_work_SO2(my_file):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import csv
    
    file = csv.DictReader(open(my_file), delimiter=",")
    # lets do this for Heart Rate
    # 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
    v_SO2 = []
    for row in file:
        if row[file.fieldnames[1]]=='NONIN_SPO2_8BEAT':
            n_value = row[file.fieldnames[4]]
            v_SO2.append(float(n_value))

    return v_SO2