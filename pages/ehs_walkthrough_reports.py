# pages/ehs_walkthrough_reports.py - EHS Walkthrough Reports Page

import dash
from dash import html, dcc, Input, Output, State, callback_context
import json

# PDF Files data
EHS_WALKTHROUGH_PDFS = [
    {"name": "EHS LINE WALKTHROUGH Report - 03.04.2026", "path": "/assets/EHS LINE WALKTHROUGH report H.O 03.04.2026.pdf", "date": "03 April 2026"},
    {"name": "EHS LINE WALKTHROUGH Report - 02.04.2026", "path": "/assets/EHS LINE WALKTHROUGH report H.O 02.04.2026.pdf", "date": "02 April 2026"}
]

def ehs_walkthrough_reports_page():
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh',
            'fontFamily': "'Inter', sans-serif"
        },
        children=[
            # Font Awesome and Google Fonts
            html.Link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ),
            html.Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
            ),
            html.Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap"
            ),
            
            # Main Container
            html.Div(
                style={'maxWidth': '1000px', 'margin': '0 auto'},
                children=[
                    # Back Button
                    dcc.Link(
                        html.Div(
                            [
                                html.I(className="fas fa-arrow-left", style={'marginRight': '8px'}),
                                html.Span("Back to Reports")
                            ],
                            style={
                                'display': 'inline-flex',
                                'alignItems': 'center',
                                'gap': '8px',
                                'marginBottom': '24px',
                                'padding': '8px 20px',
                                'background': 'white',
                                'border': '1px solid #e2e8f0',
                                'borderRadius': '10px',
                                'color': '#475569',
                                'fontSize': '13px',
                                'fontWeight': '500',
                                'transition': 'all 0.2s ease',
                                'cursor': 'pointer'
                            }
                        ),
                        href="/ehs-reports",
                        style={'textDecoration': 'none'}
                    ),
                    
                    # Page Header
                    html.Div(
                        style={'marginBottom': '32px'},
                        children=[
                            html.H1(
                                "EHS Walkthrough Reports",
                                style={
                                    'fontSize': '28px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'margin': '0 0 8px 0',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.P(
                                "Access and view EHS walkthrough reports",
                                style={
                                    'fontSize': '14px',
                                    'color': '#64748b',
                                    'margin': 0,
                                    'fontFamily': "'Inter', sans-serif"
                                }
                            )
                        ]
                    ),
                    
                    # PDF Grid
                    html.Div(
                        style={
                            'display': 'grid',
                            'gridTemplateColumns': 'repeat(2, 1fr)',
                            'gap': '24px'
                        },
                        children=[
                            html.Div(
                                style={
                                    'background': 'white',
                                    'borderRadius': '20px',
                                    'border': '1px solid #e2e8f0',
                                    'padding': '32px 24px',
                                    'textAlign': 'center',
                                    'transition': 'all 0.3s ease',
                                    'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'width': '80px',
                                            'height': '80px',
                                            'background': 'linear-gradient(135deg, #fee2e2, #fecaca)',
                                            'borderRadius': '20px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'margin': '0 auto 20px auto'
                                        },
                                        children=html.I(className="fas fa-file-pdf", style={'color': '#ef4444', 'fontSize': '36px'})
                                    ),
                                    html.Div(
                                        pdf["name"],
                                        style={
                                            'fontSize': '16px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'marginBottom': '8px',
                                            'fontFamily': "'Poppins', sans-serif"
                                        }
                                    ),
                                    html.Div(
                                        pdf["date"],
                                        style={
                                            'fontSize': '13px',
                                            'color': '#64748b',
                                            'marginBottom': '20px',
                                            'fontFamily': "'Inter', sans-serif"
                                        }
                                    ),
                                    html.Button(
                                        "View Report",
                                        id={"type": "open-pdf", "index": i},
                                        style={
                                            'padding': '10px 28px',
                                            'background': 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                                            'color': 'white',
                                            'border': 'none',
                                            'borderRadius': '10px',
                                            'cursor': 'pointer',
                                            'fontSize': '13px',
                                            'fontWeight': '600',
                                            'fontFamily': "'Poppins', sans-serif",
                                            'transition': 'all 0.3s ease'
                                        }
                                    )
                                ]
                            ) for i, pdf in enumerate(EHS_WALKTHROUGH_PDFS)
                        ]
                    )
                ]
            ),
            
            # Full Screen Modal
            html.Div(
                id="fullscreen-modal",
                style={'display': 'none', 'position': 'fixed', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'background': '#0f172a', 'zIndex': 99999, 'flexDirection': 'column'},
                children=[
                    html.Div(
                        style={
                            'padding': '16px 24px',
                            'background': '#1e293b',
                            'borderBottom': '1px solid #334155',
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'flexShrink': 0
                        },
                        children=[
                            html.Span(id="fullscreen-pdf-name", style={'fontSize': '18px', 'fontWeight': '600', 'color': 'white', 'fontFamily': "'Poppins', sans-serif"}),
                            html.Button(
                                "✕ Close",
                                id="close-fullscreen",
                                style={
                                    'padding': '8px 24px',
                                    'background': '#ef4444',
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': '8px',
                                    'cursor': 'pointer',
                                    'fontSize': '14px',
                                    'fontWeight': '600'
                                }
                            )
                        ]
                    ),
                    html.Div(
                        style={'flex': 1, 'background': '#f1f5f9', 'padding': '10px'},
                        children=[
                            html.Iframe(id="fullscreen-pdf-src", style={'width': '100%', 'height': '100%', 'border': 'none', 'borderRadius': '12px', 'background': 'white'})
                        ]
                    )
                ]
            ),
            
            dcc.Store(id="selected-pdf", data=None)
        ]
    )


def register_ehs_walkthrough_callbacks(app):
    """Register callbacks for EHS Walkthrough Reports page"""
    
    # Open PDF in full screen
    @app.callback(
        [Output("fullscreen-modal", "style"),
         Output("fullscreen-pdf-src", "src"),
         Output("fullscreen-pdf-name", "children")],
        [Input({"type": "open-pdf", "index": dash.dependencies.ALL}, "n_clicks")],
        prevent_initial_call=True
    )
    def open_fullscreen_pdf(clicks):
        ctx = callback_context
        if not ctx.triggered:
            return {'display': 'none'}, "", ""
        
        trigger = ctx.triggered[0]
        trigger_id = trigger["prop_id"].split(".")[0]
        
        try:
            if trigger_id.startswith('{'):
                trigger_dict = json.loads(trigger_id.replace("'", '"'))
                idx = trigger_dict.get("index")
                
                if idx is not None and idx < len(EHS_WALKTHROUGH_PDFS):
                    pdf = EHS_WALKTHROUGH_PDFS[idx]
                    return {'display': 'flex', 'position': 'fixed', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'background': '#0f172a', 'zIndex': 99999, 'flexDirection': 'column'}, pdf["path"], pdf["name"]
        except Exception as e:
            print(f"Error: {e}")
        
        return {'display': 'none'}, "", ""
    
    # Close full screen PDF
    @app.callback(
        Output("fullscreen-modal", "style", allow_duplicate=True),
        Input("close-fullscreen", "n_clicks"),
        prevent_initial_call=True
    )
    def close_fullscreen_pdf(n_clicks):
        if n_clicks:
            return {'display': 'none'}
        return {'display': 'none'}