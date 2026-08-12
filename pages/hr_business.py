# pages/hr_business.py - HR Business Page with HR Directives Monitoring Table

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from dash.dependencies import ALL
from datetime import datetime
import json
import re
import base64
import time
from database import (
    get_all_hr_objectives,
    save_hr_evaluation_with_evidence,
    get_hr_finance_years,
    get_hr_finance_amount_by_year
)

def hr_business_page():
    """HR Business Page - HR Directives Monitoring"""
    objectives = get_all_hr_objectives()
    finance_years = get_hr_finance_years()
    
    # Calculate statistics
    total = len(objectives)
    on_track = len([o for o in objectives if o.get('status') == 'On Track'])
    at_risk = len([o for o in objectives if o.get('status') == 'At Risk'])
    off_track = len([o for o in objectives if o.get('status') == 'Off Track'])
    not_started = len([o for o in objectives if o.get('status') == 'Not Started'])
    
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
                        "HR Directives Monitoring Table",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Track and monitor HR objectives and directives",
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
                    # Completion Rate
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #e9ecef',
                            'textAlign': 'center'
                        },
                        children=[
                            html.Div(
                                "57%",
                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#667eea'}
                            ),
                            html.Div(
                                "Completion Rate",
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
                    ),
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
                                "HR DIRECTIVES MONITORING TABLE",
                                style={'margin': '0', 'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.Div(
                                style={'display': 'flex', 'gap': '10px'},
                                children=[
                                    dcc.Input(
                                        id="hr-search-input",
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
                        id="hr-table-container",
                        style={'overflowX': 'auto'},
                        children=[
                            html.Table(
                                id="hr-table",
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
                                            html.Th("Current Achievement", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
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
                                    html.Tbody(id="hr-table-body")
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
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '16px'
                },
                children=[
                    html.Div([
                        html.Div("DOCUMENT OWNER:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("HUMAN RESOURCE", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("DOCUMENT ID:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("HMS/JHR/TMP/OBM/V3.0", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
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
                id="hr-eval-modal",
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
                                        id="hr-eval-modal-title",
                                        style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}
                                    ),
                                    html.I(
                                        className="fas fa-times",
                                        id="close-hr-eval-modal",
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
                                        id="hr-eval-objective-info",
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
                                                id="hr-eval-year-select",
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
                                                id="hr-eval-data-entry",
                                                type="number",
                                                placeholder="Enter value",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px'}
                                            )
                                        ]
                                    ),
                                    
                                    # Status Dropdown
                                    html.Div(
                                        style={'marginBottom': '16px'},
                                        children=[
                                            html.Label(
                                                "Objective Status",
                                                style={'fontSize': '13px', 'marginBottom': '6px', 'display': 'block', 'fontWeight': '600', 'color': '#1e293b'}
                                            ),
                                            dcc.Dropdown(
                                                id="hr-eval-status-dropdown",
                                                options=[
                                                    {"label": "On Track", "value": "On Track"},
                                                    {"label": "At Risk", "value": "At Risk"},
                                                    {"label": "Off Track", "value": "Off Track"},
                                                    {"label": "Not Started", "value": "Not Started"}
                                                ],
                                                placeholder="Select status",
                                                style={'borderRadius': '8px'}
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
                                                id="hr-eval-reviewed-by",
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
                                                id="hr-eval-evidence",
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
                                            html.Div(id="hr-eval-evidence-name", style={'fontSize': '12px', 'marginTop': '6px', 'color': '#10b981'})
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
                                                id="hr-eval-evidence-text",
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
                                                id="hr-eval-remarks",
                                                rows=3,
                                                placeholder="Enter remarks...",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px', 'resize': 'vertical'}
                                            )
                                        ]
                                    ),
                                    
                                    # Calculation Result
                                    html.Div(
                                        id="hr-calc-result",
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
                                        id="cancel-hr-eval-modal",
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
                                        id="save-hr-evaluation",
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
                    
                    #cancel-hr-eval-modal:hover {
                        background: #e2e8f0;
                    }
                    
                    #save-hr-evaluation:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    }
                    
                    #close-hr-eval-modal:hover {
                        color: #ef4444;
                        transform: rotate(90deg);
                    }
                </style>
                """, dangerously_allow_html=True)
            ]),
            
            # Evidence View Modal
            html.Div(
                id="hr-evidence-view-modal",
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
                                    html.I(className="fas fa-times", id="close-hr-evidence-modal", style={'cursor': 'pointer', 'color': '#94a3b8'})
                                ]
                            ),
                            html.Div(id="hr-evidence-content", style={'padding': '20px'})
                        ]
                    )
                ]
            ),
            
            # Success Toast
            html.Div(
                id="hr-success-toast",
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
                children="✓ Saved successfully!"
            ),
            
            # Stores
            dcc.Store(id="hr-objectives-store", data=objectives),
            dcc.Store(id="hr-selected-objective-id", data=None),
            dcc.Store(id="hr-modal-trigger", data=0),
            dcc.Store(id="hr-page-loaded", data=0)
        ]
    )


def register_hr_business_callbacks(app):
    """Register callbacks for HR Business page"""
    
    @app.callback(
        Output("hr-page-loaded", "data"),
        Input("hr-table-body", "children"),
        prevent_initial_call=True
    )
    def set_page_loaded(children):
        return 1
    
    @app.callback(
        Output("hr-table-body", "children"),
        [Input("hr-objectives-store", "data"),
         Input("hr-search-input", "value")]
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
            # Status dropdown
            status_options = [
                {"label": "On Track", "value": "On Track"},
                {"label": "At Risk", "value": "At Risk"},
                {"label": "Off Track", "value": "Off Track"},
                {"label": "Not Started", "value": "Not Started"}
            ]
            
            current_status = obj.get('status', 'Not Started')
            
            status_dropdown = dcc.Dropdown(
                id={"type": "status-dropdown", "index": obj.get('objective_id', 'HR-01')},
                options=status_options,
                value=current_status,
                clearable=False,
                style={
                    'width': '130px',
                    'fontSize': '11px',
                    'border': 'none',
                    'backgroundColor': 'transparent'
                },
                className="status-dropdown"
            )
            
            obj_text = str(obj.get('objective', '')) if obj.get('objective') else ''
            obj_display = obj_text[:50] + "..." if len(obj_text) > 50 else obj_text if obj_text else '-'
            
            # Trend indicator
            trend = obj.get('trend', '→ Stable')
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
            variance = obj.get('variance', '-')
            if variance and variance != '-':
                try:
                    v = float(str(variance).replace('%', ''))
                    variance_color = "#10b981" if v >= 0 else "#ef4444"
                    variance_text = f"{v}%" if '%' not in str(variance) else str(variance)
                except:
                    variance_text = str(variance)
                    variance_color = "#94a3b8"
            else:
                variance_text = "-"
                variance_color = "#94a3b8"
            
            evaluate_btn = html.Button(
                "Evaluate",
                id={"type": "evaluate-hr", "index": obj.get('objective_id', 'HR-01')},
                style={'padding': '4px 12px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '500'}
            )
            
            rows.append(html.Tr([
                html.Td(str(obj.get('objective_id', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': '#1e293b'}),
                html.Td(str(obj.get('category', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(obj_display, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(str(obj.get('kpi', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#1e293b'}),
                html.Td(str(obj.get('target', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '500', 'textAlign': 'center'}),
                html.Td(str(obj.get('timeline', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(str(obj.get('responsible_personnel', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(str(obj.get('previous_achievement', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(str(obj.get('current_achievement', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '500', 'textAlign': 'center'}),
                html.Td(variance_text, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': variance_color, 'textAlign': 'center'}),
                html.Td(trend_display, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'fontWeight': '600', 'color': trend_color, 'textAlign': 'center'}),
                html.Td(status_dropdown, style={'padding': '4px 6px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'verticalAlign': 'middle'}),
                html.Td("📄 View", style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#667eea', 'textAlign': 'center', 'cursor': 'pointer'}),
                html.Td(str(obj.get('evidence_location', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(str(obj.get('review_date', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(str(obj.get('reviewed_by', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(str(obj.get('remarks', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#64748b'}),
                html.Td(evaluate_btn, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'})
            ]))
        
        if not rows:
            rows = [html.Tr(html.Td("No matching objectives", colSpan=18, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        return rows

    @app.callback(
        Output("hr-objectives-store", "data", allow_duplicate=True),
        Input({"type": "status-dropdown", "index": ALL}, "value"),
        State("hr-objectives-store", "data"),
        prevent_initial_call=True
    )
    def update_status_dropdown(values, objectives):
        if not objectives or not values:
            return objectives
        
        # Get the triggered dropdown
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
            for obj in objectives:
                if obj.get('objective_id') == obj_key:
                    obj['status'] = new_value
                    obj['review_date'] = datetime.now().strftime("%d-%m-%Y")
                    break
        
        return objectives
    
    @app.callback(
        Output("hr-eval-data-entry", "value", allow_duplicate=True),
        Input("hr-eval-year-select", "value"),
        prevent_initial_call=True
    )
    def auto_fill_from_year(selected_year):
        if selected_year:
            # Sample data - in production, get from database
            return None
        return None
    
    @app.callback(
        Output("hr-eval-evidence-name", "children"),
        Input("hr-eval-evidence", "filename")
    )
    def show_uploaded_filename(filename):
        if filename:
            return html.Div([html.I(className="fas fa-check-circle", style={'color': '#10b981', 'marginRight': '6px'}), filename], style={'fontSize': '12px'})
        return ""
    
    @app.callback(
        Output("hr-modal-trigger", "data"),
        [Input({"type": "evaluate-hr", "index": ALL}, "n_clicks")],
        [State("hr-page-loaded", "data")],
        prevent_initial_call=True
    )
    def set_trigger(clicks, page_loaded):
        if page_loaded:
            ctx = callback_context
            if ctx.triggered:
                trigger_id = ctx.triggered[0]["prop_id"]
                if "evaluate-hr" in trigger_id:
                    match = re.search(r'"index":"([^"]+)"', trigger_id)
                    if match:
                        return match.group(1)
        return 0
    
    @app.callback(
        [Output("hr-eval-modal", "style"),
         Output("hr-eval-modal-title", "children"),
         Output("hr-eval-objective-info", "children"),
         Output("hr-selected-objective-id", "data"),
         Output("hr-eval-status-dropdown", "value")],
        [Input("hr-modal-trigger", "data"),
         Input("close-hr-eval-modal", "n_clicks"),
         Input("cancel-hr-eval-modal", "n_clicks")],
        [State("hr-objectives-store", "data"),
         State("hr-page-loaded", "data")],
        prevent_initial_call=True
    )
    def open_modal(trigger_id, close_clicks, cancel_clicks, objectives, page_loaded):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, "", html.Div(), None, None
        
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if trigger in ["close-hr-eval-modal", "cancel-hr-eval-modal"]:
            return {"display": "none"}, "", html.Div(), None, None
        
        if trigger == "hr-modal-trigger" and page_loaded and trigger_id:
            for obj in objectives:
                if obj.get('objective_id') == trigger_id:
                    info = html.Div(
                        style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '8px', 'fontSize': '13px'},
                        children=[
                            html.Div([html.Strong("ID: ", style={'color': '#64748b'}), html.Span(str(obj.get('objective_id', '')), style={'fontWeight': '500', 'color': '#1e293b'})]),
                            html.Div([html.Strong("Target: ", style={'color': '#64748b'}), html.Span(str(obj.get('target', '')), style={'fontWeight': '500', 'color': '#1e293b'})]),
                            html.Div([html.Strong("Previous: ", style={'color': '#64748b'}), html.Span(str(obj.get('previous_achievement', '-')), style={'fontWeight': '500', 'color': '#1e293b'})]),
                            html.Div([html.Strong("Current Status: ", style={'color': '#64748b'}), html.Span(str(obj.get('status', 'Not Started')), style={'fontWeight': '500', 'color': '#1e293b'})])
                        ]
                    )
                    return {"display": "flex"}, f"Evaluate: {obj.get('objective_id', '')}", info, obj.get('objective_id'), obj.get('status', 'Not Started')
        
        return {"display": "none"}, "", html.Div(), None, None
    
    @app.callback(
        [Output("hr-eval-data-entry", "value", allow_duplicate=True),
         Output("hr-eval-reviewed-by", "value", allow_duplicate=True),
         Output("hr-eval-remarks", "value", allow_duplicate=True),
         Output("hr-eval-year-select", "value", allow_duplicate=True),
         Output("hr-eval-evidence", "contents", allow_duplicate=True),
         Output("hr-eval-evidence", "filename", allow_duplicate=True),
         Output("hr-eval-evidence-text", "value", allow_duplicate=True),
         Output("hr-eval-status-dropdown", "value", allow_duplicate=True),
         Output("hr-modal-trigger", "data", allow_duplicate=True)],
        [Input("close-hr-eval-modal", "n_clicks"),
         Input("cancel-hr-eval-modal", "n_clicks")],
        prevent_initial_call=True
    )
    def clear_modal_inputs(close_clicks, cancel_clicks):
        return None, None, None, None, None, None, None, None, 0
    
    @app.callback(
        Output("hr-calc-result", "children"),
        Input("hr-eval-data-entry", "value"),
        State("hr-selected-objective-id", "data"),
        State("hr-objectives-store", "data")
    )
    def calculate_result(data_entry, obj_key, objectives):
        if not data_entry or not obj_key or not objectives:
            return html.Div()
        
        obj = None
        for o in objectives:
            if o.get('objective_id') == obj_key:
                obj = o
                break
        
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
            growth_rate = 0
            percentage = 100 if actual > 0 else 0
            status, color = ("Achieved", "#10b981") if actual > 0 else ("Not Achieved", "#dc2626")
        
        return html.Div(
            style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '10px', 'fontSize': '13px'},
            children=[
                html.Div([html.Span("Previous:", style={'color': '#64748b'}), html.Strong(f" {prev_val}", style={'color': '#1e293b', 'marginLeft': '5px'})]),
                html.Div([html.Span("Actual:", style={'color': '#64748b'}), html.Strong(f" {actual}", style={'color': '#1e293b', 'marginLeft': '5px'})]),
                html.Div([html.Span("Growth:", style={'color': '#64748b'}), html.Strong(f" {growth_rate:.1f}%", style={'color': '#667eea', 'marginLeft': '5px'})]),
                html.Div([html.Span("Status:", style={'color': '#64748b'}), html.Strong(status, style={'color': color, 'background': f"{color}15", 'padding': '2px 10px', 'borderRadius': '20px', 'marginLeft': '8px'})])
            ]
        )
    
    @app.callback(
        [Output("hr-eval-modal", "style", allow_duplicate=True),
         Output("hr-success-toast", "style"),
         Output("hr-objectives-store", "data", allow_duplicate=True)],
        Input("save-hr-evaluation", "n_clicks"),
        [State("hr-selected-objective-id", "data"),
         State("hr-eval-data-entry", "value"),
         State("hr-eval-reviewed-by", "value"),
         State("hr-eval-remarks", "value"),
         State("hr-eval-evidence", "filename"),
         State("hr-eval-evidence", "contents"),
         State("hr-eval-evidence-text", "value"),
         State("hr-eval-status-dropdown", "value"),
         State("hr-objectives-store", "data")],
        prevent_initial_call=True
    )
    def save_evaluation(n_clicks, obj_key, data_entry, reviewed_by, remarks, filename, contents, text, status, objectives):
        if not n_clicks or not obj_key:
            return {"display": "none"}, {"display": "none"}, objectives
        
        # Update the objective with new data
        updated_objectives = objectives.copy()
        for obj in updated_objectives:
            if obj.get('objective_id') == obj_key:
                # Update status from dropdown
                if status:
                    obj['status'] = status
                # Update other fields
                if data_entry:
                    obj['current_achievement'] = str(data_entry)
                if reviewed_by:
                    obj['reviewed_by'] = reviewed_by
                if remarks:
                    obj['remarks'] = remarks
                if text:
                    obj['evidence_location'] = text
                # Update review date
                obj['review_date'] = datetime.now().strftime("%d-%m-%Y")
                break
        
        # Simulate save
        time.sleep(0.5)
        
        # Return success
        return {"display": "none"}, {"display": "flex", 'position': 'fixed', 'bottom': '20px', 'right': '20px', 'zIndex': '10000', 'background': '#10b981', 'color': 'white', 'padding': '12px 20px', 'borderRadius': '10px', 'alignItems': 'center', 'gap': '10px', 'fontWeight': '500', 'boxShadow': '0 8px 25px rgba(16, 185, 129, 0.3)'}, updated_objectives
    
    @app.callback(
        Output("hr-success-toast", "style", allow_duplicate=True),
        Input("hr-success-toast", "style"),
        prevent_initial_call=True
    )
    def hide_toast(style):
        time.sleep(3)
        return {"display": "none"}