# pages/ticket_vendor_orientation.py - New Vendor EHS Orientation Request

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def ticket_vendor_orientation_page():
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
                                    'background': '#fef3c7',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center'
                                },
                                children=html.I(
                                    className="fas fa-handshake",
                                    style={'color': '#f59e0b', 'fontSize': '20px'}
                                )
                            ),
                            html.Div(
                                style={'fontSize': '22px', 'fontWeight': '700', 'color': '#1a2332'},
                                children="New Vendor EHS Orientation Request"
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'gap': '12px'},
                        children=[
                            html.Button(
                                "← Back to EHS",
                                id="back-to-ehs-vendor",
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
                        children="🏗️ Vendor EHS Orientation Form"
                    ),
                    
                    html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'},
                        children=[
                            # Vendor Company Name
                            html.Div([
                                html.Label(
                                    "Vendor Company Name *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="vendor-company",
                                    placeholder="Company name",
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
                            
                            # Vendor Contact Person
                            html.Div([
                                html.Label(
                                    "Vendor Contact Person *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="vendor-contact",
                                    placeholder="Contact person name",
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
                            
                            # Number of Personnel
                            html.Div([
                                html.Label(
                                    "Number of Personnel *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="number",
                                    id="vendor-personnel",
                                    placeholder="Number of people",
                                    min=1,
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
                            
                            # Work Location
                            html.Div([
                                html.Label(
                                    "Work Location *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="text",
                                    id="vendor-location",
                                    placeholder="Work location",
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
                            
                            # Nature of Work
                            html.Div([
                                html.Label(
                                    "Nature of Work *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                )
                            ], style={'gridColumn': 'span 2'}),
                            html.Div([
                                dcc.Textarea(
                                    id="vendor-nature",
                                    placeholder="Describe nature of work...",
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
                            
                            # Expected Start Date
                            html.Div([
                                html.Label(
                                    "Expected Start Date *",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                dcc.Input(
                                    type="date",
                                    id="vendor-start-date",
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
                            
                            # Orientation Required
                            html.Div([
                                html.Label(
                                    "Orientation Required Before Site Access",
                                    style={'fontWeight': '600', 'fontSize': '13px', 'color': '#1a2e44', 'display': 'block', 'marginBottom': '4px'}
                                ),
                                html.Div(
                                    style={
                                        'background': '#dbeafe',
                                        'padding': '10px 16px',
                                        'borderRadius': '10px',
                                        'fontSize': '14px',
                                        'fontWeight': '600',
                                        'color': '#2563eb'
                                    },
                                    children="✅ Yes (Mandatory)"
                                )
                            ])
                        ]
                    ),
                    
                    # ==================== BUTTONS ====================
                    html.Div(
                        style={'display': 'flex', 'gap': '16px', 'marginTop': '24px'},
                        children=[
                            html.Button(
                                "Submit Request",
                                id="submit-vendor-ticket",
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
                                id="clear-vendor-ticket",
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
                        id="vendor-success-message",
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
                                        "✅ Vendor Orientation Request submitted successfully!",
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


def register_ticket_vendor_callbacks(app):
    """Register callbacks for Vendor Orientation Ticket"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("back-to-ehs-vendor", "n_clicks")],
        prevent_initial_call=True
    )
    def go_back_to_ehs(n_clicks):
        if n_clicks:
            return "/ehs"
        return no_update
    
    @app.callback(
        Output("vendor-success-message", "style"),
        [Input("submit-vendor-ticket", "n_clicks")],
        [State("vendor-company", "value"),
         State("vendor-contact", "value"),
         State("vendor-personnel", "value"),
         State("vendor-location", "value"),
         State("vendor-nature", "value"),
         State("vendor-start-date", "value")],
        prevent_initial_call=True
    )
    def submit_ticket(n_clicks, company, contact, personnel, location, nature, start_date):
        if not n_clicks:
            return {'display': 'none'}
        
        if not company or not contact or not location:
            return {'display': 'none'}
        
        print(f"\n✅ VENDOR ORIENTATION REQUEST SUBMITTED")
        print(f"Company: {company}")
        print(f"Contact: {contact}")
        print(f"Personnel: {personnel}")
        print(f"Location: {location}")
        print(f"Nature of Work: {nature}")
        print(f"Start Date: {start_date}")
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
        [Output("vendor-company", "value"),
         Output("vendor-contact", "value"),
         Output("vendor-personnel", "value"),
         Output("vendor-location", "value"),
         Output("vendor-nature", "value"),
         Output("vendor-start-date", "value"),
         Output("vendor-success-message", "style", allow_duplicate=True)],
        [Input("clear-vendor-ticket", "n_clicks")],
        prevent_initial_call=True
    )
    def clear_form(n_clicks):
        if n_clicks:
            return None, None, None, None, None, None, {'display': 'none'}
        return no_update