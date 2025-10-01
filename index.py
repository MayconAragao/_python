import matplotlib.pyplot as plt

estoque = {}

while True:
    print("\n--- MENU ---")
    print("1 - Cadastrar novo produto")
    print("2 - Adicionar quantidade a produto existente")
    print("3 - Baixar produto do estoque")
    print("4 - Visualizar estoque atual")
    print("5 - Mostrar gráfico de valores totais")
    print("0 - Sair do sistema")

    escolha = input("Escolha uma opção (0 a 5): ").strip()

    if escolha == "0":
        print("Saindo do sistema...")
        break

    elif escolha == "1":  # Cadastrar
        nome = input("Nome do produto: ").strip().lower()
        if nome in estoque:
            print("Produto já cadastrado. Use a opção 2 para adicionar.")
            continue
        try:
            qtd = int(input("Quantidade: "))
            valor = float(input("Valor unitário: "))
            estoque[nome] = {
                "quantidade": qtd,
                "valor_unitario": valor
            }
            print(f"Produto '{nome}' cadastrado com sucesso!")
        except ValueError:
            print("Erro: Digite valores numéricos válidos.")

    elif escolha == "2":  # Adicionar
        nome = input("Nome do produto: ").strip().lower()
        if nome in estoque:
            try:
                qtd = int(input("Quantidade a adicionar: "))
                estoque[nome]["quantidade"] += qtd
                print(f"{qtd} unidades adicionadas ao produto '{nome}'.")
            except ValueError:
                print("Erro: Digite uma quantidade válida.")
        else:
            print("Produto não encontrado. Cadastre primeiro.")

    elif escolha == "3":  # Baixar
        nome = input("Nome do produto: ").strip().lower()
        if nome in estoque:
            try:
                qtd = int(input("Quantidade a baixar: "))
                if qtd <= estoque[nome]["quantidade"]:
                    estoque[nome]["quantidade"] -= qtd
                    print(f"{qtd} unidades baixadas do produto '{nome}'.")
                    if estoque[nome]["quantidade"] == 0:
                        del estoque[nome]
                        print(f"Produto '{nome}' removido do estoque (zerado).")
                else:
                    print("Erro: Quantidade insuficiente no estoque.")
            except ValueError:
                print("Erro: Digite uma quantidade válida.")
        else:
            print("Produto não encontrado.")

    elif escolha == "4":  # Visualizar
        if not estoque:
            print("Estoque vazio.")
        else:
            print("\n--- ESTOQUE ATUAL ---")
            for nome, info in estoque.items():
                qtd = info["quantidade"]
                valor_unit = info["valor_unitario"]
                total = qtd * valor_unit
                print(f"Produto: {nome}")
                print(f"  Quantidade: {qtd}")
                print(f"  Valor unitário: R$ {valor_unit:.2f}")
                print(f"  Valor total:    R$ {total:.2f}")
                print("-" * 30)

    elif escolha == "5":  # Gráfico com valor total
        if not estoque:
            print("Estoque vazio. Nada para mostrar.")
        else:
            nomes = list(estoque.keys())
            valores_totais = [
                estoque[n]["quantidade"] * estoque[n]["valor_unitario"]
                for n in nomes
            ]

            plt.figure(figsize=(10, 5))
            barras = plt.bar(nomes, valores_totais, color='lightgreen')

            plt.title('Valor Total em Estoque por Produto')
            plt.xlabel('Produto')
            plt.ylabel('Valor Total (R$)')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()

            # Adiciona os valores em cima das barras
            for bar, valor in zip(barras, valores_totais):
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f'R$ {valor:.2f}', ha='center', va='bottom', fontsize=9)

            plt.show()

    else:
        print("Opção inválida. Digite um número de 0 a 5.")