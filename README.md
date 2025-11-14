# Dashboard de Análise de Vendas E-commerce

## Descrição do Projeto
Sistema de dashboard para análise de vendas de uma loja online, incluindo:
- Gestão de Clientes
- Catálogo de Produtos
- Pedidos e Itens de Pedidos
- Análises e visualizações de dados

## Estrutura do Banco de Dados
- **clientes**: Informações dos clientes
- **produtos**: Catálogo de produtos
- **pedidos**: Pedidos realizados
- **itens_pedido**: Itens de cada pedido

## Tecnologias Utilizadas
- Python 3.x
- SQLite (Banco de Dados Relacional)
- Pandas (Manipulação de dados)
- Plotly (Visualizações interativas)
- Dash (Framework para dashboard)

## Instalação
```bash
pip install -r requirements.txt
```

## Execução

### Opção 1: Execução Rápida (Recomendado)
```bash
# 1. Criar banco de dados e executar consultas SQL
python banco_dados.py

# 2. Abrir dashboard (navegador)
python dashboard.py
```

### Opção 2: Execução Individual (Scripts separados)
```bash
# 1. Criar tabelas
python 1_criar_tabelas.py

# 2. Inserir dados
python 2_inserir_dados.py

# 3. Executar consultas SQL
python 3_consultas_sql.py

# 4. Abrir dashboard
python 4_dashboard.py
```

## Estrutura de Arquivos

### Scripts Principais (Recomendado)
- **`banco_dados.py`** - Script único com: criação de tabelas, inserção de dados e consultas SQL
- **`dashboard.py`** - Dashboard interativo web (Dash + Plotly)

### Scripts Individuais (Opcional)
- `1_criar_tabelas.py` - Criação das tabelas do banco de dados
- `2_inserir_dados.py` - Inserção de dados de exemplo
- `3_consultas_sql.py` - Consultas SQL (joins, group by, having, subselects)
- `4_dashboard.py` - Dashboard interativo

### Outros Arquivos
- `requirements.txt` - Dependências do projeto
- `executar_tudo.py` - Script automatizado completo
- `ecommerce.db` - Banco de dados SQLite (gerado após execução)

## Consultas SQL Implementadas

### Consulta 1: JOIN com 2 Tabelas
Lista pedidos com informações dos clientes (pedidos + clientes)

### Consulta 2: JOIN com Múltiplas Tabelas + GROUP BY + HAVING
Identifica clientes VIP que gastaram mais de R$ 5000 (clientes + pedidos + itens_pedido)

### Consulta 3: JOIN com Subselect
Produtos com vendas acima da média usando subquery

## Dashboard Interativo
Acesse em: **http://127.0.0.1:8050** após executar `python dashboard.py`

**Recursos do Dashboard:**
- 4 métricas principais (clientes, pedidos, receita, ticket médio)
- 6 gráficos interativos
- Interface moderna e responsiva
- Visualizações em tempo real
