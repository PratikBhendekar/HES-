import datetime
import uuid

class Permit:
    def __init__(self, permit_type, project, contractor, workers, location, 
                 from_date, to_date, from_time, to_time, description, risk_check,
                 requestor, holder, approver, height_decl=None, elec_decl=None, 
                 exc_decl=None, equipment=None):
        
        self.id = str(uuid.uuid4())
        self.type = permit_type
        self.permit_no = f"{permit_type[:2].upper()}-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:3]}"
        self.project = project or ""
        self.contractor = contractor or ""
        self.workers = workers or ""
        self.location = location or ""
        self.valid_from = from_date or datetime.datetime.now().strftime('%Y-%m-%d')
        self.valid_to = to_date or (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        self.time_from = from_time or "08:00"
        self.time_to = to_time or "17:00"
        self.description = description or ""
        self.risk_assessment = "risk_done" in (risk_check or [])
        self.sop_available = "sop_available" in (risk_check or [])
        self.requestor_name = requestor or ""
        self.holder_name = holder or ""
        self.approver_name = approver or ""
        self.requestor_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.holder_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.approver_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.requestor_time = datetime.datetime.now().strftime('%H:%M')
        self.holder_time = datetime.datetime.now().strftime('%H:%M')
        self.approver_time = datetime.datetime.now().strftime('%H:%M')
        self.status = "active"
        self.created_at = datetime.datetime.now().isoformat()
        self.doc_no = {
            "height": "IMS/EHS/FR/PTW/WAH",
            "electrical": "IMS/EHS/FR/PTW/ELEC",
            "excavation": "IMS/EHS/FR/PTW/EXC"
        }.get(permit_type, "IMS/EHS/FR/PTW")
        
        # Add type-specific fields
        if permit_type == "height":
            for i in range(1, 7):
                setattr(self, f"decl_{i}", f"decl_{i}" in (height_decl or []))
            self.scaffold_compliant = "scaffold" in (equipment or [])
            self.mewp_compliant = "mewp" in (equipment or [])
            self.other_compliant = "other" in (equipment or [])
        elif permit_type == "electrical":
            for i in range(1, 10):
                setattr(self, f"decl_{i}", f"decl_{i}" in (elec_decl or []))
        elif permit_type == "excavation":
            for i in range(1, 7):
                setattr(self, f"decl_{i}", f"decl_{i}" in (exc_decl or []))
    
    def to_dict(self):
        return self.__dict__