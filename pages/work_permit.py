# pages/work_permit.py - Work Permit Page with Consistent Styling

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
import datetime
import uuid
from flask import session

from components.modal import create_permit_modal
from services.pdf_generator import generate_permit_pdf

# Store for permits (in production, use database)
permits_db = []

def work_permit_page():
    # Get current permits
    now = datetime.datetime.now()
    
    # Stats calculations
    active_permits = len([p for p in permits_db if p.get('status') == 'active'])
    pending_permits = len([p for p in permits_db if p.get('status') == 'pending'])
    completed_permits = len([p for p in permits_db if p.get('status') == 'completed'])
    expiring_soon = len([p for p in permits_db if p.get('status') == 'active' and p.get('valid_to') and 
                         (datetime.datetime.strptime(p['valid_to'], '%Y-%m-%d') - now).days <= 2])
    
    # Group permits by type
    height_permits = [p for p in permits_db if p.get('type') == 'height' and p.get('status') == 'active']
    electrical_permits = [p for p in permits_db if p.get('type') == 'electrical' and p.get('status') == 'active']
    excavation_permits = [p for p in permits_db if p.get('type') == 'excavation' and p.get('status') == 'active']
    
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            # Simple Header
            html.Div(
                style={'marginBottom': '24px'},
                children=[
                    html.H1(
                        "Work Permit System",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Manage and track all work permits across the organization",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # Statistics Cards - with colored top bar
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '20px',
                    'marginBottom': '24px'
                },
                children=[
                    # Active Permits Card - Blue
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#3b82f6'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '32px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(active_permits)
                                            ),
                                            html.I(
                                                className="fas fa-file-alt",
                                                style={'color': '#3b82f6', 'fontSize': '28px'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        "Active Permits",
                                        style={'fontSize': '14px', 'color': '#64748b', 'marginTop': '12px', 'fontWeight': '500'}
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Pending Approval Card - Yellow
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#eab308'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '32px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(pending_permits)
                                            ),
                                            html.I(
                                                className="fas fa-clock",
                                                style={'color': '#eab308', 'fontSize': '28px'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        "Pending Approval",
                                        style={'fontSize': '14px', 'color': '#64748b', 'marginTop': '12px', 'fontWeight': '500'}
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Completed Card - Green
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#10b981'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '32px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(completed_permits)
                                            ),
                                            html.I(
                                                className="fas fa-check-circle",
                                                style={'color': '#10b981', 'fontSize': '28px'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        "Completed",
                                        style={'fontSize': '14px', 'color': '#64748b', 'marginTop': '12px', 'fontWeight': '500'}
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Expiring Soon Card - Red
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#dc2626'}),
                            html.Div(
                                style={'padding': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '32px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(expiring_soon)
                                            ),
                                            html.I(
                                                className="fas fa-exclamation-triangle",
                                                style={'color': '#dc2626', 'fontSize': '28px'}
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        "Expiring Soon",
                                        style={'fontSize': '14px', 'color': '#64748b', 'marginTop': '12px', 'fontWeight': '500'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Search and New Permit Button
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px',
                    'marginBottom': '20px',
                    'border': '1px solid #e9ecef',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'flexWrap': 'wrap',
                    'gap': '15px'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'gap': '15px', 'alignItems': 'center', 'flex': '1'},
                        children=[
                            html.Div(
                                style={'position': 'relative', 'flex': '1', 'maxWidth': '300px'},
                                children=[
                                    html.I(
                                        className="fas fa-search",
                                        style={'position': 'absolute', 'left': '12px', 'top': '50%', 'transform': 'translateY(-50%)', 'color': '#94a3b8', 'fontSize': '14px'}
                                    ),
                                    dcc.Input(
                                        id="permit-search",
                                        type="text",
                                        placeholder="Search permits...",
                                        style={
                                            'width': '100%',
                                            'padding': '8px 12px 8px 35px',
                                            'borderRadius': '8px',
                                            'border': '1px solid #e2e8f0',
                                            'fontSize': '13px'
                                        }
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Button(
                        ["+ New Permit", html.I(className="fas fa-plus", style={'marginLeft': '8px'})],
                        id="open-modal-btn",
                        style={
                            'padding': '8px 20px',
                            'background': '#667eea',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '8px',
                            'cursor': 'pointer',
                            'fontSize': '13px',
                            'fontWeight': '500'
                        }
                    )
                ]
            ),
            
            # Permit Categories Section
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden',
                    'marginBottom': '24px'
                },
                children=[
                    html.Div(
                        style={
                            'padding': '16px 20px',
                            'borderBottom': '1px solid #eef2f6',
                            'background': '#fafbff'
                        },
                        children=[
                            html.H3(
                                "Permit Categories",
                                style={'margin': '0', 'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b'}
                            )
                        ]
                    ),
                    html.Div(
                        style={'padding': '20px'},
                        children=[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(3, 1fr)',
                                    'gap': '20px',
                                    'marginBottom': '20px'
                                },
                                children=[
                                    # Height Work Permits Card
                                    html.Div(
                                        style={
                                            'background': '#f8fafc',
                                            'borderRadius': '12px',
                                            'padding': '16px',
                                            'border': '1px solid #e2e8f0'
                                        },
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '40px',
                                                            'height': '40px',
                                                            'background': '#dbeafe',
                                                            'borderRadius': '10px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center'
                                                        },
                                                        children=html.I(className="fas fa-arrow-up", style={'color': '#3b82f6', 'fontSize': '18px'})
                                                    ),
                                                    html.Span(
                                                        f"{len(height_permits)} Active",
                                                        style={'background': '#3b82f6', 'color': 'white', 'padding': '2px 8px', 'borderRadius': '20px', 'fontSize': '11px', 'fontWeight': '500'}
                                                    )
                                                ]
                                            ),
                                            html.H4("Work at Height Permits", style={'fontSize': '15px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '12px'}),
                                            html.Div(
                                                style={'marginBottom': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={'fontSize': '12px', 'color': '#64748b', 'padding': '8px 0'},
                                                        children=[
                                                            html.Div(
                                                                style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '6px 0'},
                                                                children=[
                                                                    html.Span(p.get('permit_no', 'N/A'), style={'fontWeight': '500'}),
                                                                    html.Span("Active", style={'color': '#10b981'})
                                                                ]
                                                            ) for p in height_permits[:3]
                                                        ] + ([html.Div("No active permits", style={'textAlign': 'center', 'padding': '20px', 'color': '#94a3b8'})] if not height_permits else [])
                                                    )
                                                ]
                                            ),
                                            html.Button(
                                                "View All Height Work",
                                                id="show-height-permits",
                                                style={'width': '100%', 'padding': '8px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            )
                                        ]
                                    ),
                                    
                                    # Electrical Permits Card
                                    html.Div(
                                        style={
                                            'background': '#f8fafc',
                                            'borderRadius': '12px',
                                            'padding': '16px',
                                            'border': '1px solid #e2e8f0'
                                        },
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '40px',
                                                            'height': '40px',
                                                            'background': '#fef3c7',
                                                            'borderRadius': '10px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center'
                                                        },
                                                        children=html.I(className="fas fa-bolt", style={'color': '#eab308', 'fontSize': '18px'})
                                                    ),
                                                    html.Span(
                                                        f"{len(electrical_permits)} Active",
                                                        style={'background': '#eab308', 'color': 'white', 'padding': '2px 8px', 'borderRadius': '20px', 'fontSize': '11px', 'fontWeight': '500'}
                                                    )
                                                ]
                                            ),
                                            html.H4("Electrical Work Permits", style={'fontSize': '15px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '12px'}),
                                            html.Div(
                                                style={'marginBottom': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={'fontSize': '12px', 'color': '#64748b', 'padding': '8px 0'},
                                                        children=[
                                                            html.Div(
                                                                style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '6px 0'},
                                                                children=[
                                                                    html.Span(p.get('permit_no', 'N/A'), style={'fontWeight': '500'}),
                                                                    html.Span("Active", style={'color': '#10b981'})
                                                                ]
                                                            ) for p in electrical_permits[:3]
                                                        ] + ([html.Div("No active permits", style={'textAlign': 'center', 'padding': '20px', 'color': '#94a3b8'})] if not electrical_permits else [])
                                                    )
                                                ]
                                            ),
                                            html.Button(
                                                "View All Electrical",
                                                id="show-electrical-permits",
                                                style={'width': '100%', 'padding': '8px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            )
                                        ]
                                    ),
                                    
                                    # Excavation Permits Card
                                    html.Div(
                                        style={
                                            'background': '#f8fafc',
                                            'borderRadius': '12px',
                                            'padding': '16px',
                                            'border': '1px solid #e2e8f0'
                                        },
                                        children=[
                                            html.Div(
                                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={
                                                            'width': '40px',
                                                            'height': '40px',
                                                            'background': '#ecfdf5',
                                                            'borderRadius': '10px',
                                                            'display': 'flex',
                                                            'alignItems': 'center',
                                                            'justifyContent': 'center'
                                                        },
                                                        children=html.I(className="fas fa-hard-hat", style={'color': '#10b981', 'fontSize': '18px'})
                                                    ),
                                                    html.Span(
                                                        f"{len(excavation_permits)} Active",
                                                        style={'background': '#10b981', 'color': 'white', 'padding': '2px 8px', 'borderRadius': '20px', 'fontSize': '11px', 'fontWeight': '500'}
                                                    )
                                                ]
                                            ),
                                            html.H4("Excavation Permits", style={'fontSize': '15px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '12px'}),
                                            html.Div(
                                                style={'marginBottom': '12px'},
                                                children=[
                                                    html.Div(
                                                        style={'fontSize': '12px', 'color': '#64748b', 'padding': '8px 0'},
                                                        children=[
                                                            html.Div(
                                                                style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '6px 0'},
                                                                children=[
                                                                    html.Span(p.get('permit_no', 'N/A'), style={'fontWeight': '500'}),
                                                                    html.Span("Active", style={'color': '#10b981'})
                                                                ]
                                                            ) for p in excavation_permits[:3]
                                                        ] + ([html.Div("No active permits", style={'textAlign': 'center', 'padding': '20px', 'color': '#94a3b8'})] if not excavation_permits else [])
                                                    )
                                                ]
                                            ),
                                            html.Button(
                                                "View All Excavation",
                                                id="show-excavation-permits",
                                                style={'width': '100%', 'padding': '8px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Quick Actions
                            html.Div(
                                style={
                                    'background': '#f8fafc',
                                    'borderRadius': '12px',
                                    'padding': '16px',
                                    'border': '1px solid #e2e8f0'
                                },
                                children=[
                                    html.H4("Quick Actions", style={'fontSize': '15px', 'fontWeight': '700', 'color': '#1e293b', 'marginBottom': '12px'}),
                                    html.Div(
                                        style={'display': 'flex', 'gap': '12px', 'flexWrap': 'wrap'},
                                        children=[
                                            html.Button(
                                                ["Height Work", html.I(className="fas fa-arrow-up", style={'marginLeft': '6px'})],
                                                id="quick-height",
                                                style={'padding': '8px 16px', 'background': '#3b82f6', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            ),
                                            html.Button(
                                                ["Electrical", html.I(className="fas fa-bolt", style={'marginLeft': '6px'})],
                                                id="quick-electrical",
                                                style={'padding': '8px 16px', 'background': '#eab308', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            ),
                                            html.Button(
                                                ["Excavation", html.I(className="fas fa-hard-hat", style={'marginLeft': '6px'})],
                                                id="quick-excavation",
                                                style={'padding': '8px 16px', 'background': '#10b981', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            ),
                                            html.Button(
                                                ["View All", html.I(className="fas fa-list", style={'marginLeft': '6px'})],
                                                id="quick-view-all",
                                                style={'padding': '8px 16px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px', 'fontWeight': '500'}
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Recent Permits Table
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'border': '1px solid #e9ecef',
                    'overflow': 'hidden'
                },
                children=[
                    html.Div(
                        style={
                            'padding': '16px 20px',
                            'borderBottom': '1px solid #eef2f6',
                            'background': '#fafbff',
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center'
                        },
                        children=[
                            html.H3(
                                "Recent Permit Applications",
                                style={'margin': '0', 'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b'}
                            ),
                            html.I(className="fas fa-download", style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '14px'})
                        ]
                    ),
                    html.Div(
                        style={'overflowX': 'auto', 'border': '1px solid #e2e8f0', 'borderRadius': '8px', 'margin': '20px'},
                        children=[
                            html.Table(
                                style={'width': '100%', 'borderCollapse': 'collapse'},
                                children=[
                                    html.Thead(
                                        html.Tr([
                                            html.Th("Permit ID", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Type", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Description", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Location", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Applicant", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Valid Until", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Status", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Actions", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc', 'width': '100px'})
                                        ])
                                    ),
                                    html.Tbody(id="permits-table-body", children=[
                                        html.Tr(
                                            children=[
                                                html.Td(p.get('permit_no', f"PERM-{i+1:03d}"), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px', 'fontWeight': '500'}),
                                                html.Td(
                                                    html.Span(
                                                        {'height': 'Height', 'electrical': 'Electrical', 'excavation': 'Excavation'}.get(p.get('type'), p.get('type')),
                                                        style={
                                                            'background': '#dbeafe' if p.get('type') == 'height' else '#fef3c7' if p.get('type') == 'electrical' else '#ecfdf5',
                                                            'color': '#1e40af' if p.get('type') == 'height' else '#b45309' if p.get('type') == 'electrical' else '#065f46',
                                                            'padding': '2px 8px',
                                                            'borderRadius': '12px',
                                                            'fontSize': '11px',
                                                            'fontWeight': '500'
                                                        }
                                                    ),
                                                    style={'padding': '10px', 'border': '1px solid #e2e8f0'}
                                                ),
                                                html.Td(p.get('description', 'N/A')[:40], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                                                html.Td(p.get('location', 'N/A'), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                                                html.Td(p.get('requestor_name', 'N/A'), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                                                html.Td(p.get('valid_to', 'N/A'), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                                                html.Td(
                                                    html.Span(
                                                        p.get('status', 'pending').capitalize(),
                                                        style={
                                                            'background': '#ecfdf5' if p.get('status') == 'active' else '#fefce8' if p.get('status') == 'pending' else '#f1f5f9',
                                                            'color': '#10b981' if p.get('status') == 'active' else '#eab308' if p.get('status') == 'pending' else '#64748b',
                                                            'padding': '4px 10px',
                                                            'borderRadius': '20px',
                                                            'fontSize': '11px',
                                                            'fontWeight': '600',
                                                            'display': 'inline-block'
                                                        }
                                                    ),
                                                    style={'padding': '10px', 'border': '1px solid #e2e8f0'}
                                                ),
                                                html.Td(
                                                    html.A("Download", href=f"/download-permit/{p['id']}", target="_blank", style={'color': '#667eea', 'textDecoration': 'none', 'fontWeight': '500'}),
                                                    style={'padding': '10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}
                                                )
                                            ]
                                        ) for i, p in enumerate(permits_db[-5:])
                                    ] + ([html.Tr(html.Td("No permits found", colSpan=8, style={'textAlign': 'center', 'padding': '40px', 'border': '1px solid #e2e8f0', 'color': '#94a3b8'}))] if not permits_db else [])
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Store for permit data
            dcc.Store(id="permit-store", data=permits_db),
            
            # Modal for new permit (imported from components)
            create_permit_modal()
        ]
    )


def register_work_permit_callbacks(app):
    
    @app.callback(
        [Output("permit-modal", "style"),
         Output("modal-title", "children"),
         Output("permit-type-select", "value")],
        [Input("open-modal-btn", "n_clicks"),
         Input("quick-height", "n_clicks"),
         Input("quick-electrical", "n_clicks"),
         Input("quick-excavation", "n_clicks"),
         Input("cancel-modal", "n_clicks"),
         Input("close-modal", "n_clicks")],
        [State("permit-modal", "style")]
    )
    def toggle_modal(open_clicks, height_clicks, elec_clicks, exc_clicks, cancel_clicks, close_clicks, current_style):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "none"}, "New Work Permit", "height"
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id in ["open-modal-btn", "quick-height", "quick-electrical", "quick-excavation"]:
            if button_id == "quick-height":
                return {"display": "flex"}, "New Height Work Permit", "height"
            elif button_id == "quick-electrical":
                return {"display": "flex"}, "New Electrical Work Permit", "electrical"
            elif button_id == "quick-excavation":
                return {"display": "flex"}, "New Excavation Permit", "excavation"
            else:
                return {"display": "flex"}, "New Work Permit", "height"
        else:
            return {"display": "none"}, "New Work Permit", "height"

    @app.callback(
        Output("dynamic-permit-fields", "children"),
        Input("permit-type-select", "value")
    )
    def update_dynamic_fields(permit_type):
        from components.forms import height_work_fields, electrical_work_fields, excavation_fields
        if permit_type == "height":
            return height_work_fields()
        elif permit_type == "electrical":
            return electrical_work_fields()
        elif permit_type == "excavation":
            return excavation_fields()
        return html.Div()

    @app.callback(
        [Output("permit-store", "data"),
         Output("permit-modal", "style", allow_duplicate=True),
         Output("permits-table-body", "children")],
        Input("submit-permit", "n_clicks"),
        [State("permit-type-select", "value"),
         State("project-name", "value"),
         State("contractor-name", "value"),
         State("num-workers", "value"),
         State("work-location", "value"),
         State("valid-from-date", "value"),
         State("valid-to-date", "value"),
         State("from-time", "value"),
         State("to-time", "value"),
         State("work-description", "value"),
         State("risk-assessment-check", "value"),
         State("requestor-name", "value"),
         State("holder-name", "value"),
         State("approver-name", "value"),
         State("height-declaration", "value"),
         State("electrical-declaration", "value"),
         State("excavation-declaration", "value"),
         State("equipment-compliance", "value")],
        prevent_initial_call=True
    )
    def submit_permit(n_clicks, permit_type, project, contractor, workers, location, 
                      from_date, to_date, from_time, to_time, description, risk_check,
                      requestor, holder, approver, height_decl, elec_decl, exc_decl, equipment):
        global permits_db
        
        if not n_clicks:
            return no_update, no_update, no_update
        
        # Generate permit number
        permit_no = f"{permit_type[:2].upper()}-{datetime.datetime.now().strftime('%Y%m%d')}-{len(permits_db)+1:03d}"
        
        # Create permit data
        permit = {
            "id": str(uuid.uuid4()),
            "type": permit_type,
            "permit_no": permit_no,
            "project": project or "",
            "contractor": contractor or "",
            "workers": workers or "",
            "location": location or "",
            "valid_from": from_date or datetime.datetime.now().strftime('%Y-%m-%d'),
            "valid_to": to_date or (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
            "time_from": from_time or "08:00",
            "time_to": to_time or "17:00",
            "description": description or "",
            "risk_assessment": "risk_done" in (risk_check or []),
            "sop_available": "sop_available" in (risk_check or []),
            "requestor_name": requestor or session.get('name', 'User'),
            "holder_name": holder or "",
            "approver_name": approver or "",
            "requestor_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "holder_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "approver_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "requestor_time": datetime.datetime.now().strftime('%H:%M'),
            "holder_time": datetime.datetime.now().strftime('%H:%M'),
            "approver_time": datetime.datetime.now().strftime('%H:%M'),
            "status": "active",
            "created_at": datetime.datetime.now().isoformat(),
            "doc_no": {
                "height": "IMS/EHS/FR/PTW/WAH",
                "electrical": "IMS/EHS/FR/PTW/ELEC",
                "excavation": "IMS/EHS/FR/PTW/EXC"
            }.get(permit_type, "IMS/EHS/FR/PTW")
        }
        
        # Add type-specific fields
        if permit_type == "height":
            for i in range(1, 7):
                permit[f"decl_{i}"] = f"decl_{i}" in (height_decl or [])
            permit["scaffold_compliant"] = "scaffold" in (equipment or [])
            permit["mewp_compliant"] = "mewp" in (equipment or [])
            permit["other_compliant"] = "other" in (equipment or [])
        elif permit_type == "electrical":
            for i in range(1, 10):
                permit[f"decl_{i}"] = f"decl_{i}" in (elec_decl or [])
        elif permit_type == "excavation":
            for i in range(1, 7):
                permit[f"decl_{i}"] = f"decl_{i}" in (exc_decl or [])
        
        # Add to database
        permits_db.append(permit)
        
        # Generate table rows
        rows = []
        for i, p in enumerate(permits_db[-5:]):
            status_style = {
                'background': '#ecfdf5' if p.get('status') == 'active' else '#fefce8' if p.get('status') == 'pending' else '#f1f5f9',
                'color': '#10b981' if p.get('status') == 'active' else '#eab308' if p.get('status') == 'pending' else '#64748b',
                'padding': '4px 10px',
                'borderRadius': '20px',
                'fontSize': '11px',
                'fontWeight': '600',
                'display': 'inline-block'
            }
            
            type_style = {
                'background': '#dbeafe' if p.get('type') == 'height' else '#fef3c7' if p.get('type') == 'electrical' else '#ecfdf5',
                'color': '#1e40af' if p.get('type') == 'height' else '#b45309' if p.get('type') == 'electrical' else '#065f46',
                'padding': '2px 8px',
                'borderRadius': '12px',
                'fontSize': '11px',
                'fontWeight': '500'
            }
            
            rows.append(html.Tr(children=[
                html.Td(p.get('permit_no', f"PERM-{i+1:03d}"), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px', 'fontWeight': '500'}),
                html.Td(
                    html.Span({'height': 'Height', 'electrical': 'Electrical', 'excavation': 'Excavation'}.get(p.get('type'), p.get('type')), style=type_style),
                    style={'padding': '10px', 'border': '1px solid #e2e8f0'}
                ),
                html.Td(p.get('description', 'N/A')[:40], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(p.get('location', 'N/A'), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(p.get('requestor_name', 'N/A'), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(p.get('valid_to', 'N/A'), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(html.Span(p.get('status', 'pending').capitalize(), style=status_style), style={'padding': '10px', 'border': '1px solid #e2e8f0'}),
                html.Td(html.A("Download", href=f"/download-permit/{p['id']}", target="_blank", style={'color': '#667eea', 'textDecoration': 'none', 'fontWeight': '500'}), style={'padding': '10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'})
            ]))
        
        if not rows:
            rows = [html.Tr(html.Td("No permits found", colSpan=8, style={'textAlign': 'center', 'padding': '40px', 'border': '1px solid #e2e8f0', 'color': '#94a3b8'}))]
        
        return permits_db, {"display": "none"}, rows