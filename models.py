from app import db

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    allocations = db.relationship("EventResourceAllocation", backref="event")

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable =False)
    type = db.Column(db.String(50), nullable=False)

    allocations = db.relationship("EventResourceAllocation", backref="resource")

class EventResourceAllocation(db.Model):
    __tablename__ = "event_resource_allocations"

    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForignKey("resource.id"), nullable=False)