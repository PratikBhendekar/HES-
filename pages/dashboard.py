# pages/dashboard.py - Dashboard with Normal Spacing

from dash import Input, Output, html, dcc
import dash
from flask import session
import datetime

def dashboard_page():
    # Get user info from session
    full_name = session.get('name', 'User') if hasattr(session, 'get') else 'User'
    
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    
    return html.Div([
        # Custom Fonts
        html.Link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
            rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap",
            rel="stylesheet"
        ),
        
        # Custom CSS Styles
        html.Div([
            dcc.Markdown("""
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                html, body {
                    overflow: hidden;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }
                
                body::-webkit-scrollbar {
                    display: none;
                }
                
                body {
                    -ms-overflow-style: none;
                    scrollbar-width: none;
                }
                
                .main-container {
                    height: 100vh;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                    background: #f0f2f5;
                }
                
                .stat-card {
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    cursor: pointer;
                    position: relative;
                    overflow: hidden;
                    aspect-ratio: 1 / 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    border-radius: 16px;
                    padding: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                }
                
                .stat-card .bubble {
                    position: absolute;
                    border-radius: 50%;
                    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), rgba(255,255,255,0.05));
                    pointer-events: none;
                    animation: bubbleRise 8s ease-in-out infinite;
                    opacity: 0.4;
                }
                
                .stat-card .bubble:nth-child(1) {
                    width: 50px;
                    height: 50px;
                    left: 5%;
                    bottom: -20%;
                    animation-duration: 6s;
                    animation-delay: 0s;
                }
                
                .stat-card .bubble:nth-child(2) {
                    width: 35px;
                    height: 35px;
                    right: 10%;
                    bottom: -15%;
                    animation-duration: 8s;
                    animation-delay: 1.5s;
                }
                
                .stat-card .bubble:nth-child(3) {
                    width: 20px;
                    height: 20px;
                    left: 25%;
                    bottom: -10%;
                    animation-duration: 7s;
                    animation-delay: 3s;
                }
                
                .stat-card .bubble:nth-child(4) {
                    width: 40px;
                    height: 40px;
                    right: 25%;
                    bottom: -25%;
                    animation-duration: 9s;
                    animation-delay: 0.8s;
                }
                
                .stat-card .bubble:nth-child(5) {
                    width: 12px;
                    height: 12px;
                    left: 55%;
                    bottom: -5%;
                    animation-duration: 5s;
                    animation-delay: 2s;
                }
                
                @keyframes bubbleRise {
                    0% {
                        transform: translateY(0) scale(1) rotate(0deg);
                        opacity: 0.4;
                    }
                    25% {
                        transform: translateY(-30px) scale(1.1) rotate(15deg);
                        opacity: 0.5;
                    }
                    50% {
                        transform: translateY(-60px) scale(0.9) rotate(-10deg);
                        opacity: 0.6;
                    }
                    75% {
                        transform: translateY(-90px) scale(1.05) rotate(20deg);
                        opacity: 0.4;
                    }
                    100% {
                        transform: translateY(-120px) scale(0.8) rotate(-5deg);
                        opacity: 0;
                    }
                }
                
                @keyframes cardFloat {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-4px); }
                }
                
                .stat-card {
                    animation: cardFloat 4s ease-in-out infinite;
                }
                
                .stat-card:nth-child(1) { animation-delay: 0s; }
                .stat-card:nth-child(2) { animation-delay: 0.3s; }
                .stat-card:nth-child(3) { animation-delay: 0.6s; }
                .stat-card:nth-child(4) { animation-delay: 0.9s; }
                .stat-card:nth-child(5) { animation-delay: 1.2s; }
                .stat-card:nth-child(6) { animation-delay: 1.5s; }
                .stat-card:nth-child(7) { animation-delay: 1.8s; }
                .stat-card:nth-child(8) { animation-delay: 2.1s; }
                .stat-card:nth-child(9) { animation-delay: 2.4s; }
                
                .stat-card:hover {
                    transform: translateY(-6px) scale(1.02) !important;
                    box-shadow: 0 20px 40px -8px rgba(0,0,0,0.2) !important;
                    z-index: 10;
                }
                
                .stat-card:active {
                    transform: scale(0.95) !important;
                }
                
                .stat-card::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.2) 0%, transparent 60%);
                    opacity: 0;
                    transition: opacity 0.6s ease;
                    pointer-events: none;
                    z-index: 5;
                }
                
                .stat-card:hover::before {
                    opacity: 1;
                }
                
                @keyframes fadeInScale {
                    0% {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                    100% {
                        opacity: 1;
                        transform: scale(1);
                    }
                }
                
                .stat-card {
                    animation: fadeInScale 0.5s ease-out forwards, cardFloat 4s ease-in-out infinite;
                    opacity: 0;
                }
                
                .stat-card:nth-child(1) { animation-delay: 0.05s, 0s; }
                .stat-card:nth-child(2) { animation-delay: 0.10s, 0.3s; }
                .stat-card:nth-child(3) { animation-delay: 0.15s, 0.6s; }
                .stat-card:nth-child(4) { animation-delay: 0.20s, 0.9s; }
                .stat-card:nth-child(5) { animation-delay: 0.25s, 1.2s; }
                .stat-card:nth-child(6) { animation-delay: 0.30s, 1.5s; }
                .stat-card:nth-child(7) { animation-delay: 0.35s, 1.8s; }
                .stat-card:nth-child(8) { animation-delay: 0.40s, 2.1s; }
                .stat-card:nth-child(9) { animation-delay: 0.45s, 2.4s; }
                
                .card-content {
                    position: relative;
                    z-index: 10;
                }
                
                .cards-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 10px;
                    flex: 1;
                    align-content: start;
                    padding-bottom: 0;
                }
                
                @keyframes shimmerSlide {
                    0% { transform: translateX(-100%) rotate(10deg); }
                    100% { transform: translateX(100%) rotate(10deg); }
                }
                
                .welcome-banner {
                    position: relative;
                    overflow: hidden;
                    flex-shrink: 0;
                }
                
                .welcome-banner::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 50%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                    animation: shimmerSlide 4s ease-in-out infinite;
                }
                
                .dashboard-header {
                    animation: fadeInScale 0.5s ease-out forwards;
                    opacity: 0;
                    animation-delay: 0s;
                    flex-shrink: 0;
                }
            </style>
            """, dangerously_allow_html=True)
        ]),
        
        # Main Container - Normal spacing
        html.Div(className="main-container", style={
            'background': '#f0f2f5',
            'height': '100vh',
            'padding': '10px 15px 10px 15px',
            'overflow': 'hidden',
            'display': 'flex',
            'flexDirection': 'column'
        }, children=[
            
            # Header
            html.Div(className="dashboard-header", style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'marginBottom': '8px',
                'flexWrap': 'wrap',
                'gap': '5px',
                'flexShrink': '0'
            }, children=[
                html.Div([
                    html.H1("Dashboard", style={
                        'fontSize': '20px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'margin': '0',
                        'fontFamily': 'Poppins, sans-serif'
                    }),
                    html.P("Enterprise Integrated Management Platform", style={
                        'fontSize': '9px',
                        'color': '#64748b',
                        'margin': '1px 0 0 0',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ]),
                
                html.Div(style={
                    'display': 'flex',
                    'gap': '6px',
                    'alignItems': 'center'
                }, children=[
                    html.Div(style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'gap': '6px',
                        'background': 'white',
                        'padding': '4px 10px',
                        'borderRadius': '20px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.06)'
                    }, children=[
                        html.Div(style={
                            'width': '26px',
                            'height': '26px',
                            'background': 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                            'borderRadius': '50%',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'fontSize': '11px',
                            'fontWeight': '700',
                            'color': 'white',
                            'fontFamily': 'Poppins, sans-serif'
                        }, children=full_name[0].upper() if full_name else 'U'),
                        html.Div([
                            html.Div(full_name, style={
                                'fontSize': '9px',
                                'fontWeight': '600',
                                'color': '#1e293b',
                                'fontFamily': 'Inter, sans-serif'
                            }),
                            html.Div("Admin", style={
                                'fontSize': '7px',
                                'color': '#64748b',
                                'fontFamily': 'Inter, sans-serif'
                            })
                        ])
                    ]),
                    
                    html.A(
                        html.Button([
                            html.I(className="fas fa-sign-out-alt", style={'marginRight': '3px', 'fontSize': '9px'}),
                            "Logout"
                        ], style={
                            'padding': '4px 10px',
                            'background': '#ef4444',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '20px',
                            'cursor': 'pointer',
                            'fontSize': '9px',
                            'fontWeight': '600',
                            'fontFamily': 'Inter, sans-serif',
                            'boxShadow': '0 2px 8px rgba(239,68,68,0.3)',
                            'transition': 'all 0.3s ease'
                        }),
                        href="/logout",
                        style={'textDecoration': 'none'}
                    )
                ])
            ]),
            
            # Welcome Banner - Normal
            html.Div(className="welcome-banner", style={
                'background': 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
                'padding': '8px 16px',
                'marginBottom': '10px',
                'borderRadius': '25px',
                'position': 'relative',
                'overflow': 'hidden',
                'boxShadow': '0 4px 20px rgba(37,99,235,0.25)',
                'flexShrink': '0'
            }, children=[
                html.Div(style={
                    'position': 'absolute',
                    'top': '-25px',
                    'right': '-25px',
                    'width': '60px',
                    'height': '60px',
                    'background': 'rgba(255,255,255,0.05)',
                    'borderRadius': '50%'
                }),
                html.Div(style={
                    'position': 'absolute',
                    'bottom': '-25px',
                    'left': '-25px',
                    'width': '60px',
                    'height': '60px',
                    'background': 'rgba(255,255,255,0.03)',
                    'borderRadius': '50%'
                }),
                
                html.Div(style={
                    'position': 'relative',
                    'zIndex': '2',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'flexWrap': 'wrap',
                    'gap': '5px'
                }, children=[
                    html.Div(style={
                        'color': 'white'
                    }, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'gap': '6px',
                            'marginBottom': '2px'
                        }, children=[
                            html.Div(style={
                                'width': '26px',
                                'height': '26px',
                                'background': 'rgba(255,255,255,0.15)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'fontSize': '12px',
                                'fontWeight': '700',
                                'fontFamily': 'Poppins, sans-serif'
                            }, children=full_name[0].upper() if full_name else 'U'),
                            html.H2(f"Welcome back, {full_name}", style={
                                'fontSize': '14px',
                                'fontWeight': '600',
                                'margin': '0',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.P("Here's your enterprise performance overview.", style={
                            'fontSize': '9px',
                            'margin': '0',
                            'opacity': '0.9',
                            'fontFamily': 'Inter, sans-serif',
                            'marginLeft': '32px'
                        })
                    ]),
                    html.Div(style={
                        'display': 'flex',
                        'gap': '5px'
                    }, children=[
                        html.Div(style={
                            'background': 'rgba(255,255,255,0.12)',
                            'padding': '3px 8px',
                            'borderRadius': '15px',
                            'display': 'flex',
                            'alignItems': 'center',
                            'gap': '3px'
                        }, children=[
                            html.I(className="fas fa-calendar-alt", style={'color': 'white', 'fontSize': '8px'}),
                            html.Span(current_date.split(',')[0], style={
                                'color': 'white',
                                'fontSize': '7px',
                                'fontFamily': 'Inter, sans-serif'
                            })
                        ]),
                        html.Div(style={
                            'background': 'rgba(255,255,255,0.12)',
                            'padding': '3px 8px',
                            'borderRadius': '15px',
                            'display': 'flex',
                            'alignItems': 'center',
                            'gap': '3px'
                        }, children=[
                            html.I(className="fas fa-clock", style={'color': 'white', 'fontSize': '8px'}),
                            html.Span(current_time, style={
                                'color': 'white',
                                'fontSize': '7px',
                                'fontFamily': 'Inter, sans-serif'
                            })
                        ])
                    ])
                ])
            ]),
            
            # CARDS GRID - Normal spacing
            html.Div(className="cards-grid", style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(3, 1fr)',
                'gap': '10px',
                'flex': '1',
                'alignContent': 'start',
                'paddingBottom': '0'
            }, children=[
                # Card 1 - MoM Tracking - Soft Blue
                html.Div(className="stat-card", id="card-mom-tracking", style={
                    'background': 'linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)',
                    'border': '2px solid rgba(56, 189, 248, 0.2)',
                    'color': '#0c4a6e'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(56, 189, 248, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-file-alt", style={'fontSize': '12px', 'color': '#38bdf8'})
                            ]),
                            html.Span("12", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#0284c7',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("MoM Tracking", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#0c4a6e',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Minutes of Meeting", style={
                            'fontSize': '7px',
                            'color': '#38bdf8',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("45", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#0c4a6e', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Actions", style={'fontSize': '6px', 'color': '#0284c7', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(56,189,248,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("12", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#0c4a6e', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Meetings", style={'fontSize': '6px', 'color': '#0284c7', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 2 - Risk Tracking - Soft Sky Blue
                html.Div(className="stat-card", id="card-risk-tracking", style={
                    'background': 'linear-gradient(135deg, #f0f9ff 0%, #b8e2f8 100%)',
                    'border': '2px solid rgba(14, 165, 233, 0.2)',
                    'color': '#0c4a6e'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(14, 165, 233, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-shield-alt", style={'fontSize': '12px', 'color': '#0ea5e9'})
                            ]),
                            html.Span("17", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#0284c7',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Risk Tracking", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#0c4a6e',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Risk Management", style={
                            'fontSize': '7px',
                            'color': '#0ea5e9',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("8", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#0c4a6e', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("High", style={'fontSize': '6px', 'color': '#0284c7', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(14,165,233,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("17", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#0c4a6e', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Total", style={'fontSize': '6px', 'color': '#0284c7', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 3 - Vendor Evaluation - Soft Mint
                html.Div(className="stat-card", id="card-vendor-evaluation", style={
                    'background': 'linear-gradient(135deg, #ecfdf3 0%, #b5e6d4 100%)',
                    'border': '2px solid rgba(16, 185, 129, 0.2)',
                    'color': '#064e3b'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(16, 185, 129, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-building", style={'fontSize': '12px', 'color': '#10b981'})
                            ]),
                            html.Span("24", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#059669',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Vendor Evaluation", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#064e3b',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Vendor Performance", style={
                            'fontSize': '7px',
                            'color': '#10b981',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("24", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#064e3b', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Vendors", style={'fontSize': '6px', 'color': '#059669', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(16,185,129,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("18", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#064e3b', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Active", style={'fontSize': '6px', 'color': '#059669', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 4 - Safety Statistics - Soft Teal
                html.Div(className="stat-card", id="card-safety-stats", style={
                    'background': 'linear-gradient(135deg, #ecfdf5 0%, #99f6e4 100%)',
                    'border': '2px solid rgba(20, 184, 166, 0.2)',
                    'color': '#0f766e'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(20, 184, 166, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-chart-line", style={'fontSize': '12px', 'color': '#14b8a6'})
                            ]),
                            html.Span("245", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#0f766e',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Safety Statistics", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#115e59',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Safety Metrics", style={
                            'fontSize': '7px',
                            'color': '#14b8a6',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("245", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#0f766e', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Safe Days", style={'fontSize': '6px', 'color': '#0f766e', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(20,184,166,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("0", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#0f766e', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Incidents", style={'fontSize': '6px', 'color': '#0f766e', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 5 - Non Conformance - Soft Lavender
                html.Div(className="stat-card", id="card-nc-criticality", style={
                    'background': 'linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%)',
                    'border': '2px solid rgba(168, 85, 247, 0.2)',
                    'color': '#4c1d95'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(168, 85, 247, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-exclamation-triangle", style={'fontSize': '12px', 'color': '#a855f7'})
                            ]),
                            html.Span("15", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#7c3aed',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Non Conformance", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#4c1d95',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Quality Management", style={
                            'fontSize': '7px',
                            'color': '#a855f7',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("3", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#4c1d95', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Major", style={'fontSize': '6px', 'color': '#7c3aed', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(168,85,247,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("15", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#4c1d95', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Total", style={'fontSize': '6px', 'color': '#7c3aed', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 6 - Org Knowledge - Soft Purple
                html.Div(className="stat-card", id="card-org-knowledge", style={
                    'background': 'linear-gradient(135deg, #f5f3ff 0%, #c4b5fd 100%)',
                    'border': '2px solid rgba(139, 92, 246, 0.2)',
                    'color': '#4c1d95'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(139, 92, 246, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-graduation-cap", style={'fontSize': '12px', 'color': '#8b5cf6'})
                            ]),
                            html.Span("156", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#6d28d9',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Org Knowledge", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#4c1d95',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Knowledge Management", style={
                            'fontSize': '7px',
                            'color': '#8b5cf6',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("156", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#4c1d95', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Docs", style={'fontSize': '6px', 'color': '#6d28d9', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(139,92,246,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("45", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#4c1d95', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("SOPs", style={'fontSize': '6px', 'color': '#6d28d9', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 7 - Security Incidents - Soft Indigo
                html.Div(className="stat-card", id="card-security-incidents", style={
                    'background': 'linear-gradient(135deg, #eef2ff 0%, #c7d2fe 100%)',
                    'border': '2px solid rgba(99, 102, 241, 0.2)',
                    'color': '#312e81'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(99, 102, 241, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-shield-alt", style={'fontSize': '12px', 'color': '#6366f1'})
                            ]),
                            html.Span("100", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#4f46e5',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Security Incidents", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#312e81',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Security Management", style={
                            'fontSize': '7px',
                            'color': '#6366f1',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("0", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#312e81', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Incidents", style={'fontSize': '6px', 'color': '#4f46e5', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(99,102,241,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("100", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#312e81', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Secure", style={'fontSize': '6px', 'color': '#4f46e5', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 8 - Quick Reports - Soft Cyan
                html.Div(className="stat-card", id="card-quick-stats", style={
                    'background': 'linear-gradient(135deg, #ecfeff 0%, #a5f3fc 100%)',
                    'border': '2px solid rgba(6, 182, 212, 0.2)',
                    'color': '#164e63'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(6, 182, 212, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-chart-bar", style={'fontSize': '12px', 'color': '#06b6d4'})
                            ]),
                            html.Span("24", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#0891b2',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Quick Reports", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#164e63',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Analytics", style={
                            'fontSize': '7px',
                            'color': '#06b6d4',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("24", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#164e63', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Reports", style={'fontSize': '6px', 'color': '#0891b2', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(6,182,212,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("12", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#164e63', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Dashboards", style={'fontSize': '6px', 'color': '#0891b2', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ]),
                
                # Card 9 - Training Feedback - Soft Violet
                html.Div(className="stat-card", id="card-training-feedback", style={
                    'background': 'linear-gradient(135deg, #faf5ff 0%, #d8b4fe 100%)',
                    'border': '2px solid rgba(168, 85, 247, 0.2)',
                    'color': '#4c1d95'
                }, children=[
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    html.Div(className="bubble"),
                    
                    html.Div(className="card-content", style={'width': '100%'}, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'marginBottom': '3px'
                        }, children=[
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'background': 'rgba(168, 85, 247, 0.2)',
                                'borderRadius': '50%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center'
                            }, children=[
                                html.I(className="fas fa-comments", style={'fontSize': '12px', 'color': '#a855f7'})
                            ]),
                            html.Span("4.8", style={
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'color': '#7c3aed',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.Div("Training Feedback", style={
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'color': '#4c1d95',
                            'fontFamily': 'Poppins, sans-serif',
                            'marginBottom': '1px'
                        }),
                        html.Div("Feedback", style={
                            'fontSize': '7px',
                            'color': '#a855f7',
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '3px'
                        }),
                        html.Div(style={
                            'display': 'flex',
                            'gap': '10px',
                            'justifyContent': 'center'
                        }, children=[
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("4.8", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#4c1d95', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Rating", style={'fontSize': '6px', 'color': '#7c3aed', 'fontFamily': 'Inter, sans-serif'})
                            ]),
                            html.Div(style={'width': '1px', 'background': 'rgba(168,85,247,0.2)'}),
                            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '3px'}, children=[
                                html.Span("156", style={'fontSize': '11px', 'fontWeight': '700', 'color': '#4c1d95', 'fontFamily': 'Poppins, sans-serif'}),
                                html.Span("Responses", style={'fontSize': '6px', 'color': '#7c3aed', 'fontFamily': 'Inter, sans-serif'})
                            ])
                        ])
                    ])
                ])
            ]),
            
            html.Div(id="dashboard-nav-click", style={"display": "none"})
        ])
    ])


def register_dashboard_callbacks(app):
    """Register callbacks for dashboard navigation"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("card-mom-tracking", "n_clicks"),
         Input("card-risk-tracking", "n_clicks"),
         Input("card-vendor-evaluation", "n_clicks"),
         Input("card-safety-stats", "n_clicks"),
         Input("card-nc-criticality", "n_clicks"),
         Input("card-org-knowledge", "n_clicks"),
         Input("card-security-incidents", "n_clicks"),
         Input("card-quick-stats", "n_clicks"),
         Input("card-training-feedback", "n_clicks")],
        prevent_initial_call=True
    )
    def navigate_dashboard_cards(mom, risk, vendor, safety, nc, org_knowledge, security, quick, training):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        nav_map = {
            "card-mom-tracking": "/mom-tracking",
            "card-risk-tracking": "/risk-management",
            "card-vendor-evaluation": "/procurement",
            "card-safety-stats": "/ehs-safety-dashboard",
            "card-nc-criticality": "/non-conformance",
            "card-org-knowledge": "/org-knowledge",
            "card-security-incidents": "/security-incidents",
            "card-quick-stats": "/ehs-reports",
            "card-training-feedback": "/training-feedback"
        }
        
        if button_id in nav_map:
            return nav_map[button_id]
        
        return dash.no_update# pages/dashboard.py

from dash import Input, Output, html, dcc
import dash
from flask import session
import datetime

def dashboard_page():
    # Get user info from session
    full_name = session.get('name', 'User') if hasattr(session, 'get') else 'User'
    
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    
    return html.Div([
        # Custom Fonts
        html.Link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
            rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap",
            rel="stylesheet"
        ),
        
        # Custom CSS Styles
        html.Div([
            dcc.Markdown("""
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                /* Hide scrollbars */
                html, body {
                    overflow: hidden;
                    height: 100%;
                }
                
                body::-webkit-scrollbar {
                    display: none;
                }
                
                body {
                    -ms-overflow-style: none;
                    scrollbar-width: none;
                }
                
                /* Square Card Styles */
                .stat-card {
                    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
                    cursor: pointer;
                    position: relative;
                    background: white;
                    overflow: hidden;
                    aspect-ratio: 1 / 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }
                
                .stat-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                    transition: left 0.5s;
                }
                
                .stat-card:hover::before {
                    left: 100%;
                }
                
                .stat-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 15px 30px -12px rgba(0,0,0,0.15) !important;
                }
                
                .stat-card:active {
                    transform: translateY(-2px);
                }
                
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .dashboard-header {
                    animation: fadeInUp 0.5s ease-out;
                }
                
                .stat-card {
                    animation: fadeInUp 0.5s ease-out;
                    animation-fill-mode: both;
                }
            </style>
            """, dangerously_allow_html=True)
        ]),
        
        # Main Container
        html.Div(style={
            'background': '#f0f2f5',
            'minHeight': '100vh',
            'padding': '20px',
            'overflow': 'hidden',
            'height': '100vh'
        }, children=[
            
            # Header with User Info and Logout
            html.Div(className="dashboard-header", style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'marginBottom': '15px',
                'flexWrap': 'wrap',
                'gap': '10px'
            }, children=[
                html.Div([
                    html.H1("Dashboard", style={
                        'fontSize': '24px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'margin': '0',
                        'fontFamily': 'Poppins, sans-serif'
                    }),
                    html.P("Enterprise Integrated Management Platform", style={
                        'fontSize': '11px',
                        'color': '#64748b',
                        'margin': '3px 0 0 0',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ]),
                
                # User Info and Logout Section
                html.Div(style={
                    'display': 'flex',
                    'gap': '10px',
                    'alignItems': 'center'
                }, children=[
                    # User Info Card
                    html.Div(style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'gap': '10px',
                        'background': 'white',
                        'padding': '6px 12px',
                        'border': '1px solid #e2e8f0'
                    }, children=[
                        html.Div(style={
                            'width': '32px',
                            'height': '32px',
                            'background': 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'fontSize': '13px',
                            'fontWeight': '700',
                            'color': 'white',
                            'fontFamily': 'Poppins, sans-serif'
                        }, children=full_name[0].upper() if full_name else 'U'),
                        html.Div([
                            html.Div(full_name, style={
                                'fontSize': '11px',
                                'fontWeight': '600',
                                'color': '#1e293b',
                                'fontFamily': 'Inter, sans-serif'
                            }),
                            html.Div("Admin", style={
                                'fontSize': '9px',
                                'color': '#64748b',
                                'fontFamily': 'Inter, sans-serif'
                            })
                        ])
                    ]),
                    
                    # Logout Button
                    html.A(
                        html.Button([
                            html.I(className="fas fa-sign-out-alt", style={'marginRight': '5px', 'fontSize': '11px'}),
                            "Logout"
                        ], style={
                            'padding': '6px 12px',
                            'background': '#ef4444',
                            'color': 'white',
                            'border': 'none',
                            'cursor': 'pointer',
                            'fontSize': '11px',
                            'fontWeight': '600',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        href="/logout",
                        style={'textDecoration': 'none'}
                    )
                ])
            ]),
            
            # Welcome Banner - Smaller
            html.Div(style={
                'background': 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
                'padding': '12px 20px',
                'marginBottom': '15px',
                'position': 'relative',
                'overflow': 'hidden'
            }, children=[
                html.Div(style={
                    'position': 'absolute',
                    'top': '-40px',
                    'right': '-40px',
                    'width': '120px',
                    'height': '120px',
                    'background': 'rgba(255,255,255,0.05)',
                    'borderRadius': '50%'
                }),
                html.Div(style={
                    'position': 'absolute',
                    'bottom': '-40px',
                    'left': '-40px',
                    'width': '120px',
                    'height': '120px',
                    'background': 'rgba(255,255,255,0.03)',
                    'borderRadius': '50%'
                }),
                
                html.Div(style={
                    'position': 'relative',
                    'zIndex': '2',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'flexWrap': 'wrap',
                    'gap': '10px'
                }, children=[
                    html.Div(style={
                        'color': 'white'
                    }, children=[
                        html.Div(style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'gap': '10px',
                            'marginBottom': '5px'
                        }, children=[
                            html.Div(style={
                                'width': '36px',
                                'height': '36px',
                                'background': 'rgba(255,255,255,0.15)',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'fontSize': '16px',
                                'fontWeight': '700',
                                'fontFamily': 'Poppins, sans-serif'
                            }, children=full_name[0].upper() if full_name else 'U'),
                            html.H2(f"Welcome back, {full_name}", style={
                                'fontSize': '16px',
                                'fontWeight': '600',
                                'margin': '0',
                                'fontFamily': 'Poppins, sans-serif'
                            })
                        ]),
                        html.P("Here's your enterprise performance overview.", style={
                            'fontSize': '10px',
                            'margin': '0',
                            'opacity': '0.9',
                            'fontFamily': 'Inter, sans-serif',
                            'marginLeft': '46px'
                        })
                    ]),
                    html.Div(style={
                        'display': 'flex',
                        'gap': '8px'
                    }, children=[
                        html.Div(style={
                            'background': 'rgba(255,255,255,0.12)',
                            'padding': '5px 10px',
                            'display': 'flex',
                            'alignItems': 'center',
                            'gap': '6px'
                        }, children=[
                            html.I(className="fas fa-calendar-alt", style={'color': 'white', 'fontSize': '10px'}),
                            html.Span(current_date.split(',')[0], style={
                                'color': 'white',
                                'fontSize': '9px',
                                'fontFamily': 'Inter, sans-serif'
                            })
                        ]),
                        html.Div(style={
                            'background': 'rgba(255,255,255,0.12)',
                            'padding': '5px 10px',
                            'display': 'flex',
                            'alignItems': 'center',
                            'gap': '6px'
                        }, children=[
                            html.I(className="fas fa-clock", style={'color': 'white', 'fontSize': '10px'}),
                            html.Span(current_time, style={
                                'color': 'white',
                                'fontSize': '9px',
                                'fontFamily': 'Inter, sans-serif'
                            })
                        ])
                    ])
                ])
            ]),
            
            # SQUARE CARDS - 3 Rows of 3 Cards (Normal Size, No Cutoff)
            html.Div(style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(3, 1fr)',
                'gap': '15px',
                'marginBottom': '0',
                'height': 'calc(100vh - 140px)'
            }, children=[
                # Card 1 - MoM Tracking
                html.Div(className="stat-card", id="card-mom-tracking", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #3b82f6',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#eff6ff',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-file-alt", style={'fontSize': '20px', 'color': '#3b82f6'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="MoM Tracking"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Minutes of Meeting"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("12", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#3b82f6'}),
                            html.Div("Meetings", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("45", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#3b82f6'}),
                            html.Div("Actions", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 2 - Risk Tracking
                html.Div(className="stat-card", id="card-risk-tracking", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #f97316',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#fff7ed',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-shield-alt", style={'fontSize': '20px', 'color': '#f97316'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Risk Tracking"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Risk Management"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("8", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#f97316'}),
                            html.Div("High", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("17", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#f97316'}),
                            html.Div("Total", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 3 - Vendor Evaluation
                html.Div(className="stat-card", id="card-vendor-evaluation", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #10b981',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#ecfdf5',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-building", style={'fontSize': '20px', 'color': '#10b981'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Vendor Evaluation"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Vendor Performance"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("24", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#10b981'}),
                            html.Div("Vendors", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("18", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#10b981'}),
                            html.Div("Active", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 4 - Safety Statistics
                html.Div(className="stat-card", id="card-safety-stats", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #06b6d4',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#ecfeff',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-chart-line", style={'fontSize': '20px', 'color': '#06b6d4'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Safety Statistics"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Safety Metrics"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("245", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#06b6d4'}),
                            html.Div("Safe Days", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("0", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#06b6d4'}),
                            html.Div("Incidents", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 5 - Non Conformance
                html.Div(className="stat-card", id="card-nc-criticality", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #ef4444',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#fef2f2',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-exclamation-triangle", style={'fontSize': '20px', 'color': '#ef4444'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Non Conformance"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Quality Management"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("3", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#ef4444'}),
                            html.Div("Major", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("15", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#ef4444'}),
                            html.Div("Total", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 6 - Org Knowledge
                html.Div(className="stat-card", id="card-org-knowledge", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #ec4899',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#fdf2f8',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-graduation-cap", style={'fontSize': '20px', 'color': '#ec4899'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Org Knowledge"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Knowledge Management"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("156", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#ec4899'}),
                            html.Div("Docs", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("45", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#ec4899'}),
                            html.Div("SOPs", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 7 - Security Incidents
                html.Div(className="stat-card", id="card-security-incidents", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #8b5cf6',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#f5f3ff',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-shield-alt", style={'fontSize': '20px', 'color': '#8b5cf6'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Security Incidents"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Security Management"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("0", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#8b5cf6'}),
                            html.Div("Incidents", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("100", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#8b5cf6'}),
                            html.Div("Secure", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 8 - Quick Reports
                html.Div(className="stat-card", id="card-quick-stats", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #6366f1',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#eef2ff',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-chart-bar", style={'fontSize': '20px', 'color': '#6366f1'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Quick Reports"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Analytics"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("24", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#6366f1'}),
                            html.Div("Reports", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("12", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#6366f1'}),
                            html.Div("Dashboards", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ]),
                
                # Card 9 - Training Feedback
                html.Div(className="stat-card", id="card-training-feedback", style={
                    'background': 'white',
                    'padding': '15px',
                    'cursor': 'pointer',
                    'transition': 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': 'none',
                    'borderLeft': '4px solid #a855f7',
                    'borderBottom': '1px solid #e2e8f0',
                    'textAlign': 'center'
                }, children=[
                    html.Div(style={
                        'width': '45px',
                        'height': '45px',
                        'background': '#faf5ff',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'margin': '0 auto 10px auto',
                        'borderRadius': '10px'
                    }, children=[
                        html.I(className="fas fa-comments", style={'fontSize': '20px', 'color': '#a855f7'})
                    ]),
                    html.Div(style={
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'color': '#1e293b',
                        'marginBottom': '5px',
                        'fontFamily': 'Poppins, sans-serif'
                    }, children="Training Feedback"),
                    html.Div(style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'marginBottom': '10px',
                        'fontFamily': 'Inter, sans-serif'
                    }, children="Feedback"),
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '15px',
                        'marginTop': '5px'
                    }, children=[
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("4.8", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#a855f7'}),
                            html.Div("Rating", style={'fontSize': '9px', 'color': '#64748b'})
                        ]),
                        html.Div(style={'width': '1px', 'background': '#e2e8f0', 'height': '30px'}),
                        html.Div(style={'textAlign': 'center'}, children=[
                            html.Div("156", style={'fontSize': '18px', 'fontWeight': '700', 'color': '#a855f7'}),
                            html.Div("Responses", style={'fontSize': '9px', 'color': '#64748b'})
                        ])
                    ])
                ])
            ]),
            
            # Hidden div for navigation
            html.Div(id="dashboard-nav-click", style={"display": "none"})
        ])
    ])


def register_dashboard_callbacks(app):
    """Register callbacks for dashboard navigation"""
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("card-mom-tracking", "n_clicks"),
         Input("card-risk-tracking", "n_clicks"),
         Input("card-vendor-evaluation", "n_clicks"),
         Input("card-safety-stats", "n_clicks"),
         Input("card-nc-criticality", "n_clicks"),
         Input("card-org-knowledge", "n_clicks"),
         Input("card-security-incidents", "n_clicks"),
         Input("card-quick-stats", "n_clicks"),
         Input("card-training-feedback", "n_clicks")],
        prevent_initial_call=True
    )
    def navigate_dashboard_cards(mom, risk, vendor, safety, nc, org_knowledge, security, quick, training):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        nav_map = {
            "card-mom-tracking": "/mom-tracking",
            "card-risk-tracking": "/risk-management",
            "card-vendor-evaluation": "/procurement",
            "card-safety-stats": "/ehs-safety-dashboard",
            "card-nc-criticality": "/non-conformance",
            "card-org-knowledge": "/org-knowledge",
            "card-security-incidents": "/security-incidents",
            "card-quick-stats": "/ehs-reports",
            "card-training-feedback": "/training-feedback"
        }
        
        if button_id in nav_map:
            return nav_map[button_id]
        
        return dash.no_update