# pages/reports_analytics.py - Reports & Analytics Page

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def reports_analytics_page():
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            # CSS for Styling
            html.Div([
                dcc.Markdown("""
                <style>
                    .report-card {
                        cursor: pointer !important;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }
                    .report-card:hover {
                        transform: translateY(-8px);
                        box-shadow: 0 20px 30px -12px rgba(0,0,0,0.15);
                    }
                </style>
                """, dangerously_allow_html=True)
            ]),
            
            # Header
            html.Div(
                style={'marginBottom': '28px'},
                children=[
                    html.H1(
                        "Reports & Analytics",
                        style={
                            'fontSize': '28px', 
                            'fontWeight': '700', 
                            'color': '#1e293b', 
                            'margin': '0 0 6px 0',
                            'fontFamily': 'Poppins, sans-serif'
                        }
                    ),
                    html.P(
                        "Access and manage EHS reports and analytics",
                        style={'fontSize': '14px', 'color': '#64748b', 'margin': 0}
                    )
                ]
            ),
            
            # Reports Grid - 3 columns
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '24px',
                    'marginBottom': '24px'
                },
                children=[
                    # Card 1: Quarterly EHS Meeting MOM Report
                    html.Div(
                        id="card-quarterly-meeting",
                        className="report-card",
                        style={
                            'background': 'white', 
                            'borderRadius': '20px', 
                            'border': '1px solid #e9ecef', 
                            'overflow': 'hidden', 
                            'cursor': 'pointer',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#8b5cf6'}),
                            html.Div(style={'padding': '28px', 'textAlign': 'center'}, children=[
                                html.Div(style={'width': '65px', 'height': '65px', 'background': '#ede9fe', 'borderRadius': '16px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin': '0 auto 18px auto'},
                                    children=html.I(className="fas fa-calendar-alt", style={'color': '#8b5cf6', 'fontSize': '28px'})),
                                html.H3("Quarterly EHS Meeting MOM Report", style={'fontSize': '17px', 'fontWeight': '700', 'color': '#1e293b', 'margin': '0 0 10px 0', 'lineHeight': '1.4', 'fontFamily': 'Poppins, sans-serif'}),
                                html.P("Review of organization-wide EHS issues, status of previously open points, and consultations/suggestions from EHS committee members.", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 16px 0', 'lineHeight': '1.5'}),
                                html.Div(style={'marginTop': '8px'}, children=html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '16px'}))
                            ])
                        ]
                    ),
                    
                    # Card 2: EHS Walkthrough Report (Opens separate page)
                    html.Div(
                        id="card-ehs-walkthrough",
                        className="report-card",
                        style={
                            'background': 'white', 
                            'borderRadius': '20px', 
                            'border': '1px solid #e9ecef', 
                            'overflow': 'hidden', 
                            'cursor': 'pointer',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#3b82f6'}),
                            html.Div(style={'padding': '28px', 'textAlign': 'center'}, children=[
                                html.Div(style={'width': '65px', 'height': '65px', 'background': '#dbeafe', 'borderRadius': '16px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin': '0 auto 18px auto'},
                                    children=html.I(className="fas fa-walking", style={'color': '#3b82f6', 'fontSize': '28px'})),
                                html.H3("EHS Walkthrough Report", style={'fontSize': '17px', 'fontWeight': '700', 'color': '#1e293b', 'margin': '0 0 10px 0', 'lineHeight': '1.4', 'fontFamily': 'Poppins, sans-serif'}),
                                html.P("Assessment of EHS implementation at site and identification of improvement recommendations.", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 16px 0', 'lineHeight': '1.5'}),
                                html.Div(style={'marginTop': '8px'}, children=html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '16px'}))
                            ])
                        ]
                    ),
                    
                    # Card 3: Management EHS Walkthrough Report
                    html.Div(
                        id="card-management-walkthrough",
                        className="report-card",
                        style={
                            'background': 'white', 
                            'borderRadius': '20px', 
                            'border': '1px solid #e9ecef', 
                            'overflow': 'hidden', 
                            'cursor': 'pointer',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#10b981'}),
                            html.Div(style={'padding': '28px', 'textAlign': 'center'}, children=[
                                html.Div(style={'width': '65px', 'height': '65px', 'background': '#ecfdf5', 'borderRadius': '16px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin': '0 auto 18px auto'},
                                    children=html.I(className="fas fa-users", style={'color': '#10b981', 'fontSize': '28px'})),
                                html.H3("Management EHS Walkthrough Report", style={'fontSize': '17px', 'fontWeight': '700', 'color': '#1e293b', 'margin': '0 0 10px 0', 'lineHeight': '1.4', 'fontFamily': 'Poppins, sans-serif'}),
                                html.P("Evaluation of leadership commitment towards EHS and consultation with employees on safety practices.", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 16px 0', 'lineHeight': '1.5'}),
                                html.Div(style={'marginTop': '8px'}, children=html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '16px'}))
                            ])
                        ]
                    ),
                    
                    # Card 4: EHS Statistics
                    html.Div(
                        id="card-ehs-statistics",
                        className="report-card",
                        style={
                            'background': 'white', 
                            'borderRadius': '20px', 
                            'border': '1px solid #e9ecef', 
                            'overflow': 'hidden', 
                            'cursor': 'pointer',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#f59e0b'}),
                            html.Div(style={'padding': '28px', 'textAlign': 'center'}, children=[
                                html.Div(style={'width': '65px', 'height': '65px', 'background': '#fef3c7', 'borderRadius': '16px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin': '0 auto 18px auto'},
                                    children=html.I(className="fas fa-chart-bar", style={'color': '#f59e0b', 'fontSize': '28px'})),
                                html.H3("EHS Statistics", style={'fontSize': '17px', 'fontWeight': '700', 'color': '#1e293b', 'margin': '0 0 10px 0', 'lineHeight': '1.4', 'fontFamily': 'Poppins, sans-serif'}),
                                html.P("Overview of key safety metrics including safe manhours, incidents, accidents, unsafe acts, and unsafe conditions.", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 16px 0', 'lineHeight': '1.5'}),
                                html.Div(style={'marginTop': '8px'}, children=html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '16px'}))
                            ])
                        ]
                    ),
                    
                    # Card 5: EHS Virtual Walkthrough
                    html.Div(
                        id="card-virtual-walkthrough",
                        className="report-card",
                        style={
                            'background': 'white', 
                            'borderRadius': '20px', 
                            'border': '1px solid #e9ecef', 
                            'overflow': 'hidden', 
                            'cursor': 'pointer',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#06b6d4'}),
                            html.Div(style={'padding': '28px', 'textAlign': 'center'}, children=[
                                html.Div(style={'width': '65px', 'height': '65px', 'background': '#cffafe', 'borderRadius': '16px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin': '0 auto 18px auto'},
                                    children=html.I(className="fas fa-video", style={'color': '#06b6d4', 'fontSize': '28px'})),
                                html.H3("EHS Virtual Walkthrough", style={'fontSize': '17px', 'fontWeight': '700', 'color': '#1e293b', 'margin': '0 0 10px 0', 'lineHeight': '1.4', 'fontFamily': 'Poppins, sans-serif'}),
                                html.P("Remote assessment of EHS implementation along with improvement recommendations.", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 16px 0', 'lineHeight': '1.5'}),
                                html.Div(style={'marginTop': '8px'}, children=html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '16px'}))
                            ])
                        ]
                    ),
                    
                    # Card 6: Incident Investigation Report
                    html.Div(
                        id="card-incident-investigation",
                        className="report-card",
                        style={
                            'background': 'white', 
                            'borderRadius': '20px', 
                            'border': '1px solid #e9ecef', 
                            'overflow': 'hidden', 
                            'cursor': 'pointer',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#ef4444'}),
                            html.Div(style={'padding': '28px', 'textAlign': 'center'}, children=[
                                html.Div(style={'width': '65px', 'height': '65px', 'background': '#fee2e2', 'borderRadius': '16px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin': '0 auto 18px auto'},
                                    children=html.I(className="fas fa-clipboard-list", style={'color': '#ef4444', 'fontSize': '28px'})),
                                html.H3("Incident Investigation Report", style={'fontSize': '17px', 'fontWeight': '700', 'color': '#1e293b', 'margin': '0 0 10px 0', 'lineHeight': '1.4', 'fontFamily': 'Poppins, sans-serif'}),
                                html.P("Detailed analysis of incidents to identify root causes and recommend corrective and preventive actions.", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 16px 0', 'lineHeight': '1.5'}),
                                html.Div(style={'marginTop': '8px'}, children=html.I(className="fas fa-arrow-right", style={'color': '#cbd5e1', 'fontSize': '16px'}))
                            ])
                        ]
                    )
                ]
            )
        ]
    )


def register_reports_analytics_callbacks(app):
    """Register callbacks for Reports & Analytics page"""
    
    # Navigation for all report cards
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("card-quarterly-meeting", "n_clicks"),
        Input("card-ehs-walkthrough", "n_clicks"),
        Input("card-management-walkthrough", "n_clicks"),
        Input("card-ehs-statistics", "n_clicks"),
        Input("card-virtual-walkthrough", "n_clicks"),
        Input("card-incident-investigation", "n_clicks"),
        prevent_initial_call=True
    )
    def navigate_reports(quarterly, ehs_walk, mgmt_walk, ehs_stats, virtual, incident):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        nav_map = {
            "card-quarterly-meeting": "/reports/quarterly-meeting",
            "card-ehs-walkthrough": "/ehs-walkthrough-reports",
            "card-management-walkthrough": "/reports/management-walkthrough",
            "card-ehs-statistics": "/ehs-safety-dashboard",
            "card-virtual-walkthrough": "/reports/virtual-walkthrough",
            "card-incident-investigation": "/reports/incident-investigation"
        }
        
        if button_id in nav_map:
            return nav_map[button_id]
        
        return no_update