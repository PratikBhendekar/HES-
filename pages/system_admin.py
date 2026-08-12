# pages/system_admin.py - System Admin Page with Administration Objectives Monitoring Table

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from dash.dependencies import ALL
import json
import re
import time
from datetime import datetime
from database import get_all_system_admin_objectives, update_system_admin_status

def system_admin():
    objectives = get_all_system_admin_objectives()
    
    # Calculate statistics
    total = len(objectives)
    on_track = len([o for o in objectives if o.get('status') == 'On Track'])
    at_risk = len([o for o in objectives if o.get('status') == 'At Risk'])
    off_track = len([o for o in objectives if o.get('status') == 'Off Track'])
    not_started = len([o for o in objectives if o.get('status') == 'Not Started'])
    completion_rate = 0 if total == 0 else round((on_track / total) * 100)
    attention_needed = at_risk + off_track
    
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
                        "ADMINISTRATION OBJECTIVES MONITORING TABLE",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Track and monitor administration objectives and directives",
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
                            'gridTemplateColumns': 'repeat(6, 1fr)',
                            'gap': '12px'
                        },
                        children=[
                            # Total Objectives
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
                                        "Total Objectives",
                                        style={'fontSize': '11px', 'color': '#64748b', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(total),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#667eea'}
                                    )
                                ]
                            ),
                            # On Track
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
                                        "On Track",
                                        style={'fontSize': '11px', 'color': '#10b981', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(on_track),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#10b981'}
                                    )
                                ]
                            ),
                            # Completion Rate
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
                                        "Completion Rate",
                                        style={'fontSize': '11px', 'color': '#64748b', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        f"{completion_rate}%",
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#667eea'}
                                    )
                                ]
                            ),
                            # At Risk
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
                                        "At Risk",
                                        style={'fontSize': '11px', 'color': '#eab308', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(at_risk),
                                        style={'fontSize': '24px', 'fontWeight': '700', 'color': '#eab308'}
                                    )
                                ]
                            ),
                            # Off Track
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
                                        "Off Track",
                                        style={'fontSize': '11px', 'color': '#dc2626', 'marginBottom': '4px'}
                                    ),
                                    html.Div(
                                        str(off_track),
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
                                "ADMINISTRATION OBJECTIVES MONITORING TABLE",
                                style={'margin': '0', 'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.Div(
                                style={'display': 'flex', 'gap': '10px'},
                                children=[
                                    dcc.Input(
                                        id="sysadmin-search-input",
                                        type="text",
                                        placeholder="Search objectives...",
                                        style={
                                            'padding': '6px 12px',
                                            'borderRadius': '6px',
                                            'border': '1px solid #e2e8f0',
                                            'fontSize': '12px',
                                            'width': '200px'
                                        }
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Table
                    html.Div(
                        id="sysadmin-table-container",
                        style={'overflowX': 'auto'},
                        children=[
                            html.Table(
                                id="sysadmin-table",
                                style={
                                    'width': '100%', 
                                    'borderCollapse': 'collapse',
                                    'fontSize': '12px',
                                    'minWidth': '1600px'
                                },
                                children=[
                                    html.Thead(
                                        html.Tr([
                                            html.Th("Objective ID", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Category", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Objective", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'minWidth': '150px'}),
                                            html.Th("KPI", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Target", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Timeline", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Responsible Personnel", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Previous Achievement", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Current Achievement*", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Variance", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Trend", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Objective Status", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap', 'minWidth': '130px'}),
                                            html.Th("Evidence", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Evidence Location", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Date of Review", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Reviewed By", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Remarks", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'minWidth': '120px'}),
                                            html.Th("Actions", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'width': '80px'})
                                        ])
                                    ),
                                    html.Tbody(id="sysadmin-table-body")
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ========== DOCUMENT USAGE GUIDELINES ==========
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': '1px solid #e9ecef',
                    'marginTop': '20px'
                },
                children=[
                    html.H4(
                        "DOCUMENT USAGE GUIDELINES & COMPLIANCE INSTRUCTIONS",
                        style={
                            'fontSize': '14px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'marginBottom': '16px'
                        }
                    ),
                    
                    html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '20px'},
                        children=[
                            # Status Classification
                            html.Div(
                                style={'border': '1px solid #eef2f6', 'borderRadius': '8px', 'padding': '16px'},
                                children=[
                                    html.H5(
                                        "1. STATUS CLASSIFICATION",
                                        style={'fontSize': '12px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '10px'}
                                    ),
                                    html.Div(style={'marginBottom': '6px'}, children=[
                                        html.Span("● ", style={'color': '#10b981', 'fontWeight': '700'}),
                                        html.Span("On Track (Green): ", style={'fontWeight': '600'}),
                                        html.Span("Achievement ≥ Target", style={'fontSize': '11px', 'color': '#475569'})
                                    ]),
                                    html.Div(style={'marginBottom': '6px'}, children=[
                                        html.Span("● ", style={'color': '#eab308', 'fontWeight': '700'}),
                                        html.Span("At Risk (Yellow): ", style={'fontWeight': '600'}),
                                        html.Span("Achievement within 5% of Target", style={'fontSize': '11px', 'color': '#475569'})
                                    ]),
                                    html.Div(style={'marginBottom': '6px'}, children=[
                                        html.Span("● ", style={'color': '#dc2626', 'fontWeight': '700'}),
                                        html.Span("Off Track (Red): ", style={'fontWeight': '600'}),
                                        html.Span("Achievement < Target by more than 5%", style={'fontSize': '11px', 'color': '#475569'})
                                    ]),
                                    html.Div(children=[
                                        html.Span("● ", style={'color': '#94a3b8', 'fontWeight': '700'}),
                                        html.Span("Not Started (Grey): ", style={'fontWeight': '600'}),
                                        html.Span("Objective not yet initiated", style={'fontSize': '11px', 'color': '#475569'})
                                    ])
                                ]
                            ),
                            
                            # Review Requirements
                            html.Div(
                                style={'border': '1px solid #eef2f6', 'borderRadius': '8px', 'padding': '16px'},
                                children=[
                                    html.H5(
                                        "2. REVIEW REQUIREMENTS",
                                        style={'fontSize': '12px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '10px'}
                                    ),
                                    html.Div(style={'marginBottom': '6px', 'fontSize': '11px', 'color': '#475569'}, children=[
                                        html.Span("• ", style={'fontWeight': '700'}),
                                        "Objectives must be reviewed quarterly at minimum"
                                    ]),
                                    html.Div(style={'marginBottom': '6px', 'fontSize': '11px', 'color': '#475569'}, children=[
                                        html.Span("• ", style={'fontWeight': '700'}),
                                        "Evidence must be documented and stored in designated location"
                                    ]),
                                    html.Div(style={'fontSize': '11px', 'color': '#475569'}, children=[
                                        html.Span("• ", style={'fontWeight': '700'}),
                                        "Reviewer must sign off on each review cycle"
                                    ])
                                ]
                            ),
                            
                            # Data Entry Standards
                            html.Div(
                                style={'border': '1px solid #eef2f6', 'borderRadius': '8px', 'padding': '16px'},
                                children=[
                                    html.H5(
                                        "3. DATA ENTRY STANDARDS",
                                        style={'fontSize': '12px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '10px'}
                                    ),
                                    html.Div(style={'marginBottom': '6px', 'fontSize': '11px', 'color': '#475569'}, children=[
                                        html.Span("• ", style={'fontWeight': '700'}),
                                        "Achievements must include % symbol for percentage values"
                                    ]),
                                    html.Div(style={'marginBottom': '6px', 'fontSize': '11px', 'color': '#475569'}, children=[
                                        html.Span("• ", style={'fontWeight': '700'}),
                                        "Dates must follow DD-MM-YYYY format"
                                    ]),
                                    html.Div(style={'fontSize': '11px', 'color': '#475569'}, children=[
                                        html.Span("• ", style={'fontWeight': '700'}),
                                        "Remarks are mandatory for any Off Track status"
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    # Additional Notes
                    html.Div(
                        style={
                            'marginTop': '16px',
                            'padding': '12px 16px',
                            'background': '#f8fafc',
                            'borderRadius': '8px',
                            'border': '1px solid #eef2f6'
                        },
                        children=[
                            html.Div(
                                style={'fontSize': '11px', 'color': '#475569', 'marginBottom': '4px'},
                                children=[
                                    html.Span("Variance: ", style={'fontWeight': '700'}),
                                    "Auto-calculated difference between Current Achievement and Target (positive = exceeding, negative = below)"
                                ]
                            ),
                            html.Div(
                                style={'fontSize': '11px', 'color': '#475569', 'marginBottom': '4px'},
                                children=[
                                    html.Span("Trend: ", style={'fontWeight': '700'}),
                                    "Auto-calculated comparison between Previous and Current Achievement (↑ Improving, ↓ Declining, → Stable)"
                                ]
                            ),
                            html.Div(
                                style={'fontSize': '11px', 'color': '#475569', 'marginBottom': '4px'},
                                children=[
                                    html.Span("Priority: ", style={'fontWeight': '700'}),
                                    "Select High/Medium/Low to indicate objective importance (required for Off Track items)"
                                ]
                            ),
                            html.Div(
                                style={'fontSize': '11px', 'color': '#475569', 'marginBottom': '4px'},
                                children=[
                                    html.Span("Action Items & Due Date: ", style={'fontWeight': '700'}),
                                    "Required for any At Risk or Off Track objectives - document corrective actions"
                                ]
                            ),
                            html.Div(
                                style={'fontSize': '11px', 'color': '#64748b', 'marginTop': '8px', 'paddingTop': '8px', 'borderTop': '1px solid #e2e8f0'},
                                children=[
                                    html.Span("Last Updated: ", style={'fontWeight': '600'}),
                                    html.Span(f"*Current Achievement can be manually entered or linked from Achievement_Records sheet", style={'color': '#475569'}),
                                    html.Span(" | ", style={'color': '#e2e8f0'}),
                                    html.Span("Last Updated Date: ", style={'fontWeight': '600'}),
                                    html.Span(datetime.now().strftime("%d-%b-%Y %H:%M"), style={'color': '#475569'})
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ========== DOCUMENT CONTROL INFORMATION ==========
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px 20px',
                    'border': '1px solid #e9ecef',
                    'marginTop': '16px',
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(6, 1fr)',
                    'gap': '12px'
                },
                children=[
                    html.Div([
                        html.Div("DOCUMENT OWNER:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("ADMINISTRATION", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("DOCUMENT ID:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("IMS/ADM/TMP/OBM/V2.0", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("CLASSIFICATION:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("INTERNAL USE ONLY", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#667eea', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("EFFECTIVE DATE:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("06-May-26", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("REVIEW CYCLE:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("Quarterly", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("NEXT REVIEW:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("05-Aug-26", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ])
                ]
            ),
            
            # ========== EVALUATION MODAL ==========
            html.Div(
                id="sysadmin-eval-modal",
                className="modal",
                style={"display": "none"},
                children=[
                    html.Div(
                        className="modal-content",
                        style={
                            'maxWidth': '600px',
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
                                    'padding': '16px 24px',
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
                                        id="sysadmin-eval-title",
                                        style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}
                                    ),
                                    html.I(
                                        className="fas fa-times",
                                        id="close-sysadmin-eval-modal",
                                        style={'cursor': 'pointer', 'color': '#94a3b8', 'fontSize': '20px', 'transition': 'all 0.3s ease'}
                                    )
                                ]
                            ),
                            
                            # Modal Body
                            html.Div(
                                style={'padding': '24px'},
                                children=[
                                    # Objective Info
                                    html.Div(
                                        id="sysadmin-eval-info",
                                        style={
                                            'background': '#f8fafc',
                                            'padding': '16px',
                                            'borderRadius': '10px',
                                            'marginBottom': '20px',
                                            'border': '1px solid #e2e8f0'
                                        }
                                    ),
                                    
                                    # Current Status
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Current Achievement*",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Input(
                                                id="sysadmin-eval-current-status",
                                                type="text",
                                                placeholder="Enter current achievement value",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Reviewed By
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Reviewed By",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Input(
                                                id="sysadmin-eval-reviewed-by",
                                                type="text",
                                                placeholder="Enter reviewer name",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Remarks
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Remarks (eg: Justification for not achieving)",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Textarea(
                                                id="sysadmin-eval-remarks",
                                                rows=3,
                                                placeholder="Enter any remarks...",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px', 'resize': 'vertical'}
                                            )
                                        ]
                                    ),
                                    
                                    # Calculation Result
                                    html.Div(
                                        id="sysadmin-calc-result",
                                        style={
                                            'background': '#f8fafc',
                                            'padding': '16px',
                                            'borderRadius': '10px',
                                            'marginTop': '10px',
                                            'border': '1px solid #e2e8f0'
                                        }
                                    )
                                ]
                            ),
                            
                            # Modal Footer
                            html.Div(
                                style={
                                    'padding': '16px 24px',
                                    'borderTop': '1px solid #eef2f6',
                                    'display': 'flex',
                                    'justifyContent': 'flex-end',
                                    'gap': '12px',
                                    'position': 'sticky',
                                    'bottom': '0',
                                    'background': 'white',
                                    'zIndex': '10',
                                    'borderRadius': '0 0 16px 16px'
                                },
                                children=[
                                    html.Button(
                                        "Cancel",
                                        id="cancel-sysadmin-eval-modal",
                                        style={
                                            'padding': '8px 20px',
                                            'background': '#f1f5f9',
                                            'border': '1px solid #e2e8f0',
                                            'borderRadius': '8px',
                                            'cursor': 'pointer',
                                            'fontWeight': '500',
                                            'fontSize': '14px',
                                            'color': '#64748b',
                                            'transition': 'all 0.3s ease'
                                        }
                                    ),
                                    html.Button(
                                        "Save",
                                        id="save-sysadmin-evaluation",
                                        style={
                                            'padding': '8px 24px',
                                            'background': 'linear-gradient(135deg, #667eea, #764ba2)',
                                            'color': 'white',
                                            'border': 'none',
                                            'borderRadius': '8px',
                                            'cursor': 'pointer',
                                            'fontWeight': '500',
                                            'fontSize': '14px',
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
                    
                    #cancel-sysadmin-eval-modal:hover {
                        background: #e2e8f0;
                    }
                    
                    #save-sysadmin-evaluation:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    }
                    
                    #close-sysadmin-eval-modal:hover {
                        color: #ef4444;
                        transform: rotate(90deg);
                    }
                </style>
                """, dangerously_allow_html=True)
            ]),
            
            # Success Toast
            html.Div(
                id="sysadmin-success-toast",
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'bottom': '20px',
                    'right': '20px',
                    'background': '#10b981',
                    'color': 'white',
                    'padding': '12px 20px',
                    'borderRadius': '10px',
                    'zIndex': '10000',
                    'fontSize': '14px',
                    'fontWeight': '500',
                    'boxShadow': '0 8px 25px rgba(16, 185, 129, 0.3)'
                },
                children="Saved successfully!"
            ),
            
            # Stores
            dcc.Store(id="sysadmin-objectives-store", data=objectives),
            dcc.Store(id="sysadmin-selected-id", data=None),
            dcc.Store(id="sysadmin-page-loaded", data=0),
            dcc.Store(id="sysadmin-modal-trigger", data=0)
        ]
    )


def register_sysadmin_callbacks(app):
    """Register callbacks for System Admin page"""
    
    @app.callback(
        Output("sysadmin-page-loaded", "data"),
        Input("sysadmin-table-body", "children"),
        prevent_initial_call=True
    )
    def set_page_loaded(children):
        return 1
    
    @app.callback(
        Output("sysadmin-table-body", "children"),
        [Input("sysadmin-objectives-store", "data"),
         Input("sysadmin-search-input", "value")]
    )
    def update_table(objectives, search_term):
        if not objectives:
            return [html.Tr(html.Td("No objectives found", colSpan=18, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        filtered = objectives.copy()
        if search_term:
            search_lower = search_term.lower()
            filtered = [o for o in filtered if 
                       search_lower in str(o.get('objective_id', '')).lower() or 
                       search_lower in str(o.get('objective', '')).lower() or
                       search_lower in str(o.get('category', '')).lower()]
        
        rows = []
        for obj in filtered:
            # Status Dropdown with 4 options
            status_options = [
                {"label": "On Track", "value": "On Track"},
                {"label": "At Risk", "value": "At Risk"},
                {"label": "Off Track", "value": "Off Track"},
                {"label": "Not Started", "value": "Not Started"}
            ]
            
            current_status = obj.get('status', 'Not Started')
            
            status_dropdown = dcc.Dropdown(
                id={"type": "sysadmin-status-dropdown", "index": obj.get('objective_id', 'ADM-01')},
                options=status_options,
                value=current_status,
                clearable=False,
                style={
                    'width': '120px',
                    'fontSize': '11px',
                    'border': 'none',
                    'backgroundColor': 'transparent',
                    'minHeight': '30px'
                },
                className="status-dropdown"
            )
            
            obj_text = str(obj.get('objective', '')) if obj.get('objective') else ''
            obj_display = obj_text[:50] + "..." if len(obj_text) > 50 else obj_text if obj_text else ''
            
            # Trend indicator
            trend = obj.get('trend', '')
            if "Improving" in str(trend):
                trend_color = "#10b981"
                trend_display = "↑ Improving"
            elif "Declining" in str(trend):
                trend_color = "#ef4444"
                trend_display = "↓ Declining"
            else:
                trend_color = "#94a3b8"
                trend_display = "→ Stable"
            
            # Variance
            variance = obj.get('variance', '')
            if variance and variance != '':
                try:
                    v = float(str(variance).replace('%', ''))
                    variance_color = "#10b981" if v >= 0 else "#ef4444"
                    variance_text = f"{v}%" if '%' not in str(variance) else str(variance)
                except:
                    variance_text = str(variance)
                    variance_color = "#94a3b8"
            else:
                variance_text = ""
                variance_color = "#94a3b8"
            
            evaluate_btn = html.Button(
                "Evaluate",
                id={"type": "sysadmin-evaluate", "index": obj.get('objective_id', 'ADM-01')},
                style={'padding': '4px 12px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '500'}
            )
            
            # Helper function - show empty string for empty values
            def get_value(val):
                if val is None or val == "":
                    return ""
                return str(val)
            
            # Objective ID - always show the value
            objective_id_value = obj.get('objective_id', '')
            
            rows.append(html.Tr([
                html.Td(objective_id_value, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': '#1e293b'}),
                html.Td(get_value(obj.get('category', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(obj_display, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(get_value(obj.get('kpi', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(get_value(obj.get('target', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '500', 'textAlign': 'center'}),
                html.Td(get_value(obj.get('timeline', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(get_value(obj.get('responsible', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(get_value(obj.get('previous_achievement', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(get_value(obj.get('current_achievement', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '500', 'textAlign': 'center'}),
                html.Td(variance_text, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': variance_color, 'textAlign': 'center'}),
                html.Td(trend_display, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': trend_color, 'textAlign': 'center'}),
                html.Td(status_dropdown, style={'padding': '4px 6px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'verticalAlign': 'middle'}),
                html.Td("View", style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#667eea', 'textAlign': 'center', 'cursor': 'pointer'}),
                html.Td(get_value(obj.get('evidence_location', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(get_value(obj.get('review_date', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(get_value(obj.get('reviewed_by', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(get_value(obj.get('remarks', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#64748b'}),
                html.Td(evaluate_btn, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'})
            ]))
        
        if not rows:
            rows = [html.Tr(html.Td("No matching objectives", colSpan=18, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        return rows
    
    # Callback to update status from dropdown
    @app.callback(
        Output("sysadmin-objectives-store", "data", allow_duplicate=True),
        Input({"type": "sysadmin-status-dropdown", "index": ALL}, "value"),
        State("sysadmin-objectives-store", "data"),
        prevent_initial_call=True
    )
    def update_status_dropdown(values, objectives):
        if not objectives or not values:
            return objectives
        
        ctx = callback_context
        if not ctx.triggered:
            return objectives
        
        trigger_id = ctx.triggered[0]["prop_id"]
        match = re.search(r'"index":"([^"]+)"', trigger_id)
        if not match:
            return objectives
        
        obj_key = match.group(1)
        new_value = values[0] if values else None
        
        if new_value:
            updated = objectives.copy()
            for obj in updated:
                if obj.get('objective_id') == obj_key:
                    obj['status'] = new_value
                    obj['review_date'] = datetime.now().strftime("%d-%m-%Y")
                    break
            return updated
        
        return objectives
    
    @app.callback(
        Output("sysadmin-modal-trigger", "data"),
        [Input({"type": "sysadmin-evaluate", "index": ALL}, "n_clicks")],
        [State("sysadmin-page-loaded", "data")],
        prevent_initial_call=True
    )
    def set_trigger(clicks, page_loaded):
        if page_loaded:
            ctx = callback_context
            if ctx.triggered:
                trigger_id = ctx.triggered[0]["prop_id"]
                if "sysadmin-evaluate" in trigger_id:
                    match = re.search(r'"index":"([^"]+)"', trigger_id)
                    if match:
                        return match.group(1)
        return None
    
    @app.callback(
        [Output("sysadmin-eval-modal", "style"),
         Output("sysadmin-eval-title", "children"),
         Output("sysadmin-eval-info", "children"),
         Output("sysadmin-selected-id", "data"),
         Output("sysadmin-eval-current-status", "value"),
         Output("sysadmin-eval-reviewed-by", "value"),
         Output("sysadmin-eval-remarks", "value")],
        [Input("sysadmin-modal-trigger", "data"),
         Input("close-sysadmin-eval-modal", "n_clicks"),
         Input("cancel-sysadmin-eval-modal", "n_clicks")],
        [State("sysadmin-objectives-store", "data"),
         State("sysadmin-page-loaded", "data")],
        prevent_initial_call=True
    )
    def open_modal(trigger_id, close_clicks, cancel_clicks, objectives, page_loaded):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, "", html.Div(), None, None, None, None
        
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if trigger in ["close-sysadmin-eval-modal", "cancel-sysadmin-eval-modal"]:
            return {"display": "none"}, "", html.Div(), None, None, None, None
        
        if trigger == "sysadmin-modal-trigger" and page_loaded and trigger_id:
            for obj in objectives:
                if obj.get('objective_id') == trigger_id:
                    info = html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '8px', 'fontSize': '13px'},
                        children=[
                            html.Div([html.Strong("ID: ", style={'color': '#64748b'}), html.Span(str(obj.get('objective_id', '')), style={'fontWeight': '500', 'color': '#1e293b'})]),
                            html.Div([html.Strong("Category: ", style={'color': '#64748b'}), html.Span(str(obj.get('category', '')), style={'fontWeight': '500', 'color': '#1e293b'})]),
                            html.Div([html.Strong("Target: ", style={'color': '#64748b'}), html.Span(str(obj.get('target', '')), style={'fontWeight': '500', 'color': '#1e293b'})]),
                            html.Div([html.Strong("Current Status: ", style={'color': '#64748b'}), html.Span(str(obj.get('status', 'Not Started')), style={'fontWeight': '500', 'color': '#1e293b'})])
                        ]
                    )
                    return {"display": "flex"}, f"Evaluate: {obj.get('objective_id', '')}", info, obj.get('objective_id'), obj.get('current_achievement', ''), None, None
        
        return {"display": "none"}, "", html.Div(), None, None, None, None
    
    @app.callback(
        [Output("sysadmin-eval-current-status", "value", allow_duplicate=True),
         Output("sysadmin-eval-reviewed-by", "value", allow_duplicate=True),
         Output("sysadmin-eval-remarks", "value", allow_duplicate=True),
         Output("sysadmin-modal-trigger", "data", allow_duplicate=True)],
        [Input("close-sysadmin-eval-modal", "n_clicks"),
         Input("cancel-sysadmin-eval-modal", "n_clicks")],
        prevent_initial_call=True
    )
    def clear_modal_inputs(close_clicks, cancel_clicks):
        return None, None, None, None
    
    @app.callback(
        Output("sysadmin-calc-result", "children"),
        Input("sysadmin-eval-current-status", "value"),
        State("sysadmin-selected-id", "data"),
        State("sysadmin-objectives-store", "data")
    )
    def calculate_result(current_status, obj_key, objectives):
        if not current_status or not obj_key or not objectives:
            return html.Div()
        
        obj = next((o for o in objectives if o.get('objective_id') == obj_key), None)
        if not obj:
            return html.Div()
        
        target = obj.get('target', '')
        
        return html.Div(
            style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '10px', 'fontSize': '13px'},
            children=[
                html.Div([html.Span("Target Value:", style={'color': '#64748b'}), html.Strong(f" {target}", style={'color': '#1e293b', 'marginLeft': '5px'})]),
                html.Div([html.Span("Updated Status:", style={'color': '#64748b'}), html.Strong(f" {current_status}", style={'color': '#667eea', 'marginLeft': '5px'})])
            ]
        )
    
    @app.callback(
        [Output("sysadmin-eval-modal", "style", allow_duplicate=True),
         Output("sysadmin-success-toast", "style"),
         Output("sysadmin-objectives-store", "data", allow_duplicate=True)],
        Input("save-sysadmin-evaluation", "n_clicks"),
        [State("sysadmin-selected-id", "data"),
         State("sysadmin-eval-current-status", "value"),
         State("sysadmin-eval-reviewed-by", "value"),
         State("sysadmin-eval-remarks", "value"),
         State("sysadmin-objectives-store", "data")],
        prevent_initial_call=True
    )
    def save_evaluation(n_clicks, obj_key, current_status, reviewed_by, remarks, objectives):
        if not n_clicks or not obj_key:
            return {"display": "none"}, {"display": "none"}, objectives
        
        updated_objectives = objectives.copy()
        for obj in updated_objectives:
            if obj.get('objective_id') == obj_key:
                if current_status:
                    obj['current_achievement'] = current_status
                if reviewed_by:
                    obj['reviewed_by'] = reviewed_by
                if remarks:
                    obj['remarks'] = remarks
                obj['review_date'] = datetime.now().strftime("%d-%m-%Y")
                break
        
        time.sleep(0.5)
        
        return {"display": "none"}, {"display": "flex", 'position': 'fixed', 'bottom': '20px', 'right': '20px', 'zIndex': '10000', 'background': '#10b981', 'color': 'white', 'padding': '12px 20px', 'borderRadius': '10px', 'alignItems': 'center', 'gap': '10px', 'fontWeight': '500', 'boxShadow': '0 8px 25px rgba(16, 185, 129, 0.3)'}, updated_objectives
    
    @app.callback(
        Output("sysadmin-success-toast", "style", allow_duplicate=True),
        Input("sysadmin-success-toast", "style"),
        prevent_initial_call=True
    )
    def hide_toast(style):
        time.sleep(3)
        return {"display": "none"}