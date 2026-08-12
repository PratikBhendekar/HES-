# pages/ehs_dashboard.py - EHS Dashboard Page with Three Stories

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def ehs_dashboard_page():
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
                        "EHS Dashboard",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Environment, Health & Safety Management",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # 8 Cards - 2 rows of 4
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '20px',
                    'marginBottom': '24px'
                },
                children=[
                    # Card 1 - Safety Dashboard (Green)
                    html.Div(
                        id="card-safety-dashboard",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#10b981'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#ecfdf5',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-chart-line", style={'color': '#10b981', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Safety Dashboard",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "EHS Dashboard →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 2 - Reports & Analytics (Blue)
                    html.Div(
                        id="card-reports",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#3b82f6'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#dbeafe',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-file-alt", style={'color': '#3b82f6', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Reports & Analytics",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "View All Reports →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 3 - Project Safety (Orange)
                    html.Div(
                        id="card-project-safety",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#f59e0b'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#fef3c7',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-hard-hat", style={'color': '#f59e0b', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Project Safety",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "Safety Monitoring →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 4 - Training Matrix (Purple)
                    html.Div(
                        id="card-training",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#8b5cf6'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#ede9fe',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-graduation-cap", style={'color': '#8b5cf6', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Training Matrix",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "Management Matrix →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 5 - Permit Management (Cyan)
                    html.Div(
                        id="card-work-permit",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#06b6d4'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#cffafe',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-clipboard-list", style={'color': '#06b6d4', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Permit Management",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "Work Permit →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 6 - Risk Management (Red)
                    html.Div(
                        id="card-risk-assessment",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#ef4444'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#fee2e2',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-exclamation-triangle", style={'color': '#ef4444', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Risk Management",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "Risk Assessment →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 7 - Incident Management (Pink)
                    html.Div(
                        id="card-incident",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#ec4899'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#fce7f3',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-bell", style={'color': '#ec4899', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Incident Management",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "Incident Alert →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 8 - Contractor Management (Indigo)
                    html.Div(
                        id="card-contractor",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#6366f1'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '16px'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '48px',
                                                    'height': '48px',
                                                    'background': '#e0e7ff',
                                                    'borderRadius': '12px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(className="fas fa-handshake", style={'color': '#6366f1', 'fontSize': '22px'})
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '14px'})
                                        ]
                                    ),
                                    html.Div([
                                        html.Div(
                                            "Contractor Management",
                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '6px'}
                                        ),
                                        html.Div(
                                            "Performance Monitoring →",
                                            style={'fontSize': '12px', 'color': '#64748b'}
                                        )
                                    ])
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Annual EHS Plan Card (Full Width)
            html.Div(
                style={
                    'marginBottom': '24px'
                },
                children=[
                    html.Div(
                        id="card-annual-plan",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#667eea'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '15px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '48px',
                                                            'height': '48px',
                                                            'background': '#eef2ff',
                                                            'borderRadius': '12px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center'
                                                        },
                                                        children=html.I(className="fas fa-calendar-alt", style={'color': '#667eea', 'fontSize': '22px'})
                                                    ),
                                                    html.Div([
                                                        html.Div(
                                                            "Annual EHS Activity Plan",
                                                            style={'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '4px'}
                                                        ),
                                                        html.Div(
                                                            "2026-2027 | View Plan",
                                                            style={'fontSize': '13px', 'color': '#64748b'}
                                                        )
                                                    ])
                                                ]
                                            ),
                                            html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '18px'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== STORY 1: TREE PLANTATION (TOP - GREEN) - 4 PHOTOS ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '24px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#065f46'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "World Environment Day 2026 - Tree Plantation at Head Office, Nagpur",
                                style={
                                    'fontSize': '20px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '4px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.P("05 June 2026", style={'fontSize': '14px', 'color': '#64748b', 'marginBottom': '16px'}),
                            
                            html.Div(
                                style={'lineHeight': '1.8', 'color': '#475569', 'fontSize': '14px', 'marginBottom': '20px'},
                                children=[
                                    html.P(
                                        "On 5th June 2026, the EHS team at Head Office, Nagpur, celebrated World Environment Day with great enthusiasm. The day began with a powerful message about environmental conservation and the importance of tree plantation.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "More than 50 trees of various species were planted across the campus. The event saw active participation from over 100 employees, including senior management. Each participant pledged to nurture the planted trees and contribute to a greener tomorrow.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "The initiative was part of our ongoing commitment to environmental sustainability and aligns with our IMS policy. The tree plantation drive not only beautified the campus but also contributed to reducing carbon footprint.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "We thank all participants for making this event a grand success. Together, we are creating a sustainable future.",
                                        style={'fontWeight': '600', 'color': '#065f46', 'marginBottom': '0'}
                                    )
                                ]
                            ),
                            
                            html.Hr(style={'border': '1px solid #eef2f6', 'margin': '0 0 20px 0'}),
                            
                            html.Div(
                                style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '16px'},
                                children=[
                                    html.I(className="fas fa-images", style={'color': '#065f46', 'fontSize': '18px'}),
                                    html.H4("Event Photos", style={'margin': '0', 'fontSize': '16px', 'fontWeight': '600', 'color': '#1e293b'})
                                ]
                            ),
                            
                            # 4 PHOTOS IN 2x2 GRID
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(2, 1fr)',
                                    'gap': '16px'
                                },
                                children=[
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0599.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Tree Plantation Ceremony", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0613.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Team Participation", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0609.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Plantation Drive", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0606.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Green Initiative", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== STORY 2: FIRST AID TRAINING (MIDDLE - RED) - 4 PHOTOS ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '24px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#dc2626'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "First Aid Training for ERT Team Members at Head Office, Nagpur",
                                style={
                                    'fontSize': '20px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '4px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.P("06 June 2026", style={'fontSize': '14px', 'color': '#64748b', 'marginBottom': '16px'}),
                            
                            html.Div(
                                style={'lineHeight': '1.8', 'color': '#475569', 'fontSize': '14px', 'marginBottom': '20px'},
                                children=[
                                    html.P(
                                        "On 6th June 2026, the EHS department organized a comprehensive First Aid Training program for the Emergency Response Team (ERT) members at the Head Office, Nagpur. The training was conducted to enhance the emergency response capabilities of the ERT team.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "The training covered essential first aid techniques including CPR, wound dressing, fracture management, and handling medical emergencies. Participants received hands-on practice sessions with medical equipment and learned how to respond effectively in emergency situations.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "More than 25 ERT team members actively participated in the training program. The session was led by certified medical trainers who shared practical knowledge and real-life case studies. The team members demonstrated great enthusiasm and commitment to learning life-saving skills.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "This initiative is part of our ongoing commitment to workplace safety and aligns with our IMS policy. We thank all participants and trainers for making this training a success.",
                                        style={'fontWeight': '600', 'color': '#dc2626', 'marginBottom': '0'}
                                    )
                                ]
                            ),
                            
                            html.Hr(style={'border': '1px solid #eef2f6', 'margin': '0 0 20px 0'}),
                            
                            html.Div(
                                style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '16px'},
                                children=[
                                    html.I(className="fas fa-images", style={'color': '#dc2626', 'fontSize': '18px'}),
                                    html.H4("Training Photos", style={'margin': '0', 'fontSize': '16px', 'fontWeight': '600', 'color': '#1e293b'})
                                ]
                            ),
                            
                            # 4 PHOTOS IN 2x2 GRID
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(2, 1fr)',
                                    'gap': '16px'
                                },
                                children=[
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0549.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("First Aid Training Session", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0555.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("ERT Team Participation", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0573.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Hands-on Practice", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0574.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Training Demonstration", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== STORY 3: MEDICAL HEALTH CHECKUP CAMP (BOTTOM - BLUE) - 8 PHOTOS ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '24px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#3b82f6'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Medical Health Checkup Camp at Head Office, Nagpur",
                                style={
                                    'fontSize': '20px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '4px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.P("05 June 2026", style={'fontSize': '14px', 'color': '#64748b', 'marginBottom': '16px'}),
                            
                            html.Div(
                                style={'lineHeight': '1.8', 'color': '#475569', 'fontSize': '14px', 'marginBottom': '20px'},
                                children=[
                                    html.P(
                                        "On 5th June 2026, the EHS department organized a Medical Health Checkup Camp at Head Office, Nagpur. The camp was organized to promote employee wellness and ensure the overall health and well-being of all employees.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "The health checkup camp provided comprehensive medical screenings including blood pressure check, blood sugar testing, BMI analysis, eye checkup, and general health consultation. More than 150 employees participated in the camp and availed the health screening services.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "A team of qualified doctors and medical professionals conducted the checkups and provided health advice to the employees. The camp also included health awareness sessions on topics like stress management, healthy lifestyle, and prevention of lifestyle diseases.",
                                        style={'marginBottom': '10px'}
                                    ),
                                    html.P(
                                        "The initiative was highly appreciated by the employees and is part of our ongoing commitment to employee health and wellness. We thank all participants and the medical team for making this camp a grand success.",
                                        style={'fontWeight': '600', 'color': '#3b82f6', 'marginBottom': '0'}
                                    )
                                ]
                            ),
                            
                            html.Hr(style={'border': '1px solid #eef2f6', 'margin': '0 0 20px 0'}),
                            
                            html.Div(
                                style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '16px'},
                                children=[
                                    html.I(className="fas fa-images", style={'color': '#3b82f6', 'fontSize': '18px'}),
                                    html.H4("Camp Photos", style={'margin': '0', 'fontSize': '16px', 'fontWeight': '600', 'color': '#1e293b'})
                                ]
                            ),
                            
                            # 8 PHOTOS IN 2x2 GRID (4 rows of 2) - SAME SIZE AS OTHERS
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(2, 1fr)',
                                    'gap': '16px'
                                },
                                children=[
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0576.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Health Checkup Camp", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0516.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Blood Pressure Check", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0519.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Medical Consultation", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0522.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Employee Participation", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0549.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Health Screening", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0555.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Medical Team", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0573.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Employee Registration", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'borderRadius': '10px', 'overflow': 'hidden', 'border': '1px solid #e2e8f0', 'background': '#f8fafc'},
                                        children=[
                                            html.Img(src="/assets/IMG_0574.JPG", style={'width': '100%', 'height': 'auto', 'aspectRatio': '16/9', 'objectFit': 'cover', 'display': 'block'}),
                                            html.Div("Health Awareness Session", style={'padding': '8px 12px', 'background': '#f8fafc', 'fontSize': '12px', 'fontWeight': '500', 'color': '#1e293b', 'textAlign': 'center'})
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


def register_ehs_dashboard_callbacks(app):
    """Register callbacks for EHS dashboard navigation"""
    
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