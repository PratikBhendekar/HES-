# pages/incident_investigation.py - Incident Investigation Report Page with Professional PDF

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
import json
import datetime
import base64
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# File to store incidents
INCIDENTS_FILE = "incidents_data.json"

def load_incidents():
    """Load incidents from JSON file"""
    if os.path.exists(INCIDENTS_FILE):
        try:
            with open(INCIDENTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_incidents(incidents):
    """Save incidents to JSON file"""
    with open(INCIDENTS_FILE, 'w') as f:
        json.dump(incidents, f, indent=2)

def incident_investigation_page():
    incidents = load_incidents()
    
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh',
            'fontFamily': "'Inter', sans-serif"
        },
        children=[
            # Font Awesome
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
            
            # Page Header with Actions
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'marginBottom': '24px',
                    'flexWrap': 'wrap',
                    'gap': '12px'
                },
                children=[
                    html.Div(
                        children=[
                            html.H1(
                                "Incident Investigation Report",
                                style={
                                    'fontSize': '24px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'margin': '0 0 4px 0',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.P(
                                "Create and manage incident investigation reports",
                                style={
                                    'fontSize': '14px',
                                    'color': '#64748b',
                                    'margin': 0
                                }
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'gap': '12px', 'flexWrap': 'wrap'},
                        children=[
                            html.Button(
                                [html.I(className="fas fa-save", style={'marginRight': '8px'}), "Save Incident"],
                                id="save-incident-btn",
                                style={
                                    'padding': '10px 20px',
                                    'background': 'linear-gradient(135deg, #10b981, #059669)',
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': '10px',
                                    'cursor': 'pointer',
                                    'fontSize': '14px',
                                    'fontWeight': '600',
                                    'transition': 'all 0.3s ease'
                                }
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== INCIDENT FORM ====================
            html.Div(
                id="incident-form-container",
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#ef4444'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Incident Details Form",
                                style={
                                    'fontSize': '18px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '16px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            
                            # Form Row 1 - Date, Time, Day
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(3, 1fr)',
                                    'gap': '16px',
                                    'marginBottom': '16px'
                                },
                                children=[
                                    html.Div(
                                        children=[
                                            html.Label("Date of Incident", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.DatePickerSingle(
                                                id="incident-date",
                                                date=datetime.date.today(),
                                                display_format="DD/MM/YYYY",
                                                style={'width': '100%'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Time", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="incident-time",
                                                type="text",
                                                placeholder="e.g. 12:27 PM",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Day of Week", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="incident-day",
                                                type="text",
                                                placeholder="e.g. Wednesday",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Form Row 2 - Location, Weather
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(2, 1fr)',
                                    'gap': '16px',
                                    'marginBottom': '16px'
                                },
                                children=[
                                    html.Div(
                                        children=[
                                            html.Label("Location", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="incident-location",
                                                type="text",
                                                placeholder="Enter location",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Weather Conditions", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="incident-weather",
                                                type="text",
                                                placeholder="e.g. Clear, Rainy",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Form Row 3 - Incident Description
                            html.Div(
                                style={'marginBottom': '16px'},
                                children=[
                                    html.Label("Incident Description", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                    dcc.Textarea(
                                        id="incident-description",
                                        placeholder="Describe the incident in detail...",
                                        value="",
                                        style={
                                            'width': '100%',
                                            'padding': '12px 14px',
                                            'border': '2px solid #e2e8f0',
                                            'borderRadius': '10px',
                                            'fontSize': '14px',
                                            'minHeight': '100px',
                                            'fontFamily': "'Inter', sans-serif",
                                            'resize': 'vertical'
                                        }
                                    )
                                ]
                            ),
                            
                            # Form Row 4 - Nature of Incident (Checkboxes)
                            html.Div(
                                style={'marginBottom': '0'},
                                children=[
                                    html.Label("Nature of Incident", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '8px', 'display': 'block'}),
                                    html.Div(
                                        style={
                                            'display': 'grid',
                                            'gridTemplateColumns': 'repeat(4, 1fr)',
                                            'gap': '8px'
                                        },
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-near-miss",
                                                        options=[{"label": "Near Miss", "value": "near-miss"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-first-aid",
                                                        options=[{"label": "First Aid Case", "value": "first-aid"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-medical",
                                                        options=[{"label": "Medical Treatment", "value": "medical"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-lti",
                                                        options=[{"label": "Lost Time Injury", "value": "lti"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-fatal",
                                                        options=[{"label": "Fatal Accident", "value": "fatal"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-property",
                                                        options=[{"label": "Property Damage", "value": "property"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-environmental",
                                                        options=[{"label": "Environmental", "value": "environmental"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'},
                                                children=[
                                                    dcc.Checklist(
                                                        id="nature-unsafe",
                                                        options=[{"label": "Unsafe Condition", "value": "unsafe"}],
                                                        value=[],
                                                        style={'display': 'inline-block'}
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== INJURED PERSON DETAILS ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#dc2626'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Injured Person Details",
                                style={
                                    'fontSize': '18px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '16px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(3, 1fr)',
                                    'gap': '16px',
                                    'marginBottom': '0'
                                },
                                children=[
                                    html.Div(
                                        children=[
                                            html.Label("Name", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="injured-name",
                                                type="text",
                                                placeholder="Enter name",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Job Title", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="injured-job",
                                                type="text",
                                                placeholder="Enter job title",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Department", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="injured-dept",
                                                type="text",
                                                placeholder="Enter department",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Contact Number", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="injured-contact",
                                                type="text",
                                                placeholder="Enter contact",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Employment Duration", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="injured-duration",
                                                type="text",
                                                placeholder="e.g. 01 August 2025",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Nature of Injury", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#dc2626', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="injured-nature",
                                                type="text",
                                                placeholder="e.g. Fracture - Left Leg",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #dc2626',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px',
                                                    'color': '#dc2626'
                                                }
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== WITNESS INFORMATION ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#8b5cf6'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Witness Information",
                                style={
                                    'fontSize': '18px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '16px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(4, 1fr)',
                                    'gap': '16px',
                                    'marginBottom': '0'
                                },
                                children=[
                                    html.Div(
                                        children=[
                                            html.Label("Name", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="witness-name",
                                                type="text",
                                                placeholder="Enter name",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Job Title", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="witness-job",
                                                type="text",
                                                placeholder="Enter job title",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Department", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="witness-dept",
                                                type="text",
                                                placeholder="Enter department",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Label("Contact Number", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="witness-contact",
                                                type="text",
                                                placeholder="Enter contact",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== ACTIONS TAKEN ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#10b981'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Actions Taken",
                                style={
                                    'fontSize': '18px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '16px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.Div(
                                style={'marginBottom': '16px'},
                                children=[
                                    html.Label("Immediate Actions", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                    dcc.Textarea(
                                        id="immediate-actions",
                                        placeholder="Describe immediate actions taken...",
                                        value="",
                                        style={
                                            'width': '100%',
                                            'padding': '12px 14px',
                                            'border': '2px solid #e2e8f0',
                                            'borderRadius': '10px',
                                            'fontSize': '14px',
                                            'minHeight': '80px',
                                            'fontFamily': "'Inter', sans-serif",
                                            'resize': 'vertical'
                                        }
                                    )
                                ]
                            ),
                            html.Div(
                                style={'marginBottom': '16px'},
                                children=[
                                    html.Label("Contributing Factors", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                    dcc.Textarea(
                                        id="contributing-factors",
                                        placeholder="List contributing factors...",
                                        value="",
                                        style={
                                            'width': '100%',
                                            'padding': '12px 14px',
                                            'border': '2px solid #e2e8f0',
                                            'borderRadius': '10px',
                                            'fontSize': '14px',
                                            'minHeight': '80px',
                                            'fontFamily': "'Inter', sans-serif",
                                            'resize': 'vertical'
                                        }
                                    )
                                ]
                            ),
                            html.Div(
                                style={'marginBottom': '0'},
                                children=[
                                    html.Label("Corrective Actions", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                    dcc.Textarea(
                                        id="corrective-actions",
                                        placeholder="Describe corrective actions...",
                                        value="",
                                        style={
                                            'width': '100%',
                                            'padding': '12px 14px',
                                            'border': '2px solid #dc2626',
                                            'borderRadius': '10px',
                                            'fontSize': '14px',
                                            'minHeight': '60px',
                                            'fontFamily': "'Inter', sans-serif",
                                            'resize': 'vertical'
                                        }
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== INVESTIGATION TEAM ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#1e293b'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Investigation Team",
                                style={
                                    'fontSize': '18px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '16px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(3, 1fr)',
                                    'gap': '16px',
                                    'marginBottom': '0'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'background': '#f8fafc',
                                            'borderRadius': '12px',
                                            'padding': '16px',
                                            'border': '1px solid #e2e8f0'
                                        },
                                        children=[
                                            html.Label("Investigator Name", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="investigator-name",
                                                type="text",
                                                placeholder="Enter name",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'background': '#f8fafc',
                                            'borderRadius': '12px',
                                            'padding': '16px',
                                            'border': '1px solid #e2e8f0'
                                        },
                                        children=[
                                            html.Label("Signature", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.Input(
                                                id="investigator-signature",
                                                type="text",
                                                placeholder="Signature",
                                                value="",
                                                style={
                                                    'width': '100%',
                                                    'padding': '10px 12px',
                                                    'border': '2px solid #e2e8f0',
                                                    'borderRadius': '10px',
                                                    'fontSize': '14px'
                                                }
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'background': '#f8fafc',
                                            'borderRadius': '12px',
                                            'padding': '16px',
                                            'border': '1px solid #e2e8f0'
                                        },
                                        children=[
                                            html.Label("Date", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                            dcc.DatePickerSingle(
                                                id="investigator-date",
                                                date=datetime.date.today(),
                                                display_format="DD/MM/YYYY",
                                                style={'width': '100%'}
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== ATTACH DOCUMENT SECTION ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#f59e0b'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.H3(
                                "Attach Document",
                                style={
                                    'fontSize': '18px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '16px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': '1fr 1fr',
                                    'gap': '20px',
                                    'alignItems': 'start'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'border': '2px dashed #cbd5e1',
                                            'borderRadius': '12px',
                                            'padding': '30px 20px',
                                            'textAlign': 'center',
                                            'background': '#fafbfc',
                                            'minHeight': '150px',
                                            'display': 'flex',
                                            'flexDirection': 'column',
                                            'justifyContent': 'center',
                                            'alignItems': 'center',
                                            'cursor': 'pointer',
                                            'transition': 'all 0.3s ease',
                                            'width': '100%'
                                        },
                                        children=[
                                            dcc.Upload(
                                                id="upload-document",
                                                children=html.Div([
                                                    html.I(className="fas fa-cloud-upload-alt", style={'fontSize': '40px', 'color': '#94a3b8', 'display': 'block', 'marginBottom': '12px'}),
                                                    html.Div("Drag & Drop or Click to Select", style={'fontSize': '16px', 'color': '#64748b', 'fontWeight': '500'}),
                                                    html.Div("PDF, JPG, PNG, DOCX (Max 10MB)", style={'fontSize': '13px', 'color': '#94a3b8', 'marginTop': '6px'})
                                                ]),
                                                style={
                                                    'width': '100%',
                                                    'height': '100%',
                                                    'cursor': 'pointer'
                                                },
                                                multiple=False
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'flexDirection': 'column',
                                            'gap': '16px',
                                            'height': '100%'
                                        },
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.Label("Document Description", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '6px', 'display': 'block'}),
                                                    dcc.Input(
                                                        id="document-description",
                                                        type="text",
                                                        placeholder="e.g. Medical Report, Photos, Investigation Photos",
                                                        value="",
                                                        style={
                                                            'width': '100%',
                                                            'padding': '12px 14px',
                                                            'border': '2px solid #e2e8f0',
                                                            'borderRadius': '10px',
                                                            'fontSize': '14px'
                                                        }
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                id="uploaded-files-list",
                                                style={
                                                    'display': 'none',
                                                    'padding': '14px 18px',
                                                    'background': '#f0fdf4',
                                                    'borderRadius': '10px',
                                                    'border': '1px solid #86efac',
                                                    'marginTop': '4px'
                                                },
                                                children=[
                                                    html.Div(
                                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'},
                                                        children=[
                                                            html.I(className="fas fa-file-pdf", style={'color': '#dc2626', 'fontSize': '22px'}),
                                                            html.Div(
                                                                style={'flex': '1'},
                                                                children=[
                                                                    html.Div(id="uploaded-file-name", style={'fontSize': '14px', 'color': '#1e293b', 'fontWeight': '500'}),
                                                                    html.Div(id="uploaded-file-size", style={'fontSize': '12px', 'color': '#64748b'})
                                                                ]
                                                            ),
                                                            html.Button(
                                                                html.I(className="fas fa-times", style={'color': '#ef4444', 'fontSize': '14px'}),
                                                                id="remove-uploaded-file",
                                                                style={
                                                                    'background': 'none',
                                                                    'border': 'none',
                                                                    'cursor': 'pointer',
                                                                    'padding': '6px 10px',
                                                                    'borderRadius': '6px',
                                                                    'transition': 'all 0.2s ease'
                                                                }
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            dcc.Store(id="uploaded-file-data", data={})
                        ]
                    )
                ]
            ),
            
            # ==================== SAVED INCIDENTS LIST ====================
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '20px'
                },
                children=[
                    html.Div(style={'height': '4px', 'background': '#6366f1'}),
                    html.Div(
                        style={'padding': '24px'},
                        children=[
                            html.Div(
                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '16px'},
                                children=[
                                    html.H3(
                                        "Saved Incidents",
                                        style={
                                            'fontSize': '18px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'margin': 0,
                                            'fontFamily': "'Poppins', sans-serif"
                                        }
                                    ),
                                    html.Span(
                                        f"Total: {len(incidents)}",
                                        style={'fontSize': '14px', 'color': '#64748b', 'fontWeight': '600'}
                                    )
                                ]
                            ),
                            
                            html.Div(
                                id="incidents-list",
                                children=create_incidents_table(incidents)
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== SAVE CONFIRMATION MODAL ====================
            html.Div(
                id="save-confirmation-modal",
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'top': 0,
                    'left': 0,
                    'width': '100%',
                    'height': '100%',
                    'background': 'rgba(0,0,0,0.5)',
                    'zIndex': 9999,
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'backdropFilter': 'blur(4px)'
                },
                children=[
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '20px',
                            'padding': '30px',
                            'maxWidth': '500px',
                            'width': '90%',
                            'textAlign': 'center',
                            'boxShadow': '0 25px 50px rgba(0,0,0,0.3)',
                            'animation': 'fadeInScale 0.3s ease-out'
                        },
                        children=[
                            html.I(className="fas fa-check-circle", style={'fontSize': '60px', 'color': '#10b981', 'marginBottom': '16px'}),
                            html.H3(
                                "Incident Saved Successfully!",
                                style={
                                    'fontSize': '24px',
                                    'fontWeight': '700',
                                    'color': '#1e293b',
                                    'marginBottom': '8px',
                                    'fontFamily': "'Poppins', sans-serif"
                                }
                            ),
                            html.P(
                                "The incident has been saved to the list.",
                                style={
                                    'fontSize': '14px',
                                    'color': '#64748b',
                                    'marginBottom': '20px'
                                }
                            ),
                            html.Button(
                                "OK",
                                id="close-save-modal",
                                style={
                                    'padding': '10px 40px',
                                    'background': 'linear-gradient(135deg, #10b981, #059669)',
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': '10px',
                                    'cursor': 'pointer',
                                    'fontSize': '14px',
                                    'fontWeight': '600',
                                    'transition': 'all 0.3s ease'
                                }
                            )
                        ]
                    )
                ]
            ),
            
            # ==================== STORES ====================
            dcc.Store(id="incident-data-store", data={}),
            dcc.Download(id="download-pdf")
        ]
    )


def create_incidents_table(incidents):
    """Create the incidents table HTML"""
    if not incidents:
        return html.Div(
            "No incidents saved yet. Fill the form and click 'Save Incident'!",
            style={
                'padding': '30px',
                'textAlign': 'center',
                'color': '#94a3b8',
                'fontSize': '14px',
                'background': '#f8fafc',
                'borderRadius': '12px',
                'border': '1px dashed #e2e8f0'
            }
        )
    
    incidents = incidents[::-1]
    
    rows = []
    for i, inc in enumerate(incidents):
        incident_id = inc.get('id', i + 1)
        date = inc.get('incident', {}).get('date', 'N/A')
        injured = inc.get('injured', {}).get('name', 'Unknown')
        location = inc.get('incident', {}).get('location', 'N/A')
        
        rows.append(
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': '80px 1.5fr 1.8fr 1.8fr 120px',
                    'gap': '12px',
                    'padding': '10px 16px',
                    'borderBottom': '1px solid #eef2f6',
                    'alignItems': 'center',
                    'background': '#fafbff' if i % 2 == 0 else 'white',
                    'borderRadius': '8px'
                },
                children=[
                    html.Span(f"#{incident_id}", style={'fontWeight': '600', 'color': '#1e293b', 'fontSize': '13px'}),
                    html.Span(date, style={'color': '#475569', 'fontSize': '13px'}),
                    html.Span(injured, style={'fontWeight': '500', 'color': '#1e293b', 'fontSize': '13px'}),
                    html.Span(location, style={'color': '#475569', 'fontSize': '13px'}),
                    html.Button(
                        [html.I(className="fas fa-file-pdf", style={'marginRight': '6px'}), "PDF"],
                        id={"type": "download-incident-pdf", "index": i},
                        style={
                            'padding': '6px 14px',
                            'background': '#dc2626',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'fontSize': '12px',
                            'fontWeight': '500',
                            'transition': 'all 0.2s ease',
                            'width': '100%'
                        }
                    )
                ]
            )
        )
    
    header = html.Div(
        style={
            'display': 'grid',
            'gridTemplateColumns': '80px 1.5fr 1.8fr 1.8fr 120px',
            'gap': '12px',
            'padding': '10px 16px',
            'background': '#f1f5f9',
            'borderRadius': '8px',
            'marginBottom': '6px',
            'fontWeight': '600',
            'fontSize': '12px',
            'color': '#64748b',
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px'
        },
        children=[
            html.Span("ID"),
            html.Span("Date"),
            html.Span("Injured Person"),
            html.Span("Location"),
            html.Span("Action")
        ]
    )
    
    return html.Div([header] + rows)


def register_incident_investigation_callbacks(app):
    """Register callbacks for Incident Investigation page"""
    
    # File Upload Handler
    @app.callback(
        [Output("uploaded-files-list", "style"),
         Output("uploaded-file-name", "children"),
         Output("uploaded-file-size", "children"),
         Output("uploaded-file-data", "data")],
        Input("upload-document", "contents"),
        [State("upload-document", "filename"),
         State("upload-document", "last_modified")],
        prevent_initial_call=True
    )
    def handle_file_upload(contents, filename, last_modified):
        if contents is not None:
            file_size = len(contents) * 3 / 4
            if file_size > 10 * 1024 * 1024:
                return {'display': 'none'}, "File too large (max 10MB)", "", {}
            
            size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"
            
            file_data = {
                "filename": filename,
                "contents": contents,
                "size": size_str,
                "last_modified": last_modified
            }
            
            return {'display': 'block'}, filename, size_str, file_data
        
        return {'display': 'none'}, "", "", {}
    
    # Remove uploaded file
    @app.callback(
        [Output("uploaded-files-list", "style", allow_duplicate=True),
         Output("uploaded-file-data", "data", allow_duplicate=True)],
        Input("remove-uploaded-file", "n_clicks"),
        prevent_initial_call=True
    )
    def remove_uploaded_file(n_clicks):
        if n_clicks:
            return {'display': 'none'}, {}
        return {'display': 'none'}, {}
    
    # Save Incident
    @app.callback(
        [Output("incidents-list", "children"),
         Output("save-confirmation-modal", "style")],
        Input("save-incident-btn", "n_clicks"),
        [State("incident-date", "date"),
         State("incident-time", "value"),
         State("incident-day", "value"),
         State("incident-location", "value"),
         State("incident-weather", "value"),
         State("incident-description", "value"),
         State("nature-near-miss", "value"),
         State("nature-first-aid", "value"),
         State("nature-medical", "value"),
         State("nature-lti", "value"),
         State("nature-fatal", "value"),
         State("nature-property", "value"),
         State("nature-environmental", "value"),
         State("nature-unsafe", "value"),
         State("injured-name", "value"),
         State("injured-job", "value"),
         State("injured-dept", "value"),
         State("injured-contact", "value"),
         State("injured-duration", "value"),
         State("injured-nature", "value"),
         State("witness-name", "value"),
         State("witness-job", "value"),
         State("witness-dept", "value"),
         State("witness-contact", "value"),
         State("immediate-actions", "value"),
         State("contributing-factors", "value"),
         State("corrective-actions", "value"),
         State("investigator-name", "value"),
         State("investigator-signature", "value"),
         State("investigator-date", "date"),
         State("uploaded-file-data", "data"),
         State("document-description", "value")],
        prevent_initial_call=True
    )
    def save_incident(n_clicks, incident_date, incident_time, incident_day, 
                      incident_location, incident_weather, incident_description,
                      nature_near_miss, nature_first_aid, nature_medical, 
                      nature_lti, nature_fatal, nature_property, 
                      nature_environmental, nature_unsafe,
                      injured_name, injured_job, injured_dept, 
                      injured_contact, injured_duration, injured_nature,
                      witness_name, witness_job, witness_dept, witness_contact,
                      immediate_actions, contributing_factors, corrective_actions,
                      investigator_name, investigator_signature, investigator_date,
                      uploaded_file, document_description):
        
        if not n_clicks:
            return create_incidents_table(load_incidents()), {'display': 'none'}
        
        if not injured_name:
            return create_incidents_table(load_incidents()), {'display': 'none'}
        
        incidents = load_incidents()
        
        new_incident = {
            "id": len(incidents) + 1,
            "incident": {
                "date": incident_date,
                "time": incident_time,
                "day": incident_day,
                "location": incident_location,
                "weather": incident_weather,
                "description": incident_description,
                "nature": {
                    "near_miss": nature_near_miss,
                    "first_aid": nature_first_aid,
                    "medical": nature_medical,
                    "lti": nature_lti,
                    "fatal": nature_fatal,
                    "property": nature_property,
                    "environmental": nature_environmental,
                    "unsafe": nature_unsafe
                }
            },
            "injured": {
                "name": injured_name,
                "job": injured_job,
                "department": injured_dept,
                "contact": injured_contact,
                "duration": injured_duration,
                "nature_of_injury": injured_nature
            },
            "witness": {
                "name": witness_name,
                "job": witness_job,
                "department": witness_dept,
                "contact": witness_contact
            },
            "actions": {
                "immediate": immediate_actions,
                "contributing": contributing_factors,
                "corrective": corrective_actions
            },
            "investigation": {
                "name": investigator_name,
                "signature": investigator_signature,
                "date": investigator_date
            },
            "attachment": {
                "filename": uploaded_file.get("filename") if uploaded_file else None,
                "contents": uploaded_file.get("contents") if uploaded_file else None,
                "description": document_description if document_description else "No description"
            } if uploaded_file else None,
            "saved_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        incidents.append(new_incident)
        save_incidents(incidents)
        
        return create_incidents_table(incidents), {'display': 'flex'}
    
    # Close save confirmation modal
    @app.callback(
        Output("save-confirmation-modal", "style", allow_duplicate=True),
        Input("close-save-modal", "n_clicks"),
        prevent_initial_call=True
    )
    def close_save_modal(n_clicks):
        if n_clicks:
            return {'display': 'none'}
        return {'display': 'none'}
    
    # Download PDF with professional formatting
    @app.callback(
        Output("download-pdf", "data"),
        Input({"type": "download-incident-pdf", "index": dash.dependencies.ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def download_incident_pdf(n_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return None
        
        trigger = ctx.triggered[0]
        trigger_id = trigger["prop_id"].split(".")[0]
        
        try:
            import json as json_mod
            trigger_dict = json_mod.loads(trigger_id.replace("'", '"'))
            index = trigger_dict.get("index")
            
            incidents = load_incidents()
            incidents_reversed = incidents[::-1]
            
            if index is not None and index < len(incidents_reversed):
                inc = incidents_reversed[index]
                return generate_pdf_from_incident(inc)
        except Exception as e:
            print(f"Error: {e}")
        
        return None
    
    # Clear form after save
    @app.callback(
        [Output("incident-date", "date", allow_duplicate=True),
         Output("incident-time", "value", allow_duplicate=True),
         Output("incident-day", "value", allow_duplicate=True),
         Output("incident-location", "value", allow_duplicate=True),
         Output("incident-weather", "value", allow_duplicate=True),
         Output("incident-description", "value", allow_duplicate=True),
         Output("nature-near-miss", "value", allow_duplicate=True),
         Output("nature-first-aid", "value", allow_duplicate=True),
         Output("nature-medical", "value", allow_duplicate=True),
         Output("nature-lti", "value", allow_duplicate=True),
         Output("nature-fatal", "value", allow_duplicate=True),
         Output("nature-property", "value", allow_duplicate=True),
         Output("nature-environmental", "value", allow_duplicate=True),
         Output("nature-unsafe", "value", allow_duplicate=True),
         Output("injured-name", "value", allow_duplicate=True),
         Output("injured-job", "value", allow_duplicate=True),
         Output("injured-dept", "value", allow_duplicate=True),
         Output("injured-contact", "value", allow_duplicate=True),
         Output("injured-duration", "value", allow_duplicate=True),
         Output("injured-nature", "value", allow_duplicate=True),
         Output("witness-name", "value", allow_duplicate=True),
         Output("witness-job", "value", allow_duplicate=True),
         Output("witness-dept", "value", allow_duplicate=True),
         Output("witness-contact", "value", allow_duplicate=True),
         Output("immediate-actions", "value", allow_duplicate=True),
         Output("contributing-factors", "value", allow_duplicate=True),
         Output("corrective-actions", "value", allow_duplicate=True),
         Output("investigator-name", "value", allow_duplicate=True),
         Output("investigator-signature", "value", allow_duplicate=True),
         Output("investigator-date", "date", allow_duplicate=True),
         Output("uploaded-files-list", "style", allow_duplicate=True),
         Output("uploaded-file-data", "data", allow_duplicate=True),
         Output("document-description", "value", allow_duplicate=True)],
        Input("save-incident-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_form_after_save(n_clicks):
        if not n_clicks:
            return [None] * 33
        
        return [
            datetime.date.today(),
            "",
            "",
            "",
            "",
            "",
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            datetime.date.today(),
            {'display': 'none'},
            {},
            ""
        ]


def generate_pdf_from_incident(inc):
    """Generate professional PDF from incident data with proper formatting"""
    buffer = BytesIO()
    
    # Create PDF with proper margins - A4 Portrait
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=0.75*inch, 
        leftMargin=0.75*inch, 
        topMargin=0.75*inch, 
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # ==================== CUSTOM STYLES ====================
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1a237e'),
        alignment=TA_CENTER,
        spaceAfter=2,
        fontName='Helvetica-Bold'
    )
    
    report_id_style = ParagraphStyle(
        'ReportID',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#546e7a'),
        alignment=TA_CENTER,
        spaceAfter=16,
        fontName='Helvetica'
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#d32f2f'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#37474f'),
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    value_style = ParagraphStyle(
        'Value',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1a237e'),
        fontName='Helvetica',
        alignment=TA_LEFT
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#78909c'),
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # ==================== HEADER WITH LOGO ====================
    try:
        logo_path = "assets/Screenshot 2026-05-26 154737.png"
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.8*inch, height=0.8*inch)
            
            # Header table with logo and title - PROPERLY ALIGNED
            header_data = [
                [logo, Paragraph("INCIDENT INVESTIGATION REPORT", title_style)]
            ]
            header_table = Table(header_data, colWidths=[1.8*inch, 4.2*inch])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (1, 0), (1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(header_table)
        else:
            story.append(Paragraph("INCIDENT INVESTIGATION REPORT", title_style))
    except:
        story.append(Paragraph("INCIDENT INVESTIGATION REPORT", title_style))
    
    # ==================== REPORT ID ====================
    story.append(Paragraph(f"Report ID: #{inc.get('id', 'N/A')} | Generated: {datetime.datetime.now().strftime('%d %B %Y')}", report_id_style))
    
    # ==================== DIVIDER LINE ====================
    story.append(Spacer(1, 0.05*inch))
    
    # ==================== 1. INCIDENT DETAILS ====================
    story.append(Paragraph("1. INCIDENT DETAILS", section_style))
    
    incident_data = inc.get('incident', {})
    
    # Build nature string
    nature_data = incident_data.get('nature', {})
    nature_list = []
    if nature_data.get('near_miss'): nature_list.append("Near Miss")
    if nature_data.get('first_aid'): nature_list.append("First Aid Case")
    if nature_data.get('medical'): nature_list.append("Medical Treatment Case")
    if nature_data.get('lti'): nature_list.append("Lost Time Injury")
    if nature_data.get('fatal'): nature_list.append("Fatal Accident")
    if nature_data.get('property'): nature_list.append("Property Damage")
    if nature_data.get('environmental'): nature_list.append("Environmental Incident")
    if nature_data.get('unsafe'): nature_list.append("Unsafe Condition")
    nature_str = ", ".join(nature_list) if nature_list else "Not specified"
    
    # Create table with proper formatting - WELL ALIGNED
    data = [
        [Paragraph("Date of Incident:", label_style), Paragraph(str(incident_data.get('date', 'Not specified')), value_style)],
        [Paragraph("Time:", label_style), Paragraph(str(incident_data.get('time', 'Not specified')), value_style)],
        [Paragraph("Day of Week:", label_style), Paragraph(str(incident_data.get('day', 'Not specified')), value_style)],
        [Paragraph("Location:", label_style), Paragraph(str(incident_data.get('location', 'Not specified')), value_style)],
        [Paragraph("Weather Conditions:", label_style), Paragraph(str(incident_data.get('weather', 'Not specified')), value_style)],
        [Paragraph("Nature of Incident:", label_style), Paragraph(str(nature_str), value_style)],
        [Paragraph("Description:", label_style), Paragraph(str(incident_data.get('description', 'Not specified')), value_style)]
    ]
    
    table = Table(data, colWidths=[1.8*inch, 4.2*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ]))
    story.append(KeepTogether(table))
    story.append(Spacer(1, 0.08*inch))
    
    # ==================== 2. INJURED PERSON ====================
    injured = inc.get('injured', {})
    if injured.get('name'):
        story.append(Paragraph("2. INJURED PERSON DETAILS", section_style))
        
        data2 = [
            [Paragraph("Name:", label_style), Paragraph(str(injured.get('name', 'Not specified')), value_style)],
            [Paragraph("Job Title:", label_style), Paragraph(str(injured.get('job', 'Not specified')), value_style)],
            [Paragraph("Department:", label_style), Paragraph(str(injured.get('department', 'Not specified')), value_style)],
            [Paragraph("Contact Number:", label_style), Paragraph(str(injured.get('contact', 'Not specified')), value_style)],
            [Paragraph("Employment Duration:", label_style), Paragraph(str(injured.get('duration', 'Not specified')), value_style)],
            [Paragraph("Nature of Injury:", label_style), Paragraph(str(injured.get('nature_of_injury', 'Not specified')), value_style)]
        ]
        
        table2 = Table(data2, colWidths=[1.8*inch, 4.2*inch])
        table2.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        story.append(KeepTogether(table2))
        story.append(Spacer(1, 0.08*inch))
    
    # ==================== 3. WITNESS ====================
    witness = inc.get('witness', {})
    if witness.get('name'):
        story.append(Paragraph("3. WITNESS INFORMATION", section_style))
        
        data3 = [
            [Paragraph("Name:", label_style), Paragraph(str(witness.get('name', 'Not specified')), value_style)],
            [Paragraph("Job Title:", label_style), Paragraph(str(witness.get('job', 'Not specified')), value_style)],
            [Paragraph("Department:", label_style), Paragraph(str(witness.get('department', 'Not specified')), value_style)],
            [Paragraph("Contact Number:", label_style), Paragraph(str(witness.get('contact', 'Not specified')), value_style)]
        ]
        
        table3 = Table(data3, colWidths=[1.8*inch, 4.2*inch])
        table3.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        story.append(KeepTogether(table3))
        story.append(Spacer(1, 0.08*inch))
    
    # ==================== 4. ACTIONS ====================
    actions = inc.get('actions', {})
    if actions.get('immediate') or actions.get('contributing') or actions.get('corrective'):
        story.append(Paragraph("4. ACTIONS TAKEN", section_style))
        
        data4 = [
            [Paragraph("Immediate Actions:", label_style), Paragraph(str(actions.get('immediate', 'Not specified')), value_style)],
            [Paragraph("Contributing Factors:", label_style), Paragraph(str(actions.get('contributing', 'Not specified')), value_style)],
            [Paragraph("Corrective Actions:", label_style), Paragraph(str(actions.get('corrective', 'Not specified')), value_style)]
        ]
        
        table4 = Table(data4, colWidths=[1.8*inch, 4.2*inch])
        table4.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        story.append(KeepTogether(table4))
        story.append(Spacer(1, 0.08*inch))
    
    # ==================== 5. INVESTIGATION TEAM ====================
    investigation = inc.get('investigation', {})
    if investigation.get('name'):
        story.append(Paragraph("5. INVESTIGATION TEAM", section_style))
        
        data5 = [
            [Paragraph("Investigator Name:", label_style), Paragraph(str(investigation.get('name', 'Not specified')), value_style)],
            [Paragraph("Signature:", label_style), Paragraph(str(investigation.get('signature', 'Not specified')), value_style)],
            [Paragraph("Date:", label_style), Paragraph(str(investigation.get('date', 'Not specified')), value_style)]
        ]
        
        table5 = Table(data5, colWidths=[1.8*inch, 4.2*inch])
        table5.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        story.append(KeepTogether(table5))
        story.append(Spacer(1, 0.08*inch))
    
    # ==================== 6. ATTACHMENT ====================
    attachment = inc.get('attachment')
    if attachment and attachment.get('filename'):
        story.append(Paragraph("6. ATTACHED DOCUMENT", section_style))
        
        data6 = [
            [Paragraph("Filename:", label_style), Paragraph(str(attachment.get('filename', 'Not specified')), value_style)],
            [Paragraph("Description:", label_style), Paragraph(str(attachment.get('description', 'Not specified')), value_style)]
        ]
        
        table6 = Table(data6, colWidths=[1.8*inch, 4.2*inch])
        table6.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        story.append(KeepTogether(table6))
    
    # ==================== FOOTER ====================
    story.append(Spacer(1, 0.3*inch))
    
    # Add a line before footer
    story.append(Paragraph("_" * 80, footer_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(
        Paragraph(
            f"Generated on: {datetime.datetime.now().strftime('%d %B %Y at %H:%M')} | Report #{inc.get('id', 'N/A')} | Page 1",
            footer_style
        )
    )
    
    # ==================== BUILD PDF ====================
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return dcc.send_bytes(
        pdf_bytes,
        f"Incident_Report_{inc.get('id', 'N/A')}_{datetime.date.today().strftime('%Y%m%d')}.pdf"
    )