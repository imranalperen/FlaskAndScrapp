from flask import (
    Blueprint,
    render_template
)
from .utils import (
    all_activities
)


activity = Blueprint("activity", __name__, url_prefix="/activity")


@activity.route("/main")
def main():
    activities = all_activities()
    return render_template("activity/activity.html",
                            activities=activities)


