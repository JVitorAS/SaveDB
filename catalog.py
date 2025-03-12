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
        self.page = 0  # Página inicial
        self.itens_page = 6  # Jogos por página

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=10, pady=10)

        self.imagens_refs = {}  # Dicionário para armazenar referências às imagens
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

        self.imagens_refs.clear()  # Limpa o dicionário de imagens

        # 🔹 Busca os jogos da página atual
        games = list_game(self.page * self.itens_page, self.itens_page)

        if not games:
            return

        for i, game in enumerate(games):
            frame = tk.Frame(self.container, borderwidth=2, relief="groove")
            frame.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

            label_img = tk.Label(frame)
            label_img.pack()

            label_nome = tk.Label(frame, text=game[0], font=("Arial", 12, "bold"))
            label_nome.pack()

            label_notas = tk.Label(frame, text=f"👍 {game[2]} | 👎 {game[3]}")
            label_notas.pack()

            # 🔹 Carregar imagens de forma assíncrona
            self.carregar_imagem(game[1], label_img)

    def carregar_imagem(self, url, label):
        """Baixa e exibe a imagem de forma assíncrona"""
        if url in image_cache:  # Verifica se a imagem já foi baixada
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

                    image_cache[url] = photo  # Armazena no cache

                    # 🔹 Atualiza a interface de forma assíncrona
                    self.after(0, lambda: label.config(image=photo) or setattr(label, "image", photo))
            except Exception as e:
                print(f"Erro ao obter imagem: {e}")

        executor.submit(baixar_imagem)  # Envia para execução em thread separada

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
