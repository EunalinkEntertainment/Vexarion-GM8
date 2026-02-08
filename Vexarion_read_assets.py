import psycopg2
import configparser
import os
import sys

# --------------------------
# Get EXE folder
# --------------------------
if getattr(sys, 'frozen', False):
    exe_folder = os.path.dirname(sys.executable)  # built EXE
else:
    exe_folder = os.path.dirname(os.path.abspath(__file__))  # script

# Go UP one level
parent_folder = os.path.dirname(exe_folder)

# --------------------------
# Create/fetch "api_ini" folder
# --------------------------
api_ini_folder = os.path.join(parent_folder, "api_ini")
os.makedirs(api_ini_folder, exist_ok=True)

# --------------------------
# Connect to Render Postgres
# --------------------------
conn = psycopg2.connect(
    host="dpg-d6467dp4tr6s73a9hd1g-a.oregon-postgres.render.com",
    port=5432,
    dbname="vexarion_1st_database",
    user="vexarion_1st_database_user",
    password="qVNlrpvzBp2uYMVcKtHb4MMKOyaftoz2"
)
cur = conn.cursor()

# --------------------------
# Fetch all spaceship names
# --------------------------
cur.execute("SELECT name FROM ships ORDER BY id")
rows = cur.fetchall()

# Close DB connection
cur.close()
conn.close()

# --------------------------
# Prepare INI file
# --------------------------
ini = configparser.ConfigParser()
ini['Spaceship_list'] = {}

# Add total assets count
ini['Spaceship_list']['assets'] = str(len(rows))

# Add each ship as ship1, ship2, ...
for idx, (name,) in enumerate(rows, start=1):
    ini['Spaceship_list'][f'{idx}'] = name

# --------------------------
# Write to file inside api_ini folder
# --------------------------
ini_file_path = os.path.join(api_ini_folder, 'spaceships.ini')
with open(ini_file_path, 'w') as configfile:
    ini.write(configfile)

print(f"INI file created: {ini_file_path}")
sys.exit(0)  # indicate success
