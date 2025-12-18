from app import app, db
from models import Event, Resource, EventResourceAllocation
from datetime import datetime, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()
    
    resources = [
        Resource(resource_name="Conference Room A", resource_type="room"),
        Resource(resource_name="HD Projector", resource_type="equipment"),
        Resource(resource_name="Senathipathi", resource_type="instructor"),
        Resource(resource_name="Laptop with HDMI", resource_type="equipment")
    ]
    
    for resource in resources:
        db.session.add(resource)
    
    db.session.commit()
   
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    
    events = [
        Event(
            title="Python Workshop",
            start_time=tomorrow.replace(hour=9, minute=0),
            end_time=tomorrow.replace(hour=11, minute=0),
            description="Introduction to Python programming for beginners"
        ),
        Event(
            title="Data Science Seminar",
            start_time=tomorrow.replace(hour=10, minute=0),
            end_time=tomorrow.replace(hour=12, minute=0),
            description="Advanced data science techniques and tools"
        ),
        Event(
            title="Web Development Class",
            start_time=tomorrow.replace(hour=14, minute=0),
            end_time=tomorrow.replace(hour=16, minute=0),
            description="Building modern web applications with Flask"
        ),
        Event(
            title="Database Workshop",
            start_time=tomorrow.replace(hour=15, minute=0),
            end_time=tomorrow.replace(hour=17, minute=0),
            description="SQL and NoSQL database fundamentals"
        )
    ]
    
    for event in events:
        db.session.add(event)
    
    db.session.commit()
    
    allocations = [
        EventResourceAllocation(event_id=1, resource_id=1),
        EventResourceAllocation(event_id=1, resource_id=2),
        EventResourceAllocation(event_id=2, resource_id=1),
        EventResourceAllocation(event_id=2, resource_id=3),
        EventResourceAllocation(event_id=3, resource_id=1),
        EventResourceAllocation(event_id=3, resource_id=4),
        EventResourceAllocation(event_id=4, resource_id=1),
        EventResourceAllocation(event_id=4, resource_id=3),
    ]
    
    for allocation in allocations:
        db.session.add(allocation)
    
    db.session.commit()
    
    print("Sample data created successfully!")
    print(f"Created {len(resources)} resources")
    print(f"Created {len(events)} events")
    print(f"Created {len(allocations)} allocations")
    print("\nNote: Events 1 and 2 overlap (9-11 and 10-12)")
    print("Note: Events 3 and 4 overlap (14-16 and 15-17)")
    print("Note: All events use Conference Room A (conflict expected)")
