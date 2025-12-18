from models import Event, Resource, EventResourceAllocation, db
from datetime import datetime, timedelta

def check_resource_conflict(resource_id, event_id, start_time, end_time):
    if start_time >= end_time:
        return True, "Start time must be before end time"
    
    allocations = EventResourceAllocation.query.filter_by(resource_id=resource_id).all()
    
    for allocation in allocations:
        if allocation.event_id == event_id:
            continue
            
        event = Event.query.get(allocation.event_id)
        if event:
            if (start_time < event.end_time and end_time > event.start_time):
                return True, f"Conflict with event '{event.title}' ({event.start_time.strftime('%Y-%m-%d %H:%M')} - {event.end_time.strftime('%Y-%m-%d %H:%M')})"
    
    return False, None

def get_all_conflicts():
    conflicts = []
    allocations = EventResourceAllocation.query.all()
    
    for i, alloc1 in enumerate(allocations):
        event1 = Event.query.get(alloc1.event_id)
        resource1 = Resource.query.get(alloc1.resource_id)
        
        for alloc2 in allocations[i+1:]:
            if alloc1.resource_id == alloc2.resource_id:
                event2 = Event.query.get(alloc2.event_id)
                
                if event1 and event2:
                    if (event1.start_time < event2.end_time and event1.end_time > event2.start_time):
                        conflicts.append({
                            'resource': resource1,
                            'event1': event1,
                            'event2': event2
                        })
    
    return conflicts

def calculate_utilization(start_date, end_date):
    resources = Resource.query.all()
    report_data = []
    
    for resource in resources:
        total_hours = 0
        upcoming_bookings = []
        
        allocations = EventResourceAllocation.query.filter_by(resource_id=resource.resource_id).all()
        
        for allocation in allocations:
            event = Event.query.get(allocation.event_id)
            if event:
                if event.start_time.date() >= start_date and event.end_time.date() <= end_date:
                    duration = (event.end_time - event.start_time).total_seconds() / 3600
                    total_hours += duration
                    
                if event.start_time >= datetime.now():
                    upcoming_bookings.append(event)
        
        upcoming_bookings.sort(key=lambda x: x.start_time)
        
        report_data.append({
            'resource': resource,
            'total_hours': round(total_hours, 2),
            'upcoming_bookings': upcoming_bookings[:5]
        })
    
    return report_data
