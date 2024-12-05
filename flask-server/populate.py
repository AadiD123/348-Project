from app import app,db, Bar, Event, Category, EventCategory  # Make sure to import your models from your main Flask app
from datetime import datetime, timedelta

# Function to delete all data and recreate tables
def reset_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully.")

# Function to populate the database
def populate_data():
    with app.app_context():
        # Add Bars
        harrys = Bar(name="Harry's", address="123 Main St", capacity=100, contact_phone="123-456-7890")
        brothers = Bar(name="Brother's", address="456 Elm St", capacity=150, contact_phone="123-456-7891")
        cactus = Bar(name="Cactus", address="789 Oak St", capacity=200, contact_phone="123-456-7892")

        db.session.add_all([harrys, brothers, cactus])
        db.session.commit()

        # Add Categories
        sports = Category(name="Sports", description="Sports events and games")
        rave = Category(name="Rave", description="High-energy dance parties")
        happy_hour = Category(name="Happy Hour", description="Discounted drinks")

        db.session.add_all([sports, rave, happy_hour])
        db.session.commit()

        # Helper function to create events
        def create_event(bar, title, description, days_from_now, start_hour, end_hour, cover_charge, categories):
            event = Event(
                bar_id=bar.bar_id,
                title=title,
                description=description,
                event_date=datetime.now().date() + timedelta(days=days_from_now),
                start_time=(datetime.now() + timedelta(hours=start_hour)).time(),
                end_time=(datetime.now() + timedelta(hours=end_hour)).time(),
                cover_charge=cover_charge,
                age_requirement=21,
                status='scheduled'
            )
            db.session.add(event)
            db.session.commit()
            
            # Associate event with categories
            for category in categories:
                event_category = EventCategory(event_id=event.event_id, category_id=category.category_id)
                db.session.add(event_category)
            db.session.commit()

        # Create events for Harry's
        create_event(harrys, "Harry's Sports Night", "Watch the big game with us!", 1, 18, 21, 10.00, [sports])
        create_event(harrys, "Harry's Rave", "Dance all night long!", 2, 22, 2, 15.00, [rave])
        create_event(harrys, "Happy Hour at Harry's", "Discounted drinks for everyone!", 3, 17, 19, 5.00, [happy_hour])

        # Create events for Brother's
        create_event(brothers, "Brother's Happy Hour", "Enjoy discounted drinks", 1, 16, 18, 5.00, [happy_hour])
        create_event(brothers, "Brother's Rave Night", "Get ready to rave!", 2, 20, 1, 15.00, [rave])

        # Create events for Cactus
        create_event(cactus, "Cactus Sports", "Catch all the action live!", 1, 19, 23, 12.00, [sports])
        create_event(cactus, "Cactus Happy Hour", "Discounted drinks to start your evening", 4, 18, 20, 6.00, [happy_hour])
        
        print("Data populated successfully.")

if __name__ == "__main__":
    reset_database()  # Uncomment this line if you want to reset the database before populating
    populate_data()
