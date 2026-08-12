# pages/operation.py - Operation Page with HR Directives Style

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
import datetime
import json
import re
import base64
import time
from database import (
    get_all_operation_objectives,
    save_operation_evaluation_with_evidence,
    get_operation_finance_years,
    get_operation_finance_amount_by_year
)

def operation_page():
    objectives = get_all_operation_objectives()
    finance_years = get_operation_finance_years()
    
    # The 7 Operation Objectives
    operation_objectives_data = [
        {
            "id": 1,
            "objective_id": "OP-01",
            "category": "Production",
            "objective": "Increase production efficiency by 15%",
            "kpi": "Production efficiency rate",
            "target": "15%",
            "timeline": "Annual",
            "responsible_personnel": "",
            "previous_achievement": "12.0",
            "current_achievement": "14.5",
            "variance": "2.5",
            "trend": "↑ Improving",
            "status": "On Track",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        },
        {
            "id": 2,
            "objective_id": "OP-02",
            "category": "Quality",
            "objective": "Reduce defect rate to below 2%",
            "kpi": "Defect rate",
            "target": "2%",
            "timeline": "Quarterly",
            "responsible_personnel": "",
            "previous_achievement": "2.5",
            "current_achievement": "2.1",
            "variance": "0.4",
            "trend": "↑ Improving",
            "status": "On Track",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        },
        {
            "id": 3,
            "objective_id": "OP-03",
            "category": "Maintenance",
            "objective": "Reduce machine downtime by 20%",
            "kpi": "Machine downtime reduction",
            "target": "20%",
            "timeline": "Half Yearly",
            "responsible_personnel": "",
            "previous_achievement": "15.0",
            "current_achievement": "18.0",
            "variance": "3.0",
            "trend": "↑ Improving",
            "status": "On Track",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        },
        {
            "id": 4,
            "objective_id": "OP-04",
            "category": "Supply Chain",
            "objective": "Achieve 98% on-time delivery",
            "kpi": "On-time delivery rate",
            "target": "98%",
            "timeline": "Monthly",
            "responsible_personnel": "",
            "previous_achievement": "95.0",
            "current_achievement": "97.0",
            "variance": "2.0",
            "trend": "↑ Improving",
            "status": "On Track",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        },
        {
            "id": 5,
            "objective_id": "OP-05",
            "category": "Inventory",
            "objective": "Reduce inventory holding cost by 10%",
            "kpi": "Inventory cost reduction",
            "target": "10%",
            "timeline": "Annual",
            "responsible_personnel": "",
            "previous_achievement": "6.0",
            "current_achievement": "8.0",
            "variance": "2.0",
            "trend": "↑ Improving",
            "status": "At Risk",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        },
        {
            "id": 6,
            "objective_id": "OP-06",
            "category": "Safety",
            "objective": "Zero lost-time incidents",
            "kpi": "Lost-time incidents",
            "target": "0",
            "timeline": "Annual",
            "responsible_personnel": "",
            "previous_achievement": "1",
            "current_achievement": "0",
            "variance": "1",
            "trend": "↑ Improving",
            "status": "On Track",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        },
        {
            "id": 7,
            "objective_id": "OP-07",
            "category": "Sustainability",
            "objective": "Reduce energy consumption by 12%",
            "kpi": "Energy reduction rate",
            "target": "12%",
            "timeline": "Annual",
            "responsible_personnel": "",
            "previous_achievement": "8.0",
            "current_achievement": "10.0",
            "variance": "2.0",
            "trend": "↑ Improving",
            "status": "At Risk",
            "evidence": "",
            "evidence_location": "",
            "review_date": "",
            "reviewed_by": "",
            "remarks": ""
        }
    ]
    
    # Calculate statistics
    total = len(operation_objectives_data)
    on_track = len([o for o in operation_objectives_data if o.get('status') == 'On Track'])
    at_risk = len([o for o in operation_objectives_data if o.get('status') == 'At Risk'])
    attention_needed = 43
    not_started = 0
    
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
                        "Operation Directives Monitoring Table",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Track and monitor Operation objectives and directives",
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
                                "43%",
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
                                "0",
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
                                "OPERATION DIRECTIVES MONITORING TABLE",
                                style={'margin': '0', 'fontSize': '14px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.Div(
                                style={'display': 'flex', 'gap': '10px'},
                                children=[
                                    dcc.Input(
                                        id="operation-search-input",
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
                        id="operation-table-container",
                        style={'overflowX': 'auto'},
                        children=[
                            html.Table(
                                id="operation-table",
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
                                            html.Th("Objective Status", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Evidence", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Evidence Location", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Date of Review", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Reviewed By", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'whiteSpace': 'nowrap'}),
                                            html.Th("Remarks", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'minWidth': '120px'}),
                                            html.Th("Actions", style={'padding': '8px 10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontWeight': '700', 'background': '#f8fafc', 'fontSize': '11px', 'width': '80px'})
                                        ])
                                    ),
                                    html.Tbody(id="operation-table-body")
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
                                    html.Div(children=[
                                        html.Span("● ", style={'color': '#ef4444', 'fontWeight': '700'}),
                                        html.Span("Off Track (Red): ", style={'fontWeight': '600'}),
                                        html.Span("Achievement < Target by more than 5%", style={'fontSize': '11px', 'color': '#475569'})
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
                        html.Div("OPERATIONS", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
                    ]),
                    html.Div([
                        html.Div("DOCUMENT ID:", style={'fontSize': '10px', 'fontWeight': '700', 'color': '#94a3b8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.Div("OP/JHR/TMP/OBM/V3.0", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginTop': '4px'})
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
                id="operation-eval-modal",
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
                                        id="operation-eval-modal-title",
                                        style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}
                                    ),
                                    html.I(
                                        className="fas fa-times",
                                        id="close-operation-eval-modal",
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
                                        id="operation-eval-objective-info",
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
                                                id="operation-eval-year-select",
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
                                                id="operation-eval-data-entry",
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
                                                id="operation-eval-reviewed-by",
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
                                                id="operation-eval-evidence",
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
                                            html.Div(id="operation-eval-evidence-name", style={'fontSize': '12px', 'marginTop': '6px', 'color': '#10b981'})
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
                                                id="operation-eval-evidence-text",
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
                                                id="operation-eval-remarks",
                                                rows=3,
                                                placeholder="Enter remarks...",
                                                style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '14px', 'resize': 'vertical'}
                                            )
                                        ]
                                    ),
                                    
                                    # Calculation Result
                                    html.Div(
                                        id="operation-calc-result",
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
                                        id="cancel-operation-eval-modal",
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
                                        id="save-operation-evaluation",
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
                    
                    #cancel-operation-eval-modal:hover {
                        background: #e2e8f0;
                    }
                    
                    #save-operation-evaluation:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    }
                    
                    #close-operation-eval-modal:hover {
                        color: #ef4444;
                        transform: rotate(90deg);
                    }
                </style>
                """, dangerously_allow_html=True)
            ]),
            
            # Evidence View Modal
            html.Div(
                id="operation-evidence-view-modal",
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
                                    html.I(className="fas fa-times", id="close-operation-evidence-modal", style={'cursor': 'pointer', 'color': '#94a3b8'})
                                ]
                            ),
                            html.Div(id="operation-evidence-content", style={'padding': '20px'})
                        ]
                    )
                ]
            ),
            
            # Success Toast
            html.Div(
                id="operation-success-toast",
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
            dcc.Store(id="operation-objectives-store", data=operation_objectives_data),
            dcc.Store(id="operation-selected-objective-id", data=None),
            dcc.Store(id="operation-table-toggle", data=False)
        ]
    )


def register_operation_callbacks(app):
    
    @app.callback(
        [Output("operation-table-body", "children")],
        [Input("operation-objectives-store", "data"),
         Input("operation-search-input", "value")]
    )
    def update_table(objectives, search_term):
        if not objectives:
            return [[html.Tr(html.Td("No objectives found", colSpan=18, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]]
        
        filtered = objectives.copy()
        if search_term:
            search_lower = search_term.lower()
            filtered = [o for o in filtered if 
                       search_lower in str(o.get('objective_id', '')).lower() or 
                       search_lower in str(o.get('objective', '')).lower()]
        
        rows = []
        for obj in filtered:
            # Status badge styling
            status_colors = {
                "On Track": {"bg": "#ecfdf5", "color": "#10b981", "text": "On Track"},
                "At Risk": {"bg": "#fefce8", "color": "#eab308", "text": "At Risk"},
                "Off Track": {"bg": "#fef2f2", "color": "#dc2626", "text": "Off Track"}
            }
            status_val = obj.get('status', 'Pending')
            if status_val in status_colors:
                sc = status_colors[status_val]
                status_badge = html.Span(
                    sc["text"],
                    style={'background': sc["bg"], 'color': sc["color"], 'padding': '3px 10px', 'borderRadius': '20px', 'fontSize': '10px', 'fontWeight': '600', 'display': 'inline-block'}
                )
            else:
                status_badge = html.Span(
                    "Pending",
                    style={'background': '#f1f5f9', 'color': '#64748b', 'padding': '3px 10px', 'borderRadius': '20px', 'fontSize': '10px'}
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
                id={"type": "evaluate-operation", "index": obj.get('id', 0)},
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
                html.Td(status_badge, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}),
                html.Td("📄 View", style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#667eea', 'textAlign': 'center', 'cursor': 'pointer'}),
                html.Td(str(obj.get('evidence_location', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(str(obj.get('review_date', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'textAlign': 'center'}),
                html.Td(str(obj.get('reviewed_by', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px'}),
                html.Td(str(obj.get('remarks', '-')), style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'fontSize': '11px', 'color': '#64748b'}),
                html.Td(evaluate_btn, style={'padding': '6px 8px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'})
            ]))
        
        if not rows:
            rows = [html.Tr(html.Td("No matching objectives", colSpan=18, style={'textAlign': 'center', 'padding': '40px', 'color': '#94a3b8', 'fontSize': '13px'}))]
        
        return [rows]
    
    # Auto-fill
    @app.callback(Output("operation-eval-data-entry", "value", allow_duplicate=True), [Input("operation-eval-year-select", "value")], prevent_initial_call=True)
    def auto_fill(year):
        if year:
            return get_operation_finance_amount_by_year(year)
        return None
    
    @app.callback(Output("operation-eval-evidence-name", "children"), [Input("operation-eval-evidence", "filename")])
    def show_filename(fname):
        if fname:
            return html.Div([html.I(className="fas fa-check-circle", style={"color": "#10b981", "marginRight": "5px"}), fname], style={"fontSize": "11px"})
        return ""
    
    # Open modal
    @app.callback(
        [Output("operation-eval-modal", "style"), Output("operation-eval-modal-title", "children"), 
         Output("operation-eval-objective-info", "children"), Output("operation-selected-objective-id", "data"),
         Output("operation-eval-data-entry", "value", allow_duplicate=True), Output("operation-eval-reviewed-by", "value"),
         Output("operation-eval-remarks", "value"), Output("operation-eval-year-select", "value"),
         Output("operation-eval-evidence", "contents"), Output("operation-eval-evidence", "filename"),
         Output("operation-eval-evidence-text", "value")],
        [Input({"type": "evaluate-operation", "index": dash.dependencies.ALL}, "n_clicks"),
         Input("close-operation-eval-modal", "n_clicks"), Input("cancel-operation-eval-modal", "n_clicks")],
        [State("operation-objectives-store", "data")], prevent_initial_call=True
    )
    def open_modal(eval_clicks, close_clicks, cancel_clicks, objectives):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, "", html.Div(), None, None, None, None, None, None, None, None
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger in ["close-operation-eval-modal", "cancel-operation-eval-modal"]:
            return {"display": "none"}, "", html.Div(), None, None, None, None, None, None, None, None
        if trigger and "evaluate-operation" in trigger:
            try:
                match = re.search(r'"index":\s*(\d+)', trigger)
                obj_id = int(match.group(1)) if match else None
                if obj_id:
                    obj = next((o for o in objectives if o.get('id') == obj_id), None)
                    if obj:
                        info = html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "8px", "fontSize": "13px"}, children=[
                            html.Div([html.Strong("ID: ", style={"color": "#64748b"}), html.Span(str(obj.get('objective_id', '')), style={"fontWeight": "500", "color": "#1e293b"})]),
                            html.Div([html.Strong("Target: ", style={"color": "#64748b"}), html.Span(str(obj.get('target', '')), style={"fontWeight": "500", "color": "#1e293b"})]),
                            html.Div([html.Strong("Previous: ", style={"color": "#64748b"}), html.Span(str(obj.get('previous_achievement', '-')), style={"fontWeight": "500", "color": "#1e293b"})]),
                            html.Div([html.Strong("Timeline: ", style={"color": "#64748b"}), html.Span(str(obj.get('timeline', '')), style={"fontWeight": "500", "color": "#1e293b"})])
                        ])
                        return {"display": "flex"}, f"Evaluate: {obj.get('objective_id', '')}", info, obj.get('id'), None, None, None, None, None, None, None
            except:
                pass
        return {"display": "none"}, "", html.Div(), None, None, None, None, None, None, None, None
    
    # Calculate
    @app.callback(Output("operation-calc-result", "children"), [Input("operation-eval-data-entry", "value")],
                  [State("operation-selected-objective-id", "data"), State("operation-objectives-store", "data")])
    def calculate(actual, obj_id, objectives):
        if not actual or not obj_id or not objectives:
            return html.Div()
        obj = next((o for o in objectives if o.get('id') == obj_id), None)
        if not obj:
            return html.Div()
        previous = obj.get('previous_achievement', 0) or 0
        try:
            prev_val = float(str(previous).replace('%', '')) if previous else 0
        except:
            prev_val = 0
        actual = float(actual)
        if prev_val > 0:
            growth = ((actual - prev_val) / prev_val) * 100
            pct = (actual / prev_val) * 100
            if pct >= 100:
                status, color = "Achieved", "#10b981"
            elif pct >= 70:
                status, color = "Partially Achieved", "#eab308"
            else:
                status, color = "Not Achieved", "#dc2626"
        else:
            growth = 0
            status, color = ("Achieved", "#10b981") if actual > 0 else ("Not Achieved", "#dc2626")
        return html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "10px", "fontSize": "13px"}, children=[
            html.Div([html.Span("Previous:", style={"color": "#64748b"}), html.Strong(f" {prev_val}", style={"color": "#1e293b", "marginLeft": "5px"})]),
            html.Div([html.Span("Actual:", style={"color": "#64748b"}), html.Strong(f" {actual}", style={"color": "#1e293b", "marginLeft": "5px"})]),
            html.Div([html.Span("Growth:", style={"color": "#64748b"}), html.Strong(f" {growth:.1f}%", style={"color": "#667eea", "marginLeft": "5px"})]),
            html.Div([html.Span("Status:", style={"color": "#64748b"}), html.Strong(status, style={"color": color, "background": f"{color}15", "padding": "2px 10px", "borderRadius": "20px", "marginLeft": "8px"})])
        ])
    
    # Save
    @app.callback(
        [Output("operation-eval-modal", "style", allow_duplicate=True), Output("operation-success-toast", "style"), Output("operation-objectives-store", "data")],
        [Input("save-operation-evaluation", "n_clicks")],
        [State("operation-selected-objective-id", "data"), State("operation-eval-data-entry", "value"),
         State("operation-eval-reviewed-by", "value"), State("operation-eval-remarks", "value"),
         State("operation-eval-evidence", "filename"), State("operation-eval-evidence", "contents"),
         State("operation-eval-evidence-text", "value"), State("operation-objectives-store", "data")], prevent_initial_call=True
    )
    def save(n_clicks, obj_id, data_entry, reviewed_by, remarks, filename, contents, text, objectives):
        if not n_clicks or not obj_id:
            return {"display": "none"}, {"display": "none"}, objectives
        evidence_content = None
        if contents:
            parts = contents.split(',')
            if len(parts) > 1:
                evidence_content = base64.b64decode(parts[1])
        success = save_operation_evaluation_with_evidence(obj_id, data_entry, reviewed_by, remarks, filename, evidence_content, text)
        if success:
            from database import get_all_operation_objectives
            return {"display": "none"}, {"display": "flex", "position": "fixed", "bottom": "20px", "right": "20px", "background": "#10b981", "color": "white", "padding": "12px 20px", "borderRadius": "10px", "fontWeight": "500", "boxShadow": "0 8px 25px rgba(16, 185, 129, 0.3)"}, get_all_operation_objectives()
        return {"display": "none"}, {"display": "none"}, objectives
    
    # View evidence
    @app.callback(
        [Output("operation-evidence-view-modal", "style"), Output("operation-evidence-content", "children")],
        [Input({"type": "view-operation-evidence", "index": dash.dependencies.ALL}, "n_clicks"), Input("close-operation-evidence-modal", "n_clicks")],
        [State("operation-objectives-store", "data")], prevent_initial_call=True
    )
    def view_evidence(view_clicks, close_clicks, objectives):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, html.Div()
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger == "close-operation-evidence-modal":
            return {"display": "none"}, html.Div()
        if trigger and "view-operation-evidence" in trigger:
            try:
                match = re.search(r'"index":\s*(\d+)', trigger)
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
                                content.append(html.A("⬇ Download File", href=f"data:application/octet-stream;base64,{fcontent}", download=fname, style={"color": "#667eea", "fontWeight": "500"}))
                        if obj.get('evidence_text'):
                            content.append(html.H4("Description:", style={"marginTop": "15px", "marginBottom": "8px", "fontSize": "14px", "fontWeight": "600"}))
                            content.append(html.Div(obj.get('evidence_text'), style={"background": "#f8fafc", "padding": "12px", "borderLeft": "3px solid #667eea", "borderRadius": "6px", "fontSize": "13px"}))
                        if not content:
                            content = [html.P("No evidence available", style={"color": "#94a3b8", "textAlign": "center", "padding": "20px"})]
                        return {"display": "flex"}, html.Div(content)
            except:
                pass
        return {"display": "none"}, html.Div()
    
    # Hide toast
    @app.callback(Output("operation-success-toast", "style", allow_duplicate=True), [Input("operation-success-toast", "style")], prevent_initial_call=True)
    def hide_toast(style):
        time.sleep(3)
        return {"display": "none"}