# pages/procurement.py - Procurement Page with Vendor Evaluation Card Only

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update

def procurement_page():
    """Procurement Department Page - Vendor Evaluation Card Only"""
    
    return html.Div([
        # Simple Header
        html.Div(style={"marginBottom": "24px"}, children=[
            html.H1("Procurement", style={"fontSize": "24px", "fontWeight": "700", "color": "#1e293b", "margin": "0 0 4px 0"}),
            html.P("Manage vendor evaluation", style={"fontSize": "14px", "color": "#64748b", "margin": 0})
        ]),
        
        # Single Card - Vendor Evaluation
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr", "gap": "24px", "marginBottom": "24px", "maxWidth": "500px"}, children=[
            # Card 1 - Vendor Evaluation (Blue/Purple theme)
            html.Div(
                id="card-vendor-evaluation", 
                style={
                    "background": "white", 
                    "borderRadius": "16px", 
                    "border": "1px solid #e9ecef", 
                    "overflow": "hidden",
                    "cursor": "pointer",
                    "transition": "transform 0.2s, box-shadow 0.2s"
                },
                children=[
                    html.Div(style={"height": "6px", "background": "#667eea"}),
                    html.Div(style={"padding": "28px"}, children=[
                        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "20px"}, children=[
                            html.Div(style={
                                "width": "56px", 
                                "height": "56px", 
                                "background": "#eef2ff", 
                                "borderRadius": "16px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center"
                            }, children=html.I(className="fas fa-clipboard-list", style={"color": "#667eea", "fontSize": "26px"})),
                            html.I(className="fas fa-arrow-right", style={"color": "#cbd5e1", "fontSize": "20px"})
                        ]),
                        html.Div([
                            html.H3("Vendor Evaluation", style={
                                "fontSize": "20px", 
                                "fontWeight": "700", 
                                "color": "#1e293b", 
                                "margin": "0 0 8px 0"
                            }),
                            html.P("Evaluate Vendors | Form V2.0", style={
                                "fontSize": "13px", 
                                "color": "#64748b", 
                                "margin": 0
                            })
                        ])
                    ])
                ]
            )
        ]),
        
        # Hidden dummy elements to prevent callback errors from other pages
        html.Div([
            html.Div(id="card-mom-tracking", style={"display": "none"}),
            html.Div(id="card-risk-tracking", style={"display": "none"}),
            html.Div(id="card-safety-stats", style={"display": "none"}),
            html.Div(id="card-nc-criticality", style={"display": "none"}),
            html.Div(id="card-nc-department", style={"display": "none"}),
            html.Div(id="card-nc-projects", style={"display": "none"}),
            html.Div(id="card-org-knowledge", style={"display": "none"}),
            html.Div(id="card-security-incidents", style={"display": "none"}),
            html.Div(id="card-quick-stats", style={"display": "none"}),
            html.Div(id="card-safety-dashboard", style={"display": "none"}),
            html.Div(id="card-reports", style={"display": "none"}),
            html.Div(id="card-project-safety", style={"display": "none"}),
            html.Div(id="card-training", style={"display": "none"}),
            html.Div(id="card-work-permit", style={"display": "none"}),
            html.Div(id="card-risk-assessment", style={"display": "none"}),
            html.Div(id="card-incident", style={"display": "none"}),
            html.Div(id="card-contractor", style={"display": "none"}),
            html.Div(id="card-annual-plan", style={"display": "none"}),
            html.Div(id="card-quarterly-meeting", style={"display": "none"}),
            html.Div(id="card-ehs-walkthrough", style={"display": "none"}),
            html.Div(id="card-management-walkthrough", style={"display": "none"}),
            html.Div(id="card-ehs-statistics", style={"display": "none"}),
            html.Div(id="card-virtual-walkthrough", style={"display": "none"}),
            html.Div(id="card-incident-investigation", style={"display": "none"}),
            html.Div(id="card-objective-monitoring", style={"display": "none"}),
            html.Div(id="card-policy", style={"display": "none"}),
            html.Div(id="card-hr-dashboard", style={"display": "none"}),
            html.Div(id="card-admin-dashboard", style={"display": "none"}),
            html.Div(id="card-operation-dashboard", style={"display": "none"}),
            html.Div(id="card-procurement-dashboard", style={"display": "none"}),
            html.Div(id="card-quality-dashboard", style={"display": "none"}),
            html.Div(id="card-engineering-dashboard", style={"display": "none"}),
            html.Div(id="card-finance-dashboard", style={"display": "none"}),
            html.Div(id="card-marketing-dashboard", style={"display": "none"}),
            html.Div(id="card-legal-dashboard", style={"display": "none"}),
            html.Div(id="card-it-dashboard", style={"display": "none"}),
            html.Div(id="card-security-dashboard", style={"display": "none"}),
            html.Div(id="card-audit-dashboard", style={"display": "none"}),
            html.Div(id="card-compliance-dashboard", style={"display": "none"}),
            html.Div(id="card-risk-dashboard", style={"display": "none"}),
            html.Div(id="card-supplychain-dashboard", style={"display": "none"}),
            html.Div(id="card-logistics-dashboard", style={"display": "none"}),
            html.Div(id="card-warehouse-dashboard", style={"display": "none"}),
            html.Div(id="card-inventory-dashboard", style={"display": "none"}),
            html.Div(id="card-maintenance-dashboard", style={"display": "none"}),
            html.Div(id="card-facility-dashboard", style={"display": "none"}),
            html.Div(id="card-environment-dashboard", style={"display": "none"}),
            html.Div(id="card-energy-dashboard", style={"display": "none"}),
            html.Div(id="card-waste-dashboard", style={"display": "none"}),
            html.Div(id="card-water-dashboard", style={"display": "none"}),
            html.Div(id="card-carbon-dashboard", style={"display": "none"}),
            html.Div(id="card-sustainability-dashboard", style={"display": "none"}),
            html.Div(id="card-training-feedback", style={"display": "none"})
        ])
    ])


def register_procurement_callbacks(app):
    """Register procurement page callbacks"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("card-vendor-evaluation", "n_clicks"),
        prevent_initial_call=True
    )
    def go_to_vendor_evaluation(n_clicks):
        if n_clicks:
            return "/vendor-evaluation"
        return no_update