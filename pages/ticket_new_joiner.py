# pages/ticket_new_joiner.py - New Joiner Safety Induction Training Request

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def ticket_new_joiner_page():
    return html.Div(
        style={
            'padding': '20px 30px',
            'background': '#f0f2f5',
            'minHeight': '100vh'
        },
        children=[
            # ==================== HEADER ====================
            html.Div(
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'space-between',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'},
                        children=[
                            html.Div(
                                style={
                                    'width': '40px',
                                    'height': '40px',
                                    'background': '#dbeafe',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center'
                                },
                                children=html.I(
                                    className="fas fa-user-graduate",
                                    style={'color': '#3b82f6', 'fontSize': '20px'}
                                )
                            ),
                            html.Div(
                                style={'fontSize': '22px', 'fontWeight': '700', 'color': '#1a2332'},
                                children="New Joiner / Visitor Safety Induction Training Request"
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'gap': '12px'},
                        children=[
                            html.Button(
                                "← Back to EHS",
                                id="back-to-ehs-joiner",
                                style={
                                    'background': '#f1f5f9',
                                    'color': '#64748b',
                                    'border': '2px solid #e2e8f0',
                                    'borderRadius': '10px',
                                    'padding': '10px 20px',
                                    'fontSize': '14px',
                                    'fontWeight': '600',
                                    'cursor': 'pointer',
                                    'fontFamily': "'Inter', sans-serif",
                                    'transition': 'all 0.3s ease'
                                }
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== FORM CARD ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e8ecf1',
                    'padding': '30px',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.04)'
                },
                children=[
                    html.Div(
                        style={
                            'fontSize': '16px',
                            'fontWeight': '700',
                            'color': '#1a2332',
                            'marginBottom': '20px',
                            'fontFamily': "'Montserrat', 'Inter', sans-serif"
                        },
                        children="📋 New Joiner / Visitor Safety Induction Training Request"
                    ),
                    
                    html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'},
                        children=[
                            # Name
                            html.Div([
                                html.Label(
                                    "Name *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="joiner-name",
                                    placeholder="Full name",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif"
                                    }
                                )
                            ]),
                            
                            # Employee ID / Visitor ID
                            html.Div([
                                html.Label(
                                    "Employee ID / Visitor ID *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="joiner-id",
                                    placeholder="Enter ID",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif"
                                    }
                                )
                            ]),
                            
                            # Department
                            html.Div([
                                html.Label(
                                    "Department *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="joiner-department",
                                    placeholder="Department name",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif"
                                    }
                                )
                            ]),
                            
                            # Manager
                            html.Div([
                                html.Label(
                                    "Manager",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="joiner-manager",
                                    placeholder="Manager name",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif"
                                    }
                                )
                            ]),
                            
                            # Joining/Visit Date
                            html.Div([
                                html.Label(
                                    "Joining/Visit Date *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="date",
                                    id="joiner-date",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif"
                                    }
                                )
                            ]),
                            
                            # Role
                            html.Div([
                                html.Label(
                                    "Role *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Dropdown(
                                    id="joiner-role",
                                    options=[
                                        {'label': 'Onsite', 'value': 'onsite'},
                                        {'label': 'Office Work', 'value': 'office'},
                                        {'label': 'Hybrid', 'value': 'hybrid'}
                                    ],
                                    placeholder="Select role...",
                                    style={
                                        'borderRadius': '10px',
                                        'border': '2px solid #e2e8f0',
                                        'fontFamily': "'Inter', sans-serif",
                                        'fontSize': '14px'
                                    }
                                )
                            ]),
                            
                            # Training Mode
                            html.Div([
                                html.Label(
                                    "Training Mode (Online) *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Dropdown(
                                    id="joiner-training-mode",
                                    options=[
                                        {'label': 'Online - Zoom', 'value': 'zoom'},
                                        {'label': 'Online - Teams', 'value': 'teams'},
                                        {'label': 'Online - Webex', 'value': 'webex'},
                                        {'label': 'In-Person', 'value': 'inperson'}
                                    ],
                                    placeholder="Select training mode...",
                                    style={
                                        'borderRadius': '10px',
                                        'border': '2px solid #e2e8f0',
                                        'fontFamily': "'Inter', sans-serif",
                                        'fontSize': '14px'
                                    }
                                )
                            ], style={'gridColumn': 'span 2'})
                        ]
                    ),
                    
                    # ==================== BUTTONS ====================
                    html.Div(
                        style={'display': 'flex', 'gap': '16px', 'marginTop': '24px'},
                        children=[
                            html.Button(
                                "Submit Request",
                                id="submit-joiner-ticket",
                                style={
                                    'background': 'linear-gradient(135deg, #0d2b55, #1a4a7a)',
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': '10px',
                                    'padding': '14px 36px',
                                    'fontSize': '15px',
                                    'fontWeight': '600',
                                    'cursor': 'pointer',
                                    'fontFamily': "'Montserrat', 'Inter', sans-serif",
                                    'boxShadow': '0 4px 15px rgba(13,43,85,0.2)',
                                    'transition': 'all 0.3s ease'
                                }
                            ),
                            html.Button(
                                "Clear Form",
                                id="clear-joiner-ticket",
                                style={
                                    'background': '#f1f5f9',
                                    'color': '#64748b',
                                    'border': '2px solid #e2e8f0',
                                    'borderRadius': '10px',
                                    'padding': '12px 24px',
                                    'fontSize': '15px',
                                    'fontWeight': '600',
                                    'cursor': 'pointer',
                                    'fontFamily': "'Montserrat', 'Inter', sans-serif",
                                    'transition': 'all 0.3s ease'
                                }
                            )
                        ]
                    ),
                    
                    # ==================== SUCCESS MESSAGE ====================
                    html.Div(
                        id="joiner-success-message",
                        style={
                            'display': 'none',
                            'background': '#ecfdf5',
                            'border': '1px solid #10b981',
                            'borderRadius': '10px',
                            'padding': '16px 20px',
                            'marginTop': '20px',
                            'color': '#065f46'
                        },
                        children=[
                            html.Div(
                                style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'},
                                children=[
                                    html.I(className="fas fa-check-circle", style={'color': '#10b981', 'fontSize': '20px'}),
                                    html.Div(
                                        "✅ New Joiner Training Request submitted successfully!",
                                        style={'fontWeight': '600', 'fontSize': '15px'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def register_ticket_joiner_callbacks(app):
    """Register callbacks for New Joiner Ticket"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("back-to-ehs-joiner", "n_clicks")],
        prevent_initial_call=True
    )
    def go_back_to_ehs(n_clicks):
        if n_clicks:
            return "/ehs"
        return no_update
    
    @app.callback(
        Output("joiner-success-message", "style"),
        [Input("submit-joiner-ticket", "n_clicks")],
        [State("joiner-name", "value"),
         State("joiner-id", "value"),
         State("joiner-department", "value"),
         State("joiner-manager", "value"),
         State("joiner-date", "value"),
         State("joiner-role", "value"),
         State("joiner-training-mode", "value")],
        prevent_initial_call=True
    )
    def submit_ticket(n_clicks, name, emp_id, dept, manager, date, role, mode):
        if not n_clicks:
            return {'display': 'none'}
        
        if not name or not emp_id or not dept or not date:
            return {'display': 'none'}
        
        print(f"\n✅ NEW JOINER TRAINING REQUEST SUBMITTED")
        print(f"Name: {name}")
        print(f"ID: {emp_id}")
        print(f"Department: {dept}")
        print(f"Manager: {manager}")
        print(f"Date: {date}")
        print(f"Role: {role}")
        print(f"Training Mode: {mode}")
        print("=" * 50)
        
        return {
            'display': 'block',
            'background': '#ecfdf5',
            'border': '1px solid #10b981',
            'borderRadius': '10px',
            'padding': '16px 20px',
            'marginTop': '20px',
            'color': '#065f46'
        }
    
    @app.callback(
        [Output("joiner-name", "value"),
         Output("joiner-id", "value"),
         Output("joiner-department", "value"),
         Output("joiner-manager", "value"),
         Output("joiner-date", "value"),
         Output("joiner-role", "value"),
         Output("joiner-training-mode", "value"),
         Output("joiner-success-message", "style", allow_duplicate=True)],
        [Input("clear-joiner-ticket", "n_clicks")],
        prevent_initial_call=True
    )
    def clear_form(n_clicks):
        if n_clicks:
            return None, None, None, None, None, None, None, {'display': 'none'}
        return no_update