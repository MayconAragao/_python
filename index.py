import matplotlib.pyplot as plt

# Estrutura de dados principal: Armazena produtos e seus dados
estoque = {}

# --- Funções de Manipulação do Estoque ---

def cadastrar_produto():
    """Opção 1: Cadastra um novo produto no estoque, incluindo a unidade de medida."""
    nome = input("Nome do produto: ").strip().lower()
    
    if nome in estoque:
        print("Produto já cadastrado. Use a opção 2 para adicionar.")
        return

    try:
        qtd = float(input("Quantidade inicial: ")) # Permite quantidades fracionadas (ex: 0.5 kg)
        if qtd < 0:
            print("Erro: A quantidade deve ser um número positivo.")
            return

        unidade = input("Unidade de medida (ex: KG, UN, LT, M): ").strip().upper()

        # Para lidar com valores como "10,50" ou "10.50"
        valor_str = input("Valor unitário (R$ por unidade): ").replace(',', '.')
        valor = float(valor_str)
        if valor < 0:
            print("Erro: O valor deve ser um número positivo.")
            return
            
        estoque[nome] = {
            "quantidade": qtd,
            "unidade": unidade,
            "valor_unitario": valor
        }
        print(f"Produto '{nome.capitalize()}' cadastrado com sucesso!")
        
    except ValueError:
        print("Erro: Digite valores numéricos válidos para quantidade e valor.")


def adicionar_quantidade():
    """Opção 2: Aumenta a quantidade de um produto existente."""
    nome = input("Nome do produto: ").strip().lower()

    if nome in estoque:
        try:
            qtd_adicionar = float(input(f"Quantidade a adicionar ({estoque[nome]['unidade']}): "))
            if qtd_adicionar <= 0:
                print("Erro: Digite uma quantidade positiva para adicionar.")
                return

            estoque[nome]["quantidade"] += qtd_adicionar
            print(f"{qtd_adicionar:.2f} {estoque[nome]['unidade']} adicionadas ao produto '{nome.capitalize()}'.")
        except ValueError:
            print("Erro: Digite uma quantidade numérica válida.")
    else:
        print("Produto não encontrado. Cadastre primeiro (Opção 1).")


def baixar_produto():
    """Opção 3: Diminui a quantidade de um produto (venda ou consumo)."""
    nome = input("Nome do produto: ").strip().lower()

    if nome in estoque:
        try:
            unidade = estoque[nome]["unidade"]
            qtd_baixar = float(input(f"Quantidade a baixar ({unidade}): "))
            
            if qtd_baixar <= 0:
                print("Erro: Digite uma quantidade positiva para baixar.")
                return
            
            qtd_atual = estoque[nome]["quantidade"]
            
            if qtd_baixar <= qtd_atual:
                estoque[nome]["quantidade"] -= qtd_baixar
                print(f"{qtd_baixar:.2f} {unidade} baixadas do produto '{nome.capitalize()}'.")
                
                # Remove o produto se a quantidade for zero ou muito próxima de zero
                if estoque[nome]["quantidade"] < 0.001: 
                    del estoque[nome]
                    print(f"Produto '{nome.capitalize()}' removido do estoque (zerado).")
            else:
                print(f"Erro: Quantidade insuficiente. Máximo disponível: {qtd_atual:.2f} {unidade}.")
        except ValueError:
            print("Erro: Digite uma quantidade numérica válida.")
    else:
        print("Produto não encontrado.")


def visualizar_estoque():
    """Opção 4: Mostra a lista completa de produtos em ordem numérica, incluindo a unidade."""
    if not estoque:
        print("Estoque vazio.")
        return

    print("\n--- ESTOQUE ATUAL ---")
    total_geral = 0
    # Ajustando a formatação da tabela
    print(f"{'Item':<4} | {'Produto':<15} | {'Qtd':<8} | {'Un.':<4} | {'Val. Unit.':<12} | {'Val. Total':<12}")
    print("-" * 62)

    item_num = 1
    for nome, info in estoque.items():
        qtd = info["quantidade"]
        unidade = info["unidade"]
        valor_unit = info["valor_unitario"]
        total = qtd * valor_unit
        total_geral += total
        
        # Formatação para melhor visualização
        print(f"{item_num:<4} | {nome.capitalize():<15} | {qtd:8.2f} | {unidade:<4} | R$ {valor_unit:8.2f} | R$ {total:8.2f}")
        item_num += 1
    
    print("-" * 62)
    print(f"{'VALOR TOTAL GERAL DO ESTOQUE':<49} R$ {total_geral:8.2f}")
    print("-" * 62)


def mostrar_grafico():
    """Opção 5: Gera e exibe um gráfico de barras com o valor total por produto."""
    if not estoque:
        print("Estoque vazio. Nada para mostrar.")
        return

    # Prepara os dados para o Matplotlib
    nomes = [n.capitalize() for n in estoque.keys()]
    valores_totais = [
        estoque[n]["quantidade"] * estoque[n]["valor_unitario"]
        for n in estoque.keys()
    ]
    
    # Cria o gráfico
    plt.figure(figsize=(12, 6))
    barras = plt.bar(nomes, valores_totais, color=['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0'])
    
    plt.title('Valor Total em Estoque por Produto', fontsize=16)
    plt.xlabel('Produto', fontsize=12)
    plt.ylabel('Valor Total (R$)', fontsize=12)
    
    plt.xticks(rotation=45, ha='right') 
    
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Adiciona os valores em cima das barras
    for bar, valor in zip(barras, valores_totais):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f'R$ {valor:.2f}', ha='center', va='bottom', fontsize=10, weight='bold')

    plt.show()

# --- Estrutura Principal do Programa ---

def menu_principal():
    """Gerencia a navegação do menu e a execução das funções."""
    while True:
        print("\n" + "="*20)
        print("   SISTEMA DE ESTOQUE")
        print("="*20)
        print("1 - Cadastrar novo produto")
        print("2 - Adicionar quantidade")
        print("3 - Baixar produto")
        print("4 - Visualizar estoque")
        print("5 - Mostrar gráfico de valores")
        print("0 - Sair do sistema")

        escolha = input("Escolha uma opção (0 a 5): ").strip()

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
        else:
            print("Opção inválida. Digite um número de 0 a 5.")

# Executa o programa
if __name__ == "__main__":
    menu_principal()