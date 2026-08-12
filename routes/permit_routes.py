from flask import send_file
from routes.auth_routes import server
from auth import login_required
from services.pdf_generator import generate_permit_pdf
from pages.work_permit import permits_db

@server.route('/download-permit/<permit_id>')
@login_required
def download_permit(permit_id):
    """Download permit as PDF"""
    # Find permit in database
    permit = next((p for p in permits_db if p['id'] == permit_id), None)
    
    if not permit:
        return "Permit not found", 404
    
    # Generate PDF
    buffer = generate_permit_pdf(permit)
    
    # Return as downloadable file
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"permit_{permit_id}.pdf",
        mimetype='application/pdf'
    )