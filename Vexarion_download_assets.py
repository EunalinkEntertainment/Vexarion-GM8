import psycopg2
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

# Create/fetch "ships" folder
ships_folder = os.path.join(parent_folder, "ships")
os.makedirs(ships_folder, exist_ok=True)

# --------------------------
# Get filename from GM8 argument
# --------------------------
# Example: python downloader.py "Orebreaker"
if len(sys.argv) < 2:
    print("No ship name provided as argument!")
    sys.exit(1)

ship_name = sys.argv[1]  # this comes from GM8 execute_program(prog, arg, wait)

# --------------------------
# Connect to Postgres
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
# Fetch the ship image by name
# --------------------------
cur.execute("SELECT image_data FROM ships WHERE name=%s", (ship_name,))
row = cur.fetchone()

if row:
    img_data = row[0]

    # Append .png extension
    file_path = os.path.join(ships_folder, f"{ship_name}.jpg")

    # Overwrite if exists
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "wb") as f:
        f.write(img_data)

    print(f"{ship_name}.png downloaded to {ships_folder}")
else:
    print(f"Ship {ship_name} not found in database.")

cur.close()
conn.close()
