from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    # Running on port 5000
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
