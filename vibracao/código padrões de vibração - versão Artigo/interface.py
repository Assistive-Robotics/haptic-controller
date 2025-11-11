import serial
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- Nova Paleta de Cores com Alto Contraste ---
cores = {
    "fundo_principal": "#FFF0F5",       # Rosa bem clarinho (Lavender Blush) - Fundo
    "fundo_secundario": "#FADADD",      # Rosa mais claro para detalhes
    
    # Texto escuro para alto contraste
    "texto_principal": "#4B0082",       # Roxo escuro / Índigo para títulos e texto
    "texto_em_botao": "#3D2C3F",        # Tom de "Berinjela" escuro para texto nos botões

    # Botões ajustados para o texto escuro
    "botao_primario": "#F48FB1",        # Rosa pastel mais suave
    "botao_secundario": "#CE93D8",      # Lilás pastel
    "botao_voltar": "#BCA2C7",          # Lilás acinzentado (Dusty Lilac)
    "botao_perigo": "#EF9A9A"           # Vermelho rosado claro, para manter o alerta
}

# --- Configuração Serial ---
try:
    # Tente conectar à porta serial. Altere 'COM3' se necessário.
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
except serial.SerialException as e:
    messagebox.showerror("Erro de Conexão", f"Não foi possível conectar à porta COM3: {e}")
    # Usa uma classe mock para permitir que a interface abra
    class MockSerial:
        def write(self, *args): print("MockSerial: Comando enviado")
        # CORRIGIDO: is_open deve ser uma propriedade (booleano), não um método, como em pyserial
        is_open = True
        def close(self): pass
    arduino = MockSerial()
    # Para rodar a GUI mesmo sem o Arduino conectado, comente o 'exit()':
    # exit() 

# O primeiro padrão personalizado é o 7 (após os 6 fixos)
contador_padroes = 7
# Lista para armazenar as variáveis de entrada dos passos do padrão personalizado
campos_passos = [] 
# Opções de atuadores: 0 a 5 (motores) e -1 (pausa)
opcoes_atuador = [-1, 0, 1, 2, 3, 4, 5]

# --- Funções de Navegação e Serial ---

def enviar_comando(comando):
    """Envia um comando para o Arduino com uma nova linha no final."""
    print(f"Enviando comando: {comando}")
    try:
        # Se for um MockSerial, apenas simula o envio
        # CORRIGIDO: Acessando arduino.is_open como propriedade (sem ())
        if hasattr(arduino, 'is_open') and not arduino.is_open:
             print("Serial não está aberta. Comando não enviado.")
             return
             
        arduino.write((str(comando) + "\n").encode('utf-8'))
    except Exception as e:
        # Se for a classe mock, este bloco não deve rodar, mas é um bom fallback
        if not isinstance(arduino, MockSerial):
            print(f"Erro ao enviar comando: {e}")

def abrir_padroes():
    """Navega para a tela de reprodução de padrões."""
    tela_inicial.pack_forget()
    tela_padroes.pack(fill="both", expand=True)
    

def abrir_criar_padroes():
    """Navega para a tela de criação de novos padrões."""
    tela_inicial.pack_forget()
    tela_criar_padroes.pack(fill="both", expand=True)

def voltar_inicio(tela_atual):
    """Oculta a tela atual e exibe a tela inicial."""
    tela_atual.pack_forget()
    tela_inicial.pack(fill="both", expand=True)

# --- Funções de Criação de Padrão ---

def adicionar_passo(frame_container, atuador_default=0, duracao_default=100):
    """Adiciona um novo par de campos (Atuador e Duração) à interface de criação."""
    
    # Frame para agrupar o passo (atuador + duração)
    frame_passo = tk.Frame(frame_container, bg=cores["fundo_secundario"], padx=5, pady=5)
    frame_passo.pack(pady=2, fill='x')

    # 1. Entrada do Atuador (Dropdown)
    var_atuador = tk.IntVar(value=atuador_default)
    label_atuador = tk.Label(frame_passo, text="Atuador:", bg=cores["fundo_secundario"], fg=cores["texto_principal"])
    label_atuador.pack(side=tk.LEFT, padx=(5, 2))
    opt_atuador = tk.OptionMenu(frame_passo, var_atuador, *opcoes_atuador)
    opt_atuador.config(bg=cores["botao_secundario"], fg=cores["texto_em_botao"], relief=tk.FLAT)
    opt_atuador["menu"].config(bg=cores["fundo_secundario"], fg=cores["texto_em_botao"])
    opt_atuador.pack(side=tk.LEFT, padx=5)

    # 2. Entrada da Duração (Entry)
    var_duracao = tk.StringVar(value=str(duracao_default))
    label_duracao = tk.Label(frame_passo, text="Duração (ms):", bg=cores["fundo_secundario"], fg=cores["texto_principal"])
    label_duracao.pack(side=tk.LEFT, padx=(10, 2))
    entry_duracao = tk.Entry(frame_passo, textvariable=var_duracao, width=8, justify='center', 
                            fg=cores["texto_principal"], bg=cores["fundo_principal"])
    entry_duracao.pack(side=tk.LEFT, padx=5)
    
    # Adiciona a referência do passo à lista global
    campos_passos.append({'frame': frame_passo, 'atuador': var_atuador, 'duracao': var_duracao})

def remover_ultimo_passo():
    """Remove o último passo adicionado da interface e da lista de controle."""
    if campos_passos:
        passo_removido = campos_passos.pop()
        passo_removido['frame'].destroy()

def criar_padrao():
    """Lê os campos dinâmicos, serializa para o formato do Arduino e envia o comando."""
    global contador_padroes
    
    if not campos_passos:
        messagebox.showwarning("Atenção", "Adicione pelo menos um passo para criar um padrão.")
        return

    dados_serializados = []
    
    for i, passo in enumerate(campos_passos):
        try:
            atuador = passo['atuador'].get()
            # Garante que o input seja um inteiro válido
            duracao_str = passo['duracao'].get().strip()
            if not duracao_str.isdigit():
                 raise ValueError("Duração não é um número.")
            duracao = int(duracao_str)
        except ValueError:
            messagebox.showerror("Erro de Entrada", f"Duração inválida no passo {i+1}. Use apenas números inteiros positivos.")
            return

        # Validação simples
        if atuador not in opcoes_atuador:
            messagebox.showerror("Erro de Validação", f"Atuador inválido no passo {i+1}. Use -1, 0, 1, 2, 3, 4 ou 5.")
            return
        
        if duracao <= 0:
            messagebox.showerror("Erro de Validação", f"Duração deve ser maior que 0 no passo {i+1}.")
            return
        
        # Constrói o formato serial: atuador,duracao
        dados_serializados.append(f"{atuador},{duracao}")

    # Junta todos os pares para formar a string final
    string_final = ",".join(dados_serializados)

    # Envia o comando de criação de padrão (@) seguido dos dados
    enviar_comando(f"@{string_final}")
    
    # Após o envio bem-sucedido, cria o botão e limpa a tela de criação
    adicionar_botao_padrao(contador_padroes)
    contador_padroes += 1
    
    # Limpa a tela de criação para um novo padrão
    while campos_passos:
        remover_ultimo_passo()
    # Adiciona um passo inicial vazio
    adicionar_passo(frame_passos, 0, 100)
    
    messagebox.showinfo("Sucesso", f"Padrão {contador_padroes - 1} criado e enviado!")


# --- Funções de Gerenciamento de Botões ---

def excluir_padrao_personalizado(numero_do_padrao, frame_do_botao):
    """Envia o comando de exclusão para o Arduino e remove o botão da GUI."""
    if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o Padrão {numero_do_padrao}?"):
        # Envia o comando de exclusão (#)
        enviar_comando(f"#{numero_do_padrao}")
        frame_do_botao.destroy()

def adicionar_botao_padrao(numero):
    """Cria um novo conjunto de botões (Padrão + Excluir) para um padrão personalizado."""
    
    # Cria um frame container para o botão e o botão de exclusão
    # Adiciona ao container_padroes, que está dentro do Canvas scrollable
    frame = tk.Frame(container_padroes, bg=cores["fundo_principal"]) # Usando fundo_principal para o frame container
    frame.pack(pady=5, fill='x', padx=10)
    
    # Botão para Tocar o Padrão
    novo_botao = tk.Button(
        frame, text=f"Padrão {numero}", bg=cores["botao_primario"], fg=cores["texto_em_botao"], 
        font=("Segoe UI", 12, "bold"), command=lambda n=numero: enviar_comando(n), relief=tk.FLAT
    )
    novo_botao.pack(side=tk.LEFT, expand=True, fill='x', ipady=10)
    
    # Botão de Excluir
    btn_excluir = tk.Button(
        frame, text="Excluir", bg=cores["botao_perigo"], fg=cores["texto_em_botao"], 
        font=("Segoe UI", 10, "bold"), command=lambda n=numero, f=frame: excluir_padrao_personalizado(n, f), relief=tk.FLAT
    )
    btn_excluir.pack(side=tk.LEFT, padx=(5, 0), ipady=10)
    
    # Força a atualização do scrollbar após adicionar um novo botão
    container_padroes.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# --- Configuração da Janela Principal ---
root = tk.Tk()
root.title("Controle de Vibração")
root.geometry("350x600") 
root.configure(bg=cores["fundo_principal"])

# --- Tela Inicial ---
tela_inicial = tk.Frame(root, bg=cores["fundo_principal"])
tela_inicial.pack(fill="both", expand=True, pady=40)
frame_central_inicial = tk.Frame(tela_inicial, bg=cores["fundo_principal"])
frame_central_inicial.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Botões da tela inicial
tk.Button(frame_central_inicial, text="""Padrões Fixos e
Customizados""", bg=cores["botao_primario"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 14, "bold"), command=abrir_padroes, width=20, relief=tk.FLAT).pack(pady=10, ipady=10)
tk.Button(frame_central_inicial, text="Criar Novo Padrão", bg=cores["botao_primario"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 14, "bold"), command=abrir_criar_padroes, width=20, relief=tk.FLAT).pack(pady=10, ipady=10)
tk.Button(frame_central_inicial, text="Sair", bg=cores["botao_perigo"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 14, "bold"), command=root.quit, width=20, relief=tk.FLAT).pack(pady=10, ipady=10)

# --- Tela de Padrões (Reprodução) ---
tela_padroes = tk.Frame(root, bg=cores["fundo_principal"])

# Configurações do Canvas e Scrollbar
canvas = tk.Canvas(tela_padroes, bg=cores["fundo_principal"], highlightthickness=0)
scrollbar = tk.Scrollbar(tela_padroes, orient="vertical", command=canvas.yview)
# O container_padroes é onde os botões (fixos e dinâmicos) serão adicionados
container_padroes = tk.Frame(canvas, bg=cores["fundo_principal"]) 

container_padroes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=container_padroes, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Empacotamento do Canvas (ocupa a maior parte da tela) e do Scrollbar
canvas.pack(side="top", fill="both", expand=True) # Alterado para top
scrollbar.pack(side="right", fill="y") # Mantido à direita

# Botões de Padrões Fixos (1 a 6)
padroes = ["Padrão 1: Movimento Direita", "Padrão 2: Movimento Esquerda", 
           "Padrão 3: Bidirecional Simples", "Padrão 4: Perigo Complexo", 
           "Padrão 5: Estático Direita", "Padrão 6: Estático Esquerda"]

for padrao in padroes:
    btn_id = padroes.index(padrao) + 1
    btn = tk.Button(
        container_padroes, text=padrao, bg=cores["botao_secundario"], fg=cores["texto_em_botao"], 
        font=("Segoe UI", 12, "bold"), command=lambda n=btn_id: enviar_comando(n), relief=tk.FLAT
    )
    btn.pack(pady=5, ipady=10, fill='x', padx=10)

# --- Botão Voltar da Tela de Padrões ---
# Empacotado diretamente na tela_padroes, fora do canvas, garantindo que seja sempre visível no fundo
tk.Button(tela_padroes, text="Voltar para Início", bg=cores["botao_voltar"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 12, "bold"), command=lambda: voltar_inicio(tela_padroes), relief=tk.FLAT).pack(side=tk.BOTTOM, pady=10, ipady=10, fill='x', padx=10)


# --- Tela Criar Padrões ---
tela_criar_padroes = tk.Frame(root, bg=cores["fundo_principal"])

# Título e Instruções
tk.Label(tela_criar_padroes, text="""Criar Novo Padrão de Vibração
(Passo a Passo)""",
          bg=cores["fundo_principal"], fg=cores["texto_principal"], font=("Segoe UI", 14, "bold")).pack(pady=10)

tk.Label(tela_criar_padroes, text="Atuadores: 0 a 5 | Pausa: -1",
          bg=cores["fundo_principal"], fg=cores["texto_principal"], font=("Segoe UI", 10)).pack(pady=5)

# Container Scrollable para os Passos
canvas_passos = tk.Canvas(tela_criar_padroes, bg=cores["fundo_secundario"], highlightthickness=0)
vscrollbar_passos = tk.Scrollbar(tela_criar_padroes, orient="vertical", command=canvas_passos.yview)
frame_passos = tk.Frame(canvas_passos, bg=cores["fundo_secundario"]) # Frame onde os passos serão adicionados

# Configuração do Scrollbar
frame_passos.bind("<Configure>", lambda e: canvas_passos.configure(scrollregion=canvas_passos.bbox("all")))
canvas_passos.create_window((0, 0), window=frame_passos, anchor="nw")
canvas_passos.configure(yscrollcommand=vscrollbar_passos.set)

canvas_passos.pack(pady=10, padx=10, fill="both", expand=True)
vscrollbar_passos.pack(side="right", fill="y")

# Frame para Botões de Ação
frame_acoes = tk.Frame(tela_criar_padroes, bg=cores["fundo_principal"])
frame_acoes.pack(pady=5, fill='x', padx=10)

# Botões de Adicionar/Remover
tk.Button(frame_acoes, text="+ Adicionar Passo", bg=cores["botao_secundario"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 10, "bold"), command=lambda: adicionar_passo(frame_passos), relief=tk.FLAT).pack(side=tk.LEFT, expand=True, fill='x', ipady=5)

tk.Button(frame_acoes, text="- Remover Último", bg=cores["botao_perigo"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 10, "bold"), command=remover_ultimo_passo, relief=tk.FLAT).pack(side=tk.LEFT, expand=True, fill='x', padx=(5, 0), ipady=5)

# Botão de Criação e Envio
tk.Button(tela_criar_padroes, text="Criar e Enviar Padrão para Arduino", bg=cores["botao_primario"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 12, "bold"), command=criar_padrao, relief=tk.FLAT).pack(pady=(10, 5), ipady=10, fill='x', padx=10)

# --- Botão Voltar da Tela Criar Padrões ---
tk.Button(tela_criar_padroes, text="Voltar para Início", bg=cores["botao_voltar"], fg=cores["texto_em_botao"], 
          font=("Segoe UI", 12, "bold"), command=lambda: voltar_inicio(tela_criar_padroes), relief=tk.FLAT).pack(side=tk.BOTTOM, pady=(0, 10), ipady=10, fill='x', padx=10)

# Adiciona o passo inicial ao carregar a tela
adicionar_passo(frame_passos, 0, 100)


# --- Encerramento ---

def on_closing():
    """Fecha a porta serial e destrói a janela."""
    # CORRIGIDO: Acessando arduino.is_open como propriedade (sem ())
    if hasattr(arduino, 'is_open') and arduino.is_open:
        arduino.close()
        print("Porta serial fechada.")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
