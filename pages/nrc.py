# pages/nrc.py - NRC Page with Audit Checklist Table

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from dash.dependencies import ALL
import json
import re
import time
from datetime import datetime
from database import get_audit_checklist, update_audit_checklist_status

def nrc_page():
    """NRC Page - Audit Checklist"""
    
    audit_checklist = get_audit_checklist()
    
    # Calculate statistics
    total = len(audit_checklist)
    compliant = len([i for i in audit_checklist if i.get('status') == 'Compliant'])
    non_compliant = len([i for i in audit_checklist if i.get('status') == 'Non-Compliant'])
    partially_compliant = len([i for i in audit_checklist if i.get('status') == 'Partially Compliant'])
    not_started = len([i for i in audit_checklist if i.get('status') == 'Not Started'])
    
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            # Header
            html.Div(
                style={'marginBottom': '20px'},
                children=[
                    html.H1(
                        "NRC - Audit Checklist",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Track and monitor audit checklist items",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # ========== PERFORMANCE DASHBOARD - STATUS OVERVIEW ==========
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px 20px',
                    'border': '1px solid #e9ecef',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(
                        style={'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '12px'},
                        children="PERFORMANCE DASHBOARD - STATUS OVERVIEW"
                    ),
                    html.Div(
                        style={
                            'display': 'grid',
                            'gridTemplateColumns': 'repeat(5, 1fr)',
                            'gap': '12px'
                        },
                        children=[
                            # Total
                            html.Div(
                                style={
                                    'background': '#f8fafc',
                                    'borderRadius': '8px',
                                    'padding': '12px',
                                    'textAlign': 'center',
                                    'border': '1px solid #e2e8f0'
                                },
                                children=[
                                    html.Div(
                                        "Total Items",
                                        style={'fontSize': '11px', 'color': '#64748b', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(total),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#667eea'}
                                    )
                                ]
                            ),
                            # Compliant
                            html.Div(
                                style={
                                    'background': '#f8fafc',
                                    'borderRadius': '8px',
                                    'padding': '12px',
                                    'textAlign': 'center',
                                    'border': '1px solid #e2e8f0'
                                },
                                children=[
                                    html.Div(
                                        "Compliant",
                                        style={'fontSize': '11px', 'color': '#10b981', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(compliant),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#10b981'}
                                    )
                                ]
                            ),
                            # Partially Compliant
                            html.Div(
                                style={
                                    'background': '#f8fafc',
                                    'borderRadius': '8px',
                                    'padding': '12px',
                                    'textAlign': 'center',
                                    'border': '1px solid #e2e8f0'
                                },
                                children=[
                                    html.Div(
                                        "Partially Compliant",
                                        style={'fontSize': '11px', 'color': '#eab308', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(partially_compliant),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#eab308'}
                                    )
                                ]
                            ),
                            # Non-Compliant
                            html.Div(
                                style={
                                    'background': '#f8fafc',
                                    'borderRadius': '8px',
                                    'padding': '12px',
                                    'textAlign': 'center',
                                    'border': '1px solid #e2e8f0'
                                },
                                children=[
                                    html.Div(
                                        "Non-Compliant",
                                        style={'fontSize': '11px', 'color': '#dc2626', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(non_compliant),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#dc2626'}
                                    )
                                ]
                            ),
                            # Not Started
                            html.Div(
                                style={
                                    'background': '#f8fafc',
                                    'borderRadius': '8px',
                                    'padding': '12px',
                                    'textAlign': 'center',
                                    'border': '1px solid #e2e8f0'
                                },
                                children=[
                                    html.Div(
                                        "Not Started",
                                        style={'fontSize': '11px', 'color': '#94a3b8', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(not_started),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#94a3b8'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ========== TABLE ==========
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px',
                    'border': '1px solid #e9ecef',
                    'overflowX': 'auto'
                },
                children=[
                    # Table Title with Search
                    html.Div(
                        style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'marginBottom': '16px',
                            'paddingBottom': '12px',
                            'borderBottom': '2px solid #eef2f6'
                        },
                        children=[
                            html.H3(
                                "AUDIT CHECKLIST",
                                style={'margin': '0', 'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.Div(
                                style={'display': 'flex', 'gap': '10px'},
                                children=[
                                    dcc.Input(
                                        id="nrc-search-input",
                                        type="text",
                                        placeholder="Search by clause or description...",
                                        style={
                                            'padding': '6px 12px',
                                            'borderRadius': '6px',
                                            'border': '1px solid #e2e8f0',
                                            'fontSize': '12px',
                                            'width': '250px'
                                        }
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Table
                    html.Div(
                        id="nrc-table-container",
                        style={'overflowX': 'auto'},
                        children=[
                            html.Table(
                                id="nrc-table",
                                style={
                                    'width': '100%', 
                                    'borderCollapse': 'collapse',
                                    'fontSize': '12px',
                                    'minWidth': '1200px'
                                },
                                children=[
                                    html.Thead(
                                        html.Tr([
                                            html.Th("Clause", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Description", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'minWidth': '200px'}),
                                            html.Th("QMS 9001", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '100px'}),
                                            html.Th("EMS 14001", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '100px'}),
                                            html.Th("OHSMS 45001", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '100px'}),
                                            html.Th("ITSMS 20000-1", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '100px'}),
                                            html.Th("ISMS 27001", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '100px'}),
                                            html.Th("Status", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '100px'}),
                                            html.Th("Findings/Remarks", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'minWidth': '150px'}),
                                            html.Th("Actions", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'width': '80px'})
                                        ])
                                    ),
                                    html.Tbody(id="nrc-table-body")
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ========== EVALUATION MODAL ==========
            html.Div(
                id="nrc-eval-modal",
                className="modal",
                style={"display": "none"},
                children=[
                    html.Div(
                        className="modal-content",
                        style={
                            'maxWidth': '500px',
                            'width': '90%',
                            'maxHeight': '80vh',
                            'borderRadius': '16px',
                            'background': 'white',
                            'border': '1px solid #e2e8f0',
                            'overflowY': 'auto',
                            'scrollbarWidth': 'none',
                            'msOverflowStyle': 'none'
                        },
                        children=[
                            # Modal Header
                            html.Div(
                                style={
                                    'padding': '16px 20px',
                                    'borderBottom': '1px solid #eef2f6',
                                    'display': 'flex',
                                    'justifyContent': 'space-between',
                                    'alignItems': 'center',
                                    'background': '#fafbff',
                                    'position': 'sticky',
                                    'top': '0',
                                    'zIndex': '10',
                                    'borderRadius': '16px 16px 0 0'
                                },
                                children=[
                                    html.H2(
                                        id="nrc-eval-title",
                                        style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}
                                    ),
                                    html.I(
                                        className="fas fa-times",
                                        id="close-nrc-eval-modal",
                                        style={'cursor': 'pointer', 'color': '#94a3b8', 'fontSize': '20px', 'transition': 'all 0.3s ease'}
                                    )
                                ]
                            ),
                            
                            # Modal Body
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    # Info
                                    html.Div(
                                        id="nrc-eval-info",
                                        style={
                                            'background': '#f8fafc',
                                            'padding': '12px',
                                            'borderRadius': '8px',
                                            'marginBottom': '16px',
                                            'border': '1px solid #e2e8f0',
                                            'fontSize': '13px'
                                        }
                                    ),
                                    
                                    # Status Dropdown
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Status",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Dropdown(
                                                id="nrc-eval-status",
                                                options=[
                                                    {"label": "Compliant", "value": "Compliant"},
                                                    {"label": "Partially Compliant", "value": "Partially Compliant"},
                                                    {"label": "Non-Compliant", "value": "Non-Compliant"},
                                                    {"label": "Not Started", "value": "Not Started"}
                                                ],
                                                placeholder="Select status",
                                                style={'borderRadius': '8px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Findings/Remarks
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Findings / Remarks",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Textarea(
                                                id="nrc-eval-remarks",
                                                rows=3,
                                                placeholder="Enter findings or remarks...",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px', 'resize': 'vertical'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Modal Footer
                            html.Div(
                                style={
                                    'padding': '12px 20px',
                                    'borderTop': '1px solid #eef2f6',
                                    'display': 'flex',
                                    'justifyContent': 'flex-end',
                                    'gap': '10px',
                                    'position': 'sticky',
                                    'bottom': '0',
                                    'background': 'white',
                                    'zIndex': '10',
                                    'borderRadius': '0 0 16px 16px'
                                },
                                children=[
                                    html.Button(
                                        "Cancel",
                                        id="cancel-nrc-eval-modal",
                                        style={
                                            'padding': '6px 16px',
                                            'background': '#f1f5f9',
                                            'border': '1px solid #e2e8f0',
                                            'borderRadius': '6px',
                                            'cursor': 'pointer',
                                            'fontWeight': '500',
                                            'fontSize': '13px',
                                            'color': '#64748b',
                                            'transition': 'all 0.3s ease'
                                        }
                                    ),
                                    html.Button(
                                        "Save",
                                        id="save-nrc-evaluation",
                                        style={
                                            'padding': '6px 20px',
                                            'background': 'linear-gradient(135deg, #667eea, #764ba2)',
                                            'color': 'white',
                                            'border': 'none',
                                            'borderRadius': '6px',
                                            'cursor': 'pointer',
                                            'fontWeight': '500',
                                            'fontSize': '13px',
                                            'transition': 'all 0.3s ease'
                                        }
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # CSS
            html.Div([
                dcc.Markdown("""
                <style>
                    .modal-content::-webkit-scrollbar {
                        display: none;
                    }
                    .modal-content {
                        scrollbar-width: none;
                        -ms-overflow-style: none;
                    }
                    
                    #cancel-nrc-eval-modal:hover {
                        background: #e2e8f0;
                    }
                    
                    #save-nrc-evaluation:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    }
                    
                    #close-nrc-eval-modal:hover {
                        color: #ef4444;
                        transform: rotate(90deg);
                    }
                    
                    .toast-success {
                        animation: slideInRight 0.5s ease;
                    }
                    
                    @keyframes slideInRight {
                        from {
                            transform: translateX(100%);
                            opacity: 0;
                        }
                        to {
                            transform: translateX(0);
                            opacity: 1;
                        }
                    }
                </style>
                """, dangerously_allow_html=True)
            ]),
            
            # Success Toast
            html.Div(
                id="nrc-success-toast",
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'bottom': '30px',
                    'right': '30px',
                    'background': '#10b981',
                    'color': 'white',
                    'padding': '14px 24px',
                    'borderRadius': '12px',
                    'zIndex': '10000',
                    'fontSize': '14px',
                    'fontWeight': '500',
                    'boxShadow': '0 8px 30px rgba(16, 185, 129, 0.4)',
                    'alignItems': 'center',
                    'gap': '12px',
                    'minWidth': '200px'
                },
                children=[
                    html.I(className="fas fa-check-circle", style={'fontSize': '18px'}),
                    html.Span("Saved successfully!")
                ]
            ),
            
            # Stores
            dcc.Store(id="nrc-data-store", data=audit_checklist),
            dcc.Store(id="nrc-selected-id", data=None),
            dcc.Store(id="nrc-modal-trigger", data=0),
            dcc.Store(id="nrc-page-loaded", data=0)
        ]
    )


def register_nrc_callbacks(app):
    """Register callbacks for NRC page"""
    
    @app.callback(
        Output("nrc-page-loaded", "data"),
        Input("nrc-table-body", "children"),
        prevent_initial_call=True
    )
    def set_page_loaded(children):
        return 1
    
    @app.callback(
        Output("nrc-table-body", "children"),
        [Input("nrc-data-store", "data"),
         Input("nrc-search-input", "value")]
    )
    def update_table(audit_data, search_term):
        if not audit_data:
            return [html.Tr(html.Td("No items found", colSpan=10, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        filtered = audit_data.copy()
        if search_term:
            search_lower = search_term.lower()
            filtered = [i for i in filtered if 
                       search_lower in str(i.get('clause', '')).lower() or 
                       search_lower in str(i.get('description', '')).lower()]
        
        rows = []
        for item in filtered:
            # Status badge colors
            status_colors = {
                "Compliant": {"bg": "#ecfdf5", "color": "#10b981"},
                "Partially Compliant": {"bg": "#fefce8", "color": "#eab308"},
                "Non-Compliant": {"bg": "#fef2f2", "color": "#dc2626"},
                "Not Started": {"bg": "#f1f5f9", "color": "#94a3b8"}
            }
            
            # Function to create status badge
            def get_status_badge(value):
                if not value:
                    value = "Not Started"
                sc = status_colors.get(value, {"bg": "#f1f5f9", "color": "#94a3b8"})
                return html.Span(
                    value,
                    style={'background': sc["bg"], 'color': sc["color"], 'padding': '3px 8px', 'borderRadius': '20px', 'fontSize': '10px', 'fontWeight': '600', 'display': 'inline-block'}
                )
            
            status_badge = get_status_badge(item.get('status', 'Not Started'))
            
            edit_btn = html.Button(
                "Edit",
                id={"type": "edit-nrc", "index": item.get('id', 0)},
                style={'padding': '4px 12px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '500'}
            )
            
            rows.append(html.Tr([
                html.Td(str(item.get('clause', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': '#1e293b'}),
                html.Td(str(item.get('description', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(get_status_badge(item.get('qms_9001')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td(get_status_badge(item.get('ems_14001')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td(get_status_badge(item.get('ohsms_45001')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td(get_status_badge(item.get('itsms_20000_1')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td(get_status_badge(item.get('isms_27001')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td(status_badge, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td(str(item.get('findings_remarks', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#64748b'}),
                html.Td(edit_btn, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'})
            ]))
        
        if not rows:
            rows = [html.Tr(html.Td("No matching items", colSpan=10, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        return rows
    
    @app.callback(
        Output("nrc-modal-trigger", "data"),
        [Input({"type": "edit-nrc", "index": ALL}, "n_clicks")],
        [State("nrc-page-loaded", "data")],
        prevent_initial_call=True
    )
    def set_modal_trigger(edit_clicks, page_loaded):
        if not page_loaded:
            return 0
        
        ctx = callback_context
        if not ctx.triggered:
            return 0
        
        trigger_id = ctx.triggered[0]["prop_id"]
        
        if "edit-nrc" in trigger_id:
            match = re.search(r'"index":(\d+)', trigger_id)
            if match:
                return int(match.group(1))
        
        return 0
    
    @app.callback(
        [Output("nrc-eval-modal", "style"),
         Output("nrc-eval-title", "children"),
         Output("nrc-eval-info", "children"),
         Output("nrc-selected-id", "data"),
         Output("nrc-eval-status", "value"),
         Output("nrc-eval-remarks", "value")],
        [Input("nrc-modal-trigger", "data"),
         Input("close-nrc-eval-modal", "n_clicks"),
         Input("cancel-nrc-eval-modal", "n_clicks")],
        [State("nrc-data-store", "data")],
        prevent_initial_call=True
    )
    def open_modal(trigger_id, close_clicks, cancel_clicks, audit_data):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, "Edit Item", html.Div(), None, None, None
        
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if trigger in ["close-nrc-eval-modal", "cancel-nrc-eval-modal"]:
            return {"display": "none"}, "Edit Item", html.Div(), None, None, None
        
        if trigger == "nrc-modal-trigger" and trigger_id and trigger_id > 0:
            for item in audit_data:
                if item.get('id') == trigger_id:
                    info = html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '6px', 'fontSize': '13px'},
                        children=[
                            html.Div([html.Strong("Clause: ", style={'color': '#64748b'}), html.Span(str(item.get('clause', '')), style={'fontWeight': '500'})]),
                            html.Div([html.Strong("Description: ", style={'color': '#64748b'}), html.Span(str(item.get('description', '')), style={'fontWeight': '500'})]),
                            html.Div([html.Strong("Current Status: ", style={'color': '#64748b'}), html.Span(str(item.get('status', 'Not Started')), style={'fontWeight': '500'})])
                        ]
                    )
                    return (
                        {"display": "flex"},
                        f"Edit: {item.get('clause', '')}",
                        info,
                        item.get('id'),
                        item.get('status', 'Not Started'),
                        item.get('findings_remarks', '')
                    )
        
        return {"display": "none"}, "Edit Item", html.Div(), None, None, None
    
    @app.callback(
        [Output("nrc-data-store", "data", allow_duplicate=True),
         Output("nrc-eval-modal", "style", allow_duplicate=True),
         Output("nrc-success-toast", "style", allow_duplicate=True)],
        Input("save-nrc-evaluation", "n_clicks"),
        [State("nrc-selected-id", "data"),
         State("nrc-eval-status", "value"),
         State("nrc-eval-remarks", "value"),
         State("nrc-data-store", "data")],
        prevent_initial_call=True
    )
    def save_item(n_clicks, selected_id, status, remarks, audit_data):
        if not n_clicks or not selected_id:
            return audit_data, {"display": "none"}, {"display": "none"}
        
        # Update the item in the list
        updated_data = audit_data.copy()
        for item in updated_data:
            if item.get('id') == selected_id:
                if status:
                    item['status'] = status
                if remarks is not None:
                    item['findings_remarks'] = remarks
                break
        
        # Save to database
        success = update_audit_checklist_status(selected_id, status, remarks)
        
        if success:
            # Refresh from database
            from database import get_audit_checklist
            return get_audit_checklist(), {"display": "none"}, {
                'display': 'flex',
                'position': 'fixed',
                'bottom': '30px',
                'right': '30px',
                'background': '#10b981',
                'color': 'white',
                'padding': '14px 24px',
                'borderRadius': '12px',
                'zIndex': '10000',
                'fontSize': '14px',
                'fontWeight': '500',
                'boxShadow': '0 8px 30px rgba(16, 185, 129, 0.4)',
                'alignItems': 'center',
                'gap': '12px',
                'minWidth': '200px'
            }
        
        return updated_data, {"display": "none"}, {"display": "none"}
    
    @app.callback(
        Output("nrc-success-toast", "style", allow_duplicate=True),
        Input("nrc-success-toast", "style"),
        prevent_initial_call=True
    )
    def hide_toast(style):
        if style and style.get('display') != 'none':
            time.sleep(3)
            return {"display": "none"}
        return {"display": "none"}