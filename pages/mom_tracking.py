# pages/mom_tracking.py - Minutes of Meeting Tracking Page (FIXED MODAL - NO SCROLLBAR)

from dash import html, dcc, Input, Output, State, callback_context, no_update
import dash
import datetime
import uuid

# Sample Data
sample_moms = [
    {
        "id": "mom-001",
        "mom_no": "MOM-20250415-001",
        "title": "Project Kickoff Meeting",
        "date": "2025-04-15",
        "time": "10:00 AM",
        "venue": "Conference Room A",
        "mode": "Physical",
        "chairperson": "John Doe (Ceinsys)",
        "secretary": "Jane Smith (Ceinsys)",
        "party3": "Mike Johnson (Client)",
        "agenda": ["Project initiation discussion", "Resource allocation", "Timeline planning"],
        "notes": "Project kickoff was successful. All stakeholders agreed on timelines.",
        "status": "In Progress",
        "follow_up_1_date": None,
        "follow_up_2_date": None,
        "created_by": "Admin",
        "created_at": "2025-04-15T10:30:00",
        "action_items": [
            {
                "id": "act-001",
                "action": "Prepare project plan",
                "responsible": "John Doe",
                "target_date": "2025-04-22",
                "status": "Pending",
                "follow_up_1_status": None,
                "follow_up_1_date": None,
                "follow_up_2_status": None,
                "follow_up_2_date": None,
                "evidence": None
            },
            {
                "id": "act-002",
                "action": "Setup development environment",
                "responsible": "Jane Smith",
                "target_date": "2025-04-20",
                "status": "In Progress",
                "follow_up_1_status": None,
                "follow_up_1_date": None,
                "follow_up_2_status": None,
                "follow_up_2_date": None,
                "evidence": None
            }
        ]
    },
    {
        "id": "mom-002",
        "mom_no": "MOM-20250410-002",
        "title": "Safety Committee Meeting",
        "date": "2025-04-10",
        "time": "2:00 PM",
        "venue": "Safety Hall",
        "mode": "Hybrid",
        "chairperson": "Sarah Wilson (Ceinsys)",
        "secretary": "Tom Brown (External)",
        "party3": "Safety Consultants",
        "agenda": ["Review of safety protocols", "Incident reports", "Training schedule"],
        "notes": "New safety protocols approved. Training scheduled for next month.",
        "status": "Follow-up 1",
        "follow_up_1_date": "2025-04-17",
        "follow_up_2_date": None,
        "created_by": "Admin",
        "created_at": "2025-04-10T14:15:00",
        "action_items": [
            {
                "id": "act-003",
                "action": "Update safety manual",
                "responsible": "Sarah Wilson",
                "target_date": "2025-04-17",
                "status": "Completed",
                "follow_up_1_status": "Completed",
                "follow_up_1_date": "2025-04-17",
                "follow_up_2_status": None,
                "follow_up_2_date": None,
                "evidence": "safety_manual_v2.pdf"
            }
        ]
    },
    {
        "id": "mom-003",
        "mom_no": "MOM-20250405-003",
        "title": "Vendor Evaluation Meeting",
        "date": "2025-04-05",
        "time": "11:30 AM",
        "venue": "Virtual",
        "mode": "Virtual",
        "chairperson": "Robert Chen (Ceinsys)",
        "secretary": "Lisa Wang (Ceinsys)",
        "party3": "Vendors Group",
        "agenda": ["Vendor shortlisting", "Contract terms", "Timeline discussion"],
        "notes": "Top 3 vendors shortlisted. Contract negotiation next week.",
        "status": "Completed",
        "follow_up_1_date": "2025-04-12",
        "follow_up_2_date": "2025-04-19",
        "created_by": "Admin",
        "created_at": "2025-04-05T11:45:00",
        "action_items": [
            {
                "id": "act-004",
                "action": "Send RFQ to shortlisted vendors",
                "responsible": "Robert Chen",
                "target_date": "2025-04-12",
                "status": "Completed",
                "follow_up_1_status": "Completed",
                "follow_up_1_date": "2025-04-12",
                "follow_up_2_status": "Completed",
                "follow_up_2_date": "2025-04-19",
                "evidence": "rfq_sent.pdf"
            }
        ]
    }
]

# Store for MoMs
moms_db = sample_moms.copy()

def mom_tracking_page():
    total_moms = len(moms_db)
    in_progress = len([m for m in moms_db if m['status'] == 'In Progress'])
    follow_up_1 = len([m for m in moms_db if m['status'] == 'Follow-up 1'])
    follow_up_2 = len([m for m in moms_db if m['status'] == 'Follow-up 2'])
    completed = len([m for m in moms_db if m['status'] == 'Completed'])
    
    overdue = 0
    today = datetime.datetime.now().date()
    for mom in moms_db:
        for action in mom['action_items']:
            if action['status'] not in ['Completed']:
                if action['target_date']:
                    target_date = datetime.datetime.strptime(action['target_date'], '%Y-%m-%d').date()
                    if target_date < today:
                        overdue += 1
    
    completion_rate = (completed / total_moms * 100) if total_moms > 0 else 0
    
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
                        "Minutes of Meeting (MoM) Tracking",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Track and manage meeting minutes with action items",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            # Statistics Cards
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(6, 1fr)',
                    'gap': '16px',
                    'marginBottom': '24px'
                },
                children=[
                    # Total MoMs
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#667eea'}),
                            html.Div(
                                style={'padding': '16px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(total_moms)
                                            ),
                                            html.I(className="fas fa-file-alt", style={'color': '#667eea', 'fontSize': '24px'})
                                        ]
                                    ),
                                    html.Div("Total MoMs", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '8px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    ),
                    # In Progress
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
                                style={'padding': '16px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(in_progress)
                                            ),
                                            html.I(className="fas fa-clock", style={'color': '#eab308', 'fontSize': '24px'})
                                        ]
                                    ),
                                    html.Div("In Progress", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '8px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    ),
                    # Follow-up 1
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
                                style={'padding': '16px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(follow_up_1)
                                            ),
                                            html.I(className="fas fa-calendar-check", style={'color': '#3b82f6', 'fontSize': '24px'})
                                        ]
                                    ),
                                    html.Div("Follow-up 1", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '8px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    ),
                    # Follow-up 2
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden'
                        },
                        children=[
                            html.Div(style={'height': '4px', 'background': '#6366f1'}),
                            html.Div(
                                style={'padding': '16px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(follow_up_2)
                                            ),
                                            html.I(className="fas fa-calendar-week", style={'color': '#6366f1', 'fontSize': '24px'})
                                        ]
                                    ),
                                    html.Div("Follow-up 2", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '8px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    ),
                    # Completed
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
                                style={'padding': '16px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(completed)
                                            ),
                                            html.I(className="fas fa-check-circle", style={'color': '#10b981', 'fontSize': '24px'})
                                        ]
                                    ),
                                    html.Div("Completed", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '8px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    ),
                    # Overdue
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
                                style={'padding': '16px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.Div(
                                                style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1e293b'},
                                                children=str(overdue)
                                            ),
                                            html.I(className="fas fa-exclamation-triangle", style={'color': '#dc2626', 'fontSize': '24px'})
                                        ]
                                    ),
                                    html.Div("Overdue Actions", style={'fontSize': '12px', 'color': '#64748b', 'marginTop': '8px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Progress Bar
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px',
                    'marginBottom': '20px',
                    'border': '1px solid #e9ecef'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '8px'},
                        children=[
                            html.Span("Overall Completion Rate", style={'fontSize': '13px', 'fontWeight': '600', 'color': '#475569'}),
                            html.Span(f"{completion_rate:.1f}%", style={'fontSize': '16px', 'fontWeight': '700', 'color': '#10b981'})
                        ]
                    ),
                    html.Div(
                        style={'background': '#e2e8f0', 'borderRadius': '20px', 'height': '8px', 'overflow': 'hidden'},
                        children=[
                            html.Div(style={'width': f"{completion_rate}%", 'background': '#10b981', 'height': '100%', 'borderRadius': '20px'})
                        ]
                    )
                ]
            ),
            
            # Filters Section
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '16px',
                    'marginBottom': '20px',
                    'border': '1px solid #e9ecef'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'gap': '15px', 'alignItems': 'flex-end', 'flexWrap': 'wrap'},
                        children=[
                            html.Div(
                                style={'flex': '1', 'minWidth': '200px'},
                                children=[
                                    html.Label("Search:", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                    dcc.Input(
                                        id="mom-search-input",
                                        type="text",
                                        placeholder="Search by MoM No, Title or Chairperson...",
                                        style={'width': '100%', 'padding': '8px 12px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}
                                    )
                                ]
                            ),
                            html.Div(
                                style={'flex': '1', 'minWidth': '180px'},
                                children=[
                                    html.Label("Status Filter:", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                    dcc.Dropdown(
                                        id="status-filter-dropdown",
                                        options=[
                                            {"label": "All", "value": "All"},
                                            {"label": "In Progress", "value": "In Progress"},
                                            {"label": "Follow-up 1", "value": "Follow-up 1"},
                                            {"label": "Follow-up 2", "value": "Follow-up 2"},
                                            {"label": "Completed", "value": "Completed"}
                                        ],
                                        value="All",
                                        clearable=False,
                                        style={'borderRadius': '8px'}
                                    )
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.Button(
                                        "Clear Filters",
                                        id="clear-filters-btn",
                                        style={'padding': '8px 20px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '8px', 'cursor': 'pointer', 'fontSize': '13px', 'fontWeight': '500', 'color': '#475569'}
                                    )
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.Button(
                                        "+ New MoM",
                                        id="new-mom-btn",
                                        style={'padding': '8px 20px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '8px', 'cursor': 'pointer', 'fontSize': '13px', 'fontWeight': '500'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # MoM Data Table
            html.Div(
                style={
                    'background': 'white',
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': '1px solid #e9ecef'
                },
                children=[
                    html.Div(
                        style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '16px', 'paddingBottom': '12px', 'borderBottom': '1px solid #eef2f6'},
                        children=[
                            html.H3("Minutes of Meeting Records", style={'margin': '0', 'fontSize': '16px', 'fontWeight': '700', 'color': '#1e293b'})
                        ]
                    ),
                    html.Div(
                        id="mom-table-container",
                        style={'overflowX': 'auto', 'border': '1px solid #e2e8f0', 'borderRadius': '8px'},
                        children=[
                            html.Table(
                                style={'width': '100%', 'borderCollapse': 'collapse'},
                                children=[
                                    html.Thead(
                                        html.Tr([
                                            html.Th("MoM No", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Title", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Date", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Venue", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Chairperson", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Status", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Follow-up Stage", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc'}),
                                            html.Th("Actions", style={'padding': '12px', 'border': '1px solid #e2e8f0', 'textAlign': 'center', 'fontSize': '13px', 'fontWeight': '700', 'background': '#f8fafc', 'width': '100px'})
                                        ])
                                    ),
                                    html.Tbody(id="mom-table-body")
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # NEW MOM MODAL - NO SCROLLBAR, SCROLLS ONLY WHEN NEEDED
            html.Div(
                id="mom-modal",
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'right': '0',
                    'bottom': '0',
                    'background': 'rgba(0,0,0,0.5)',
                    'zIndex': '1000',
                    'alignItems': 'center',
                    'justifyContent': 'center'
                },
                children=[
                    html.Div(
                        style={
                            'background': 'white',
                            'borderRadius': '12px',
                            'width': '90%',
                            'maxWidth': '800px',
                            'maxHeight': '90vh',
                            'overflowY': 'auto',
                            'boxShadow': '0 20px 25px -5px rgba(0,0,0,0.1)',
                            'scrollbarWidth': 'thin'
                        },
                        children=[
                            # Modal Header
                            html.Div(
                                style={'padding': '20px', 'borderBottom': '1px solid #e2e8f0', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                children=[
                                    html.H3("Create New Minutes of Meeting", style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}),
                                    html.I(className="fas fa-times", id="close-mom-modal", style={'cursor': 'pointer', 'color': '#94a3b8', 'fontSize': '20px'})
                                ]
                            ),
                            # Modal Body - SCROLLS ONLY WHEN CONTENT OVERFLOWS
                            html.Div(
                                style={'padding': '20px', 'maxHeight': 'calc(90vh - 80px)', 'overflowY': 'auto'},
                                children=[
                                    # Meeting Details
                                    html.H4("Meeting Details", style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '15px'}),
                                    html.Div(
                                        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '15px', 'marginBottom': '15px'},
                                        children=[
                                            html.Div([
                                                html.Label("Date", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.DatePickerSingle(id="mom-date", display_format="YYYY-MM-DD", style={'width': '100%'})
                                            ]),
                                            html.Div([
                                                html.Label("Time", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Input(id="mom-time", type="text", placeholder="10:00 AM", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                            ]),
                                            html.Div([
                                                html.Label("Venue", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Input(id="mom-venue", type="text", placeholder="Conference Room", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                            ]),
                                            html.Div([
                                                html.Label("Mode", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Dropdown(id="mom-mode", options=[{"label": "Physical", "value": "Physical"}, {"label": "Virtual", "value": "Virtual"}, {"label": "Hybrid", "value": "Hybrid"}], value="Physical", style={'borderRadius': '8px'})
                                            ])
                                        ]
                                    ),
                                    html.Div(style={'marginBottom': '15px'}, children=[
                                        html.Label("Title", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                        dcc.Input(id="mom-title", type="text", placeholder="Enter meeting title", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                    ]),
                                    
                                    # Attendees
                                    html.H4("Attendees", style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '15px'}),
                                    html.Div(
                                        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '15px', 'marginBottom': '15px'},
                                        children=[
                                            html.Div([
                                                html.Label("Party 1 (Ceinsys)", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Input(id="mom-chairperson", type="text", placeholder="Name", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                            ]),
                                            html.Div([
                                                html.Label("Party 2", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Input(id="mom-secretary", type="text", placeholder="Name", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                            ]),
                                            html.Div([
                                                html.Label("Party 3 (External)", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Input(id="mom-party3", type="text", placeholder="Name", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                            ])
                                        ]
                                    ),
                                    
                                    # Agenda
                                    html.H4("Agenda Points", style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '15px'}),
                                    html.Div(id="agenda-container", children=[
                                        html.Div(id="agenda-0", style={'display': 'flex', 'alignItems': 'center', 'gap': '8px', 'marginBottom': '8px'}, children=[
                                            html.Div("1.", style={'fontWeight': '600', 'width': '25px', 'color': '#1e293b'}),
                                            dcc.Input(id="agenda-text-0", type="text", placeholder="Enter agenda point", style={'flex': '1', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'}),
                                            html.Button(html.I(className="fas fa-trash"), id="remove-agenda-0", style={'background': '#fee2e2', 'border': 'none', 'padding': '6px 10px', 'borderRadius': '6px', 'cursor': 'pointer', 'color': '#dc2626'})
                                        ])
                                    ]),
                                    html.Button("+ Add Agenda Point", id="add-agenda-btn", style={'marginBottom': '15px', 'padding': '6px 12px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px'}),
                                    
                                    # Meeting Notes
                                    html.H4("Meeting Notes", style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '15px'}),
                                    dcc.Textarea(id="mom-notes", rows=3, placeholder="Enter meeting summary...", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'}),
                                    
                                    # Action Items
                                    html.H4("Action Items", style={'fontSize': '14px', 'fontWeight': '600', 'color': '#1e293b', 'marginBottom': '15px'}),
                                    html.Div(id="action-items-container", children=[
                                        html.Div(id="action-0", style={'background': '#f8fafc', 'padding': '12px', 'borderRadius': '8px', 'marginBottom': '12px'}, children=[
                                            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '8px'}, children=[
                                                html.Span("Action Item #1", style={'fontWeight': '600', 'fontSize': '12px', 'color': '#1e293b'}),
                                                html.Button(html.I(className="fas fa-trash"), id="remove-action-0", style={'background': '#fee2e2', 'border': 'none', 'padding': '5px 8px', 'borderRadius': '6px', 'cursor': 'pointer', 'color': '#dc2626'})
                                            ]),
                                            html.Div(style={'marginBottom': '8px'}, children=[
                                                html.Label("Action Description", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                dcc.Textarea(id="action-desc-0", rows=2, placeholder="Describe the action item", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                            ]),
                                            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '8px'}, children=[
                                                html.Div([
                                                    html.Label("Responsible", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                    dcc.Input(id="action-responsible-0", type="text", placeholder="Name", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                                                ]),
                                                html.Div([
                                                    html.Label("Target Date", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                    dcc.DatePickerSingle(id="action-target-0", display_format="YYYY-MM-DD", style={'width': '100%'})
                                                ]),
                                                html.Div([
                                                    html.Label("Status", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                                                    dcc.Dropdown(id="action-status-0", options=[{"label": "Pending", "value": "Pending"}, {"label": "In Progress", "value": "In Progress"}, {"label": "Completed", "value": "Completed"}], value="Pending", style={'borderRadius': '8px'})
                                                ])
                                            ])
                                        ])
                                    ]),
                                    html.Button("+ Add Action Item", id="add-action-btn", style={'padding': '6px 12px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '12px'})
                                ]
                            ),
                            # Modal Footer
                            html.Div(
                                style={'padding': '20px', 'borderTop': '1px solid #e2e8f0', 'display': 'flex', 'justifyContent': 'flex-end', 'gap': '12px'},
                                children=[
                                    html.Button("Cancel", id="cancel-mom-modal", style={'padding': '8px 20px', 'background': '#f1f5f9', 'border': '1px solid #e2e8f0', 'borderRadius': '8px', 'cursor': 'pointer', 'fontSize': '13px', 'fontWeight': '500', 'color': '#475569'}),
                                    html.Button("Create MoM", id="submit-mom-modal", style={'padding': '8px 20px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '8px', 'cursor': 'pointer', 'fontSize': '13px', 'fontWeight': '500'})
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # MoM Details Modal
            html.Div(
                id="mom-detail-modal",
                style={'display': 'none'},
                children=[
                    html.Div(
                        style={
                            'position': 'fixed',
                            'top': '0',
                            'left': '0',
                            'right': '0',
                            'bottom': '0',
                            'background': 'rgba(0,0,0,0.5)',
                            'zIndex': '1000',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        },
                        children=[
                            html.Div(
                                style={
                                    'background': 'white',
                                    'borderRadius': '12px',
                                    'width': '90%',
                                    'maxWidth': '900px',
                                    'maxHeight': '90vh',
                                    'overflowY': 'auto',
                                    'boxShadow': '0 20px 25px -5px rgba(0,0,0,0.1)',
                                    'scrollbarWidth': 'thin'
                                },
                                children=[
                                    html.Div(
                                        style={'padding': '20px', 'borderBottom': '1px solid #e2e8f0', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                                        children=[
                                            html.H3(id="detail-modal-title", style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700', 'color': '#1e293b'}),
                                            html.Button("✕", id="close-detail-modal", style={'background': 'none', 'border': 'none', 'fontSize': '20px', 'cursor': 'pointer', 'color': '#94a3b8'})
                                        ]
                                    ),
                                    html.Div(id="mom-detail-content", style={'padding': '20px', 'maxHeight': 'calc(90vh - 80px)', 'overflowY': 'auto'})
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Hidden stores
            dcc.Store(id="moms-store", data=moms_db),
            dcc.Store(id="agenda-count", data=1),
            dcc.Store(id="action-count", data=1),
            dcc.Store(id="selected-mom-id", data=None)
        ]
    )


def register_mom_callbacks(app):
    """Register callbacks for MoM Tracking"""
    
    @app.callback(
        Output("mom-table-body", "children"),
        [Input("moms-store", "data"),
         Input("mom-search-input", "value"),
         Input("status-filter-dropdown", "value")]
    )
    def update_mom_table(moms_data, search_term, status_filter):
        if not moms_data:
            return [html.Tr(html.Td("No MoMs found", colSpan=8, style={'textAlign': 'center', 'padding': '40px', 'border': '1px solid #e2e8f0'}))]
        
        filtered_moms = moms_data.copy()
        
        if search_term:
            search_lower = search_term.lower()
            filtered_moms = [m for m in filtered_moms if 
                           search_lower in m['mom_no'].lower() or 
                           search_lower in m['title'].lower() or 
                           search_lower in m['chairperson'].lower()]
        
        if status_filter != "All":
            filtered_moms = [m for m in filtered_moms if m['status'] == status_filter]
        
        rows = []
        for mom in filtered_moms:
            follow_up_stage = ""
            if mom['status'] == "Follow-up 1":
                follow_up_stage = f"Follow-up 1 (Due: {mom['follow_up_1_date']})" if mom['follow_up_1_date'] else "Follow-up 1"
            elif mom['status'] == "Follow-up 2":
                follow_up_stage = f"Follow-up 2 (Due: {mom['follow_up_2_date']})" if mom['follow_up_2_date'] else "Follow-up 2"
            elif mom['status'] == "Completed":
                follow_up_stage = "Closed"
            else:
                follow_up_stage = "-"
            
            status_colors = {
                "In Progress": {"bg": "#fefce8", "color": "#eab308", "text": "In Progress"},
                "Follow-up 1": {"bg": "#dbeafe", "color": "#3b82f6", "text": "Follow-up 1"},
                "Follow-up 2": {"bg": "#e0e7ff", "color": "#6366f1", "text": "Follow-up 2"},
                "Completed": {"bg": "#ecfdf5", "color": "#10b981", "text": "Completed"}
            }
            sc = status_colors.get(mom['status'], {"bg": "#f1f5f9", "color": "#64748b", "text": mom['status']})
            status_badge = html.Span(
                sc["text"],
                style={'background': sc["bg"], 'color': sc["color"], 'padding': '4px 10px', 'borderRadius': '20px', 'fontSize': '11px', 'fontWeight': '600', 'display': 'inline-block'}
            )
            
            rows.append(html.Tr([
                html.Td(mom['mom_no'], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px', 'fontWeight': '500'}),
                html.Td(mom['title'][:50] + "..." if len(mom['title']) > 50 else mom['title'], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(mom['date'], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(mom['venue'], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(mom['chairperson'], style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(status_badge, style={'padding': '10px', 'border': '1px solid #e2e8f0'}),
                html.Td(follow_up_stage, style={'padding': '10px', 'border': '1px solid #e2e8f0', 'fontSize': '13px'}),
                html.Td(
                    html.Button("View", id={"type": "view-mom", "index": mom['id']}, 
                              style={'padding': '5px 12px', 'background': '#667eea', 'color': 'white', 'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '500'}),
                    style={'padding': '10px', 'border': '1px solid #e2e8f0', 'textAlign': 'center'}
                )
            ]))
        
        if not rows:
            rows = [html.Tr(html.Td("No MoMs found matching criteria", colSpan=8, style={'textAlign': 'center', 'padding': '40px', 'border': '1px solid #e2e8f0', 'color': '#94a3b8'}))]
        
        return rows
    
    @app.callback(
        [Output("mom-search-input", "value"),
         Output("status-filter-dropdown", "value")],
        [Input("clear-filters-btn", "n_clicks")]
    )
    def clear_filters(n_clicks):
        if n_clicks:
            return "", "All"
        return no_update, no_update
    
    @app.callback(
        Output("mom-modal", "style"),
        [Input("new-mom-btn", "n_clicks"),
         Input("cancel-mom-modal", "n_clicks"),
         Input("close-mom-modal", "n_clicks")]
    )
    def toggle_mom_modal(new_clicks, cancel_clicks, close_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return {'display': 'none'}
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "new-mom-btn":
            return {'display': 'flex', 'position': 'fixed', 'top': '0', 'left': '0', 'right': '0', 'bottom': '0', 'background': 'rgba(0,0,0,0.5)', 'zIndex': '1000', 'alignItems': 'center', 'justifyContent': 'center'}
        else:
            return {'display': 'none'}
    
    @app.callback(
        [Output("agenda-container", "children", allow_duplicate=True),
         Output("agenda-count", "data")],
        [Input("add-agenda-btn", "n_clicks")],
        [State("agenda-container", "children"),
         State("agenda-count", "data")],
        prevent_initial_call=True
    )
    def add_agenda_point(n_clicks, current_agendas, agenda_count):
        if not n_clicks or not current_agendas:
            return current_agendas, agenda_count
        
        new_index = agenda_count
        new_agenda = html.Div(id=f"agenda-{new_index}", style={'display': 'flex', 'alignItems': 'center', 'gap': '8px', 'marginBottom': '8px'}, children=[
            html.Div(f"{new_index + 1}.", style={'fontWeight': '600', 'width': '25px', 'color': '#1e293b'}),
            dcc.Input(id=f"agenda-text-{new_index}", type="text", placeholder="Enter agenda point", style={'flex': '1', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'}),
            html.Button(html.I(className="fas fa-trash"), id=f"remove-agenda-{new_index}", style={'background': '#fee2e2', 'border': 'none', 'padding': '6px 10px', 'borderRadius': '6px', 'cursor': 'pointer', 'color': '#dc2626'})
        ])
        
        current_agendas.append(new_agenda)
        return current_agendas, agenda_count + 1
    
    @app.callback(
        [Output("action-items-container", "children", allow_duplicate=True),
         Output("action-count", "data")],
        [Input("add-action-btn", "n_clicks")],
        [State("action-items-container", "children"),
         State("action-count", "data")],
        prevent_initial_call=True
    )
    def add_action_item(n_clicks, current_actions, action_count):
        if not n_clicks or not current_actions:
            return current_actions, action_count
        
        new_index = action_count
        new_action = html.Div(id=f"action-{new_index}", style={'background': '#f8fafc', 'padding': '12px', 'borderRadius': '8px', 'marginBottom': '12px'}, children=[
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '8px'}, children=[
                html.Span(f"Action Item #{new_index + 1}", style={'fontWeight': '600', 'fontSize': '12px', 'color': '#1e293b'}),
                html.Button(html.I(className="fas fa-trash"), id=f"remove-action-{new_index}", style={'background': '#fee2e2', 'border': 'none', 'padding': '5px 8px', 'borderRadius': '6px', 'cursor': 'pointer', 'color': '#dc2626'})
            ]),
            html.Div(style={'marginBottom': '8px'}, children=[
                html.Label("Action Description", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                dcc.Textarea(id=f"action-desc-{new_index}", rows=2, placeholder="Describe the action item", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
            ]),
            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '8px'}, children=[
                html.Div([
                    html.Label("Responsible", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                    dcc.Input(id=f"action-responsible-{new_index}", type="text", placeholder="Name", style={'width': '100%', 'padding': '8px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                ]),
                html.Div([
                    html.Label("Target Date", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                    dcc.DatePickerSingle(id=f"action-target-{new_index}", display_format="YYYY-MM-DD", style={'width': '100%'})
                ]),
                html.Div([
                    html.Label("Status", style={'fontSize': '12px', 'fontWeight': '600', 'marginBottom': '5px', 'display': 'block', 'color': '#475569'}),
                    dcc.Dropdown(id=f"action-status-{new_index}", options=[{"label": "Pending", "value": "Pending"}, {"label": "In Progress", "value": "In Progress"}, {"label": "Completed", "value": "Completed"}], value="Pending", style={'borderRadius': '8px'})
                ])
            ])
        ])
        
        current_actions.append(new_action)
        return current_actions, action_count + 1
    
    @app.callback(
        Output("agenda-container", "children", allow_duplicate=True),
        Input({"type": "remove-agenda", "index": dash.dependencies.ALL}, "n_clicks"),
        [State("agenda-container", "children")],
        prevent_initial_call=True
    )
    def remove_agenda_point(clicks, current_agendas):
        ctx = callback_context
        if not ctx.triggered or not current_agendas:
            return current_agendas
        
        trigger = ctx.triggered[0]
        if trigger and trigger["prop_id"] != ".":
            try:
                import json
                trigger_str = trigger["prop_id"].split(".")[0]
                if trigger_str.startswith("{") and trigger_str.endswith("}"):
                    trigger_id = json.loads(trigger_str.replace("'", '"'))
                    index_to_remove = trigger_id.get("index")
                    if index_to_remove is not None:
                        new_agendas = [a for i, a in enumerate(current_agendas) if i != index_to_remove]
                        for i, agenda in enumerate(new_agendas):
                            if 'props' in agenda and 'children' in agenda['props']:
                                number_div = agenda['props']['children'][0]
                                if 'props' in number_div:
                                    number_div['props']['children'] = f"{i + 1}."
                        return new_agendas
            except:
                pass
        return current_agendas
    
    @app.callback(
        Output("action-items-container", "children", allow_duplicate=True),
        Input({"type": "remove-action", "index": dash.dependencies.ALL}, "n_clicks"),
        [State("action-items-container", "children")],
        prevent_initial_call=True
    )
    def remove_action_item(clicks, current_actions):
        ctx = callback_context
        if not ctx.triggered or not current_actions:
            return current_actions
        
        trigger = ctx.triggered[0]
        if trigger and trigger["prop_id"] != ".":
            try:
                import json
                trigger_str = trigger["prop_id"].split(".")[0]
                if trigger_str.startswith("{") and trigger_str.endswith("}"):
                    trigger_id = json.loads(trigger_str.replace("'", '"'))
                    index_to_remove = trigger_id.get("index")
                    if index_to_remove is not None:
                        new_actions = [a for i, a in enumerate(current_actions) if i != index_to_remove]
                        for i, action in enumerate(new_actions):
                            if 'props' in action and 'children' in action['props']:
                                header = action['props']['children'][0]
                                if 'props' in header and 'children' in header['props']:
                                    number_span = header['props']['children'][0]
                                    if 'props' in number_span:
                                        number_span['props']['children'] = f"Action Item #{i + 1}"
                        return new_actions
            except:
                pass
        return current_actions
    
    @app.callback(
        [Output("moms-store", "data"),
         Output("mom-modal", "style", allow_duplicate=True)],
        [Input("submit-mom-modal", "n_clicks")],
        [State("mom-date", "value"),
         State("mom-time", "value"),
         State("mom-venue", "value"),
         State("mom-mode", "value"),
         State("mom-title", "value"),
         State("mom-chairperson", "value"),
         State("mom-secretary", "value"),
         State("mom-party3", "value"),
         State("mom-notes", "value"),
         State("agenda-container", "children"),
         State("action-items-container", "children"),
         State("moms-store", "data")],
        prevent_initial_call=True
    )
    def submit_new_mom(n_clicks, date, time, venue, mode, title, chairperson, secretary, party3, notes, agendas, actions, current_moms):
        if not n_clicks or not current_moms:
            return no_update, no_update
        
        mom_no = f"MOM-{datetime.datetime.now().strftime('%Y%m%d')}-{len(current_moms)+1:03d}"
        
        agenda_list = []
        if agendas:
            for agenda in agendas:
                if agenda and 'props' in agenda and 'children' in agenda['props']:
                    text_input = agenda['props']['children'][1]
                    if text_input and 'props' in text_input and 'value' in text_input['props']:
                        text = text_input['props']['value']
                        if text:
                            agenda_list.append(text)
        
        action_items = []
        if actions:
            for action in actions:
                if action and 'props' in action:
                    try:
                        desc = ""
                        desc_div = action['props']['children'][1]
                        if desc_div and 'props' in desc_div and 'children' in desc_div['props']:
                            desc_textarea = desc_div['props']['children'][1]
                            if desc_textarea and 'props' in desc_textarea and 'value' in desc_textarea['props']:
                                desc = desc_textarea['props']['value']
                        
                        responsible = ""
                        form_row = action['props']['children'][2]['props']['children']
                        responsible_input = form_row[0]['props']['children'][1]
                        if responsible_input and 'props' in responsible_input and 'value' in responsible_input['props']:
                            responsible = responsible_input['props']['value']
                        
                        target_date = ""
                        target_picker = form_row[1]['props']['children'][1]
                        if target_picker and 'props' in target_picker and 'date' in target_picker['props']:
                            target_date = target_picker['props']['date']
                        
                        status = "Pending"
                        status_dropdown = form_row[2]['props']['children'][1]
                        if status_dropdown and 'props' in status_dropdown and 'value' in status_dropdown['props']:
                            status = status_dropdown['props']['value']
                        
                        if desc:
                            action_items.append({
                                "id": str(uuid.uuid4()),
                                "action": desc,
                                "responsible": responsible,
                                "target_date": target_date,
                                "status": status,
                                "follow_up_1_status": None,
                                "follow_up_1_date": target_date if target_date else None,
                                "follow_up_2_status": None,
                                "follow_up_2_date": None,
                                "evidence": None
                            })
                    except:
                        pass
        
        new_mom = {
            "id": str(uuid.uuid4()),
            "mom_no": mom_no,
            "title": title or "Untitled Meeting",
            "date": date or datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": time or "10:00 AM",
            "venue": venue or "Not specified",
            "mode": mode or "Physical",
            "chairperson": chairperson or "Not specified",
            "secretary": secretary or "Not specified",
            "party3": party3 or "Not specified",
            "agenda": agenda_list,
            "notes": notes or "",
            "status": "In Progress",
            "follow_up_1_date": None,
            "follow_up_2_date": None,
            "created_by": "Admin",
            "created_at": datetime.datetime.now().isoformat(),
            "action_items": action_items
        }
        
        current_moms.append(new_mom)
        return current_moms, {'display': 'none'}
    
    @app.callback(
        [Output("mom-detail-modal", "style"),
         Output("detail-modal-title", "children"),
         Output("mom-detail-content", "children"),
         Output("selected-mom-id", "data")],
        [Input({"type": "view-mom", "index": dash.dependencies.ALL}, "n_clicks")],
        [State("moms-store", "data")]
    )
    def view_mom_details(clicks, moms_data):
        ctx = callback_context
        if not ctx.triggered or not moms_data:
            return {'display': 'none'}, "", html.Div(), None
        
        trigger = ctx.triggered[0]
        if not trigger["value"]:
            return {'display': 'none'}, "", html.Div(), None
        
        try:
            import json
            trigger_str = trigger["prop_id"].split(".")[0]
            if trigger_str.startswith("{") and trigger_str.endswith("}"):
                trigger_id = json.loads(trigger_str.replace("'", '"'))
                mom_id = trigger_id.get("index")
            else:
                return {'display': 'none'}, "", html.Div(), None
        except:
            return {'display': 'none'}, "", html.Div(), None
        
        mom = next((m for m in moms_data if m['id'] == mom_id), None)
        if not mom:
            return {'display': 'none'}, "", html.Div(), None
        
        content = html.Div([
            html.Div(style={"marginBottom": "20px"}, children=[
                html.H4("Meeting Details", style={"fontSize": "14px", "fontWeight": "700", "color": "#1e293b", "marginBottom": "12px"}),
                html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "10px", "fontSize": "13px"}, children=[
                    html.Div([html.Strong("MoM No:"), html.Span(f" {mom['mom_no']}", style={"color": "#1e293b"})]),
                    html.Div([html.Strong("Title:"), html.Span(f" {mom['title']}", style={"color": "#1e293b"})]),
                    html.Div([html.Strong("Date:"), html.Span(f" {mom['date']}", style={"color": "#1e293b"})]),
                    html.Div([html.Strong("Time:"), html.Span(f" {mom['time']}", style={"color": "#1e293b"})]),
                    html.Div([html.Strong("Venue:"), html.Span(f" {mom['venue']}", style={"color": "#1e293b"})]),
                    html.Div([html.Strong("Mode:"), html.Span(f" {mom['mode']}", style={"color": "#1e293b"})])
                ])
            ]),
            html.Div(style={"marginBottom": "20px"}, children=[
                html.H4("Attendees", style={"fontSize": "14px", "fontWeight": "700", "color": "#1e293b", "marginBottom": "12px"}),
                html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "10px", "fontSize": "13px"}, children=[
                    html.Div(style={"background": "#f8fafc", "padding": "10px", "borderRadius": "8px"}, children=[html.Strong("Party 1:"), html.Span(f" {mom['chairperson']}")]),
                    html.Div(style={"background": "#f8fafc", "padding": "10px", "borderRadius": "8px"}, children=[html.Strong("Party 2:"), html.Span(f" {mom['secretary']}")]),
                    html.Div(style={"background": "#f8fafc", "padding": "10px", "borderRadius": "8px"}, children=[html.Strong("Party 3:"), html.Span(f" {mom['party3']}")])
                ])
            ]),
            html.Div(style={"marginBottom": "20px"}, children=[
                html.H4("Agenda", style={"fontSize": "14px", "fontWeight": "700", "color": "#1e293b", "marginBottom": "12px"}),
                html.Ul([html.Li(point, style={"padding": "4px 0", "fontSize": "13px"}) for point in mom['agenda']], style={"margin": "0", "paddingLeft": "20px"})
            ]),
            html.Div(style={"marginBottom": "20px"}, children=[
                html.H4("Meeting Notes", style={"fontSize": "14px", "fontWeight": "700", "color": "#1e293b", "marginBottom": "12px"}),
                html.P(mom['notes'] if mom['notes'] else "-", style={"fontSize": "13px", "color": "#475569", "lineHeight": "1.5"})
            ]),
            html.Div(style={"marginBottom": "20px"}, children=[
                html.H4("Action Items", style={"fontSize": "14px", "fontWeight": "700", "color": "#1e293b", "marginBottom": "12px"}),
                html.Div(style={"overflowX": "auto"}, children=[
                    html.Table(style={"width": "100%", "borderCollapse": "collapse"}, children=[
                        html.Thead(html.Tr([
                            html.Th("#", style={"padding": "10px", "border": "1px solid #e2e8f0", "fontSize": "12px", "fontWeight": "700"}),
                            html.Th("Action", style={"padding": "10px", "border": "1px solid #e2e8f0", "fontSize": "12px", "fontWeight": "700"}),
                            html.Th("Responsible", style={"padding": "10px", "border": "1px solid #e2e8f0", "fontSize": "12px", "fontWeight": "700"}),
                            html.Th("Target Date", style={"padding": "10px", "border": "1px solid #e2e8f0", "fontSize": "12px", "fontWeight": "700"}),
                            html.Th("Status", style={"padding": "10px", "border": "1px solid #e2e8f0", "fontSize": "12px", "fontWeight": "700"})
                        ])),
                        html.Tbody([
                            html.Tr([
                                html.Td(str(i+1), style={"padding": "8px", "border": "1px solid #e2e8f0", "fontSize": "12px"}),
                                html.Td(action['action'], style={"padding": "8px", "border": "1px solid #e2e8f0", "fontSize": "12px"}),
                                html.Td(action['responsible'], style={"padding": "8px", "border": "1px solid #e2e8f0", "fontSize": "12px"}),
                                html.Td(action['target_date'], style={"padding": "8px", "border": "1px solid #e2e8f0", "fontSize": "12px"}),
                                html.Td(
                                    html.Span(
                                        action['status'],
                                        style={
                                            'background': '#ecfdf5' if action['status'] == 'Completed' else '#fefce8' if action['status'] == 'In Progress' else '#f1f5f9',
                                            'color': '#10b981' if action['status'] == 'Completed' else '#eab308' if action['status'] == 'In Progress' else '#64748b',
                                            'padding': '2px 8px',
                                            'borderRadius': '12px',
                                            'fontSize': '11px',
                                            'fontWeight': '500'
                                        }
                                    ),
                                    style={"padding": "8px", "border": "1px solid #e2e8f0", "textAlign": "center"}
                                )
                            ]) for i, action in enumerate(mom['action_items'])
                        ])
                    ])
                ])
            ])
        ])
        
        return {'display': 'flex', 'position': 'fixed', 'top': '0', 'left': '0', 'right': '0', 'bottom': '0', 'background': 'rgba(0,0,0,0.5)', 'zIndex': '1000', 'alignItems': 'center', 'justifyContent': 'center'}, f"MoM Details: {mom['mom_no']}", content, mom_id
    
    @app.callback(
        Output("mom-detail-modal", "style", allow_duplicate=True),
        [Input("close-detail-modal", "n_clicks")],
        prevent_initial_call=True
    )
    def close_detail_modal(n_clicks):
        return {'display': 'none'}