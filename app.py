# app.py - Complete Integrated Management System with Advanced Design

import dash
from dash import Dash, html, dcc, Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc
from flask import Flask, session, redirect, request, send_from_directory
import secrets
from pathlib import Path
import os
import datetime
import uuid
import base64
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import SECRET_KEY, LOGO_PATH, FALLBACK_LOGO
from auth import login_required
from components.sidebar import create_sidebar
from pages.dashboard import dashboard_page, register_dashboard_callbacks
from pages.ehs_dashboard import ehs_dashboard_page, register_ehs_dashboard_callbacks
from pages.reports_analytics import reports_analytics_page, register_reports_analytics_callbacks
from pages.ehs_walkthrough_reports import ehs_walkthrough_reports_page, register_ehs_walkthrough_callbacks
from pages.work_permit import work_permit_page, register_work_permit_callbacks
from pages.placeholder import placeholder_page
from pages.mom_tracking import mom_tracking_page, register_mom_callbacks
from pages.business_development import business_development_page, register_bd_callbacks
from pages.system_admin import system_admin, register_sysadmin_callbacks
from pages.hr import hr_page, register_hr_callbacks
from pages.hr_business import hr_business_page, register_hr_business_callbacks
from pages.training_feedback import training_feedback_page, register_training_feedback_callbacks
from pages.admin_obj import admin_page, register_admin_callbacks
from pages.operation import operation_page, register_operation_callbacks
from pages.procurement import procurement_page, register_procurement_callbacks
from pages.vendor_evaluation import vendor_evaluation_page, register_vendor_evaluation_callbacks
from pages.safety_dashboard import safety_dashboard_page, register_safety_dashboard_callbacks
from pages.ims_policy import ims_policy_page
from pages.incident_investigation import incident_investigation_page, register_incident_investigation_callbacks
from pages.quality_assurance import quality_assurance_page, register_qa_callbacks
from pages.isms import isms_page, register_isms_callbacks
from pages.nrc import nrc_page, register_nrc_callbacks

# ==================== TICKET PAGES IMPORTS ====================
from pages.ticket_safety_observation import ticket_safety_observation_page, register_ticket_safety_callbacks
from pages.ticket_new_joiner import ticket_new_joiner_page, register_ticket_joiner_callbacks
from pages.ticket_vendor_orientation import ticket_vendor_orientation_page, register_ticket_vendor_callbacks
from pages.ticket_incident_report import ticket_incident_report_page, register_ticket_incident_callbacks

from routes.auth_routes import auth_bp
from utils.helpers import load_logo
from database import get_report_data, authenticate_user

# ==================== CREATE FLASK SERVER ====================
server = Flask(__name__)
server.secret_key = SECRET_KEY
server.register_blueprint(auth_bp)

# ==================== LOAD LOGO ====================
logo_data = load_logo(LOGO_PATH)

# ==================== IMAGE ENCODING FUNCTION ====================
def encode_image_to_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        if Path(image_path).exists():
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            ext = Path(image_path).suffix.lower()
            if ext in ['.jpg', '.jpeg']:
                mime = 'image/jpeg'
            elif ext == '.png':
                mime = 'image/png'
            elif ext == '.avif':
                mime = 'image/avif'
            else:
                mime = 'image/jpeg'
            return f"data:{mime};base64,{encoded}"
        else:
            print(f"⚠️ Image not found: {image_path}")
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
    return None

# ==================== ENCODE IMAGES ====================
BACKGROUND_IMAGE_PATH = r"C:\Users\12797\Downloads\premium_photo-1681823094945-41f3c086d5ec.avif"
LOGO_IMAGE_PATH = r"C:\Users\12797\Videos\07\HES1 - Copy\assets\Screenshot 2026-05-26 154737.png"

BACKGROUND_BASE64 = encode_image_to_base64(BACKGROUND_IMAGE_PATH)
LOGO_BASE64 = encode_image_to_base64(LOGO_IMAGE_PATH)

print("=" * 60)
print("IMAGE ENCODING STATUS:")
print(f"Background Image: {'✅ LOADED' if BACKGROUND_BASE64 else '❌ FAILED'}")
print(f"Logo Image: {'✅ LOADED' if LOGO_BASE64 else '❌ FAILED'}")
print("=" * 60)

# ==================== BLUES NEWS LOGIN PAGE ====================
BLUES_NEWS_LOGIN = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSTECH Ai IMS Portal</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            min-height: 100vh;
            width: 100%;
        }}
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-image: url('{BACKGROUND_BASE64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            position: relative;
        }}
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(0.5px);
            z-index: 0;
        }}
        .container {{
            background: #ffffff;
            border-radius: 28px;
            max-width: 1100px;
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.20);
            overflow: hidden;
            position: relative;
            z-index: 1;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        .left-panel {{
            background: linear-gradient(145deg, #1a3a6a, #0d2b55);
            color: #ffffff;
            padding: 45px 35px;
            flex: 1 1 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            min-height: 500px;
        }}
        .left-panel .logo-img {{
            text-align: center;
            margin-bottom: 22px;
        }}
        .left-panel .logo-img img {{
            max-width: 180px;
            height: auto;
            border-radius: 16px;
            background: #ffffff;
            padding: 12px 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.30);
            border: 2px solid rgba(79, 195, 247, 0.3);
            transition: 0.3s;
        }}
        .left-panel .logo-img img:hover {{
            transform: scale(1.03);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.40);
        }}
        .left-panel h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
            color: #ffffff;
            letter-spacing: -0.5px;
            line-height: 1.2;
            text-transform: uppercase;
            text-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
        }}
        .left-panel h1 .highlight {{
            color: #4fc3f7;
            font-weight: 900;
        }}
        .left-panel .subhead {{
            font-family: 'Open Sans', sans-serif;
            font-size: 14px;
            font-weight: 400;
            opacity: 0.85;
            margin-bottom: 32px;
            border-left: 4px solid #4fc3f7;
            padding-left: 16px;
            color: #b3d9f5;
            background: rgba(255, 255, 255, 0.06);
            padding: 10px 16px;
            border-radius: 0 10px 10px 0;
            backdrop-filter: blur(4px);
            text-transform: uppercase;
            font-size: 12px;
            font-weight: 600;
        }}
        .role-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 6px;
        }}
        .role-card {{
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(6px);
            border-radius: 12px;
            padding: 20px 18px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
        }}
        .role-card:hover {{
            background: rgba(255, 255, 255, 0.12);
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.20);
            border-color: rgba(79, 195, 247, 0.3);
        }}
        .role-card i {{
            font-size: 22px;
            color: #4fc3f7;
            margin-bottom: 8px;
            background: rgba(79, 195, 247, 0.10);
            padding: 8px;
            border-radius: 10px;
            display: inline-block;
        }}
        .role-card h4 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #ffffff;
            text-transform: uppercase;
        }}
        .role-card p {{
            font-family: 'Open Sans', sans-serif;
            font-size: 12px;
            font-weight: 400;
            opacity: 0.7;
            margin-top: 4px;
            color: #b3d9f5;
        }}
        .right-panel {{
            padding: 45px 40px;
            flex: 1 1 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: linear-gradient(145deg, #e8f0fe, #d4e4f7);
            position: relative;
        }}
        .right-panel .login-header {{
            margin-bottom: 28px;
        }}
        .right-panel .login-header h2 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: #0a1f33;
            text-transform: uppercase;
        }}
        .right-panel .login-header h2 .login-highlight {{
            color: #1a6a9e;
            font-weight: 900;
        }}
        .right-panel .login-header .login-sub {{
            font-family: 'Open Sans', sans-serif;
            color: #4a6a8a;
            font-size: 13px;
            font-weight: 400;
            margin-top: 4px;
        }}
        .form-group {{
            margin-bottom: 18px;
        }}
        .form-group label {{
            display: block;
            font-family: 'Montserrat', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: #1a2e44;
            margin-bottom: 6px;
            text-transform: uppercase;
        }}
        .form-group label i {{
            color: #1a6a9e;
            margin-right: 6px;
        }}
        .form-group input {{
            width: 100%;
            padding: 13px 18px;
            border: 2px solid rgba(200, 215, 235, 0.6);
            border-radius: 10px;
            font-family: 'Open Sans', sans-serif;
            font-size: 14px;
            font-weight: 400;
            transition: 0.3s;
            background: rgba(255, 255, 255, 0.85);
            color: #0b1a2e;
        }}
        .form-group input:focus {{
            outline: none;
            border-color: #1a6a9e;
            box-shadow: 0 0 0 4px rgba(26, 92, 138, 0.08);
            background: #ffffff;
        }}
        .form-group input::placeholder {{
            color: #8aa3c0;
            font-weight: 300;
            font-size: 13px;
        }}
        .remember-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Open Sans', sans-serif;
            font-size: 13px;
            font-weight: 400;
            margin-bottom: 24px;
        }}
        .remember-row label {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #1a2e44;
            cursor: pointer;
        }}
        .remember-row label input[type="checkbox"] {{
            width: 17px;
            height: 17px;
            accent-color: #1a6a9e;
            cursor: pointer;
        }}
        .remember-row a {{
            color: #1a6a9e;
            text-decoration: none;
            font-weight: 600;
            transition: 0.2s;
            font-family: 'Montserrat', sans-serif;
            font-size: 12px;
            text-transform: uppercase;
        }}
        .remember-row a:hover {{
            color: #0d4a7a;
            text-decoration: underline;
        }}
        .btn-login {{
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #0d2b55, #1a4a7a);
            color: white;
            border: none;
            border-radius: 10px;
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 4px 20px rgba(13, 43, 85, 0.30);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .btn-login:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 35px rgba(13, 43, 85, 0.40);
            background: linear-gradient(135deg, #0d2b55, #1a5a8a);
        }}
        .btn-login i {{
            margin-right: 8px;
        }}
        .divider {{
            text-align: center;
            margin: 22px 0 18px;
            color: #6a8aaa;
            font-family: 'Open Sans', sans-serif;
            font-size: 12px;
            font-weight: 400;
            position: relative;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .divider::before,
        .divider::after {{
            content: "";
            position: absolute;
            top: 50%;
            width: 40%;
            height: 1px;
            background: rgba(200, 215, 235, 0.6);
        }}
        .divider::before {{ left: 0; }}
        .divider::after {{ right: 0; }}
        .btn-microsoft {{
            width: 100%;
            padding: 13px;
            background: rgba(255, 255, 255, 0.85);
            border: 2px solid rgba(200, 215, 235, 0.6);
            border-radius: 10px;
            font-family: 'Montserrat', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #1a2e44;
            cursor: pointer;
            transition: 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .btn-microsoft:hover {{
            background: #ffffff;
            border-color: #1a6a9e;
            box-shadow: 0 4px 20px rgba(26, 92, 138, 0.06);
        }}
        .btn-microsoft i {{
            font-size: 20px;
            color: #2b5797;
        }}
        .footer-tags {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-top: 32px;
            gap: 8px;
            border-top: 1px solid rgba(200, 215, 235, 0.4);
            padding-top: 24px;
        }}
        .footer-tags span {{
            font-family: 'Montserrat', sans-serif;
            font-size: 11px;
            color: #1a2e44;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .footer-tags span i {{
            margin-right: 6px;
            color: #1a6a9e;
        }}
        .footer-tags .tag-desc {{
            font-weight: 400;
            color: #5a7a9a;
            font-size: 10px;
            margin-left: 4px;
            font-family: 'Open Sans', sans-serif;
            text-transform: none;
        }}
        .footer-bottom {{
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-top: 18px;
            font-family: 'Open Sans', sans-serif;
            font-size: 11px;
            font-weight: 400;
            color: #6a8aaa;
            border-top: 1px solid rgba(200, 215, 235, 0.4);
            padding-top: 18px;
        }}
        .footer-bottom a {{
            color: #1a6a9e;
            text-decoration: none;
            margin: 0 6px;
            transition: 0.2s;
            font-weight: 600;
            font-family: 'Montserrat', sans-serif;
            font-size: 10px;
            text-transform: uppercase;
        }}
        .footer-bottom a:hover {{
            color: #0d4a7a;
            text-decoration: underline;
        }}
        @media (max-width: 750px) {{
            .left-panel, .right-panel {{ flex: 1 1 100%; }}
            .role-grid {{ grid-template-columns: 1fr 1fr; }}
            .left-panel .logo-img img {{ max-width: 140px; }}
            .left-panel {{ border-right: none; border-bottom: 1px solid rgba(255, 255, 255, 0.1); min-height: 400px; }}
            .right-panel {{ border-left: none; }}
            .left-panel h1 {{ font-size: 26px; }}
            .right-panel .login-header h2 {{ font-size: 22px; }}
        }}
        @media (max-width: 450px) {{
            .role-grid {{ grid-template-columns: 1fr; }}
            .left-panel h1 {{ font-size: 20px; }}
            .right-panel {{ padding: 25px 20px; }}
            .left-panel {{ padding: 25px 20px; min-height: 350px; }}
            .left-panel .logo-img img {{ max-width: 110px; padding: 8px 14px; }}
            .right-panel .login-header h2 {{ font-size: 18px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <div class="logo-img">
                <img src="{LOGO_BASE64}" alt="CSTECH Ai Logo" />
            </div>
            <h1>Welcome to <span class="highlight">CSTECH Ai</span> IMS Portal</h1>
            <div class="subhead">
                One Integrated Platform for Quality, Safety, Environment, Compliance &amp; Excellence.
            </div>
            <div class="role-grid">
                <div class="role-card">
                    <i class="fas fa-user"></i>
                    <h4>Employee</h4>
                    <p>Access your tasks, training and records</p>
                </div>
                <div class="role-card">
                    <i class="fas fa-tasks"></i>
                    <h4>Project Manager</h4>
                    <p>Manage projects, resources and progress</p>
                </div>
                <div class="role-card">
                    <i class="fas fa-clipboard-check"></i>
                    <h4>QA Team</h4>
                    <p>Ensure quality, audits and compliance</p>
                </div>
                <div class="role-card">
                    <i class="fas fa-chart-pie"></i>
                    <h4>Management</h4>
                    <p>View dashboards, reports and insights</p>
                </div>
            </div>
        </div>
        <div class="right-panel">
            <div class="login-header">
                <h2>Login to <span class="login-highlight">your account</span></h2>
                <p class="login-sub">Please enter your credentials to continue</p>
            </div>
            <form method="POST" action="/login">
                <div class="form-group">
                    <label for="loginId"><i class="fas fa-user-circle"></i> Login ID / Email</label>
                    <input type="text" id="loginId" name="username" placeholder="Enter your email or ID" required />
                </div>
                <div class="form-group">
                    <label for="password"><i class="fas fa-lock"></i> Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" required />
                </div>
                <div class="remember-row">
                    <label>
                        <input type="checkbox" name="remember" /> Remember me
                    </label>
                    <a href="#">Forgot password?</a>
                </div>
                <button type="submit" class="btn-login"><i class="fas fa-sign-in-alt"></i> Login</button>
            </form>
            <div class="divider">or</div>
            <button class="btn-microsoft" onclick="alert('🔷 Redirecting to Microsoft login...')">
                <i class="fab fa-microsoft"></i> Sign in with Microsoft
            </button>
            <div class="footer-tags">
                <span><i class="fas fa-shield-alt"></i> Secure <span class="tag-desc">— role-based access</span></span>
                <span><i class="fas fa-clock"></i> Reliable <span class="tag-desc">— always available</span></span>
                <span><i class="fas fa-chart-line"></i> Insightful <span class="tag-desc">— real-time dashboards</span></span>
                <span><i class="fas fa-handshake"></i> Collaborative <span class="tag-desc">— better together</span></span>
            </div>
            <div class="footer-bottom">
                <span>&copy; 2024 CSTECH Ai. All rights reserved.</span>
                <span>
                    <a href="#">Privacy Policy</a> |
                    <a href="#">Terms of Use</a> |
                    <a href="#">Support</a>
                </span>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==================== LOGIN FAILED PAGE ====================
LOGIN_FAILED_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Failed</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Montserrat', 'Inter', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(145deg, #1a3a6a, #0d2b55);
        }
        .error-box {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 420px;
            border: 2px solid rgba(79, 195, 247, 0.2);
        }
        .error-box i { font-size: 60px; color: #ef4444; margin-bottom: 15px; }
        h2 { font-family: 'Montserrat', sans-serif; color: #ef4444; margin-bottom: 15px; text-transform: uppercase; }
        p { font-family: 'Open Sans', sans-serif; color: #64748b; margin-bottom: 20px; }
        .btn {
            background: linear-gradient(145deg, #1a3a6a, #0d2b55);
            color: white;
            padding: 14px 40px;
            border-radius: 12px;
            text-decoration: none;
            display: inline-block;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            transition: 0.3s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(13, 43, 85, 0.3); }
        .creds-box {
            background: #f8fafc;
            border-radius: 12px;
            padding: 15px;
            margin: 20px 0;
            border: 1px dashed #cbd5e1;
        }
        .creds-box h4 { font-family: 'Montserrat', sans-serif; color: #1a2e44; margin-bottom: 10px; font-size: 13px; text-transform: uppercase; }
        .cred-row { display: flex; justify-content: space-between; margin-bottom: 5px; color: #475569; font-family: 'Open Sans', sans-serif; font-size: 13px; }
        .cred-label { font-weight: 600; }
        .cred-value { color: #1a6a9e; font-weight: 600; }
    </style>
</head>
<body>
    <div class="error-box">
        <i class="fas fa-times-circle"></i>
        <h2>Login Failed</h2>
        <p>Invalid username or password. Please try again.</p>
        <div class="creds-box">
            <h4>📋 Demo Credentials</h4>
            <div class="cred-row">
                <span class="cred-label">Username:</span>
                <span class="cred-value">Pratik Bhendekar</span>
            </div>
            <div class="cred-row">
                <span class="cred-label">Password:</span>
                <span class="cred-value">pratik@123</span>
            </div>
        </div>
        <a href="/login" class="btn"><i class="fas fa-arrow-left"></i> Try Again</a>
    </div>
</body>
</html>
"""

# ==================== IMAGE ENCODING FOR CAROUSEL ====================
def encode_image(image_path):
    try:
        if Path(image_path).exists():
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
    return None

image_paths = [
    r"C:\Users\12797\Videos\HES1\assets\WhatsApp Image 2026-02-13 at 6.13.42 PM (1).jpeg",
    r"C:\Users\12797\Videos\HES1\assets\WhatsApp Image 2026-02-13 at 6.13.42 PM.jpeg",
    r"C:\Users\12797\Videos\HES1\assets\WhatsApp Image 2026-02-13 at 6.13.41 PM.jpeg",
    r"C:\Users\12797\Videos\HES1\assets\WhatsApp Image 2026-02-13 at 6.13.40 PM.jpeg",
    r"C:\Users\12797\Videos\HES1\assets\WhatsApp Image 2026-02-13 at 6.13.39 PM.jpeg",
    r"C:\Users\12797\Videos\HES1\assets\WhatsApp Image 2026-02-13 at 6.11.02 PM.jpeg"
]

encoded_images = [encode_image(path) for path in image_paths if encode_image(path)]

# ==================== DASH APP ====================
app = Dash(
    __name__, 
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True,
    routes_pathname_prefix='/',
    requests_pathname_prefix='/'
)

# ==================== FULL CSS STYLES ====================
app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>INTEGRATED MANAGEMENT SYSTEM</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #f0f2f5; color: #1e293b; }
        .app-container { display: flex; min-height: 100vh; }
        
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 99999;
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }
        
        .loading-container {
            text-align: center;
            animation: fadeInUp 0.3s ease;
        }
        
        .loading-spinner {
            width: 60px;
            height: 60px;
            margin: 0 auto 20px;
            position: relative;
        }
        
        .loading-spinner .circle {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(255, 255, 255, 0.2);
            border-top: 3px solid white;
            border-right: 3px solid white;
            border-radius: 50%;
            animation: spin 0.5s linear infinite;
        }
        
        .loading-spinner .inner-circle {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 30px;
            height: 30px;
            background: white;
            border-radius: 50%;
            animation: pulse 0.8s ease infinite;
        }
        
        .loading-text {
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        
        .loading-dots {
            display: flex;
            justify-content: center;
            gap: 6px;
            margin-top: 15px;
        }
        
        .loading-dots span {
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
            animation: bounce 0.8s ease infinite;
        }
        
        .loading-dots span:nth-child(1) { animation-delay: 0s; }
        .loading-dots span:nth-child(2) { animation-delay: 0.15s; }
        .loading-dots span:nth-child(3) { animation-delay: 0.3s; }
        
        .loading-progress {
            width: 200px;
            height: 3px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            margin: 20px auto 0;
            overflow: hidden;
        }
        
        .loading-progress-bar {
            width: 0%;
            height: 100%;
            background: white;
            border-radius: 10px;
            animation: progress 1s ease forwards;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
            50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        }
        
        @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes progress {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        
        .sidebar { 
            width: 240px; 
            background: linear-gradient(180deg, #1a1a3e 0%, #2d1b69 30%, #1a1a4e 60%, #0f3460 100%);
            box-shadow: 2px 0 10px rgba(0,0,0,0.1); 
            padding: 20px 15px; 
            position: fixed; 
            height: 100vh; 
            overflow-y: auto; 
            z-index: 100; 
        }
        .sidebar * {
            color: #ffffff !important;
        }
        .sidebar::-webkit-scrollbar { width: 4px; }
        .sidebar::-webkit-scrollbar-thumb { background: #8b5cf6; border-radius: 10px; }
        
        .user-info { 
            background: rgba(255,255,255,0.1); 
            border-radius: 12px; 
            padding: 12px; 
            margin-bottom: 15px; 
            border: 1px solid rgba(255,255,255,0.2); 
        }
        .user-name { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
        .user-role { font-size: 11px; margin-bottom: 6px; opacity: 0.8; }
        .user-role-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; background: rgba(255,255,255,0.2); }
        .logout-btn { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: rgba(239,68,68,0.2); border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 12px; margin-top: 8px; transition: all 0.3s ease; }
        .logout-btn:hover { background: rgba(239,68,68,0.3); transform: translateX(5px); }
        
        .search-container { position: relative; margin-bottom: 15px; }
        .search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); font-size: 13px; opacity: 0.7; }
        .sidebar-search { width: 100%; padding: 8px 10px 8px 35px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; font-size: 12px; transition: all 0.3s ease; }
        .sidebar-search:focus { outline: none; border-color: #60a5fa; background: rgba(255,255,255,0.15); }
        .sidebar-search::placeholder { opacity: 0.6; }
        
        .nav-section { margin-bottom: 12px; }
        .nav-section-title { 
            font-size: 10px; 
            font-weight: 700; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            margin-bottom: 8px; 
            padding-left: 8px;
            opacity: 0.7;
        }
        .nav-link { 
            display: flex; 
            align-items: center; 
            gap: 10px; 
            padding: 7px 12px; 
            border-radius: 8px; 
            margin-bottom: 2px; 
            font-weight: 500; 
            text-decoration: none; 
            transition: all 0.3s ease; 
            font-size: 12px; 
            cursor: pointer; 
        }
        .nav-link i { width: 18px; font-size: 13px; opacity: 0.8; }
        .nav-link:hover { background: rgba(255,255,255,0.15); transform: translateX(5px); }
        .nav-link:hover i { opacity: 1; }
        
        .collapsible { display: flex; align-items: center; justify-content: space-between; cursor: pointer; }
        .collapsible .nav-text { flex: 1; }
        .arrow-icon { margin-left: auto; transition: transform 0.3s ease; font-size: 11px; opacity: 0.7; }
        .arrow-icon.rotated { transform: rotate(90deg); }
        
        .submenu { margin-left: 20px; margin-top: 3px; border-left: 1px dashed rgba(255,255,255,0.3); padding-left: 12px; overflow: hidden; transition: max-height 0.3s ease; }
        .submenu.collapsed { max-height: 0; }
        .submenu.expanded { max-height: 500px; }
        .subnav-link { 
            display: block; 
            padding: 5px 10px; 
            text-decoration: none; 
            font-size: 11px; 
            transition: all 0.3s ease; 
            border-radius: 6px; 
            margin-bottom: 1px; 
            white-space: nowrap;
            opacity: 0.8;
        }
        .subnav-link:hover { background: rgba(255,255,255,0.1); transform: translateX(5px); opacity: 1; }
        
        .main-content { flex: 1; margin-left: 240px; padding: 20px; background: #f8fafc; min-height: 100vh; animation: contentFadeIn 0.3s ease; }
        
        @keyframes contentFadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .dashboard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .dashboard-title { font-size: 22px; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .header-search { position: relative; width: 280px; }
        .header-search i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
        .header-search-input { width: 100%; padding: 8px 10px 8px 35px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 13px; background: white; transition: all 0.3s ease; }
        .header-search-input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        .breadcrumb { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; font-size: 13px; }
        .breadcrumb-item { color: #64748b; }
        .breadcrumb-item.active { color: #667eea; font-weight: 600; }
        .breadcrumb-sep { color: #cbd5e1; }
        
        .welcome-banner {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 16px;
            padding: 20px 25px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }
        
        .welcome-text h2 {
            font-size: 20px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        
        .welcome-text p {
            opacity: 0.9;
            font-size: 13px;
        }
        
        .welcome-datetime {
            display: flex;
            gap: 15px;
        }
        
        .datetime-box {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            cursor: pointer;
            min-height: 80px;
            border: 1px solid #e2e8f0;
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .stat-icon {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #667eea20, #764ba220);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .stat-icon i {
            font-size: 20px;
            color: #667eea;
        }
        
        .stat-info {
            flex: 1;
            min-width: 0;
        }
        
        .stat-number {
            font-size: 15px;
            font-weight: 700;
            color: #1e293b;
            line-height: 1.3;
            margin-bottom: 3px;
        }
        
        .stat-label {
            font-size: 10px;
            color: #64748b;
            font-weight: 500;
        }
        
        .ehs-card { cursor: pointer; transition: all 0.3s ease; border: 1px solid #e2e8f0; }
        .ehs-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); border-color: #667eea; background: linear-gradient(135deg, #667eea02, #764ba202); }
        
        .annual-plan-card {
            background: linear-gradient(135deg, #667eea15, #764ba215);
            border: 2px solid #667eea;
            position: relative;
            overflow: hidden;
        }
        
        .annual-plan-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
            animation: pulse 3s ease infinite;
        }
        
        .annual-icon {
            font-size: 28px;
            color: #667eea;
            animation: bounce 2s ease infinite;
        }
        
        .reports-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 15px;
        }
        
        .report-card-hover {
            background: white;
            border-radius: 14px;
            padding: 25px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            position: relative;
            border: 1px solid #e2e8f0;
            overflow: visible;
        }
        
        .report-card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .report-card-icon {
            font-size: 36px;
            color: #667eea;
            margin-bottom: 12px;
            transition: all 0.3s ease;
        }
        
        .report-card-hover:hover .report-card-icon {
            color: #764ba2;
            transform: scale(1.05);
        }
        
        .report-card-title {
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0;
            transition: all 0.3s ease;
            line-height: 1.4;
        }
        
        .report-card-description {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%) translateY(-10px);
            background: #1e293b;
            color: white;
            font-size: 11px;
            line-height: 1.5;
            padding: 10px 14px;
            border-radius: 10px;
            width: 240px;
            text-align: center;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 100;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            margin-bottom: 10px;
            pointer-events: none;
        }
        
        .report-card-description::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 8px;
            border-style: solid;
            border-color: #1e293b transparent transparent transparent;
        }
        
        .report-card-hover:hover .report-card-description {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(0);
        }
        
        .policy-objectives-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        
        .policy-card {
            background: white;
            border-radius: 14px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #e9ecef;
        }
        
        .policy-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        
        .policy-card-top-bar {
            height: 5px;
        }
        
        .policy-card-top-bar.orange { background: #f59e0b; }
        .policy-card-top-bar.blue { background: #3b82f6; }
        
        .policy-card-content {
            padding: 24px;
        }
        
        .policy-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .policy-card-icon {
            width: 50px;
            height: 50px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .policy-card-icon.orange-bg { background: #fef3c7; }
        .policy-card-icon.blue-bg { background: #dbeafe; }
        
        .policy-card-icon i {
            font-size: 22px;
        }
        
        .policy-card-icon.orange-bg i { color: #f59e0b; }
        .policy-card-icon.blue-bg i { color: #3b82f6; }
        
        .policy-card-arrow {
            color: #cbd5e1;
            font-size: 18px;
        }
        
        .policy-card-title {
            font-size: 18px;
            font-weight: 700;
            color: #1e293b;
            margin: 0 0 6px 0;
        }
        
        .policy-card-description {
            font-size: 12px;
            color: #64748b;
            margin: 0;
            line-height: 1.5;
        }
        
        .pdf-viewer-container {
            background: white;
            border-radius: 14px;
            padding: 16px;
            height: calc(100vh - 180px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        
        .pdf-iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 10px;
        }
        
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            backdrop-filter: blur(4px);
        }
        
        .modal-content {
            background: white;
            border-radius: 16px;
            width: 90%;
            max-width: 800px;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            position: relative;
            margin: auto;
            animation: fadeInScale 0.3s ease-out;
        }
        
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .modal-header {
            padding: 16px 20px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 16px 16px 0 0;
            position: sticky;
            top: 0;
            background: white;
            z-index: 10;
        }
        
        .modal-header h2 { font-size: 20px; color: #667eea; font-weight: 700; }
        .modal-close { cursor: pointer; color: #94a3b8; font-size: 20px; transition: all 0.2s ease; }
        .modal-close:hover { color: #ef4444; transform: rotate(90deg); }
        .modal-body { padding: 20px; }
        .modal-footer {
            padding: 16px 20px;
            border-top: 1px solid #e2e8f0;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            background: #f8fafc;
            border-radius: 0 0 16px 16px;
        }
        .modal-btn {
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
            font-size: 13px;
        }
        .modal-btn.cancel { background: #f1f5f9; color: #64748b; }
        .modal-btn.cancel:hover { background: #e2e8f0; transform: translateY(-2px); }
        .modal-btn.submit { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
        .modal-btn.submit:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        
        .form-row { display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
        .form-group { margin-bottom: 16px; }
        .form-group.half { flex: 1; min-width: 200px; }
        .form-label { display: block; font-weight: 600; margin-bottom: 6px; color: #1e293b; font-size: 13px; }
        .form-input, .form-textarea { width: 100%; padding: 10px 14px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 13px; transition: all 0.3s ease; background: white; }
        .form-input:focus, .form-textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        
        .carousel-section {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-top: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        
        .carousel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f0f2f5;
        }
        
        .carousel-title {
            font-size: 18px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .carousel-controls {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .carousel-btn {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .carousel-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .slide-indicator {
            font-size: 13px;
            font-weight: 600;
            color: #667eea;
            background: #f0f2f5;
            padding: 6px 14px;
            border-radius: 16px;
        }
        
        .carousel-container { text-align: center; }
        
        .carousel-image-container {
            width: 100%;
            height: 350px;
            overflow: hidden;
            border-radius: 14px;
            background: #f8fafc;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .carousel-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 10px;
            transition: transform 0.3s ease;
        }
        
        .carousel-image:hover { transform: scale(1.02); }
        
        .carousel-dots {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 16px;
        }
        
        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #cbd5e1;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .dot:hover { background: #667eea; transform: scale(1.2); }
        .dot.active { background: linear-gradient(135deg, #667eea, #764ba2); width: 25px; border-radius: 10px; }
        
        .placeholder-page { background: white; border-radius: 14px; padding: 40px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .placeholder-title { font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 12px; }
        .placeholder-text { color: #64748b; margin-bottom: 25px; }
        .placeholder-icon { font-size: 40px; color: #667eea; opacity: 0.5; }
        
        @media (max-width: 1200px) { 
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .reports-grid { grid-template-columns: repeat(2, 1fr); }
            .policy-objectives-grid { grid-template-columns: 1fr; }
        }
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .main-content { margin-left: 0; }
            .stats-grid { grid-template-columns: 1fr; }
            .reports-grid { grid-template-columns: 1fr; }
            .policy-objectives-grid { grid-template-columns: 1fr; }
            .carousel-image-container { height: 200px; }
            .carousel-header { flex-direction: column; gap: 12px; }
            .modal-content { width: 95%; max-height: 90vh; }
            .modal-body { padding: 12px; }
            .welcome-banner { flex-direction: column; text-align: center; gap: 12px; }
            .welcome-datetime { flex-direction: column; gap: 8px; }
            .form-row { flex-direction: column; gap: 12px; }
        }
    </style>
</head>
<body>
    <div id="loading-overlay" class="loading-overlay" style="display: none;">
        <div class="loading-container">
            <div class="loading-spinner">
                <div class="circle"></div>
                <div class="inner-circle"></div>
            </div>
            <div class="loading-text">LOADING</div>
            <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div class="loading-progress">
                <div class="loading-progress-bar"></div>
            </div>
        </div>
    </div>
    
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
    
    <script>
        function showLoading() {
            var overlay = document.getElementById('loading-overlay');
            if (overlay) {
                overlay.style.display = 'flex';
                setTimeout(function() { hideLoading(); }, 800);
            }
        }
        function hideLoading() {
            var overlay = document.getElementById('loading-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(function() {
                    overlay.style.display = 'none';
                    overlay.style.opacity = '1';
                }, 200);
            }
        }
        window.addEventListener('load', function() { showLoading(); });
        document.addEventListener('click', function(e) {
            var target = e.target;
            while (target && target !== document) {
                if ((target.classList && (target.classList.contains('stat-card') || 
                    target.classList.contains('ehs-card') || target.classList.contains('report-card-hover') ||
                    target.classList.contains('nav-link') || target.classList.contains('mom-card') ||
                    target.classList.contains('policy-card') ||
                    target.tagName === 'BUTTON')) || target.closest('.stat-card') || 
                    target.closest('.ehs-card') || target.closest('.report-card-hover') || 
                    target.closest('.mom-card') || target.closest('.policy-card')) {
                    showLoading();
                    break;
                }
                target = target.parentNode;
            }
        });
        document.addEventListener('submit', function(e) { showLoading(); });
    </script>
</body>
</html>
"""

# ==================== AUTHENTICATION MIDDLEWARE ====================
@app.server.before_request
def check_login():
    public_routes = ['/login', '/logout', '/download-permit', '/assets']
    
    if any(request.path.startswith(route) for route in public_routes):
        return None
    
    if request.path.startswith('/_dash-') or request.path.startswith('/assets'):
        return None
    
    if 'user_id' not in session:
        return redirect('/login')
    
    return None

# ==================== MAIN LAYOUT ====================
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", data={}),
    dcc.Download(id="download-permit"),
    html.Div(className="app-container", children=[
        create_sidebar(logo_data),
        html.Div(className="main-content", id="page-content")
    ])
])

# ==================== COMBINED NAVIGATION CALLBACKS ====================
@app.callback(
    Output("user-info-sidebar", "children"),
    Input("url", "pathname")
)
def update_user_info(pathname):
    if 'user_id' in session:
        name = session.get('name', 'User')
        username = session.get('username', '')
        user_type = session.get('user_type', 'user').upper()
        return html.Div([
            html.Div(name, className="user-name"),
            html.Div(username, className="user-role"),
            html.Div(className="user-role-badge", children=user_type),
            html.A(className="logout-btn", href="/logout", children=[
                html.I(className="fas fa-sign-out-alt"), "Logout"
            ])
        ])
    else:
        return html.Div([
            html.Div("Guest", className="user-name"),
            html.Div("", className="user-role"),
            html.Div(className="user-role-badge", children="GUEST"),
            html.A(className="logout-btn", href="/login", children=[
                html.I(className="fas fa-sign-in-alt"), "Login"
            ])
        ])

@app.callback(
    [Output("qms-submenu", "className"),
     Output("qms-arrow", "className")],
    [Input("qms-toggle", "n_clicks")],
    [State("qms-submenu", "className")]
)
def toggle_qms_submenu(n_clicks, current_class):
    if n_clicks and n_clicks > 0:
        if "expanded" in current_class:
            return "submenu collapsed", "fas fa-chevron-right arrow-icon"
        else:
            return "submenu expanded", "fas fa-chevron-down arrow-icon"
    return "submenu collapsed", "fas fa-chevron-right arrow-icon"

def create_dots(active_index):
    if not encoded_images:
        return html.Div()
    return html.Div([
        html.Div(className=f"dot {'active' if i == active_index else ''}", id=f"dot-{i}")
        for i in range(len(encoded_images))
    ])

@app.callback(
    [Output("carousel-index", "data", allow_duplicate=True),
     Output("current-slide-image", "src", allow_duplicate=True),
     Output("slide-indicator", "children", allow_duplicate=True),
     Output("carousel-dots", "children", allow_duplicate=True)],
    [Input("next-slide", "n_clicks"),
     Input("prev-slide", "n_clicks")],
    [State("carousel-index", "data")],
    prevent_initial_call=True
)
def carousel_nav(next_clicks, prev_clicks, current_index):
    ctx = callback_context
    if not ctx.triggered:
        return current_index, encoded_images[current_index] if encoded_images else "", f"{current_index+1} / {len(encoded_images)}" if encoded_images else "0 / 0", create_dots(current_index)
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    current = current_index if current_index else 0
    total = len(encoded_images)
    
    if total == 0:
        return 0, "", "0 / 0", html.Div()
    
    if button_id == "next-slide":
        new_index = (current + 1) % total
    elif button_id == "prev-slide":
        new_index = (current - 1) % total    
    else:
        new_index = current
    
    return new_index, encoded_images[new_index], f"{new_index+1} / {total}", create_dots(new_index)

# ==================== NAVIGATION CALLBACK FOR TICKET CARDS ====================
@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    [Input("card-safety-ticket", "n_clicks"),
     Input("card-joiner-ticket", "n_clicks"),
     Input("card-vendor-ticket", "n_clicks"),
     Input("card-incident-ticket", "n_clicks")],
    prevent_initial_call=True
)
def navigate_ticket_cards(safety, joiner, vendor, incident):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    nav_map = {
        "card-safety-ticket": "/ticket-safety-observation",
        "card-joiner-ticket": "/ticket-new-joiner",
        "card-vendor-ticket": "/ticket-vendor-orientation",
        "card-incident-ticket": "/ticket-incident-report"
    }
    
    if button_id in nav_map:
        return nav_map[button_id]
    
    return no_update

# ==================== NAVIGATION CALLBACK FOR TICKET TOGGLE ====================
@app.callback(
    [Output("ticket-cards-container", "style"),
     Output("raise-ticket-arrow", "className")],
    [Input("raise-ticket-main-card", "n_clicks")],
    [State("ticket-cards-container", "style")]
)
def toggle_ticket_cards(n_clicks, current_style):
    if n_clicks and n_clicks > 0:
        if current_style and current_style.get('display') == 'grid':
            return {'display': 'none'}, "fas fa-chevron-down"
        else:
            return {
                'display': 'grid',
                'padding': '0 20px 20px 20px',
                'gridTemplateColumns': 'repeat(4, 1fr)',
                'gap': '16px'
            }, "fas fa-chevron-up"
    return {'display': 'none'}, "fas fa-chevron-down"

# ==================== EHS CARD NAVIGATION ====================
@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    [Input("card-annual-plan", "n_clicks"),
     Input("card-safety-dashboard", "n_clicks"),
     Input("card-reports", "n_clicks"),
     Input("card-project-safety", "n_clicks"),
     Input("card-training", "n_clicks"),
     Input("card-work-permit", "n_clicks"),
     Input("card-risk-assessment", "n_clicks"),
     Input("card-incident", "n_clicks"),
     Input("card-contractor", "n_clicks")],
    prevent_initial_call=True
)
def navigate_ehs_cards(annual_plan, safety_dash, reports, project_safety,
                       training, work_permit, risk_assessment, incident, contractor):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    nav_map = {
        "card-annual-plan": "/annual-ehs-plan",
        "card-safety-dashboard": "/ehs-safety-dashboard",
        "card-reports": "/ehs-reports",
        "card-project-safety": "/ehs-project-safety",
        "card-training": "/ehs-training-matrix",
        "card-work-permit": "/work-permit",
        "card-risk-assessment": "/ehs-risk-assessment",
        "card-incident": "/incident-management",
        "card-contractor": "/ehs-contractor"
    }
    
    if button_id in nav_map:
        return nav_map[button_id]
    
    return no_update

# ==================== POLICY AND HR NAVIGATION ====================
@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    [Input("card-objective-monitoring", "n_clicks"),
     Input("card-policy", "n_clicks")],
    prevent_initial_call=True
)
def navigate_policy_cards(obj_clicks, policy_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "card-objective-monitoring":
        return "/business-dev"
    elif button_id == "card-policy":
        return "/ims-policy"
    
    return no_update

@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    [Input("card-hr-business-doc", "n_clicks"),
     Input("card-hr-feedback", "n_clicks")],
    prevent_initial_call=True
)
def navigate_hr_cards(business_clicks, feedback_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "card-hr-business-doc":
        return "/hr-business"
    elif button_id == "card-hr-feedback":
        return "/hr-feedback"
    
    return no_update

# ==================== MAIN ROUTER ====================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def router(pathname):
    if pathname == "/" or pathname == "/dashboard":
        return dashboard_page()
    elif pathname == "/mrm":
        return placeholder_page("Management Review Meeting")
    elif pathname == "/ims":
        return placeholder_page("IMS - Integrated Management System")
    elif pathname == "/ehs":
        return ehs_dashboard_page()
    elif pathname == "/ehs-reports":
        return reports_analytics_page()
    elif pathname == "/ehs-safety-dashboard":
        return safety_dashboard_page()
    elif pathname == "/work-permit":
        return work_permit_page()
    elif pathname == "/ehs-walkthrough-reports":
        return ehs_walkthrough_reports_page()
    elif pathname == "/annual-ehs-plan":
        return annual_ehs_plan_page()
    elif pathname == "/mom-tracking":
        return mom_tracking_page()
    elif pathname == "/business-dev":
        return business_development_page()
    elif pathname == "/policy-objectives":
        return policy_objectives_page_content()
    elif pathname == "/ims-policy":
        return ims_policy_page_content()
    elif pathname == "/system-admin":
        return system_admin()
    elif pathname == "/hr":
        return hr_page()
    elif pathname == "/hr-business":
        return hr_business_page()
    elif pathname == "/hr-feedback":
        return training_feedback_page()
    elif pathname == "/admin":
        return admin_page()
    elif pathname == "/operation":
        return operation_page()
    elif pathname == "/procurement":
        return procurement_page()
    elif pathname == "/vendor-evaluation":
        return vendor_evaluation_page()
    elif pathname == "/training-feedback":
        return training_feedback_page()
    elif pathname == "/incident-management":
        return incident_investigation_page()
    elif pathname == "/quality-assurance":
        return quality_assurance_page()
    elif pathname == "/isms":
        return isms_page()
    elif pathname == "/nrc":
        return nrc_page()
    
    # ==================== TICKET PAGES ROUTES ====================
    elif pathname == "/ticket-safety-observation":
        return ticket_safety_observation_page()
    elif pathname == "/ticket-new-joiner":
        return ticket_new_joiner_page()
    elif pathname == "/ticket-vendor-orientation":
        return ticket_vendor_orientation_page()
    elif pathname == "/ticket-incident-report":
        return ticket_incident_report_page()
    
    elif pathname == "/context-organization":
        return placeholder_page("Context of the Organization")
    elif pathname == "/risk-management":
        return placeholder_page("Risk Management")
    elif pathname == "/internal-audit":
        return placeholder_page("Internal Audit")
    elif pathname == "/non-conformance":
        return placeholder_page("Non Conformance")
    elif pathname.startswith("/reports/"):
        return placeholder_page("Report Details")
    elif pathname.startswith("/ehs-"):
        return placeholder_page("EHS Module")
    else:
        return placeholder_page("404 - Page Not Found")

# ==================== PAGE FUNCTIONS ====================
def annual_ehs_plan_page():
    return html.Div([
        html.Div(className="dashboard-header", children=[
            html.H1("ANNUAL EHS ACTIVITY PLAN 2026-2027", className="dashboard-title"),
            html.Div(className="header-search", children=[
                html.I(className="fas fa-search"),
                dcc.Input(type="text", placeholder="Search...", className="header-search-input")
            ])
        ]),
        html.Div(className="breadcrumb", children=[
            html.Span("EHS", className="breadcrumb-item"),
            html.Span(">", className="breadcrumb-sep"),
            html.Span("Annual EHS Activity Plan", className="breadcrumb-item active")
        ]),
        html.Div(className="pdf-viewer-container", children=[
            html.Iframe(src="/assets/EHS_Yearly_Calendar_FY_2026_2027.pdf", className="pdf-iframe")
        ])
    ])

def policy_objectives_page_content():
    return html.Div(
        style={
            'padding': '24px',
            'background': '#f8fafc',
            'minHeight': '100vh'
        },
        children=[
            html.Div(
                style={'marginBottom': '24px'},
                children=[
                    html.H1(
                        "Policy & Objectives",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '700',
                            'color': '#1e293b',
                            'margin': '0 0 4px 0'
                        }
                    ),
                    html.P(
                        "Manage IMS Policy and monitor business objectives",
                        style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': 0
                        }
                    )
                ]
            ),
            
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 1fr)',
                    'gap': '24px'
                },
                children=[
                    html.Div(
                        id="card-objective-monitoring",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '6px', 'background': '#f59e0b'}),
                            html.Div(
                                style={'padding': '28px'},
                                children=[
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'justifyContent': 'space-between',
                                            'alignItems': 'flex-start',
                                            'marginBottom': '20px'
                                        },
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '56px',
                                                    'height': '56px',
                                                    'background': '#fef3c7',
                                                    'borderRadius': '16px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(
                                                    className="fas fa-bullseye",
                                                    style={'color': '#f59e0b', 'fontSize': '26px'}
                                                )
                                            ),
                                            html.I(
                                                className="fas fa-arrow-right",
                                                style={'color': '#cbd5e1', 'fontSize': '20px'}
                                            )
                                        ]
                                    ),
                                    html.Div([
                                        html.H3(
                                            "Objective Monitoring",
                                            style={
                                                'fontSize': '20px',
                                                'fontWeight': '700',
                                                'color': '#1e293b',
                                                'margin': '0 0 8px 0'
                                            }
                                        ),
                                        html.P(
                                            "Track and monitor Business Development objectives, KPIs, and performance metrics.",
                                            style={
                                                'fontSize': '13px',
                                                'color': '#64748b',
                                                'margin': 0,
                                                'lineHeight': '1.5'
                                            }
                                        )
                                    ])
                                ]
                            )
                        ]
                    ),
                    
                    html.Div(
                        id="card-policy",
                        style={
                            'background': 'white',
                            'borderRadius': '16px',
                            'border': '1px solid #e9ecef',
                            'overflow': 'hidden',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s'
                        },
                        children=[
                            html.Div(style={'height': '6px', 'background': '#3b82f6'}),
                            html.Div(
                                style={'padding': '28px'},
                                children=[
                                    html.Div(
                                        style={
                                            'display': 'flex',
                                            'justifyContent': 'space-between',
                                            'alignItems': 'flex-start',
                                            'marginBottom': '20px'
                                        },
                                        children=[
                                            html.Div(
                                                style={
                                                    'width': '56px',
                                                    'height': '56px',
                                                    'background': '#dbeafe',
                                                    'borderRadius': '16px',
                                                    'display': 'flex',
                                                    'alignItems': 'center',
                                                    'justifyContent': 'center'
                                                },
                                                children=html.I(
                                                    className="fas fa-file-alt",
                                                    style={'color': '#3b82f6', 'fontSize': '26px'}
                                                )
                                            ),
                                            html.I(
                                                className="fas fa-arrow-right",
                                                style={'color': '#cbd5e1', 'fontSize': '20px'}
                                            )
                                        ]
                                    ),
                                    html.Div([
                                        html.H3(
                                            "IMS Policy",
                                            style={
                                                'fontSize': '20px',
                                                'fontWeight': '700',
                                                'color': '#1e293b',
                                                'margin': '0 0 8px 0'
                                            }
                                        ),
                                        html.P(
                                            "View the Integrated Management System (IMS) Policy document.",
                                            style={
                                                'fontSize': '13px',
                                                'color': '#64748b',
                                                'margin': 0,
                                                'lineHeight': '1.5'
                                            }
                                        )
                                    ])
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def ims_policy_page_content():
    return html.Div([
        html.Div(className="dashboard-header", children=[
            html.H1("IMS POLICY", className="dashboard-title"),
            html.Div(className="header-search", children=[
                html.I(className="fas fa-search"),
                dcc.Input(type="text", placeholder="Search...", className="header-search-input")
            ])
        ]),
        html.Div(className="breadcrumb", children=[
            html.Span("QMS", className="breadcrumb-item"),
            html.Span(">", className="breadcrumb-sep"),
            html.Span("IMS Policy", className="breadcrumb-item active")
        ]),
        html.Div(className="pdf-viewer-container", children=[
            html.Iframe(src="/assets/IMS Policy Eng.pdf", className="pdf-iframe")
        ])
    ])

def quality_assurance_page_content():
    return quality_assurance_page()

def isms_page_content():
    return isms_page()

def nrc_page_content():
    return nrc_page()

# ==================== REGISTER CALLBACKS ====================
register_work_permit_callbacks(app)
register_dashboard_callbacks(app)
register_mom_callbacks(app)
register_bd_callbacks(app)
register_sysadmin_callbacks(app)
register_hr_callbacks(app)
register_hr_business_callbacks(app)
register_training_feedback_callbacks(app)
register_admin_callbacks(app)
register_operation_callbacks(app)
register_procurement_callbacks(app)
register_vendor_evaluation_callbacks(app)
register_safety_dashboard_callbacks(app)
register_reports_analytics_callbacks(app)
register_ehs_walkthrough_callbacks(app)
register_incident_investigation_callbacks(app)
register_qa_callbacks(app)
register_isms_callbacks(app)
register_nrc_callbacks(app)

# ==================== REGISTER TICKET CALLBACKS ====================
register_ticket_safety_callbacks(app)
register_ticket_joiner_callbacks(app)
register_ticket_vendor_callbacks(app)
register_ticket_incident_callbacks(app)

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRATED MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Server starting on http://localhost:8070")
    print("=" * 60)
    print("Login Credentials:")
    print("   Username: Pratik Bhendekar")
    print("   Password: pratik@123")
    print("=" * 60)
    print("Available Pages:")
    print("   - Dashboard (/)")
    print("   - EHS Dashboard (/ehs)")
    print("   - Work Permit (/work-permit)")
    print("   - MoM Tracking (/mom-tracking)")
    print("   - Business Development (/business-dev)")
    print("   - Policy & Objectives (/policy-objectives)")
    print("   - IMS Policy (/ims-policy)")
    print("   - System Admin (/system-admin)")
    print("   - HR Objectives (/hr)")
    print("   - HR Business (/hr-business)")
    print("   - HR Feedback (/hr-feedback)")
    print("   - Admin Objectives (/admin)")
    print("   - Operation Objectives (/operation)")
    print("   - Procurement (/procurement)")
    print("   - Vendor Evaluation (/vendor-evaluation)")
    print("   - Training Feedback (/training-feedback)")
    print("   - Safety Dashboard (/ehs-safety-dashboard)")
    print("   - Reports & Analytics (/ehs-reports)")
    print("   - EHS Walkthrough Reports (/ehs-walkthrough-reports)")
    print("   - Incident Investigation (/incident-management)")
    print("   - Quality Assurance (/quality-assurance)")
    print("   - ISMS (/isms)")
    print("   - NRC (/nrc)")
    print("   - Ticket: Safety Observation (/ticket-safety-observation)")
    print("   - Ticket: New Joiner (/ticket-new-joiner)")
    print("   - Ticket: Vendor Orientation (/ticket-vendor-orientation)")
    print("   - Ticket: Incident Report (/ticket-incident-report)")
    print("=" * 60)
      
    app.run(debug=True, port=8070, host='127.0.0.1')
