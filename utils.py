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
    """
    Detects all scheduling conflicts by finding events that overlap in time.
    Shows all time-overlapping events as potential scheduling conflicts.
    """
    conflicts = []
    seen_pairs = set()  # To avoid duplicate event pairs
    
    # Get all events
    all_events = Event.query.order_by(Event.start_time).all()
    
    # Check each pair of events for time overlap
    for i, event1 in enumerate(all_events):
        for event2 in all_events[i+1:]:
            # Check if events overlap in time
            if (event1.start_time < event2.end_time and 
                event1.end_time > event2.start_time):
                
                conflict_key = (event1.event_id, event2.event_id)
                
                if conflict_key not in seen_pairs:
                    seen_pairs.add(conflict_key)
                    
                    # Get all resources for both events
                    alloc1_resources = {a.resource_id for a in EventResourceAllocation.query.filter_by(event_id=event1.event_id).all()}
                    alloc2_resources = {a.resource_id for a in EventResourceAllocation.query.filter_by(event_id=event2.event_id).all()}
                    shared_resources = alloc1_resources.intersection(alloc2_resources)
                    
                    # If they share resources, add a conflict for each shared resource
                    if shared_resources:
                        for resource_id in shared_resources:
                            resource = Resource.query.get(resource_id)
                            conflicts.append({
                                'resource': resource,
                                'event1': event1,
                                'event2': event2
                            })
                    else:
                        # No shared resources yet, but events overlap (scheduling conflict)
                        # Show a conflict for EACH resource that's allocated to either event
                        all_resources = alloc1_resources.union(alloc2_resources)
                        if all_resources:
                            for resource_id in all_resources:
                                resource = Resource.query.get(resource_id)
                                conflicts.append({
                                    'resource': resource,
                                    'event1': event1,
                                    'event2': event2
                                })
                        else:
                            # No resources allocated to either event - create a placeholder
                            resource = type('obj', (object,), {
                                'resource_name': 'Time Slot',
                                'resource_type': 'scheduling'
                            })()
                            conflicts.append({
                                'resource': resource,
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
