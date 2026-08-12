# pages/training_feedback.py - Training Feedback Form with Professional PDF

import dash
from dash import html, dcc, Input, Output, State, callback_context, no_update
from datetime import datetime
import base64
import os
import io
from flask import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch

# File to store feedbacks
FEEDBACK_FILE = "training_feedbacks_data.json"

def load_all_feedbacks():
    """Load all saved feedbacks from file"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_feedback_to_file(employee_name, data):
    """Save feedback to file"""
    feedbacks = load_all_feedbacks()
    feedbacks[employee_name] = data
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, indent=2, ensure_ascii=False)

def training_feedback_page():
    """Training Feedback Form Page - Professional Style"""
    
    return html.Div([
        # Header
        html.Div(className="dashboard-header", children=[
            html.H1("Training Feedback", style={"fontSize": "24px", "fontWeight": "600", "color": "#1e293b", "margin": "0"}),
            html.Div(style={"display": "flex", "gap": "12px"}, children=[
                html.Button("← Back", id="back-to-procurement-fb", style={
                    "padding": "8px 18px",
                    "background": "white",
                    "border": "1px solid #e2e8f0",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                    "color": "#64748b",
                    "fontSize": "13px",
                    "fontWeight": "500"
                }),
                html.Button("Download PDF", id="download-feedback-pdf", style={
                    "padding": "8px 18px",
                    "background": "#dc2626",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                    "fontSize": "13px",
                    "fontWeight": "500"
                })
            ])
        ]),
        
        # Breadcrumb
        html.Div(style={"marginBottom": "20px", "fontSize": "13px", "color": "#64748b"}, children=[
            html.Span("Procurement", style={"color": "#64748b"}),
            html.Span(" / ", style={"margin": "0 5px", "color": "#cbd5e1"}),
            html.Span("Training Feedback", style={"color": "#667eea", "fontWeight": "500"})
        ]),
        
        # Search Section
        html.Div(style={
            "background": "white",
            "borderRadius": "12px",
            "padding": "20px",
            "marginBottom": "20px",
            "border": "1px solid #e9ecef"
        }, children=[
            html.Div(style={"display": "flex", "gap": "15px", "alignItems": "flex-end", "flexWrap": "wrap"}, children=[
                html.Div(style={"flex": "1", "minWidth": "250px"}, children=[
                    html.Label("Search Past Feedbacks", style={"fontSize": "12px", "fontWeight": "500", "marginBottom": "5px", "display": "block", "color": "#475569"}),
                    dcc.Input(type="text", id="search-past-feedback", placeholder="Enter Employee Name...", 
                             style={"width": "100%", "padding": "10px", "borderRadius": "6px", "border": "1px solid #e2e8f0", "fontSize": "13px"})
                ]),
                html.Div([
                    html.Button("Search", id="search-feedback-btn", style={
                        "padding": "10px 25px",
                        "background": "#667eea",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "fontSize": "13px",
                        "fontWeight": "500"
                    })
                ]),
                html.Div(id="feedback-search-status", style={"fontSize": "12px", "marginLeft": "10px"})
            ]),
            
            # Saved Feedback Display Card
            html.Div(id="saved-feedback-card", style={"display": "none", "marginTop": "20px", "background": "#f8fafc", "borderRadius": "8px", "padding": "15px", "border": "1px solid #e2e8f0"}, children=[
                html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "10px"}, children=[
                    html.H5("Previously Saved Feedback", style={"margin": "0", "fontSize": "14px", "color": "#1e293b"}),
                    html.Button("Load Data", id="load-feedback-data", style={"padding": "5px 15px", "background": "#10b981", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer", "fontSize": "11px"})
                ]),
                html.Div(id="saved-feedback-details", style={"fontSize": "12px", "color": "#475569"})
            ])
        ]),
        
        # Main Form Card
        html.Div(style={
            "background": "white",
            "borderRadius": "16px",
            "padding": "30px",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
            "border": "1px solid #e9ecef"
        }, children=[
            
            # Header with Logo
            html.Div(style={"textAlign": "center", "marginBottom": "30px"}, children=[
                html.Img(
                    src="/assets/Screenshot 2026-05-26 154737.png",
                    style={"height": "50px", "width": "auto", "marginBottom": "12px"}
                ),
                html.H2("Training Feedback Form", style={"margin": "0", "fontSize": "22px", "fontWeight": "600", "color": "#1e293b"}),
                html.Div("IMS/TRM/FDBK/V2.0", style={"color": "#94a3b8", "fontSize": "12px", "marginTop": "5px"})
            ]),
            
            # Employee Information
            html.Div(style={"marginBottom": "25px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "20px"
                }, children=[
                    html.H4("Employee Information", style={"margin": "0", "fontSize": "16px", "fontWeight": "600", "color": "#1e293b"})
                ]),
                
                html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "20px"}, children=[
                    html.Div([
                        html.Label("Employee Name", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "6px", "display": "block", "color": "#475569"}),
                        dcc.Input(type="text", id="emp-name", placeholder="Enter employee name", 
                                 style={"width": "100%", "padding": "10px", "borderRadius": "8px", "border": "1px solid #e2e8f0", "fontSize": "14px"})
                    ]),
                    html.Div([
                        html.Label("Date", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "6px", "display": "block", "color": "#475569"}),
                        dcc.DatePickerSingle(id="feedback-date", date=datetime.now().strftime("%Y-%m-%d"), display_format="DD-MM-YYYY",
                                            style={"width": "100%", "borderRadius": "8px"})
                    ]),
                    html.Div([
                        html.Label("Course Name", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "6px", "display": "block", "color": "#475569"}),
                        dcc.Input(type="text", id="course-name", placeholder="Enter course name", 
                                 style={"width": "100%", "padding": "10px", "borderRadius": "8px", "border": "1px solid #e2e8f0", "fontSize": "14px"})
                    ]),
                    html.Div([
                        html.Label("Trainer Name", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "6px", "display": "block", "color": "#475569"}),
                        dcc.Input(type="text", id="trainer-name", placeholder="Enter trainer name", 
                                 style={"width": "100%", "padding": "10px", "borderRadius": "8px", "border": "1px solid #e2e8f0", "fontSize": "14px"})
                    ])
                ])
            ]),
            
            # Rating Scale Info
            html.Div(style={
                "background": "#f8fafc", 
                "borderRadius": "12px", 
                "padding": "15px", 
                "marginBottom": "25px"
            }, children=[
                html.Div(style={"display": "flex", "justifyContent": "space-between", "textAlign": "center", "fontSize": "12px"}, children=[
                    html.Div(style={"flex": "1"}, children=[html.Div("1", style={"fontWeight": "bold", "color": "#dc2626"}), html.Small("Strongly Disagree")]),
                    html.Div(style={"flex": "1"}, children=[html.Div("2", style={"fontWeight": "bold", "color": "#ea580c"}), html.Small("Disagree")]),
                    html.Div(style={"flex": "1"}, children=[html.Div("3", style={"fontWeight": "bold", "color": "#ca8a04"}), html.Small("Agree")]),
                    html.Div(style={"flex": "1"}, children=[html.Div("4", style={"fontWeight": "bold", "color": "#16a34a"}), html.Small("Strongly Agree")])
                ])
            ]),
            
            # Section A - Objectives
            html.Div(style={"marginBottom": "25px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "15px"
                }, children=[
                    html.H4("A. Objectives", style={"margin": "0", "fontSize": "16px", "fontWeight": "600", "color": "#1e293b"})
                ]),
                _fb_row("obj1", "1. Objectives for this course were clearly stated and communicated."),
                _fb_row("obj2", "2. Overall, the session met its stated objectives.")
            ]),
            
            # Section B - Course Content
            html.Div(style={"marginBottom": "25px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "15px"
                }, children=[
                    html.H4("B. Course Content & Delivery", style={"margin": "0", "fontSize": "16px", "fontWeight": "600", "color": "#1e293b"})
                ]),
                _fb_row("content1", "1. The subject matter presented met the stated objectives."),
                _fb_row("content2", "2. The session length was appropriate to achieve the stated objective."),
                _fb_row("content3", "3. The course presentation content matched the course description.")
            ]),
            
            # Section C - Trainer Effectiveness
            html.Div(style={"marginBottom": "25px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "15px"
                }, children=[
                    html.H4("C. Trainer Effectiveness", style={"margin": "0", "fontSize": "16px", "fontWeight": "600", "color": "#1e293b"})
                ]),
                _fb_row("trainer1", "1. The Trainer was knowledgeable of the subject matter."),
                _fb_row("trainer2", "2. The Trainer demonstrated competency in presenting and facilitating the session."),
                _fb_row("trainer3", "3. The Trainer developed a good rapport with the session."),
                _fb_row("trainer4", "4. The Trainer did a good job of summarizing the content at the end."),
                _fb_row("trainer5", "5. I would like the opportunity to learn from this trainer again.")
            ]),
            
            # Section D - Open Ended Questions
            html.Div(style={"marginBottom": "25px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "15px"
                }, children=[
                    html.H4("D. Open Ended Questions", style={"margin": "0", "fontSize": "16px", "fontWeight": "600", "color": "#1e293b"})
                ]),
                html.Div(style={"marginBottom": "16px"}, children=[
                    html.Label("1. What did you like about this session?", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "8px", "display": "block", "color": "#475569"}),
                    dcc.Textarea(id="liked", placeholder="Enter your feedback...", 
                                style={"width": "100%", "padding": "10px", "borderRadius": "8px", "border": "1px solid #e2e8f0", "minHeight": "70px", "fontSize": "13px"})
                ]),
                html.Div(style={"marginBottom": "16px"}, children=[
                    html.Label("2. How could this session be improved?", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "8px", "display": "block", "color": "#475569"}),
                    dcc.Textarea(id="improved", placeholder="Enter suggestions...", 
                                style={"width": "100%", "padding": "10px", "borderRadius": "8px", "border": "1px solid #e2e8f0", "minHeight": "70px", "fontSize": "13px"})
                ])
            ]),
            
            # Section E - Signature
            html.Div(style={"marginBottom": "25px"}, children=[
                html.Div(style={
                    "borderLeft": "3px solid #667eea",
                    "paddingLeft": "12px",
                    "marginBottom": "15px"
                }, children=[
                    html.H4("E. Acknowledgement", style={"margin": "0", "fontSize": "16px", "fontWeight": "600", "color": "#1e293b"})
                ]),
                html.Div(style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}, children=[
                    html.Div(style={"flex": "1"}, children=[
                        html.Label("Signature", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "6px", "display": "block", "color": "#475569"}),
                        dcc.Input(type="text", id="signature", placeholder="Type your name", 
                                 style={"width": "100%", "padding": "10px", "borderRadius": "8px", "border": "1px solid #e2e8f0", "fontSize": "14px"})
                    ]),
                    html.Div(style={"flex": "1"}, children=[
                        html.Label("Date", style={"fontSize": "13px", "fontWeight": "500", "marginBottom": "6px", "display": "block", "color": "#475569"}),
                        dcc.DatePickerSingle(id="sign-date", date=datetime.now().strftime("%Y-%m-%d"), display_format="DD-MM-YYYY",
                                            style={"width": "100%", "borderRadius": "8px"})
                    ])
                ])
            ]),
            
            # Submit Button
            html.Div(style={"textAlign": "right", "marginTop": "10px"}, children=[
                html.Button("Submit Feedback", id="submit-feedback", style={
                    "padding": "10px 28px", 
                    "background": "#667eea", 
                    "color": "white", 
                    "border": "none", 
                    "borderRadius": "8px", 
                    "cursor": "pointer", 
                    "fontWeight": "500",
                    "fontSize": "14px"
                })
            ]),
            
            # Success Message
            html.Div(id="submit-success", style={"marginTop": "16px", "textAlign": "center", "fontSize": "13px"})
        ]),
        
        # PDF Download component
        dcc.Download(id="download-feedback-pdf-file"),
        dcc.Store(id="feedback-ratings-store", data={})
    ])

def _fb_row(id_name, label):
    """Create a feedback row with radio buttons"""
    return html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "14px", "flexWrap": "wrap", "padding": "4px 0"}, children=[
        html.Div(label, style={"flex": "2", "fontSize": "13px", "color": "#334155"}),
        html.Div(style={"display": "flex", "gap": "20px", "flex": "1", "alignItems": "center", "justifyContent": "flex-end"}, children=[
            html.Span("1", style={"fontSize": "12px", "color": "#dc2626"}),
            dcc.RadioItems(
                id=id_name, 
                options=[
                    {"label": "", "value": 1}, 
                    {"label": "", "value": 2},
                    {"label": "", "value": 3}, 
                    {"label": "", "value": 4}
                ], 
                labelStyle={"display": "inline-block", "marginRight": "20px"}, 
                inline=True,
                style={"display": "flex", "gap": "25px"}
            ),
            html.Span("4", style={"fontSize": "12px", "color": "#10b981"})
        ])
    ])

def register_training_feedback_callbacks(app):
    """Register training feedback callbacks"""
    
    # Submit form
    @app.callback(
        Output("submit-success", "children"),
        [Input("submit-feedback", "n_clicks")],
        [State("emp-name", "value"),
         State("course-name", "value"),
         State("trainer-name", "value"),
         State("feedback-date", "date"),
         State("obj1", "value"),
         State("obj2", "value"),
         State("content1", "value"),
         State("content2", "value"),
         State("content3", "value"),
         State("trainer1", "value"),
         State("trainer2", "value"),
         State("trainer3", "value"),
         State("trainer4", "value"),
         State("trainer5", "value"),
         State("liked", "value"),
         State("improved", "value"),
         State("signature", "value"),
         State("sign-date", "date")]
    )
    def submit_form(n_clicks, emp_name, course_name, trainer_name, fb_date, 
                    obj1, obj2, c1, c2, c3, t1, t2, t3, t4, t5, liked, improved, signature, sign_date):
        if not n_clicks:
            return ""
        
        if not emp_name:
            return html.Div("❌ Please enter employee name", style={"color": "#dc2626", "fontWeight": "500", "padding": "10px", "background": "#fef2f2", "borderRadius": "8px"})
        
        # Calculate average rating
        ratings = [obj1, obj2, c1, c2, c3, t1, t2, t3, t4, t5]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            avg_rating = sum(valid_ratings) / len(valid_ratings)
            if avg_rating >= 3.5:
                overall = "Excellent"
                color = "#10b981"
            elif avg_rating >= 2.5:
                overall = "Good"
                color = "#16a34a"
            else:
                overall = "Needs Improvement"
                color = "#ea580c"
        else:
            overall = "No ratings"
            color = "#94a3b8"
        
        # Save to file
        feedback_data = {
            "employee_name": emp_name,
            "course_name": course_name,
            "trainer_name": trainer_name,
            "feedback_date": fb_date,
            "ratings": {
                "obj1": obj1, "obj2": obj2,
                "content1": c1, "content2": c2, "content3": c3,
                "trainer1": t1, "trainer2": t2, "trainer3": t3, "trainer4": t4, "trainer5": t5
            },
            "liked": liked,
            "improved": improved,
            "signature": signature,
            "sign_date": sign_date,
            "overall_rating": overall,
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_feedback_to_file(emp_name, feedback_data)
        
        return html.Div(f"✅ Feedback submitted successfully! Overall: {overall}", 
                       style={"color": color, "fontWeight": "500", "padding": "10px", "background": f"{color}15", "borderRadius": "8px"})
    
    # Search past feedback
    @app.callback(
        [Output("saved-feedback-card", "style"),
         Output("saved-feedback-details", "children"),
         Output("feedback-search-status", "children")],
        Input("search-feedback-btn", "n_clicks"),
        State("search-past-feedback", "value")
    )
    def search_past_feedback(n_clicks, emp_name):
        if not n_clicks or not emp_name:
            return {"display": "none"}, "", ""
        
        feedbacks = load_all_feedbacks()
        if emp_name in feedbacks:
            data = feedbacks[emp_name]
            details = html.Div([
                html.Div(f"Course: {data.get('course_name', 'N/A')}", style={"marginBottom": "5px"}),
                html.Div(f"Trainer: {data.get('trainer_name', 'N/A')}", style={"marginBottom": "5px"}),
                html.Div(f"Feedback Date: {data.get('feedback_date', 'N/A')}", style={"marginBottom": "5px"}),
                html.Div(f"Overall Rating: {data.get('overall_rating', 'N/A')}", style={"marginBottom": "5px", "fontWeight": "bold", "color": "#667eea"}),
                html.Div(f"Saved On: {data.get('saved_date', 'N/A')}", style={"marginBottom": "5px"})
            ])
            return {"display": "block", "marginTop": "20px", "background": "#f8fafc", "borderRadius": "8px", "padding": "15px", "border": "1px solid #e2e8f0"}, details, f"✅ Found feedback for {emp_name}"
        else:
            return {"display": "none"}, "", f"❌ No feedback found for {emp_name}"
    
    # Load saved data into form
    @app.callback(
        [Output("emp-name", "value", allow_duplicate=True),
         Output("course-name", "value", allow_duplicate=True),
         Output("trainer-name", "value", allow_duplicate=True),
         Output("feedback-date", "date", allow_duplicate=True),
         Output("obj1", "value", allow_duplicate=True),
         Output("obj2", "value", allow_duplicate=True),
         Output("content1", "value", allow_duplicate=True),
         Output("content2", "value", allow_duplicate=True),
         Output("content3", "value", allow_duplicate=True),
         Output("trainer1", "value", allow_duplicate=True),
         Output("trainer2", "value", allow_duplicate=True),
         Output("trainer3", "value", allow_duplicate=True),
         Output("trainer4", "value", allow_duplicate=True),
         Output("trainer5", "value", allow_duplicate=True),
         Output("liked", "value", allow_duplicate=True),
         Output("improved", "value", allow_duplicate=True),
         Output("signature", "value", allow_duplicate=True),
         Output("sign-date", "date", allow_duplicate=True),
         Output("saved-feedback-card", "style", allow_duplicate=True),
         Output("feedback-search-status", "children", allow_duplicate=True)],
        Input("load-feedback-data", "n_clicks"),
        State("search-past-feedback", "value"),
        prevent_initial_call=True
    )
    def load_saved_data(n_clicks, emp_name):
        if not n_clicks or not emp_name:
            return [None] * 20
        
        feedbacks = load_all_feedbacks()
        if emp_name in feedbacks:
            data = feedbacks[emp_name]
            ratings = data.get('ratings', {})
            return (
                emp_name,
                data.get('course_name'), data.get('trainer_name'), data.get('feedback_date'),
                ratings.get('obj1'), ratings.get('obj2'),
                ratings.get('content1'), ratings.get('content2'), ratings.get('content3'),
                ratings.get('trainer1'), ratings.get('trainer2'), ratings.get('trainer3'),
                ratings.get('trainer4'), ratings.get('trainer5'),
                data.get('liked'), data.get('improved'),
                data.get('signature'), data.get('sign_date'),
                {"display": "none"}, "✅ Data loaded successfully!"
            )
        return [None] * 20
    
    # PDF Download - Professional PDF generation
    @app.callback(
        Output("download-feedback-pdf-file", "data"),
        Input("download-feedback-pdf", "n_clicks"),
        [State("emp-name", "value"),
         State("course-name", "value"),
         State("trainer-name", "value"),
         State("feedback-date", "date"),
         State("obj1", "value"),
         State("obj2", "value"),
         State("content1", "value"),
         State("content2", "value"),
         State("content3", "value"),
         State("trainer1", "value"),
         State("trainer2", "value"),
         State("trainer3", "value"),
         State("trainer4", "value"),
         State("trainer5", "value"),
         State("liked", "value"),
         State("improved", "value"),
         State("signature", "value"),
         State("sign-date", "date")]
    )
    def download_pdf(n_clicks, emp_name, course_name, trainer_name, fb_date,
                     obj1, obj2, c1, c2, c3, t1, t2, t3, t4, t5, liked, improved, signature, sign_date):
        if not n_clicks:
            return None
        
        if not emp_name:
            return None
        
        # Get logo as base64
        logo_path = os.path.join("assets", "Screenshot 2026-05-26 154737.png")
        logo_base64 = ""
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Professional margins
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
        story.append(Paragraph("Training Feedback Report", title_style))
        story.append(Paragraph("IMS/TRM/FDBK/V2.0", subtitle_style))
        story.append(Spacer(1, 15))
        
        # EMPLOYEE INFORMATION
        story.append(Paragraph("EMPLOYEE INFORMATION", heading_style))
        
        emp_data = [
            ["Employee Name:", emp_name or 'N/A'],
            ["Course Name:", course_name or 'N/A'],
            ["Trainer Name:", trainer_name or 'N/A'],
            ["Feedback Date:", fb_date or 'N/A']
        ]
        
        emp_table = Table(emp_data, colWidths=[1.2*inch, 3.5*inch])
        emp_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
        ]))
        story.append(emp_table)
        story.append(Spacer(1, 12))
        
        # SECTION A - OBJECTIVES
        story.append(Paragraph("A. OBJECTIVES", heading_style))
        
        obj_data = [
            ["1. Objectives clearly stated:", _get_rating_text(obj1)],
            ["2. Session met objectives:", _get_rating_text(obj2)]
        ]
        
        obj_table = Table(obj_data, colWidths=[3.5*inch, 1.5*inch])
        obj_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ]))
        story.append(obj_table)
        story.append(Spacer(1, 10))
        
        # SECTION B - COURSE CONTENT
        story.append(Paragraph("B. COURSE CONTENT & DELIVERY", heading_style))
        
        content_data = [
            ["1. Subject matter met objectives:", _get_rating_text(c1)],
            ["2. Session length appropriate:", _get_rating_text(c2)],
            ["3. Content matched description:", _get_rating_text(c3)]
        ]
        
        content_table = Table(content_data, colWidths=[3.5*inch, 1.5*inch])
        content_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ]))
        story.append(content_table)
        story.append(Spacer(1, 10))
        
        # SECTION C - TRAINER EFFECTIVENESS
        story.append(Paragraph("C. TRAINER EFFECTIVENESS", heading_style))
        
        trainer_data = [
            ["1. Trainer knowledgeable:", _get_rating_text(t1)],
            ["2. Trainer competent:", _get_rating_text(t2)],
            ["3. Good rapport with session:", _get_rating_text(t3)],
            ["4. Good summary at end:", _get_rating_text(t4)],
            ["5. Would learn from this trainer again:", _get_rating_text(t5)]
        ]
        
        trainer_table = Table(trainer_data, colWidths=[3.5*inch, 1.5*inch])
        trainer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ]))
        story.append(trainer_table)
        story.append(Spacer(1, 10))
        
        # SECTION D - OPEN ENDED QUESTIONS
        story.append(Paragraph("D. OPEN ENDED QUESTIONS", heading_style))
        
        # Calculate average rating
        ratings = [obj1, obj2, c1, c2, c3, t1, t2, t3, t4, t5]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            avg_rating = sum(valid_ratings) / len(valid_ratings)
            if avg_rating >= 3.5:
                overall = "Excellent"
                color = "#10b981"
            elif avg_rating >= 2.5:
                overall = "Good"
                color = "#16a34a"
            else:
                overall = "Needs Improvement"
                color = "#ea580c"
        else:
            overall = "No ratings"
            color = "#94a3b8"
        
        liked_text = liked or 'No comments provided'
        improved_text = improved or 'No suggestions provided'
        
        open_data = [
            ["What did you like?", liked_text],
            ["How could this be improved?", improved_text],
            ["", ""],
            ["Overall Rating:", overall]
        ]
        
        open_table = Table(open_data, colWidths=[1.5*inch, 3.2*inch])
        open_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (0, -2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (0, -1), 'Helvetica-Bold'),
            ('SPAN', (0, 3), (1, 3)),
            ('ALIGN', (0, 3), (1, 3), 'CENTER'),
            ('BACKGROUND', (0, 3), (1, 3), colors.HexColor(f"{color}20")),
            ('TEXTCOLOR', (0, 3), (1, 3), colors.HexColor(color)),
        ]))
        story.append(open_table)
        story.append(Spacer(1, 10))
        
        # SECTION E - ACKNOWLEDGEMENT
        story.append(Paragraph("E. ACKNOWLEDGEMENT", heading_style))
        
        sig_data = [
            ["Signature:", signature or 'N/A'],
            ["Date:", sign_date or 'N/A']
        ]
        
        sig_table = Table(sig_data, colWidths=[1.2*inch, 3.5*inch])
        sig_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(sig_table)
        story.append(Spacer(1, 15))
        
        # Footer Note
        note_style = ParagraphStyle(
            'Note',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#94a3b8'),
            alignment=1
        )
        story.append(Paragraph("Thank you for your valuable feedback!", note_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Encode to base64
        pdf_b64 = base64.b64encode(pdf_content).decode()
        
        return dict(
            content=pdf_b64,
            filename=f"Training_Feedback_{emp_name or 'Report'}_{datetime.now().strftime('%Y%m%d')}.pdf",
            base64=True
        )
    
    # Back button
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("back-to-procurement-fb", "n_clicks"),
        prevent_initial_call=True
    )
    def go_back(n_clicks):
        if n_clicks:
            return "/procurement"
        return no_update

def _get_rating_text(value):
    if value == 4:
        return "4 - Strongly Agree"
    elif value == 3:
        return "3 - Agree"
    elif value == 2:
        return "2 - Disagree"
    elif value == 1:
        return "1 - Strongly Disagree"
    else:
        return "Not Rated"