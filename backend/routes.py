from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for item in data:
        if item.get("id") == id:  
            return jsonify(item), 200 
    
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    rec_data = request.get_json()
    new_id = rec_data.get('id')
    
    # Check for existing picture with the same ID
    if any(pic['id'] == new_id for pic in data):
        return jsonify({"Message": f"picture with id {new_id} already present"}), 302
    
    data.append(rec_data)
    return jsonify(rec_data), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_pic = request.get_json()
    for i, item in enumerate(data):
        if item["id"] == id:
            data[i].update(update_pic)
            return item, 201
    
    return {"message": "no such picture"}, 404
        

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for item in data:
        if item.get("id") == id: 
            data.remove(item) 
            return "", 204

    return {"message": "no such picture"}, 404