from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import current_app, request

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        facade = current_app.config['FACADE']
        try:
            review_data = request.json
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        facade = current_app.config['FACADE']
        reviews = facade.get_all_reviews()

        if not reviews:
            return {'error': 'List of reviews not found'}, 404

        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        facade = current_app.config['FACADE']
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError:
            api.abort(404, f"Review with ID {review_id} not found")

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        facade = current_app.config['FACADE']
        try:
            review_data = request.json
            updated_review = facade.update_review(review_id, review_data)
            # return updated_review.to_dict(), 200
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            if str(e) == "Review not found":
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        facade = current_app.config['FACADE']
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError:
            api.abort(404, f"Review with ID {review_id} not found")

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        facade = current_app.config['FACADE']
        try:
            reviews = facade.get_reviews_by_place(place_id)
            if not reviews:
                return {"Error": "No reviews found for this place"}, 404
            return [review.to_dict() for review in reviews], 200
        except ValueError:
            api.abort(404, f"Place with ID {place_id} not found")