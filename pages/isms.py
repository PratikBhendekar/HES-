# pages/isms.py - ISMS Page with NRC Card

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def isms_page():
    """ISMS Page - Information Security Management System with NRC Card"""
    
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            # Header
            html.Div(
                style={'marginBottom': '24px'},
                children=[
                    html.H1(
                        "ISMS - Information Security Management System",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Information Security Management System",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # ========== NRC CARD ==========
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(1, 1fr)',
                    'gap': '20px',
                    'maxWidth': '600px'
                },
                children=[
                    # NRC Card - Clickable
                    html.Div(
                        id="nrc-card",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'padding': '30px',
                            'border': '1px solid #e9ecef',
                            'boxShadow': '0 2px 10px rgba(0,0,0,0.06)',
                            'borderLeft': '6px solid #667eea',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer'
                        },
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '16px',
                                    'marginBottom': '16px'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'width': '56px',
                                            'height': '56px',
                                            'background': '#eef2ff',
                                            'borderRadius': '14px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center'
                                        },
                                        children=html.I(
                                            className="fas fa-clipboard-check",
                                            style={'color': '#667eea', 'fontSize': '28px'}
                                        )
                                    ),
                                    html.H2(
                                        "NRC",
                                        style={
                                            'fontSize': '22px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'margin': 0
                                        }
                                    )
                                ]
                            ),
                            html.P(
                                "Audit Checklist - Track and monitor audit compliance items",
                                style={
                                    'fontSize': '14px',
                                    'color': '#64748b',
                                    'margin': '0 0 12px 0',
                                    'lineHeight': '1.6'
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'gap': '20px',
                                    'flexWrap': 'wrap',
                                    'paddingTop': '16px',
                                    'borderTop': '1px solid #f1f5f9'
                                },
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'},
                                        children=[
                                            html.Span("●", style={'color': '#10b981', 'fontSize': '12px'}),
                                            html.Span("Active", style={'fontSize': '13px', 'color': '#1e293b', 'fontWeight': '500'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'},
                                        children=[
                                            html.I(className="fas fa-arrow-right", style={'color': '#667eea', 'fontSize': '13px'}),
                                            html.Span("Click to view", style={'fontSize': '13px', 'color': '#64748b'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def register_isms_callbacks(app):
    """Register callbacks for ISMS page"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("nrc-card", "n_clicks"),
        prevent_initial_call=True
    )
    def navigate_to_nrc(n_clicks):
        if n_clicks and n_clicks > 0:
            return "/nrc"
        return no_update