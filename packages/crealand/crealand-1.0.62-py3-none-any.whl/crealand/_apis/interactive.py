from crealand._core.bridge import _interface
from crealand._apis import _constants
from crealand._utils import _utils
from typing import Union as _Union 

class Dialogue:
    # 立绘对话 获取选项
    option_value = ""
    @staticmethod
    def get_option_value():
        return Dialogue.option_value

    # 立绘对话 初始化
    @staticmethod
    def init():
        _interface.call_api(
            "web-ide", 
            "api.prepareDialogBoard", 
            [{}]
        )
        

    # 立绘对话 显示
    @_utils.check_type
    @staticmethod
    def set_dialogue(
        obj_name: str,
        content: str,
        res_id: str="",
        volume: str=_constants.Volume.MEDIUM
    ):
        _utils.check_out_of_range("set_dialogue", "volume", 
            volume, _constants.Volume)
        _interface.call_api(
            "web-ide",
            "api.showDialog",
            [
                {
                    "speaker": obj_name,
                    "type": volume,
                    "txt": content,
                    "voiceId": "",
                    "pythonOssId":res_id,
                }
            ],
        )
    
    @_utils.check_type
    @staticmethod
    def set_dialogue_tone(
        obj_name: str,
        content: str,
        res_id: str="",
        tone: str="",
        volume: str=_constants.Volume.MEDIUM,
    ):
        if tone != "":
            _utils.check_out_of_range("set_dialogue_tone", "tone", 
                tone, _constants.Tone)
        _utils.check_out_of_range("set_dialogue_tone", "volume", 
            volume, _constants.Volume)
        _interface.call_api(
            "web-ide",
            "api.showDialog",
            [
                {
                    "speaker": obj_name,
                    "type": volume,
                    "txt": content,
                    "voiceId": "",
                    "imgId":tone,
                    "pythonOssId":res_id,
                }
            ],
        )

    # 立绘对话 设置选项
    @_utils.check_type
    @staticmethod
    def set_option(
        content: str, 
        opt_name: str=_constants.OptionName.OPTION01
    ):
        _utils.check_out_of_range("set_option", "opt_name", 
            opt_name, _constants.OptionName)
        options = {}
        options[opt_name] = content
        _interface.call_api(
            "web-ide",
            "api.setDialogOptions",
            [{"options": options}],
        )

    # 立绘对话选项 显示
    @_utils.check_type
    @staticmethod
    def set_option_show(is_show: bool=True):
        Dialogue.option_value = _interface.call_api(
            "web-ide", 
            "api.toggleDialogOptions", 
            [{"show": is_show}]
        )
        
    #  立绘对话 显示
    @_utils.check_type
    @staticmethod
    def show(is_show: bool=True):
        if not is_show:
           Dialogue.option_value = ""
            
        _interface.call_api(
            "web-ide", 
            "api.toggleDialogBoard", 
            [{"show": is_show}]
        )


class HelpPanel:
    # 帮助面板 初始化
    @staticmethod
    def init():
        _interface.call_api("web-ide", "api.prepareHelpboard", [{}])

    # 帮助面板 设置标题
    @_utils.check_type
    @staticmethod
    def set_tips(title: str, res_id: str=""):
        _interface.call_api(
            "web-ide",
            "api.addHelpItem",
            [
                {
                    "title": title,
                    "pythonOssId": res_id,
                }
            ],
        )

    # 帮助面板 显示
    @_utils.check_type
    @staticmethod
    def show(is_show: bool=True):
        _interface.call_api(
            "web-ide",
            "api.toggleHelpboard",
            [
                {
                    "show": is_show,
                }
            ],
        )


class TaskPanel:

    # 任务面板 设置标题
    @_utils.check_type
    @staticmethod
    def set_task(title: str, nickname: str):
        _interface.call_api(
            "web-ide",
            "api.createTaskboard",
            [
                {
                    "title": title,
                    "alias": nickname,
                }
            ],
        )

    # 任务面板 设置任务项
    @_utils.check_type
    @staticmethod
    def set_task_progress(
        task_name: str, 
        subtasks_content: str, 
        completed_tasks: int, 
        total_tasks: int
    ):
        total_tasks = max(1, total_tasks)
        completed_tasks = max(0, min(completed_tasks, total_tasks))
        _interface.call_api(
            "web-ide",
            "api.setTaskboard",
            [
                {
                    "alias": task_name,
                    "taskName": subtasks_content,
                    "process": [completed_tasks, total_tasks],
                }
            ],
        )

    # 任务面板 显示
    @_utils.check_type
    @staticmethod
    def set_task_show(task_name: str, is_show: bool=True):
        _interface.call_api(
            "web-ide",
            "api.toggleTaskboard",
            [{"alias": task_name, "show": is_show}],
        )


class Speak:
    # 说
    @_utils.check_type
    @staticmethod
    def text(runtime_id: int, content: str, time: _Union[int, float]=2):
        runtime_id = max(0, runtime_id)
        if time != -1:
            time = max(0, time)
        _interface.call_api_async(
            "unity", 
            "unity.actor.speak", 
            [runtime_id, content, time]
        )

    # 说-img
    @_utils.check_type
    @staticmethod
    def image(runtime_id: int, res_id: str, time: _Union[int, float]=2):
        runtime_id = max(0, runtime_id)
        if time != -1:
            time = max(0, time)
        _interface.call_api_async(
           "unity", 
           "unity.actor.speakImage", 
           [runtime_id, res_id, time]
        )


class Interactive:
    # 提示面板显示
    @_utils.check_type
    @staticmethod
    def set_tip_show(option: str=_constants.ResultType.START):
        _utils.check_out_of_range("set_tip_show", "option", 
            option, _constants.ResultType)
        _interface.call_api(
            "web-ide",
            "api.showTipboardResult",
            [
                {
                    "result": option,
                }
            ],
        )

    # 提示面板显示
    @_utils.check_type
    @staticmethod
    def toast(
        content: str,
        position: str=_constants.ToastPosition.TOP,
        state: str=_constants.ToastState.DYNAMIC,
    ):
        _utils.check_out_of_range("toast", "position", 
            position, _constants.ToastPosition)
        _utils.check_out_of_range("toast", "state", 
            state, _constants.ToastState)
        _interface.call_api_async(
            "web-ide",
            "api.toast",
            [
                {
                    "position": position,
                    "mode": state,
                    "txt": content,
                }
            ],
            
        )

    # 对象显示
    @_utils.check_type
    @staticmethod
    def show_tag(runtime_id: int, content: str, height: int=0):
        runtime_id = max(0, runtime_id)
        height = max(-5, min(height, 30))
        _interface.call_api(
            "unity", 
            "unity.actor.showTextHUD", 
            [runtime_id, content, height]
        )


    @_utils.check_type
    @staticmethod
    def hide_tag(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api(
            "unity", 
            "unity.actor.hideTextHUD", 
            [runtime_id]
        )
