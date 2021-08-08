#date: 7/8/2021
#name: Martin Benko
#purpose: select and insert the data to the psql table
# !!!!!!!
# IMPORTANT: I added 1 columns in the table (variable with name as "number" and it is SERIAL PRIMARY KEY)
# variable "id" column has None values and I changed the datatype as "INTEGER" and must be "SERIAL PRIMARY KEY"
# The "SERIAL" type must not be NONE


import psycopg2
import json

with open('/home/mbenko/Downloads/configClear_v2.json', 'r') as f:
    data = json.load(f)

#Creating a cursor object using the cursor() method

conn = psycopg2.connect(
   database='frinxPy', user='mbenko', password='mbenko', host='127.0.0.1', port= '5432')

cursor = conn.cursor()
# define sql table 
cursor.execute("DROP TABLE IF EXISTS INTERFACES;")
 
sql = """CREATE TABLE INTERFACES (
        number SERIAL PRIMARY KEY,
        id INTEGER,
        connection INTEGER,
        name VARCHAR(255),
        description VARCHAR(255),
        config json,
        type VARCHAR(50),
        infra_type VARCHAR(50),
        port_channel_id INTEGER,
        max_frame_size INTEGER
    );"""
    
cursor.execute(sql)
print('TABLE created successfully')

conn.commit()

# work with data
dat1 = data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface'] # link to the data from json

db_interface = ['Port-channel','TenGigabitEthernet','GigabitEthernet'] #interface
k=0
db = []
for i in range(len(db_interface)):
        
    dat = dat1[db_interface[i]] #read the port-channel, ten gigabit and gigabitEthernet
    
    for j in range(len(dat)): #channel 2, Tengigabit 4, gigabit 3
        line = []
        k = k+1 # number
        line.append(k)

        try:
            line.append(dat[j]["Cisco-IOS-XE-ethernet:service"]['instance'][0]['id']) # id
        except KeyError: 
            line.append(None)
        
        try:
            line.append(db_interface[i] + str(dat[j]['name']))# name
        except KeyError:
            line.append(None)

        try:
            line.append(dat[j]['description']) #description
        except KeyError:
            line.append(None)   

        try:
            line.append(json.dumps(dat[j])) # config
        except KeyError:
            line.append(None)

        try:
            line.append(dat[j]['Cisco-IOS-XE-ethernet:channel-group']['number']) #Port channel
        except KeyError:
            line.append(None)
        
        try:
            line.append(dat[j]['mtu']) # max frame size
        except KeyError:
            line.append(None)
        
        db.append(line)
        # write row in table

        cursor.execute('''INSERT INTO INTERFACES(number, id, name, description, config, port_channel_id, max_frame_size) VALUES (%s, %s, %s, %s, %s, %s, %s);''', line)
        conn.commit()  
        
conn.commit()
print('record inserted...')        
conn.close()
