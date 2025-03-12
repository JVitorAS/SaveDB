import mysql.connector
import pandas as pd
import os

host = "localhost"
user = "root"
password = ""
db = "STEAM"
dataset_path = "C:\\sales walmart\\"
conn = mysql.connector.connect(host=host, user=user, password=password)
cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
cursor.execute(f"USE {db}")


files = [
    "steam.csv",
    "steamspy_tag_data.csv",
    "steam_description_data.csv",
    "steam_media_data.csv",
    "steam_requirements_data.csv",
    "steam_support_info.csv"
]

for file in files:
    file_path = os.path.join(dataset_path, file)
    
    # Carregar CSV
    df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
    
    table_name = file.replace(".csv", "")  
    columns = ", ".join([f"`{col}` TEXT" for col in df.columns])  

    sql_create = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})"
    cursor.execute(sql_create)

    for _, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(row))
        sql_insert = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
        cursor.execute(sql_insert, tuple(row))

    conn.commit()
    print(f"Tabela `{table_name}` criada e populada com sucesso.")

cursor.close()
conn.close()
print("Processo concluído com sucesso.")
