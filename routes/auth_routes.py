from flask import Flask, session, redirect, request
import secrets
from database import authenticate_user

SECRET_KEY = secrets.token_hex(32)

server = Flask(__name__)
server.secret_key = SECRET_KEY

@server.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"\n{'='*50}")
        print(f"LOGIN ATTEMPT")
        print(f"Username: '{username}'")
        print(f"Password: '{password}'")
        print(f"{'='*50}")
        
        # Authenticate from database
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
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login Failed</title>
                <style>
                    body { font-family: 'Inter', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                    .error-box { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); text-align: center; max-width: 400px; }
                    h2 { color: #ef4444; margin-bottom: 15px; }
                    p { color: #64748b; margin-bottom: 20px; }
                    .btn { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; }
                </style>
            </head>
            <body>
                <div class="error-box">
                    <h2>Login Failed</h2>
                    <p>Invalid username or password</p>
                    <p><strong>Username:</strong> Pratik Bhendekar<br><strong>Password:</strong> pratik@123</p>
                    <a href="/login" class="btn">Try Again</a>
                </div>
            </body>
            </html>
            """
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>IMS Portal Login</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-container {
                width: 100%;
                max-width: 450px;
                padding: 20px;
            }
            .login-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.3);
                animation: slideUp 0.5s ease;
            }
            @keyframes slideUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            .logo {
                text-align: center;
                margin-bottom: 30px;
            }
            .logo h1 {
                font-size: 28px;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 5px;
            }
            .logo p {
                color: #64748b;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-label {
                display: block;
                font-weight: 600;
                margin-bottom: 8px;
                color: #1e293b;
                font-size: 14px;
            }
            .form-input {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                font-size: 14px;
                transition: all 0.3s ease;
                background: white;
            }
            .form-input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .login-btn {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 10px;
            }
            .login-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                color: #94a3b8;
                font-size: 12px;
            }
            .credentials {
                background: #f8fafc;
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                font-size: 12px;
                border: 1px dashed #cbd5e1;
            }
            .credentials h4 {
                color: #1e293b;
                margin-bottom: 10px;
            }
            .cred-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 5px;
                color: #475569;
            }
            .cred-label {
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-card">
                <div class="logo">
                    <h1>INTEGRATED MANAGEMENT SYSTEM</h1>
                    <p>Environment Health & Safety Management System</p>
                </div>
                
                <form method="POST" action="/login">
                    <div class="form-group">
                        <label class="form-label">Username</label>
                        <input type="text" name="username" class="form-input" placeholder="Enter employee name" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-input" placeholder="Enter password" required>
                    </div>
                    
                    <button type="submit" class="login-btn">Sign In</button>
                </form>
                
                <div class="credentials">
                    <h4>Database Credentials:</h4>
                    <div class="cred-row">
                        <span class="cred-label">Username:</span>
                        <span>Pratik Bhendekar</span>
                    </div>
                    <div class="cred-row">
                        <span class="cred-label">Password:</span>
                        <span>pratik@123</span>
                    </div>
                </div>
                
                <div class="footer">
                    &copy; 2024 Integrated Management System. All rights reserved.
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@server.route('/logout')
def logout():
    session.clear()
    return redirect('/login')