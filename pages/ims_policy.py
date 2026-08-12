# pages/ims_policy.py - IMS Policy Page

from dash import html, dcc

def ims_policy_page():
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
                        "IMS Policy",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Integrated Management System Policy Document",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # PDF Viewer Card
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'
                },
                children=[
                    # Card Header
                    html.Div(
                        style={
                            'padding': '16px 20px',
                            'borderBottom': '1px solid #eef2f6',
                            'background': '#fafbff'
                        },
                        children=[
                            html.Div(
                                style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'},
                                children=[
                                    html.I(
                                        className="fas fa-file-pdf",
                                        style={'color': '#dc2626', 'fontSize': '18px'}
                                    ),
                                    html.H3(
                                        "IMS Policy Document",
                                        style={
                                            'margin': 0,
                                            'fontSize': '16px',
                                            'fontWeight': '700',
                                            'color': '#1e293b'
                                        }
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # PDF Viewer Container
                    html.Div(
                        style={
                            'padding': '20px',
                            'background': '#f8fafc'
                        },
                        children=[
                            html.Iframe(
                                src="/assets/IMS Policy Eng.pdf",
                                style={
                                    "width": "100%",
                                    "height": "75vh",
                                    "border": "1px solid #e2e8f0",
                                    "borderRadius": "12px",
                                    "background": "white"
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )