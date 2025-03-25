import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from placeholder import EntryPlaceHolder
from tkcalendar import DateEntry

# Conectar ao banco de dados
conn = sqlite3.connect('casamento.db')
cursor = conn.cursor()

# Criar tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS convidados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    contato TEXT NOT NULL,
    confirmacao TEXT CHECK(confirmacao IN ('Sim', 'Não', 'Pendente')),
    funcao TEXT CHECK(funcao IN ('Convidado', 'Madrinha', 'Padrinho')) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS fornecedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    servico TEXT NOT NULL,
    contato TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS financeiro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK(tipo IN ('Entrada', 'Saída')) NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
)
''')

conn.commit()

def adicionar_convidado():
    nome = entry_nome_convidado.get()
    contato = entry_contato_convidado.get()
    confirmacao = combo_confirmacao.get()
    funcao = combo_funcao.get()
    if nome and contato:
        cursor.execute('INSERT INTO convidados (nome, contato, confirmacao, funcao) VALUES (?, ?, ?, ?)', (nome, contato, confirmacao, funcao))
        conn.commit()
        entry_nome_convidado.delete(0, tk.END)
        atualizar_lista_convidados()
    else:
        messagebox.showwarning("Atenção", "Nome do convidado não pode estar vazio.")

def abrir_tela_edicao_convidados():
    selected_item = lista_convidados.selection()
    if selected_item:
        item = lista_convidados.item(selected_item)
        convidado_id, nome_atual, contato_atual, confirmacao_atual, funcao_atual = item['values']
        
        def salvar_edicao():
            novo_nome = entry_nome_editar.get()
            novo_contato = entry_contato_editar.get()
            nova_funcao = combo_funcao_editar.get()
            nova_confirmacao = combo_confirmacao_editar.get()
            if novo_nome:
                cursor.execute('UPDATE convidados SET nome = ?, contato = ?, funcao = ?, confirmacao = ? WHERE id = ?', 
                               (novo_nome, novo_contato, nova_funcao, nova_confirmacao, convidado_id))
                conn.commit()
                atualizar_lista_convidados()
                janela_edicao.destroy()
            else:
                messagebox.showwarning("Atenção", "Nome e contato não podem estar vazios.")
        
        def deletar_convidado():
            confirma_delete = tk.Toplevel(root)
            confirma_delete.title("Tem certeza?")
            
            ttk.Label(confirma_delete, text="Você tem certeza que deseja deletar este convidado?").grid(row=0, column=0, columnspan=2)
            ttk.Button(confirma_delete, width=20, text="Sim", command=deletar).grid(row=1, column=0)
            ttk.Button(confirma_delete, width=20, text="Não", command=confirma_delete.destroy).grid(row=1, column=1)

        def deletar():
            cursor.execute('DELETE FROM convidados WHERE id = ?', (convidado_id,))
            conn.commit()
            atualizar_lista_convidados()

        janela_edicao = tk.Toplevel(root)
        janela_edicao.title("Editar Convidado")
        
        ttk.Label(janela_edicao, text="Nome:").grid(row=0, column=0)
        entry_nome_editar = ttk.Entry(janela_edicao, width=20)
        entry_nome_editar.grid(row=0, column=1)
        entry_nome_editar.insert(0, nome_atual)
        
        ttk.Label(janela_edicao, text="Contato:").grid(row=1, column=0)
        entry_contato_editar = ttk.Entry(janela_edicao, width=20)
        entry_contato_editar.grid(row=1, column=1)
        entry_contato_editar.insert(0, contato_atual)
        
        ttk.Label(janela_edicao, text="Confirmação:").grid(row=2, column=0)
        combo_confirmacao_editar = ttk.Combobox(janela_edicao, width=20, values=["Sim", "Não", "Pendente"])
        combo_confirmacao_editar.grid(row=2, column=1)
        combo_confirmacao_editar.set(confirmacao_atual)
        
        ttk.Label(janela_edicao, text="Função:").grid(row=3, column=0)
        combo_funcao_editar = ttk.Combobox(janela_edicao, width=20, values=["Convidado", "Madrinha", "Padrinho"])
        combo_funcao_editar.grid(row=3, column=1)
        combo_funcao_editar.set(funcao_atual)
        
        ttk.Button(janela_edicao, width=20, text="Salvar", command=salvar_edicao).grid(row=4, column=0)
        ttk.Button(janela_edicao, width=20, text="Deletar", command=deletar_convidado).grid(row=4, column=1)
    else:
        messagebox.showwarning("Atenção", "Selecione um convidado para editar.")


def atualizar_lista_convidados():
    lista_convidados.delete(*lista_convidados.get_children())
    cursor.execute('SELECT * FROM convidados')
    for row in cursor.fetchall():
        lista_convidados.insert('', tk.END, values=row)

def adicionar_fornecedor():
    nome = entry_nome_fornecedor.get()
    servico = entry_servico_fornecedor.get()
    contato = entry_contato_fornecedor.get()
    if nome and servico and contato:
        cursor.execute('INSERT INTO fornecedores (nome, servico, contato) VALUES (?, ?, ?)', (nome, servico, contato))
        conn.commit()
        entry_nome_fornecedor.delete(0, tk.END)
        entry_servico_fornecedor.delete(0, tk.END)
        entry_contato_fornecedor.delete(0, tk.END)
        atualizar_lista_fornecedores()
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

def abrir_tela_edicao_fornecedores():
    selected_item = lista_fornecedores.selection()
    if selected_item:
        item = lista_fornecedores.item(selected_item)
        fornecedor_id, nome_atual, servico_atual, contato_atual = item['values']
        
        def salvar_edicao_fornecedores():
            novo_nome = entry_nome_editar.get()
            novo_contato = entry_contato_editar.get()
            novo_servico = entry_servico_editar.get()
            if novo_nome:
                cursor.execute('UPDATE fornecedores SET nome = ?, servico = ?, contato = ? WHERE id = ?', 
                               (novo_nome, novo_servico, novo_contato, fornecedor_id))
                conn.commit()
                atualizar_lista_fornecedores()
                janela_edicao.destroy()
            else:
                messagebox.showwarning("Atenção", "Nome e contato não podem estar vazios.")
        
        def deletar_fornecedor():
            confirma_delete = tk.Toplevel(root)
            confirma_delete.title("Tem certeza?")
            
            ttk.Label(confirma_delete, text="Você tem certeza que deseja deletar este convidado?").grid(row=0, column=0, columnspan=2)
            ttk.Button(confirma_delete, width=20, text="Sim", command=deletar).grid(row=1, column=0)
            ttk.Button(confirma_delete, width=20, text="Não", command=confirma_delete.destroy).grid(row=1, column=1)

        def deletar():
            cursor.execute('DELETE FROM fornecedores WHERE id = ?', (fornecedor_id,))
            conn.commit()
            atualizar_lista_fornecedores()

        janela_edicao = tk.Toplevel(root)
        janela_edicao.title("Editar Convidado")
        
        ttk.Label(janela_edicao, text="Nome:").grid(row=0, column=0)
        entry_nome_editar = ttk.Entry(janela_edicao, width=20)
        entry_nome_editar.grid(row=0, column=1)
        entry_nome_editar.insert(0, nome_atual)
        
        ttk.Label(janela_edicao, text="Serviço:").grid(row=1, column=0)
        entry_servico_editar = ttk.Entry(janela_edicao, width=20)
        entry_servico_editar.grid(row=1, column=1)
        entry_servico_editar.insert(0, servico_atual)
        
        ttk.Label(janela_edicao, text="Contato:").grid(row=2, column=0)
        entry_contato_editar = ttk.Entry(janela_edicao, width=20)
        entry_contato_editar.grid(row=2, column=1)
        entry_contato_editar.insert(0, contato_atual)
        
        ttk.Button(janela_edicao, width=20, text="Salvar", command=salvar_edicao_fornecedores).grid(row=3, column=0)
        ttk.Button(janela_edicao, width=20, text="Deletar", command=deletar_fornecedor).grid(row=3, column=1)
    else:
        messagebox.showwarning("Atenção", "Selecione um convidado para editar.")

def atualizar_lista_fornecedores():
    lista_fornecedores.delete(*lista_fornecedores.get_children())
    cursor.execute('SELECT * FROM fornecedores')
    for row in cursor.fetchall():
        lista_fornecedores.insert('', tk.END, values=row)

def adicionar_transacao():
    tipo = combo_tipo_transacao.get()
    descricao = entry_descricao_transacao.get()
    valor = entry_valor_transacao.get()
    data = entry_data_transacao.get()
    if descricao and valor and data:
        cursor.execute('INSERT INTO financeiro (tipo, descricao, valor, data) VALUES (?, ?, ?, ?)', (tipo, descricao, valor, data))
        conn.commit()
        entry_descricao_transacao.delete(0, tk.END)
        entry_valor_transacao.delete(0, tk.END)
        entry_data_transacao.delete(0, tk.END)
        atualizar_lista_financeiro()
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

def abrir_tela_edicao_financeiro():
    selected_item = lista_financeiro.selection()
    if selected_item:
        item = lista_financeiro.item(selected_item)
        financeiro_id, tipo_atual, descricao_atual, valor_atual, data_atual = item['values']
        
        def salvar_edicao_financeiro():
            novo_tipo = combo_tipo_editar.get()
            nova_descricao = entry_descricao_editar.get()
            novo_valor = entry_valor_editar.get()
            nova_data = entry_data_editar.get()
            if novo_tipo and novo_valor and nova_data and nova_descricao:
                cursor.execute('UPDATE financeiro SET tipo = ?, descricao = ?, valor = ?, data = ? WHERE id = ?', 
                               (novo_tipo, nova_descricao, novo_valor, nova_data, financeiro_id))
                conn.commit()
                atualizar_lista_financeiro()
                janela_edicao.destroy()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")
        
        def deletar_financeiro():
            ttk.Label(janela_edicao, text="Você tem certeza que deseja deletar este convidado?").grid(row=5, column=0, columnspan=2)
            ttk.Button(janela_edicao, width=20, text="Sim", command=deletar).grid(row=6, column=0)
            ttk.Button(janela_edicao, width=20, text="Não", command=janela_edicao.destroy).grid(row=6, column=1)
                
        def deletar():
            cursor.execute('DELETE FROM financeiro WHERE id = ?', (financeiro_id,))
            conn.commit()
            atualizar_lista_financeiro()
            janela_edicao.destroy()
            
        janela_edicao = tk.Toplevel(root)
        janela_edicao.title("Editar Convidado")
        
        ttk.Label(janela_edicao, text="Tipo:").grid(row=0, column=0)
        combo_tipo_editar = ttk.Combobox(janela_edicao, width=17, values=["Entrada", "Saída"])
        combo_tipo_editar.grid(row=0, column=1)
        combo_tipo_editar.insert(0, tipo_atual)
        
        ttk.Label(janela_edicao, text="Descrição:").grid(row=1, column=0)
        entry_descricao_editar = ttk.Entry(janela_edicao, width=20)
        entry_descricao_editar.grid(row=1, column=1)
        entry_descricao_editar.insert(0, descricao_atual)
        
        ttk.Label(janela_edicao, text="Valor:").grid(row=2, column=0)
        entry_valor_editar = ttk.Entry(janela_edicao, width=20)
        entry_valor_editar.grid(row=2, column=1)
        entry_valor_editar.insert(0, valor_atual)
        
        ttk.Label(janela_edicao, text="Data:").grid(row=3, column=0)
        entry_data_editar = DateEntry(janela_edicao, width=15, date_pattern='dd/MM/yyyy', selectmode='day')
        entry_data_editar.grid(row=3, column=1)
        entry_data_editar.insert(0, data_atual)
        
        ttk.Button(janela_edicao, width=20, text="Salvar", command=salvar_edicao_financeiro).grid(row=4, column=0)
        ttk.Button(janela_edicao, width=20, text="Deletar", command=deletar_financeiro).grid(row=4, column=1)
    else:
        messagebox.showwarning("Atenção", "Selecione um convidado para editar.")

def atualizar_lista_financeiro():
    lista_financeiro.delete(*lista_financeiro.get_children())
    cursor.execute('SELECT * FROM financeiro')
    for row in cursor.fetchall():
        lista_financeiro.insert('', tk.END, values=row)
    atualizar_saldo()
        
def atualizar_saldo():
    cursor.execute("SELECT SUM(valor) FROM financeiro WHERE tipo='Entrada'")
    entradas = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(valor) FROM financeiro WHERE tipo='Saída'")
    saidas = cursor.fetchone()[0] or 0
    saldo_final = entradas - saidas
    label_saldo_valor.config(text=f"R$ {saldo_final:.2f}")

# Criando interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Casamento")
root.geometry("1000x600")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

tabControl = ttk.Notebook(root)
tab_convidados = ttk.Frame(tabControl)
tab_fornecedores = ttk.Frame(tabControl)
tab_financeiro = ttk.Frame(tabControl)

tabControl.add(tab_convidados, text='Convidados')
tabControl.add(tab_fornecedores, text='Fornecedores')
tabControl.add(tab_financeiro, text='Financeiro')
tabControl.pack(expand=1, fill="both")

# Aba Convidados
frame_convidados = ttk.LabelFrame(tab_convidados, text="Adicionar Convidados")
frame_convidados.pack(pady=10, padx=10, fill="x")
entry_nome_convidado = EntryPlaceHolder(frame_convidados, 'Nome do convidado')
entry_nome_convidado.pack(side="left", padx=5, fill="x", expand=True)
entry_contato_convidado = EntryPlaceHolder(frame_convidados, 'Contato do convidado')
entry_contato_convidado.pack(side="left", padx=5, fill="x", expand=True)
combo_funcao = ttk.Combobox(frame_convidados, values=["Convidado", "Madrinha", "Padrinho"], width=15)
combo_funcao.pack(side="left", padx=5, fill="x", expand=True)
combo_funcao.current(0)
combo_confirmacao = ttk.Combobox(frame_convidados, values=["Sim", "Não", "Pendente"], width=10)
combo_confirmacao.pack(side="left", padx=5, fill="x", expand=True)
combo_confirmacao.current(2)
ttk.Button(frame_convidados, width=20, text="Adicionar", command=adicionar_convidado).pack(side="left", padx=5, fill="x", expand=True)
ttk.Button(frame_convidados, width=20, text="Editar", command=abrir_tela_edicao_convidados).pack(side="left", padx=5, fill="x", expand=True)

lista_convidados = ttk.Treeview(tab_convidados, height=15, columns=("ID", "Nome", "Contato", "Confirmação", "Função"), show="headings")
lista_convidados.heading("ID", text="ID")
lista_convidados.heading("Nome", text="Nome")
lista_convidados.heading("Contato", text="Contato")
lista_convidados.heading("Confirmação", text="Confirmação")
lista_convidados.heading("Função", text="Função")
lista_convidados.pack(fill="both", expand=True)
atualizar_lista_convidados()

# Aba Fornecedores
frame_fornecedores = ttk.LabelFrame(tab_fornecedores, text="Adicionar Fornecedor")
frame_fornecedores.pack(pady=10, padx=10, fill="x")
entry_nome_fornecedor = EntryPlaceHolder(frame_fornecedores, 'Nome')
entry_nome_fornecedor.pack(side="left", padx=5)
entry_servico_fornecedor = EntryPlaceHolder(frame_fornecedores, 'Serviço')
entry_servico_fornecedor.pack(side="left", padx=5)
entry_contato_fornecedor = EntryPlaceHolder(frame_fornecedores, 'Contato')
entry_contato_fornecedor.pack(side="left", padx=5)
ttk.Button(frame_fornecedores, width=20, text="Adicionar", command=adicionar_fornecedor).pack(side="left", padx=5)
ttk.Button(frame_fornecedores, width=20, text="Editar", command=abrir_tela_edicao_fornecedores).pack(side="left", padx=5)

lista_fornecedores = ttk.Treeview(tab_fornecedores, columns=("ID", "Nome", "Serviço", "Contato"), show="headings")
lista_fornecedores.heading("ID", text="ID")
lista_fornecedores.heading("Nome", text="Nome")
lista_fornecedores.heading("Serviço", text="Serviço")
lista_fornecedores.heading("Contato", text="Contato")
lista_fornecedores.pack(fill="both", expand=True)
atualizar_lista_fornecedores()

# Aba Financeiro
frame_financeiro = ttk.LabelFrame(tab_financeiro, text="Adicionar Transação")
frame_financeiro.pack(pady=10, padx=10, fill="x")
combo_tipo_transacao = ttk.Combobox(frame_financeiro, values=["Entrada", "Saída"], width=10)
combo_tipo_transacao.pack(side="left", padx=5, fill="x", expand=True)
combo_tipo_transacao.current(0)
entry_descricao_transacao = EntryPlaceHolder(frame_financeiro, 'Descrição')
entry_descricao_transacao.pack(side="left", padx=5, fill="x", expand=True)
entry_valor_transacao = EntryPlaceHolder(frame_financeiro, 'Valor')
entry_valor_transacao.pack(side="left", padx=5, fill="x", expand=True)
# entry_data_transacao = EntryPlaceHolder(frame_financeiro, 'Data')
# entry_data_transacao.pack(side="left", padx=5, fill="x", expand=True)
entry_data_transacao = DateEntry(frame_financeiro, date_pattern='dd/MM/yyyy', selectmode='day')
entry_data_transacao.pack(side="left", padx=5, fill="x", expand=True)
ttk.Button(frame_financeiro, width=20, text="Adicionar", command=adicionar_transacao).pack(side="left", padx=5)
ttk.Button(frame_financeiro, width=20, text="Editar", command=abrir_tela_edicao_financeiro).pack(side="left", padx=5)

lista_financeiro = ttk.Treeview(tab_financeiro, columns=("ID", "Tipo", "Descrição", "Valor", "Data"), show="headings")
lista_financeiro.heading("ID", text="ID")
lista_financeiro.heading("Tipo", text="Tipo")
lista_financeiro.heading("Descrição", text="Descrição")
lista_financeiro.heading("Valor", text="Valor")
lista_financeiro.heading("Data", text="Data")
lista_financeiro.pack(fill="both", expand=True)

frame_saldo = ttk.LabelFrame(tab_financeiro, text="Saldo Final")
frame_saldo.pack(pady=10, padx=10, fill="x")
label_saldo = ttk.Label(frame_saldo, text="Saldo Total:")
label_saldo.pack(side="left", padx=5)
label_saldo_valor = ttk.Label(frame_saldo, text="R$ 0.00", font=("Arial", 12, "bold"))
label_saldo_valor.pack(side="left", padx=5)

atualizar_lista_financeiro()


root.mainloop()
conn.close()
