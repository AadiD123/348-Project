# blueprints/events.py
from flask import Blueprint, request, jsonify
from datetime import datetime, date, time
from models import db, Event, Bar

events_blueprint = Blueprint('events', __name__)
# GET all events
# events.py in the get_events route
@events_blueprint.route('/get_events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

# CREATE a new event
# events.py in the create_event route
@events_blueprint.route('/add_events', methods=['POST'])
def create_event():
    data = request.json
    try:
        # Convert event_date to a date object
        event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
        
        # Convert start_time and end_time to time objects
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        new_event = Event(
            bar_id=data['bar_id'],
            title=data['title'],
            description=data.get('description', ''),
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            cover_charge=float(data.get('cover_charge', 0.0)),  # Convert cover_charge to float
            age_requirement=data.get('age_requirement', 21),
            status=data.get('status', 'scheduled')
        )
        
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Event created", "event": new_event.to_dict()}), 201

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
    
@events_blueprint.route('/bars', methods=['GET'])
def get_bars():
    bars = Bar.query.all()
    return jsonify([{"bar_id": bar.bar_id, "name": bar.name} for bar in bars])

# Other CRUD routes (READ, UPDATE, DELETE) follow here as previously defined
