from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event, _constants
from crealand._utils import _logger_setup, _utils
from typing import Callable as _Callable

_logger = _logger_setup.setup_logger()

# 人脸识别
# 机器学习
# 数字识别

# https://ew9vfg36e3.feishu.cn/docx/NoRsdvGcso1EZKxus7UcVDFfn1f 
# 将用Digit类替换Figure类
class Digit:

    _digit=""
    # 打开手写数字识别教学页面
    @staticmethod
    def open_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openDigitRecognitionTeachingPage", 
            [{"name":""}]
        )

    # 打开神经网络教学页面
    @staticmethod
    def open_NN_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openNeuralNetworkTeachingPage", 
            [{"type":""}]
        )

    # 开始手写数字识别
    @staticmethod
    def start_digit_recognition():
        # 识别返回的结果需要设置保存
        # call_api_async("web-ide","api.digitRecognition",[{"type":"start"}])
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Digit._digit = int(data["data"])
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent("", on_result)

    # 结束手写数字识别
    @staticmethod
    def stop_digit_recognition():
        Digit._digit =""
        _interface.call_api_async(
            "web-ide", 
            "api.digitRecognition", 
            [{"type":"end"}]
        )

    # 数字识别结果
    @staticmethod
    def get_Digit_value():
        return Digit._digit

    # 清除数字识别结果
    @staticmethod
    def clear_Digit_value():
        Digit._digit =""
        _interface.call_api(
            "web-ide", 
            "api.digitRecognitionClear", 
            [{"type":""}]
        )

    @_utils.check_type
    @staticmethod
    def onAIDigitEvent(number: int, cb: _Callable):
        # 识别返回的结果需要设置保存
        number = max(0, min(number, 9))
        # call_api_async("web-ide","api.digitRecognition",[{"type":"start"}])
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Digit._digit = int(data["data"])
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent(number, on_result)


class Figure:

    _digit=""
    # 打开手写数字识别教学页面
    @staticmethod
    def open_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openDigitRecognitionTeachingPage", 
            [{"name":""}]
        )

    # 打开神经网络教学页面
    @staticmethod
    def open_NN_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openNeuralNetworkTeachingPage", 
            [{"type":""}]
        )

    # 开始手写数字识别
    @staticmethod
    def start_digital_recognition():
        # 识别返回的结果需要设置保存
        # call_api_async("web-ide","api.digitRecognition",[{"type":"start"}])
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Figure._digit = int(data["data"])
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent("", on_result)

    # 结束手写数字识别
    @staticmethod
    def stop_digital_recognition():
        Figure._digit =""
        _interface.call_api_async(
            "web-ide", 
            "api.digitRecognition", 
            [{"type":"end"}]
        )

    # 数字识别结果
    @staticmethod
    def get_figure_value():
        return Figure._digit

    # 清除数字识别结果
    @staticmethod
    def clear_figure_value():
        Figure._digit =""
        _interface.call_api(
            "web-ide", 
            "api.digitRecognitionClear", 
            [{"type":""}]
        )

    @_utils.check_type
    @staticmethod
    def onAIFigureEvent(number: int, cb: _Callable):
        # 识别返回的结果需要设置保存
        number = max(0, min(number, 9))
        # call_api_async("web-ide","api.digitRecognition",[{"type":"start"}])
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Figure._digit = int(data["data"])
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent(number, on_result)


# 手势识别
class Gesture:
    _direction=""
    # 开始手势识别 并等待结束
    @staticmethod
    def start_gesture_recognition():
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Gesture._direction = data["data"]
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIGestureEvent("", on_result)

    # 结束手势识别
    @staticmethod
    def stop_gesture_recognition():
        Gesture._direction=""
        _interface.call_api_async(
            "web-ide", 
            "api.gestureRecognition", 
            [{"type":"end"}]
        )

    # 当前手势识别结果为
    @staticmethod
    def get_gesture_value():
        return Gesture._direction

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIGestureEvent(direction:str,cb:_Callable):
        _utils.check_out_of_range("onAIGestureEvent", "direction", 
            direction, _constants.Direction)
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Gesture._direction = data["data"]
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIGestureEvent(direction, on_result)

# https://ew9vfg36e3.feishu.cn/docx/NoRsdvGcso1EZKxus7UcVDFfn1f 
# 将用Speech类替换Voice类


# 语音识别
class Speech:
    _text=""
    # 开始语音识别
    @staticmethod
    def start_speech_recognition():
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Speech._text = data["data"]
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent("", on_result)


    # 结束识别
    @staticmethod
    def stop_speech_recognition():
        Speech._text =""
        _interface.call_api(
            "web-ide", 
            "api.openVoiceRecognition", 
            [{"type":"end"}]
        )

    # 语音识别结果
    @staticmethod
    def get_speech_value():
        return Speech._text


    # 打开语音识别教学页面
    @staticmethod
    def open_speech_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openVoiceRecognitionTeachingPage", 
            [{"name":""}]
        )

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIAsrEvent(text: str, cb: _Callable):
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Speech._text = data["data"]
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent(text, on_result)


# 语音识别
class Voice:
    _text=""
    # 开始语音识别
    @staticmethod
    def start_voice_recognition():
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Voice._text = data["data"]
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent("", on_result)


    # 结束识别
    @staticmethod
    def stop_voice_recognition():
        Voice._text =""
        _interface.call_api(
            "web-ide", 
            "api.openVoiceRecognition", 
            [{"type":"end"}]
        )

    # 语音识别结果
    @staticmethod
    def get_voice_value():
        return Voice._text


    # 打开语音识别教学页面
    @staticmethod
    def open_voice_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openVoiceRecognitionTeachingPage", 
            [{"name":""}]
        )

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIAsrEvent(text: str, cb: _Callable):
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Voice._text = data["data"]
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent(text, on_result)


# 人脸识别
class Face:
    _face_data = {
        "lib_id": "",
        "name": "无匹配结果",
        "mood": "",
        "gender": "",
        "match_percent": 0
    }

    @_utils.check_type
    @staticmethod
    def choose_face_library(id: str):
        Face._face_data["lib_id"] = id

    @_utils.check_type
    @staticmethod
    def add_face(id: str):
        Face._face_data["lib_id"] = id
        _interface.call_api(
            "web-ide", 
            "api.addFaceToFaceLibrary", 
            [{"id": id}]
        )

    @staticmethod
    def start_face_recognition():
        result=_interface.call_api(
            "web-ide", 
            "api.selectedFaceLibrary", 
            [{"id": Face._face_data["lib_id"]}]
        )
        if result:
            data_list = result.rstrip(',').split(",")
            data_list = [item.strip("' ") for item in data_list]
            Face._face_data["mood"] = data_list[0] if data_list[0] else ""
            Face._face_data["gender"] = data_list[1] if data_list[1] else ""
            Face._face_data["match_percent"] = \
                float(data_list[2]) if data_list[2] else 0
            Face._face_data["name"] = \
                data_list[3] if data_list[3] else "无匹配结果"

    @staticmethod
    def open_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openFaceRecognitionTeachingPage", 
            [{"name": ""}]
        )

    @staticmethod
    def get_name():
        return Face._face_data["name"]

    @staticmethod
    def get_mood():
        return _constants.MOOD_MAP.get(Face._face_data["mood"])
    
    @staticmethod
    def get_gender():
        return _constants.GENDER_MAP.get(Face._face_data["gender"])

    @staticmethod
    def get_match_percent():
        return Face._face_data["match_percent"]

class Model:

    @_utils.check_type
    @staticmethod
    def get_predict_result(id: str):
        return _interface.call_api(
            "web-ide", 
            "api.modelPredictionResult", 
            [{"modelId": id}]
        )

    @_utils.check_type
    @staticmethod
    def get_confidence_result(id: str, value: str):
        return _interface.call_api(
            "web-ide", 
            "api.modelPredictionResult", 
            [{"modelId": id, "modelValue": value}]
        )

    @staticmethod
    def open_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openDecisionTreeTeachingPage", 
            [{"name": ""}]
        )


class AIGC:
    _agent={}
    @_utils.check_type
    @staticmethod
    def bind_to_object(agent_id: str, runtime_id: int):
        runtime_id = max(0, runtime_id)
        AIGC._agent[runtime_id] = {'agent_id':agent_id,'conversationId':None}

    @_utils.check_type
    @staticmethod
    def start_dialogue(runtime_id: int, name: str):
        runtime_id = max(0, runtime_id)

        if runtime_id not in AIGC._agent:
            raise KeyError(f"runtime_id {runtime_id} has not been bound to an agent")

        agent_id = AIGC._agent.get(runtime_id).get('agent_id')
        conversationId=AIGC._agent.get(runtime_id).get('conversationId') if AIGC._agent.get(runtime_id).get('conversationId') else ""
        reuslt=_interface.call_api(
            "web-ide", 
            "api.openDialogWithAgent", 
            [{
                "objId": runtime_id, 
                "name": name, 
                "agentId": agent_id, 
                "conversationId": conversationId
            }]
        )
        if reuslt:
            AIGC._agent[runtime_id]['conversationId'] = reuslt