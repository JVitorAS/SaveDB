import conn
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# 🔹 Criar um cache para imagens já carregadas
image_cache = {}

# 🔹 Criar um pool de conexões no início (ajustável para sua necessidade)
executor = ThreadPoolExecutor(max_workers=6)

# 🔹 Função para buscar jogos no banco de dados
def list_game(offset, limit=6):
    conexao = conn.connect()
    cursor = conexao.cursor()
    view = """
        CREATE VIEW IF NOT EXISTS CATALOG_GAMES AS
        SELECT * FROM (
            SELECT 
                S.NAME, 
                M.HEADER_IMAGE, 
                CAST(S.POSITIVE_RATINGS AS INT) AS POSITIVE_RATINGS, 
                CAST(S.NEGATIVE_RATINGS AS INT) AS NEGATIVE_RATINGS
            FROM STEAM S
            INNER JOIN STEAM_MEDIA_DATA M ON S.APPID = M.STEAM_APPID
            WHERE M.HEADER_IMAGE IS NOT NULL
            ORDER BY S.POSITIVE_RATINGS DESC
        ) AS ordered_view;   
    """
    cursor.execute(view)

    sql_games = """
        SELECT * FROM CATALOG_GAMES LIMIT %s OFFSET %s
    """
    cursor.execute(sql_games, (limit, offset))
    games = cursor.fetchall()

    cursor.close()
    conexao.close()
    return games

# 🔹 Classe do Catálogo de Jogos
class CatalogoJogos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catálogo de Jogos")
        self.geometry("700x770")
        #  Página inicial  & Jogos por página
        self.page = 0 
        self.itens_page = 9 

        self.container = tk.Frame(self)

        self.container.pack(expand=True, fill="both", padx=10, pady=10)

        # Dicionário para armazenar referências às imagens
        self.imagens_refs = {}  
        self.carregar()

        # Botões de navegação
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=10, pady=10)

        self.btn_anterior = tk.Button(frame_botoes, text="◀ Anterior", command=self.pagina_anterior)
        self.btn_anterior.pack(side="left", padx=10)

        self.btn_proximo = tk.Button(frame_botoes, text="Próximo ▶", command=self.pagina_proxima)
        self.btn_proximo.pack(side="right", padx=10)

    def carregar(self):
        # 🔹 Remove widgets antigos
        for widget in self.container.winfo_children():
            widget.destroy()

        # Limpa o dicionário de imagens
        self.imagens_refs.clear()  

        # 🔹 Busca os jogos da página atual
        games = list_game(self.page * self.itens_page, self.itens_page)

        if not games:
            return

        for i, game in enumerate(games):
            frame = tk.Frame(self.container, borderwidth=2, relief="groove")
            
            # Modificado para ter 3 colunas e 3 linhas
            row = i // 3
            column = i % 3

            frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            label_img = tk.Label(frame)
            label_img.pack()

            label_nome = tk.Label(frame, text=game[0], font=("Arial", 12, "bold"))
            label_nome.pack()

            label_notas = tk.Label(frame, text=f"👍 {game[2]} | 👎 {game[3]}")
            label_notas.pack()

            # Carregar imagens de forma assíncrona
            self.carregar_imagem(game[1], label_img)



    def carregar_imagem(self, url, label):
        """Baixa e exibe a imagem de forma assíncrona"""
         # Verifica se a imagem já foi baixada
        if url in image_cache: 
            label.config(image=image_cache[url])
            label.image = image_cache[url]
            return

        def baixar_imagem():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((150, 150), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)

                    # Armazena no cache
                    image_cache[url] = photo 

                    # 🔹 Atualiza a interface de forma assíncrona
                    self.after(0, lambda: label.config(image=photo) or setattr(label, "image", photo))
            except Exception as e:
                print(f"Erro ao obter imagem: {e}")

        # Envia para execução em thread separada
        executor.submit(baixar_imagem)

    def pagina_proxima(self):
        self.page += 1
        self.carregar()

    def pagina_anterior(self):
        if self.page > 0:
            self.page -= 1
            self.carregar()

# 🔹 Inicia o aplicativo
if __name__ == "__main__":
    app = CatalogoJogos()
    app.mainloop()