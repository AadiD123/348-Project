from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Bar(db.Model):
    __tablename__ = 'bars'
    
    bar_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer)
    contact_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    events = db.relationship('Event', backref='bar', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'
    
    event_id = db.Column(db.Integer, primary_key=True)
    bar_id = db.Column(db.Integer, db.ForeignKey('bars.bar_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    cover_charge = db.Column(db.Numeric(10, 2))
    age_requirement = db.Column(db.Integer, default=21)
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    categories = db.relationship('Category', secondary='event_categories', backref=db.backref('events', lazy='dynamic'))

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)

# Initialize the database
with app.app_context():
    db.create_all()

# CREATE: Add a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    try:
        new_event = Event(
            bar_id=data['bar_id'],
            title=data['title'],
            description=data.get('description', ''),
            event_date=datetime.strptime(data['event_date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M:%S').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M:%S').time(),
            cover_charge=data.get('cover_charge', 0),
            age_requirement=data.get('age_requirement', 21),
            status=data.get('status', 'scheduled')
        )
        db.session.add(new_event)
        db.session.commit()

        # Relate event to category
        category_id = data['category_id']
        if category_id:
            category = Category.query.get(category_id)
            if category:
                new_event.categories.append(category)
                db.session.commit()
            else:
                return jsonify({'error': 'Category not found'}), 404
        else:
            return jsonify({'error': 'Category ID is required'}), 400

        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# READ: Get all bars
@app.route('/bars', methods=['GET'])
def get_bars():
    try:
        bars = Bar.query.all()
        bars_list = [{'bar_id': bar.bar_id, 'name': bar.name, 'address': bar.address} for bar in bars]
        return jsonify(bars_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# READ: Get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        categories_list = [{'category_id': category
                            .category_id, 'name': category.name, 'description': category.description} for category in categories]
        return jsonify(categories_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# READ: Get all events or filter by bar_id
@app.route('/events', methods=['GET'])
def get_events():
    bar_id = request.args.get('bar_id')
    try:
        if bar_id:
            events = Event.query.filter_by(bar_id=bar_id).all()
        else:
            events = Event.query.all()
        
        events_list = [{
            'event_id': event.event_id,
            'bar_id': event.bar_id,
            'title': event.title,
            'description': event.description,
            'event_date': event.event_date.isoformat(),  # Convert date to string
            'start_time': event.start_time.strftime('%H:%M:%S'),  # Convert time to string
            'end_time': event.end_time.strftime('%H:%M:%S'),  # Convert time to string
            'cover_charge': float(event.cover_charge) if event.cover_charge else None,
            'age_requirement': event.age_requirement,
            'status': event.status,
            'created_at': event.created_at.isoformat() if event.created_at else None
        } for event in events]
        
        return jsonify(events_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# READ: Get a single event by event_id
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = Event.query.get(event_id)
        if event is None:
            return jsonify({'error': 'Event not found'}), 404
        return jsonify({
            'event_id': event.event_id,
            'bar_id': event.bar_id,
            'title': event.title,
            'description': event.description,
            'event_date': event.event_date.isoformat(),  # Convert date to string
            'start_time': event.start_time.strftime('%H:%M:%S'),  # Convert time to string
            'end_time': event.end_time.strftime('%H:%M:%S'),  # Convert time to string
            'cover_charge': float(event.cover_charge) if event.cover_charge else None,
            'age_requirement': event.age_requirement,
            'status': event.status,
            'created_at': event.created_at.isoformat() if event.created_at else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# UPDATE: Update an existing event
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    try:
        event = Event.query.get(event_id)
        if event is None:
            return jsonify({'error': 'Event not found'}), 404
        
        event.bar_id = data['bar_id']
        event.title = data['title']
        event.description = data.get('description', '')
        event.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
        event.start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        event.end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        event.cover_charge = data.get('cover_charge', 0)
        event.age_requirement = data.get('age_requirement', 21)
        event.status = data.get('status', 'scheduled')
        
        db.session.commit()
        return jsonify({'message': 'Event updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# DELETE: Delete an event by event_id
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        event = Event.query.get(event_id)
        if event is None:
            return jsonify({'error': 'Event not found'}), 404
        
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@app.route('/event-stats', methods=['GET'])
def get_event_stats():
    # Extract query parameters
    category_name = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    bar_id = request.args.get('bar_id')
    print(category_name, start_date, end_date, bar_id)

    # Base query for events
    query = db.session.query(Event)

    # Filter by bar if provided
    if bar_id:
        try:
            bar_id = int(bar_id)
            query = query.filter(Event.bar_id == bar_id)
        except ValueError:
            return jsonify({"error": "Invalid bar_id format. Must be an integer."}), 400

    # Filter by date range if provided
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Event.event_date >= start_date, Event.event_date <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Filter by category if provided
    if category_name:
        query = query.join(EventCategory).join(Category).filter(Category.name == category_name)

    # Execute query with all filters
    filtered_events = query.all()
    print(filtered_events)  # Debug filtered events

    # Calculate statistics based on filtered query
    avg_cover = query.with_entities(func.avg(Event.cover_charge)).scalar() or 0
    avg_age_requirement = query.with_entities(func.avg(Event.age_requirement)).scalar() or 0
    avg_duration = query.with_entities(func.avg(
        func.julianday(Event.end_time) - func.julianday(Event.start_time)
    ) * 24 * 60).scalar() or 0  # Average duration in minutes
    avg_event_time = query.with_entities(func.avg(
        (func.strftime('%H', Event.start_time).cast(db.Integer) * 60) +
        func.strftime('%M', Event.start_time).cast(db.Integer)
    )).scalar() or 0  # Average start time in minutes from midnight

    # Convert avg_event_time back to hours and minutes
    avg_hours = int(avg_event_time // 60)
    avg_minutes = int(avg_event_time % 60)
    avg_event_time_formatted = f"{avg_hours:02}:{avg_minutes:02}"

    # Build response
    response = {
        "average_cover_charge": round(avg_cover, 2),
        "average_duration_minutes": round(avg_duration, 2),
        "average_age_requirement": round(avg_age_requirement, 2),
        "average_event_time": avg_event_time_formatted
    }

    return jsonify(response), 200

@app.route('/filtered-events', methods=['GET'])
def get_event_stats_events():
    # Extract query parameters
    category_name = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    bar_id = request.args.get('bar_id')

    # Base query for events
    query = db.session.query(Event)

    # Filter by bar if provided
    if bar_id:
        try:
            bar_id = int(bar_id)
            query = query.filter(Event.bar_id == bar_id)
        except ValueError:
            return jsonify({"error": "Invalid bar_id format. Must be an integer."}), 400

    # Filter by date range if provided
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Event.event_date >= start_date, Event.event_date <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Filter by category if provided
    if category_name:
        query = query.join(EventCategory).join(Category).filter(Category.name == category_name)

    # Execute query with all filters
    filtered_events = query.all()
    events_list = [{
            'event_id': event.event_id,
            'bar_id': event.bar_id,
            'title': event.title,
            'description': event.description,
            'event_date': event.event_date.isoformat(),  # Convert date to string
            'start_time': event.start_time.strftime('%H:%M:%S'),  # Convert time to string
            'end_time': event.end_time.strftime('%H:%M:%S'),  # Convert time to string
            'cover_charge': float(event.cover_charge) if event.cover_charge else None,
            'age_requirement': event.age_requirement,
            'status': event.status,
            'created_at': event.created_at.isoformat() if event.created_at else None
        } for event in filtered_events]
        
    return jsonify(events_list)
    

# Ensure this code is in your main script
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create tables with the updated structure
    app.run(debug=True)
