from flask import Blueprint, request, jsonify
from app.models import Member
from app import db
import json

members_bp = Blueprint('members', __name__)

@members_bp.route('', methods=['GET'])
def get_members():
    members = Member.query.filter_by(share=True).all()
    return jsonify([member.to_dict() for member in members])

@members_bp.route('', methods=['POST'])
def add_member():
    data = request.get_json()
    
    name = data.get('name')
    number = data.get('number')
    groups = data.get('groups', [])
    share = data.get('share', False)
    
    new_member = Member(
        name=name,
        phone_no=number,
        groups=json.dumps(groups),
        share=share
    )
    
    db.session.add(new_member)
    db.session.commit()
    
    return jsonify({
        'id': new_member.id,
        'name': new_member.name,
        'number': new_member.phone_no,
        'groups': groups,
        'share': new_member.share
    }), 201
