🚀 ERP Moda Estoque 

Este projeto é um **Sistema Básico de Gestão Empresarial (ERP)** focado no segmento de **Varejo de Roupas**. Foi desenvolvido em Python, utilizando SQLite para persistência de dados e Matplotlib para análise visual.

Atualmente, o projeto é operado via console, mas está modularizado para futura implementação de uma interface gráfica (Front-end) com Tkinter.

✨ Funcionalidades Principais

O sistema gerencia duas entidades principais: **Estoque (Produtos)** e **Pessoal (Funcionários)**.

Estoque & Operações
* **CRUD Básico:** Cadastrar, Adicionar Quantidade, Baixar (Venda).
* **Visualização:** Listagem completa do estoque com cálculo de valor total.
* **Importação/Exportação:** Importação e Remoção em Massa de produtos via arquivos CSV.

### Pessoal & RH
* **CRUD:** Cadastrar, Listar e Remover funcionários (por ID ou em massa via CSV).
* **Análise:** Busca de funcionário por nome (parcial) e cálculo da Média Salarial da empresa.

### 📊 Análises Gráficas (Matplotlib)

O sistema possui uma seção dedicada a relatórios visuais essenciais para a tomada de decisões:

| Nº | Gráfico | Objetivo de Análise |
| :--- | :--- | :--- |
| 1 | Tendência Diária (Linha) | Simula a evolução da quantidade de um produto específico ao longo de 7 dias. |
| 2 | Comparação (Barras) | Compara as quantidades em estoque dos produtos mais abundantes (Top 10). |
| 3 | Proporção de Categorias (Pizza) | Visualiza a distribuição do **valor total** do estoque por categorias de vestuário (Calçados, Blusas, Acessórios, etc.). |
| 4 | Preço vs. Quantidade (Dispersão) | Analisa a correlação entre o preço unitário e a quantidade em estoque para identificar a gestão de itens caros vs. baratos. |

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Banco de Dados:** SQLite (nativo do Python, persistência em arquivo `meu_estoque.db`).
* **Visualização de Dados:** Matplotlib e NumPy.
* **Organização:** Módulos `csv` e `os` para importação e gestão de arquivos.

## ⚙️ Como Instalar e Executar

Para rodar este projeto em sua máquina local, siga os passos abaixo:

### Pré-requisitos
Certifique-se de ter o Python 3.x instalado e o `pip` atualizado.

Você precisa instalar as bibliotecas de visualização:

```bash
pip install matplotlib numpy
