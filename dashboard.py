"""
=================================================================================
Dashboard E-commerce - MySQL
Para executar: python dashboard.py
Acesse em: http://127.0.0.1:8050
=================================================================================
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Configuração da conexão com o MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Giuseppe1490",
    "database": "ecommerce",
}

def get_connection():
    """Retorna uma conexão ativa com o banco MySQL 'ecommerce'."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"\nERRO ao conectar ao banco de dados: {e}")
        print("Verifique se o MySQL está rodando e se o banco 'ecommerce' existe.")
        print("Execute primeiro: python banco_dados.py")
        exit(1)

# =================================================================================
# FUNÇÕES PARA CARREGAR DADOS
# =================================================================================

def carregar_dados():
    """Carrega todos os dados necessários para o dashboard"""
    conn = get_connection()
    
    # Query 1: Vendas por Categoria
    query_categoria = """
    SELECT 
        prod.categoria,
        COUNT(DISTINCT ip.id_pedido) AS total_pedidos,
        SUM(ip.quantidade) AS quantidade_vendida,
        SUM(ip.subtotal) AS receita_total
    FROM produtos prod
    INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
    GROUP BY prod.categoria
    ORDER BY receita_total DESC
    """
    df_categoria = pd.read_sql_query(query_categoria, conn)
    
    # Query 2: Top Produtos
    query_produtos = """
    SELECT 
        prod.nome_produto,
        prod.categoria,
        SUM(ip.quantidade) AS quantidade_vendida,
        SUM(ip.subtotal) AS receita_gerada
    FROM produtos prod
    INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
    GROUP BY prod.id_produto, prod.nome_produto, prod.categoria
    ORDER BY receita_gerada DESC
    LIMIT 10
    """
    df_produtos = pd.read_sql_query(query_produtos, conn)
    
    # Query 3: Vendas por Estado
    query_estado = """
    SELECT 
        c.estado,
        COUNT(DISTINCT c.id_cliente) AS total_clientes,
        COUNT(DISTINCT p.id_pedido) AS total_pedidos,
        SUM(p.valor_total) AS receita_total
    FROM clientes c
    INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
    GROUP BY c.estado
    ORDER BY receita_total DESC
    """
    df_estado = pd.read_sql_query(query_estado, conn)
    
    # Query 4: Vendas ao longo do tempo (por mês)
    query_tempo = """
    SELECT 
        DATE_FORMAT(p.data_pedido, '%%Y-%%m') as mes,
        COUNT(p.id_pedido) AS total_pedidos,
        SUM(p.valor_total) AS receita
    FROM pedidos p
    GROUP BY DATE_FORMAT(p.data_pedido, '%%Y-%%m')
    ORDER BY mes
    """
    df_tempo = pd.read_sql_query(query_tempo, conn)
    df_tempo['mes'] = pd.to_datetime(df_tempo['mes'])
    
    # Query 5: Status dos Pedidos
    query_status = """
    SELECT 
        status,
        COUNT(*) AS quantidade,
        SUM(valor_total) AS valor_total
    FROM pedidos
    GROUP BY status
    """
    df_status = pd.read_sql_query(query_status, conn)
    
    # Query 6: Top Clientes
    query_clientes = """
    SELECT 
        c.nome AS cliente,
        c.cidade,
        c.estado,
        COUNT(p.id_pedido) AS total_pedidos,
        SUM(p.valor_total) AS valor_total_gasto
    FROM clientes c
    INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
    GROUP BY c.id_cliente, c.nome, c.cidade, c.estado
    ORDER BY valor_total_gasto DESC
    LIMIT 10
    """
    df_clientes = pd.read_sql_query(query_clientes, conn)
    
    # Query 7: Vendas por Categoria e Quantidade
    query_categoria_qtd = """
    SELECT 
        prod.categoria,
        SUM(ip.quantidade) AS quantidade_vendida,
        SUM(ip.subtotal) AS receita_total
    FROM produtos prod
    INNER JOIN itens_pedido ip ON prod.id_produto = ip.id_produto
    GROUP BY prod.categoria
    ORDER BY quantidade_vendida DESC
    """
    df_categoria_qtd = pd.read_sql_query(query_categoria_qtd, conn)
    
    # Métricas gerais
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE ativo = 1")
    total_clientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(valor_total) FROM pedidos")
    receita_total = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT AVG(valor_total) FROM pedidos")
    ticket_medio = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT categoria) FROM produtos")
    total_categorias = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return {
        'categoria': df_categoria,
        'produtos': df_produtos,
        'estado': df_estado,
        'tempo': df_tempo,
        'status': df_status,
        'clientes': df_clientes,
        'categoria_qtd': df_categoria_qtd,
        'metricas': {
            'total_clientes': total_clientes,
            'total_pedidos': total_pedidos,
            'receita_total': receita_total,
            'ticket_medio': ticket_medio,
            'total_produtos': total_produtos,
            'total_categorias': total_categorias
        }
    }

# =================================================================================
# CONFIGURAÇÃO DO DASHBOARD
# =================================================================================

# Carregar dados
print("\nCarregando dados do banco de dados...")
dados = carregar_dados()
print("Dados carregados com sucesso!\n")

# Criar aplicação Dash
app = Dash(__name__)

# Cores do tema
cores = {
    'background': '#f8f9fa',
    'card': '#ffffff',
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c'
}

# =================================================================================
# LAYOUT DO DASHBOARD
# =================================================================================

app.layout = html.Div(style={'backgroundColor': cores['background'], 'padding': '20px'}, children=[
    
    # Cabeçalho
    html.Div([
        html.H1('📊 Dashboard E-commerce - Análise de Vendas', 
                style={'textAlign': 'center', 'color': cores['primary'], 'marginBottom': '10px'}),
        html.P('Sistema de análise de vendas em tempo real - MySQL Database',
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px'})
    ]),
    
    html.Hr(),
    
    # Cards de Métricas - Linha 1
    html.Div([
        html.Div([
            html.Div([
                html.H4('👥 Clientes Ativos', style={'color': cores['primary']}),
                html.H2(f"{dados['metricas']['total_clientes']}", 
                       style={'color': cores['secondary'], 'fontWeight': 'bold'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('📦 Total de Pedidos', style={'color': cores['primary']}),
                html.H2(f"{dados['metricas']['total_pedidos']}", 
                       style={'color': cores['success'], 'fontWeight': 'bold'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('💰 Receita Total', style={'color': cores['primary']}),
                html.H2(f"R$ {dados['metricas']['receita_total']:,.2f}", 
                       style={'color': cores['warning'], 'fontWeight': 'bold', 'fontSize': '24px'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('🎯 Ticket Médio', style={'color': cores['primary']}),
                html.H2(f"R$ {dados['metricas']['ticket_medio']:,.2f}", 
                       style={'color': cores['danger'], 'fontWeight': 'bold', 'fontSize': '24px'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
    ], style={'marginBottom': '20px'}),
    
    # Cards de Métricas - Linha 2
    html.Div([
        html.Div([
            html.Div([
                html.H4('📊 Total Produtos', style={'color': cores['primary']}),
                html.H2(f"{dados['metricas']['total_produtos']}", 
                       style={'color': '#9b59b6', 'fontWeight': 'bold'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('🏷️ Categorias', style={'color': cores['primary']}),
                html.H2(f"{dados['metricas']['total_categorias']}", 
                       style={'color': '#16a085', 'fontWeight': 'bold'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ], style={'marginBottom': '30px'}),
    
    # Primeira linha de gráficos - PRINCIPAIS
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-tempo')
        ], style={'width': '98%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Segunda linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-categoria')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            dcc.Graph(id='grafico-estado')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Terceira linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-produtos')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            dcc.Graph(id='grafico-clientes')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Quarta linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-status')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            dcc.Graph(id='grafico-categoria-qtd')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Rodapé
    html.Div([
        html.Hr(),
        html.P('Dashboard desenvolvido em Python com Dash e Plotly | Banco de dados MySQL',
               style={'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '30px'})
    ])
])

# =================================================================================
# CALLBACKS - ATUALIZAÇÃO DOS GRÁFICOS
# =================================================================================

@app.callback(
    Output('grafico-tempo', 'figure'),
    Input('grafico-tempo', 'id')
)
def update_tempo(_):
    """Gráfico de linha - Evolução de vendas ao longo do tempo"""
    fig = go.Figure()
    
    # Linha de receita
    fig.add_trace(go.Scatter(
        x=dados['tempo']['mes'], 
        y=dados['tempo']['receita'],
        mode='lines+markers',
        name='Receita',
        line=dict(color=cores['secondary'], width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))
    
    fig.update_layout(
        title='📈 Evolução de Vendas ao Longo do Tempo (Mensal)',
        xaxis_title='Período',
        yaxis_title='Receita (R$)',
        plot_bgcolor='white',
        hovermode='x unified',
        height=400
    )
    return fig

@app.callback(
    Output('grafico-categoria', 'figure'),
    Input('grafico-categoria', 'id')
)
def update_categoria(_):
    """Gráfico de barras - Receita por categoria"""
    fig = px.bar(
        dados['categoria'], 
        x='categoria', 
        y='receita_total',
        title='💼 Receita por Categoria de Produto',
        labels={'receita_total': 'Receita (R$)', 'categoria': 'Categoria'},
        color='receita_total',
        color_continuous_scale='Blues',
        text='receita_total'
    )
    fig.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
    fig.update_layout(showlegend=False, plot_bgcolor='white', height=400)
    return fig

@app.callback(
    Output('grafico-estado', 'figure'),
    Input('grafico-estado', 'id')
)
def update_estado(_):
    """Gráfico de pizza - Distribuição por estado"""
    fig = px.pie(
        dados['estado'], 
        values='receita_total', 
        names='estado',
        title='🗺️ Distribuição de Receita por Estado',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output('grafico-produtos', 'figure'),
    Input('grafico-produtos', 'id')
)
def update_produtos(_):
    """Gráfico de barras horizontais - Top produtos"""
    fig = px.bar(
        dados['produtos'], 
        x='receita_gerada', 
        y='nome_produto',
        title='🏆 Top 10 Produtos Mais Vendidos',
        labels={'receita_gerada': 'Receita (R$)', 'nome_produto': 'Produto'},
        orientation='h',
        color='receita_gerada',
        color_continuous_scale='Greens',
        text='receita_gerada'
    )
    fig.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
    fig.update_layout(
        showlegend=False, 
        plot_bgcolor='white', 
        yaxis={'categoryorder':'total ascending'},
        height=400
    )
    return fig

@app.callback(
    Output('grafico-clientes', 'figure'),
    Input('grafico-clientes', 'id')
)
def update_clientes(_):
    """Gráfico de barras horizontais - Top clientes"""
    fig = px.bar(
        dados['clientes'], 
        x='valor_total_gasto', 
        y='cliente',
        title='👑 Top 10 Clientes VIP (Maior Valor de Compra)',
        labels={'valor_total_gasto': 'Valor Gasto (R$)', 'cliente': 'Cliente'},
        orientation='h',
        color='valor_total_gasto',
        color_continuous_scale='Reds',
        text='valor_total_gasto'
    )
    fig.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
    fig.update_layout(
        showlegend=False, 
        plot_bgcolor='white', 
        yaxis={'categoryorder':'total ascending'},
        height=400
    )
    return fig

@app.callback(
    Output('grafico-status', 'figure'),
    Input('grafico-status', 'id')
)
def update_status(_):
    """Gráfico de barras - Status dos pedidos"""
    fig = px.bar(
        dados['status'], 
        x='status', 
        y='quantidade',
        title='📦 Status dos Pedidos',
        labels={'quantidade': 'Quantidade', 'status': 'Status'},
        color='status',
        color_discrete_sequence=px.colors.qualitative.Set2,
        text='quantidade'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, plot_bgcolor='white', height=400)
    return fig

@app.callback(
    Output('grafico-categoria-qtd', 'figure'),
    Input('grafico-categoria-qtd', 'id')
)
def update_categoria_qtd(_):
    """Gráfico de rosca - Quantidade vendida por categoria"""
    fig = px.pie(
        dados['categoria_qtd'], 
        values='quantidade_vendida', 
        names='categoria',
        title='📊 Quantidade Vendida por Categoria',
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    return fig

# =================================================================================
# EXECUTAR SERVIDOR
# =================================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("INICIANDO DASHBOARD E-COMMERCE...")
    print("=" * 80)
    print("\nDashboard disponível em: http://127.0.0.1:8050")
    print("Pressione CTRL+C para encerrar o servidor\n")
    print("=" * 80 + "\n")
    
    app.run_server(debug=True, port=8050)
