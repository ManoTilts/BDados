"""
=================================================================================
Script Completo: Criação de Tabelas, Inserção de Dados e Consultas SQL
Banco de Dados: Relacional (SQLite)
=================================================================================
"""

import sqlite3
from datetime import datetime, timedelta
import random

# =================================================================================
# SEÇÃO 1: CRIAÇÃO DO BANCO DE DADOS E TABELAS
# =================================================================================

def criar_tabelas():
    """Cria o banco de dados e todas as tabelas necessárias"""
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("SEÇÃO 1: CRIAÇÃO DO BANCO DE DADOS E TABELAS")
    print("=" * 80)
    
    # Tabela de Clientes
    print("\nCriando tabela CLIENTES...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cidade VARCHAR(50),
            estado VARCHAR(2),
            data_cadastro DATE NOT NULL,
            ativo BOOLEAN DEFAULT 1
        )
    ''')
    print("   Tabela CLIENTES criada com sucesso")
    
    # Tabela de Produtos
    print("\nCriando tabela PRODUTOS...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto VARCHAR(100) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INTEGER DEFAULT 0,
            fornecedor VARCHAR(100)
        )
    ''')
    print("   Tabela PRODUTOS criada com sucesso")
    
    # Tabela de Pedidos
    print("\nCriando tabela PEDIDOS...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            data_pedido DATE NOT NULL,
            status VARCHAR(20) DEFAULT 'Pendente',
            valor_total DECIMAL(10, 2),
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        )
    ''')
    print("   Tabela PEDIDOS criada com sucesso")
    
    # Tabela de Itens do Pedido
    print("\nCriando tabela ITENS_PEDIDO...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario DECIMAL(10, 2) NOT NULL,
            subtotal DECIMAL(10, 2),
            FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
        )
    ''')
    print("   Tabela ITENS_PEDIDO criada com sucesso")
    
    conn.commit()
    
    # Exibir estrutura das tabelas
    print("\n" + "=" * 80)
    print("ESTRUTURA DAS TABELAS CRIADAS")
    print("=" * 80)
    
    tabelas = ['clientes', 'produtos', 'pedidos', 'itens_pedido']
    
    for tabela in tabelas:
        print(f"\nTabela: {tabela.upper()}")
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = cursor.fetchall()
        for coluna in colunas:
            print(f"   - {coluna[1]} ({coluna[2]})")
    
    return conn

# =================================================================================
# SEÇÃO 2: INSERÇÃO DE DADOS
# =================================================================================

def inserir_dados(conn):
    """Insere dados de exemplo nas tabelas"""
    
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("SEÇÃO 2: INSERÇÃO DE DADOS")
    print("=" * 80)
    
    # Inserir Clientes
    print("\nInserindo dados na tabela CLIENTES...")
    clientes = [
        ('João Silva', 'joao.silva@email.com', 'São Paulo', 'SP', '2023-01-15', 1),
        ('Maria Santos', 'maria.santos@email.com', 'Rio de Janeiro', 'RJ', '2023-02-20', 1),
        ('Pedro Oliveira', 'pedro.oliveira@email.com', 'Belo Horizonte', 'MG', '2023-03-10', 1),
        ('Ana Costa', 'ana.costa@email.com', 'Curitiba', 'PR', '2023-04-05', 1),
        ('Carlos Souza', 'carlos.souza@email.com', 'Porto Alegre', 'RS', '2023-05-12', 1),
        ('Juliana Lima', 'juliana.lima@email.com', 'São Paulo', 'SP', '2023-06-18', 1),
        ('Roberto Alves', 'roberto.alves@email.com', 'Salvador', 'BA', '2023-07-22', 1),
        ('Fernanda Rocha', 'fernanda.rocha@email.com', 'Fortaleza', 'CE', '2023-08-30', 1),
        ('Lucas Pereira', 'lucas.pereira@email.com', 'Brasília', 'DF', '2023-09-14', 1),
        ('Patrícia Martins', 'patricia.martins@email.com', 'Recife', 'PE', '2023-10-08', 1),
        ('Ricardo Gomes', 'ricardo.gomes@email.com', 'São Paulo', 'SP', '2023-11-01', 1),
        ('Camila Ferreira', 'camila.ferreira@email.com', 'Rio de Janeiro', 'RJ', '2023-12-15', 1),
        ('Thiago Barbosa', 'thiago.barbosa@email.com', 'Belo Horizonte', 'MG', '2024-01-20', 1),
        ('Amanda Silva', 'amanda.silva@email.com', 'Curitiba', 'PR', '2024-02-10', 1),
        ('Bruno Ribeiro', 'bruno.ribeiro@email.com', 'Porto Alegre', 'RS', '2024-03-05', 1),
    ]
    
    cursor.executemany('''
        INSERT INTO clientes (nome, email, cidade, estado, data_cadastro, ativo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', clientes)
    print(f"   {len(clientes)} registros inseridos")
    
    # Inserir Produtos
    print("\nInserindo dados na tabela PRODUTOS...")
    produtos = [
        ('Notebook Dell Inspiron', 'Eletrônicos', 3500.00, 15, 'Dell Inc'),
        ('Mouse Logitech MX', 'Eletrônicos', 250.00, 50, 'Logitech'),
        ('Teclado Mecânico RGB', 'Eletrônicos', 450.00, 30, 'Razer'),
        ('Monitor LG 27"', 'Eletrônicos', 1200.00, 20, 'LG Electronics'),
        ('Webcam HD', 'Eletrônicos', 300.00, 40, 'Logitech'),
        ('Headset Gamer', 'Eletrônicos', 350.00, 25, 'HyperX'),
        ('SSD 1TB Samsung', 'Eletrônicos', 600.00, 35, 'Samsung'),
        ('Memória RAM 16GB', 'Eletrônicos', 400.00, 45, 'Kingston'),
        ('Cadeira Gamer', 'Móveis', 1100.00, 12, 'DXRacer'),
        ('Mesa para Computador', 'Móveis', 800.00, 18, 'Madesa'),
        ('Mousepad Grande', 'Acessórios', 80.00, 60, 'Warrior'),
        ('Hub USB 3.0', 'Acessórios', 120.00, 55, 'Anker'),
        ('Cabo HDMI 2m', 'Acessórios', 45.00, 70, 'Elg'),
        ('Suporte para Notebook', 'Acessórios', 150.00, 40, 'Octoo'),
        ('Webcam 4K', 'Eletrônicos', 800.00, 15, 'Logitech'),
        ('Microfone USB', 'Eletrônicos', 550.00, 22, 'Blue Microphones'),
        ('Switch 8 Portas', 'Eletrônicos', 200.00, 28, 'TP-Link'),
        ('Roteador Wi-Fi 6', 'Eletrônicos', 450.00, 20, 'TP-Link'),
        ('Nobreak 1200VA', 'Eletrônicos', 650.00, 16, 'SMS'),
        ('Estabilizador', 'Eletrônicos', 280.00, 24, 'Enermax'),
    ]
    
    cursor.executemany('''
        INSERT INTO produtos (nome_produto, categoria, preco, estoque, fornecedor)
        VALUES (?, ?, ?, ?, ?)
    ''', produtos)
    print(f"   {len(produtos)} registros inseridos")
    
    # Inserir Pedidos e Itens
    print("\nInserindo dados nas tabelas PEDIDOS e ITENS_PEDIDO...")
    
    data_inicial = datetime(2024, 1, 1)
    status_opcoes = ['Concluído', 'Concluído', 'Concluído', 'Pendente', 'Enviado']
    
    pedidos_inseridos = 0
    itens_inseridos = 0
    
    for cliente_id in range(1, 16):
        num_pedidos = random.randint(2, 5)
        
        for _ in range(num_pedidos):
            dias_aleatorios = random.randint(0, 300)
            data_pedido = (data_inicial + timedelta(days=dias_aleatorios)).strftime('%Y-%m-%d')
            status = random.choice(status_opcoes)
            
            cursor.execute('''
                INSERT INTO pedidos (id_cliente, data_pedido, status, valor_total)
                VALUES (?, ?, ?, 0)
            ''', (cliente_id, data_pedido, status))
            
            id_pedido = cursor.lastrowid
            pedidos_inseridos += 1
            
            num_itens = random.randint(1, 5)
            valor_total_pedido = 0
            produtos_no_pedido = random.sample(range(1, 21), num_itens)
            
            for produto_id in produtos_no_pedido:
                cursor.execute('SELECT preco FROM produtos WHERE id_produto = ?', (produto_id,))
                preco = cursor.fetchone()[0]
                
                quantidade = random.randint(1, 3)
                subtotal = preco * quantidade
                valor_total_pedido += subtotal
                
                cursor.execute('''
                    INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (id_pedido, produto_id, quantidade, preco, subtotal))
                
                itens_inseridos += 1
            
            cursor.execute('''
                UPDATE pedidos SET valor_total = ? WHERE id_pedido = ?
            ''', (valor_total_pedido, id_pedido))
    
    print(f"   {pedidos_inseridos} pedidos inseridos")
    print(f"   {itens_inseridos} itens de pedido inseridos")
    
    conn.commit()
    
    # Resumo dos dados
    print("\n" + "=" * 80)
    print("RESUMO DOS DADOS INSERIDOS")
    print("=" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    print(f"\nTotal de Clientes: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM produtos")
    print(f"Total de Produtos: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    print(f"Total de Pedidos: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM itens_pedido")
    print(f"Total de Itens de Pedido: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT SUM(valor_total) FROM pedidos")
    total_vendas = cursor.fetchone()[0]
    print(f"Valor Total de Vendas: R$ {total_vendas:,.2f}")

# =================================================================================
# SEÇÃO 3: CONSULTAS SQL
# =================================================================================

def executar_consultas(conn):
    """Executa as consultas SQL obrigatórias"""
    
    print("\n\n" + "=" * 80)
    print("SEÇÃO 3: CONSULTAS SQL")
    print("=" * 80)
    
    cursor = conn.cursor()
    
    # =========================================================================
    # CONSULTA 1: JOIN COM 2 TABELAS
    # =========================================================================
    print("\n" + "=" * 80)
    print("CONSULTA 1: JOIN COM 2 TABELAS")
    print("Objetivo: Listar pedidos com informações dos clientes")
    print("=" * 80)
    
    query1 = """
    SELECT 
        p.id_pedido,
        c.nome AS cliente,
        c.cidade,
        c.estado,
        p.data_pedido,
        p.status,
        p.valor_total
    FROM pedidos p
    INNER JOIN clientes c ON p.id_cliente = c.id_cliente
    ORDER BY p.data_pedido DESC
    LIMIT 15
    """
    
    print("\nSQL:")
    print(query1)
    
    cursor.execute(query1)
    resultados = cursor.fetchall()
    
    print("\nResultado:")
    print(f"{'ID':<5} {'Cliente':<20} {'Cidade':<15} {'UF':<4} {'Data':<12} {'Status':<12} {'Valor':>12}")
    print("-" * 85)
    for row in resultados:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<4} {row[4]:<12} {row[5]:<12} R$ {row[6]:>9,.2f}")
    print(f"\n   Total de registros: {len(resultados)}")
    
    # =========================================================================
    # CONSULTA 2: JOIN COM MÚLTIPLAS TABELAS, GROUP BY E HAVING
    # =========================================================================
    print("\n\n" + "=" * 80)
    print("CONSULTA 2: JOIN COM MÚLTIPLAS TABELAS, GROUP BY E HAVING")
    print("Objetivo: Clientes que gastaram mais de R$ 5000 (Clientes VIP)")
    print("=" * 80)
    
    query2 = """
    SELECT 
        c.nome AS cliente,
        c.cidade,
        c.estado,
        COUNT(DISTINCT p.id_pedido) AS total_pedidos,
        COUNT(ip.id_item) AS total_itens_comprados,
        SUM(ip.subtotal) AS valor_total_gasto,
        AVG(p.valor_total) AS ticket_medio
    FROM clientes c
    INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
    INNER JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
    GROUP BY c.id_cliente, c.nome, c.cidade, c.estado
    HAVING SUM(ip.subtotal) > 5000
    ORDER BY valor_total_gasto DESC
    """
    
    print("\nSQL:")
    print(query2)
    
    cursor.execute(query2)
    resultados = cursor.fetchall()
    
    print("\nResultado:")
    if len(resultados) > 0:
        print(f"{'Cliente':<20} {'Cidade':<15} {'UF':<4} {'Pedidos':<9} {'Itens':<7} {'Total Gasto':>14} {'Ticket Médio':>14}")
        print("-" * 95)
        for row in resultados:
            print(f"{row[0]:<20} {row[1]:<15} {row[2]:<4} {row[3]:<9} {row[4]:<7} R$ {row[5]:>10,.2f} R$ {row[6]:>10,.2f}")
        print(f"\n   Total de clientes VIP: {len(resultados)}")
    else:
        print("   Nenhum cliente com gasto superior a R$ 5000")
    
    # =========================================================================
    # CONSULTA 3: JOIN COM SUBSELECT
    # =========================================================================
    print("\n\n" + "=" * 80)
    print("CONSULTA 3: JOIN COM SUBSELECT")
    print("Objetivo: Produtos com vendas acima da média")
    print("=" * 80)
    
    query3 = """
    SELECT 
        prod.nome_produto,
        prod.categoria,
        prod.preco,
        vendas.total_vendido,
        vendas.quantidade_total,
        vendas.receita_total
    FROM produtos prod
    INNER JOIN (
        SELECT 
            ip.id_produto,
            COUNT(DISTINCT ip.id_pedido) AS total_vendido,
            SUM(ip.quantidade) AS quantidade_total,
            SUM(ip.subtotal) AS receita_total
        FROM itens_pedido ip
        GROUP BY ip.id_produto
    ) vendas ON prod.id_produto = vendas.id_produto
    WHERE vendas.total_vendido > (
        SELECT AVG(total_vendas)
        FROM (
            SELECT COUNT(DISTINCT id_pedido) AS total_vendas
            FROM itens_pedido
            GROUP BY id_produto
        )
    )
    ORDER BY vendas.receita_total DESC
    """
    
    print("\nSQL:")
    print(query3)
    
    cursor.execute(query3)
    resultados = cursor.fetchall()
    
    print("\nResultado:")
    print(f"{'Produto':<25} {'Categoria':<13} {'Preço':>10} {'Pedidos':<9} {'Qtd':<6} {'Receita':>12}")
    print("-" * 85)
    for row in resultados:
        print(f"{row[0]:<25} {row[1]:<13} R$ {row[2]:>6,.2f} {row[3]:<9} {row[4]:<6} R$ {row[5]:>9,.2f}")
    print(f"\n   Total de produtos acima da média: {len(resultados)}")
    
    # =========================================================================
    # CONSULTAS EXTRAS
    # =========================================================================
    print("\n\n" + "=" * 80)
    print("CONSULTAS EXTRAS - ANÁLISES ADICIONAIS")
    print("=" * 80)
    
    # EXTRA 1: Vendas por Categoria
    print("\nEXTRA 1: Vendas por Categoria")
    query_extra1 = """
    SELECT 
        prod.categoria,
        COUNT(DISTINCT ip.id_pedido) AS total_pedidos,
        SUM(ip.quantidade) AS quantidade_vendida,
        SUM(ip.subtotal) AS receita_total,
        AVG(ip.preco_unitario) AS preco_medio
    FROM produtos prod
    INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
    GROUP BY prod.categoria
    ORDER BY receita_total DESC
    """
    
    cursor.execute(query_extra1)
    resultados = cursor.fetchall()
    print(f"\n{'Categoria':<15} {'Pedidos':<9} {'Qtd Vendida':<13} {'Receita Total':>15} {'Preço Médio':>14}")
    print("-" * 75)
    for row in resultados:
        print(f"{row[0]:<15} {row[1]:<9} {row[2]:<13} R$ {row[3]:>11,.2f} R$ {row[4]:>10,.2f}")
    
    # EXTRA 2: Top 10 Produtos
    print("\n\nEXTRA 2: Top 10 Produtos Mais Vendidos")
    query_extra2 = """
    SELECT 
        prod.nome_produto,
        prod.categoria,
        SUM(ip.quantidade) AS quantidade_vendida,
        SUM(ip.subtotal) AS receita_gerada
    FROM produtos prod
    INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
    GROUP BY prod.id_produto, prod.nome_produto, prod.categoria
    ORDER BY quantidade_vendida DESC
    LIMIT 10
    """
    
    cursor.execute(query_extra2)
    resultados = cursor.fetchall()
    print(f"\n{'Produto':<25} {'Categoria':<13} {'Qtd Vendida':<13} {'Receita':>12}")
    print("-" * 70)
    for row in resultados:
        print(f"{row[0]:<25} {row[1]:<13} {row[2]:<13} R$ {row[3]:>9,.2f}")
    
    # EXTRA 3: Vendas por Estado
    print("\n\nEXTRA 3: Vendas por Estado")
    query_extra3 = """
    SELECT 
        c.estado,
        COUNT(DISTINCT c.id_cliente) AS total_clientes,
        COUNT(DISTINCT p.id_pedido) AS total_pedidos,
        SUM(p.valor_total) AS receita_total,
        AVG(p.valor_total) AS ticket_medio
    FROM clientes c
    INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
    GROUP BY c.estado
    ORDER BY receita_total DESC
    """
    
    cursor.execute(query_extra3)
    resultados = cursor.fetchall()
    print(f"\n{'Estado':<8} {'Clientes':<10} {'Pedidos':<9} {'Receita Total':>15} {'Ticket Médio':>14}")
    print("-" * 65)
    for row in resultados:
        print(f"{row[0]:<8} {row[1]:<10} {row[2]:<9} R$ {row[3]:>11,.2f} R$ {row[4]:>10,.2f}")

# =================================================================================
# FUNÇÃO PRINCIPAL
# =================================================================================

def main():
    """Função principal que executa todo o script"""
    
    print("\n")
    print("=" * 80)
    print("     SISTEMA DE BANCO DE DADOS E-COMMERCE")
    print("     Script Completo: Criação, Inserção e Consultas SQL")
    print("=" * 80)
    print("\n")
    
    try:
        # Criar tabelas
        conn = criar_tabelas()
        
        # Inserir dados
        inserir_dados(conn)
        
        # Executar consultas
        executar_consultas(conn)
        
        # Fechar conexão
        conn.close()
        
        print("\n\n" + "=" * 80)
        print("SCRIPT EXECUTADO COM SUCESSO!")
        print("=" * 80)
        print("\nBanco de dados criado: ecommerce.db")
        print("Para visualizar os dados no dashboard, execute: python dashboard.py")
        print("\n" + "=" * 80 + "\n")
        
    except Exception as e:
        print(f"\nERRO: {e}")
        print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()
