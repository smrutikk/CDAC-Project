from flask import Blueprint, jsonify
from controllers import event_controller
from models.user import User

# VULN A01: Broken Access Control.
# These admin endpoints do NOT verify JWT or role. Any anonymous caller can hit
# them and read user/registration data or manage events.
# FIX: apply @admin_required from middleware.auth to every route below.
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/events", methods=["GET"])
def admin_list_events():
    from models.event import Event
    return jsonify([e.to_dict() for e in Event.query.all()])


@admin_bp.route("/admin/users", methods=["GET"])
def admin_list_users():
    users = User.query.all()
    # Also leaks password hashes -- part of the intentional issue.
    return jsonify([
        {**u.to_dict(), "password_hash": u.password} for u in users
    ])


@admin_bp.route("/admin/registrations", methods=["GET"])
def admin_registrations():
    return event_controller.all_registrations()
