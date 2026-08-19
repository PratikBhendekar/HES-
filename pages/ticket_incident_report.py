# pages/ticket_incident_report.py - Incident Report Ticket

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def ticket_incident_report_page():
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
                                    'background': '#fee2e2',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center'
                                },
                                children=html.I(
                                    className="fas fa-exclamation-triangle",
                                    style={'color': '#ef4444', 'fontSize': '20px'}
                                )
                            ),
                            html.Div(
                                style={'fontSize': '22px', 'fontWeight': '700', 'color': '#1a2332'},
                                children="Incident Report Ticket"
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'gap': '12px'},
                        children=[
                            html.Button(
                                "← Back to EHS",
                                id="back-to-ehs-incident",
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
                        children="🚨 Incident Report Form"
                    ),
                    
                    html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'},
                        children=[
                            # Incident Date & Time
                            html.Div([
                                html.Label(
                                    "Incident Date & Time *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="incident-datetime",
                                    placeholder="YYYY-MM-DD HH:MM",
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
                            
                            # Location
                            html.Div([
                                html.Label(
                                    "Location *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="incident-location",
                                    placeholder="Incident location",
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
                            
                            # Type of Incident
                            html.Div([
                                html.Label(
                                    "Type of Incident *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Dropdown(
                                    id="incident-type",
                                    options=[
                                        {'label': 'Medical Treatment', 'value': 'medical'},
                                        {'label': 'First Aid', 'value': 'first_aid'},
                                        {'label': 'Near Miss', 'value': 'near_miss'},
                                        {'label': 'Fatal', 'value': 'fatal'},
                                        {'label': 'Lost Time Injury', 'value': 'lti'}
                                    ],
                                    placeholder="Select incident type...",
                                    style={
                                        'borderRadius': '10px',
                                        'border': '2px solid #e2e8f0',
                                        'fontFamily': "'Inter', sans-serif",
                                        'fontSize': '14px'
                                    }
                                )
                            ]),
                            
                            # Persons Involved
                            html.Div([
                                html.Label(
                                    "Persons Involved",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="incident-persons",
                                    placeholder="Names of persons involved",
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
                            
                            # Incident Description
                            html.Div([
                                html.Label(
                                    "Incident Description *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="incident-description",
                                    placeholder="Describe the incident in detail...",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif",
                                        'height': '80px',
                                        'resize': 'vertical'
                                    }
                                )
                            ], style={'gridColumn': 'span 2'}),
                            
                            # Injury/Damage Details
                            html.Div([
                                html.Label(
                                    "Injury/Damage Details",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="incident-damage",
                                    placeholder="Describe injury or damage...",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif",
                                        'height': '60px',
                                        'resize': 'vertical'
                                    }
                                )
                            ], style={'gridColumn': 'span 2'}),
                            
                            # Immediate Corrective Action
                            html.Div([
                                html.Label(
                                    "Immediate Corrective Action Taken",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="incident-corrective",
                                    placeholder="Describe corrective action taken...",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif",
                                        'height': '60px',
                                        'resize': 'vertical'
                                    }
                                )
                            ], style={'gridColumn': 'span 2'}),
                            
                            # Witness Details
                            html.Div([
                                html.Label(
                                    "Witness Details (if any)",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="incident-witness",
                                    placeholder="Witness names and contact",
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
                            
                            # Reported By
                            html.Div([
                                html.Label(
                                    "Reported By *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="incident-reported-by",
                                    placeholder="Your name",
                                    style={
                                        'width': '100%',
                                        'padding': '12px 16px',
                                        'border': '2px solid #e2e8f0',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontFamily': "'Inter', sans-serif"
                                    }
                                )
                            ])
                        ]
                    ),
                    
                    # ==================== BUTTONS ====================
                    html.Div(
                        style={'display': 'flex', 'gap': '16px', 'marginTop': '24px'},
                        children=[
                            html.Button(
                                "Submit Report",
                                id="submit-incident-ticket",
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
                                id="clear-incident-ticket",
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
                        id="incident-success-message",
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
                                        "✅ Incident Report submitted successfully!",
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


def register_ticket_incident_callbacks(app):
    """Register callbacks for Incident Report Ticket"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("back-to-ehs-incident", "n_clicks")],
        prevent_initial_call=True
    )
    def go_back_to_ehs(n_clicks):
        if n_clicks:
            return "/ehs"
        return no_update
    
    @app.callback(
        Output("incident-success-message", "style"),
        [Input("submit-incident-ticket", "n_clicks")],
        [State("incident-datetime", "value"),
         State("incident-location", "value"),
         State("incident-type", "value"),
         State("incident-persons", "value"),
         State("incident-description", "value"),
         State("incident-damage", "value"),
         State("incident-corrective", "value"),
         State("incident-witness", "value"),
         State("incident-reported-by", "value")],
        prevent_initial_call=True
    )
    def submit_ticket(n_clicks, datetime, location, incident_type, persons, description, damage, corrective, witness, reported_by):
        if not n_clicks:
            return {'display': 'none'}
        
        if not location or not incident_type or not description or not reported_by:
            return {'display': 'none'}
        
        print(f"\n✅ INCIDENT REPORT SUBMITTED")
        print(f"Date/Time: {datetime}")
        print(f"Location: {location}")
        print(f"Type: {incident_type}")
        print(f"Persons: {persons}")
        print(f"Description: {description}")
        print(f"Damage: {damage}")
        print(f"Corrective Action: {corrective}")
        print(f"Witness: {witness}")
        print(f"Reported By: {reported_by}")
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
        [Output("incident-datetime", "value"),
         Output("incident-location", "value"),
         Output("incident-type", "value"),
         Output("incident-persons", "value"),
         Output("incident-description", "value"),
         Output("incident-damage", "value"),
         Output("incident-corrective", "value"),
         Output("incident-witness", "value"),
         Output("incident-reported-by", "value"),
         Output("incident-success-message", "style", allow_duplicate=True)],
        [Input("clear-incident-ticket", "n_clicks")],
        prevent_initial_call=True
    )
    def clear_form(n_clicks):
        if n_clicks:
            return None, None, None, None, None, None, None, None, None, {'display': 'none'}
        return no_update