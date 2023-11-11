import os
from secrets import token_urlsafe
from flask import Flask, render_template, redirect, jsonify, request
from forms import *
from threading import Thread
from websocket_server import SocketServer

from utils.serverutils import ServerManager
from utils.config_reader import load_config

load_config("dashboard-config")

server_manager = ServerManager()

app = Flask(__name__)
app.secret_key = token_urlsafe(16)

is_application_debug = True if os.environ.get("DEBUG") == "True" else False
websocket_address = os.environ.get("WEBSOCKET_ADDRESS")
websocket_port = os.environ.get("WEBSOCKET_PORT")

WEBSOCKET_LOCAL_ADDRESS = "127.0.0.1" if is_application_debug else "0.0.0.0"
WEBSOCKET_PUBLIC_ADDRESS = (
    websocket_address if websocket_address is not None else "127.0.0.1"
)
WEBSOCKET_PORT = websocket_port if websocket_port is not None else 6942

WEBSOCKET_CONNECTION_STRING = f"ws://{WEBSOCKET_PUBLIC_ADDRESS}:{WEBSOCKET_PORT}/"

socket_server = SocketServer(
    WEBSOCKET_LOCAL_ADDRESS, int(WEBSOCKET_PORT), server_manager
)
socket_thread = Thread(target=socket_server.run)
socket_thread.daemon = True
socket_thread.start()


@app.route("/")
def index():
    server_manager.apply_properties()
    start_server_form = StartServerForm()
    stop_server_form = StopServerForm()
    restart_server_form = RestartServerForm()

    send_command_form = SendCommandForm()
    update_server_form = UpdateServerForm()
    level_upload_form = LevelUploadForm()
    kick_user_form = KickUserForm()

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
        "kick_user_form": kick_user_form,
    }

    if is_application_debug:
        server_manager.connected_players = [
            "joe",
            "bob",
            "jordan",
            "ligma",
            "bophades",
            "ZyggyK",
            "deezus",
        ]

    return render_template(
        "index.html",
        forms=forms,
        server_manager=server_manager,
        websocket_server=WEBSOCKET_CONNECTION_STRING,
    )


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
    if server_manager.is_server_busy or server_manager.is_server_running:
        return redirect("/")

    thread = Thread(target=server_manager.start_server)
    thread.start()

    return redirect("/")


@app.route("/stop-server", methods=["POST"])
def stop_server():
    if server_manager.is_server_busy or not server_manager.is_server_running:
        return redirect("/")
    thread = Thread(target=server_manager.stop_server)
    thread.start()
    # server_manager.stop_server()
    return redirect("/")


@app.route("/restart-server", methods=["POST"])
def restart_server():
    if server_manager.is_server_busy:
        return redirect("/")
    thread = Thread(target=server_manager.restart_server)
    thread.start()

    return redirect("/")


@app.route("/update-server", methods=["POST"])
def update_server():
    if server_manager.is_server_busy:
        return redirect("/")
    thread = Thread(target=server_manager.update_server)
    thread.start()
    # server_manager.update_server()

    return redirect("/")


@app.route("/send-command", methods=["POST"])
def send_command():
    form = SendCommandForm()

    if server_manager.is_server_busy or not server_manager.is_server_running:
        return redirect("/")
    if form.validate_on_submit():
        thread = Thread(
            target=server_manager.term_manager.send, args=(form.command_field.data,)
        )
        thread.start()

        # server_manager.term_manager.send(form.command_field.data)

    return redirect("/")


@app.route("/change-level", methods=["POST"])
def change_level():
    levels = server_manager.get_levels()
    current = server_manager.get_current_level()
    form = ChangeLevelForm()
    form.selected_level_field.choices = [(level, level) for level in levels]

    if server_manager.is_server_busy:
        return redirect("/")
    if form.validate_on_submit():
        thread = Thread(
            target=server_manager.set_level, args=(form.selected_level_field.data,)
        )
        thread.start()

        # server_manager.set_level(form.selected_level_field.data)
    return redirect("/")


@app.route("/upload-level", methods=["POST"])
def upload_level():
    form = LevelUploadForm()
    if server_manager.is_server_busy:
        return redirect("/")

    file = request.files["file"]
    filename = secure_filename(file.filename)
    save_path = os.path.join("temp/", filename)

    current_chunk = int(request.form["dzchunkindex"])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        # return make_response(("File already exists", 400))
        return redirect("/")

    try:
        with open(save_path, "ab") as f:
            f.seek(int(request.form["dzchunkbyteoffset"]))
            f.write(file.stream.read())
    except OSError:
        # log.exception will include the traceback so we can see what's wrong
        # log.exception('Could not write to file')
        # return make_response(("Not sure why,"
        #                     " but we couldn't write the file to disk", 500))
        return redirect("/")

    total_chunks = int(request.form["dztotalchunkcount"])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
            # log.error(
            #     f"File {file.filename} was completed, "
            #     f"but has a size mismatch."
            #     f"Was {os.path.getsize(save_path)} but we"
            #     f" expected {request.form['dztotalfilesize']} "
            # )
            # return make_response(("Size mismatch", 500))
            return redirect("/")
        else:
            # log.info(f"File {file.filename} has been uploaded successfully")
            thread = Thread(target=server_manager.upload_level, args=(filename,))
            thread.start()
    else:
        # log.debug(
        #     f"Chunk {current_chunk + 1} of {total_chunks} "
        #     f"for file {file.filename} complete"
        # )
        pass

    # if form.validate_on_submit():
    #     try:
    #         file = form.zip_file_field.data
    #         filename = secure_filename(file.filename)
    #         file.save(f"temp/{filename}")
    #         thread = Thread(target=server_manager.upload_level, args=(file, filename))
    #         thread.start()

    # server_manager.upload_level(file, filename)

    # except Exception as e:
    #     print(e)
    ## make call to function here to save the world
    return redirect("/")


@app.route("/kick", methods=["POST"])
def kick():
    form = KickUserForm()

    if form.validate_on_submit():
        command = f"kick {form.player_name.data} {form.kick_reason.data}"
        thread = Thread(target=server_manager.term_manager.send, args=(command,))
        thread.start()

    return redirect("/")


# try:
#     server_manager = ServerManager()
#     server_manager.install_server()
# except:
#     print("Failed to download/unzip file")
