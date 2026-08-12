import io
import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from config import LOGO_PATH

def generate_permit_pdf(permit):
    """Generate PDF for permit"""
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # Center alignment
        spaceAfter=20,
        textColor=colors.HexColor('#667eea')
    )
    
    # Add logo if available
    try:
        if Path(LOGO_PATH).exists():
            img = Image(LOGO_PATH, width=1.5*inch, height=0.5*inch)
            story.append(img)
    except:
        pass
    
    # Title
    if permit['type'] == 'height':
        title = "HEIGHT WORK PERMIT (Above 1.8 meter height)"
    elif permit['type'] == 'electrical':
        title = "PERMIT TO WORK - ELECTRICAL"
    else:
        title = "EXCAVATION PERMIT TO WORK"
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Document info
    doc_info = [
        ["Document no:", permit.get('doc_no', 'IMS/EHS/FR/PTW/WAH')],
        ["Version:", "1.1"],
        ["Issue date:", permit.get('issue_date', datetime.datetime.now().strftime('%Y-%m-%d'))]
    ]
    
    doc_table = Table(doc_info, colWidths=[100, 300])
    doc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))
    story.append(doc_table)
    story.append(Spacer(1, 20))
    
    # Permit Details
    story.append(Paragraph("PERMIT DETAILS:", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    permit_details = [
        ["Name of project:", permit.get('project', ''), "Permit no:", permit.get('permit_no', '')],
        ["Name of contractor:", permit.get('contractor', ''), "No of contractor workers:", permit.get('workers', '')],
        ["Exact location:", permit.get('location', ''), "", ""],
        ["Permit Validity Date:", permit.get('validity_date', ''), "Time From:", permit.get('time_from', '')],
        ["", "", "To:", permit.get('time_to', '')]
    ]
    
    details_table = Table(permit_details, colWidths=[120, 150, 120, 150])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 20))
    
    # Work Description
    story.append(Paragraph("WORK DESCRIPTION:", styles['Heading2']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(permit.get('description', ''), styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Risk Assessment
    story.append(Paragraph("RISK ASSESSMENT", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    risk_data = [
        ["Is Risk assessment done for work activity planned?", "Yes" if permit.get('risk_assessment') else "No"],
        ["Is SOP available and communicated to all workers?", "Yes" if permit.get('sop_available') else "No"]
    ]
    
    risk_table = Table(risk_data, colWidths=[300, 100])
    risk_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 20))
    
    # Declaration based on permit type
    story.append(Paragraph("DECLARATION:", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    if permit['type'] == 'height':
        decl_data = [
            ["1. All workers inducted, medically fit, and briefed on task/PPE?", "Yes" if permit.get('decl_1') else "No"],
            ["2. All workers trained on harness/PFAS use?", "Yes" if permit.get('decl_2') else "No"],
            ["3. Appropriate access/egress and anchor points provided?", "Yes" if permit.get('decl_3') else "No"],
            ["4. Area barricaded; no activity/vehicles below?", "Yes" if permit.get('decl_4') else "No"],
            ["5. No overhead electrical hazards; weather suitable?", "Yes" if permit.get('decl_5') else "No"],
            ["6. Rescue plan briefed and in place?", "Yes" if permit.get('decl_6') else "No"]
        ]
    elif permit['type'] == 'electrical':
        decl_data = [
            ["1. Verified all workers medically fit to work?", "Yes" if permit.get('decl_1') else "No"],
            ["2. All workers have received job specific trainings?", "Yes" if permit.get('decl_2') else "No"],
            ["3. Workers competent to get the job done as per SOP?", "Yes" if permit.get('decl_3') else "No"],
            ["4. PPE provided and in good condition?", "Yes" if permit.get('decl_4') else "No"],
            ["5. All required permissions and licensed obtained?", "Yes" if permit.get('decl_5') else "No"],
            ["6. All hazards identified and control measures taken?", "Yes" if permit.get('decl_6') else "No"],
            ["7. Is LOTO implemented?", "Yes" if permit.get('decl_7') else "No"],
            ["8. Measuring tools calibrated?", "Yes" if permit.get('decl_8') else "No"],
            ["9. Emergency procedure communicated to all?", "Yes" if permit.get('decl_9') else "No"]
        ]
    else:
        decl_data = [
            ["1. Underground services located and marked?", "Yes" if permit.get('decl_1') else "No"],
            ["2. Excavation greater than 1.5m - shoring/benching provided?", "Yes" if permit.get('decl_2') else "No"],
            ["3. Safe means of access/egress provided?", "Yes" if permit.get('decl_3') else "No"],
            ["4. Excavation protected from vehicle collision?", "Yes" if permit.get('decl_4') else "No"],
            ["5. Excavated material placed at safe distance?", "Yes" if permit.get('decl_5') else "No"],
            ["6. Atmospheric testing done if required?", "Yes" if permit.get('decl_6') else "No"]
        ]
    
    decl_table = Table(decl_data, colWidths=[350, 50])
    decl_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))
    story.append(decl_table)
    story.append(Spacer(1, 20))
    
    # Equipment Compliance for Height Work
    if permit['type'] == 'height':
        story.append(Paragraph("EQUIPMENT COMPLIANCE", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        equip_data = [
            ["Scaffold compliant?", "Yes" if permit.get('scaffold_compliant') else "No"],
            ["MEWP compliant?", "Yes" if permit.get('mewp_compliant') else "No"],
            ["Other Equipment compliant?", "Yes" if permit.get('other_compliant') else "No"]
        ]
        
        equip_table = Table(equip_data, colWidths=[300, 100])
        equip_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(equip_table)
        story.append(Spacer(1, 20))
    
    # Permit Open
    story.append(Paragraph("PERMIT OPEN", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    open_data = [
        ["Permit Requestor", "Permit Holder", "Permit Approver"],
        [
            f"Name: {permit.get('requestor_name', '')}\nDate: {permit.get('requestor_date', '')}\nTime: {permit.get('requestor_time', '')}",
            f"Name: {permit.get('holder_name', '')}\nDate: {permit.get('holder_date', '')}\nTime: {permit.get('holder_time', '')}",
            f"Name: {permit.get('approver_name', '')}\nDate: {permit.get('approver_date', '')}\nTime: {permit.get('approver_time', '')}"
        ]
    ]
    
    open_table = Table(open_data, colWidths=[150, 150, 150])
    open_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    story.append(open_table)
    story.append(Spacer(1, 20))
    
    # Notes
    story.append(Paragraph("Note:", styles['Heading3']))
    story.append(Paragraph("1. Any change will invalidate this permit.", styles['Normal']))
    story.append(Paragraph("2. The copy of this Work permit shall be displayed at the location of work.", styles['Normal']))
    if permit['type'] == 'height':
        story.append(Paragraph("3. If Hot works are planned at Height, hot work permit shall be obtained separately.", styles['Normal']))
        story.append(Paragraph("4. No. of workmen deployed Annexure shall be attached with this Work Permit.", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer