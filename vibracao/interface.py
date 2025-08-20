import serial
import tkinter as tk

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

botoes_dinamicos = []
contador_padroes = 6  # começa em 6 porque 1–5 são fixos

def enviar_comando(comando):
    arduino.write((comando + "\n").encode())

def abrir_padroes():
    tela_inicial.pack_forget()
    tela_padroes.pack()

def abrir_criar_padroes():
    tela_inicial.pack_forget()
    tela_criar_padroes.pack()

def voltar_inicio(tela):
    tela.pack_forget()
    tela_inicial.pack()

def criar_padrao():
    global contador_padroes
    valores = entry_valores.get().strip()
    if valores:
        enviar_comando("@" + valores)
        adicionar_botao_padrao(contador_padroes)
        contador_padroes += 1
        entry_valores.delete(0, tk.END)

def excluir_padrao_personalizado(numero, frame):
    enviar_comando(f"#{numero}")
    frame.destroy()

def adicionar_botao_padrao(numero):
    frame = tk.Frame(tela_padroes, bg="#A0A0A0")
    frame.pack(pady=5)

    novo_botao = tk.Button(
        frame,
        text=f"Padrão {numero}",
        bg="#9370DB",
        fg="black",
        font=("Comic Sans MS", 10, "bold"),
        command=lambda n=numero: enviar_comando(str(n)),
        height=2,
        width=10
    )
    novo_botao.pack(side=tk.LEFT)

    btn_excluir = tk.Button(
        frame,
        text="Excluir",
        bg="#9370DB",
        fg="black",
        font=("Comic Sans MS", 10, "bold"),
        command=lambda n=numero, f=frame: excluir_padrao_personalizado(n, f),
        height=2,
        width=8
    )
    btn_excluir.pack(side=tk.LEFT)

    botoes_dinamicos.append((numero, frame))

root = tk.Tk()
root.title("Controle de Vibração")
root.geometry("300x400")
root.configure(bg="#A0A0A0")

# Tela Inicial
tela_inicial = tk.Frame(root, bg="#A0A0A0")
tela_inicial.pack()

btn_padroes = tk.Button(
    tela_inicial,
    text="Padrões",
    bg="#9370DB",
    fg="black",
    font=("Comic Sans MS", 10, "bold"),
    command=abrir_padroes,
    height=2,
    width=15
)
btn_padroes.pack(pady=10)

btn_criar_padroes = tk.Button(
    tela_inicial,
    text="Criar Padrões",
    bg="#9370DB",
    fg="black",
    font=("Comic Sans MS", 10, "bold"),
    command=abrir_criar_padroes,
    height=2,
    width=15
)
btn_criar_padroes.pack(pady=10)

btn_sair = tk.Button(
    tela_inicial,
    text="Sair",
    bg="#9370DB",
    fg="black",
    font=("Comic Sans MS", 10, "bold"),
    command=root.quit,
    height=2,
    width=15
)
btn_sair.pack(pady=10)

# Tela de Padrões
tela_padroes = tk.Frame(root, bg="#A0A0A0")

for i in range(1, 6):
    frame = tk.Frame(tela_padroes, bg="#A0A0A0")
    frame.pack(pady=5)

    btn = tk.Button(
        frame,
        text=f"Padrão {i}",
        bg="#9370DB",
        fg="black",
        font=("Comic Sans MS", 10, "bold"),
        command=lambda n=i: enviar_comando(str(n)),
        height=2,
        width=10
    )
    btn.pack()

btn_voltar = tk.Button(
    tela_padroes,
    text="Voltar",
    bg="#9370DB",
    fg="black",
    font=("Comic Sans MS", 10, "bold"),
    command=lambda: voltar_inicio(tela_padroes),
    height=2,
    width=15
)
btn_voltar.pack(pady=10)

# Tela Criar Padrões
tela_criar_padroes = tk.Frame(root, bg="#A0A0A0")

lbl_info = tk.Label(
    tela_criar_padroes,
    text="Digite tempos separados por vírgula:\nEx: 100,200,100,200",
    bg="#A0A0A0",
    fg="black",
    font=("Comic Sans MS", 10, "bold")
)
lbl_info.pack(pady=10)

entry_valores = tk.Entry(tela_criar_padroes, font=("Comic Sans MS", 10, "bold"))
entry_valores.pack(pady=10)

btn_criar = tk.Button(
    tela_criar_padroes,
    text="Enviar Padrão",
    bg="#9370DB",
    fg="black",
    font=("Comic Sans MS", 10, "bold"),
    command=criar_padrao,
    height=2,
    width=15
)
btn_criar.pack(pady=10)

btn_voltar_criar = tk.Button(
    tela_criar_padroes,
    text="Voltar",
    bg="#9370DB",
    fg="black",
    font=("Comic Sans MS", 10, "bold"), 
    command=lambda: voltar_inicio(tela_criar_padroes),
    height=2,
    width=15
)
btn_voltar_criar.pack(pady=10)

root.mainloop()
