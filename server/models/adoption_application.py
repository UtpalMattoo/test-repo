from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import db


class AdoptionApplication(db.Model):
    """Model for dog adoption applications."""
    
    __tablename__ = 'adoption_applications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dogs.id'), nullable=False, unique=True)
    applicant_name = Column(String(50), nullable=False)
    applicant_email = Column(String(320), nullable=False)
    applicant_phone = Column(String(15), nullable=False)
    submission_timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    application_status = Column(String(20), nullable=False, default='PENDING')
    
    # Relationship to Dog model
    dog = relationship("Dog", back_populates="applications")
    
    def __init__(self, **kwargs):
        """Initialize AdoptionApplication with default values."""
        super().__init__(**kwargs)
        # Set default values if not provided
        if not hasattr(self, 'application_status') or self.application_status is None:
            self.application_status = 'PENDING'
        if not hasattr(self, 'submission_timestamp') or self.submission_timestamp is None:
            self.submission_timestamp = datetime.now(timezone.utc)
    
    def __repr__(self) -> str:
        return f'<AdoptionApplication {self.id} for Dog {self.dog_id}>'
    
    def to_dict(self) -> dict:
        """Convert application to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'dog_id': self.dog_id,
            'applicant_name': self.applicant_name,
            'applicant_email': self.applicant_email,
            'applicant_phone': self.applicant_phone,
            'submission_timestamp': self.submission_timestamp.isoformat() if self.submission_timestamp else None,
            'application_status': self.application_status
        }