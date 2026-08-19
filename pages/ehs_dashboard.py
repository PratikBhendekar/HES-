# pages/ehs_dashboard.py - EHS Dashboard with Advanced Gradient & Modern Design

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc

def ehs_dashboard_page():
    return html.Div(
        style={
            'padding': '0',
            'background': 'linear-gradient(135deg, #f0f4ff 0%, #e8edf5 50%, #dce3ef 100%)',
            'minHeight': '100vh'
        },
        children=[
            # ==================== HEADER ====================
            html.Div(
                style={
                    'background': 'rgba(255, 255, 255, 0.85)',
                    'backdropFilter': 'blur(20px)',
                    'padding': '0 30px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'space-between',
                    'height': '90px',
                    'boxShadow': '0 4px 30px rgba(0,0,0,0.05)',
                    'margin': '0 0 4px 0',
                    'borderBottom': '1px solid rgba(255,255,255,0.3)'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'},
                        children=[
                            html.Div(
                                style={
                                    'width': '44px',
                                    'height': '44px',
                                    'background': 'linear-gradient(135deg, #667eea, #764ba2)',
                                    'borderRadius': '12px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center',
                                    'boxShadow': '0 4px 15px rgba(102,126,234,0.3)'
                                },
                                children=html.I(
                                    className="fas fa-shield-alt",
                                    style={'color': '#ffffff', 'fontSize': '20px'}
                                )
                            ),
                            html.Div(
                                style={
                                    'fontSize': '22px',
                                    'fontWeight': '700',
                                    'color': '#1a2332',
                                    'fontFamily': "'Inter', 'Segoe UI', sans-serif",
                                    'letterSpacing': '-0.3px',
                                    'background': 'linear-gradient(135deg, #1a3a6a, #667eea)',
                                    '-webkit-background-clip': 'text',
                                    '-webkit-text-fill-color': 'transparent'
                                },
                                children="Welcome to EHS"
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'alignItems': 'center', 'height': '90px', 'padding': '0'},
                        children=[
                            html.Img(
                                src="/assets/ChatGPT Image Aug 18, 2026, 10_01_00 AM.png",
                                style={
                                    'height': '90px',
                                    'width': 'auto',
                                    'objectFit': 'contain',
                                    'maxHeight': '90px',
                                    'borderRadius': '0',
                                    'border': 'none',
                                    'padding': '0',
                                    'background': 'transparent',
                                    'display': 'block'
                                }
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== MAIN CONTENT ====================
            html.Div(
                style={'padding': '20px 30px'},
                children=[
                    # ==================== RAISE A TICKET - MAIN CARD ====================
                    html.Div(
                        id="raise-ticket-main-card",
                        style={
                            'background': 'linear-gradient(135deg, #ffffff, #f8faff)',
                            'borderRadius': '16px',
                            'border': '1px solid rgba(255,255,255,0.6)',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                            'marginBottom': '24px',
                            'boxShadow': '0 8px 32px rgba(0,0,0,0.06)',
                            'backdropFilter': 'blur(10px)'
                        },
                        children=[
                            # Top Bar
                            html.Div(
                                style={'height': '4px', 'background': 'linear-gradient(90deg, #1a3a6a, #667eea, #764ba2)'}
                            ),
                            html.Div(
                                style={'padding': '16px 20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #eef2ff, #e0e7ff)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(102,126,234,0.1)'
                                                        },
                                                        children=html.I(
                                                            className="fas fa-ticket-alt",
                                                            style={'color': '#1a3a6a', 'fontSize': '18px'}
                                                        )
                                                    ),
                                                    html.Div([
                                                        html.Div(
                                                            "Raise a Ticket",
                                                            style={
                                                                'fontSize': '15px',
                                                                'fontWeight': '700',
                                                                'color': '#1a2332',
                                                                'background': 'linear-gradient(135deg, #1a3a6a, #667eea)',
                                                                '-webkit-background-clip': 'text',
                                                                '-webkit-text-fill-color': 'transparent'
                                                            }
                                                        ),
                                                        html.Div(
                                                            "EHS Tickets",
                                                            style={
                                                                'fontSize': '12px',
                                                                'color': '#94a3b8'
                                                            }
                                                        )
                                                    ])
                                                ]
                                            ),
                                            html.I(
                                                id="raise-ticket-arrow",
                                                className="fas fa-chevron-down",
                                                style={
                                                    'color': '#667eea',
                                                    'fontSize': '14px',
                                                    'transition': 'transform 0.4s ease',
                                                    'background': 'rgba(102,126,234,0.08)',
                                                    'padding': '8px',
                                                    'borderRadius': '50%'
                                                }
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # ==================== 4 TICKET CARDS ====================
                            html.Div(
                                id="ticket-cards-container",
                                style={
                                    'display': 'none',
                                    'padding': '0 20px 20px 20px',
                                    'gridTemplateColumns': 'repeat(4, 1fr)',
                                    'gap': '16px'
                                },
                                children=[
                                    # Ticket 1: Safety Observation
                                    html.Div(
                                        id="card-safety-ticket",
                                        style={
                                            'background': 'linear-gradient(135deg, #ffffff, #f0fdf4)',
                                            'borderRadius': '14px',
                                            'border': '1px solid rgba(16,185,129,0.2)',
                                            'overflow': 'hidden',
                                            'cursor': 'pointer',
                                            'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                            'boxShadow': '0 2px 12px rgba(0,0,0,0.04)'
                                        },
                                        children=[
                                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #10b981, #34d399)'}),
                                            html.Div(
                                                style={'padding': '16px 18px'},
                                                children=[
                                                    html.Div(
                                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                        children=[
                                                            html.Div(
                                                                style={
                                                                    'width': '44px',
                                                                    'height': '44px',
                                                                    'background': 'linear-gradient(135deg, #ecfdf5, #d1fae5)',
                                                                    'borderRadius': '12px',
                                                                    'display': 'flex',
                                                                    'alignItems': 'center',
                                                                    'justifyContent': 'center',
                                                                    'boxShadow': '0 2px 10px rgba(16,185,129,0.15)'
                                                                },
                                                                children=html.I(
                                                                    className="fas fa-shield-alt",
                                                                    style={'color': '#10b981', 'fontSize': '18px'}
                                                                )
                                                            ),
                                                            html.I(
                                                                className="fas fa-chevron-right",
                                                                style={'color': '#10b981', 'fontSize': '12px', 'opacity': '0.5'}
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        "Safety Observation",
                                                        style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                                    ),
                                                    html.Div(
                                                        "Report safety observations",
                                                        style={'fontSize': '12px', 'color': '#94a3b8'}
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    
                                    # Ticket 2: New Joiner Training
                                    html.Div(
                                        id="card-joiner-ticket",
                                        style={
                                            'background': 'linear-gradient(135deg, #ffffff, #eff6ff)',
                                            'borderRadius': '14px',
                                            'border': '1px solid rgba(59,130,246,0.2)',
                                            'overflow': 'hidden',
                                            'cursor': 'pointer',
                                            'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                            'boxShadow': '0 2px 12px rgba(0,0,0,0.04)'
                                        },
                                        children=[
                                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #3b82f6, #60a5fa)'}),
                                            html.Div(
                                                style={'padding': '16px 18px'},
                                                children=[
                                                    html.Div(
                                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                        children=[
                                                            html.Div(
                                                                style={
                                                                    'width': '44px',
                                                                    'height': '44px',
                                                                    'background': 'linear-gradient(135deg, #dbeafe, #bfdbfe)',
                                                                    'borderRadius': '12px',
                                                                    'display': 'flex',
                                                                    'alignItems': 'center',
                                                                    'justifyContent': 'center',
                                                                    'boxShadow': '0 2px 10px rgba(59,130,246,0.15)'
                                                                },
                                                                children=html.I(
                                                                    className="fas fa-user-graduate",
                                                                    style={'color': '#3b82f6', 'fontSize': '18px'}
                                                                )
                                                            ),
                                                            html.I(
                                                                className="fas fa-chevron-right",
                                                                style={'color': '#3b82f6', 'fontSize': '12px', 'opacity': '0.5'}
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        "New Joiner Training",
                                                        style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                                    ),
                                                    html.Div(
                                                        "Safety induction request",
                                                        style={'fontSize': '12px', 'color': '#94a3b8'}
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    
                                    # Ticket 3: Vendor Orientation
                                    html.Div(
                                        id="card-vendor-ticket",
                                        style={
                                            'background': 'linear-gradient(135deg, #ffffff, #fffbeb)',
                                            'borderRadius': '14px',
                                            'border': '1px solid rgba(245,158,11,0.2)',
                                            'overflow': 'hidden',
                                            'cursor': 'pointer',
                                            'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                            'boxShadow': '0 2px 12px rgba(0,0,0,0.04)'
                                        },
                                        children=[
                                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #f59e0b, #fbbf24)'}),
                                            html.Div(
                                                style={'padding': '16px 18px'},
                                                children=[
                                                    html.Div(
                                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                        children=[
                                                            html.Div(
                                                                style={
                                                                    'width': '44px',
                                                                    'height': '44px',
                                                                    'background': 'linear-gradient(135deg, #fef3c7, #fde68a)',
                                                                    'borderRadius': '12px',
                                                                    'display': 'flex',
                                                                    'alignItems': 'center',
                                                                    'justifyContent': 'center',
                                                                    'boxShadow': '0 2px 10px rgba(245,158,11,0.15)'
                                                                },
                                                                children=html.I(
                                                                    className="fas fa-handshake",
                                                                    style={'color': '#f59e0b', 'fontSize': '18px'}
                                                                )
                                                            ),
                                                            html.I(
                                                                className="fas fa-chevron-right",
                                                                style={'color': '#f59e0b', 'fontSize': '12px', 'opacity': '0.5'}
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        "Vendor Orientation",
                                                        style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                                    ),
                                                    html.Div(
                                                        "EHS orientation request",
                                                        style={'fontSize': '12px', 'color': '#94a3b8'}
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    
                                    # Ticket 4: Incident Report
                                    html.Div(
                                        id="card-incident-ticket",
                                        style={
                                            'background': 'linear-gradient(135deg, #ffffff, #fef2f2)',
                                            'borderRadius': '14px',
                                            'border': '1px solid rgba(239,68,68,0.2)',
                                            'overflow': 'hidden',
                                            'cursor': 'pointer',
                                            'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                            'boxShadow': '0 2px 12px rgba(0,0,0,0.04)'
                                        },
                                        children=[
                                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #ef4444, #f87171)'}),
                                            html.Div(
                                                style={'padding': '16px 18px'},
                                                children=[
                                                    html.Div(
                                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                        children=[
                                                            html.Div(
                                                                style={
                                                                    'width': '44px',
                                                                    'height': '44px',
                                                                    'background': 'linear-gradient(135deg, #fee2e2, #fecaca)',
                                                                    'borderRadius': '12px',
                                                                    'display': 'flex',
                                                                    'alignItems': 'center',
                                                                    'justifyContent': 'center',
                                                                    'boxShadow': '0 2px 10px rgba(239,68,68,0.15)'
                                                                },
                                                                children=html.I(
                                                                    className="fas fa-exclamation-triangle",
                                                                    style={'color': '#ef4444', 'fontSize': '18px'}
                                                                )
                                                            ),
                                                            html.I(
                                                                className="fas fa-chevron-right",
                                                                style={'color': '#ef4444', 'fontSize': '12px', 'opacity': '0.5'}
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        "Incident Report",
                                                        style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                                    ),
                                                    html.Div(
                                                        "Report incidents",
                                                        style={'fontSize': '12px', 'color': '#94a3b8'}
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # ==================== 8 EHS CARDS ====================
                    html.Div(
                        style={
                            'display': 'grid',
                            'gridTemplateColumns': 'repeat(4, 1fr)',
                            'gap': '16px',
                            'marginBottom': '24px'
                        },
                        children=[
                            # Card 1 - Safety Dashboard
                            html.Div(
                                id="card-safety-dashboard",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #f0fdf4)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(16,185,129,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #10b981, #34d399)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #ecfdf5, #d1fae5)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(16,185,129,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-chart-line", style={'color': '#10b981', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#10b981', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Safety Dashboard",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "EHS Dashboard",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 2 - Reports & Analytics
                            html.Div(
                                id="card-reports",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #eff6ff)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(59,130,246,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #3b82f6, #60a5fa)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #dbeafe, #bfdbfe)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(59,130,246,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-file-alt", style={'color': '#3b82f6', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#3b82f6', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Reports & Analytics",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "View All Reports",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 3 - Project Safety
                            html.Div(
                                id="card-project-safety",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #fffbeb)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(245,158,11,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #f59e0b, #fbbf24)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #fef3c7, #fde68a)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(245,158,11,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-hard-hat", style={'color': '#f59e0b', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#f59e0b', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Project Safety",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "Safety Monitoring",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 4 - Training Matrix
                            html.Div(
                                id="card-training",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #f5f3ff)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(139,92,246,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #8b5cf6, #a78bfa)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #ede9fe, #ddd6fe)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(139,92,246,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-graduation-cap", style={'color': '#8b5cf6', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#8b5cf6', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Training Matrix",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "Management Matrix",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 5 - Permit Management
                            html.Div(
                                id="card-work-permit",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #ecfeff)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(6,182,212,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #06b6d4, #22d3ee)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #cffafe, #a5f3fc)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(6,182,212,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-clipboard-list", style={'color': '#06b6d4', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#06b6d4', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Permit Management",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "Work Permit",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 6 - Risk Management
                            html.Div(
                                id="card-risk-assessment",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #fef2f2)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(239,68,68,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #ef4444, #f87171)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #fee2e2, #fecaca)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(239,68,68,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-exclamation-triangle", style={'color': '#ef4444', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#ef4444', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Risk Management",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "Risk Assessment",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 7 - Incident Management
                            html.Div(
                                id="card-incident",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #fdf2f8)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(236,72,153,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #ec4899, #f472b6)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #fce7f3, #fbcfe8)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(236,72,153,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-bell", style={'color': '#ec4899', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#ec4899', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Incident Management",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "Incident Alert",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Card 8 - Contractor Management
                            html.Div(
                                id="card-contractor",
                                style={
                                    'background': 'linear-gradient(135deg, #ffffff, #eef2ff)',
                                    'borderRadius': '14px',
                                    'border': '1px solid rgba(99,102,241,0.15)',
                                    'overflow': 'hidden',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                    'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                                },
                                children=[
                                    html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #6366f1, #818cf8)'}),
                                    html.Div(
                                        style={'padding': '16px 18px'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '10px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #e0e7ff, #c7d2fe)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(99,102,241,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-handshake", style={'color': '#6366f1', 'fontSize': '18px'})
                                                    ),
                                                    html.I(className="fas fa-chevron-right", style={'color': '#6366f1', 'fontSize': '12px', 'opacity': '0.5'})
                                                ]
                                            ),
                                            html.Div(
                                                "Contractor Management",
                                                style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1a2332', 'marginBottom': '2px'}
                                            ),
                                            html.Div(
                                                "Performance Monitoring",
                                                style={'fontSize': '12px', 'color': '#94a3b8'}
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # ==================== ANNUAL EHS PLAN CARD ====================
                    html.Div(
                        id="card-annual-plan",
                        style={
                            'background': 'linear-gradient(135deg, #ffffff, #eef2ff)',
                            'borderRadius': '14px',
                            'border': '1px solid rgba(102,126,234,0.2)',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                            'marginBottom': '24px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #667eea, #764ba2)'}),
                            html.Div(
                                style={'padding': '16px 20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '44px',
                                                            'height': '44px',
                                                            'background': 'linear-gradient(135deg, #eef2ff, #e0e7ff)',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center',
                                                            'boxShadow': '0 2px 10px rgba(102,126,234,0.15)'
                                                        },
                                                        children=html.I(className="fas fa-calendar-alt", style={'color': '#667eea', 'fontSize': '18px'})
                                                    ),
                                                    html.Div([
                                                        html.Div(
                                                            "Annual EHS Activity Plan",
                                                            style={
                                                                'fontSize': '14px',
                                                                'fontWeight': '600',
                                                                'color': '#1a2332'
                                                            }
                                                        ),
                                                        html.Div(
                                                            "2026-2027",
                                                            style={
                                                                'fontSize': '12px',
                                                                'color': '#94a3b8'
                                                            }
                                                        )
                                                    ])
                                                ]
                                            ),
                                            html.I(
                                                className="fas fa-chevron-right",
                                                style={'color': '#667eea', 'fontSize': '14px', 'opacity': '0.5'}
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # ==================== THREE STORIES ====================
                    # Story 1: Tree Plantation
                    html.Div(
                        style={
                            'background': 'linear-gradient(135deg, #ffffff, #f0fdf4)',
                            'borderRadius': '14px',
                            'border': '1px solid rgba(6,95,70,0.1)',
                            'overflow': 'hidden',
                            'marginBottom': '20px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #065f46, #34d399)'}),
                            html.Div(
                                style={'padding': '20px 24px'},
                                children=[
                                    html.Div(
                                        "World Environment Day 2026 - Tree Plantation at Head Office, Nagpur",
                                        style={
                                            'fontSize': '18px',
                                            'fontWeight': '600',
                                            'color': '#1a2332',
                                            'marginBottom': '4px'
                                        }
                                    ),
                                    html.Div("05 June 2026", style={'fontSize': '13px', 'color': '#94a3b8', 'marginBottom': '12px'}),
                                    html.Div(
                                        style={'fontSize': '13px', 'color': '#475569', 'lineHeight': '1.6', 'marginBottom': '16px'},
                                        children=[
                                            "On 5th June 2026, the EHS team at Head Office, Nagpur, celebrated World Environment Day with great enthusiasm. More than 50 trees were planted across the campus with participation from over 100 employees."
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'grid',
                                            'gridTemplateColumns': 'repeat(4, 1fr)',
                                            'gap': '12px'
                                        },
                                        children=[
                                            html.Img(src="/assets/IMG_0599.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0613.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0609.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0606.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Story 2: First Aid Training
                    html.Div(
                        style={
                            'background': 'linear-gradient(135deg, #ffffff, #fef2f2)',
                            'borderRadius': '14px',
                            'border': '1px solid rgba(220,38,38,0.1)',
                            'overflow': 'hidden',
                            'marginBottom': '20px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #dc2626, #f87171)'}),
                            html.Div(
                                style={'padding': '20px 24px'},
                                children=[
                                    html.Div(
                                        "First Aid Training for ERT Team Members at Head Office, Nagpur",
                                        style={
                                            'fontSize': '18px',
                                            'fontWeight': '600',
                                            'color': '#1a2332',
                                            'marginBottom': '4px'
                                        }
                                    ),
                                    html.Div("06 June 2026", style={'fontSize': '13px', 'color': '#94a3b8', 'marginBottom': '12px'}),
                                    html.Div(
                                        style={'fontSize': '13px', 'color': '#475569', 'lineHeight': '1.6', 'marginBottom': '16px'},
                                        children=[
                                            "On 6th June 2026, the EHS department organized a comprehensive First Aid Training program for the Emergency Response Team (ERT) members. More than 25 team members participated in the training."
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'grid',
                                            'gridTemplateColumns': 'repeat(4, 1fr)',
                                            'gap': '12px'
                                        },
                                        children=[
                                            html.Img(src="/assets/IMG_0549.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0555.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0573.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0574.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Story 3: Medical Health Checkup
                    html.Div(
                        style={
                            'background': 'linear-gradient(135deg, #ffffff, #eff6ff)',
                            'borderRadius': '14px',
                            'border': '1px solid rgba(59,130,246,0.1)',
                            'overflow': 'hidden',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': 'linear-gradient(90deg, #3b82f6, #60a5fa)'}),
                            html.Div(
                                style={'padding': '20px 24px'},
                                children=[
                                    html.Div(
                                        "Medical Health Checkup Camp at Head Office, Nagpur",
                                        style={
                                            'fontSize': '18px',
                                            'fontWeight': '600',
                                            'color': '#1a2332',
                                            'marginBottom': '4px'
                                        }
                                    ),
                                    html.Div("05 June 2026", style={'fontSize': '13px', 'color': '#94a3b8', 'marginBottom': '12px'}),
                                    html.Div(
                                        style={'fontSize': '13px', 'color': '#475569', 'lineHeight': '1.6', 'marginBottom': '16px'},
                                        children=[
                                            "On 5th June 2026, the EHS department organized a Medical Health Checkup Camp at Head Office. More than 150 employees participated in the health screening services."
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'grid',
                                            'gridTemplateColumns': 'repeat(4, 1fr)',
                                            'gap': '12px'
                                        },
                                        children=[
                                            html.Img(src="/assets/IMG_0576.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0516.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0519.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'}),
                                            html.Img(src="/assets/IMG_0522.JPG", style={'width': '100%', 'aspectRatio': '16/10', 'objectFit': 'cover', 'borderRadius': '8px', 'border': '1px solid #e8ecf1'})
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


# ==================== CALLBACKS ====================
def register_ehs_dashboard_callbacks(app):
    """Register callbacks for EHS dashboard navigation and ticket toggle"""
    
    # ==================== TOGGLE TICKET CARDS ====================
    @app.callback(
        [Output("ticket-cards-container", "style"),
         Output("raise-ticket-arrow", "className")],
        [Input("raise-ticket-main-card", "n_clicks")],
        [State("ticket-cards-container", "style")]
    )
    def toggle_ticket_cards(n_clicks, current_style):
        if n_clicks and n_clicks > 0:
            if current_style and current_style.get('display') == 'grid':
                return {'display': 'none'}, "fas fa-chevron-down"
            else:
                return {
                    'display': 'grid',
                    'padding': '0 20px 20px 20px',
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '16px'
                }, "fas fa-chevron-up"
        return {'display': 'none'}, "fas fa-chevron-down"
    
    # ==================== TICKET CARD NAVIGATION ====================
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("card-safety-ticket", "n_clicks"),
         Input("card-joiner-ticket", "n_clicks"),
         Input("card-vendor-ticket", "n_clicks"),
         Input("card-incident-ticket", "n_clicks")],
        prevent_initial_call=True
    )
    def navigate_ticket_cards(safety, joiner, vendor, incident):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        nav_map = {
            "card-safety-ticket": "/ticket-safety-observation",
            "card-joiner-ticket": "/ticket-new-joiner",
            "card-vendor-ticket": "/ticket-vendor-orientation",
            "card-incident-ticket": "/ticket-incident-report"
        }
        
        if button_id in nav_map:
            return nav_map[button_id]
        
        return no_update
    
    # ==================== EHS CARD NAVIGATION ====================
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("card-safety-dashboard", "n_clicks"),
         Input("card-reports", "n_clicks"),
         Input("card-project-safety", "n_clicks"),
         Input("card-training", "n_clicks"),
         Input("card-work-permit", "n_clicks"),
         Input("card-risk-assessment", "n_clicks"),
         Input("card-incident", "n_clicks"),
         Input("card-contractor", "n_clicks"),
         Input("card-annual-plan", "n_clicks")],
        prevent_initial_call=True
    )
    def navigate_ehs_cards(safety, reports, project, training, work_permit, risk, incident, contractor, annual_plan):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        nav_map = {
            "card-safety-dashboard": "/ehs-safety-dashboard",
            "card-reports": "/ehs-reports",
            "card-project-safety": "/ehs-project-safety",
            "card-training": "/ehs-training-matrix",
            "card-work-permit": "/work-permit",
            "card-risk-assessment": "/ehs-risk-assessment",
            "card-incident": "/incident-management",
            "card-contractor": "/ehs-contractor",
            "card-annual-plan": "/annual-ehs-plan"
        }
        
        if button_id in nav_map:
            return nav_map[button_id]
        
        return no_update
