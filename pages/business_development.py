# pages/business_development.py - Business Development Page with Database Data

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from dash.dependencies import ALL
import datetime
import json
import re
import base64
import time
from database import (
    get_all_bd_objectives, 
    save_bd_evaluation_with_evidence,
    get_finance_years, 
    get_finance_amount_by_year,
    save_evidence,
    add_missing_columns
)

def business_development_page():
    objectives = get_all_bd_objectives()
    finance_years = get_finance_years()
    
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
                        "Business Development Directives Monitoring Table",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Track and monitor Business Development objectives and directives",
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
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(6, 1fr)',
                    'gap': '12px',
                    'marginBottom': '20px'
                },
                children=[
                    # Total
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center',
                            'borderTop': '4px solid #667eea'
                        },
                        children=[
                            html.Div(
                                str(total),
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#667eea'}
                            ),
                            html.Div(
                                "Total Objectives",
                                style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'}
                            )
                        ]
                    ),
                    # On Track
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center',
                            'borderTop': '4px solid #10b981'
                        },
                        children=[
                            html.Div(
                                str(on_track),
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#10b981'}
                            ),
                            html.Div(
                                "On Track",
                                style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'}
                            )
                        ]
                    ),
                    # At Risk
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center',
                            'borderTop': '4px solid #eab308'
                        },
                        children=[
                            html.Div(
                                str(at_risk),
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#eab308'}
                            ),
                            html.Div(
                                "At Risk",
                                style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'}
                            )
                        ]
                    ),
                    # Off Track
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center',
                            'borderTop': '4px solid #dc2626'
                        },
                        children=[
                            html.Div(
                                str(off_track),
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#dc2626'}
                            ),
                            html.Div(
                                "Off Track",
                                style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'}
                            )
                        ]
                    ),
                    # Attention Needed
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center',
                            'borderTop': '4px solid #f59e0b'
                        },
                        children=[
                            html.Div(
                                str(attention_needed),
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#f59e0b'}
                            ),
                            html.Div(
                                "Attention Needed",
                                style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'}
                            )
                        ]
                    ),
                    # Not Started
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center',
                            'borderTop': '4px solid #94a3b8'
                        },
                        children=[
                            html.Div(
                                str(not_started),
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#94a3b8'}
                            ),
                            html.Div(
                                "Not Started",
                                style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '4px'}
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
                    # Table Title
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
                                "BUSINESS DEVELOPMENT DIRECTIVES MONITORING TABLE",
                                style={'margin': '0', 'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.Div(
                                style={'display': 'flex', 'gap': '10px'},
                                children=[
                                    dcc.Input(
                                        id="bd-search-input",
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
                        id="bd-table-container",
                        style={'overflowX': 'auto'},
                        children=[
                            html.Table(
                                id="bd-table",
                                style={
                                    'width': '100%', 
                                    'borderCollapse': 'collapse',
                                    'fontSize': '12px',
                                    'minWidth': '1400px'
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
                                    html.Tbody(id="bd-table-body")
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
                                        "Review must sign off on each review cycle"
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
                                    "Auto-calibrated difference between Current Achievement and Target (positive = exceeding, negative = below)"
                                ]
                            ),
                            html.Div(
                                style={'fontSize': '11px', 'color': '#475569', 'marginBottom': '4px'},
                                children=[
                                    html.Span("Trend: ", style={'fontWeight': '700'}),
                                    "Auto-calibrated comparison between Previous and Current Achievement (↑ Improving, ↓ Declining, → Stable)"
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
                                style={'fontSize': '11px', 'color': '#475569'},
                                children=[
                                    html.Span("Action Items & Due Date: ", style={'fontWeight': '700'}),
                                    "Required for any At Risk or Off Track objectives - document corrective actions"
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
                        html.Div("BUSINESS DEVELOPMENT", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("DOCUMENT ID:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("BD/JHR/TMP/OBM/V3.0", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("CLASSIFICATION:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("INTERNAL USE ONLY", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#667eea', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("EFFECTIVE DATE:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("08-May-28", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("REVIEW CYCLE:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("Quarterly", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("NEXT REVIEW:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("05-Aug-28", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ])
                ]
            ),
            
            # ========== EVALUATION MODAL ==========
            html.Div(
                id="bd-eval-modal",
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
                                        id="eval-modal-title",
                                        style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}
                                    ),
                                    html.I(
                                        className="fas fa-times",
                                        id="close-eval-modal",
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
                                        id="eval-objective-info",
                                        style={
                                            'background': '#f8fafc',
                                            'padding': '16px',
                                            'borderRadius': '10px',
                                            'marginBottom': '20px',
                                            'border': '1px solid #e2e8f0'
                                        }
                                    ),
                                    
                                    # Financial Year
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Financial Year",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Dropdown(
                                                id="eval-year-select",
                                                options=[{"label": year, "value": year} for year in finance_years] if finance_years else [{"label": "2024-25", "value": "2024-25"}, {"label": "2025-26", "value": "2025-26"}, {"label": "2026-27", "value": "2026-27"}],
                                                placeholder="Select year",
                                                style={'borderRadius': '8px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Actual Achievement
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Actual Achievement",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Input(
                                                id="eval-data-entry",
                                                type="number",
                                                placeholder="Enter value",
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
                                                id="eval-reviewed-by",
                                                type="text",
                                                placeholder="Enter name",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Upload Evidence
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Upload Evidence",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Upload(
                                                id="eval-evidence",
                                                style={
                                                    'border': '2px dashed #e2e8f0',
                                                    'borderRadius': '8px',
                                                    'padding': '16px',
                                                    'textAlign': 'center',
                                                    'background': '#fafbff',
                                                    'cursor': 'pointer',
                                                    'transition': 'all 0.3s ease'
                                                },
                                                children=html.Div([
                                                    html.I(className="fas fa-cloud-upload-alt", style={'fontSize': '24px', 'color': '#667eea'}),
                                                    html.Div("Click or drag to upload", style={'marginTop': '6px', 'color': '#64748b', 'fontSize': '13px'})
                                                ])
                                            ),
                                            html.Div(id="eval-evidence-name", style={'fontSize': '12px', 'marginTop': '6px', 'color': '#10b981'})
                                        ]
                                    ),
                                    
                                    # Evidence Description
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Evidence Description",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Input(
                                                id="eval-evidence-text",
                                                type="text",
                                                placeholder="Enter description",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Remarks
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Remarks",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Textarea(
                                                id="eval-remarks",
                                                rows=3,
                                                placeholder="Enter remarks...",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px', 'resize': 'vertical'}
                                            )
                                        ]
                                    ),
                                    
                                    # Calculation Result
                                    html.Div(
                                        id="calc-result",
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
                                        id="cancel-eval-modal",
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
                                        "Save Evaluation",
                                        id="save-evaluation",
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
                    
                    #cancel-eval-modal:hover {
                        background: #e2e8f0;
                    }
                    
                    #save-evaluation:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    }
                    
                    #close-eval-modal:hover {
                        color: #ef4444;
                        transform: rotate(90deg);
                    }
                </style>
                """, dangerously_allow_html=True)
            ]),
            
            # Evidence View Modal
            html.Div(
                id="evidence-view-modal",
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
                                    'zIndex': '10'
                                },
                                children=[
                                    html.H2("View Evidence", style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700'}),
                                    html.I(className="fas fa-times", id="close-evidence-modal", style={'cursor': 'pointer', 'color': '#94a3b8'})
                                ]
                            ),
                            html.Div(id="evidence-content", style={'padding': '20px'})
                        ]
                    )
                ]
            ),
            
            # Success Toast
            html.Div(
                id="success-toast",
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
            dcc.Store(id="bd-objectives-store", data=objectives),
            dcc.Store(id="selected-objective-id", data=None),
            dcc.Store(id="selected-evidence-data", data=None),
            dcc.Store(id="bd-table-toggle", data=False)
        ]
    )


def register_bd_callbacks(app):
    """Register callbacks for Business Development page"""
    
    @app.callback(
        Output("bd-table-body", "children"),
        [Input("bd-objectives-store", "data"),
         Input("bd-search-input", "value")]
    )
    def update_table(objectives, search_term):
        if not objectives:
            return [html.Tr(html.Td("No objectives found", colSpan=18, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        filtered = objectives.copy()
        if search_term:
            search_lower = search_term.lower()
            filtered = [o for o in filtered if 
                       search_lower in str(o.get('objective_id', '')).lower() or 
                       search_lower in str(o.get('objective', '')).lower()]
        
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
                id={"type": "bd-status-dropdown", "index": obj.get('id', 0)},
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
            if "Improving" in str(trend) or "↑" in str(trend):
                trend_color = "#10b981"
                trend_display = "↑ Improving"
            elif "Declining" in str(trend) or "↓" in str(trend):
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
                id={"type": "evaluate-bd", "index": obj.get('id', 0)},
                style={'padding': '4px 12px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '500'}
            )
            
            # Helper function - show empty string for empty values
            def get_value(val):
                if val is None or val == "":
                    return ""
                return str(val)
            
            rows.append(html.Tr([
                html.Td(get_value(obj.get('objective_id', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': '#1e293b'}),
                html.Td(get_value(obj.get('category', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(obj_display, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(get_value(obj.get('kpi', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(get_value(obj.get('target', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '500', 'textAlign': 'center'}),
                html.Td(get_value(obj.get('timeline', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(get_value(obj.get('responsible_personnel', '')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
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
        Output("bd-objectives-store", "data", allow_duplicate=True),
        Input({"type": "bd-status-dropdown", "index": ALL}, "value"),
        State("bd-objectives-store", "data"),
        prevent_initial_call=True
    )
    def update_status_dropdown(values, objectives):
        if not objectives or not values:
            return objectives
        
        ctx = callback_context
        if not ctx.triggered:
            return objectives
        
        trigger_id = ctx.triggered[0]["prop_id"]
        match = re.search(r'"index":(\d+)', trigger_id)
        if not match:
            return objectives
        
        obj_id = int(match.group(1))
        new_value = values[0] if values else None
        
        if new_value:
            updated = objectives.copy()
            for obj in updated:
                if obj.get('id') == obj_id:
                    obj['status'] = new_value
                    obj['review_date'] = datetime.datetime.now().strftime("%d-%m-%Y")
                    break
            return updated
        
        return objectives
    
    @app.callback(
        Output("eval-data-entry", "value", allow_duplicate=True),
        Input("eval-year-select", "value"),
        prevent_initial_call=True
    )
    def auto_fill_from_year(selected_year):
        if selected_year:
            amount = get_finance_amount_by_year(selected_year)
            return amount if amount else None
        return None
    
    @app.callback(
        Output("eval-evidence-name", "children"),
        Input("eval-evidence", "filename")
    )
    def show_uploaded_filename(filename):
        if filename:
            return html.Div([html.I(className="fas fa-check-circle", style={"color": "#10b981", "marginRight": "5px"}), filename], style={"fontSize": "11px"})
        return ""
    
    @app.callback(
        [Output("bd-eval-modal", "style"), 
         Output("eval-modal-title", "children"), 
         Output("eval-objective-info", "children"),
         Output("selected-objective-id", "data"), 
         Output("eval-data-entry", "value", allow_duplicate=True),
         Output("eval-reviewed-by", "value"), 
         Output("eval-remarks", "value"), 
         Output("eval-year-select", "value"),
         Output("eval-evidence", "contents"), 
         Output("eval-evidence", "filename"), 
         Output("eval-evidence-text", "value")],
        [Input({"type": "evaluate-bd", "index": ALL}, "n_clicks"), 
         Input("close-eval-modal", "n_clicks"), 
         Input("cancel-eval-modal", "n_clicks")],
        [State("bd-objectives-store", "data")], 
        prevent_initial_call=True
    )
    def open_eval_modal(eval_clicks, close_clicks, cancel_clicks, objectives):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, "", html.Div(), None, None, None, None, None, None, None, None
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id in ["close-eval-modal", "cancel-eval-modal"]:
            return {"display": "none"}, "", html.Div(), None, None, None, None, None, None, None, None
        if trigger_id and "evaluate-bd" in trigger_id:
            try:
                match = re.search(r'"index":(\d+)', trigger_id)
                obj_id = int(match.group(1)) if match else None
                if obj_id:
                    obj = next((o for o in objectives if o.get('id') == obj_id), None)
                    if obj:
                        info = html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "10px", "fontSize": "13px"}, children=[
                            html.Div([html.Strong("ID: "), html.Span(str(obj.get('objective_id', '')), style={"fontWeight": "500"})]),
                            html.Div([html.Strong("Target: "), html.Span(str(obj.get('target', '')), style={"fontWeight": "500"})]),
                            html.Div([html.Strong("Previous: "), html.Span(str(obj.get('previous_achievement', '')), style={"fontWeight": "500"})]),
                            html.Div([html.Strong("Timeline: "), html.Span(str(obj.get('timeline', '')), style={"fontWeight": "500"})])
                        ])
                        return {"display": "flex"}, f"Evaluate: {obj.get('objective_id', '')}", info, obj.get('id'), None, None, None, None, None, None, None
            except:
                pass
        return {"display": "none"}, "", html.Div(), None, None, None, None, None, None, None, None
    
    @app.callback(
        Output("calc-result", "children"),
        Input("eval-data-entry", "value"),
        State("selected-objective-id", "data"),
        State("bd-objectives-store", "data")
    )
    def calculate_result(data_entry, obj_id, objectives):
        if not data_entry or not obj_id or not objectives:
            return html.Div()
        obj = next((o for o in objectives if o.get('id') == obj_id), None)
        if not obj:
            return html.Div()
        previous = obj.get('previous_achievement', 0) or 0
        try:
            prev_val = float(str(previous).replace('%', '')) if previous else 0
        except:
            prev_val = 0
        actual = float(data_entry) if data_entry else 0
        if prev_val > 0:
            growth_rate = ((actual - prev_val) / prev_val) * 100
            percentage = (actual / prev_val) * 100
            if percentage < 70:
                status, color = "Not Achieved", "#dc2626"
            elif percentage < 100:
                status, color = "Partially Achieved", "#eab308"
            else:
                status, color = "Achieved", "#10b981"
        else:
            growth_rate, percentage = 0, 100 if actual > 0 else 0
            status, color = ("Achieved", "#10b981") if actual > 0 else ("Not Achieved", "#dc2626")
        return html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "10px", "fontSize": "13px"}, children=[
            html.Div([html.Span("Previous:", style={"color": "#64748b"}), html.Strong(f" {prev_val}", style={"color": "#1e293b", "marginLeft": "5px"})]),
            html.Div([html.Span("Actual:", style={"color": "#64748b"}), html.Strong(f" {actual}", style={"color": "#1e293b", "marginLeft": "5px"})]),
            html.Div([html.Span("Growth:", style={"color": "#64748b"}), html.Strong(f" {growth_rate:.1f}%", style={"color": "#667eea", "marginLeft": "5px"})]),
            html.Div([html.Span("Status:", style={"color": "#64748b"}), html.Strong(status, style={"color": color, "background": f"{color}15", "padding": "2px 10px", "borderRadius": "20px", "marginLeft": "8px"})])
        ])
    
    @app.callback(
        [Output("bd-eval-modal", "style", allow_duplicate=True), 
         Output("success-toast", "style"), 
         Output("bd-objectives-store", "data")],
        Input("save-evaluation", "n_clicks"),
        [State("selected-objective-id", "data"), 
         State("eval-data-entry", "value"), 
         State("eval-reviewed-by", "value"),
         State("eval-remarks", "value"), 
         State("eval-evidence", "filename"), 
         State("eval-evidence", "contents"),
         State("eval-evidence-text", "value"), 
         State("bd-objectives-store", "data")], 
        prevent_initial_call=True
    )
    def save_evaluation(n_clicks, obj_id, data_entry, reviewed_by, remarks, evidence_filename, evidence_contents, evidence_text, objectives):
        if not n_clicks or not obj_id:
            return {"display": "none"}, {"display": "none"}, objectives
        evidence_content = None
        final_filename = None
        if evidence_contents:
            parts = evidence_contents.split(',')
            if len(parts) > 1:
                evidence_content = base64.b64decode(parts[1])
                final_filename = evidence_filename
        success = save_bd_evaluation_with_evidence(obj_id, data_entry, reviewed_by, remarks, final_filename, evidence_content, evidence_text)
        if success:
            from database import get_all_bd_objectives
            return {"display": "none"}, {"display": "flex", "position": "fixed", "bottom": "20px", "right": "20px", "zIndex": "10000", "background": "#10b981", "color": "white", "padding": "12px 20px", "borderRadius": "10px", "alignItems": "center", "gap": "10px", "fontWeight": "500", "boxShadow": "0 8px 25px rgba(16, 185, 129, 0.3)"}, get_all_bd_objectives()
        return {"display": "none"}, {"display": "none"}, objectives
    
    @app.callback(
        [Output("evidence-view-modal", "style"), 
         Output("evidence-content", "children")],
        [Input({"type": "view-evidence", "index": ALL}, "n_clicks"), 
         Input("close-evidence-modal", "n_clicks")],
        [State("bd-objectives-store", "data")], 
        prevent_initial_call=True
    )
    def view_evidence(view_clicks, close_clicks, objectives):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, html.Div()
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "close-evidence-modal":
            return {"display": "none"}, html.Div()
        if trigger_id and "view-evidence" in trigger_id:
            try:
                match = re.search(r'"index":(\d+)', trigger_id)
                obj_id = int(match.group(1)) if match else None
                if obj_id:
                    obj = next((o for o in objectives if o.get('id') == obj_id), None)
                    if obj and (obj.get('evidence') or obj.get('evidence_text')):
                        content = []
                        if obj.get('evidence') and obj.get('evidence_filename'):
                            fname = obj.get('evidence_filename')
                            fcontent = obj.get('evidence')
                            ext = fname.split('.')[-1].lower() if fname else 'png'
                            content.append(html.H4("File Evidence:", style={"marginBottom": "10px", "fontSize": "14px", "fontWeight": "600"}))
                            if ext in ['jpg','jpeg','png','gif','webp']:
                                content.append(html.Img(src=f"data:image/{ext};base64,{fcontent}", style={"maxWidth": "100%", "borderRadius": "8px"}))
                            else:
                                content.append(html.A("Download File", href=f"data:application/octet-stream;base64,{fcontent}", download=fname, style={"color": "#667eea", "fontWeight": "500"}))
                        if obj.get('evidence_text'):
                            content.append(html.H4("Description:", style={"marginTop": "15px", "marginBottom": "8px", "fontSize": "14px", "fontWeight": "600"}))
                            content.append(html.Div(obj.get('evidence_text'), style={"background": "#f8fafc", "padding": "12px", "borderLeft": "3px solid #667eea", "borderRadius": "6px", "fontSize": "13px"}))
                        if not content:
                            content = [html.P("No evidence available", style={"color": "#94a3b8", "textAlign": "center", "padding": "20px"})]
                        return {"display": "flex"}, html.Div(content)
            except:
                pass
        return {"display": "none"}, html.Div()
    
    @app.callback(
        Output("success-toast", "style", allow_duplicate=True),
        Input("success-toast", "style"),
        prevent_initial_call=True
    )
    def hide_toast(style):
        time.sleep(3)
        return {"display": "none"}