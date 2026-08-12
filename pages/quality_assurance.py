# pages/quality_assurance.py - Quality Assurance Page (4 Simple Cards)

import dash
from dash import html

def quality_assurance_page():
    """Quality Assurance Page - 4 Simple Cards"""
    
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
                        "Quality Assurance",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Internal Audit, Non-conformance, OPAL and PDCA Management",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # ========== 4 CARDS ==========
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '20px'
                },
                children=[
                    # Card 1: Internal Audit
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'border': '1px solid #e2e8f0',
                            'borderLeft': '5px solid #667eea',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.06)',
                            'transition': 'all 0.3s ease'
                        },
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '12px',
                                    'marginBottom': '10px'
                                },
                                children=[
                                    html.I(
                                        className="fas fa-search",
                                        style={'color': '#667eea', 'fontSize': '20px', 'width': '24px'}
                                    ),
                                    html.H3(
                                        "Internal Audit",
                                        style={
                                            'fontSize': '15px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'margin': 0
                                        }
                                    )
                                ]
                            ),
                            html.P(
                                "Plan, conduct and track internal audits for compliance and continuous improvement.",
                                style={
                                    'fontSize': '13px',
                                    'color': '#64748b',
                                    'margin': '0 0 12px 0',
                                    'lineHeight': '1.5'
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'gap': '14px',
                                    'flexWrap': 'wrap',
                                    'paddingTop': '10px',
                                    'borderTop': '1px solid #f1f5f9'
                                },
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.Span("●", style={'color': '#ef4444', 'fontSize': '10px'}),
                                            html.Span("5 Open", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.Span("●", style={'color': '#eab308', 'fontSize': '10px'}),
                                            html.Span("3 In Progress", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.Span("●", style={'color': '#10b981', 'fontSize': '10px'}),
                                            html.Span("2 Closed", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Card 2: OPAL - Org Process Assets Library
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'border': '1px solid #e2e8f0',
                            'borderLeft': '5px solid #10b981',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.06)',
                            'transition': 'all 0.3s ease'
                        },
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '12px',
                                    'marginBottom': '10px'
                                },
                                children=[
                                    html.I(
                                        className="fas fa-book",
                                        style={'color': '#10b981', 'fontSize': '20px', 'width': '24px'}
                                    ),
                                    html.H3(
                                        "OPAL - Org Process Assets Library",
                                        style={
                                            'fontSize': '15px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'margin': 0
                                        }
                                    )
                                ]
                            ),
                            html.P(
                                "Organizational Process Assets Library with policies, procedures, templates, and guidelines.",
                                style={
                                    'fontSize': '13px',
                                    'color': '#64748b',
                                    'margin': '0 0 12px 0',
                                    'lineHeight': '1.5'
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'gap': '12px',
                                    'flexWrap': 'wrap',
                                    'paddingTop': '10px',
                                    'borderTop': '1px solid #f1f5f9'
                                },
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.I(className="fas fa-file-alt", style={'color': '#10b981', 'fontSize': '12px'}),
                                            html.Span("5 Policies", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.I(className="fas fa-list", style={'color': '#10b981', 'fontSize': '12px'}),
                                            html.Span("12 Procedures", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.I(className="fas fa-copy", style={'color': '#10b981', 'fontSize': '12px'}),
                                            html.Span("8 Templates", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'display': 'flex', 'alignItems': 'center', 'gap': '5px'},
                                        children=[
                                            html.I(className="fas fa-edit", style={'color': '#10b981', 'fontSize': '12px'}),
                                            html.Span("6 Guidelines", style={'fontSize': '12px', 'color': '#1e293b'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Card 3: OPAL - Org Process Assets Library ISO
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'border': '1px solid #e2e8f0',
                            'borderLeft': '5px solid #f59e0b',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.06)',
                            'transition': 'all 0.3s ease'
                        },
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '12px',
                                    'marginBottom': '10px'
                                },
                                children=[
                                    html.I(
                                        className="fas fa-certificate",
                                        style={'color': '#f59e0b', 'fontSize': '20px', 'width': '24px'}
                                    ),
                                    html.H3(
                                        "OPAL - Org Process Assets Library ISO",
                                        style={
                                            'fontSize': '15px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'margin': 0
                                        }
                                    )
                                ]
                            ),
                            html.P(
                                "ISO compliant process assets library for quality management systems.",
                                style={
                                    'fontSize': '13px',
                                    'color': '#64748b',
                                    'margin': '0 0 12px 0',
                                    'lineHeight': '1.5'
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'gap': '6px',
                                    'paddingTop': '10px',
                                    'borderTop': '1px solid #f1f5f9'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'space-between',
                                            'padding': '5px 10px',
                                            'background': '#f8fafc',
                                            'borderRadius': '6px'
                                        },
                                        children=[
                                            html.Span("ISO 9001:2026", style={'fontSize': '12px', 'fontWeight': '600', 'color': '#1e293b'}),
                                            html.Span("Quality", style={'fontSize': '11px', 'color': '#64748b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'space-between',
                                            'padding': '5px 10px',
                                            'background': '#f8fafc',
                                            'borderRadius': '6px'
                                        },
                                        children=[
                                            html.Span("ISO 14001:2026", style={'fontSize': '12px', 'fontWeight': '600', 'color': '#1e293b'}),
                                            html.Span("Environmental", style={'fontSize': '11px', 'color': '#64748b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'space-between',
                                            'padding': '5px 10px',
                                            'background': '#f8fafc',
                                            'borderRadius': '6px'
                                        },
                                        children=[
                                            html.Span("ISO 45001:2026", style={'fontSize': '12px', 'fontWeight': '600', 'color': '#1e293b'}),
                                            html.Span("Health & Safety", style={'fontSize': '11px', 'color': '#64748b'})
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'space-between',
                                            'padding': '5px 10px',
                                            'background': '#f8fafc',
                                            'borderRadius': '6px'
                                        },
                                        children=[
                                            html.Span("ISO 27001:2026", style={'fontSize': '12px', 'fontWeight': '600', 'color': '#1e293b'}),
                                            html.Span("Information Security", style={'fontSize': '11px', 'color': '#64748b'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Card 4: PDCA - Plan Do Check Act
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'border': '1px solid #e2e8f0',
                            'borderLeft': '5px solid #8b5cf6',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.06)',
                            'transition': 'all 0.3s ease'
                        },
                        children=[
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '12px',
                                    'marginBottom': '10px'
                                },
                                children=[
                                    html.I(
                                        className="fas fa-sync-alt",
                                        style={'color': '#8b5cf6', 'fontSize': '20px', 'width': '24px'}
                                    ),
                                    html.H3(
                                        "PDCA - Plan Do Check Act",
                                        style={
                                            'fontSize': '15px',
                                            'fontWeight': '700',
                                            'color': '#1e293b',
                                            'margin': 0
                                        }
                                    )
                                ]
                            ),
                            html.P(
                                "Continuous improvement cycle for quality management and process optimization.",
                                style={
                                    'fontSize': '13px',
                                    'color': '#64748b',
                                    'margin': '0 0 12px 0',
                                    'lineHeight': '1.5'
                                }
                            ),
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(2, 1fr)',
                                    'gap': '6px',
                                    'paddingTop': '10px',
                                    'borderTop': '1px solid #f1f5f9'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'gap': '5px',
                                            'padding': '4px 8px',
                                            'background': '#eef2ff',
                                            'borderRadius': '4px'
                                        },
                                        children=[
                                            html.Span("📋", style={'fontSize': '12px'}),
                                            html.Span("Plan", style={'fontSize': '11px', 'fontWeight': '600', 'color': '#4f46e5'})
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'gap': '5px',
                                            'padding': '4px 8px',
                                            'background': '#ecfdf5',
                                            'borderRadius': '4px'
                                        },
                                        children=[
                                            html.Span("▶️", style={'fontSize': '12px'}),
                                            html.Span("Do", style={'fontSize': '11px', 'fontWeight': '600', 'color': '#059669'})
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'gap': '5px',
                                            'padding': '4px 8px',
                                            'background': '#fefce8',
                                            'borderRadius': '4px'
                                        },
                                        children=[
                                            html.Span("🔍", style={'fontSize': '12px'}),
                                            html.Span("Check", style={'fontSize': '11px', 'fontWeight': '600', 'color': '#d97706'})
                                        ]
                                    ),
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'gap': '5px',
                                            'padding': '4px 8px',
                                            'background': '#fef2f2',
                                            'borderRadius': '4px'
                                        },
                                        children=[
                                            html.Span("✅", style={'fontSize': '12px'}),
                                            html.Span("Act", style={'fontSize': '11px', 'fontWeight': '600', 'color': '#dc2626'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def register_qa_callbacks(app):
    """Register callbacks for Quality Assurance page"""
    # No callbacks needed for simple cards
    pass