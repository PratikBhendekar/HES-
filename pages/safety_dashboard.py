# pages/safety_dashboard.py - Safety Dashboard with Consistent Styling

import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
from database import get_report_data

# Professional color palette for different cards
CARD_COLORS = {
    'green': '#10b981',
    'yellow': '#f59e0b',
    'purple': '#8b5cf6',
    'blue': '#667eea',
    'red': '#ef4444',
    'teal': '#14b8a6',
    'orange': '#f97316',
    'pink': '#ec4899',
    'indigo': '#6366f1',
    'cyan': '#06b6d4',
    'amber': '#fbbf24',
    'emerald': '#059669',
    'violet': '#7c3aed'
}

def safety_dashboard_page():
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            # Simple Header
            html.Div(
                style={'marginBottom': '24px'},
                children=[
                    html.H1(
                        "Safety Dashboard",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Safety Metrics & Analytics",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # Filter Section
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px',
                    'marginBottom': '24px',
                    'border': '1px solid #e9ecef'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'gap': '15px', 'alignItems': 'flex-end', 'flexWrap': 'wrap'},
                        children=[
                            html.Div(
                                style={'flex': '2', 'minWidth': '200px'},
                                children=[
                                    html.Label(
                                        'Data Source',
                                        style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}
                                    ),
                                    dcc.Dropdown(
                                        id='table-select-dropdown',
                                        options=[
                                            {'label': 'Monthly Report 1', 'value': 'hes_monthly_report'},
                                            {'label': 'Monthly Report 2', 'value': 'hes_monthly_report_1'}
                                        ],
                                        value='hes_monthly_report',
                                        clearable=False,
                                        style={'borderRadius': '6px', 'fontSize': '13px'}
                                    )
                                ]
                            ),
                            html.Div(
                                style={'flex': '1', 'minWidth': '120px'},
                                children=[
                                    html.Label(
                                        'Year',
                                        style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}
                                    ),
                                    dcc.Dropdown(
                                        id='year-filter-dropdown',
                                        options=[
                                            {'label': '2024', 'value': '2024'},
                                            {'label': '2023', 'value': '2023'}
                                        ],
                                        value='2024',
                                        clearable=False,
                                        style={'borderRadius': '6px', 'fontSize': '13px'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # KPI Cards Row
            html.Div(id='kpi-cards', style={'marginBottom': '24px'}),
            
            # Charts Grid
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(id='chart-1'),
                    html.Div(id='chart-2'),
                    html.Div(id='chart-3')
                ]
            ),
            
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(id='chart-4'),
                    html.Div(id='chart-5'),
                    html.Div(id='chart-6')
                ]
            ),
            
            html.Div(id='chart-7', style={'marginBottom': '20px'}),
            html.Div(id='chart-8', style={'marginBottom': '20px'}),
            
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(id='chart-9'),
                    html.Div(id='chart-10'),
                    html.Div(id='chart-11')
                ]
            ),
            
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(id='chart-12'),
                    html.Div(id='chart-13')
                ]
            ),
            
            # Data Table Section
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': '1px solid #e9ecef'
                },
                children=[
                    html.Div(
                        style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'marginBottom': '16px',
                            'paddingBottom': '12px',
                            'borderBottom': '1px solid #eef2f6'
                        },
                        children=[
                            html.H3(
                                'Monthly Report Data',
                                style={'margin': '0', 'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.Button(
                                [html.I(className='fas fa-download', style={'marginRight': '6px'}), 'Export CSV'],
                                style={
                                    'padding': '6px 14px',
                                    'background': '#667eea',
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': '6px',
                                    'cursor': 'pointer',
                                    'fontSize': '12px',
                                    'fontWeight': '500'
                                }
                            )
                        ]
                    ),
                    html.Div(
                        id='data-table-container',
                        style={
                            'overflowX': 'auto',
                            'border': '1px solid #e2e8f0',
                            'borderRadius': '8px'
                        }
                    )
                ]
            ),
            
            # Stores
            dcc.Store(id='report-data-store'),
            dcc.Store(id='months-store'),
            dcc.Store(id='kpi-store'),
            
            # Font Awesome
            html.Link(
                rel='stylesheet',
                href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
            )
        ]
    )


def safe_convert(value):
    """Safely convert value to float"""
    if value is None or value == '-' or value == '':
        return 0.0
    try:
        if hasattr(value, 'strftime'):
            return 0.0
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def create_kpi_card(title, value, icon, color, trend):
    """Create a KPI card with colored top bar"""
    return html.Div(
        style={
            'background': 'white',
            'borderRadius': '12px',
            'border': '1px solid #e9ecef',
            'overflow': 'hidden'
        },
        children=[
            html.Div(style={'height': '4px', 'background': color}),
            html.Div(
                style={'padding': '20px'},
                children=[
                    html.Div(
                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'},
                        children=[
                            html.Div([
                                html.I(className=icon, style={'fontSize': '28px', 'color': color, 'marginBottom': '12px', 'display': 'inline-block'}),
                                html.Div(title, style={'fontSize': '12px', 'color': '#64748b', 'marginBottom': '8px', 'fontWeight': '500'}),
                                html.Div(value, style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'})
                            ]),
                            html.Div(
                                style={
                                    'background': '#f1f5f9',
                                    'padding': '4px 10px',
                                    'borderRadius': '20px',
                                    'fontSize': '11px',
                                    'fontWeight': '600',
                                    'color': color
                                },
                                children=f'▲ {trend}'
                            )
                        ]
                    )
                ]
            )
        ]
    )


def create_chart_card(title, chart_component, top_color):
    """Create a chart card with colored top bar (no icon)"""
    return html.Div(
        style={
            'background': 'white',
            'borderRadius': '12px',
            'border': '1px solid #e9ecef',
            'overflow': 'hidden'
        },
        children=[
            html.Div(style={'height': '4px', 'background': top_color}),
            html.Div(
                style={'padding': '16px'},
                children=[
                    html.Div(
                        style={
                            'marginBottom': '12px',
                            'paddingBottom': '8px',
                            'borderBottom': '1px solid #eef2f6'
                        },
                        children=[
                            html.H3(
                                title,
                                style={'margin': '0', 'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b'}
                            )
                        ]
                    ),
                    html.Div(chart_component, style={'minHeight': '300px'})
                ]
            )
        ]
    )


def create_bar_chart(x_data, y_data, color):
    """Create a compact bar chart"""
    if not y_data or all(v == 0 for v in y_data):
        return html.Div('No data available', style={'textAlign': 'center', 'padding': '60px 20px', 'color': '#94a3b8', 'fontSize': '12px'})
    
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker_color=color,
            marker_line_color='white',
            marker_line_width=1,
            text=[f'{v:,.0f}' for v in y_data],
            textposition='outside',
            textfont={'size': 9}
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=300,
        margin=dict(l=35, r=20, t=10, b=35),
        xaxis_title='Month',
        yaxis_title='Count',
        xaxis={'gridcolor': '#e2e8f0', 'showgrid': True, 'tickangle': -45, 'tickfont': {'size': 9}},
        yaxis={'gridcolor': '#e2e8f0', 'showgrid': True, 'tickfont': {'size': 9}},
        showlegend=False
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_line_chart(x_data, y_data, color):
    """Create a compact line chart"""
    if not y_data or all(v == 0 for v in y_data):
        return html.Div('No data available', style={'textAlign': 'center', 'padding': '60px 20px', 'color': '#94a3b8', 'fontSize': '12px'})
    
    fig = go.Figure(data=[
        go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines+markers',
            line=dict(color=color, width=2),
            marker=dict(size=6, color=color),
            text=[f'{v:,.0f}' for v in y_data],
            textposition='top center',
            textfont={'size': 9}
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=300,
        margin=dict(l=35, r=20, t=10, b=35),
        xaxis_title='Month',
        yaxis_title='Count',
        xaxis={'gridcolor': '#e2e8f0', 'showgrid': True, 'tickfont': {'size': 9}},
        yaxis={'gridcolor': '#e2e8f0', 'showgrid': True, 'tickfont': {'size': 9}},
        showlegend=False
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_grouped_bar_chart(x_data, y1_data, y2_data, label1, label2, color1, color2):
    """Create a compact grouped bar chart"""
    if not y1_data or not y2_data:
        return html.Div('No data available', style={'textAlign': 'center', 'padding': '60px 20px', 'color': '#94a3b8', 'fontSize': '12px'})
    
    fig = go.Figure(data=[
        go.Bar(name=label1, x=x_data, y=y1_data, marker_color=color1, 
               text=[f'{v:,.0f}' for v in y1_data], textposition='inside', textfont={'size': 9}),
        go.Bar(name=label2, x=x_data, y=y2_data, marker_color=color2, 
               text=[f'{v:,.0f}' for v in y2_data], textposition='inside', textfont={'size': 9})
    ])
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=300,
        margin=dict(l=35, r=20, t=10, b=50),
        xaxis={'gridcolor': '#e2e8f0', 'showgrid': True, 'tickangle': -45, 'tickfont': {'size': 9}},
        yaxis={'gridcolor': '#e2e8f0', 'showgrid': True, 'tickfont': {'size': 9}},
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1, 'font': {'size': 9}}
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def register_safety_dashboard_callbacks(app):
    """Register callbacks for safety dashboard"""
    
    @app.callback(
        [Output('report-data-store', 'data'),
         Output('months-store', 'data'),
         Output('kpi-store', 'data')],
        [Input('table-select-dropdown', 'value'),
         Input('year-filter-dropdown', 'value')]
    )
    def load_report_data(table_name, year):
        if not table_name:
            return None, None, None
        
        df, months = get_report_data(table_name)
        
        if df is not None and not df.empty:
            clean_months = []
            for m in months:
                if hasattr(m, 'strftime'):
                    clean_months.append(m.strftime('%b'))
                else:
                    month_str = str(m)
                    clean_months.append(month_str[:3] if len(month_str) > 3 else month_str)
            
            kpis = {'safe_manhours': 0, 'toolbox_talks': 0, 'ehs_trainings': 0}
            
            if 'items' in df.columns:
                for _, row in df.iterrows():
                    item = str(row['items']) if row['items'] else ''
                    
                    if 'manhour' in item.lower():
                        values = []
                        for m in months:
                            val = row.get(m, 0)
                            values.append(safe_convert(val))
                        kpis['safe_manhours'] = max(values) if values else 0
                    elif 'tool box' in item.lower():
                        total = 0
                        for m in months:
                            total += safe_convert(row.get(m, 0))
                        kpis['toolbox_talks'] = total
                    elif 'training' in item.lower() and 'ehs' in item.lower():
                        total = 0
                        for m in months:
                            total += safe_convert(row.get(m, 0))
                        kpis['ehs_trainings'] = total
            
            return df.to_dict('records'), clean_months, kpis
        return None, None, None
    
    @app.callback(
        Output('kpi-cards', 'children'),
        [Input('kpi-store', 'data')]
    )
    def update_kpi_cards(kpis):
        if not kpis or kpis.get('safe_manhours', 0) == 0:
            cards = html.Div(
                style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px'},
                children=[
                    create_kpi_card('Safe Manhours', '0', 'fas fa-shield-alt', '#64748b', '0%'),
                    create_kpi_card('Toolbox Talks', '0', 'fas fa-chalkboard', '#64748b', '0%'),
                    create_kpi_card('EHS Trainings', '0', 'fas fa-graduation-cap', '#64748b', '0%'),
                    create_kpi_card('Safety Score', '0/100', 'fas fa-star', '#64748b', '0%')
                ]
            )
            return cards
        
        cards = html.Div(
            style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px'},
            children=[
                create_kpi_card('Safe Manhours', f"{kpis.get('safe_manhours', 0):,.0f}", 'fas fa-shield-alt', '#10b981', '+12%'),
                create_kpi_card('Toolbox Talks', f"{kpis.get('toolbox_talks', 0):,}", 'fas fa-chalkboard', '#f59e0b', '+8%'),
                create_kpi_card('EHS Trainings', f"{kpis.get('ehs_trainings', 0):,}", 'fas fa-graduation-cap', '#8b5cf6', '+15%'),
                create_kpi_card('Safety Score', '94.5/100', 'fas fa-star', '#667eea', '+5%')
            ]
        )
        
        return cards
    
    @app.callback(
        [Output('chart-1', 'children'),
         Output('chart-2', 'children'),
         Output('chart-3', 'children'),
         Output('chart-4', 'children'),
         Output('chart-5', 'children'),
         Output('chart-6', 'children'),
         Output('chart-7', 'children'),
         Output('chart-8', 'children'),
         Output('chart-9', 'children'),
         Output('chart-10', 'children'),
         Output('chart-11', 'children'),
         Output('chart-12', 'children'),
         Output('chart-13', 'children'),
         Output('data-table-container', 'children')],
        [Input('report-data-store', 'data'),
         Input('months-store', 'data')]
    )
    def update_all_charts(data_records, months):
        if not data_records or not months:
            no_data_card = create_chart_card('No Data', html.Div('No data available', style={'textAlign': 'center', 'padding': '60px 20px', 'color': '#94a3b8', 'fontSize': '12px'}), '#64748b')
            return [no_data_card] * 14
        
        df = pd.DataFrame(data_records)
        items_list = df['items'].tolist() if 'items' in df.columns else []
        
        item_data = {}
        for _, row in df.iterrows():
            item = str(row['items']) if row['items'] else ''
            values = []
            for col in df.columns:
                if col not in ['items', 'id']:
                    if any(m in str(col) for m in months) or str(col) in months:
                        values.append(safe_convert(row.get(col, 0)))
            if values and len(values) == len(months):
                item_data[item] = values
        
        def get_values(keywords):
            for kw in keywords:
                matching = [i for i in items_list if kw in i.lower()]
                if matching and matching[0] in item_data:
                    return item_data[matching[0]]
            return [0] * len(months)
        
        # Chart 1 - Safe Manhours Trend (Green)
        chart1 = create_chart_card('Safe Manhours Trend', create_line_chart(months, get_values(['manhour']), '#10b981'), CARD_COLORS['green'])
        
        # Chart 2 - Toolbox Talk Trainings (Yellow)
        chart2 = create_chart_card('Toolbox Talk Trainings', create_bar_chart(months, get_values(['tool box']), '#f59e0b'), CARD_COLORS['yellow'])
        
        # Chart 3 - EHS Trainings Conducted (Purple)
        chart3 = create_chart_card('EHS Trainings Conducted', create_line_chart(months, get_values(['ehs training']), '#8b5cf6'), CARD_COLORS['purple'])
        
        # Chart 4 - Permits Issued (Blue)
        chart4 = create_chart_card('Permits Issued', create_bar_chart(months, get_values(['permit']), '#667eea'), CARD_COLORS['blue'])
        
        # Chart 5 - Contractor Workers (Red)
        chart5 = create_chart_card('Contractor Workers', create_bar_chart(months, get_values(['contractor']), '#ef4444'), CARD_COLORS['red'])
        
        # Chart 6 - Fire Accidents (Orange)
        chart6 = create_chart_card('Fire Accidents', create_bar_chart(months, get_values(['fire']), '#f97316'), CARD_COLORS['orange'])
        
        # Chart 7 - Unsafe Acts Analysis (Pink)
        chart7 = create_chart_card('Unsafe Acts Analysis', create_grouped_bar_chart(months, get_values(['unsafe acts reported']), get_values(['unsafe acts corrected']), 'Reported', 'Corrected', '#ef4444', '#10b981'), CARD_COLORS['pink'])
        
        # Chart 8 - Unsafe Conditions Analysis (Amber)
        chart8 = create_chart_card('Unsafe Conditions Analysis', create_grouped_bar_chart(months, get_values(['unsafe conditions reported']), get_values(['unsafe conditions corrected']), 'Reported', 'Corrected', '#f59e0b', '#10b981'), CARD_COLORS['amber'])
        
        # Chart 9 - Near Miss Reports (Teal)
        chart9 = create_chart_card('Near Miss Reports', create_line_chart(months, get_values(['near miss']), '#14b8a6'), CARD_COLORS['teal'])
        
        # Chart 10 - First Aid Cases (Cyan)
        chart10 = create_chart_card('First Aid Cases', create_bar_chart(months, get_values(['first aid']), '#06b6d4'), CARD_COLORS['cyan'])
        
        # Chart 11 - LTIR Rate (Indigo)
        chart11 = create_chart_card('LTIR Rate', create_line_chart(months, get_values(['ltir']), '#6366f1'), CARD_COLORS['indigo'])
        
        # Chart 12 - Induction Training (Violet)
        chart12 = create_chart_card('Induction Training', create_bar_chart(months, get_values(['induction']), '#7c3aed'), CARD_COLORS['violet'])
        
        # Chart 13 - Vendor Evaluations (Emerald)
        chart13 = create_chart_card('Vendor Evaluations', create_bar_chart(months, get_values(['vendor']), '#059669'), CARD_COLORS['emerald'])
        
        # Data Table
        if not df.empty:
            display_df = df.copy()
            for col in display_df.columns:
                if col not in ['items']:
                    display_df[col] = display_df[col].apply(safe_convert)
            
            table = html.Table(
                style={'width': '100%', 'borderCollapse': 'collapse'},
                children=[
                    html.Thead(
                        html.Tr([
                            html.Th(col, style={
                                'padding': '12px',
                                'border': '1px solid #e2e8f0',
                                'textAlign': 'left',
                                'fontSize': '12px',
                                'fontWeight': '700',
                                'background': '#f8fafc',
                                'position': 'sticky',
                                'top': 0
                            }) for col in display_df.columns
                        ])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(str(row[col]), style={
                                'padding': '10px',
                                'border': '1px solid #e2e8f0',
                                'fontSize': '12px',
                                'textAlign': 'left'
                            }) for col in display_df.columns
                        ]) for _, row in display_df.iterrows()
                    ])
                ]
            )
            
            data_table = html.Div([table], style={'overflowX': 'auto', 'maxHeight': '400px', 'overflowY': 'auto'})
        else:
            data_table = html.Div('No data available', style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'})
        
        return [chart1, chart2, chart3, chart4, chart5, chart6, chart7, chart8, chart9, chart10, chart11, chart12, chart13, data_table]