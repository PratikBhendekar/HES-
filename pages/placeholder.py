from dash import html

def placeholder_page(title):
    return html.Div(className="placeholder-page", children=[
        html.H2(title, className="placeholder-title"),
        html.P("This page is under construction. Front-end demo only.", className="placeholder-text"),
        html.Div(className="placeholder-icon", children=html.I(className="fas fa-tools"))
    ])