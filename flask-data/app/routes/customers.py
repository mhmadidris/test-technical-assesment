from flask import Blueprint, jsonify, request
import json
import os
from app.utils.response import create_response

customers_bp = Blueprint('customers', __name__)

def load_customers_data():
    # Path relative to the root of flask-data
    file_path = os.path.join(os.getcwd(), 'data', 'customers.json')
    with open(file_path, 'r') as f:
        return json.load(f)

@customers_bp.route('/', methods=['GET'])
def get_customers():
    # Get pagination parameters from query string
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    all_data = load_customers_data()
    total = len(all_data)

    # Calculate start and end indices for pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_data = all_data[start:end]

    return create_response(
        data=paginated_data,
        message="Customers retrieved successfully",
        total=total,
        page=page,
        limit=limit
    )

@customers_bp.route('/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    data = load_customers_data()
    customer = next((item for item in data if item["customer_id"] == customer_id), None)
    if customer:
        return create_response(data=customer, message="Customer found")
    return create_response(message="Customer not found", status_code=404)
