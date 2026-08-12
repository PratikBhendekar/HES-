from dash import html, dcc

def height_work_fields():
    return html.Div([
        html.H3("Height Work Declaration", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        dcc.Checklist(
            id="height-declaration",
            options=[
                {"label": " 1. All workers inducted, medically fit, and briefed on task/PPE", "value": "decl_1"},
                {"label": " 2. All workers trained on harness/PFAS use", "value": "decl_2"},
                {"label": " 3. Appropriate access/egress and anchor points provided", "value": "decl_3"},
                {"label": " 4. Area barricaded; no activity/vehicles below", "value": "decl_4"},
                {"label": " 5. No overhead electrical hazards; weather suitable", "value": "decl_5"},
                {"label": " 6. Rescue plan briefed and in place", "value": "decl_6"}
            ],
            value=[]
        ),
        
        html.H3("Equipment Compliance", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        dcc.Checklist(
            id="equipment-compliance",
            options=[
                {"label": " Scaffold compliant (inspected, decked, access, nets, isolated)", "value": "scaffold"},
                {"label": " MEWP compliant (operator certified, checks done, area clear)", "value": "mewp"},
                {"label": " Other Equipment (e.g., ladders/PFAS) compliant", "value": "other"}
            ],
            value=[]
        ),
        
        html.H3("Permit Open Signatures", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        html.Div(className="form-row", children=[
            html.Div(className="form-group third", children=[
                html.Label("Permit Requestor Name", className="form-label"),
                dcc.Input(id="requestor-name", type="text", className="form-input", placeholder="Name")
            ]),
            html.Div(className="form-group third", children=[
                html.Label("Permit Holder Name", className="form-label"),
                dcc.Input(id="holder-name", type="text", className="form-input", placeholder="Name")
            ]),
            html.Div(className="form-group third", children=[
                html.Label("Permit Approver Name", className="form-label"),
                dcc.Input(id="approver-name", type="text", className="form-input", placeholder="Name")
            ])
        ])
    ])

def electrical_work_fields():
    return html.Div([
        html.H3("Electrical Work Declaration", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        dcc.Checklist(
            id="electrical-declaration",
            options=[
                {"label": " 1. Verified all workers deployed at site medically fit to work", "value": "decl_1"},
                {"label": " 2. All workers have received job specific trainings", "value": "decl_2"},
                {"label": " 3. Workers deployed competent to get the job done as per SOP", "value": "decl_3"},
                {"label": " 4. PPE required to complete job are provided and are in good condition", "value": "decl_4"},
                {"label": " 5. All required permissions and licensed obtained", "value": "decl_5"},
                {"label": " 6. All hazards identified and control measures taken as mentioned in HIARO", "value": "decl_6"},
                {"label": " 7. LOTO implemented", "value": "decl_7"},
                {"label": " 8. All measuring tools calibrated and calibration certificate available", "value": "decl_8"},
                {"label": " 9. Emergency procedure communicated to all", "value": "decl_9"}
            ],
            value=[]
        ),
        
        html.H3("Permit Open Signatures", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        html.Div(className="form-row", children=[
            html.Div(className="form-group third", children=[
                html.Label("Permit Requestor Name", className="form-label"),
                dcc.Input(id="requestor-name", type="text", className="form-input", placeholder="Name")
            ]),
            html.Div(className="form-group third", children=[
                html.Label("Permit Holder Name", className="form-label"),
                dcc.Input(id="holder-name", type="text", className="form-input", placeholder="Name")
            ]),
            html.Div(className="form-group third", children=[
                html.Label("Permit Approver Name", className="form-label"),
                dcc.Input(id="approver-name", type="text", className="form-input", placeholder="Name")
            ])
        ])
    ])

def excavation_fields():
    return html.Div([
        html.H3("Excavation Declaration", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        dcc.Checklist(
            id="excavation-declaration",
            options=[
                {"label": " 1. Underground services located and marked", "value": "decl_1"},
                {"label": " 2. Excavation greater than 1.5m - shoring/benching provided", "value": "decl_2"},
                {"label": " 3. Safe means of access/egress provided", "value": "decl_3"},
                {"label": " 4. Excavation protected from vehicle collision", "value": "decl_4"},
                {"label": " 5. Excavated material placed at safe distance", "value": "decl_5"},
                {"label": " 6. Atmospheric testing done if required", "value": "decl_6"}
            ],
            value=[]
        ),
        
        html.H3("Permit Open Signatures", style={"marginTop": "20px", "marginBottom": "15px"}),
        
        html.Div(className="form-row", children=[
            html.Div(className="form-group third", children=[
                html.Label("Permit Requestor Name", className="form-label"),
                dcc.Input(id="requestor-name", type="text", className="form-input", placeholder="Name")
            ]),
            html.Div(className="form-group third", children=[
                html.Label("Permit Holder Name", className="form-label"),
                dcc.Input(id="holder-name", type="text", className="form-input", placeholder="Name")
            ]),
            html.Div(className="form-group third", children=[
                html.Label("Permit Approver Name", className="form-label"),
                dcc.Input(id="approver-name", type="text", className="form-input", placeholder="Name")
            ])
        ])
    ])