import time as _time
from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event, _constants
from typing import (
    Callable as _Callable, 
    Union as _Union
)
from crealand._utils import _utils

# 超声波传感器

class Ultrasonic:
    _sensors = {}

    # 前端处理传感器信息绑定
    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: int, attachment_id: tuple) -> None:
        runtime_id = max(0, runtime_id)
        _utils.check_attachment_id("add_sensor", "attachment_id", 
            attachment_id)
        attach=_utils.Handle_point(attachment_id)
        Ultrasonic._sensors[sensor] = (runtime_id, attach)

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> list:
        if sensor in Ultrasonic._sensors:
            return Ultrasonic._sensors[sensor]
        else:
            raise KeyError(f'Sensor "{sensor}" not found')

    @_utils.check_type
    @staticmethod
    def onSensorUltrasonicEvent(
        sensor: str, 
        compare: str, 
        distance: _Union[int, float], 
        cb: _Callable
    ):
        def cb_wrapper(err, data):
            if err is None:
                cb()
            else:
                _utils.raise_error("onSensorUltrasonicEvent", err, data)

        _utils.check_compare_operator("onSensorUltrasonicEvent", 
            "compare", compare)
        sensor_info = Ultrasonic.get_sensor(sensor)
        _subscribe_event.onSensorUltrasonicEvent(sensor_info[0], 
            sensor_info[1], compare, distance, cb_wrapper)

    @_utils.check_type
    @staticmethod
    def get_obstacle_distance(sensor: str) -> _Union[int, float]:
        _time.sleep(_constants.SLEEP_TIME)
        sensor_info = Ultrasonic.get_sensor(sensor) 
        return _interface.call_api(
            "unity", 
            "unity.sensor.ultrasonicRanging", 
            [sensor_info[0], sensor_info[1]]
        )
    

class Auditory:
    _decibel_val=0

    # 获取声音强度
    @staticmethod
    def get_decibel_value():
        return Auditory._decibel_val

    @_utils.check_type
    @staticmethod
    def onSensorSoundEvent(
        compare: str, 
        decibel_value: _Union[int, float], 
        cb: _Callable
    ):
        def cb_wrapper(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Auditory._decibel_val = data["data"]
                    cb()
            else:
                _utils.raise_error("onSensorSoundEvent", err, data)

        _utils.check_compare_operator("onSensorSoundEvent", 
            "compare", compare)
        decibel_value = max(0, min(decibel_value, 150))
        _subscribe_event.onSensorSoundEvent(compare, decibel_value, cb_wrapper)

    # 开始分贝识别
    @staticmethod
    def start_decibel_recognition():
        def cb_wrapper(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Auditory._decibel_val = data["data"]
            else:
                _utils.raise_error("start_decibel_recognition", err, data)

        _subscribe_event.onSensorSoundEvent("==", "", cb_wrapper)

    # 结束分贝识别
    @staticmethod
    def stop_decibel_recognition():
        _interface.call_api_async(
            "web-ide", 
            "api.openDecibelDetectionPage", 
            [{"type":"end"}]
        )


class Visual:
    _sensors = {}

    # 将传感器绑定到对象的挂点
    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: int, attachment_id: tuple):
        runtime_id = max(0, runtime_id)
        _utils.check_attachment_id("add_sensor", "attachment_id", 
            attachment_id)
        attach=_utils.Handle_point(attachment_id)
        Visual._sensors[sensor] = (runtime_id, attach)

    # 获取传感器信息
    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str):
        if sensor in Visual._sensors:
            return Visual._sensors[sensor]
        else:
            raise KeyError(f'Sensor "{sensor}" not found')

    # 打开或关闭传感器画面
    @_utils.check_type
    @staticmethod
    def open_visual_sensor(sensor: str, action_type: bool=True):
        sensor_info=Visual.get_sensor(sensor)
        if action_type:
            _interface.call_api(
                "unity",
                "unity.sensor.openVision",
                [sensor_info[0], sensor_info[1], sensor]
            )
        else:
            _interface.call_api(
                "unity", 
                "unity.sensor.closeVision", 
                [sensor]
            )

class Temperature:
    _sensors = {}

    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: int) -> None:
        runtime_id = max(0, runtime_id)
        Temperature._sensors[sensor] = runtime_id
        _interface.call_api(
            "unity",
            "unity.sensor.attachTemperature",
            [runtime_id]
        )

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> int:
        if sensor in Temperature._sensors:
            return Temperature._sensors[sensor]
        else:
            raise KeyError(f'Sensor "{sensor}" not found')

    @_utils.check_type
    @staticmethod
    def onSensorTemperatureEvent(
        sensor: str, 
        compare: str, 
        temperature: _Union[int, float],
        cb: _Callable
    ):
        def cb_wrapper(err, data):
            if err is None:
                cb()
            else:
                _utils.raise_error("onSensorTemperatureEvent", err, data)

        _utils.check_compare_operator("onSensorTemperatureEvent", 
            "compare", compare)
        temperature = max(-40, min(temperature, 120))
        runtime_id = Temperature.get_sensor(sensor)
        _subscribe_event.onSensorTemperatureEvent(runtime_id,
            compare, temperature, cb_wrapper)
    
    # 设置判定区域温度
    @_utils.check_type
    @staticmethod
    def set_temperature(area_id: int, temp_val: _Union[int, float]=0):
        area_id = max(0, area_id)
        temp_val = max(-40, min(temp_val, 120))
        _interface.call_api(
            "unity", 
            "unity.sensor.setTemperature", 
            [area_id, temp_val]
        )

    # 持续检测判定区域温度
    @_utils.check_type
    @staticmethod
    def startTemperatureDetection(area_id: int):
        area_id = max(0, area_id)
        _subscribe_event.startTemperatureDetection(area_id)

    # 获取温度值
    @_utils.check_type
    @staticmethod
    def get_temperature_value(sensor: str):
        _time.sleep(_constants.SLEEP_TIME)
        runtime_id=Temperature.get_sensor(sensor)
        return _interface.call_api(
            "unity",
            "unity.sensor.getTemperature",
            [runtime_id]
        )


class Humidity:
    _sensors = {}

    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: int) ->None:
        runtime_id = max(0, runtime_id)
        Humidity._sensors[sensor] = runtime_id
        _interface.call_api(
            "unity",
            "unity.sensor.attachHumidity",
            [runtime_id]
        )

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> int:
        if sensor in Humidity._sensors:
            return Humidity._sensors[sensor]
        else:
            raise KeyError(f'Sensor "{sensor}" not found')

    @_utils.check_type
    @staticmethod
    def onSensorHumidityEvent(
        sensor: str, 
        compare: str, 
        humidity_value: _Union[int, float],
        cb: _Callable
    ):
        def cb_wrapper(err, data):
            if err is None:
                cb()
            else:
                _utils.raise_error("onSensorHumidityEvent", err, data)

        _utils.check_compare_operator("onSensorHumidityEvent", 
            "compare", compare)
        humidity_value= max(0, min(humidity_value, 100))
        runtime_id = Humidity.get_sensor(sensor) 
        _subscribe_event.onSensorHumidityEvent(runtime_id, compare,
            humidity_value, cb_wrapper)

    # 设置判定区域湿度
    @_utils.check_type
    @staticmethod
    def set_humidity(area_id: int, humidity_value: _Union[int, float]=0):
        area_id = max(0, area_id)
        humidity_value= max(0, min(humidity_value, 100))
        _interface.call_api(
            "unity",
            "unity.sensor.setHumidity",
            [area_id, humidity_value]
        )

    # 持续检测判定区域湿度
    @_utils.check_type
    @staticmethod
    def startHumidityDetection(area_id: int):
        area_id = max(0, area_id)
        _subscribe_event.startHumidityDetection(area_id)

    @_utils.check_type
    @staticmethod
    def get_humidity_value(sensor: str):
        _time.sleep(_constants.SLEEP_TIME)
        runtime_id=Humidity.get_sensor(sensor)
        return _interface.call_api(
            "unity",
            "unity.sensor.getHumidity",
            [runtime_id]
        )


class Gravity:
    _sensors = {}

    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, area_id: int) -> None:
        area_id = max(0, area_id)
        Gravity._sensors[sensor] = area_id
        _interface.call_api(
            "unity",
            "unity.sensor.attachGravity",
            [area_id]
        )

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> int:
        if sensor in Gravity._sensors:
            return Gravity._sensors[sensor]
        else:
            raise KeyError(f'Sensor "{sensor}" not found')

    @_utils.check_type
    @staticmethod
    def onSensorGravityEvent(
        sensor: str, 
        compare: str, 
        gravity_value: _Union[int, float],
        cb: _Callable
    ):
        def cb_wrapper(err, data):
            if err is None:
                cb()
            else:
                _utils.raise_error("onSensorGravityEvent", err, data)

        _utils.check_compare_operator("onSensorGravityEvent", 
            "compare", compare)
        gravity_value= max(0, min(gravity_value, 10000))
        runtime_id = Gravity.get_sensor(sensor)
        _subscribe_event.onSensorGravityEvent(runtime_id, compare,
            gravity_value, cb_wrapper)

    # 设置对象重力
    @_utils.check_type
    @staticmethod
    def set_gravity(runtime_id: int, gravity_value: _Union[int, float]=0):
        runtime_id = max(0, runtime_id)
        gravity_value= max(0, min(gravity_value, 10000))
        _interface.call_api(
            "unity",
            "unity.sensor.setGravity",
            [runtime_id, gravity_value]
        )

    # 获取重力值
    @_utils.check_type
    @staticmethod
    def get_gravity_value(sensor: str):
        _time.sleep(_constants.SLEEP_TIME)
        runtime_id = Gravity.get_sensor(sensor) 
        return _interface.call_api(
            "unity",
            "unity.sensor.getGravity",
            [runtime_id]
        )

