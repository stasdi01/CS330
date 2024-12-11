from app import db
from datetime import datetime
import os

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save_image(self, image_file):
        if image_file:
            upload_dir = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            filename = f"{image_file.filename}"
            filepath = os.path.join(upload_dir, filename)
            
            image_file.save(filepath)
            self.image_filename = filename

    @property
    def image_url(self):
        if self.image_filename:
            return f"/static/uploads/{self.image_filename}"
        return "/static/uploads/default.png"