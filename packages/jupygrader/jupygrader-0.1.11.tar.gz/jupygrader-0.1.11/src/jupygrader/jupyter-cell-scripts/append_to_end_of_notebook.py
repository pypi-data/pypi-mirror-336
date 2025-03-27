# Jupygrader After File Code
# REMOVE_IN_HTML_OUTPUT
import json
import datetime
from jupygrader.constants import GRADED_RESULT_JSON_FILENAME

grading_end_time = datetime.datetime.now(datetime.timezone.utc)

_graded_result.grading_finished_at = grading_end_time.strftime("%Y-%m-%d %I:%M %p %Z")
_graded_result.grading_duration_in_seconds = round(
    (grading_end_time - grading_start_time).total_seconds(), 2
)
_graded_result.num_total_test_cases = len(_graded_result.test_case_results)

for test_case_result in _graded_result.test_case_results:
    _graded_result.learner_autograded_score += test_case_result.points
    _graded_result.max_total_score += test_case_result.available_points

    if test_case_result.grade_manually:
        _graded_result.max_manually_graded_score += test_case_result.available_points
        _graded_result.num_manually_graded_cases += 1
    else:
        _graded_result.max_autograded_score += test_case_result.available_points
        _graded_result.num_autograded_cases += 1

        if test_case_result.did_pass:
            _graded_result.num_passed_cases += 1
        else:
            _graded_result.num_failed_cases += 1

with open(GRADED_RESULT_JSON_FILENAME, "w") as fp:
    json.dump(_graded_result.to_dict(), fp, indent=2)
