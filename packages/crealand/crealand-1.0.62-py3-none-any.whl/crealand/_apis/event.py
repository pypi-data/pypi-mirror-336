import time as _time
from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event, _constants
from crealand._utils import _utils
from typing import Callable as _Callable

#收到广播事件
@_utils.check_type
def onBroadcastEvent(info: str, cb: _Callable):
    _subscribe_event.onBroadcastEvent(info,cb)

#发送广播事件
@_utils.check_type
def send_broadcast(info: str):
    _subscribe_event.sendBroadcast(info)

#对象进入/离开判定区域事件
@_utils.check_type
def onAreaObjectEvent(
    runtime_id: int, 
    action: int, 
    area_id: int, 
    cb: _Callable
):
    _utils.check_out_of_range("onAreaObjectEvent", "action", 
                              action, _constants.ActionType)
    runtime_id = max(0, runtime_id)
    area_id = max(0, area_id)
    def cb_wrapper(err, data):
        if err is None:
            cb()
        else:
            _utils.raise_error("onAreaObjectEvent", err, data)
    _subscribe_event.onAreaObjectEvent(runtime_id, action, 
        area_id, cb_wrapper)

#分类进入/离开判定区域事件
@_utils.check_type
def onAreaClassEvent(
    config_id: str, 
    action: int, 
    area_id: int, 
    cb: _Callable
):
    _utils.check_out_of_range("onAreaClassEvent", "action", 
        action, _constants.ActionType)
    area_id = max(0, area_id)
    def cb_wrapper(err, data):
        if err is None:
            cb()
        else:
            _utils.raise_error("onAreaClassEvent", err, data)
    _subscribe_event.onAreaClassEvent(config_id, action, 
        area_id, cb_wrapper)

# 验证按键是否按下
@_utils.check_type
def keypress_state(button: int):
    _utils.check_out_of_range("keypress_state", "button", 
        button, _constants.KeyType)
    _time.sleep(_constants.SLEEP_TIME)
    return _interface.call_api(
        "unity", 
        "unity.input.verifyKeyCodeState", 
        [button, _constants.KeyPress.KEY_PRESS]
    )

# 鼠标键盘事件
@_utils.check_type
def onKeyEvent(action: int, button: int, cb: _Callable):
    _utils.check_out_of_range("onKeyEvent", "action", 
        action, _constants.KeyActiveType)
    _utils.check_out_of_range("onKeyEvent", "button", 
        button, _constants.KeyType)
    def cb_wrapper(err, data):
        if err is None:
            cb()
        else:
            _utils.raise_error("onKeyEvent", err, data)
    _subscribe_event.onKeyEvent(action, button, cb_wrapper)
