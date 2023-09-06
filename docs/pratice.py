import csv

cv="myfile.csv"
with open (cv,mode='r',newline='') as file:
    reader=csv.reader(file,delimiter=';')
    i=0
    a=""
    count=0
    boxes=[]
    for row in reader:
        i=i+1
        if row[2]!=a:#crea lista de las cajas
            a=row[2]
            count=count+1
            boxes.append(a)
        #for raw in row:
        #   print(raw)
        #col1n=row[3]

        #print(col1, row)
        


        if  i == 3:
            print(type(a),a)
            print(boxes)
            break

