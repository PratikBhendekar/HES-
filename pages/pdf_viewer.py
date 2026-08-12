from dash import html, dcc

def pdf_viewer_page(pdf_path, title):
    return html.Div([
        html.Div(className="dashboard-header", children=[
            html.H1(title, className="dashboard-title"),
            html.Div(className="header-search", children=[
                html.I(className="fas fa-search"),
                dcc.Input(type="text", placeholder="Search...", className="header-search-input")
            ])
        ]),
        
        html.Div(className="breadcrumb", children=[
            html.Span("EHS", className="breadcrumb-item"),
            html.Span(">", className="breadcrumb-sep"),
            html.Span(title, className="breadcrumb-item active")
        ]),
        
        html.Div(className="pdf-viewer-container", children=[
            html.Iframe(
                src=pdf_path,
                className="pdf-iframe",
                style={
                    "width": "100%",
                    "height": "85vh",
                    "border": "none",
                    "borderRadius": "16px",
                    "boxShadow": "0 4px 15px rgba(0,0,0,0.1)"
                }
            )
        ])
    ])