# pages/hr.py - Human Resources Page with HR Business Document & HR Feedback Form (Training Feedback)

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from datetime import datetime
import json
import re
import base64
import time
import os
import io
from flask import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from database import (
    get_all_hr_objectives,
    save_hr_evaluation_with_evidence,
    get_hr_finance_years,
    get_hr_finance_amount_by_year
)

# File to store HR feedbacks
FEEDBACK_FILE = "hr_feedbacks_data.json"

def load_all_hr_feedbacks():
    """Load all saved HR feedbacks from file"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_hr_feedback_to_file(employee_name, data):
    """Save HR feedback to file"""
    feedbacks = load_all_hr_feedbacks()
    feedbacks[employee_name] = data
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, indent=2, ensure_ascii=False)

def hr_page():
    """Human Resources Page"""
    objectives = get_all_hr_objectives()
    finance_years = get_hr_finance_years()
    
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            # Header
            html.Div(
                style={'marginBottom': '24px'},
                children=[
                    html.H1(
                        "Human Resources",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "HR Business Documents & Feedback Management",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # ========== TWO CARDS ==========
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 1fr)',
                    'gap': '20px'
                },
                children=[
                    # Card 1 - HR Business Document (Clickable)
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'padding': '24px',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)',
                            'cursor': 'pointer',
                            'transition': 'all 0.3s ease'
                        },
                        id="card-hr-business-doc",
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '16px'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'width': '48px',
                                            'height': '48px',
                                            'background': '#dbeafe',
                                            'borderRadius': '12px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center'
                                        },
                                        children=[
                                            html.I(
                                                className="fas fa-file-alt",
                                                style={'color': '#3b82f6', 'fontSize': '20px'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        style={'flex': '1'},
                                        children=[
                                            html.H3(
                                                "HR Business Document",
                                                style={
                                                    'fontSize': '16px',
                                                    'fontWeight': '700',
                                                    'color': '#1e293b',
                                                    'margin': '0'
                                                }
                                            ),
                                            html.P(
                                                "View and manage HR business documents",
                                                style={
                                                    'fontSize': '12px',
                                                    'color': '#64748b',
                                                    'margin': '4px 0 0 0'
                                                }
                                            )
                                        ]
                                    ),
                                    html.I(
                                        className="fas fa-chevron-right",
                                        style={'color': '#94a3b8', 'fontSize': '14px'}
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Card 2 - HR Feedback Form (Training Feedback)
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'padding': '24px',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)',
                            'cursor': 'pointer',
                            'transition': 'all 0.3s ease'
                        },
                        id="card-hr-feedback",
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '16px'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'width': '48px',
                                            'height': '48px',
                                            'background': '#ede9fe',
                                            'borderRadius': '12px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center'
                                        },
                                        children=[
                                            html.I(
                                                className="fas fa-comment-dots",
                                                style={'color': '#8b5cf6', 'fontSize': '20px'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        style={'flex': '1'},
                                        children=[
                                            html.H3(
                                                "HR Feedback Form",
                                                style={
                                                    'fontSize': '16px',
                                                    'fontWeight': '700',
                                                    'color': '#1e293b',
                                                    'margin': '0'
                                                }
                                            ),
                                            html.P(
                                                "Submit and manage HR feedback",
                                                style={
                                                    'fontSize': '12px',
                                                    'color': '#64748b',
                                                    'margin': '4px 0 0 0'
                                                }
                                            )
                                        ]
                                    ),
                                    html.I(
                                        className="fas fa-chevron-right",
                                        style={'color': '#94a3b8', 'fontSize': '14px'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # CSS for hover effect
            html.Div([
                dcc.Markdown("""
                <style>
                    #card-hr-business-doc:hover, #card-hr-feedback:hover {
                        transform: translateY(-4px);
                        border-color: #667eea !important;
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
                    }
                </style>
                """, dangerously_allow_html=True)
            ])
        ]
    )


def register_hr_callbacks(app):
    """Register callbacks for HR page"""
    pass