from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import event_controller

event_bp = Blueprint("events", __name__)

# Public reads
event_bp.route("/events", methods=["GET"])(event_controller.list_events)
event_bp.route("/events/search", methods=["GET"])(event_controller.search_events)
event_bp.route("/events/<int:event_id>", methods=["GET"])(event_controller.get_event)

# Authenticated user actions
event_bp.route("/events/<int:event_id>/register", methods=["POST"])(
    jwt_required()(event_controller.register_for_event)
)
event_bp.route("/my-events", methods=["GET"])(
    jwt_required()(event_controller.my_events)
)

# VULN A01: event mutation endpoints require JWT but NOT admin role.
# Any authenticated user can create/update/delete events.
# FIX: replace jwt_required() with admin_required from middleware.auth.
event_bp.route("/events", methods=["POST"])(
    jwt_required()(event_controller.create_event)
)
event_bp.route("/events/<int:event_id>", methods=["PUT"])(
    jwt_required()(event_controller.update_event)
)
event_bp.route("/events/<int:event_id>", methods=["DELETE"])(
    jwt_required()(event_controller.delete_event)
)
