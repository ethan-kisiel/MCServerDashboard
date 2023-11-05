from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import ValidationError
from werkzeug.utils import secure_filename


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


class ChangeLevelForm(FlaskForm):
    submit_route = "/"
    save_level_btn = SubmitField("Save")
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