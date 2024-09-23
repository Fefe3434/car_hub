import app.api_main as api_main


api = api_main.get_global_api()

if __name__ == "__main__":
    # Please do not set debug=True in production
    api.run(host='0.0.0.0', port=5000)
