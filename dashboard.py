"""
=================================================================================
Para executar: python dashboard.py
Acesse em: http://127.0.0.1:8050
=================================================================================
"""

import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import os

# Verificar se o banco existe
if not os.path.exists('ecommerce.db'):
    print("\nERRO: Banco de dados não encontrado!")
    print("Execute primeiro: python banco_dados.py")
    exit(1)

# =================================================================================
# FUNÇÕES PARA CARREGAR DADOS
# =================================================================================

def carregar_dados():
    """Carrega todos os dados necessários para o dashboard"""
    conn = sqlite3.connect('ecommerce.db')
    
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
    
    # Query 4: Vendas ao longo do tempo
    query_tempo = """
    SELECT 
        DATE(p.data_pedido) as data,
        COUNT(p.id_pedido) AS total_pedidos,
        SUM(p.valor_total) AS receita
    FROM pedidos p
    GROUP BY DATE(p.data_pedido)
    ORDER BY data
    """
    df_tempo = pd.read_sql_query(query_tempo, conn)
    df_tempo['data'] = pd.to_datetime(df_tempo['data'])
    
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
    
    # Métricas gerais
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(valor_total) FROM pedidos")
    receita_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(valor_total) FROM pedidos")
    ticket_medio = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'categoria': df_categoria,
        'produtos': df_produtos,
        'estado': df_estado,
        'tempo': df_tempo,
        'status': df_status,
        'clientes': df_clientes,
        'metricas': {
            'total_clientes': total_clientes,
            'total_pedidos': total_pedidos,
            'receita_total': receita_total,
            'ticket_medio': ticket_medio
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
        html.H1('Dashboard E-commerce - Análise de Vendas', 
                style={'textAlign': 'center', 'color': cores['primary'], 'marginBottom': '10px'}),
        html.P('Sistema de análise de vendas com dados em tempo real',
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px'})
    ]),
    
    html.Hr(),
    
    # Cards de Métricas
    html.Div([
        html.Div([
            html.Div([
                html.H4('Total de Clientes', style={'color': cores['primary']}),
                html.H2(f"{dados['metricas']['total_clientes']}", 
                       style={'color': cores['secondary'], 'fontWeight': 'bold'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('Total de Pedidos', style={'color': cores['primary']}),
                html.H2(f"{dados['metricas']['total_pedidos']}", 
                       style={'color': cores['success'], 'fontWeight': 'bold'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('Receita Total', style={'color': cores['primary']}),
                html.H2(f"R$ {dados['metricas']['receita_total']:,.2f}", 
                       style={'color': cores['warning'], 'fontWeight': 'bold', 'fontSize': '24px'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4('Ticket Médio', style={'color': cores['primary']}),
                html.H2(f"R$ {dados['metricas']['ticket_medio']:,.2f}", 
                       style={'color': cores['danger'], 'fontWeight': 'bold', 'fontSize': '24px'})
            ], style={'backgroundColor': cores['card'], 'padding': '20px', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
    ], style={'marginBottom': '30px'}),
    
    # Primeira linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-categoria')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            dcc.Graph(id='grafico-produtos')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Segunda linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-estado')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            dcc.Graph(id='grafico-tempo')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Terceira linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-status')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            dcc.Graph(id='grafico-clientes')
        ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
    ]),
    
    # Rodapé
    html.Div([
        html.Hr(),
        html.P('Dashboard desenvolvido em Python com Dash e Plotly | Banco de dados SQLite',
               style={'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '30px'})
    ])
])

# =================================================================================
# CALLBACKS - ATUALIZAÇÃO DOS GRÁFICOS
# =================================================================================

@app.callback(
    Output('grafico-categoria', 'figure'),
    Input('grafico-categoria', 'id')
)
def update_categoria(_):
    fig = px.bar(dados['categoria'], 
                 x='categoria', 
                 y='receita_total',
                 title='Receita por Categoria de Produto',
                 labels={'receita_total': 'Receita (R$)', 'categoria': 'Categoria'},
                 color='receita_total',
                 color_continuous_scale='Blues')
    fig.update_layout(showlegend=False, plot_bgcolor='white')
    return fig

@app.callback(
    Output('grafico-produtos', 'figure'),
    Input('grafico-produtos', 'id')
)
def update_produtos(_):
    fig = px.bar(dados['produtos'], 
                 x='receita_gerada', 
                 y='nome_produto',
                 title='Top 10 Produtos Mais Vendidos',
                 labels={'receita_gerada': 'Receita (R$)', 'nome_produto': 'Produto'},
                 orientation='h',
                 color='receita_gerada',
                 color_continuous_scale='Greens')
    fig.update_layout(showlegend=False, plot_bgcolor='white', yaxis={'categoryorder':'total ascending'})
    return fig

@app.callback(
    Output('grafico-estado', 'figure'),
    Input('grafico-estado', 'id')
)
def update_estado(_):
    fig = px.pie(dados['estado'], 
                 values='receita_total', 
                 names='estado',
                 title='Distribuição de Receita por Estado',
                 hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

@app.callback(
    Output('grafico-tempo', 'figure'),
    Input('grafico-tempo', 'id')
)
def update_tempo(_):
    fig = px.line(dados['tempo'], 
                  x='data', 
                  y='receita',
                  title='Evolução de Vendas ao Longo do Tempo',
                  labels={'receita': 'Receita (R$)', 'data': 'Data'})
    fig.update_traces(line_color=cores['secondary'], line_width=3)
    fig.update_layout(plot_bgcolor='white')
    return fig

@app.callback(
    Output('grafico-status', 'figure'),
    Input('grafico-status', 'id')
)
def update_status(_):
    fig = px.bar(dados['status'], 
                 x='status', 
                 y='quantidade',
                 title='Status dos Pedidos',
                 labels={'quantidade': 'Quantidade', 'status': 'Status'},
                 color='status',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(showlegend=False, plot_bgcolor='white')
    return fig

@app.callback(
    Output('grafico-clientes', 'figure'),
    Input('grafico-clientes', 'id')
)
def update_clientes(_):
    fig = px.bar(dados['clientes'], 
                 x='valor_total_gasto', 
                 y='cliente',
                 title='Top 10 Clientes (Maior Valor de Compra)',
                 labels={'valor_total_gasto': 'Valor Gasto (R$)', 'cliente': 'Cliente'},
                 orientation='h',
                 color='valor_total_gasto',
                 color_continuous_scale='Reds')
    fig.update_layout(showlegend=False, plot_bgcolor='white', yaxis={'categoryorder':'total ascending'})
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
