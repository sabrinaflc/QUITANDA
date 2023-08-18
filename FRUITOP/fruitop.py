from tkinter import messagebox, ttk
from tkinter import *
import sqlite3

root = Tk()

class Func():
    def limpa_tela(self):
        self.campo1.delete(0, END)
        self.campo2.delete(0, END)
        self.campo3.delete(0, END)
        self.campo4.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("frutas.db")
        self.cursor = self.conn.cursor()
        print('Conectando ao Banco de Dados...')

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando do Banco de Dados.")

    def montaTabelas(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS frutas(
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(40) NOT NULL, 
                qtd FLOAT,
                preco FLOAT
            );        
        """)
        self.conn.commit()
        print("Banco de Dados criado!")

    def variaveis(self):
        self.qtdLar = self.entry_quantidade_lar.get()
        self.qtdMor = self.entry_quantidade_mor.get()
        self.qtdKi = self.entry_quantidade_ki.get()
        self.qtdBan = self.entry_quantidade_ban.get()
        self.qtdMe = self.entry_quantidade_me.get()
        self.qtdUv = self.entry_quantidade_uv.get()
        self.qtdMa = self.entry_quantidade_ma.get()
        self.qtdMela = self.entry_quantidade_mela.get()
        self.qtdAba = self.entry_quantidade_aba.get()

        self.produtosQtd = [self.qtdLar, self.qtdMor, self.qtdKi, self.qtdBan, self.qtdMe, self.qtdUv, self.qtdMa, self.qtdMela, self.qtdAba]

        self.produtos = ['Laranja', 'Morango', 'Kiwi', 'Banana', 'Melão', 'Uva', 'Maçã', 'Melancia', 'Abacaxi']
        self.precos = [2, 10, 7.50, 4, 5.50, 8.50, 3, 15, 9]

        self.itens = []
        for i in range(len(self.produtosQtd)):
            qtd = self.produtosQtd[i]
            if qtd != '':
                qtd = float(qtd)
                if qtd > 0:
                    produto = self.produtos[i]
                    preco = self.precos[i]
                    self.itens.append([produto, qtd, preco])

    def add_carrinho(self):
        self.variaveis()
        self.conecta_bd()
        self.montaTabelas()
        for item in self.itens:
            if item[1] > 0:  # Verifica se a quantidade é maior que 0
                self.cursor.execute(""" INSERT INTO frutas(nome, qtd, preco)
                VALUES(?, ?, ?)""", (item[0], item[1], item[2]))
                print(item[0], item[1], item[2])
                self.conn.commit()
        self.desconecta_bd()

    def pegar_treeview(self, treeview):
        self.treeview = treeview

    def select_lista(self):
        self.conecta_bd()
        self.listaCar.delete(*self.listaCar.get_children())
        lista = self.cursor.execute(""" SELECT cod, nome, qtd, preco FROM frutas 
        ORDER BY nome ASC; """)
        for i in lista:
            self.listaCar.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCar.selection()
        for n in self.listaCar.selection():
            col1, col2, col3, col4 = self.listaCar.item(n, "values")
            self.cod_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.qtd_entry.insert(END, col3)
            self.preco_entry.insert(END, col4)

    def deleta(self, nome):
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM frutas WHERE nome = ? """, (nome,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def calcular_total(self):
        self.conecta_bd()
        total = self.cursor.execute("SELECT SUM(preco * qtd) FROM frutas").fetchone()[0]
        self.desconecta_bd()
        return total   
        
    def finalizar_compra(self):
        total = self.calcular_total()
        messagebox.showinfo("Total da Compra", f"Total: R$ {total:.2f}")

    def limpar_campos_frame2(self):
        self.entry_quantidade_lar.delete(0, END)
        self.entry_quantidade_mor.delete(0, END)
        self.entry_quantidade_ki.delete(0, END)
        self.entry_quantidade_ban.delete(0, END)
        self.entry_quantidade_me.delete(0, END)
        self.entry_quantidade_uv.delete(0, END)
        self.entry_quantidade_ma.delete(0, END)
        self.entry_quantidade_mela.delete(0, END)
        self.entry_quantidade_aba.delete(0, END)

class Application(Func):
    def __init__(self):
        self.root = root
        self.treeview = ''
        self.tela()
        self.frame_de_tela()
        self.lista_frames()
        self.montaTabelas()
        self.select_lista()
        root.mainloop()

    def tela(self):
        self.root.title("l")
        self.root.geometry("1366x768")
        self.root.resizable(False, False)

    def frame_de_tela(self):
        self.frame1 = Frame(self.root)  # Primeiro frame
        self.frame1.pack()

        # Carregar a imagem
        self.image1 = PhotoImage(file="p1.png")

        # Exibir a imagem na primeira frame
        self.canvas1 = Canvas(self.frame1, width=1366, height=768)
        self.canvas1.pack()
        self.canvas1.create_image(0, 0, anchor="nw", image=self.image1)

        # Exibir a imagem na primeira frame
        self.canvas1 = Canvas(self.frame1, width=1366, height=768)
        self.canvas1.pack()
        self.canvas1.create_image(0, 0, anchor="nw", image=self.image1)

        self.bt_entrar = Button(self.frame1, cursor='heart', relief='ridge',command=self.show_frame2, text='COMEÇAR A COMPRAR', bd=2, bg='black', fg='white')
        self.bt_entrar.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
    
        self.frame2 = Frame(self.root, bd=4, bg='#CEDFC6', highlightbackground='black', highlightthickness=2)
        self.frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame3 = Frame(self.root, bd=4, bg='green', highlightbackground='black', highlightthickness=2)
        self.frame3.place(relx=0, rely=0, relwidth=1, relheight=0.46)

        # Carregar a imagem da segunda frame
        self.image2 = PhotoImage(file="c.png")

        # Exibir a imagem na segunda frame
        self.canvas2 = Canvas(self.frame2, width=1366, height=768)
        self.canvas2.grid(row=0, column=0, sticky="nsew")
        self.canvas2.create_image(0, 0, anchor="nw", image=self.image2)

        #BOTÃO VOLTAR
        self.bt_home = Button(self.frame2, text='HOME', command=self.show_frame1,cursor="heart",relief='ridge', bd=2, bg='yellow', fg='black')
        self.bt_home.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.bt_carrinho = Button(self.frame2, text='CARRINHO', command=lambda: self.show_frame3(self.frame3),cursor="heart",relief='ridge', bd=2, bg='yellow', fg='black')
        self.bt_carrinho.grid(row=0, column=0, padx=1270, pady=10, sticky="nw")

        self.bt_voltar2 = Button(self.frame3, text='VOLTAR', command=self.show_frame2,cursor="heart",relief='ridge', bd=2, bg='yellow', fg='black')
        self.bt_voltar2.grid(row=0, column=0, padx=10, pady=310, sticky="nw")

        #BOTÃO ADICIONAR NO CARRINHO
        self.bt_add = Button(self.frame2, text='Adicionar ao carrinho',relief='ridge', bd=2, bg='green', fg='white', command=self.add_carrinho)
        self.bt_add.grid(row=0, column=0, padx=620, pady=10, sticky="nw")

        #BOTÃO DELETAR
        self.bt_deleta = Button(self.frame3, text='Remover', relief='ridge', bd=2, bg='red', fg='white', command=lambda: self.deleta(self.nome_entry.get()))
        self.bt_deleta.grid(row=0, column=0, padx=870, pady=310, sticky="nw")

        self.nome_entry = Entry(self.frame3, width=10)
        self.nome_entry.grid(row=0, column=0, padx=802, pady=313, sticky="nw")

        #BOTÃO FINALIZAR COMPRA
        self.bt_finalizar = Button(self.frame3, text='Finalizar compra', relief='ridge', bd=2, bg='yellow', fg='black', command=self.finalizar_compra)
        self.bt_finalizar.grid(row=0, column=0, padx=940, pady=310, sticky="nw")

        #LARANJA
        self.label_quantidade_lar = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_lar.grid(row=0, column=0, padx=265, pady=180, sticky="nw")

        self.entry_quantidade_lar = Entry(self.frame2, width=4)
        self.entry_quantidade_lar.grid(row=0, column=0, padx=265, pady=150, sticky="nw")

        #MORANGO
        self.label_quantidade_mor = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_mor.grid(row=0, column=0, padx=701, pady=180, sticky="nw")

        self.entry_quantidade_mor = Entry(self.frame2, width=4)
        self.entry_quantidade_mor.grid(row=0, column=0, padx=701, pady=150, sticky="nw")

        #KIWI
        self.label_quantidade_ki = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_ki.grid(row=0, column=0, padx=1170, pady=180, sticky="nw")

        self.entry_quantidade_ki = Entry(self.frame2, width=4)
        self.entry_quantidade_ki.grid(row=0, column=0, padx=1170, pady=150, sticky="nw")

        #BANANA
        self.label_quantidade_ban = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_ban.grid(row=0, column=0, padx=265, pady=390, sticky="nw")

        self.entry_quantidade_ban = Entry(self.frame2, width=4)
        self.entry_quantidade_ban.grid(row=0, column=0, padx=265, pady=360, sticky="nw")

        #MELÃO
        self.label_quantidade_me = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_me.grid(row=0, column=0, padx=701, pady=390, sticky="nw")

        self.entry_quantidade_me = Entry(self.frame2, width=4)
        self.entry_quantidade_me.grid(row=0, column=0, padx=701, pady=360, sticky="nw")

        #UVA
        self.label_quantidade_uv = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_uv.grid(row=0, column=0, padx=1170, pady=390, sticky="nw")

        self.entry_quantidade_uv = Entry(self.frame2, width=4)
        self.entry_quantidade_uv.grid(row=0, column=0, padx=1169, pady=360, sticky="nw")

        #MAÇÃ
        self.label_quantidade_ma = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_ma.grid(row=0, column=0, padx=265, pady=630, sticky="nw")

        self.entry_quantidade_ma = Entry(self.frame2, width=4)
        self.entry_quantidade_ma.grid(row=0, column=0, padx=265, pady=599, sticky="nw")

        #MELANCIA
        self.label_quantidade_mela = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_mela.grid(row=0, column=0, padx=701, pady=630, sticky="nw")

        self.entry_quantidade_mela = Entry(self.frame2, width=4)
        self.entry_quantidade_mela.grid(row=0, column=0, padx=701, pady=599, sticky="nw")

        #ABACAXI
        self.label_quantidade_aba = Label(self.frame2, text='Insira a quantidade desejada')
        self.label_quantidade_aba.grid(row=0, column=0, padx=1169, pady=630, sticky="nw")

        self.entry_quantidade_aba = Entry(self.frame2, width=4)
        self.entry_quantidade_aba.grid(row=0, column=0, padx=1169, pady=599, sticky="nw")

        # Mostrar a primeira frame inicialmente
        self.show_frame1()

        self.root.mainloop()

    def show_frame1(self):
        self.frame1.tkraise()  # Exibir a primeira frame
        self.root.title("Home - Frame 1")  # Atualizar o título da janela

    def show_frame2(self):
        self.limpar_campos_frame2() # Limpar os campos
        self.frame2.tkraise()  # Exibir a segunda frame
        self.root.title("Catálogo - Frame 2")  # Atualizar o título da janela]

    def show_frame3(self, frame3):
        # self.lista_frames()
        self.listaCar = ttk.Treeview(frame3, height=3, columns=("col1","col2","col3", "col4"))

        self.listaCar.heading("#0", text=" ")
        self.listaCar.heading("#1", text="Código", anchor=CENTER)
        self.listaCar.heading("#2", text="Nome", anchor=CENTER)
        self.listaCar.heading("#3", text="Quantidade", anchor=CENTER)
        self.listaCar.heading("#4", text="Valor(un)", anchor=CENTER)

        self.listaCar.column("#0", width=0, stretch=0)
        self.listaCar.column("#1", width=50, anchor=CENTER)
        self.listaCar.column("#2", width=200, anchor=CENTER)
        self.listaCar.column("#3", width=125, anchor=CENTER)
        self.listaCar.column("#4", width=125, anchor=CENTER)
        self.listaCar.place(relx=0.01, rely=0.01, relwidth= 0.95, relheight= 0.85)
        
        frame3.tkraise()  # Exibir a segunda frame
        self.root.title("Carrinho - Frame 3")  # Atualizar o título da janela
        self.select_lista()

    # def lista_frames(self):
    #     self.variaveis()
    #     self.listaCar = ttk.Treeview(self.frame3, height=3, columns=("col1","col2","col3", "col4"))

    #     self.listaCar.heading("#0", text=" ")
    #     self.listaCar.heading("#1", text="Código")
    #     self.listaCar.heading("#2", text="Nome")
    #     self.listaCar.heading("#3", text="Quantidade")
    #     self.listaCar.heading("#4", text="Valor(un)")

    #     self.listaCar.column("#0", width=1)
    #     self.listaCar.column("#1", width=50)
    #     self.listaCar.column("#2", width=200)
    #     self.listaCar.column("#3", width=125)
    #     self.listaCar.column("#4", width=125)
    #     self.listaCar.place(relx=0.01, rely=0.01, relwidth= 0.95, relheight= 0.85)
    
        # self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        # self.listaCar.configure(yscrollcommand=self.scroolLista.set)
        # self.scroolLista.place(relx=0.96, rely=0.01, relwidth=0.04, relheight=0.85)
        # self.listaCar.bind('<Double-1>', self.OnDoubleClick)
# --
app = Application()
