import matplotlib.pyplot as plt
import sqlite3
import csv
from datetime import datetime

def conectar_bd():
    conn = sqlite3.connect('meu_estoque.db')
    conn.row_factory = sqlite3.Row 
    return conn

def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            quantidade REAL,
            unidade TEXT,
            valor_unitario REAL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT,
            salario REAL,
            data_contratacao TEXT
        );
    """)
    
    conn.commit()
    conn.close()

def cadastrar_produto():
    nome = input("Nome do produto: ").strip().lower()
    
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome FROM estoque WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("Produto já cadastrado. Use a opção 2 para adicionar.")
        conn.close()
        return

    try:
        qtd = float(input("Quantidade inicial: "))
        if qtd < 0:
            print("Erro: A quantidade deve ser um número positivo.")
            conn.close()
            return

        unidade = input("Unidade de medida (ex: KG, UN, LT, M): ").strip().upper()

        valor_str = input("Valor unitário (R$ por unidade): ").replace(',', '.')
        valor = float(valor_str)
        if valor < 0:
            print("Erro: O valor deve ser um número positivo.")
            conn.close()
            return
            
        cursor.execute("""
            INSERT INTO estoque (nome, quantidade, unidade, valor_unitario) 
            VALUES (?, ?, ?, ?)
        """, (nome, qtd, unidade, valor))
        
        conn.commit()
        print(f"Produto '{nome.capitalize()}' cadastrado com sucesso no DB!")
        
    except ValueError:
        print("Erro: Digite valores numéricos válidos para quantidade e valor.")
    except sqlite3.IntegrityError:
         print("Erro de integridade: Produto já existe ou dado inválido.")
    finally:
        conn.close()


def adicionar_quantidade():
    nome = input("Nome do produto: ").strip().lower()
    
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantidade, unidade FROM estoque WHERE nome = ?", (nome,))
    produto = cursor.fetchone()
    
    if produto:
        try:
            unidade = produto['unidade']
            qtd_adicionar = float(input(f"Quantidade a adicionar ({unidade}): "))
            if qtd_adicionar <= 0:
                print("Erro: Digite uma quantidade positiva para adicionar.")
                conn.close()
                return

            nova_qtd = produto['quantidade'] + qtd_adicionar
            
            cursor.execute("""
                UPDATE estoque SET quantidade = ? WHERE nome = ?
            """, (nova_qtd, nome))
            
            conn.commit()
            print(f"{qtd_adicionar:.2f} {unidade} adicionadas ao produto '{nome.capitalize()}'.")
        except ValueError:
            print("Erro: Digite uma quantidade numérica válida.")
        finally:
            conn.close()
    else:
        print("Produto não encontrado. Cadastre primeiro (Opção 1).")
        conn.close()


def baixar_produto():
    nome = input("Nome do produto: ").strip().lower()

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade, unidade FROM estoque WHERE nome = ?", (nome,))
    produto = cursor.fetchone()

    if produto:
        try:
            unidade = produto['unidade']
            qtd_atual = produto['quantidade']
            qtd_baixar = float(input(f"Quantidade a baixar ({unidade}): "))
            
            if qtd_baixar <= 0:
                print("Erro: Digite uma quantidade positiva para baixar.")
                return
            
            if qtd_baixar <= qtd_atual:
                nova_qtd = qtd_atual - qtd_baixar
                
                if nova_qtd < 0.001: 
                    cursor.execute("DELETE FROM estoque WHERE nome = ?", (nome,))
                    print(f"Produto '{nome.capitalize()}' removido do estoque (zerado).")
                else:
                    cursor.execute("UPDATE estoque SET quantidade = ? WHERE nome = ?", (nova_qtd, nome))
                    print(f"{qtd_baixar:.2f} {unidade} baixadas do produto '{nome.capitalize()}'.")
                    
                conn.commit()
            else:
                print(f"Erro: Quantidade insuficiente. Máximo disponível: {qtd_atual:.2f} {unidade}.")
        except ValueError:
            print("Erro: Digite uma quantidade numérica válida.")
        finally:
            conn.close()
    else:
        print("Produto não encontrado.")
        conn.close()


def visualizar_estoque():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, quantidade, unidade, valor_unitario FROM estoque ORDER BY nome")
    produtos = cursor.fetchall()
    conn.close()
    
    if not produtos:
        print("Estoque vazio.")
        return

    print("\n--- ESTOQUE ATUAL ---")
    total_geral = 0
    print(f"{'Item':<4} | {'Produto':<15} | {'Qtd':<8} | {'Un.':<4} | {'Val. Unit.':<12} | {'Val. Total':<12}")
    print("-" * 62)

    item_num = 1
    for produto in produtos:
        nome = produto['nome']
        qtd = produto['quantidade']
        unidade = produto['unidade']
        valor_unit = produto['valor_unitario']
        
        total = qtd * valor_unit
        total_geral += total
        
        print(f"{item_num:<4} | {nome.capitalize():<15} | {qtd:8.2f} | {unidade:<4} | R$ {valor_unit:8.2f} | R$ {total:8.2f}")
        item_num += 1
    
    print("-" * 62)
    print(f"{'VALOR TOTAL GERAL DO ESTOQUE':<49} R$ {total_geral:8.2f}")
    print("-" * 62)


def mostrar_grafico():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, quantidade, valor_unitario FROM estoque")
    produtos = cursor.fetchall()
    conn.close()
    
    if not produtos:
        print("Estoque vazio. Nada para mostrar.")
        return

    nomes = [p['nome'].capitalize() for p in produtos]
    valores_totais = [p['quantidade'] * p['valor_unitario'] for p in produtos]
    
    plt.figure(figsize=(12, 6))
    barras = plt.bar(nomes, valores_totais, color=['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0'])
    
    plt.title('Valor Total em Estoque por Produto', fontsize=16)
    plt.xlabel('Produto', fontsize=12)
    plt.ylabel('Valor Total (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right') 
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    for bar, valor in zip(barras, valores_totais):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f'R$ {valor:.2f}', ha='center', va='bottom', fontsize=10, weight='bold')

    plt.show()


def importar_produtos_csv(nome_arquivo='produtos.csv'):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    produtos_importados = 0
    produtos_ignorados = 0

    try:
        with open(nome_arquivo, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                nome = row['nome'].strip().lower()
                
                try:
                    qtd = float(row['quantidade'].replace(',', '.'))
                    valor = float(row['valor_unitario'].replace(',', '.'))
                    unidade = row['unidade'].strip().upper()
                except ValueError:
                    print(f"AVISO: Linha com erro de valor numérico ignorada (Produto: {nome.capitalize()}).")
                    produtos_ignorados += 1
                    continue
                
                try:
                    cursor.execute("""
                        INSERT INTO estoque (nome, quantidade, unidade, valor_unitario) 
                        VALUES (?, ?, ?, ?)
                    """, (nome, qtd, unidade, valor))
                    produtos_importados += 1
                    
                except sqlite3.IntegrityError:
                    print(f"AVISO: Produto '{nome.capitalize()}' já existe e foi ignorado.")
                    produtos_ignorados += 1

        conn.commit()
        print("\n" + "="*40)
        print(f"IMPORTAÇÃO CONCLUÍDA:")
        print(f"-> {produtos_importados} produtos importados com sucesso.")
        print(f"-> {produtos_ignorados} produtos ignorados (erro de valor ou duplicidade).")
        print("="*40)
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{nome_arquivo}' não encontrado. Crie o '{nome_arquivo}' na pasta do projeto.")
    finally:
        conn.close()

def cadastrar_funcionario():
    nome = input("Nome do funcionário: ").strip().title()
    cargo = input("Cargo: ").strip().title()
    
    conn = conectar_bd()
    cursor = conn.cursor()
    
    try:
        salario_str = input("Salário (R$): ").replace(',', '.')
        salario = float(salario_str)
        if salario < 0:
            print("Erro: O salário deve ser um número positivo.")
            conn.close()
            return
            
        data_input = input(f"Data de contratação (AAAA-MM-DD, vazio para hoje): ").strip()
        data_contratacao = data_input if data_input else datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT INTO funcionarios (nome, cargo, salario, data_contratacao) 
            VALUES (?, ?, ?, ?)
        """, (nome, cargo, salario, data_contratacao))
        
        conn.commit()
        print(f"Funcionário '{nome}' ({cargo}) cadastrado com sucesso!")
        
    except ValueError:
        print("Erro: Digite um valor numérico válido para o salário.")
    finally:
        conn.close()

def listar_funcionarios():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cargo, salario, data_contratacao FROM funcionarios ORDER BY nome")
    funcionarios = cursor.fetchall()
    conn.close()
    
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return

    print("\n--- LISTA DE FUNCIONÁRIOS ---")
    print(f"{'ID':<4} | {'Nome':<20} | {'Cargo':<15} | {'Salário':<12} | {'Contratação':<12}")
    print("-" * 68)

    for func in funcionarios:
        salario_formatado = f"R$ {func['salario']:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
        
        print(f"{func['id']:<4} | {func['nome']:<20} | {func['cargo']:<15} | {salario_formatado:<12} | {func['data_contratacao']:<12}")
    
    print("-" * 68)

def buscar_funcionario_por_nome():
    busca = input("Digite o nome ou parte do nome do funcionário: ").strip().lower()
    
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nome, cargo, salario, data_contratacao FROM funcionarios 
        WHERE nome LIKE ? 
        ORDER BY nome
    """, (f'%{busca}%',))
    
    funcionarios = cursor.fetchall()
    conn.close()
    
    if not funcionarios:
        print(f"Nenhum funcionário encontrado com o nome ou parte do nome '{busca}'.")
        return

    print(f"\n--- RESULTADOS DA BUSCA ({len(funcionarios)}) ---")
    print(f"{'ID':<4} | {'Nome':<20} | {'Cargo':<15} | {'Salário':<12} | {'Contratação':<12}")
    print("-" * 68)

    for func in funcionarios:
        salario_formatado = f"R$ {func['salario']:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
        
        print(f"{func['id']:<4} | {func['nome']:<20} | {func['cargo']:<15} | {salario_formatado:<12} | {func['data_contratacao']:<12}")
    
    print("-" * 68)

def calcular_media_salarial():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT AVG(salario) AS media_salarial, COUNT(id) AS total_funcionarios FROM funcionarios")
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and resultado['total_funcionarios'] > 0:
        media = resultado['media_salarial']
        total = resultado['total_funcionarios']
        media_formatada = f"R$ {media:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')

        print("\n--- ESTATÍSTICAS SALARIAIS ---")
        print(f"Total de funcionários: {total}")
        print(f"Média salarial da empresa: {media_formatada}")
        print("-" * 30)
    else:
        print("Não há funcionários para calcular a média salarial.")

def remover_funcionario():
    print("\n--- REMOVER FUNCIONÁRIO ---")
    
    try:
        id_remover = int(input("Digite o ID do funcionário a ser removido: "))
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, cargo FROM funcionarios WHERE id = ?", (id_remover,))
    funcionario = cursor.fetchone()
    
    if not funcionario:
        print(f"Erro: Funcionário com ID {id_remover} não encontrado.")
        conn.close()
        return

    nome = funcionario['nome']
    cargo = funcionario['cargo']
    
    confirmacao = input(f"CONFIRMAÇÃO: Deseja realmente remover {nome} ({cargo})? (S/N): ").strip().upper()
    
    if confirmacao == 'S':
        try:
            cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_remover,))
            conn.commit()
            print(f"Funcionário '{nome}' removido com sucesso do sistema.")
        except Exception as e:
            print(f"Ocorreu um erro ao remover: {e}")
        finally:
            conn.close()
    else:
        print("Operação de remoção cancelada.")

def menu_funcionarios():
    while True:
        print("\n" + "="*25)
        print("   GERENCIAMENTO DE PESSOAL")
        print("="*25)
        print("1 - Cadastrar novo funcionário")
        print("2 - Listar todos os funcionários")
        print("3 - Buscar funcionário por nome")
        print("4 - Calcular média salarial")
        print("5 - Remover funcionário")
        print("0 - Voltar ao menu principal")

        escolha = input("Escolha uma opção (0 a 5): ").strip()

        if escolha == "0":
            break
        elif escolha == "1":
            cadastrar_funcionario()
        elif escolha == "2":
            listar_funcionarios()
        elif escolha == "3":
            buscar_funcionario_por_nome()
        elif escolha == "4":
            calcular_media_salarial()
        elif escolha == "5":
            remover_funcionario()
        else:
            print("Opção inválida. Digite um número de 0 a 5.")

def menu_principal():
    while True:
        print("\n" + "="*20)
        print("   SISTEMA DE ESTOQUE ERP")
        print("="*20)
        print("1 - Cadastrar novo produto")
        print("2 - Adicionar quantidade")
        print("3 - Baixar produto")
        print("4 - Visualizar estoque")
        print("5 - Mostrar gráfico de valores")
        print("6 - Importar produtos de CSV")
        print("7 - Gerenciamento de Funcionários")
        print("0 - Sair do sistema")

        escolha = input("Escolha uma opção (0 a 7): ").strip()

        if escolha == "0":
            print("Saindo do sistema. Até logo!")
            break
        elif escolha == "1":
            cadastrar_produto()
        elif escolha == "2":
            adicionar_quantidade()
        elif escolha == "3":
            baixar_produto()
        elif escolha == "4":
            visualizar_estoque()
        elif escolha == "5":
            mostrar_grafico()
        elif escolha == "6":
            importar_produtos_csv()
        elif escolha == "7":
            menu_funcionarios()
        else:
            print("Opção inválida. Digite um número de 0 a 7.")

if __name__ == "__main__":
    criar_tabelas() 
    menu_principal()