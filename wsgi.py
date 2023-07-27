from secrets import token_urlsafe
from flask import Flask, render_template, redirect, url_for
from forms import *

from utils.serverutils import ServerManager

server_manager = ServerManager()

app = Flask(__name__)
app.secret_key = token_urlsafe(16)


@app.route("/")
def index():
    start_server_form = StartServerForm()
    stop_server_form = StopServerForm()
    restart_server_form = RestartServerForm()

    send_command_form = SendCommandForm()
    update_server_form = UpdateServerForm()

    if server_manager.is_server_running:
        start_server_form.start_server_btn.render_kw = {"disabled": "disabled"}
    else:
        restart_server_form.restart_server_btn.render_kw = {"disabled": "disabled"}
        stop_server_form.stop_server_btn.render_kw = {"disabled": "disabled"}

    forms = {
        "start_form": start_server_form,
        "stop_form": stop_server_form,
        "restart_form": restart_server_form,
        "command_form": send_command_form,
        "update_form": update_server_form,
    }

    return render_template("index.html", forms=forms, server_manager=server_manager)


@app.route("/start-server", methods=["POST"])
def start_server():
    server_manager.start_server()
    return redirect("/")


@app.route("/stop-server", methods=["POST"])
def stop_server():
    server_manager.stop_server()
    return redirect("/")


@app.route("/restart-server", methods=["POST"])
def restart_server():
    server_manager.restart_server()
    return redirect("/")


@app.route("/update-server", methods=["POST"])
def update_server():
    server_manager.update_server()
    return redirect("/")


@app.route("/send-command", methods=["POST"])
def send_command():
    form = SendCommandForm()
    if form.validate_on_submit():
        server_manager.term_manager.send(form.command_field.data)

    return redirect("/")


# try:
#     server_manager = ServerManager()
#     server_manager.install_server()
# except:
#     print("Failed to download/unzip file")
