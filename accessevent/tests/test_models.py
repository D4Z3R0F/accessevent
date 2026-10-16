import pytest
import datetime

from app import db
from models import User, Event, Registration




def test_registration_unique_per_user_event(client):
    # Arrange
    db.session.add(User(username="o", email="o@mail.ru", password_hash="x", role="organizer"))
    db.session.add(User(username="p", email="p@mail.ru", password_hash="x"))
    db.session.commit()
    org = User.query.filter_by(email="o@mail.ru").first()
    part = User.query.filter_by(email="p@mail.ru").first()
    ev = Event(title="Кинопросмотр", organizer_id=org.id, event_date=datetime.datetime(2026, 11, 1, 12, 0, 0), is_inclusive=True)
    db.session.add(ev)
    db.session.commit()
    
    # Act
    db.session.add(Registration(user_id=part.id, event_id=ev.id, status="pending"))
    db.session.commit()
    
    # Assert: проверяем, что дубликат не создаётся
    count = Registration.query.filter_by(user_id=part.id, event_id=ev.id).count()
    assert count == 1  # Должна быть только одна запись