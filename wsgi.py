import asyncio
import logging
from secrets import token_urlsafe
from flask import Flask, render_template, redirect, url_for, jsonify
from forms import *
from threading import Thread
from websocket_server import SocketServer

from utils.serverutils import ServerManager

server_manager = ServerManager()

app = Flask(__name__)
app.secret_key = token_urlsafe(16)


socket_server = SocketServer("127.0.0.1", 6942, server_manager)
socket_thread = Thread(target=socket_server.run)
socket_thread.start()

thread = Thread(target=server_manager.read_server_output)
thread.start()


@app.route("/")
def index():
    server_manager.apply_properties()
    start_server_form = StartServerForm()
    stop_server_form = StopServerForm()
    restart_server_form = RestartServerForm()

    send_command_form = SendCommandForm()
    update_server_form = UpdateServerForm()
    level_upload_form = LevelUploadForm()

    levels = server_manager.get_levels()
    current = server_manager.get_current_level()

    change_level_form = ChangeLevelForm()
    change_level_form.selected_level_field.choices = [
        (level, level) for level in levels
    ]
    change_level_form.selected_level_field.default = current
    change_level_form.selected_level_field.data = current

    # handle disabling of elements
    if server_manager.is_server_running:
        start_server_form.start_server_btn.render_kw = {"disabled": "disabled"}
    else:
        restart_server_form.restart_server_btn.render_kw = {"disabled": "disabled"}
        stop_server_form.stop_server_btn.render_kw = {"disabled": "disabled"}

    if server_manager.is_server_busy:  # disable all elements if server is busy
        start_server_form.start_server_btn.render_kw = {"disabled": "disabled"}
        restart_server_form.restart_server_btn.render_kw = {"disabled": "disabled"}
        stop_server_form.stop_server_btn.render_kw = {"disabled": "disabled"}
        update_server_form.update_server_btn.render_kw = {"disabled": "disabled"}
        send_command_form.send_command_btn.render_kw = {"disabled": "disabled"}
        change_level_form.save_level_btn.render_kw = {"disabled": "disabled"}
        level_upload_form.file_upload_btn.render_kw = {"disabled": "disabled"}

    forms = {
        "start_form": start_server_form,
        "stop_form": stop_server_form,
        "restart_form": restart_server_form,
        "command_form": send_command_form,
        "update_form": update_server_form,
        "level_form": change_level_form,
        "level_upload_form": level_upload_form,
    }

    return render_template("index.html", forms=forms, server_manager=server_manager)


@app.route("/server-status")
def server_status():
    status_options = ["running", "stopped", "pending"]

    if server_manager.is_server_busy:
        current_status = status_options[2]
    elif server_manager.is_server_running:
        current_status = status_options[0]
    else:
        current_status = status_options[1]

    return jsonify(status=current_status)


@app.route("/connected-players")
def connected_players():
    return jsonify(connected_players=server_manager.connected_players)


@app.route("/start-server", methods=["POST"])
def start_server():
    server_manager.start_server()
    # asyncio.run(socket_server.update_status("Test"))
    # socket_server.update_status()
    return redirect("/")


@app.route("/stop-server", methods=["POST"])
def stop_server():
    thread = Thread(target=server_manager.stop_server)
    thread.start()
    # server_manager.stop_server()
    return redirect("/")


@app.route("/restart-server", methods=["POST"])
def restart_server():
    thread = Thread(target=server_manager.restart_server)
    thread.start()

    return redirect("/")


@app.route("/update-server", methods=["POST"])
def update_server():
    thread = Thread(target=server_manager.update_server)
    thread.start()
    # server_manager.update_server()
    return redirect("/")


@app.route("/send-command", methods=["POST"])
def send_command():
    form = SendCommandForm()
    if form.validate_on_submit():
        server_manager.term_manager.send(form.command_field.data)

    return redirect("/")


@app.route("/change-level", methods=["POST"])
def change_level():
    levels = server_manager.get_levels()
    current = server_manager.get_current_level()
    form = ChangeLevelForm()
    form.selected_level_field.choices = [(level, level) for level in levels]

    if form.validate_on_submit():
        server_manager.set_level(form.selected_level_field.data)

    return redirect("/")


@app.route("/upload-level", methods=["POST"])
def upload_level():
    form = LevelUploadForm()
    if form.validate_on_submit():
        try:
            file = form.zip_file_field.data
            filename = secure_filename(file.filename)
            file.save(f"temp/{filename}")

            server_manager.upload_level(file, filename)

        except Exception as e:
            print(e)
    ## make call to function here to save the world
    return redirect("/")


# try:
#     server_manager = ServerManager()
#     server_manager.install_server()
# except:
#     print("Failed to download/unzip file")
