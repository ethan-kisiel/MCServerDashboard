from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, SelectField, FileField, PasswordField
from wtforms.validators import ValidationError
from werkzeug.utils import secure_filename


class LoginForm(FlaskForm):
    password_field = PasswordField(
        "Password",
        render_kw={"class": "form-control", "placeholder": "Enter the passcode..."},
    )
    password_submit_btn = SubmitField("Enter", render_kw={"class": "form-control"})


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


class ClearWeatherForm(FlaskForm):
    submit_route = "/clear-weather"
    update_server_btn = SubmitField("Clear Weather")


class SetDayForm(FlaskForm):
    submit_route = "/set-day"
    update_server_btn = SubmitField("Set Day")


class ChangeLevelForm(FlaskForm):
    submit_route = "/"
    save_level_btn = SubmitField("Change Level")
    selected_level_field = SelectField(
        "Choose an option", choices=[("default", "default")]
    )


def allowed_file_extension(form, field):
    if field.data:
        filename = secure_filename(field.data.filename)
        if not filename.lower().endswith(".zip"):
            raise ValidationError("Only .zip files are allowed!")


class LevelUploadForm(FlaskForm):
    zip_file_field = FileField(
        "Select a .zip file",
        validators=[allowed_file_extension],
    )
    file_upload_btn = SubmitField("Upload")


class KickUserForm(FlaskForm):
    submit_route = "/kick"

    player_name = StringField(render_kw={"hidden": "true"})

    kick_reason = StringField(
        "Kick Reason",
        render_kw={"placeholder": "Enter a reason for kicking this player..."},
    )

    submit_btn = SubmitField("Kick User")
