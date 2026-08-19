# pages/ticket_safety_observation.py - Safety Observation Ticket Form

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
import datetime

def ticket_safety_observation_page():
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
                                    'background': '#ecfdf5',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center'
                                },
                                children=html.I(
                                    className="fas fa-shield-alt",
                                    style={'color': '#10b981', 'fontSize': '20px'}
                                )
                            ),
                            html.Div(
                                style={'fontSize': '22px', 'fontWeight': '700', 'color': '#1a2332'},
                                children="Safety Observation Ticket"
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'gap': '12px'},
                        children=[
                            html.Button(
                                "← Back to EHS",
                                id="back-to-ehs-btn",
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
                        children="🛡️ Safety Observation Form"
                    ),
                    
                    html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'},
                        children=[
                            # Location
                            html.Div([
                                html.Label(
                                    "Location *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="safety-location",
                                    placeholder="Enter location",
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
                            
                            # Date/Time
                            html.Div([
                                html.Label(
                                    "Date/Time *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="safety-datetime",
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
                            
                            # Observation Details
                            html.Div([
                                html.Label(
                                    "Observation Details *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="safety-details",
                                    placeholder="Describe the observation in detail...",
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
                            
                            # Potential Risk
                            html.Div([
                                html.Label(
                                    "Potential Risk",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="safety-risk",
                                    placeholder="Describe potential risk...",
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
                            
                            # Immediate Action
                            html.Div([
                                html.Label(
                                    "Immediate Action Taken (if any)",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="safety-action",
                                    placeholder="Describe immediate action taken...",
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
                            
                            # Reported By
                            html.Div([
                                html.Label(
                                    "Reported By *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="safety-reported-by",
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
                                "Submit Ticket",
                                id="submit-safety-ticket",
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
                                id="clear-safety-ticket",
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
                        id="safety-success-message",
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
                                        "✅ Safety Observation Ticket submitted successfully!",
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


def register_ticket_safety_callbacks(app):
    """Register callbacks for Safety Observation Ticket"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("back-to-ehs-btn", "n_clicks")],
        prevent_initial_call=True
    )
    def go_back_to_ehs(n_clicks):
        if n_clicks:
            return "/ehs"
        return no_update
    
    @app.callback(
        Output("safety-success-message", "style"),
        [Input("submit-safety-ticket", "n_clicks")],
        [State("safety-location", "value"),
         State("safety-datetime", "value"),
         State("safety-details", "value"),
         State("safety-risk", "value"),
         State("safety-action", "value"),
         State("safety-reported-by", "value")],
        prevent_initial_call=True
    )
    def submit_ticket(n_clicks, location, datetime, details, risk, action, reported_by):
        if not n_clicks:
            return {'display': 'none'}
        
        if not location or not details or not reported_by:
            return {'display': 'none'}
        
        print(f"\n✅ SAFETY OBSERVATION TICKET SUBMITTED")
        print(f"Location: {location}")
        print(f"Date/Time: {datetime}")
        print(f"Details: {details}")
        print(f"Risk: {risk}")
        print(f"Action: {action}")
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
        [Output("safety-location", "value"),
         Output("safety-datetime", "value"),
         Output("safety-details", "value"),
         Output("safety-risk", "value"),
         Output("safety-action", "value"),
         Output("safety-reported-by", "value"),
         Output("safety-success-message", "style", allow_duplicate=True)],
        [Input("clear-safety-ticket", "n_clicks")],
        prevent_initial_call=True
    )
    def clear_form(n_clicks):
        if n_clicks:
            return None, None, None, None, None, None, {'display': 'none'}
        return no_update