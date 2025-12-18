from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Event, Resource, EventResourceAllocation
from utils import check_resource_conflict, get_all_conflicts, calculate_utilization
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total_events = Event.query.count()
    total_resources = Resource.query.count()
    total_allocations = EventResourceAllocation.query.count()
    
    return render_template('index.html', 
                         total_events=total_events,
                         total_resources=total_resources,
                         total_allocations=total_allocations)

@app.route('/events')
def events():
    events_list = Event.query.order_by(Event.start_time.desc()).all()
    return render_template('events.html', events=events_list)

@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        description = request.form['description']
        
        if start_time >= end_time:
            flash('Start time must be before end time', 'error')
            return redirect(url_for('add_event'))
        
        event = Event(title=title, start_time=start_time, end_time=end_time, description=description)
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully', 'success')
        return redirect(url_for('events'))
    
    return render_template('event_form.html', event=None)

@app.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form['title']
        event.start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        event.end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        event.description = request.form['description']
        
        if event.start_time >= event.end_time:
            flash('Start time must be before end time', 'error')
            return redirect(url_for('edit_event', event_id=event_id))
        
        allocations = EventResourceAllocation.query.filter_by(event_id=event_id).all()
        for allocation in allocations:
            has_conflict, message = check_resource_conflict(
                allocation.resource_id, 
                event_id, 
                event.start_time, 
                event.end_time
            )
            if has_conflict:
                flash(f'Cannot update: {message}', 'error')
                return redirect(url_for('edit_event', event_id=event_id))
        
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('events'))
    
    return render_template('event_form.html', event=event)

@app.route('/events/delete/<int:event_id>')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('events'))

@app.route('/resources')
def resources():
    resources_list = Resource.query.all()
    return render_template('resources.html', resources=resources_list)

@app.route('/resources/add', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        resource_name = request.form['resource_name']
        resource_type = request.form['resource_type']
        
        resource = Resource(resource_name=resource_name, resource_type=resource_type)
        db.session.add(resource)
        db.session.commit()
        
        flash('Resource created successfully', 'success')
        return redirect(url_for('resources'))
    
    return render_template('resource_form.html', resource=None)

@app.route('/resources/edit/<int:resource_id>', methods=['GET', 'POST'])
def edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    if request.method == 'POST':
        resource.resource_name = request.form['resource_name']
        resource.resource_type = request.form['resource_type']
        
        db.session.commit()
        flash('Resource updated successfully', 'success')
        return redirect(url_for('resources'))
    
    return render_template('resource_form.html', resource=resource)

@app.route('/resources/delete/<int:resource_id>')
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted successfully', 'success')
    return redirect(url_for('resources'))

@app.route('/allocate', methods=['GET', 'POST'])
def allocate():
    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        resource_ids = request.form.getlist('resource_ids')
        
        event = Event.query.get(event_id)
        
        for resource_id in resource_ids:
            resource_id = int(resource_id)
            
            has_conflict, message = check_resource_conflict(
                resource_id, 
                event_id, 
                event.start_time, 
                event.end_time
            )
            
            if has_conflict:
                flash(f'Conflict detected: {message}', 'error')
                continue
            
            existing = EventResourceAllocation.query.filter_by(
                event_id=event_id, 
                resource_id=resource_id
            ).first()
            
            if not existing:
                allocation = EventResourceAllocation(event_id=event_id, resource_id=resource_id)
                db.session.add(allocation)
        
        db.session.commit()
        flash('Resources allocated successfully', 'success')
        return redirect(url_for('allocate'))
    
    events_list = Event.query.order_by(Event.start_time.desc()).all()
    resources_list = Resource.query.all()
    allocations = EventResourceAllocation.query.all()
    
    return render_template('allocate.html', 
                         events=events_list, 
                         resources=resources_list,
                         allocations=allocations)

@app.route('/conflicts')
def conflicts():
    conflicts_list = get_all_conflicts()
    return render_template('conflicts.html', conflicts=conflicts_list)

@app.route('/utilization', methods=['GET', 'POST'])
def utilization():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        report_data = calculate_utilization(start_date, end_date)
        
        return render_template('utilization.html', 
                             report_data=report_data,
                             start_date=start_date,
                             end_date=end_date)
    
    return render_template('utilization.html', report_data=None)

if __name__ == '__main__':
    app.run(debug=True)
