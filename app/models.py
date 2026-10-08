from app import db

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(50), nullable=False)
    groups = db.Column(db.Text, nullable=False) # Store JSON string of groups
    share = db.Column(db.Boolean, default=True)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'phone_no': self.phone_no,
            'groups': json.loads(self.groups) if self.groups else [],
            'share': self.share
        }
