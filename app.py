from flask import Flask, jsonify, request
from duckfine import DuckFine

app = Flask(__name__)

# run this using "http://localhost:5000/fine?days=5"

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.route('/fine', methods=['GET'])
def fine():
    """
    Calculate DuckFine fee based on query parameters.
    
    Query Parameters:
    - days: Number of days late (required, must be non-negative integer)
    - deluxe: Whether the duck is deluxe (optional, 1 for true, 0 for false)
    
    Returns:
    - JSON with the calculated fee
    - 400 error if days is invalid
    """
    days_param = request.args.get('days')
    deluxe_param = request.args.get('deluxe', '0')
    
    # Validate days parameter
    if days_param is None:
        return jsonify({"error": "Missing required parameter: days"}), 400
    
    try:
        days = int(days_param)
    except ValueError:
        return jsonify({"error": "days must be a valid integer"}), 400
    
    if days < 0:
        return jsonify({"error": "days must not be negative"}), 400
    
    # Parse deluxe parameter
    deluxe = deluxe_param == '1'
    
    # Calculate the fine
    duck_fine = DuckFine(member_id="api_user")
    fee = duck_fine.charge(days_late=days, deluxe=deluxe)
    
    return jsonify({"fee": fee})


if __name__ == '__main__':
    app.run(debug=True)
