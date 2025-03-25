from crealand._core.bridge import _interface
from crealand._utils import _utils

class Sound:
    # 播放声音
    @_utils.check_type
    @staticmethod
    def play(runtime_id: int, res_id: str,is_loop: bool=False):
        runtime_id = max(0, runtime_id)
        _interface.call_api_async(
            "unity",
            "unity.sound.playSound",
            [runtime_id, is_loop, res_id],
        )

    # 声音
    @staticmethod
    @_utils.check_type
    def adjust_volume(runtime_id: int, volume: int = 50):
        runtime_id = max(0, runtime_id)
        volume = max(0, min(volume, 100))
        _interface.call_api_async(
            "unity",
            "unity.sound.adjustVolume",
            [runtime_id, volume],
        )

    # 停止播放
    @_utils.check_type
    @staticmethod
    def stop(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api_async(
            "unity", 
            "unity.sound.stopSound", 
            [runtime_id]
        )

    # 设置背景音效
    @_utils.check_type
    @staticmethod
    def play_bgm(res_id: str):
        _interface.call_api_async(
            "unity", 
            "unity.sound.playBgSound", 
            [res_id]
        )

    # 背景音效音量
    @_utils.check_type
    @staticmethod
    def adjust_bgm_volume(volume: int = 50):
        volume = max(0, min(volume, 100))
        _interface.call_api_async(
            "unity",
            "unity.sound.adjustBgVolume",
            [volume],
        )

    # 停止背景音效
    @staticmethod
    def stop_bgm():
        _interface.call_api_async(
            "unity",
            "unity.sound.stopBgSound",
            [],
        )


class Video:
    # 播放视频
    @_utils.check_type
    @staticmethod
    def play(res_id: str):
        _interface.call_api(
            "web-ide",
            "api.playVideo",
            [{"pythonOssId":res_id}],
        )


class Image:
    # 播放图片
    @_utils.check_type
    @staticmethod
    def show(res_id: str):
        _interface.call_api(
            "web-ide",
            "api.showImage",
            [{"pythonOssId":res_id}],
        )
