from flask import Flask, request, make_response
from urllib import parse
import json
from datetime import datetime
import base64
import slackbot_module.slackbot_api as slackAPI
import slackbot_module.slackbot_info as slackInfo
from google_calendar_module.google_calendar_api import calendarAPI
from google_calendar_module.google_calendar_block_builder import block_builder
from google_calendar_module.google_calendar_modal_builder import modal_builder
from google_calendar_module.google_calendar_apphome import apphome

app = Flask(__name__)


@app.route("/interaction", methods=["POST"])
def interactivity_controll():
    # Slack이 Content-Type이 x-from-included-data인 request를 보냄
    # request가 url encoded 되어 있기 때문에 url decoding 실행
    url_encoded_data = request.get_data(as_text=True)
    request_body = json.loads(parse.unquote(url_encoded_data).split("payload=")[-1])

    print(json_prettier(request_body))

    # 핸들링에 필요한 액션 처리
    (action_service, action_type) = get_action_info(request_body=request_body)

    handling_func = ACTION_DICT[action_service][action_type]
    if handling_func == None:
        return "this action have no function", 200

    return handling_func(request_body, action_type)


def get_action_info(request_body):
    action = request_body.get("actions")

    # modal submit 일 때
    if action == None:
        callback_id = request_body["view"]["callback_id"].split("-")
        action_service = callback_id[0]
        action_type = callback_id[1]
        return (action_service, action_type)

    # 그 이외 action 일 때
    action_id = action[0].get("action_id").split("-")
    action_service = action_id[0]
    action_type = action_id[1]

    return (action_service, action_type)


# Get을 쓰면 없는거 불러올 때 오류는 안난다
# 각 액션에 대한 response value를 가져옴
def get_value_from_action(action_dict):
    action_type_dict = {
        "timepicker": ["selected_time"],
        "datepicker": ["selected_date"],
        "static_select": ["selected_option", "text", "text"],
        "users_select": ["selected_user"],
        "plain_text_input": ["value"],
        "checkboxes": ["selected_options"],
    }

    keys = action_type_dict[action_dict["type"]]

    # selected_option, text, text
    value = get_dictionary_value_for_depth(
        keys=keys, dictionary=action_dict, current_depth=0
    )

    return value


def get_dictionary_value_for_depth(keys, dictionary, current_depth):
    current_dictionary = dictionary[keys[current_depth]]

    if current_depth == len(keys) - 1:
        return current_dictionary

    return get_dictionary_value_for_depth(keys, current_dictionary, current_depth + 1)


def get_user_name(user_id):
    return slackInfo.get_user_info(user_id, "real_name")


def event_modal_submit(request_body, action_type):
    view = UTFToKoreanJSON(request_body["view"])
    view_id = view["id"]

    data = dict()

    for block in view["state"]["values"].values():
        for action_id, action_dict in block.items():
            data[action_id] = get_value_from_action(action_dict)

    request = make_google_calendar_api_event_insert_request(data=data)

    # 캘린더에 업데이트
    calendarAPI.insert_event(event_request=request)

    # 슬랙에 전송
    slackAPI.modal_update(
        view=modal_builder.get_base_view(None, ""),
        view_id=view_id,
        response_action="clear",
    )

    modal_builder.after_submit(view["private_metadata"])

    return "ok", 200


def allday_changed(request_body, action_name):
    # +기호 이슈로 인한 디코딩 코드 추가
    view = UTFToKoreanJSON(request_body["view"])
    view_id = view["id"]

    occured_action = request_body["actions"][0]
    action_id = occured_action["action_id"]
    block_id = occured_action["block_id"]

    selected_checkbox = view["state"]["values"][block_id][action_id]["selected_options"]

    # 선택된 체크박스의 갯수가 1개 이상이면 all-day
    all_day = True if len(selected_checkbox) > 0 else False

    updated_view = modal_builder.update_event_insert_modal(
        original_view=view, all_day=all_day
    )

    print("Updated: ", json_prettier(updated_view))
    slackAPI.modal_update(view=updated_view, view_id=view_id, response_action="update")

    return "ok", 200


def vacation_modal_submit(request_body, action_type):
    # +기호 이슈로 인한 디코딩 코드 추가
    view = UTFToKoreanJSON(request_body["view"])
    view_id = view["id"]

    data = dict()

    for block in view["state"]["values"].values():
        for action_id, action_dict in block.items():
            data[action_id] = get_value_from_action(action_dict)

    request = make_google_calendar_api_vacation_insert_request(data=data)

    # 캘린더에 업데이트
    calendarAPI.insert_event(event_request=request)

    # 슬랙에 전송
    slackAPI.modal_update(
        view=modal_builder.get_base_view(None, ""),
        view_id=view_id,
        response_action="clear",
    )

    return "ok", 200


def make_google_calendar_api_event_insert_request(data):
    request = dict()

    print("DATA:", data)

    # google_calendar api 표준 : Dict {summary, start, end, all-day}
    start_time = data.get("update_calendar-modal_event_start_time")
    end_time = data.get("update_calendar-modal_event_end_time")
    date = data.get("update_calendar-modal_event_date")

    summary = data.get("update_calendar-modal_event_summary")
    description = data.get("update_calendar-modal_event_description")
    all_day = True if len(data.get("update_calendar-modal_event_allday")) > 0 else False

    # 2023-01-09
    # 연차일 경우는 date, 이외는 dateTime
    (start, end) = (
        (
            datetime.strptime(date, "%Y-%m-%d"),
            datetime.strptime(date, "%Y-%m-%d"),
        )
        if all_day
        else (
            datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M"),
            datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M"),
        )
    )

    # 최용태 - 연차
    request["summary"] = summary
    request["start"] = start
    request["end"] = end
    request["description"] = description
    request["all-day"] = all_day

    return request


def make_google_calendar_api_vacation_insert_request(data):
    request = dict()

    # google_calendar api 표준 : Dict {summary, start, end, all-day}
    start_time = data.get("update_calendar-modal_vacation_start_time")
    end_time = data.get("update_calendar-modal_vacation_end_time")
    start_date = data.get("update_calendar-modal_vacation_start_date")
    end_date = data.get("update_calendar-modal_vacation_end_date")

    vacation_type = data["update_calendar-modal_vacation_type_select"]

    # 2023-01-09
    # 연차일 경우는 date, 이외는 dateTime
    (start, end) = (
        (
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d"),
        )
        if vacation_type == "연차"
        else (
            datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M"),
            datetime.strptime(f"{start_date} {end_time}", "%Y-%m-%d %H:%M"),
        )
    )

    # 최용태 - 연차
    request["summary"] = (
        get_user_name(data["update_calendar-modal_vacation_member_select"])
        + "-"
        + vacation_specify(
            vacation_type=data["update_calendar-modal_vacation_type_select"],
            start=start,
        )
    )

    request["start"] = start
    request["end"] = end
    request["description"] = None  # 사용하지 않음
    request["all-day"] = True if vacation_type == "연차" else False

    return request


def vacation_specify(vacation_type, start: datetime):
    AM_START = 9
    PM_START = 12

    result = vacation_type

    if vacation_type == "반차":
        prefix = "오전 " if start.hour < 12 else "오후 "
        result = prefix + result

    return result


def vacation_type_selected(request_body, action_name):
    # +기호 이슈로 인한 디코딩 코드 추가
    view = UTFToKoreanJSON(request_body["view"])
    view_id = view["id"]

    occured_action = request_body["actions"][0]
    action_id = occured_action["action_id"]
    block_id = occured_action["block_id"]

    selected_option = view["state"]["values"][block_id][action_id]["selected_option"]

    vacation_type = selected_option["value"]

    updated_view = modal_builder.update_vacation_insert_modal(
        orginal_view=view, vacation_type=vacation_type
    )

    slackAPI.modal_update(view=updated_view, view_id=view_id, response_action="update")

    return "ok", 200


def modal_open(request_body, action_name):
    # Required Argument
    trigger_id = request_body["trigger_id"]
    user_id = request_body["user"]["id"]
    modal_type = action_name.split("_")[-1]  # "modal_open_vacation" -> vacation

    modal_view = modal_builder.get_modal(modal_name=f"{modal_type}", creator_id=user_id)
    slackAPI.modal_open(view=modal_view, trigger_id=trigger_id)

    return "ok", 200


def calendar_refresh(request_body, action_name):
    # Required Argument
    user_id = request_body["user"]["id"]

    apphome.refresh_app_home(user_id=user_id)

    return "ok", 200


def UTFToKorean(text):
    return text.encode("UTF-8").decode("UTF-8").replace("+", " ")


def UTFToKoreanJSON(data):
    converted_data = json.dumps(data).replace("+", " ")
    return json.loads(converted_data)


def json_prettier(data):
    return json.dumps(data, indent=4, separators=(",", ":"), sort_keys=True)


ACTION_DICT = {
    "read_calendar": {
        "refresh": calendar_refresh,
        "today_vacation": None,
        "today_event": None,
    },
    "update_calendar": {
        "modal_open_vacation": modal_open,
        "modal_open_event": modal_open,
        "modal_vacation_member_select": None,
        "modal_vacation_start_time": None,
        "modal_vacation_end_time": None,
        "modal_vacation_start_date": None,
        "modal_vacation_end_date": None,
        "modal_vacation_type_select": vacation_type_selected,
        "modal_vacation_submit": vacation_modal_submit,
        "modal_event_summary": None,
        "modal_event_date": None,
        "modal_event_start_time": None,
        "modal_event_end_time": None,
        "modal_event_description": None,
        "modal_event_allday": allday_changed,
        "modal_event_submit": event_modal_submit,
    },
}


# # 현재 쓰고있지 않음
# def calendar_message_handling(action_type, channel_id):
#     action_func_dict = {
#         "today_vacation": calendarAPI.get_vacation_list,
#         "today_event": calendarAPI.get_common_event_list,
#     }

#     event_list = action_func_dict[action_type](option="today")

#     blocks = block_builder.make_block_list(
#         event_list=event_list, action_type=action_type, day_option="today"
#     )
#     return slackAPI.post_message(channel_id, f"read_calendar-{action_type}", blocks)


# 알림
# 무엇을 알림?
# 슬랙의 특정 사용자에 대한 일정을 알림!
# 애매해서 우선 순위를 뒤로 두자
# @app.route('/calendar/alert')
