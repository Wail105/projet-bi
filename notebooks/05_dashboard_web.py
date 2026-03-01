import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================
engine = create_engine('mysql+pymysql://root:@localhost/dw_agriculture')

fait = pd.read_sql("SELECT * FROM fait_meteo", engine)
dim_station = pd.read_sql("SELECT * FROM dim_station", engine)
dim_temps = pd.read_sql("SELECT * FROM dim_temps", engine)
dim_alerte = pd.read_sql("SELECT * FROM dim_alerte", engine)

df = fait.merge(dim_station, on='id_station', how='left')
df = df.merge(dim_temps, on='id_date', how='left')
df = df.merge(dim_alerte, on='id_alerte', how='left')
df = df.rename(columns={'severity_index_x': 'severity_index'})
df = df.drop(columns=['severity_index_y'], errors='ignore')

mois_labels = {1:'Jan', 2:'Fév', 3:'Mar', 4:'Avr', 5:'Mai', 6:'Jun',
               7:'Jul', 8:'Aoû', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Déc'}
df['mois_label'] = df['mois'].map(mois_labels)

# ============================================
# APP
# ============================================
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.CYBORG,
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap'
])

# ============================================
# STYLES
# ============================================
COLORS = {
    'bg': '#020818',
    'card': '#0a1628',
    'card2': '#0d1f3c',
    'accent': '#00d4ff',
    'accent2': '#7b2ff7',
    'green': '#00ff88',
    'red': '#ff4757',
    'orange': '#ffa502',
    'yellow': '#ffdd59',
    'text': '#e8f4f8',
    'subtext': '#5a7a9a',
    'grid': '#0f2a4a',
    'glow': '0 0 20px rgba(0, 212, 255, 0.3)',
    'glow_red': '0 0 20px rgba(255, 71, 87, 0.4)',
}

card_style = {
    'backgroundColor': COLORS['card'],
    'border': f'1px solid {COLORS["accent"]}22',
    'borderRadius': '16px',
    'boxShadow': COLORS['glow'],
    'transition': 'all 0.3s ease',
    'overflow': 'hidden'
}

filter_style = {
    'backgroundColor': COLORS['card2'],
    'color': COLORS['text'],
    'border': f'1px solid {COLORS["accent"]}44',
    'borderRadius': '10px',
}

# ============================================
# LAYOUT
# ============================================
app.layout = html.Div([

    # ANIMATED BACKGROUND
    html.Div(style={
        'position': 'fixed', 'top': 0, 'left': 0,
        'width': '100%', 'height': '100%',
        'background': f'radial-gradient(ellipse at 20% 50%, {COLORS["accent2"]}15 0%, transparent 50%), radial-gradient(ellipse at 80% 20%, {COLORS["accent"]}10 0%, transparent 50%), {COLORS["bg"]}',
        'zIndex': -1
    }),

    dbc.Container([

        # HEADER
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("🌍", style={'fontSize': '50px', 'textAlign': 'center'}),
                    html.H1("AGRICULTURE-RÉSILIENCE 2030",
                            style={
                                'fontFamily': 'Orbitron, sans-serif',
                                'color': COLORS['accent'],
                                'textAlign': 'center',
                                'fontSize': '2rem',
                                'fontWeight': '900',
                                'letterSpacing': '4px',
                                'textShadow': f'0 0 30px {COLORS["accent"]}',
                                'marginBottom': '5px'
                            }),
                    html.P("PLATEFORME DÉCISIONNELLE STRATÉGIQUE — MINISTÈRE DE L'AGRICULTURE DU MAROC",
                           style={
                               'fontFamily': 'Rajdhani, sans-serif',
                               'color': COLORS['subtext'],
                               'textAlign': 'center',
                               'letterSpacing': '2px',
                               'fontSize': '0.8rem'
                           }),
                    html.Div(style={
                        'height': '2px',
                        'background': f'linear-gradient(90deg, transparent, {COLORS["accent"]}, {COLORS["accent2"]}, transparent)',
                        'marginTop': '15px'
                    })
                ], style={'padding': '30px 0 10px 0'})
            ])
        ]),

        # FILTRES
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("🗺️ ZONE GÉOGRAPHIQUE",
                               style={'color': COLORS['accent'], 'fontFamily': 'Rajdhani',
                                      'letterSpacing': '1px', 'fontSize': '0.75rem', 'fontWeight': '600'}),
                    dcc.Dropdown(
                        id='filter-zone',
                        options=[{'label': '✦ Toutes les zones', 'value': 'all'}] +
                                [{'label': z, 'value': z} for z in sorted(df['zone_geo'].unique())],
                        value='all',
                        style=filter_style,
                        className='custom-dropdown'
                    )
                ], style={'padding': '5px'})
            ], width=3),
            dbc.Col([
                html.Div([
                    html.Label("📅 MOIS",
                               style={'color': COLORS['accent'], 'fontFamily': 'Rajdhani',
                                      'letterSpacing': '1px', 'fontSize': '0.75rem', 'fontWeight': '600'}),
                    dcc.Dropdown(
                        id='filter-mois',
                        options=[{'label': '✦ Tous les mois', 'value': 0}] +
                                [{'label': v, 'value': k} for k, v in mois_labels.items()],
                        value=0,
                        style=filter_style,
                    )
                ], style={'padding': '5px'})
            ], width=3),
            dbc.Col([
                html.Div([
                    html.Label("🚨 NIVEAU D'ALERTE",
                               style={'color': COLORS['accent'], 'fontFamily': 'Rajdhani',
                                      'letterSpacing': '1px', 'fontSize': '0.75rem', 'fontWeight': '600'}),
                    dcc.Dropdown(
                        id='filter-severity',
                        options=[{'label': '✦ Tous les niveaux', 'value': 'all'},
                                 {'label': '🟢 RAS', 'value': 'RAS'},
                                 {'label': '🟡 Jaune', 'value': 'Jaune'},
                                 {'label': '🟠 Orange', 'value': 'Orange'},
                                 {'label': '🔴 Rouge', 'value': 'Rouge'}],
                        value='all',
                        style=filter_style,
                    )
                ], style={'padding': '5px'})
            ], width=3),
            dbc.Col([
                html.Div([
                    html.Label("🔧 TYPE CAPTEUR",
                               style={'color': COLORS['accent'], 'fontFamily': 'Rajdhani',
                                      'letterSpacing': '1px', 'fontSize': '0.75rem', 'fontWeight': '600'}),
                    dcc.Dropdown(
                        id='filter-capteur',
                        options=[{'label': '✦ Tous', 'value': 'all'}] +
                                [{'label': c, 'value': c} for c in df['capteur_type'].unique()],
                        value='all',
                        style=filter_style,
                    )
                ], style={'padding': '5px'})
            ], width=3),
        ], style={
            'backgroundColor': COLORS['card'],
            'borderRadius': '16px',
            'border': f'1px solid {COLORS["accent"]}22',
            'padding': '15px',
            'marginBottom': '20px',
            'boxShadow': COLORS['glow']
        }),

        # KPI CARDS
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("📋", style={'fontSize': '2rem', 'textAlign': 'center'}),
                    html.H2(id='kpi-releves', style={
                        'color': COLORS['accent'], 'textAlign': 'center',
                        'fontFamily': 'Orbitron', 'fontWeight': '700',
                        'textShadow': f'0 0 20px {COLORS["accent"]}',
                        'margin': '5px 0'
                    }),
                    html.P("TOTAL RELEVÉS", style={
                        'color': COLORS['subtext'], 'textAlign': 'center',
                        'fontFamily': 'Rajdhani', 'letterSpacing': '2px',
                        'fontSize': '0.7rem', 'margin': 0
                    })
                ], style={**card_style, 'padding': '20px',
                          'borderTop': f'3px solid {COLORS["accent"]}'})
            ], width=3),

            dbc.Col([
                html.Div([
                    html.Div("🌡️", style={'fontSize': '2rem', 'textAlign': 'center'}),
                    html.H2(id='kpi-temp', style={
                        'color': COLORS['orange'], 'textAlign': 'center',
                        'fontFamily': 'Orbitron', 'fontWeight': '700',
                        'textShadow': f'0 0 20px {COLORS["orange"]}',
                        'margin': '5px 0'
                    }),
                    html.P("TEMP. MOYENNE", style={
                        'color': COLORS['subtext'], 'textAlign': 'center',
                        'fontFamily': 'Rajdhani', 'letterSpacing': '2px',
                        'fontSize': '0.7rem', 'margin': 0
                    })
                ], style={**card_style, 'padding': '20px',
                          'borderTop': f'3px solid {COLORS["orange"]}'})
            ], width=3),

            dbc.Col([
                html.Div([
                    html.Div("⚠️", style={'fontSize': '2rem', 'textAlign': 'center'}),
                    html.H2(id='kpi-risque', style={
                        'color': COLORS['yellow'], 'textAlign': 'center',
                        'fontFamily': 'Orbitron', 'fontWeight': '700',
                        'textShadow': f'0 0 20px {COLORS["yellow"]}',
                        'margin': '5px 0'
                    }),
                    html.P("INDICE RISQUE MOYEN", style={
                        'color': COLORS['subtext'], 'textAlign': 'center',
                        'fontFamily': 'Rajdhani', 'letterSpacing': '2px',
                        'fontSize': '0.7rem', 'margin': 0
                    })
                ], style={**card_style, 'padding': '20px',
                          'borderTop': f'3px solid {COLORS["yellow"]}'})
            ], width=3),

            dbc.Col([
                html.Div([
                    html.Div("🚨", style={'fontSize': '2rem', 'textAlign': 'center'}),
                    html.H2(id='kpi-alertes', style={
                        'color': COLORS['red'], 'textAlign': 'center',
                        'fontFamily': 'Orbitron', 'fontWeight': '700',
                        'textShadow': COLORS['glow_red'],
                        'margin': '5px 0'
                    }),
                    html.P("ALERTES ROUGES", style={
                        'color': COLORS['subtext'], 'textAlign': 'center',
                        'fontFamily': 'Rajdhani', 'letterSpacing': '2px',
                        'fontSize': '0.7rem', 'margin': 0
                    })
                ], style={**card_style, 'padding': '20px',
                          'borderTop': f'3px solid {COLORS["red"]}'})
            ], width=3),
        ], className='mb-4'),

        # ROW 1 GRAPHS
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-temp-zone', config={'displayModeBar': False})
                ], style=card_style)
            ], width=8),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-alertes', config={'displayModeBar': False})
                ], style=card_style)
            ], width=4),
        ], className='mb-3'),

        # ROW 2 GRAPHS
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-evolution', config={'displayModeBar': False})
                ], style=card_style)
            ], width=8),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-drill', config={'displayModeBar': False})
                ], style=card_style)
            ], width=4),
        ], className='mb-3'),

        # ROW 3 GRAPHS
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-precip', config={'displayModeBar': False})
                ], style=card_style)
            ], width=6),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-risque', config={'displayModeBar': False})
                ], style=card_style)
            ], width=6),
        ], className='mb-3'),

        # FOOTER
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div(style={
                        'height': '1px',
                        'background': f'linear-gradient(90deg, transparent, {COLORS["accent"]}, transparent)',
                        'marginBottom': '15px'
                    }),
                    html.P("🌍 Agriculture-Résilience 2030 — Ibn Tofail University — Projet BI 2025-2026",
                           style={
                               'color': COLORS['subtext'], 'textAlign': 'center',
                               'fontFamily': 'Rajdhani', 'fontSize': '0.8rem',
                               'letterSpacing': '1px'
                           })
                ])
            ])
        ], className='mb-4'),

    ], fluid=True)

], style={'backgroundColor': COLORS['bg'], 'minHeight': '100vh', 'fontFamily': 'Rajdhani, sans-serif'})


# ============================================
# CALLBACKS
# ============================================
@app.callback(
    [Output('kpi-releves', 'children'),
     Output('kpi-temp', 'children'),
     Output('kpi-risque', 'children'),
     Output('kpi-alertes', 'children'),
     Output('graph-temp-zone', 'figure'),
     Output('graph-alertes', 'figure'),
     Output('graph-precip', 'figure'),
     Output('graph-risque', 'figure'),
     Output('graph-evolution', 'figure'),
     Output('graph-drill', 'figure')],
    [Input('filter-zone', 'value'),
     Input('filter-mois', 'value'),
     Input('filter-severity', 'value'),
     Input('filter-capteur', 'value')]
)

def update_dashboard(zone, mois, severity, capteur):
    try:
        filtered = df.copy()
        if zone != 'all':
            filtered = filtered[filtered['zone_geo'] == zone]
        if mois != 0:
            filtered = filtered[filtered['mois'] == mois]
        if severity != 'all':
            filtered = filtered[filtered['severity_index'] == severity]
        if capteur != 'all':
            filtered = filtered[filtered['capteur_type'] == capteur]

        BG = COLORS['bg']
        CARD = COLORS['card']
        TEXT = COLORS['text']
        GRID = COLORS['grid']

        layout_base = dict(
            paper_bgcolor=BG,
            plot_bgcolor=CARD,
            font=dict(color=TEXT, family='Rajdhani'),
            xaxis=dict(gridcolor=GRID, showgrid=True, zeroline=False),
            yaxis=dict(gridcolor=GRID, showgrid=True, zeroline=False),
            margin=dict(l=40, r=20, t=50, b=40),
            transition={'duration': 500, 'easing': 'cubic-in-out'}
        )

        # KPIs
        kpi_releves = f"{len(filtered):,}"
        kpi_temp = f"{filtered['temp_c'].mean():.1f}°C"
        kpi_risque = f"{filtered['indice_risque'].mean():.1f}"
        kpi_alertes = str(len(filtered[filtered['severity_index'] == 'Rouge']))

        # Graph 1 — Temp par zone
        temp_zone = filtered.groupby('zone_geo')['temp_c'].mean().round(1).reset_index()
        temp_zone = temp_zone.sort_values('temp_c', ascending=False)
        fig1 = go.Figure(go.Bar(
            x=temp_zone['zone_geo'],
            y=temp_zone['temp_c'],
            marker=dict(
                color=temp_zone['temp_c'],
                colorscale=[[0, '#00ff88'], [0.5, '#ffa502'], [1, '#ff4757']],
                showscale=True,
                colorbar=dict(title='°C', tickfont=dict(color=TEXT)),
                line=dict(color=COLORS['bg'], width=1)
            ),
            text=temp_zone['temp_c'].astype(str) + '°C',
            textposition='outside',
            textfont=dict(color=TEXT, size=11),
        ))
        fig1.update_layout(
            title=dict(text='🌡️ Température Moyenne par Zone Géographique',
                       font=dict(color=COLORS['accent'], size=14, family='Orbitron')),
            paper_bgcolor=BG,
            plot_bgcolor=CARD,
            font=dict(color=TEXT, family='Rajdhani'),
            xaxis=dict(gridcolor=GRID, tickangle=-30, color=TEXT, showgrid=True, zeroline=False),
            yaxis=dict(gridcolor=GRID, showgrid=True, zeroline=False),
            margin=dict(l=40, r=20, t=50, b=40),
            transition={'duration': 500, 'easing': 'cubic-in-out'},
            bargap=0.3
        )

        # Graph 2 — Alertes donut
        alertes_count = filtered['severity_index'].value_counts().reset_index()
        alertes_count.columns = ['Severity', 'Count']
        colors_map = {'Rouge': '#ff4757', 'Orange': '#ffa502',
                      'Jaune': '#ffdd59', 'RAS': '#00ff88'}
        fig2 = go.Figure(go.Pie(
            labels=alertes_count['Severity'],
            values=alertes_count['Count'],
            hole=0.65,
            marker=dict(
                colors=[colors_map.get(s, '#888') for s in alertes_count['Severity']],
                line=dict(color=BG, width=4)
            ),
            textfont=dict(color=TEXT, size=12),
            hovertemplate='<b>%{label}</b><br>%{value} relevés<br>%{percent}<extra></extra>'
        ))
        total = len(filtered)
        fig2.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:10px'>relevés</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=TEXT, family='Orbitron')
        )
        fig2.update_layout(
            title=dict(text='🚨 Répartition des Alertes',
                       font=dict(color=COLORS['accent'], size=14, family='Orbitron')),
            paper_bgcolor=BG,
            font=dict(color=TEXT),
            legend=dict(font=dict(color=TEXT), bgcolor=CARD),
            margin=dict(l=20, r=20, t=50, b=20),
            transition={'duration': 500}
        )

        # Graph 3 — Précipitations
        precip = filtered.groupby('mois')['precip_mm'].sum().reset_index()
        precip['mois_label'] = precip['mois'].map(mois_labels)
        fig3 = go.Figure(go.Bar(
            x=precip['mois_label'],
            y=precip['precip_mm'],
            marker=dict(
                color=precip['precip_mm'],
                colorscale='Blues',
                line=dict(color=COLORS['accent'], width=1)
            ),
            text=precip['precip_mm'].round(0).astype(int),
            textposition='outside',
            textfont=dict(color=TEXT)
        ))
        fig3.update_layout(
            title=dict(text='🌧️ Précipitations Totales par Mois',
                       font=dict(color=COLORS['accent'], size=14, family='Orbitron')),
            **layout_base
        )

        # Graph 4 — Risque par zone
        risque = filtered.groupby('zone_geo')['indice_risque'].mean().round(2).reset_index()
        risque = risque.sort_values('indice_risque', ascending=True)
        colors_r = ['#ff4757' if v > 60 else '#ffa502' if v > 45 else '#00ff88'
                    for v in risque['indice_risque']]
        fig4 = go.Figure(go.Bar(
            x=risque['indice_risque'],
            y=risque['zone_geo'],
            orientation='h',
            marker=dict(color=colors_r, line=dict(color=BG, width=1)),
            text=risque['indice_risque'],
            textposition='outside',
            textfont=dict(color=TEXT)
        ))
        fig4.add_vline(x=60, line_dash='dash', line_color='#ff4757', line_width=1.5,
                       annotation_text='⚠ Critique', annotation_font_color='#ff4757')
        fig4.add_vline(x=45, line_dash='dash', line_color='#ffa502', line_width=1.5,
                       annotation_text='⚠ Alerte', annotation_font_color='#ffa502')
        fig4.update_layout(
            title=dict(text='⚠️ Indice de Risque Moyen par Zone',
                       font=dict(color=COLORS['accent'], size=14, family='Orbitron')),
            **layout_base
        )

        # Graph 5 — Evolution
        temp_mois = filtered.groupby('mois').agg(
            Temp_Max=('temp_c', 'max'),
            Temp_Min=('temp_c', 'min'),
            Temp_Moy=('temp_c', 'mean')
        ).round(1).reset_index()
        temp_mois['mois_label'] = temp_mois['mois'].map(mois_labels)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=temp_mois['mois_label'], y=temp_mois['Temp_Max'],
            name='Maximum', mode='lines+markers',
            line=dict(color='#ff4757', width=2.5, shape='spline'),
            marker=dict(size=7, color='#ff4757', line=dict(color=BG, width=2))
        ))
        fig5.add_trace(go.Scatter(
            x=temp_mois['mois_label'], y=temp_mois['Temp_Moy'],
            name='Moyenne', mode='lines+markers',
            line=dict(color=COLORS['accent'], width=2.5, shape='spline'),
            fill='tonexty', fillcolor='rgba(255,71,87,0.08)',
            marker=dict(size=7, color=COLORS['accent'], line=dict(color=BG, width=2))
        ))
        fig5.add_trace(go.Scatter(
            x=temp_mois['mois_label'], y=temp_mois['Temp_Min'],
            name='Minimum', mode='lines+markers',
            line=dict(color=COLORS['green'], width=2.5, shape='spline'),
            fill='tonexty', fillcolor='rgba(0,212,255,0.08)',
            marker=dict(size=7, color=COLORS['green'], line=dict(color=BG, width=2))
        ))
        fig5.update_layout(
            title=dict(text='📈 Évolution des Températures par Mois',
                       font=dict(color=COLORS['accent'], size=14, family='Orbitron')),
            **layout_base,
            legend=dict(bgcolor=CARD, font=dict(color=TEXT),
                        bordercolor='rgba(0, 212, 255, 0.3)', borderwidth=1)
        )

        # Graph 6 — Sunburst Drill-down
        drill = filtered.groupby(['zone_geo', 'ville', 'nom_station'])['indice_risque'].mean().round(2).reset_index()
        fig6 = px.sunburst(
            drill,
            path=['zone_geo', 'ville', 'nom_station'],
            values='indice_risque',
            color='indice_risque',
            color_continuous_scale=[[0, '#00ff88'], [0.5, '#ffa502'], [1, '#ff4757']],
            title='🔍 Drill-down Zone → Ville → Station'
        )
        fig6.update_layout(
            paper_bgcolor=BG,
            font=dict(color=TEXT, family='Rajdhani'),
            title=dict(font=dict(color=COLORS['accent'], size=14, family='Orbitron')),
            margin=dict(l=10, r=10, t=50, b=10),
            transition={'duration': 500}
        )
        fig6.update_traces(
            textfont=dict(color=TEXT),
            insidetextorientation='radial'
        )

        return (kpi_releves, kpi_temp, kpi_risque, kpi_alertes,
                fig1, fig2, fig3, fig4, fig5, fig6)

    except Exception as e:
        print(f"ERREUR DÉTAILLÉE: {e}")
        raise e





if __name__ == '__main__':
    app.run(debug=True, port=8050)