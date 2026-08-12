from dash import html, dcc

def create_permit_modal():
    return html.Div(
        id="permit-modal", 
        className="modal", 
        style={"display": "none"}, 
        children=[
            html.Div(className="modal-overlay", children=[
                html.Div(className="modal-content", children=[
                    html.Div(className="modal-header", children=[
                        html.H2(id="modal-title", children="New Work Permit"),
                        html.I(className="fas fa-times modal-close", id="close-modal")
                    ]),
                    html.Div(className="modal-body", children=[
                        # Permit Type Selection
                        html.Div(className="form-group", children=[
                            html.Label("Permit Type", className="form-label"),
                            dcc.Dropdown(
                                id="permit-type-select",
                                options=[
                                    {"label": "Height Work Permit", "value": "height"},
                                    {"label": "Electrical Work Permit", "value": "electrical"},
                                    {"label": "Excavation Permit", "value": "excavation"}
                                ],
                                value="height",
                                clearable=False
                            )
                        ]),
                        
                        # Basic Details (Common for all)
                        html.Div(className="form-group", children=[
                            html.Label("Project Name", className="form-label"),
                            dcc.Input(id="project-name", type="text", className="form-input", placeholder="Enter project name")
                        ]),
                        
                        html.Div(className="form-group", children=[
                            html.Label("Contractor Name", className="form-label"),
                            dcc.Input(id="contractor-name", type="text", className="form-input", placeholder="Enter contractor name")
                        ]),
                        
                        html.Div(className="form-group", children=[
                            html.Label("Number of Workers", className="form-label"),
                            dcc.Input(id="num-workers", type="number", className="form-input", placeholder="Enter number of workers")
                        ]),
                        
                        html.Div(className="form-group", children=[
                            html.Label("Work Location", className="form-label"),
                            dcc.Input(id="work-location", type="text", className="form-input", placeholder="Enter exact location")
                        ]),
                        
                        html.Div(className="form-row", children=[
                            html.Div(className="form-group half", children=[
                                html.Label("Valid From Date", className="form-label"),
                                dcc.DatePickerSingle(
                                    id="valid-from-date",
                                    placeholder="Select date",
                                    className="form-datepicker",
                                    display_format="YYYY-MM-DD"
                                )
                            ]),
                            html.Div(className="form-group half", children=[
                                html.Label("Valid To Date", className="form-label"),
                                dcc.DatePickerSingle(
                                    id="valid-to-date",
                                    placeholder="Select date",
                                    className="form-datepicker",
                                    display_format="YYYY-MM-DD"
                                )
                            ])
                        ]),
                        
                        html.Div(className="form-row", children=[
                            html.Div(className="form-group half", children=[
                                html.Label("From Time", className="form-label"),
                                dcc.Input(id="from-time", type="text", className="form-input", placeholder="08:00", value="08:00")
                            ]),
                            html.Div(className="form-group half", children=[
                                html.Label("To Time", className="form-label"),
                                dcc.Input(id="to-time", type="text", className="form-input", placeholder="17:00", value="17:00")
                            ])
                        ]),
                        
                        html.Div(className="form-group", children=[
                            html.Label("Work Description", className="form-label"),
                            dcc.Textarea(id="work-description", className="form-textarea", placeholder="Describe the work to be performed")
                        ]),
                        
                        html.H3("Risk Assessment", style={"marginTop": "20px", "marginBottom": "15px"}),
                        
                        html.Div(className="form-group", children=[
                            dcc.Checklist(
                                id="risk-assessment-check",
                                options=[
                                    {"label": " Risk assessment done for work activity planned", "value": "risk_done"},
                                    {"label": " SOP available and communicated to all workers", "value": "sop_available"}
                                ],
                                value=[]
                            )
                        ]),
                        
                        # Dynamic Form Fields based on permit type
                        html.Div(id="dynamic-permit-fields")
                    ]),
                    
                    html.Div(className="modal-footer", children=[
                        html.Button("Cancel", id="cancel-modal", className="modal-btn cancel"),
                        html.Button("Submit Permit", id="submit-permit", className="modal-btn submit")
                    ])
                ])
            ])
        ]
    )