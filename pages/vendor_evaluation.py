# pages/vendor_evaluation.py - Vendor Evaluation Form with Responsive Design

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from datetime import datetime
import base64
import json
import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import re

# File to store evaluations
EVALUATIONS_FILE = "vendor_evaluations_data.json"

def load_all_evaluations():
    """Load all saved evaluations from file"""
    if os.path.exists(EVALUATIONS_FILE):
        try:
            with open(EVALUATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_evaluation_to_file(vendor_code, data):
    """Save evaluation to file"""
    evaluations = load_all_evaluations()
    evaluations[vendor_code] = data
    with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)

def vendor_evaluation_page():
    """Vendor Evaluation Form Page - Responsive"""
    
    return html.Div([
        # Simple Header - Responsive
        html.Div(style={"marginBottom": "24px"}, children=[
            html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "flexWrap": "wrap", "gap": "15px"}, children=[
                html.Div([
                    html.H1("Vendor Evaluation", style={
                        "fontSize": "clamp(20px, 5vw, 24px)", 
                        "fontWeight": "700", 
                        "color": "#1e293b", 
                        "margin": "0 0 4px 0"
                    }),
                    html.P("Evaluate vendors using IMS/PRC/TRM/VEFV2.0 form", style={
                        "fontSize": "clamp(12px, 3vw, 14px)", 
                        "color": "#64748b", 
                        "margin": 0
                    })
                ]),
                html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"}, children=[
                    html.Button("← Back", id="back-to-procurement", style={
                        "padding": "8px 18px",
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "borderRadius": "8px",
                        "cursor": "pointer",
                        "color": "#475569",
                        "fontSize": "13px",
                        "fontWeight": "500",
                        "transition": "all 0.2s"
                    }),
                    html.Button("Download PDF", id="download-vendor-pdf", style={
                        "padding": "8px 18px",
                        "background": "#dc2626",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "8px",
                        "cursor": "pointer",
                        "fontSize": "13px",
                        "fontWeight": "500",
                        "transition": "all 0.2s"
                    })
                ])
            ])
        ]),
        
        # Search Section - Responsive Card
        html.Div(style={
            "background": "white",
            "borderRadius": "16px",
            "padding": "clamp(15px, 4vw, 20px)",
            "marginBottom": "20px",
            "border": "1px solid #e9ecef",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"
        }, children=[
            html.H3("Search Past Evaluations", style={
                "fontSize": "clamp(13px, 4vw, 14px)", 
                "fontWeight": "700", 
                "color": "#1e293b", 
                "margin": "0 0 12px 0"
            }),
            html.Div(style={"display": "flex", "gap": "12px", "alignItems": "flex-end", "flexWrap": "wrap"}, children=[
                html.Div(style={"flex": "1", "minWidth": "200px"}, children=[
                    html.Label("Vendor Code", style={
                        "fontSize": "12px", 
                        "fontWeight": "600", 
                        "marginBottom": "5px", 
                        "display": "block", 
                        "color": "#475569"
                    }),
                    dcc.Input(
                        type="text", 
                        id="search-past-vendor", 
                        placeholder="Enter Vendor Code...", 
                        style={
                            "width": "100%", 
                            "padding": "10px 12px", 
                            "borderRadius": "8px", 
                            "border": "1px solid #e2e8f0", 
                            "fontSize": "13px"
                        }
                    )
                ]),
                html.Button("Search", id="search-past-btn", style={
                    "padding": "10px 24px",
                    "background": "#667eea",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "8px",
                    "cursor": "pointer",
                    "fontSize": "13px",
                    "fontWeight": "500",
                    "transition": "all 0.2s"
                }),
                html.Div(id="search-result-status", style={"fontSize": "12px", "marginLeft": "10px"})
            ]),
            
            # Saved Evaluation Display Card
            html.Div(id="saved-evaluation-card", style={
                "display": "none", 
                "marginTop": "16px", 
                "background": "#f8fafc", 
                "borderRadius": "12px", 
                "padding": "15px", 
                "border": "1px solid #e2e8f0"
            }, children=[
                html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "flexWrap": "wrap", "gap": "10px", "marginBottom": "10px"}, children=[
                    html.H5("Previously Saved Evaluation", style={
                        "margin": "0", 
                        "fontSize": "13px", 
                        "fontWeight": "700", 
                        "color": "#1e293b"
                    }),
                    html.Button("Load Data", id="load-saved-data", style={
                        "padding": "5px 15px", 
                        "background": "#10b981", 
                        "color": "white", 
                        "border": "none", 
                        "borderRadius": "6px", 
                        "cursor": "pointer", 
                        "fontSize": "11px",
                        "fontWeight": "500",
                        "transition": "all 0.2s"
                    })
                ]),
                html.Div(id="saved-evaluation-details", style={"fontSize": "12px", "color": "#475569"})
            ])
        ]),
        
        # Main Form Card - Responsive
        html.Div(style={
            "background": "white",
            "borderRadius": "16px",
            "padding": "clamp(20px, 5vw, 30px)",
            "border": "1px solid #e9ecef",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
            "overflowX": "auto"
        }, children=[
            
            # Header with Logo
            html.Div(style={"textAlign": "center", "marginBottom": "30px", "paddingBottom": "20px", "borderBottom": "1px solid #eef2f6"}, children=[
                html.Img(
                    src="/assets/Screenshot 2026-05-26 154737.png",
                    style={"height": "clamp(40px, 8vw, 50px)", "width": "auto", "marginBottom": "12px"}
                ),
                html.H2("Vendor Evaluation Form", style={
                    "margin": "0", 
                    "fontSize": "clamp(18px, 5vw, 22px)", 
                    "fontWeight": "700", 
                    "color": "#1e293b"
                }),
                html.Div("IMS/PRC/TRM/VEFV2.0", style={"color": "#94a3b8", "fontSize": "12px", "marginTop": "5px"})
            ]),
            
            # Vendor Information Section
            html.Div(style={"marginBottom": "30px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "20px"
                }, children=[
                    html.H4("Vendor Information", style={
                        "margin": "0", 
                        "fontSize": "clamp(14px, 4vw, 16px)", 
                        "fontWeight": "700", 
                        "color": "#1e293b"
                    })
                ]),
                
                html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))", "gap": "16px"}, children=[
                    html.Div([
                        html.Label("Vendor Code *", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Input(
                            type="text", 
                            id="vendor-code", 
                            placeholder="Enter code", 
                            style={
                                "width": "100%", 
                                "padding": "10px 12px", 
                                "borderRadius": "8px", 
                                "border": "1px solid #e2e8f0", 
                                "fontSize": "14px"
                            }
                        )
                    ]),
                    html.Div([
                        html.Label("Vendor Name", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Input(
                            type="text", 
                            id="vendor-name", 
                            placeholder="Enter name", 
                            style={
                                "width": "100%", 
                                "padding": "10px 12px", 
                                "borderRadius": "8px", 
                                "border": "1px solid #e2e8f0", 
                                "fontSize": "14px"
                            }
                        )
                    ]),
                    html.Div([
                        html.Label("Scope of Supply", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Input(
                            type="text", 
                            id="scope-supply", 
                            placeholder="Enter scope", 
                            style={
                                "width": "100%", 
                                "padding": "10px 12px", 
                                "borderRadius": "8px", 
                                "border": "1px solid #e2e8f0", 
                                "fontSize": "14px"
                            }
                        )
                    ]),
                    html.Div([
                        html.Label("Registration Date", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.DatePickerSingle(
                            id="reg-date", 
                            date=datetime.now().strftime("%Y-%m-%d"), 
                            display_format="DD-MM-YYYY", 
                            style={"width": "100%", "borderRadius": "8px"}
                        )
                    ]),
                    html.Div([
                        html.Label("MSME Status", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Dropdown(
                            id="msme-status", 
                            options=[
                                {"label": "Yes", "value": "Yes"}, 
                                {"label": "No", "value": "No"}, 
                                {"label": "Applied", "value": "Applied"}
                            ], 
                            placeholder="Select", 
                            style={"borderRadius": "8px"}
                        )
                    ]),
                    html.Div([
                        html.Label("Outsource Type", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Dropdown(
                            id="outsource-type", 
                            options=[
                                {"label": "Manufacturer", "value": "Manufacturer"}, 
                                {"label": "Supplier", "value": "Supplier"},
                                {"label": "Service Provider", "value": "Service Provider"}, 
                                {"label": "Contractor", "value": "Contractor"}
                            ], 
                            placeholder="Select", 
                            style={"borderRadius": "8px"}
                        )
                    ]),
                    html.Div([
                        html.Label("GST Number", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "6px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Input(
                            type="text", 
                            id="gst-reg", 
                            placeholder="Enter GST", 
                            style={
                                "width": "100%", 
                                "padding": "10px 12px", 
                                "borderRadius": "8px", 
                                "border": "1px solid #e2e8f0", 
                                "fontSize": "14px"
                            }
                        )
                    ])
                ])
            ]),
            
            # Rating Scale Box - Responsive
            html.Div(style={
                "background": "#f8fafc", 
                "borderRadius": "12px", 
                "padding": "clamp(12px, 3vw, 15px)", 
                "marginBottom": "25px",
                "border": "1px solid #e2e8f0",
                "overflowX": "auto"
            }, children=[
                html.Div(style={"display": "flex", "justifyContent": "space-between", "textAlign": "center", "fontSize": "12px", "minWidth": "400px"}, children=[
                    html.Div(style={"flex": "1"}, children=[
                        html.Div("1", style={"fontWeight": "700", "color": "#dc2626", "fontSize": "clamp(14px, 4vw, 16px)"}), 
                        html.Small("Poor", style={"color": "#64748b"})
                    ]),
                    html.Div(style={"flex": "1"}, children=[
                        html.Div("2", style={"fontWeight": "700", "color": "#ea580c", "fontSize": "clamp(14px, 4vw, 16px)"}), 
                        html.Small("Weak", style={"color": "#64748b"})
                    ]),
                    html.Div(style={"flex": "1"}, children=[
                        html.Div("3", style={"fontWeight": "700", "color": "#ca8a04", "fontSize": "clamp(14px, 4vw, 16px)"}), 
                        html.Small("Adequate", style={"color": "#64748b"})
                    ]),
                    html.Div(style={"flex": "1"}, children=[
                        html.Div("4", style={"fontWeight": "700", "color": "#16a34a", "fontSize": "clamp(14px, 4vw, 16px)"}), 
                        html.Small("Good", style={"color": "#64748b"})
                    ]),
                    html.Div(style={"flex": "1"}, children=[
                        html.Div("5", style={"fontWeight": "700", "color": "#10b981", "fontSize": "clamp(14px, 4vw, 16px)"}), 
                        html.Small("Excellent", style={"color": "#64748b"})
                    ])
                ])
            ]),
            
            # Evaluation Table - Responsive with horizontal scroll
            html.Div(style={"marginBottom": "30px", "overflowX": "auto"}, children=[
                html.Div(style={"marginBottom": "15px"}, children=[
                    html.H4("Evaluation Parameters", style={
                        "margin": "0", 
                        "fontSize": "clamp(14px, 4vw, 16px)", 
                        "fontWeight": "700", 
                        "color": "#1e293b"
                    })
                ]),
                html.Table(style={
                    "width": "100%", 
                    "borderCollapse": "collapse", 
                    "border": "1px solid #e2e8f0", 
                    "borderRadius": "8px",
                    "minWidth": "600px"
                }, children=[
                    html.Thead(html.Tr([
                        html.Th("#", style={"padding": "12px", "background": "#f8fafc", "border": "1px solid #e2e8f0", "textAlign": "left", "fontSize": "13px", "fontWeight": "700", "width": "50px"}),
                        html.Th("Parameter", style={"padding": "12px", "background": "#f8fafc", "border": "1px solid #e2e8f0", "textAlign": "left", "fontSize": "13px", "fontWeight": "700"}),
                        html.Th("Rating", style={"padding": "12px", "background": "#f8fafc", "border": "1px solid #e2e8f0", "textAlign": "center", "fontSize": "13px", "fontWeight": "700", "width": "120px"}),
                        html.Th("Status", style={"padding": "12px", "background": "#f8fafc", "border": "1px solid #e2e8f0", "textAlign": "center", "fontSize": "13px", "fontWeight": "700", "width": "120px"})
                    ])),
                    html.Tbody([
                        _row(1, "Legal Compliance (Registration, GST, Licenses)"),
                        _row(2, "Experience (Years in Business, Similar Work)"),
                        _row(3, "Technical Capability (Equipment, Technology)"),
                        _row(4, "Management System (Supervision, Documentation)"),
                        _row(5, "Financial Stability (Turnover, Credit)"),
                        _row(6, "Manpower Competence (Staff, Training)"),
                        _row(7, "Delivery / Service Capacity (Lead Time, Support)"),
                        _row(8, "HSE Compliance (Safety, PPE)"),
                        _row(9, "Commercial Terms (Pricing, Payment)"),
                        _row(10, "Reputation (Market Image, Feedback)")
                    ])
                ])
            ]),
            
            # Score Summary - Responsive
            html.Div(style={
                "background": "#f8fafc",
                "borderRadius": "12px",
                "padding": "clamp(15px, 4vw, 20px)",
                "marginBottom": "25px",
                "border": "1px solid #e2e8f0"
            }, children=[
                html.Div(style={"display": "flex", "justifyContent": "space-around", "textAlign": "center", "flexWrap": "wrap", "gap": "20px"}, children=[
                    html.Div([
                        html.Div("Total Score", style={"fontSize": "12px", "color": "#64748b", "marginBottom": "5px", "fontWeight": "500"}),
                        html.Div(id="total-score", style={"fontSize": "clamp(24px, 6vw, 32px)", "fontWeight": "700", "color": "#667eea"})
                    ]),
                    html.Div([
                        html.Div("Average Score", style={"fontSize": "12px", "color": "#64748b", "marginBottom": "5px", "fontWeight": "500"}),
                        html.Div(id="avg-score", style={"fontSize": "clamp(24px, 6vw, 32px)", "fontWeight": "700", "color": "#667eea"})
                    ]),
                    html.Div([
                        html.Div("Final Status", style={"fontSize": "12px", "color": "#64748b", "marginBottom": "5px", "fontWeight": "500"}),
                        html.Div(id="final-status", style={"fontSize": "14px", "fontWeight": "600", "padding": "6px 18px", "borderRadius": "30px", "display": "inline-block"})
                    ])
                ])
            ]),
            
            # Note - Responsive
            html.Div(style={
                "background": "#fffbeb", 
                "borderRadius": "8px", 
                "padding": "clamp(10px, 3vw, 12px) clamp(12px, 4vw, 16px)", 
                "marginBottom": "25px", 
                "fontSize": "12px", 
                "color": "#92400e",
                "border": "1px solid #fde68a"
            }, children=[
                html.I(className="fas fa-info-circle", style={"marginRight": "8px"}),
                "Note: This applies to individual vendor registration. Final selection based on comparative scope of work."
            ]),
            
            # Footer - Responsive
            html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "justifyContent": "space-between", "alignItems": "flex-end"}, children=[
                html.Div(style={"display": "flex", "gap": "16px", "flex": "1", "flexWrap": "wrap"}, children=[
                    html.Div(style={"flex": "1", "minWidth": "180px"}, children=[
                        html.Label("Evaluated By", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "5px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Input(
                            type="text", 
                            id="evaluated-by", 
                            placeholder="Name", 
                            style={
                                "width": "100%", 
                                "padding": "10px", 
                                "borderRadius": "8px", 
                                "border": "1px solid #e2e8f0", 
                                "fontSize": "13px"
                            }
                        )
                    ]),
                    html.Div(style={"flex": "2", "minWidth": "200px"}, children=[
                        html.Label("Remarks", style={
                            "fontSize": "12px", 
                            "fontWeight": "600", 
                            "marginBottom": "5px", 
                            "display": "block", 
                            "color": "#475569"
                        }),
                        dcc.Input(
                            type="text", 
                            id="remarks", 
                            placeholder="Additional comments", 
                            style={
                                "width": "100%", 
                                "padding": "10px", 
                                "borderRadius": "8px", 
                                "border": "1px solid #e2e8f0", 
                                "fontSize": "13px"
                            }
                        )
                    ])
                ]),
                html.Button("Save Evaluation", id="save-evaluation", style={
                    "padding": "clamp(10px, 3vw, 12px) clamp(24px, 5vw, 32px)", 
                    "background": "#667eea", 
                    "color": "white", 
                    "border": "none", 
                    "borderRadius": "8px", 
                    "cursor": "pointer", 
                    "fontWeight": "600",
                    "fontSize": "clamp(13px, 4vw, 14px)",
                    "transition": "all 0.2s"
                })
            ])
        ]),
        
        # PDF Download component
        dcc.Download(id="download-vendor-pdf-file"),
        dcc.Store(id="vendor-ratings-store", data={}),
        dcc.Store(id="vendor-total-score", data="0"),
        dcc.Store(id="vendor-avg-score", data="0"),
        dcc.Store(id="vendor-final-status", data="Pending")
    ])

def _row(num, param):
    return html.Tr([
        html.Td(str(num), style={
            "padding": "10px", 
            "border": "1px solid #e2e8f0", 
            "color": "#64748b", 
            "fontSize": "13px", 
            "fontWeight": "500", 
            "textAlign": "center"
        }),
        html.Td(param, style={
            "padding": "10px", 
            "border": "1px solid #e2e8f0", 
            "fontSize": "13px", 
            "color": "#334155"
        }),
        html.Td(
            dcc.Dropdown(
                id=f"rating-{num}",
                options=[{"label": str(i), "value": i} for i in range(1, 6)],
                value=3,
                clearable=False,
                style={"width": "80px", "borderRadius": "6px", "margin": "0 auto"}
            ),
            style={"padding": "10px", "border": "1px solid #e2e8f0", "textAlign": "center"}
        ),
        html.Td(id=f"status-{num}", style={
            "padding": "8px", 
            "border": "1px solid #e2e8f0", 
            "textAlign": "center"
        })
    ])

def register_vendor_evaluation_callbacks(app):
    """Register vendor evaluation callbacks"""
    
    for i in range(1, 11):
        @app.callback(
            Output(f"status-{i}", "children"),
            Output(f"status-{i}", "style"),
            Input(f"rating-{i}", "value")
        )
        def update_status(value, n=i):
            if value == 5:
                return "Excellent", {
                    "padding": "4px 12px", 
                    "background": "#d1fae5", 
                    "color": "#10b981", 
                    "borderRadius": "30px", 
                    "fontSize": "11px", 
                    "display": "inline-block", 
                    "fontWeight": "600"
                }
            elif value == 4:
                return "Good", {
                    "padding": "4px 12px", 
                    "background": "#bbf7d0", 
                    "color": "#16a34a", 
                    "borderRadius": "30px", 
                    "fontSize": "11px", 
                    "display": "inline-block", 
                    "fontWeight": "600"
                }
            elif value == 3:
                return "Adequate", {
                    "padding": "4px 12px", 
                    "background": "#fef08a", 
                    "color": "#ca8a04", 
                    "borderRadius": "30px", 
                    "fontSize": "11px", 
                    "display": "inline-block", 
                    "fontWeight": "600"
                }
            elif value == 2:
                return "Weak", {
                    "padding": "4px 12px", 
                    "background": "#fed7aa", 
                    "color": "#ea580c", 
                    "borderRadius": "30px", 
                    "fontSize": "11px", 
                    "display": "inline-block", 
                    "fontWeight": "600"
                }
            else:
                return "Poor", {
                    "padding": "4px 12px", 
                    "background": "#fecaca", 
                    "color": "#dc2626", 
                    "borderRadius": "30px", 
                    "fontSize": "11px", 
                    "display": "inline-block", 
                    "fontWeight": "600"
                }
    
    @app.callback(
        [Output("total-score", "children"),
         Output("avg-score", "children"),
         Output("final-status", "children"),
         Output("final-status", "style"),
         Output("vendor-total-score", "data"),
         Output("vendor-avg-score", "data"),
         Output("vendor-final-status", "data")],
        [Input(f"rating-{i}", "value") for i in range(1, 11)]
    )
    def update_scores(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10):
        ratings = [r or 0 for r in [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]]
        total = sum(ratings)
        avg = total / 10
        
        if avg >= 4:
            status = "Accepted"
            style = {
                "fontSize": "13px", 
                "fontWeight": "700", 
                "padding": "6px 16px", 
                "borderRadius": "30px", 
                "display": "inline-block", 
                "background": "#d1fae5", 
                "color": "#10b981"
            }
        elif avg >= 2.6:
            status = "Conditionally Accepted"
            style = {
                "fontSize": "13px", 
                "fontWeight": "700", 
                "padding": "6px 16px", 
                "borderRadius": "30px", 
                "display": "inline-block", 
                "background": "#fef3c7", 
                "color": "#f59e0b"
            }
        else:
            status = "Rejected"
            style = {
                "fontSize": "13px", 
                "fontWeight": "700", 
                "padding": "6px 16px", 
                "borderRadius": "30px", 
                "display": "inline-block", 
                "background": "#fee2e2", 
                "color": "#dc2626"
            }
        
        return f"{total}/50", f"{avg:.1f}", status, style, f"{total}/50", f"{avg:.1f}", status
    
    # Search past evaluation
    @app.callback(
        [Output("saved-evaluation-card", "style"),
         Output("saved-evaluation-details", "children"),
         Output("search-result-status", "children")],
        Input("search-past-btn", "n_clicks"),
        State("search-past-vendor", "value")
    )
    def search_past_evaluation(n_clicks, vendor_code):
        if not n_clicks or not vendor_code:
            return {"display": "none"}, "", ""
        
        evaluations = load_all_evaluations()
        if vendor_code in evaluations:
            data = evaluations[vendor_code]
            details = html.Div([
                html.Div([html.Strong("Vendor Name: "), data.get('vendor_name', 'N/A')], style={"marginBottom": "6px"}),
                html.Div([html.Strong("Evaluation Date: "), data.get('saved_date', 'N/A')], style={"marginBottom": "6px"}),
                html.Div([html.Strong("Total Score: "), data.get('total_score', 'N/A')], style={"marginBottom": "6px"}),
                html.Div([html.Strong("Final Status: "), html.Span(data.get('final_status', 'N/A'), style={"color": "#667eea", "fontWeight": "600"})])
            ])
            return {
                "display": "block", 
                "marginTop": "16px", 
                "background": "#f8fafc", 
                "borderRadius": "12px", 
                "padding": "15px", 
                "border": "1px solid #e2e8f0"
            }, details, f"✅ Found evaluation for {vendor_code}"
        else:
            return {"display": "none"}, "", f"❌ No evaluation found for {vendor_code}"
    
    # Load saved data into form
    @app.callback(
        [Output("vendor-name", "value"),
         Output("scope-supply", "value"),
         Output("reg-date", "date"),
         Output("msme-status", "value"),
         Output("outsource-type", "value"),
         Output("gst-reg", "value"),
         Output("evaluated-by", "value"),
         Output("remarks", "value"),
         Output("rating-1", "value"),
         Output("rating-2", "value"),
         Output("rating-3", "value"),
         Output("rating-4", "value"),
         Output("rating-5", "value"),
         Output("rating-6", "value"),
         Output("rating-7", "value"),
         Output("rating-8", "value"),
         Output("rating-9", "value"),
         Output("rating-10", "value"),
         Output("saved-evaluation-card", "style", allow_duplicate=True),
         Output("search-result-status", "children", allow_duplicate=True)],
        Input("load-saved-data", "n_clicks"),
        State("search-past-vendor", "value"),
        prevent_initial_call=True
    )
    def load_saved_data(n_clicks, vendor_code):
        if not n_clicks or not vendor_code:
            return [None] * 20
        
        evaluations = load_all_evaluations()
        if vendor_code in evaluations:
            data = evaluations[vendor_code]
            ratings = data.get('ratings', {})
            return (
                data.get('vendor_name'), data.get('scope_supply'), data.get('reg_date'),
                data.get('msme_status'), data.get('outsource_type'), data.get('gst_reg'),
                data.get('evaluated_by'), data.get('remarks'),
                ratings.get('Legal Compliance', 3), ratings.get('Experience', 3),
                ratings.get('Technical Capability', 3), ratings.get('Management System', 3),
                ratings.get('Financial Stability', 3), ratings.get('Manpower Competence', 3),
                ratings.get('Delivery Capacity', 3), ratings.get('HSE Compliance', 3),
                ratings.get('Commercial Terms', 3), ratings.get('Reputation', 3),
                {"display": "none"}, "✅ Data loaded successfully!"
            )
        return [None] * 20
    
    # Save evaluation
    @app.callback(
        Output("save-evaluation", "children"),
        Input("save-evaluation", "n_clicks"),
        [State("vendor-code", "value"),
         State("vendor-name", "value"),
         State("scope-supply", "value"),
         State("reg-date", "date"),
         State("msme-status", "value"),
         State("outsource-type", "value"),
         State("gst-reg", "value"),
         State("evaluated-by", "value"),
         State("remarks", "value"),
         State("vendor-total-score", "data"),
         State("vendor-avg-score", "data"),
         State("vendor-final-status", "data"),
         State("rating-1", "value"),
         State("rating-2", "value"),
         State("rating-3", "value"),
         State("rating-4", "value"),
         State("rating-5", "value"),
         State("rating-6", "value"),
         State("rating-7", "value"),
         State("rating-8", "value"),
         State("rating-9", "value"),
         State("rating-10", "value")]
    )
    def save_evaluation(n_clicks, vendor_code, vendor_name, scope_supply, reg_date, msme_status,
                        outsource_type, gst_reg, evaluated_by, remarks, total_score, avg_score, final_status,
                        r1, r2, r3, r4, r5, r6, r7, r8, r9, r10):
        if not n_clicks:
            return "Save Evaluation"
        
        if not vendor_code:
            return html.Div([
                html.I(className="fas fa-exclamation-triangle", style={"marginRight": "6px"}), 
                " Vendor Code Required"
            ], style={
                "color": "#dc2626", 
                "display": "flex", 
                "alignItems": "center", 
                "gap": "5px", 
                "fontSize": "13px"
            })
        
        evaluation_data = {
            "vendor_code": vendor_code,
            "vendor_name": vendor_name,
            "scope_supply": scope_supply,
            "reg_date": reg_date,
            "msme_status": msme_status,
            "outsource_type": outsource_type,
            "gst_reg": gst_reg,
            "evaluated_by": evaluated_by,
            "remarks": remarks,
            "total_score": total_score,
            "avg_score": avg_score,
            "final_status": final_status,
            "ratings": {
                "Legal Compliance": r1 or 0,
                "Experience": r2 or 0,
                "Technical Capability": r3 or 0,
                "Management System": r4 or 0,
                "Financial Stability": r5 or 0,
                "Manpower Competence": r6 or 0,
                "Delivery Capacity": r7 or 0,
                "HSE Compliance": r8 or 0,
                "Commercial Terms": r9 or 0,
                "Reputation": r10 or 0
            },
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_evaluation_to_file(vendor_code, evaluation_data)
        
        return html.Div([
            html.I(className="fas fa-check-circle", style={"marginRight": "6px"}), 
            " Saved Successfully!"
        ], style={
            "color": "#10b981", 
            "display": "flex", 
            "alignItems": "center", 
            "gap": "5px", 
            "fontSize": "13px"
        })
    
    # Professional PDF Generation
    @app.callback(
        Output("download-vendor-pdf-file", "data"),
        Input("download-vendor-pdf", "n_clicks"),
        [State("vendor-code", "value"),
         State("vendor-name", "value"),
         State("scope-supply", "value"),
         State("reg-date", "date"),
         State("msme-status", "value"),
         State("outsource-type", "value"),
         State("gst-reg", "value"),
         State("evaluated-by", "value"),
         State("remarks", "value"),
         State("vendor-total-score", "data"),
         State("vendor-avg-score", "data"),
         State("vendor-final-status", "data"),
         State("rating-1", "value"),
         State("rating-2", "value"),
         State("rating-3", "value"),
         State("rating-4", "value"),
         State("rating-5", "value"),
         State("rating-6", "value"),
         State("rating-7", "value"),
         State("rating-8", "value"),
         State("rating-9", "value"),
         State("rating-10", "value")]
    )
    def download_pdf(n_clicks, vendor_code, vendor_name, scope_supply, reg_date, msme_status, 
                     outsource_type, gst_reg, evaluated_by, remarks, total_score, avg_score, final_status,
                     r1, r2, r3, r4, r5, r6, r7, r8, r9, r10):
        if not n_clicks:
            return None
        
        # Get logo as base64
        logo_path = os.path.join("assets", "Screenshot 2026-05-26 154737.png")
        logo_base64 = ""
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1e293b'),
            alignment=1,
            spaceAfter=5,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#94a3b8'),
            alignment=1,
            spaceAfter=15
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.white,
            backColor=colors.HexColor('#667eea'),
            leftIndent=10,
            rightIndent=10,
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        # Logo
        if logo_base64:
            try:
                img_buffer = io.BytesIO(base64.b64decode(logo_base64))
                img = Image(img_buffer, width=100, height=40)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 5))
            except:
                pass
        
        # Title
        story.append(Paragraph("Vendor Evaluation Report", title_style))
        story.append(Paragraph("IMS/PRC/TRM/VEFV2.0", subtitle_style))
        story.append(Spacer(1, 15))
        
        # VENDOR INFORMATION SECTION
        story.append(Paragraph("VENDOR INFORMATION", heading_style))
        
        vendor_data = [
            ["Vendor Code:", vendor_code or 'N/A'],
            ["Vendor Name:", vendor_name or 'N/A'],
            ["Scope of Supply:", scope_supply or 'N/A'],
            ["Registration Date:", reg_date or 'N/A'],
            ["MSME Status:", msme_status or 'N/A'],
            ["Outsource Type:", outsource_type or 'N/A'],
            ["GST Number:", gst_reg or 'N/A']
        ]
        
        vendor_table = Table(vendor_data, colWidths=[1.2*inch, 3.5*inch])
        vendor_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(vendor_table)
        story.append(Spacer(1, 15))
        
        # EVALUATION PARAMETERS SECTION
        story.append(Paragraph("EVALUATION PARAMETERS", heading_style))
        
        rating_values = [r1 or 0, r2 or 0, r3 or 0, r4 or 0, r5 or 0, r6 or 0, r7 or 0, r8 or 0, r9 or 0, r10 or 0]
        
        def get_status_text(val):
            if val == 5: return "Excellent"
            elif val == 4: return "Good"
            elif val == 3: return "Adequate"
            elif val == 2: return "Weak"
            else: return "Poor"
        
        def get_status_color(val):
            if val == 5: return colors.HexColor('#10b981')
            elif val == 4: return colors.HexColor('#16a34a')
            elif val == 3: return colors.HexColor('#ca8a04')
            elif val == 2: return colors.HexColor('#ea580c')
            else: return colors.HexColor('#dc2626')
        
        eval_data = [["#", "Parameter", "Rating", "Status"]]
        
        parameters = [
            "Legal Compliance (Registration, GST, Licenses)",
            "Experience (Years in Business, Similar Work)",
            "Technical Capability (Equipment, Technology)",
            "Management System (Supervision, Documentation)",
            "Financial Stability (Turnover, Credit)",
            "Manpower Competence (Staff, Training)",
            "Delivery / Service Capacity (Lead Time, Support)",
            "HSE Compliance (Safety, PPE)",
            "Commercial Terms (Pricing, Payment)",
            "Reputation (Market Image, Feedback)"
        ]
        
        for i, param in enumerate(parameters):
            rating = rating_values[i]
            status_text = get_status_text(rating)
            eval_data.append([str(i+1), param, str(rating), status_text])
        
        eval_table = Table(eval_data, colWidths=[0.5*inch, 3.2*inch, 0.8*inch, 1.2*inch])
        
        table_style = [
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155')),
        ]
        
        for i in range(1, 11):
            rating = rating_values[i-1]
            status_color = get_status_color(rating)
            table_style.append(('TEXTCOLOR', (3, i), (3, i), status_color))
            table_style.append(('FONTNAME', (3, i), (3, i), 'Helvetica-Bold'))
        
        eval_table.setStyle(TableStyle(table_style))
        story.append(eval_table)
        story.append(Spacer(1, 15))
        
        # SCORE SUMMARY SECTION
        story.append(Paragraph("SCORE SUMMARY", heading_style))
        
        total_val = total_score or '0'
        avg_val = avg_score or '0'
        status_val = final_status or 'Pending'
        
        if status_val == 'Accepted':
            status_color = colors.HexColor('#10b981')
            status_bg = colors.HexColor('#d1fae5')
        elif status_val == 'Conditionally Accepted':
            status_color = colors.HexColor('#f59e0b')
            status_bg = colors.HexColor('#fef3c7')
        else:
            status_color = colors.HexColor('#dc2626')
            status_bg = colors.HexColor('#fee2e2')
        
        score_data = [
            ["Total Score:", total_val],
            ["Average Score:", f"{avg_val} / 5"],
            ["Final Status:", status_val]
        ]
        
        score_table = Table(score_data, colWidths=[2*inch, 2.5*inch])
        score_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (1, 2), (1, 2), status_bg),
            ('TEXTCOLOR', (1, 2), (1, 2), status_color),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 15))
        
        # EVALUATION DETAILS SECTION
        story.append(Paragraph("EVALUATION DETAILS", heading_style))
        
        details_data = [
            ["Evaluated By:", evaluated_by or 'N/A'],
            ["Remarks:", remarks or 'N/A'],
            ["Report Generated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        details_table = Table(details_data, colWidths=[1.2*inch, 3.5*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        # Footer Note
        note_style = ParagraphStyle(
            'Note',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#94a3b8'),
            alignment=1,
            spaceBefore=10
        )
        story.append(Paragraph("Note: This applies to individual vendor registration. Final selection based on comparative scope of work.", note_style))
        
        # Build PDF
        doc.build(story)
        
        pdf_content = buffer.getvalue()
        buffer.close()
        
        pdf_b64 = base64.b64encode(pdf_content).decode()
        
        return dict(
            content=pdf_b64,
            filename=f"Vendor_Evaluation_{vendor_code or 'Report'}_{datetime.now().strftime('%Y%m%d')}.pdf",
            base64=True
        )
    
    # Back button
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("back-to-procurement", "n_clicks"),
        prevent_initial_call=True
    )
    def go_back(n):
        if n:
            return "/procurement"
        return no_update