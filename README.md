# 📊 Sistema de Banco de Dados E-commerce com Dashboard

Sistema completo de análise de vendas e-commerce desenvolvido em Python com banco de dados **MySQL** e dashboard interativo usando **Dash/Plotly**.

## 🚀 Características

- **Banco de Dados MySQL** com stored procedures
- **Dashboard Interativo** com 7 gráficos de análise
- **Interface de menu** no terminal para gerenciar o banco
- **Análises avançadas** com JOINs, GROUP BY, HAVING e subqueries
- **Métricas em tempo real** com visualizações modernas

## 📋 Pré-requisitos

- Python 3.8+
- MySQL Server 5.7+ ou 8.0+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/ManoTilts/BDados.git
cd BDados
```

### 2. Instale as dependências Python
```bash
pip install -r requirements.txt
```

### 3. Configure o MySQL

Edite o arquivo `banco_dados.py` e atualize as credenciais do banco (linhas 13-17):

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "seu_usuario",      # <-- Altere aqui
    "password": "sua_senha",     # <-- Altere aqui
    "database": "ecommerce",
}
```

Faça o mesmo no arquivo `dashboard.py` (linhas 13-17).

## 📊 Uso

### 1. Executar o Sistema de Banco de Dados

```bash
python banco_dados.py
```

**Menu de opções disponíveis:**

1. Criação ou acesso ao banco de dados
2. Criação das tabelas
3. Inserção dos dados
4. CONSULTA 1: JOIN COM 2 TABELAS
5. CONSULTA 2: JOIN COM MÚLTIPLAS TABELAS
6. CONSULTA 3: JOIN COM SUBSELECT
7. CONSULTAS EXTRAS
8. Executar TODAS as consultas
0. Sair

**Fluxo recomendado para primeira execução:**
- Execute opção **1** (criar banco)
- Execute opção **2** (criar tabelas)
- Execute opção **3** (inserir dados)
- Execute opção **8** (visualizar todas as consultas)

### 2. Executar o Dashboard

Após popular o banco de dados:

```bash
python dashboard.py
```

Acesse no navegador: **http://127.0.0.1:8050**

Pressione **CTRL+C** para encerrar o servidor.

## 📈 Gráficos do Dashboard

O dashboard apresenta **7 visualizações interativas**:

1. **📈 Evolução de Vendas** - Gráfico de linha mostrando receita mensal ao longo do tempo
2. **💼 Receita por Categoria** - Barras comparando faturamento entre categorias
3. **🗺️ Distribuição por Estado** - Pizza mostrando participação de vendas por região
4. **🏆 Top 10 Produtos** - Ranking dos produtos mais vendidos
5. **👑 Top 10 Clientes VIP** - Maiores compradores da plataforma
6. **📦 Status dos Pedidos** - Acompanhamento do status de todos os pedidos
7. **📊 Quantidade por Categoria** - Volume de produtos vendidos por categoria

## 🎯 Métricas Exibidas (Cards)

- 👥 **Clientes Ativos** - Total de clientes cadastrados ativos
- 📦 **Total de Pedidos** - Quantidade total de pedidos realizados
- 💰 **Receita Total** - Valor total de vendas
- 🎯 **Ticket Médio** - Valor médio por pedido
- 📊 **Total de Produtos** - Produtos no catálogo
- 🏷️ **Categorias** - Número de categorias disponíveis

## 🗂️ Estrutura do Banco de Dados

### Tabelas:

**clientes**
- id_cliente (PK)
- nome
- email (UNIQUE)
- cidade
- estado
- data_cadastro
- ativo

**produtos**
- id_produto (PK)
- nome_produto
- categoria
- preco
- estoque
- fornecedor

**pedidos**
- id_pedido (PK)
- id_cliente (FK)
- data_pedido
- status
- valor_total

**itens_pedido**
- id_item (PK)
- id_pedido (FK)
- id_produto (FK)
- quantidade
- preco_unitario
- subtotal

### Stored Procedures:

- **CriarTabelas()** - Cria toda a estrutura do banco de dados
- **InserirDadosBasicos()** - Popula clientes e produtos
- **sp_consulta_1()** - JOIN com 2 tabelas (pedidos + clientes)
- **sp_consulta_2()** - JOIN múltiplas tabelas + GROUP BY + HAVING
- **sp_consulta_3()** - JOIN com subselect
- **sp_consultas_extras()** - Análises adicionais (vendas por categoria, top produtos, vendas por estado)

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação
- **MySQL 8.0** - Banco de dados relacional
- **mysql-connector-python** - Driver de conexão MySQL
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Biblioteca de visualizações interativas
- **Dash** - Framework para criação de dashboards web

## 📁 Estrutura de Arquivos

```
BDados/
│
├── banco_dados.py          # Sistema principal com menu interativo
├── dashboard.py            # Dashboard web interativo
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🔍 Consultas SQL Implementadas

### Consulta 1: JOIN com 2 Tabelas
Lista pedidos com informações dos clientes usando INNER JOIN entre `pedidos` e `clientes`.

### Consulta 2: JOIN Múltiplas Tabelas + GROUP BY + HAVING
Identifica clientes VIP que gastaram mais de R$ 5.000, usando JOIN de três tabelas (`clientes`, `pedidos`, `itens_pedido`) com agregações e filtro HAVING.

### Consulta 3: JOIN com Subselect
Produtos com vendas acima da média, utilizando subquery para calcular a média e JOIN para obter detalhes dos produtos.

### Consultas Extras
- Vendas por categoria
- Top 10 produtos mais vendidos
- Vendas por estado

## 🎨 Características do Dashboard

- **Interface Moderna** - Design limpo e profissional
- **Responsivo** - Adaptável a diferentes tamanhos de tela
- **Interativo** - Gráficos com hover e zoom
- **Tempo Real** - Dados atualizados do banco MySQL
- **Cores Temáticas** - Paleta de cores consistente e agradável

## 📝 Observações

- O sistema usa **stored procedures** do MySQL para otimizar operações
- Os dados são inseridos automaticamente com valores realistas
- O dashboard carrega dados diretamente do MySQL em tempo real
- Todos os valores monetários são exibidos em Real (R$)

## 🐛 Troubleshooting

**Erro de conexão com MySQL:**
- Verifique se o MySQL Server está rodando
- Confirme as credenciais em `DB_CONFIG`
- Certifique-se que o banco `ecommerce` foi criado

**Dashboard não carrega:**
- Execute primeiro `banco_dados.py` para popular o banco
- Verifique se a porta 8050 está disponível
- Confirme que as dependências foram instaladas

**Erro ao instalar mysql-connector-python:**
```bash
pip install --upgrade pip
pip install mysql-connector-python
```

## 📝 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido para fins educacionais - Demonstração de banco de dados relacional e visualização de dados com Python.

---

⭐ Se este projeto foi útil, considere dar uma estrela no repositório!
