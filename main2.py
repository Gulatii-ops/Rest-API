from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")     # / -> home directory
def home():         # Fn that runs in home_dir
    return 'Home'

# http methods:
# GET - request data from a resource/database
# POST - create a resource
# PUT - update a resource
# DELETE - delete a resource

@app.route("/get_user/<user_id>")
def get_user(user_id):
    user_info = {
        "user_id" : user_id,
        "name" : "ABC",
        "email" : "abc@abc.com"
    }

    # The Request, in Flask, is an object that contains all the data sent from the Client to Server.
    # This data can be recovered using the GET/POST Methods. It can be used to retrieve any additional information
    # from the datatbase
    # Test with browser url- <http://127.0.0.1:5000/get_user/123?company=google>
    company = request.args.get("company")
    if company:
        user_info["company_name"] = company

    return jsonify(user_info), 200      # 200 = status code

@app.route("/create_user", methods=['POST'])
def create_user():
    data = request.get_json()

    # confirm user was created
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)