from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date 
import json
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///workshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Appointment(db.Model):  
 id = db.Column(db.Interger, primary_key=True),
Customer_name=db.Column(db.String(100), nullable=False)
Customer_email=db.Column(db.String(100), nullable=False)
customer_phone = db.Column(db.String(20), nullable=False)
appointment_date = db.Column(db.String(20), nullable=False)
appointment_time = db.Column(db.String(20), nullable=False)
car_make = db.Column(db.String(50), nullable=False)
car_model = db.Column(db.String(50), nullable=False)
car_year = db.Column(db.String(4), nullable=False)
car_license = db.Column(db.String(20), nullable=False)
service_type = db.Column(db.String(100), nullable=False)
car_issues = db.Column(db.Text, nullable=True)
status = db.Column(db.String(20), default='pending')
created_at = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'appointment_date': self.appointment_date,
            'appointment_time': self.appointment_time,
            'car_make': self.car_make,
            'car_model': self.car_model,
            'car_year': self.car_year,
            'car_license': self.car_license,
            'service_type': self.service_type,
            'car_issues': self.car_issues,
            'status': self.status,
            'created_at': self.created_at
        }

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # Get form data
        appointment = Appointment(
            customer_name=request.form['customer_name'],
            customer_email=request.form['customer_email'],
            customer_phone=request.form['customer_phone'],
            appointment_date=request.form['appointment_date'],
            appointment_time=request.form['appointment_time'],
            car_make=request.form['car_make'],
            car_model=request.form['car_model'],
            car_year=request.form['car_year'],
            car_license=request.form['car_license'],
            service_type=request.form['service_type'],
            car_issues=request.form.get('car_issues', '')
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return redirect(url_for('confirmation', id=appointment.id))
    
    return render_template('schedule.html')

@app.route('/confirmation/<int:id>')
def confirmation(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template('confirmation.html', appointment=appointment)

@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('appointments.html', appointments=all_appointments)

@app.route('/api/appointments')
def api_appointments():
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])

@app.route('/api/check-availability')
def check_availability():
    date = request.args.get('date')
    time = request.args.get('time')
    
    existing = Appointment.query.filter_by(
        appointment_date=date,
        appointment_time=time
    ).first()
    
    return jsonify({'available': existing is None})

@app.route('/cancel/<int:id>')
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('appointments'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)