# components/sidebar.py - Sidebar with Working Scrollbar

from dash import html, dcc

def create_sidebar(logo_data):
    return html.Div(className="sidebar", style={
        'background': 'linear-gradient(180deg, #2451C9 0%, #3A6BE0 40%, #5A8CFF 100%)',
        'width': '220px',
        'height': '100vh',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'zIndex': '1000',
        'transition': 'all 0.3s ease',
        'boxShadow': '2px 0 15px rgba(36, 81, 201, 0.2)',
        'overflowY': 'auto',
        'overflowX': 'hidden',
        'borderRight': '1px solid rgba(255,255,255,0.06)'
    }, children=[
        # CSS Styles - Working Scrollbar
        html.Div([
            dcc.Markdown("""
            <style>
                .sidebar * {
                    color: #ffffff !important;
                }
                
                /* Working scrollbar - small and clean */
                .sidebar::-webkit-scrollbar {
                    width: 4px;
                }
                
                .sidebar::-webkit-scrollbar-track {
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                }
                
                .sidebar::-webkit-scrollbar-thumb {
                    background: rgba(255,255,255,0.3);
                    border-radius: 10px;
                }
                
                .sidebar::-webkit-scrollbar-thumb:hover {
                    background: rgba(255,255,255,0.5);
                }
                
                /* Firefox scrollbar */
                .sidebar {
                    scrollbar-width: thin;
                    scrollbar-color: rgba(255,255,255,0.3) rgba(255,255,255,0.1);
                }
                
                .sidebar-logo {
                    max-width: 100px;
                    width: 100%;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                    position: relative;
                    z-index: 1;
                }
                
                .logo-container {
                    padding: 12px 12px 8px 12px;
                    border-bottom: 1px solid rgba(255,255,255,0.08);
                    margin-bottom: 8px;
                    position: relative;
                    overflow: hidden;
                    flex-shrink: 0;
                }
                
                .logo-container::before {
                    content: '';
                    position: absolute;
                    top: -20px;
                    right: -20px;
                    width: 50px;
                    height: 50px;
                    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                }
                
                .logo-container::after {
                    content: '';
                    position: absolute;
                    bottom: -15px;
                    left: -15px;
                    width: 40px;
                    height: 40px;
                    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                }
                
                .nav-section { 
                    margin-bottom: 6px;
                    padding: 0 4px;
                }
                
                .nav-section:first-of-type {
                    margin-top: 0px;
                }
                
                .nav-section-title { 
                    font-size: 8px; 
                    font-weight: 600; 
                    text-transform: uppercase; 
                    letter-spacing: 0.8px; 
                    margin-bottom: 4px; 
                    padding-left: 10px;
                    opacity: 0.5;
                    color: rgba(255,255,255,0.7) !important;
                }
                
                .nav-link {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    padding: 4px 10px;
                    border-radius: 6px;
                    margin: 1px 4px;
                    font-weight: 500;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    font-size: 11px;
                    border: 1px solid transparent;
                    position: relative;
                    overflow: hidden;
                }
                
                .nav-link::before {
                    content: '';
                    position: absolute;
                    top: -20px;
                    right: -20px;
                    width: 25px;
                    height: 25px;
                    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .nav-link:hover::before {
                    opacity: 1;
                }
                
                .nav-link i { 
                    width: 14px; 
                    font-size: 11px; 
                    opacity: 0.6; 
                    transition: all 0.3s ease;
                }
                
                .nav-link:hover { 
                    background: rgba(255,255,255,0.08); 
                    transform: translateX(2px);
                    border-color: rgba(255,255,255,0.06);
                }
                
                .nav-link:hover i { 
                    opacity: 1; 
                    transform: scale(1.05);
                }
                
                .collapsible { 
                    cursor: pointer; 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center;
                }
                
                .collapsible .nav-text { 
                    flex: 1; 
                }
                
                .arrow-icon { 
                    transition: transform 0.3s ease; 
                    font-size: 9px; 
                    margin-left: auto; 
                    opacity: 0.5;
                }
                
                .arrow-icon.rotated { 
                    transform: rotate(90deg); 
                }
                
                .submenu { 
                    overflow: hidden; 
                    transition: max-height 0.3s ease; 
                    margin-left: 12px; 
                    border-left: 1px solid rgba(255,255,255,0.06); 
                    padding-left: 6px; 
                }
                
                .submenu.collapsed { 
                    max-height: 0; 
                }
                
                .submenu.expanded { 
                    max-height: 500px; 
                }
                
                .subnav-link {
                    display: block;
                    padding: 3px 8px;
                    text-decoration: none;
                    font-size: 10px;
                    transition: all 0.3s ease;
                    border-radius: 4px;
                    margin: 1px 0;
                    opacity: 0.6;
                    border: 1px solid transparent;
                }
                
                .subnav-link:hover { 
                    background: rgba(255,255,255,0.06); 
                    padding-left: 12px; 
                    opacity: 1;
                    border-color: rgba(255,255,255,0.06);
                }
                
                @keyframes bubbleFloat {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-2px); }
                }
                
                .nav-link:hover {
                    animation: bubbleFloat 2s ease-in-out infinite;
                }
            </style>
            """, dangerously_allow_html=True)
        ]),
        
        # Logo Section
        html.Div(className="logo-container", children=[
            html.Img(
                src=logo_data, 
                className="sidebar-logo",
                style={
                    "maxWidth": "100px",
                    "width": "100%",
                    "height": "auto",
                    "display": "block",
                    "margin": "0 auto",
                    "position": "relative",
                    "zIndex": "1"
                }
            )
        ]),
        
        # Navigation
        html.Div(children=[
            # MAIN
            html.Div(className="nav-section", children=[
                html.Div(className="nav-section-title", children="MAIN"),
                dcc.Link([html.I(className="fas fa-tachometer-alt"), html.Span(" Dashboard", className="nav-text")], href="/dashboard", className="nav-link"),
                dcc.Link([html.I(className="fas fa-chart-bar"), html.Span(" MRM", className="nav-text")], href="/mrm", className="nav-link"),
                dcc.Link([html.I(className="fas fa-shield-alt"), html.Span(" Risk Management", className="nav-text")], href="/risk-management", className="nav-link"),
            ]),
            
            # QMS
            html.Div(className="nav-section", children=[
                html.Div(className="nav-section-title", children="QMS"),
                html.Div(className="nav-link collapsible", id="qms-toggle", children=[
                    html.I(className="fas fa-clipboard-check"),
                    html.Span(" QMS", className="nav-text"),
                    html.I(className="fas fa-chevron-right arrow-icon", id="qms-arrow")
                ]),
                html.Div(id="qms-submenu", className="submenu collapsed", children=[
                    dcc.Link("Quality Assurance", href="/quality-assurance", className="subnav-link"),
                    dcc.Link("Policy and Objectives", href="/policy-objectives", className="subnav-link"),
                    dcc.Link("HR", href="/hr", className="subnav-link"),
                    dcc.Link("Admin", href="/admin", className="subnav-link"),
                    dcc.Link("Procurement", href="/procurement", className="subnav-link"),
                    dcc.Link("System Admin", href="/system-admin", className="subnav-link"),
                    dcc.Link("Business Development", href="/business-dev", className="subnav-link"),
                    dcc.Link("Operation", href="/operation", className="subnav-link"),
                ])
            ]),
            
            # EHS
            html.Div(className="nav-section", children=[
                html.Div(className="nav-section-title", children="EHS"),
                dcc.Link([html.I(className="fas fa-leaf"), html.Span(" EHS Dashboard", className="nav-text")], href="/ehs", className="nav-link"),
            ]),
            
            # ITSMS
            html.Div(className="nav-section", children=[
                html.Div(className="nav-section-title", children="ITSMS"),
                dcc.Link([html.I(className="fas fa-server"), html.Span(" ITSMS", className="nav-text")], href="/itsms", className="nav-link"),
            ]),
            
            # ISMS
            html.Div(className="nav-section", children=[
                html.Div(className="nav-section-title", children="ISMS"),
                dcc.Link([html.I(className="fas fa-lock"), html.Span(" ISMS", className="nav-text")], href="/isms", className="nav-link"),
            ]),
            
            # Communication
            html.Div(className="nav-section", children=[
                html.Div(className="nav-section-title", children="COMMUNICATION"),
                dcc.Link([html.I(className="fas fa-comments"), html.Span(" Communication", className="nav-text")], href="/communication", className="nav-link"),
                dcc.Link([html.I(className="fas fa-folder"), html.Span(" Documentation Repository", className="nav-text")], href="/document-center", className="nav-link"),
                dcc.Link([html.I(className="fas fa-graduation-cap"), html.Span(" Sharing Information", className="nav-text")], href="/learning", className="nav-link"),
            ])
        ])
    ])