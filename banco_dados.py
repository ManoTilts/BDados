# ================================================================================
# Script Completo: Criação de Tabelas, Inserção de Dados e Consultas SQL
# Banco de Dados: Relacional (MySQL)
# Com interface de menu no terminal e uso de PROCEDURES
# ================================================================================

import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

# Configuração da conexão com o MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",                 # <-- altere se Com seu user
    "password": "Giuseppe1490",     # <-- altere com sua senha
    "database": "ecommerce",        # nome do banco que usaremos
}

# =================================================================================
# Funções auxiliares de conexão
# =================================================================================

def criar_banco_se_nao_existir():
    """Cria o banco de dados no MySQL se ainda não existir."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"\nBanco de dados '{DB_CONFIG['database']}' verificado/criado com sucesso.")
    except Error as e:
        print(f"\nERRO ao criar/acessar o banco de dados: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def get_connection():
    """Retorna uma conexão ativa com o banco MySQL 'ecommerce'."""
    return mysql.connector.connect(**DB_CONFIG)


# =================================================================================
# PROCEDURE DE CRIAÇÃO DE TABELAS
# =================================================================================

def criar_procedure_criar_tabelas():
    """Cria (ou recria) a stored procedure CriarTabelas no MySQL."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP PROCEDURE IF EXISTS CriarTabelas")

    procedure_sql = """
    CREATE PROCEDURE CriarTabelas()
    BEGIN
        -- Tabela de Clientes
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cidade VARCHAR(50),
            estado VARCHAR(2),
            data_cadastro DATE NOT NULL,
            ativo TINYINT(1) DEFAULT 1
        );

        -- Tabela de Produtos
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INT AUTO_INCREMENT PRIMARY KEY,
            nome_produto VARCHAR(100) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INT DEFAULT 0,
            fornecedor VARCHAR(100)
        );

        -- Tabela de Pedidos
        CREATE TABLE IF NOT EXISTS pedidos (
            id_pedido INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT NOT NULL,
            data_pedido DATE NOT NULL,
            status VARCHAR(20) DEFAULT 'Pendente',
            valor_total DECIMAL(10, 2),
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );

        -- Tabela de Itens do Pedido
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id_item INT AUTO_INCREMENT PRIMARY KEY,
            id_pedido INT NOT NULL,
            id_produto INT NOT NULL,
            quantidade INT NOT NULL,
            preco_unitario DECIMAL(10, 2) NOT NULL,
            subtotal DECIMAL(10, 2),
            FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
        );
    END
    """

    cursor.execute(procedure_sql)
    conn.commit()

    print("Procedure CriarTabelas() criada/recriada com sucesso.")

    cursor.close()
    conn.close()


# =================================================================================
# PROCEDURE DE INSERÇÃO DE DADOS BÁSICOS (CLIENTES + PRODUTOS)
# =================================================================================

def criar_procedure_inserir_dados():
    """Cria (ou recria) a stored procedure InserirDadosBasicos no MySQL."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP PROCEDURE IF EXISTS InserirDadosBasicos")

    procedure_sql = """
    CREATE PROCEDURE InserirDadosBasicos()
    BEGIN
        DECLARE v_clientes INT DEFAULT 0;
        DECLARE v_produtos INT DEFAULT 0;

        -- Verifica se já existem clientes
        SELECT COUNT(*) INTO v_clientes FROM clientes;
        IF v_clientes = 0 THEN
            -- Inserir Clientes
            INSERT INTO clientes (nome, email, cidade, estado, data_cadastro, ativo) VALUES
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
                ('Bruno Ribeiro', 'bruno.ribeiro@email.com', 'Porto Alegre', 'RS', '2024-03-05', 1);
        END IF;

        -- Verifica se já existem produtos
        SELECT COUNT(*) INTO v_produtos FROM produtos;
        IF v_produtos = 0 THEN
            -- Inserir Produtos
            INSERT INTO produtos (nome_produto, categoria, preco, estoque, fornecedor) VALUES
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
                ('Estabilizador', 'Eletrônicos', 280.00, 24, 'Enermax');
        END IF;
    END
    """

    cursor.execute(procedure_sql)
    conn.commit()

    print("Procedure InserirDadosBasicos() criada/recriada com sucesso.")

    cursor.close()
    conn.close()



# =================================================================================
# SEÇÃO 1: CRIAÇÃO DAS TABELAS (via PROCEDURE)
# =================================================================================

def criar_tabelas():
    """Chama a stored procedure CriarTabelas e exibe a estrutura das tabelas."""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 80)
    print("SEÇÃO 1: CRIAÇÃO DAS TABELAS ")
    print("=" * 80)

    print("\nChamando procedure CriarTabelas()...")
    cursor.execute("CALL CriarTabelas()")
    conn.commit()
    print("   Procedure executada com sucesso. Tabelas criadas/validadas.")

    print("\n" + "=" * 80)
    print("ESTRUTURA DAS TABELAS CRIADAS")
    print("=" * 80)
    
    tabelas = ['clientes', 'produtos', 'pedidos', 'itens_pedido']
    
    for tabela in tabelas:
        print(f"\nTabela: {tabela.upper()}")
        cursor.execute(f"DESCRIBE {tabela}")
        colunas = cursor.fetchall()
        for coluna in colunas:
            print(f"   - {coluna[0]} ({coluna[1]})")
    
    return conn


# =================================================================================
# SEÇÃO 2: INSERÇÃO DE DADOS (PROCEDURE + PYTHON)
# =================================================================================

def inserir_dados(conn):
    """Insere dados de exemplo nas tabelas (MySQL) usando PROCEDURE + Python."""
    
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("SEÇÃO 2: INSERÇÃO DE DADOS")
    print("=" * 80)
    
    print("\nChamando procedure InserirDadosBasicos() para inserir CLIENTES e PRODUTOS...")
    cursor.execute("CALL InserirDadosBasicos()")
    conn.commit()
    print("   Clientes e produtos inseridos com sucesso pela procedure.")

    print("\nInserindo dados nas tabelas PEDIDOS e ITENS_PEDIDO (via Python)...")
    
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
                VALUES (%s, %s, %s, %s)
            ''', (cliente_id, data_pedido, status, 0))
            
            id_pedido = cursor.lastrowid
            pedidos_inseridos += 1
            
            num_itens = random.randint(1, 5)
            valor_total_pedido = 0
            produtos_no_pedido = random.sample(range(1, 21), num_itens)
            
            for produto_id in produtos_no_pedido:
                cursor.execute('SELECT preco FROM produtos WHERE id_produto = %s', (produto_id,))
                preco = cursor.fetchone()[0]
                
                quantidade = random.randint(1, 3)
                subtotal = preco * quantidade
                valor_total_pedido += subtotal
                
                cursor.execute('''
                    INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (id_pedido, produto_id, quantidade, preco, subtotal))
                
                itens_inseridos += 1
            
            cursor.execute('''
                UPDATE pedidos SET valor_total = %s WHERE id_pedido = %s
            ''', (valor_total_pedido, id_pedido))
    
    print(f"   {pedidos_inseridos} pedidos inseridos")
    print(f"   {itens_inseridos} itens de pedido inseridos")
    
    conn.commit()
    
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
# PROCEDURES PARA AS CONSULTAS
# =================================================================================

def criar_procedure_consulta_1():
    """Cria/recria a procedure sp_consulta_1 (JOIN com 2 tabelas)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP PROCEDURE IF EXISTS sp_consulta_1")

    procedure_sql = """
    CREATE PROCEDURE sp_consulta_1()
    BEGIN
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
        LIMIT 15;
    END
    """

    cursor.execute(procedure_sql)
    conn.commit()
    print("Procedure sp_consulta_1() criada/recriada com sucesso.")

    cursor.close()
    conn.close()


def criar_procedure_consulta_2():
    """Cria/recria a procedure sp_consulta_2 (JOIN múltiplas tabelas, GROUP BY, HAVING)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP PROCEDURE IF EXISTS sp_consulta_2")

    procedure_sql = """
    CREATE PROCEDURE sp_consulta_2()
    BEGIN
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
        ORDER BY valor_total_gasto DESC;
    END
    """

    cursor.execute(procedure_sql)
    conn.commit()
    print("Procedure sp_consulta_2() criada/recriada com sucesso.")

    cursor.close()
    conn.close()


def criar_procedure_consulta_3():
    """Cria/recria a procedure sp_consulta_3 (JOIN com subselect)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP PROCEDURE IF EXISTS sp_consulta_3")

    procedure_sql = """
    CREATE PROCEDURE sp_consulta_3()
    BEGIN
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
            ) AS t
        )
        ORDER BY vendas.receita_total DESC;
    END
    """

    cursor.execute(procedure_sql)
    conn.commit()
    print("Procedure sp_consulta_3() criada/recriada com sucesso.")

    cursor.close()
    conn.close()


def criar_procedure_consultas_extras():
    """Cria/recria a procedure sp_consultas_extras (3 SELECTs: categoria, top produtos, estado)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP PROCEDURE IF EXISTS sp_consultas_extras")

    procedure_sql = """
    CREATE PROCEDURE sp_consultas_extras()
    BEGIN
        -- EXTRA 1: Vendas por Categoria
        SELECT 
            prod.categoria,
            COUNT(DISTINCT ip.id_pedido) AS total_pedidos,
            SUM(ip.quantidade) AS quantidade_vendida,
            SUM(ip.subtotal) AS receita_total,
            AVG(ip.preco_unitario) AS preco_medio
        FROM produtos prod
        INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
        GROUP BY prod.categoria
        ORDER BY receita_total DESC;

        -- EXTRA 2: Top 10 Produtos Mais Vendidos
        SELECT 
            prod.nome_produto,
            prod.categoria,
            SUM(ip.quantidade) AS quantidade_vendida,
            SUM(ip.subtotal) AS receita_gerada
        FROM produtos prod
        INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
        GROUP BY prod.id_produto, prod.nome_produto, prod.categoria
        ORDER BY quantidade_vendida DESC
        LIMIT 10;

        -- EXTRA 3: Vendas por Estado
        SELECT 
            c.estado,
            COUNT(DISTINCT c.id_cliente) AS total_clientes,
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            SUM(p.valor_total) AS receita_total,
            AVG(p.valor_total) AS ticket_medio
        FROM clientes c
        INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
        GROUP BY c.estado
        ORDER BY receita_total DESC;
    END
    """

    cursor.execute(procedure_sql)
    conn.commit()
    print("Procedure sp_consultas_extras() criada/recriada com sucesso.")

    cursor.close()
    conn.close()


def criar_procedures_consultas():
    """Cria todas as procedures de consulta."""
    criar_procedure_consulta_1()
    criar_procedure_consulta_2()
    criar_procedure_consulta_3()
    criar_procedure_consultas_extras()


# =================================================================================
# SEÇÃO 3: CONSULTAS SQL (agora usando PROCEDURES)
# =================================================================================

def consulta_1(conn):
    """CONSULTA 1: JOIN COM 2 TABELAS - Pedidos + Clientes ."""
    print("\n" + "=" * 80)
    print("CONSULTA 1: JOIN COM 2 TABELAS")
    print("Objetivo: Listar pedidos com informações dos clientes")
    print("=" * 80)
    
    cursor = conn.cursor()
    
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
    LIMIT 15;
    """
    
    print("\nSQL (dentro da procedure sp_consulta_1):")
    print(query1)
    
    cursor.execute("CALL sp_consulta_1()")
    resultados = cursor.fetchall()
    
    print("\nResultado:")
    print(f"{'ID':<5} {'Cliente':<20} {'Cidade':<15} {'UF':<4} {'Data':<12} {'Status':<12} {'Valor':>12}")
    print("-" * 85)
    for row in resultados:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<4} {str(row[4]):<12} {row[5]:<12} R$ {row[6]:>9,.2f}")
    print(f"\n   Total de registros: {len(resultados)}")


def consulta_2(conn):
    """CONSULTA 2: JOIN COM MÚLTIPLAS TABELAS, GROUP BY E HAVING ."""
    print("\n" + "=" * 80)
    print("CONSULTA 2: JOIN COM MÚLTIPLAS TABELAS, GROUP BY E HAVING")
    print("Objetivo: Clientes que gastaram mais de R$ 5000 (Clientes VIP)")
    print("=" * 80)
    
    cursor = conn.cursor()
    
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
    ORDER BY valor_total_gasto DESC;
    """
    
    print("\nSQL (dentro da procedure sp_consulta_2):")
    print(query2)
    
    cursor.execute("CALL sp_consulta_2()")
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


def consulta_3(conn):
    """CONSULTA 3: JOIN COM SUBSELECT ."""
    print("\n" + "=" * 80)
    print("CONSULTA 3: JOIN COM SUBSELECT")
    print("Objetivo: Produtos com vendas acima da média")
    print("=" * 80)
    
    cursor = conn.cursor()
    
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
        ) AS t
    )
    ORDER BY vendas.receita_total DESC;
    """
    
    print("\nSQL (dentro da procedure sp_consulta_3):")
    print(query3)
    
    cursor.execute("CALL sp_consulta_3()")
    resultados = cursor.fetchall()
    
    print("\nResultado:")
    print(f"{'Produto':<25} {'Categoria':<13} {'Preço':>10} {'Pedidos':<9} {'Qtd':<6} {'Receita':>12}")
    print("-" * 85)
    for row in resultados:
        print(f"{row[0]:<25} {row[1]:<13} R$ {row[2]:>6,.2f} {row[3]:<9} {row[4]:<6} R$ {row[5]:>9,.2f}")
    print(f"\n   Total de produtos acima da média: {len(resultados)}")


def consultas_extras(conn):
    """Consultas extras."""
    print("\n" + "=" * 80)
    print("CONSULTAS EXTRAS - ANÁLISES ADICIONAIS")
    print("=" * 80)
    
    cursor = conn.cursor()

    print("\nChamando procedure sp_consultas_extras()...")
    cursor.execute("CALL sp_consultas_extras()")

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
    ORDER BY receita_total DESC;
    """
    print("\nSQL (parte 1 da procedure sp_consultas_extras):")
    print(query_extra1)

    resultados = cursor.fetchall()
    print(f"\n{'Categoria':<15} {'Pedidos':<9} {'Qtd Vendida':<13} {'Receita Total':>15} {'Preço Médio':>14}")
    print("-" * 75)
    for row in resultados:
        print(f"{row[0]:<15} {row[1]:<9} {row[2]:<13} R$ {row[3]:>11,.2f} R$ {row[4]:>10,.2f}")

    # EXTRA 2: Top 10 Produtos Mais Vendidos
    if cursor.nextset():
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
        LIMIT 10;
        """
        print("\nSQL (parte 2 da procedure sp_consultas_extras):")
        print(query_extra2)

        resultados = cursor.fetchall()
        print(f"\n{'Produto':<25} {'Categoria':<13} {'Qtd Vendida':<13} {'Receita':>12}")
        print("-" * 70)
        for row in resultados:
            print(f"{row[0]:<25} {row[1]:<13} {row[2]:<13} R$ {row[3]:>9,.2f}")

    # EXTRA 3: Vendas por Estado
    if cursor.nextset():
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
        ORDER BY receita_total DESC;
        """
        print("\nSQL (parte 3 da procedure sp_consultas_extras):")
        print(query_extra3)

        resultados = cursor.fetchall()
        print(f"\n{'Estado':<8} {'Clientes':<10} {'Pedidos':<9} {'Receita Total':>15} {'Ticket Médio':>14}")
        print("-" * 65)
        for row in resultados:
            print(f"{row[0]:<8} {row[1]:<10} {row[2]:<9} R$ {row[3]:>11,.2f} R$ {row[4]:>10,.2f}")


def executar_consultas(conn):
    """Atalho: cria as procedures de consulta e executa todas."""
    criar_procedures_consultas()
    print("\n\n" + "=" * 80)
    print("SEÇÃO 3: CONSULTAS SQL (TODAS)")
    print("=" * 80)
    consulta_1(conn)
    consulta_2(conn)
    consulta_3(conn)
    consultas_extras(conn)


# =================================================================================
# INTERFACE DE MENU NO TERMINAL
# =================================================================================

def opcao_criar_ou_acessar_banco():
    print("\n" + "=" * 80)
    print("OPÇÃO 1: CRIAÇÃO OU ACESSO AO BANCO DE DADOS (MySQL)")
    print("=" * 80)
    
    criar_banco_se_nao_existir()
    try:
        conn = get_connection()
        conn.close()
        print(f"\nConexão com o banco '{DB_CONFIG['database']}' realizada com sucesso.")
    except Error as e:
        print(f"\nERRO ao conectar ao banco: {e}")
    
    print("=" * 80)


def opcao_criacao_tabelas():
    criar_procedure_criar_tabelas()
    conn = criar_tabelas()
    conn.close()
    print("\nConexão fechada após criação das tabelas.")


def opcao_insercao_dados():
    print("\n" + "=" * 80)
    print("OPÇÃO 3: INSERÇÃO DOS DADOS")
    print("=" * 80)
    
    criar_procedure_inserir_dados()
    
    conn = get_connection()
    try:
        inserir_dados(conn)
    except Exception as e:
        print(f"\nERRO ao inserir dados: {e}")
    finally:
        conn.close()
        print("\nConexão fechada após inserção dos dados.")


def opcao_consulta_1():
    conn = get_connection()
    try:
        criar_procedure_consulta_1()
        consulta_1(conn)
    except Exception as e:
        print(f"\nERRO na consulta 1: {e}")
    finally:
        conn.close()


def opcao_consulta_2():
    conn = get_connection()
    try:
        criar_procedure_consulta_2()
        consulta_2(conn)
    except Exception as e:
        print(f"\nERRO na consulta 2: {e}")
    finally:
        conn.close()


def opcao_consulta_3():
    conn = get_connection()
    try:
        criar_procedure_consulta_3()
        consulta_3(conn)
    except Exception as e:
        print(f"\nERRO na consulta 3: {e}")
    finally:
        conn.close()


def opcao_consultas_extras():
    conn = get_connection()
    try:
        criar_procedure_consultas_extras()
        consultas_extras(conn)
    except Exception as e:
        print(f"\nERRO nas consultas extras: {e}")
    finally:
        conn.close()


def mostrar_menu():
    print("\n" + "=" * 80)
    print("     SISTEMA DE BANCO DE DADOS E-COMMERCE (MySQL)")
    print("     MENU PRINCIPAL")
    print("=" * 80)
    print("1 - Criação ou acesso ao banco de dados")
    print("2 - Criação das tabelas")
    print("3 - Inserção dos dados ")
    print("4 - CONSULTA 1: JOIN COM 2 TABELAS")
    print("5 - CONSULTA 2: JOIN COM MÚLTIPLAS TABELAS")
    print("6 - CONSULTA 3: JOIN COM SUBSELECT ")
    print("7 - CONSULTAS EXTRAS")
    print("8 - Executar TODAS as consultas")
    print("0 - Sair")
    print("=" * 80)


# =================================================================================
# FUNÇÃO PRINCIPAL (USA O MENU)
# =================================================================================

def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            opcao_criar_ou_acessar_banco()
        elif opcao == "2":
            opcao_criacao_tabelas()
        elif opcao == "3":
            opcao_insercao_dados()
        elif opcao == "4":
            opcao_consulta_1()
        elif opcao == "5":
            opcao_consulta_2()
        elif opcao == "6":
            opcao_consulta_3()
        elif opcao == "7":
            opcao_consultas_extras()
        elif opcao == "8":
            conn = get_connection()
            try:
                executar_consultas(conn)
            except Exception as e:
                print(f"\nERRO ao executar todas as consultas: {e}")
            finally:
                conn.close()
        elif opcao == "0":
            print("\nSaindo do sistema... Até logo!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()


