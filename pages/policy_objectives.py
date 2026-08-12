# pages/policy_objectives.py - Policy & Objectives Page

from dash import Input, Output, html, dcc, no_update
import dash

def policy_objectives_page():
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
                        "Policy & Objectives",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Manage IMS Policy and monitor business objectives",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # Two Cards - Same style as procurement page
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 1fr)',
                    'gap': '24px'
                },
                children=[
                    # Card 1 - Objective Monitoring
                    html.Div(
                        id="card-objective-monitoring",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '6px', 'background': '#f59e0b'}),
                            html.Div(
                                style={'padding': '28px'},
                                children=[
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'justifyContent': 'space-between',
                                            'alignItems': 'flex-start',
                                            'marginBottom': '20px'
                                        },
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '56px',
                                                    'height': '56px',
                                                    'background': '#fef3c7',
                                                    'borderRadius': '16px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(
                                                    className="fas fa-bullseye",
                                                    style={'color': '#f59e0b', 'fontSize': '26px'}
                                                )
                                            ),
                                            html.I(
                                                className="fas fa-arrow-right",
                                                style={'color': '#cbd5e1', 'fontSize': '20px'}
                                            )
                                        ]
                                    ),
                                    html.Div([
                                        html.H3(
                                            "Objective Monitoring",
                                            style={
                                                'fontSize': '20px',
                                                'fontWeight': '700',
                                                'color': '#1e293b',
                                                'margin': '0 0 8px 0'
                                            }
                                        ),
                                        html.P(
                                            "Track and monitor Business Development objectives, KPIs, and performance metrics.",
                                            style={
                                                'fontSize': '13px',
                                                'color': '#64748b',
                                                'margin': 0,
                                                'lineHeight': '1.5'
                                            }
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Card 2 - IMS Policy
                    html.Div(
                        id="card-policy",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '6px', 'background': '#3b82f6'}),
                            html.Div(
                                style={'padding': '28px'},
                                children=[
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'justifyContent': 'space-between',
                                            'alignItems': 'flex-start',
                                            'marginBottom': '20px'
                                        },
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '56px',
                                                    'height': '56px',
                                                    'background': '#dbeafe',
                                                    'borderRadius': '16px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(
                                                    className="fas fa-file-alt",
                                                    style={'color': '#3b82f6', 'fontSize': '26px'}
                                                )
                                            ),
                                            html.I(
                                                className="fas fa-arrow-right",
                                                style={'color': '#cbd5e1', 'fontSize': '20px'}
                                            )
                                        ]
                                    ),
                                    html.Div([
                                        html.H3(
                                            "IMS Policy",
                                            style={
                                                'fontSize': '20px',
                                                'fontWeight': '700',
                                                'color': '#1e293b',
                                                'margin': '0 0 8px 0'
                                            }
                                        ),
                                        html.P(
                                            "View the Integrated Management System (IMS) Policy document.",
                                            style={
                                                'fontSize': '13px',
                                                'color': '#64748b',
                                                'margin': 0,
                                                'lineHeight': '1.5'
                                            }
                                        )
                                    ])
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def register_policy_objectives_callbacks(app):
    """Register callbacks for Policy & Objectives page"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("card-objective-monitoring", "n_clicks"),
         Input("card-policy", "n_clicks")],
        prevent_initial_call=True
    )
    def navigate_policy_cards(obj_clicks, policy_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id == "card-objective-monitoring":
            return "/business-dev"
        elif button_id == "card-policy":
            return "/ims-policy"
        
        return no_update