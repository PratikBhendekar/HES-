# app.py - Complete Integrated Management System

import dash
from dash import Dash, html, dcc, Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc
from flask import session, redirect, request
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
from pages.nrc import nrc_page, register_nrc_callbacks  # ADD NRC IMPORT
from routes.auth_routes import server
from utils.helpers import load_logo
from database import get_report_data

# -------------------- IMAGE ENCODING FOR CAROUSEL --------------------
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

# -------------------- DASH APP --------------------
app = Dash(
    __name__, 
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True,
    routes_pathname_prefix='/',
    requests_pathname_prefix='/'
)

# -------------------- CSS STYLES --------------------
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
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
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
        
        .modal-header h2 {
            font-size: 20px;
            color: #667eea;
            font-weight: 700;
        }
        
        .modal-close {
            cursor: pointer;
            color: #94a3b8;
            font-size: 20px;
            transition: all 0.2s ease;
        }
        
        .modal-close:hover {
            color: #ef4444;
            transform: rotate(90deg);
        }
        
        .modal-body {
            padding: 20px;
        }
        
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
        
        .modal-btn.cancel {
            background: #f1f5f9;
            color: #64748b;
        }
        
        .modal-btn.cancel:hover {
            background: #e2e8f0;
            transform: translateY(-2px);
        }
        
        .modal-btn.submit {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .modal-btn.submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .form-row {
            display: flex;
            gap: 16px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-group.half {
            flex: 1;
            min-width: 200px;
        }
        
        .form-label {
            display: block;
            font-weight: 600;
            margin-bottom: 6px;
            color: #1e293b;
            font-size: 13px;
        }
        
        .form-input, .form-textarea {
            width: 100%;
            padding: 10px 14px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 13px;
            transition: all 0.3s ease;
            background: white;
        }
        
        .form-input:focus, .form-textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
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
        
        .carousel-container {
            text-align: center;
        }
        
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
        
        .carousel-image:hover {
            transform: scale(1.02);
        }
        
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
        
        .dot:hover {
            background: #667eea;
            transform: scale(1.2);
        }
        
        .dot.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            width: 25px;
            border-radius: 10px;
        }
        
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

logo_data = load_logo(LOGO_PATH)

# -------------------- PAGE FUNCTIONS --------------------
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
    """Quality Assurance page wrapper"""
    return quality_assurance_page()

def isms_page_content():
    """ISMS page wrapper"""
    return isms_page()

def nrc_page_content():
    """NRC page wrapper"""
    return nrc_page()

# -------------------- AUTHENTICATION MIDDLEWARE --------------------
@app.server.before_request
def check_login():
    public_routes = ['/login', '/logout', '/download-permit']
    
    if any(request.path.startswith(route) for route in public_routes):
        return None
    
    if request.path.startswith('/_dash-') or request.path.startswith('/assets'):
        return None
    
    if 'user_id' not in session:
        return redirect('/login')
    
    return None

# -------------------- MAIN LAYOUT --------------------
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", data={}),
    dcc.Download(id="download-permit"),
    html.Div(className="app-container", children=[
        create_sidebar(logo_data),
        html.Div(className="main-content", id="page-content")
    ])
])

# -------------------- COMBINED NAVIGATION CALLBACKS --------------------
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

# Navigation for HR Cards - HR Business Document and HR Feedback Form
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
    elif pathname == "/nrc":  # ADD NRC ROUTE
        return nrc_page()
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

# Register all callbacks
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
register_nrc_callbacks(app)  # ADD NRC CALLBACKS

# -------------------- RUN APPLICATION --------------------
if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRATED MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Server starting on http://localhost:8090")
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
    print("   - NRC (/nrc)")  # ADD THIS
    print("=" * 60)
      
    app.run(debug=True, port=8090, host='127.0.0.1')