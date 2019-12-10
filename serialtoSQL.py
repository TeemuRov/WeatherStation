import MySQLdb
import serial
import time
import datetime

db = MySQLdb.connect(host="mweatherstation.cpd96oxpry4s.us-east-1.rds.amazonaws.com", user="t8mios00",
                     passwd="kahvia1234", db="WeatherStation")

cur = db.cursor()

port = "/dev/ttyACM0"
baud = 9600
sample = 20

serialPort = serial.Serial(port, baud, timeout = 1)

#time.sleep(1)

tempSum = 0.0
humiSum = 0.0
count = 0
temperature = ""
humidity = ""

while True:
    ser = str(serialPort.readline())
    if(len(ser) > 10 and len(ser) < 30): #15, 22 / 10, 30
        try:
            alku, humiTemp, humidity, temperature ,loppu = ser.split()
        except:
            humidity = 0;
            temperature = 0;
            count -= 1
            
        tempSum += float(temperature)
        humiSum += float(humidity)
        #time.sleep(.1)
        count += 1
    
    if count == sample:
        cur.execute("SELECT MAX(idweather) FROM weather")
        currentID = str(cur.fetchall())
        currentID = int(currentID.replace("(", "").replace(",", "").replace(")", ""))
        
        tempAvg = tempSum / sample
        humiAvg = humiSum / sample
        print("%.6f "%tempAvg)
        print("%.6f"%humiAvg)
        
        time = datetime.datetime.now().time()
        date = datetime.datetime.now().date()
        
        sql = ("INSERT INTO weather VALUES(%s, '%s', '%s', %.4f, %s)" % \
               (currentID + 1, date, time, tempAvg, humiAvg))
        try:
            cur.execute(sql)
            db.commit()
            print("jes")
        except:
            db.rollback()
            print("es")
            
        count = 0
        tempSum = 0.0
        humiSum = 0.0

serialPort.close()
db.close()

