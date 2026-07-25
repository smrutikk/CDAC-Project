from flask import request, jsonify
from sqlalchemy import text
from flask_jwt_extended import get_jwt_identity

from database import db
from models.event import Event, Registration


def list_events():
    return jsonify([e.to_dict() for e in Event.query.all()])


def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict())


def search_events():
    """
    VULN A03: SQL Injection.
    User-controlled `name` is concatenated directly into a raw SQL string.
    Example exploit:  /api/events/search?name=' OR '1'='1
    FIX: use parameterized query / SQLAlchemy filter:
        Event.query.filter(Event.name.ilike(f"%{name}%")).all()
    """
    name = request.args.get("name", "")
    query = "SELECT id, name, description, location, date, capacity FROM events " \
            "WHERE name LIKE '%" + name + "%'"
    result = db.session.execute(text(query))
    rows = [dict(r._mapping) for r in result]
    return jsonify(rows)


def create_event():
    data = request.get_json() or {}
    required = ["name", "description", "location", "date"]
    if not all(data.get(k) for k in required):
        return jsonify({"error": "Missing fields"}), 400
    event = Event(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        date=data["date"],
        capacity=int(data.get("capacity", 100)),
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201


def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    data = request.get_json() or {}
    for f in ["name", "description", "location", "date", "capacity"]:
        if f in data:
            setattr(event, f, data[f])
    db.session.commit()
    return jsonify(event.to_dict())


def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Deleted"})


def register_for_event(event_id):
    user_id = int(get_jwt_identity())
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({"error": "Already registered"}), 409
    reg = Registration(user_id=user_id, event_id=event_id)
    db.session.add(reg)
    db.session.commit()
    return jsonify({"message": "Registered", "event": event.to_dict()}), 201


def my_events():
    user_id = int(get_jwt_identity())
    regs = Registration.query.filter_by(user_id=user_id).all()
    events = [Event.query.get(r.event_id).to_dict() for r in regs if Event.query.get(r.event_id)]
    return jsonify(events)


def all_registrations():
    regs = Registration.query.all()
    return jsonify([
        {"id": r.id, "user_id": r.user_id, "event_id": r.event_id}
        for r in regs
    ])
