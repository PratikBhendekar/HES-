# routes/auth_routes.py - Updated with Base64 Images

from flask import Blueprint, render_template_string, session, redirect, request
from database import authenticate_user
import base64
from pathlib import Path

auth_bp = Blueprint('auth', __name__, url_prefix='/')

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
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
    return None

# ==================== ENCODE IMAGES ====================
BACKGROUND_IMAGE_PATH = r"C:\Users\12797\Downloads\premium_photo-1681823094945-41f3c086d5ec.avif"
LOGO_IMAGE_PATH = r"C:\Users\12797\Videos\07\HES1 - Copy\assets\Screenshot 2026-05-26 154737.png"

BACKGROUND_BASE64 = encode_image_to_base64(BACKGROUND_IMAGE_PATH)
LOGO_BASE64 = encode_image_to_base64(LOGO_IMAGE_PATH)

print("=" * 60)
print("AUTH ROUTES - IMAGE ENCODING STATUS:")
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
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
            -ms-interpolation-mode: nearest-neighbor;
            -webkit-background-size: cover;
            -moz-background-size: cover;
            -o-background-size: cover;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
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
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
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
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
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
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
        }}

        .left-panel::before {{
            content: '';
            position: absolute;
            top: -30%;
            left: -20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(100, 180, 255, 0.08), transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }}

        .left-panel::after {{
            content: '';
            position: absolute;
            bottom: -20%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(100, 180, 255, 0.05), transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }}

        .left-panel>* {{
            position: relative;
            z-index: 1;
        }}

        .left-panel .logo-img {{
            text-align: center;
            margin-bottom: 22px;
            position: relative;
            z-index: 1;
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
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
            -ms-interpolation-mode: bicubic;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            display: inline-block;
        }}

        .left-panel .logo-img img:hover {{
            transform: scale(1.03);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.40);
            border-color: rgba(79, 195, 247, 0.6);
        }}

        .left-panel h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
            color: #ffffff;
            letter-spacing: -0.5px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            line-height: 1.2;
            text-transform: uppercase;
            text-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
        }}

        .left-panel h1 .highlight {{
            font-family: 'Montserrat', sans-serif;
            color: #4fc3f7;
            font-weight: 900;
            position: relative;
        }}

        .left-panel h1 .highlight::after {{
            content: '';
            position: absolute;
            bottom: 2px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4fc3f7, #81d4fa);
            border-radius: 4px;
            opacity: 0.6;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            letter-spacing: 0.3px;
            text-transform: uppercase;
            font-size: 12px;
            font-weight: 600;
        }}

        .role-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 6px;
            position: relative;
            z-index: 1;
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
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            letter-spacing: 0.3px;
            text-transform: uppercase;
        }}

        .role-card p {{
            font-family: 'Open Sans', sans-serif;
            font-size: 12px;
            font-weight: 400;
            opacity: 0.7;
            margin-top: 4px;
            color: #b3d9f5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .right-panel {{
            padding: 45px 40px;
            flex: 1 1 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: linear-gradient(145deg, #e8f0fe, #d4e4f7);
            position: relative;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-left: 1px solid rgba(255, 255, 255, 0.5);
        }}

        .right-panel::before {{
            content: '';
            position: absolute;
            top: -30%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(26, 92, 138, 0.06), transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }}

        .right-panel::after {{
            content: '';
            position: absolute;
            bottom: -20%;
            left: -10%;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(26, 92, 138, 0.04), transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }}

        .right-panel>* {{
            position: relative;
            z-index: 1;
        }}

        .right-panel .login-header {{
            margin-bottom: 28px;
        }}

        .right-panel .login-header h2 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: #0a1f33;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            letter-spacing: -0.3px;
            text-transform: uppercase;
        }}

        .right-panel .login-header h2 .login-highlight {{
            color: #1a6a9e;
            font-weight: 900;
            position: relative;
        }}

        .right-panel .login-header h2 .login-highlight::after {{
            content: '';
            position: absolute;
            bottom: 2px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #1a6a9e, #4a9ac8);
            border-radius: 4px;
            opacity: 0.5;
        }}

        .right-panel .login-header .login-sub {{
            font-family: 'Open Sans', sans-serif;
            color: #4a6a8a;
            font-size: 13px;
            font-weight: 400;
            margin-top: 4px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            letter-spacing: 0.5px;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            letter-spacing: 0.5px;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            backdrop-filter: blur(4px);
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-family: 'Montserrat', sans-serif;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
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

        .divider::before {{
            left: 0;
        }}
        .divider::after {{
            right: 0;
        }}

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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            backdrop-filter: blur(4px);
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-transform: uppercase;
            letter-spacing: 0.5px;
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
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
            letter-spacing: 0.5px;
        }}

        .footer-bottom a:hover {{
            color: #0d4a7a;
            text-decoration: underline;
        }}

        @media (max-width: 750px) {{
            .left-panel, .right-panel {{
                flex: 1 1 100%;
            }}
            .role-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            .left-panel .logo-img img {{
                max-width: 140px;
            }}
            .left-panel {{
                border-right: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                min-height: 400px;
            }}
            .right-panel {{
                border-left: none;
            }}
            .left-panel h1 {{
                font-size: 26px;
            }}
            .right-panel .login-header h2 {{
                font-size: 22px;
            }}
        }}

        @media (max-width: 450px) {{
            .role-grid {{
                grid-template-columns: 1fr;
            }}
            .left-panel h1 {{
                font-size: 20px;
            }}
            .right-panel {{
                padding: 25px 20px;
            }}
            .left-panel {{
                padding: 25px 20px;
                min-height: 350px;
            }}
            .left-panel .logo-img img {{
                max-width: 110px;
                padding: 8px 14px;
            }}
            body::before {{
                background: rgba(255, 255, 255, 0.05);
            }}
            .right-panel .login-header h2 {{
                font-size: 18px;
            }}
            .footer-tags span {{
                font-size: 9px;
            }}
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
        .error-box i {
            font-size: 60px;
            color: #ef4444;
            margin-bottom: 15px;
        }
        h2 {
            font-family: 'Montserrat', sans-serif;
            color: #ef4444;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        p {
            font-family: 'Open Sans', sans-serif;
            color: #64748b;
            margin-bottom: 20px;
        }
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
            letter-spacing: 1px;
            transition: 0.3s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(13, 43, 85, 0.3);
        }
        .creds-box {
            background: #f8fafc;
            border-radius: 12px;
            padding: 15px;
            margin: 20px 0;
            border: 1px dashed #cbd5e1;
        }
        .creds-box h4 {
            font-family: 'Montserrat', sans-serif;
            color: #1a2e44;
            margin-bottom: 10px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .cred-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            color: #475569;
            font-family: 'Open Sans', sans-serif;
            font-size: 13px;
        }
        .cred-label {
            font-weight: 600;
        }
        .cred-value {
            color: #1a6a9e;
            font-weight: 600;
        }
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

# ==================== LOGIN ROUTES ====================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"\n{'='*50}")
        print(f"LOGIN ATTEMPT")
        print(f"Username: '{username}'")
        print(f"Password: '{password}'")
        print(f"{'='*50}")
        
        user = authenticate_user(username, password)
        
        if user:
            print(f"\n✅ LOGIN SUCCESS for: {user['username']}")
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['user_type'] = user['user_type']
            session['designation'] = user.get('designation', '')
            session['email'] = user.get('email', '')
            session['phone'] = user.get('phone', '')
            return redirect('/dashboard')
        else:
            print(f"\n❌ LOGIN FAILED for: {username}")
            return LOGIN_FAILED_PAGE
    
    return BLUES_NEWS_LOGIN

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
