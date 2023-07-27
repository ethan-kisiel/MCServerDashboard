from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class StartServerForm(FlaskForm):
    submit_route = "/start-server"
    start_server_btn = SubmitField("Start Server")


class StopServerForm(FlaskForm):
    submit_route = "/stop-server"
    stop_server_btn = SubmitField("Stop Server")


class RestartServerForm(FlaskForm):
    submit_route = "/restart-server"
    restart_server_btn = SubmitField("Restart Server")


class SendCommandForm(FlaskForm):
    submit_route = "/send-command"
    command_field = StringField(
        "Command", render_kw={"placeholder": "Enter a terminal command..."}
    )
    send_command_btn = SubmitField("Send")


class UpdateServerForm(FlaskForm):
    submit_route = "/update-server"
    update_server_btn = SubmitField("Update Server")
