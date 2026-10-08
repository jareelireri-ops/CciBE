from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models import Opportunity, EmployerProfile
from app.jwt import require_role
from datetime import datetime

opportunities_bp = Blueprint('opportunities', __name__)

# GET opportunities with direct frontend filters enabled
@opportunities_bp.route('/', methods=['GET'])
def get_all():
    # Start with a base query for published items
    query = Opportunity.query.filter_by(status='published')
    
    # 1. Sector Filter: If 'All' or empty, we skip filtering and show everything
    sector_param = request.args.get('sector')
    if sector_param and sector_param.lower() != 'all':
        query = query.filter(Opportunity.sector.ilike(sector_param))
        
    # 2. County/Location Filter
    county_param = request.args.get('county')
    if county_param and county_param.lower() != 'all counties':
        query = query.filter(Opportunity.location.ilike(county_param))
        
    # 3. Job Type Filter (e.g., Full-time, Part-time)
    type_param = request.args.get('type')
    if type_param and type_param.lower() != 'all types':
        query = query.filter(Opportunity.type.ilike(type_param))
        
    # 4. Schedule/Time Filter (Tracking duration or custom text field values if passed)
    time_param = request.args.get('time')
    if time_param and time_param.lower() != 'any time':
        query = query.filter(Opportunity.duration.ilike(time_param))

    # Execute query and transform data using our upgraded safe dictionary mapping
    opps = query.all()
    return jsonify([o.to_dict() for o in opps])

# GET one opportunity
@opportunities_bp.route('/<id>', methods=['GET'])
def get_one(id):
    opp = Opportunity.query.get(id)
    if not opp:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(opp.to_dict())

# POST opportunities
@opportunities_bp.route('/', methods=['POST'])
@require_role('employer')
def create():
    data = request.get_json()
    user_id = get_jwt_identity()
    employer = EmployerProfile.query.filter_by(user_id=user_id).first()

    if not employer:
        return jsonify({'message':'Create an employer profile first'}), 400

    opp = Opportunity(
        employer_id = employer.id,
        title = data['title'],
        description = data['description'],
        type = data.get('type'),
        sector = data.get('sector'),
        location = data.get('location'),
        duration = data.get('duration'),
        compensation_amount = data.get('compensation', 0), # Fallback to 0 if empty
        deadline = datetime.strptime(data['deadline'], '%Y-%m-%d') if data.get('deadline') else None,
        status = 'draft'
    )
    db.session.add(opp)
    db.session.commit()
    return jsonify(opp.to_dict()), 201

# PATCH opportunity status
@opportunities_bp.route('/<id>/status', methods=['PATCH'])
@require_role('employer')
def update_status(id):
    opp = Opportunity.query.get(id)
    if not opp:
        return jsonify({'message': 'Not found'}), 404
    opp.status = request.get_json().get('status')
    db.session.commit()
    return jsonify(opp.to_dict())

# DELETE an opportunity
@opportunities_bp.route('/<id>', methods=['DELETE'])
@require_role('employer')
def delete(id):
    opp = Opportunity.query.get(id)
    if not opp:
        return jsonify({'message': 'Not found'}), 404
    db.session.delete(opp)
    db.session.commit()
    return jsonify({'message': 'Deleted'})