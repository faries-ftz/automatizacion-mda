from selenium import webdriver
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
#import undetected_chromedriver as uc
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

url="http://epmigpm.epmigraciones.gob.pe:7001/prod-mgr/ui/login#!com.gemalto.ics.rnd.pm.ri.web.ui.view.LoginView"
user="ftobalaz"
password="Peru1234!"
path=r'C:\Users\VB\Desktop\docs\docs\msedgedriver.exe'

edge_drive_path=(path)
edge_service=Service(edge_drive_path)
edge_option=Options()

#browser=uc.Chrome(service=edge_service,options=edge_option)  
browser=webdriver.Edge(service=edge_service,options=edge_option) #original
browser.get(url)
wait=WebDriverWait(browser,50) #asignas valor de esperar hasta 50s por respuesta
wait.until(EC.presence_of_element_located((By.TAG_NAME,"body"))) # requiere doble () para ser entendido como 1 solo dato

rock=browser.find_element(By.ID,'com.gemalto.ics.rnd.pm.ri.web.loginpage.form.usernameField')
rock.send_keys(user)
rock=browser.find_element(By.ID,'com.gemalto.ics.rnd.pm.ri.web.loginpage.form.passwordField')
rock.send_keys(password)
rock.send_keys(Keys.ENTER)
wait=WebDriverWait(browser,10) #espera
# visible_element=wait.until(EC.visibility_of_element_located((By.ID,'com.gemalto.ics.rnd.pm.ri.web.loginpage.form.passwordField')))
wait.until(EC.visibility_of_element_located((By.ID,'com.gemalto.ics.rnd.pm.web.panel.MenuPanel.item[com.gemalto.ics.peru.pm.mod.stockmanagement.ui.menu.countdocumentspanel]')))
#print(visible_element)

# fin de ingreso con la cuenta
# entrando a plataforma PM
rock=browser.find_element(By.ID,'com.gemalto.ics.rnd.pm.web.panel.MenuPanel.item[com.gemalto.ics.peru.pm.mod.stockmanagement.ui.menu.countdocumentspanel]')
rock.send_keys(Keys.ENTER)

#ingreso al apartado de contados de codigos de pasaportes
#   requiere de especificar varios atributos del elemento
# <input type="text" class="v-textfield v-widget v-has-width" tabindex="0" style="width: 200px;">

selector="input.v-textfield.v-widget.v-has-width[type='text'][style='width: 200px;']" #funciono
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,selector)))
rock=browser.find_element(By.CSS_SELECTOR,selector)

#ingreso de datos
#nota: no funciona el EC.presence_of_element_located((By.ID,selector)) tampoco el EC.text_to_be_present_in_element_value((By.ID, "mi_casilla_de_entrada"), "")
#se intenta con el EC.element_to_be_clickable((By.CSS_SELECTOR, selector)) --- tampoco

folder=os.listdir(r'C:\Users\VB\Desktop\docs\documentos_csv')
folder_csv=[file for file in folder if file.endswith(".csv")] # 
print(f"--- se encontraron {len(folder_csv)} para ingresar datos ---")
BOX=[]
for rote in folder_csv:
    cv=os.path.join(r'C:\Users\VB\Desktop\docs\documentos_csv',rote)
    with open (cv,mode='r',newline='') as file:
        reader=csv.reader(file,delimiter=';')
        i=0
        a=""
        count=0
        boxes=[]
        
        #<table class="v-table-table">
        for row in reader:
            tabla=browser.find_element(By.CSS_SELECTOR, "table.v-table-table") #identificamos a la tabla donde se agregara valores
            #b=0 #comparativo para while
            
            if row[2]!=a:#crea lista de las cajas
                a=row[2]
                count=count+1
                boxes.append(a)

            filas =len(tabla.find_elements(By.TAG_NAME, "tr")) #identificamos todas las listas de la tabla, luego su cantidad    
            #while i != -1:
            rock.send_keys(row[3])
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,selector))) #espera hasta que cargue el dato enviado
            while a == "a":
                try:
                    WebDriverWait(browser, 10).until(lambda x: (browser.find_elements(By.CSS_SELECTOR,selector)) == row[3])
                    a="b"
                except:
                    a="a"
            rock.send_keys(Keys.ENTER) #acaba de ingresar dato nuevo
            #IA dice que la tabla desaparece y reaparece por lo que debemos esperar a que aparezca primero
            #wait.until(EC.staleness_of(tabla)) # espera hasta que reaparezca tabla
            #wait.until(lambda x: len(tabla.find_elements(By.TAG_NAME, "tr"))>filas) #intentamos que el nuevo valor de filas sera mayor al anterior bajo condicional lambda.
            #el siguiente codigo espera hast encontrar un nuevo elemento de tabla y cuenta su cantidad de listas para luego compararla con la cantidad anterior
            
            try:
                WebDriverWait(browser, 10).until(lambda x: len(browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")) >= filas)
                #if len(browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")) > filas:
                fila=browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")
                wait.until(fila[-1]==row[3])
                i=-1
            except: 

                i=i+1
                print(f"intento: {i}\nse enuentra un error estando el el csv: {rote} con el {row[0]}")
                x=input("hubo un error en la ejecucion, analizar porfa ;')  y luego dar ENTER para reintentar o ctrl+c en path para cancelar\ntambien puede ingresar s para saltar este evento")
                if x=="s":
                    i=-1
            
            #
            # WebDriverWait(browser, 12).until(lambda x: len(browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")) > filas)
            #i= -1
            """""
            while b==1:
                try:
                    tabla=browser.find_element(By.CSS_SELECTOR, "table.v-table-table")
                    #tendremos que volver a indetificar la nueva tabla
                    if len(tabla) >filas: # comparamos la nueva cantidad de datos con la anterior
                        b+=1
                except:
                    pass
            """

            """""
            #este es 
            if  i == 4:
                print(type(a),a)
                break
            """
        
        """"
        if i ==1000:
            selector=browser.find_element(By.CSS_SELECTOR,"div.v-button.v-widget span.v-button-caption")
            selector.click()
            print("--- se cargo 1000 pasaportes")
        else:
            print("se llego ingresar: "+str(i)+" pasaportes")
            x=input("desea cancelar(c) o ingresar datos?(s): ")
            if x =="s":
                selector=browser.find_element(By.CSS_SELECTOR,"div.v-button.v-widget span.v-button-caption")
                selector.click()
            elif x=="c":
                #<div tabindex="0" role="button" class="v-button v-widget">
                selector=browser.find_element(By.CSS_SELECTOR,"div.v-button.v-widget span.v-button-caption")
                """ #investigar porque 2 botones se ven igual 
        # con esto identificamos los botones cancelar y guardar y los ponemos en una lista.
        botones = browser.find_elements(By.CSS_SELECTOR, "div.v-button.v-widget span.v-button-caption")
        BOX.append(boxes)
# Ahora puedes hacer clic en el botón que desees según su posición en la lista
# Por ejemplo, para hacer clic en "Guardar":
        input("--- se cargo los datos, desea subirlos? ---")
        botones[0].click()
        #hacemos esperar hasta que la tabla no tenga elementos en ella
        wait.until(lambda x: len(browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")) == 0)
        # O para hacer clic en "Cancelar":
        # botones[1].click()
    



time.sleep(4)
print(f" --- fin de conteos ---\n las cajas son: {BOX}")
#browser.quit()
