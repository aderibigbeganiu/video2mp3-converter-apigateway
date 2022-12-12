import json
import os
import gridfs
import pika
from auth import validate
from auth_svc import access
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from storage import util
from bson import ObjectId

server = Flask(__name__)

mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")
fs_videos = gridfs.GridFS(mongo_video.db)

mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def uplaod():
    access, err = validate.token(request)
    access = json.loads(access)

    if err:
        return err

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file required", 400

        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access)

            if err:
                return err
        return "Success!", 200
    else:
        return "not authorize", 401


@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)
    access = json.loads(access)

    if err:
        return err

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "Fid is required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "Internal server error", 500

    return "not authorize", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
