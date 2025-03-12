import conn
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

conn = conn.connect()
cursor = conn.cursor()

cursor.execute("ALTER TABLE STEAM MODIFY MEDIAN_PLAYTIME FLOAT;")

cursor.execute("""
    SELECT APPID, NAME, PUBLISHER, MEDIAN_PLAYTIME 
    FROM STEAM 
    WHERE MEDIAN_PLAYTIME > 0 
    ORDER BY MEDIAN_PLAYTIME DESC;
""")

rows = cursor.fetchall()

pdf_file = "relatorio_horas_jogadas.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4

try:
    c.drawImage("017bfba4b10181c6d81ada273e09962a.jpg", 50, height - 95, width=80, height=80)
except:
    print("Imagem não encontrada.")

c.setFont("Helvetica-Bold", 18)
c.setFillColor(colors.black)
c.drawString(180, height - 60, "Relatório de Horas Jogadas")
c.setFillColor(colors.black)

x_positions = [50, 150, 280, 420, 550]
headers = ["ID", "Jogo", "Publicadora", "Horas"]
c.setFont("Helvetica-Bold", 12)

for i, header in enumerate(headers):
    c.drawString(x_positions[i], height - 110, header)

c.line(50, height - 115, 550, height - 115)

y = height - 140
c.setFont("Helvetica", 11)

for row in rows:
    game_name = simpleSplit(row[1], "Helvetica", 11, 120)
    publisher = simpleSplit(row[2] if row[2] is not None else "", "Helvetica", 11, 120)

    max_lines = max(len(game_name), len(publisher))

    c.drawString(x_positions[0], y, str(row[0]))
    for i, line in enumerate(game_name):
        c.drawString(x_positions[1], y - (i * 14), line)

    for i, line in enumerate(publisher):
        c.drawString(x_positions[2], y - (i * 14), line)

    c.drawString(x_positions[3], y, str(row[3]))
    

    c.setStrokeColor(colors.lightgrey)
    c.line(50, y - (max_lines * 14) - 5, 550, y - (max_lines * 14) - 5)
    
    y -= (max_lines * 14) + 20 

   
    if y < 50:
        c.showPage()
        y = height - 140

c.save()
print(f"PDF gerado com sucesso: {pdf_file}")

cursor.close()
conn.close()