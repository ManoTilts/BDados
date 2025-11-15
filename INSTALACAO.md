# Script de Instalação e Teste do Dashboard E-commerce

## IMPORTANTE: Execute os passos na ordem

### 1. Instalar dependências Python
```bash
pip install -r requirements.txt
```

### 2. Verificar instalação do MySQL
Certifique-se que o MySQL Server está instalado e rodando.
Você pode verificar com:
```bash
mysql --version
```

### 3. Configurar credenciais do banco
Edite os arquivos `banco_dados.py` e `dashboard.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",              # Altere se necessário
    "password": "sua_senha",     # Coloque sua senha do MySQL
    "database": "ecommerce",
}
```

### 4. Executar o sistema de banco de dados
```bash
python banco_dados.py
```

No menu, execute:
- Opção 1: Criar banco
- Opção 2: Criar tabelas  
- Opção 3: Inserir dados

### 5. Executar o dashboard
```bash
python dashboard.py
```

Acesse: http://127.0.0.1:8050

## Dependências que serão instaladas:
- pandas>=2.0.0
- plotly>=5.14.0
- dash>=2.9.0
- mysql-connector-python>=8.0.0

## Troubleshooting:

### Erro: "Access denied for user"
- Verifique usuário e senha em DB_CONFIG
- Confirme que o MySQL está aceitando conexões

### Erro: "Unknown database 'ecommerce'"
- Execute a opção 1 do menu do banco_dados.py primeiro

### Erro: "No module named 'dash'"
- Execute: pip install dash plotly pandas mysql-connector-python

### Dashboard não carrega dados
- Certifique-se que executou banco_dados.py e populou o banco (opções 1, 2, 3)

## Recursos do Dashboard:

✅ 6 Cards de métricas principais
✅ 7 Gráficos interativos:
   - Evolução de vendas (linha temporal)
   - Receita por categoria (barras)
   - Distribuição por estado (pizza)
   - Top 10 produtos (barras horizontais)
   - Top 10 clientes VIP (barras horizontais)
   - Status dos pedidos (barras)
   - Quantidade por categoria (rosca)

✅ Interface responsiva e moderna
✅ Dados em tempo real do MySQL
✅ Visualizações interativas (zoom, hover, etc)
