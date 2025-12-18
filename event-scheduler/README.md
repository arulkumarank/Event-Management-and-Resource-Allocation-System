# Event Scheduling & Resource Allocation System

A Flask-based web application for managing events and allocating shared resources with built-in conflict detection.

## Features

- Event Management: Create, edit, view, and delete events
- Resource Management: Manage rooms, instructors, equipment, and other resources
- Resource Allocation: Assign resources to events
- Conflict Detection: Automatic detection of double-booking and time overlaps
- Utilization Reports: Track resource usage over time periods

## Technology Stack

- Backend: Flask, SQLAlchemy
- Database: SQLite
- Frontend: HTML, CSS (minimalistic design)
- Python 3.x

## Installation

1. Clone the repository

```
git clone <repository-url>
cd event-scheduler
```

2. Create a virtual environment

```
python -m venv venv
```

3. Activate the virtual environment

Windows:
```
venv\Scripts\activate
```

Linux/Mac:
```
source venv/bin/activate
```

4. Install dependencies

```
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server

```
python app.py
```

2. Open your browser and navigate to

```
http://127.0.0.1:5000
```

## Usage Guide

### Creating Resources

1. Navigate to Resources page
2. Click "Add New Resource"
3. Enter resource name and select type (room, instructor, equipment, other)
4. Click "Create Resource"

### Creating Events

1. Navigate to Events page
2. Click "Add New Event"
3. Fill in event details:
   - Title
   - Start time
   - End time
   - Description
4. Click "Create Event"

### Allocating Resources

1. Navigate to Allocate page
2. Select an event from the dropdown
3. Check the resources you want to allocate
4. Click "Allocate Resources"
5. System will show warnings if conflicts are detected

### Viewing Conflicts

1. Navigate to Conflicts page
2. View all detected resource booking conflicts
3. System shows which events are conflicting and the time overlap

### Generating Utilization Reports

1. Navigate to Utilization Report page
2. Select start date and end date
3. Click "Generate Report"
4. View resource usage statistics and upcoming bookings

## Database Schema

### Event Table
- event_id: Primary key
- title: Event name
- start_time: Event start datetime
- end_time: Event end datetime
- description: Event details

### Resource Table
- resource_id: Primary key
- resource_name: Name of the resource
- resource_type: Type (room, instructor, equipment, other)

### EventResourceAllocation Table
- allocation_id: Primary key
- event_id: Foreign key to Event
- resource_id: Foreign key to Resource

## Conflict Detection Logic

The system checks for conflicts by:

1. Validating that start time is before end time
2. Checking for overlapping time intervals
3. Handling edge cases:
   - Exact time matches
   - Partial overlaps
   - Nested intervals
   - Events starting when another ends

Algorithm: Two events conflict if (start1 < end2) AND (end1 > start2)

## Sample Data

The application includes test cases for:
- 4 Resources (Conference Room A, Projector, Instructor John, Laptop)
- 4 Events with intentional time overlaps
- Multiple allocations demonstrating conflict scenarios

## Screenshots

### Dashboard
The main dashboard shows system statistics and quick action buttons.

### Events Management
View, create, edit, and delete events with datetime pickers.

### Resources Management
Manage all types of resources with simple forms.

### Resource Allocation
Allocate multiple resources to events with inline conflict warnings.

### Conflict Detection
Automatically detects and displays all resource booking conflicts.

### Utilization Report
Generate reports showing resource usage over custom date ranges.

## Video Demonstration

A complete walkthrough video demonstrating all features is available at:
[Link to be added]

## Project Structure

```
event-scheduler/
├── app.py                  Main Flask application
├── models.py              Database models
├── utils.py               Utility functions
├── requirements.txt       Python dependencies
├── database.db            SQLite database
├── static/
│   └── style.css         Minimalistic stylesheet
└── templates/
    ├── base.html         Base template
    ├── index.html        Dashboard
    ├── events.html       Event listing
    ├── event_form.html   Event form
    ├── resources.html    Resource listing
    ├── resource_form.html Resource form
    ├── allocate.html     Allocation interface
    ├── conflicts.html    Conflict view
    └── utilization.html  Report view
```

## Development Notes

- No code comments (as per requirements)
- Minimalistic UI design
- Clean and structured code
- Proper separation of concerns
- SQLAlchemy ORM for database operations
- Flask flash messages for user feedback

## Future Enhancements

- User authentication and authorization
- Email notifications for upcoming events
- Calendar view for events
- Export reports to PDF/Excel
- Recurring events support
- Multi-language support

## Author

Developed as part of technical assessment for web application development skills.
