#!/usr/bin/python3
"""
View for Reviews that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def reviews_all(place_id):
    """Returns list of all Review objects for a specific Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    
    reviews_all = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_all)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_get(review_id):
    """Handles GET method for a specific Review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def review_delete(review_id):
    """Handles DELETE method for a specific Review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def review_post(place_id):
    """Handles POST method to create a new Review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")
    
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """Handles PUT method to update a Review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    
    review.save()
    return jsonify(review.to_dict()), 200
