from crealand._core.bridge import _interface
from crealand._apis import _constants
from crealand._utils import _utils
from typing import (
    List as _List, 
    Union as _Union, 
    Literal as _Literal
)

# 信息
class Info:

    # 别名对象id
    @_utils.check_type
    @staticmethod
    def get_alias_id(nickname: str):
        return _interface.call_api(
            "unity", 
            "unity.alias.getByAlias", 
            [nickname]
        )

    # 获取configID的对象id
    @_utils.check_type
    @staticmethod
    def get_object_id(runtime_id: int) -> int:
        runtime_id = max(0, runtime_id)
        return _interface.call_api(
            "unity",
            "unity.actor.getConfigID",
            [runtime_id]
        )

    # 获取对象的空间坐标
    @_utils.check_type
    @staticmethod
    def get_object_coordinates(runtime_id: int):
        runtime_id = max(0, runtime_id)
        return _interface.call_api(
            "unity", 
            "unity.actor.getCoordinate", 
            [runtime_id]
        )

    # 获取判定区域中的对象id
    @_utils.check_type
    @staticmethod
    def get_id_in_area(area_id: int, config_ids: _List[str]):
        area_id = max(0, area_id)
        return _interface.call_api(
            "unity",
            "unity.editableTrigger.getContentRuntimeIds",
            [area_id, config_ids]
        )

    # 获取空间坐标某个轴的值
    @_utils.check_type
    @staticmethod
    def get_spatial_coordinates(
        coordinate: _List[_Union[int, float]], 
        axis: _Literal["X", "Y", "Z"]="X"
    ):
        _utils.check_three_dimensions("get_spatial_coordinates", "coordinate", 
            coordinate)
        AXIS = {"X": 0, "Y": 1, "Z": 2}
        return coordinate[AXIS[axis]]

    # 获取对象的运动方向向量
    @_utils.check_type
    @staticmethod
    def get_motion_vector(runtime_id: int):
        runtime_id = max(0, runtime_id)
        return _interface.call_api(
            "unity", 
            "unity.character.getMoveDirection", 
            [runtime_id]
        )


class Camera:
    default_id = ""

    # 获取相机ID
    @staticmethod
    def get_default_id():
        Camera.default_id = _interface.call_api(
            "unity", 
            "unity.camera.getDefaultID", 
            []
        )
        return Camera.default_id

    # 获取空间坐标
    @_utils.check_type
    @staticmethod
    def get_object_coordinates(runtime_id: int):
        runtime_id = max(0, runtime_id)
        return _interface.call_api(
            "unity", 
            "unity.actor.getCoordinate", 
            [runtime_id]
        )

    # 相机移动
    @_utils.check_type
    @staticmethod
    def move_to(
        time: _Union[int, float], 
        coordinate: _List[_Union[int, float]], 
        block: bool=False
    ):
        time = max(0, time)
        _utils.check_three_dimensions("move_to", "coordinate", coordinate)
        _interface.call_api(
            "unity",
            "unity.camera.moveTo",
            [Camera.default_id, time, coordinate, block]
        )

    # 调整FOV
    @_utils.check_type
    @staticmethod
    def adjust_FOV(time: _Union[int, float]=1, fov: _Union[int, float]=80):
        time = max(0, time)
        fov = max(60, min(fov, 120))
        _interface.call_api_async(
            "unity",
            "unity.camera.adjustFOV",
            [Camera.default_id, time, fov]
        )

    # 相机锁定朝向并移动
    @_utils.check_type
    @staticmethod
    def move_while_looking(
        coordinate_1: _List[_Union[int, float]],
        time: _Union[int,float]=1,
        coordinate_2: _List[_Union[int, float]]=[0, 0, 1],
        block: bool=False
    ):
        _utils.check_three_dimensions("move_while_looking", "coordinate_1", 
            coordinate_1)
        time = max(0, time)
        _utils.check_three_dimensions("move_while_looking", "coordinate_2", 
            coordinate_2)
        _interface.call_api_async(
            "unity",
            "unity.camera.moveWhileLooking",
            [Camera.default_id, time, coordinate_2, coordinate_1, block]
        )

    # 获取相机坐标
    @staticmethod
    def get_camera_coordinate() -> _List[_Union[int, float]]:
        result = Camera.get_object_coordinates(Camera.default_id)
        return result

    # 相机朝向
    @_utils.check_type
    @staticmethod
    def look_at(coordinate: _List[_Union[int, float]]):
        _utils.check_three_dimensions("look_at", "coordinate", coordinate)
        _interface.call_api_async(
            "unity",
            "unity.camera.lookAt",
            [Camera.default_id, coordinate]
        )

    # 相机跟随
    @_utils.check_type
    @staticmethod
    def follow_target(
        runtime_id: int, 
        distance: _Union[int, float]=10, 
        is_rotate: bool=True
    ):
        runtime_id = max(0, runtime_id)
        _interface.call_api_async(
            "unity",
            "unity.camera.followTarget",
            [Camera.default_id, runtime_id, distance, is_rotate]
        )

    # 相机结束跟随
    @staticmethod
    def end_follow_target():
        _interface.call_api_async(
            "unity",
            "unity.camera.stopFollowing",
            [Camera.default_id]
        )

    # 相机 滤镜
    @_utils.check_type
    @staticmethod
    def filters(filter_name: int=_constants.FilterStyle.FOG, state: bool=True):
        _utils.check_out_of_range("filters", "filter_name", 
            filter_name, _constants.FilterStyle)
        _interface.call_api_async(
            "unity",
            "unity.camera.openEffect",
            [Camera.default_id, filter_name, state]
        )


class Motion:
    # 创建对象
    @_utils.check_type
    @staticmethod
    def create_object_coordinate(
        config_id: str, 
        coordinate: _List[_Union[int,float]]=[0, 0, 1]
    ):
        _utils.check_three_dimensions("create_object_coordinate", "coordinate", coordinate)
        return _interface.call_api(
            "unity",
            "unity.actor.createObject",
            [config_id, coordinate]
        )

    # 测距
    @_utils.check_type
    @staticmethod
    def ray_ranging(
        runtime_id: int, 
        attachment_id: tuple=(_constants.HangPointType.LEFT_FRONT_WHEEL,)
    ):
        runtime_id = max(0, runtime_id)
        _utils.check_attachment_id("ray_ranging", "attachment_id", 
            attachment_id)
        _utils.check_out_of_range("ray_ranging", "attachment_id", 
            attachment_id[0], _constants.HangPointType)
        return _interface.call_api(
            "unity",
            "unity.actor.rayRanging",
            [runtime_id, _utils.Handle_point(attachment_id), 20]
        )

    # 移动
    @_utils.check_type
    @staticmethod
    def move_to(
        runtime_id: int, 
        coordinate: _List[_Union[int, float]]=[0, 0, 1]
    ):
        runtime_id = max(0, runtime_id)
        _utils.check_three_dimensions("move_to", "coordinate", coordinate)
        _interface.call_api(
            "unity",
            "unity.actor.setObjectPosition",
            [runtime_id, coordinate]
        )

    # 朝向
    @_utils.check_type
    @staticmethod
    def face_towards(
        runtime_id: int, 
        coordinate: _List[_Union[int, float]]=[0, 0, 1]
    ):
        runtime_id = max(0, runtime_id)
        _utils.check_three_dimensions("face_towards", "coordinate", coordinate)
        _interface.call_api(
            "unity",
            "unity.actor.setObjectTowardPosition",
            [runtime_id, coordinate]
        )

    # 前进
    @_utils.check_type
    @staticmethod
    def move_forward(
        runtime_id: int, 
        speed: int=1, 
        distance: _Union[int, float]=3, 
        block: bool=False
    ):
        runtime_id = max(0, runtime_id)
        speed = max(1, min(speed, 5))
        _interface.call_api(
            "unity",
            "unity.actor.moveForwardByDistance",
            [runtime_id, distance, abs(distance / speed), block]
        )

    # 对象旋转
    @_utils.check_type
    @staticmethod
    def rotate(
        runtime_id: int, 
        time: _Union[int, float]=1, 
        angle: _Union[int, float]=90, 
        block: bool=False
    ):
        runtime_id = max(0, runtime_id)
        time = max(time, 0)
        _interface.call_api(
            "unity",
            "unity.character.rotateUpAxisByAngle",
            [runtime_id, angle, time, block]
        )

    # 云台旋转 & 机械臂旋转
    @_utils.check_type
    @staticmethod
    def ptz(runtime_id: int, angle: _Union[int, float]=90, block: bool=False):
        runtime_id = max(0, runtime_id)
        _interface.call_api(
            "unity",
            "unity.actor.rotatePTZUpAxisByAngle",
            [runtime_id, angle, abs(angle) / 30, block]
        )

    # 播放动作
    @_utils.check_type
    @staticmethod
    def action(runtime_id: int, action: str, block: bool=False):
        runtime_id = max(0, runtime_id)
        _interface.call_api(
            "unity",
            "unity.actor.playAnimation",
            [runtime_id, action, block]
        )

    # # 将对象吸附到挂点
    @_utils.check_type
    @staticmethod
    def attach_to(
        absorbed_runtime_id: int, 
        absorb_runtime_id: int, 
        attachment_id: tuple
    ):
        absorbed_runtime_id = max(0, absorbed_runtime_id)
        absorb_runtime_id = max(0, absorb_runtime_id)
        _utils.check_attachment_id("attach_to", "attachment_id", 
            attachment_id)
        _utils.check_out_of_range("attach_to", "attachment_id", 
            attachment_id[0], _constants.HangPointType)
        _interface.call_api(
            "unity",
            "unity.actor.attach",
            [
                absorbed_runtime_id, 
                absorb_runtime_id, 
                _utils.Handle_point(attachment_id)
            ]
        )

    # 绑定挂点
    @_utils.check_type
    @staticmethod
    def bind_to_object_point(
        runtime_id_1: int,
        attachment_id_1: tuple, 
        runtime_id_2: int,
        attachment_id_2: tuple
    ):
        runtime_id_1 = max(0, runtime_id_1)
        _utils.check_attachment_id("bind_to_object_point", "attachment_id_1", 
            attachment_id_1)
        _utils.check_out_of_range("bind_to_object_point", "attachment_id_1", 
            attachment_id_1[0], _constants.HangPointType)
        runtime_id_2 = max(0, runtime_id_2)
        _utils.check_attachment_id("bind_to_object_point", "attachment_id_2", 
            attachment_id_2)
        _utils.check_out_of_range("bind_to_object_point", "attachment_id_2", 
            attachment_id_2[0], _constants.HangPointType)
        _interface.call_api(
            "unity",
            "unity.actor.bindAnchor",
            [
                runtime_id_1, 
                _utils.Handle_point(attachment_id_1), 
                runtime_id_2, 
                _utils.Handle_point(attachment_id_2)
            ]
        )

    # 解除绑定
    @_utils.check_type
    @staticmethod
    def detach(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api(
            "unity",
            "unity.actor.detach",
            [runtime_id]
        )

    # 新的解除绑定接口，详情请查看
    # https://ew9vfg36e3.feishu.cn/docx/NoRsdvGcso1EZKxus7UcVDFfn1f
    @_utils.check_type
    @staticmethod
    def unbind(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api(
            "unity",
            "unity.actor.detach",
            [runtime_id]
        )

    # 向画面空间前进
    @_utils.check_type
    @staticmethod
    def move_towards_screen_space(
        runtime_id: int, 
        speed: int=1, 
        direction: _List[_Union[int, float]]=[0, 0, 1]
    ):
        runtime_id = max(0, runtime_id)
        speed = max(1, min(speed, 5))
        _utils.check_three_dimensions("move_towards_screen_space", "direction", 
            direction)
        _interface.call_api(
            "unity",
            "unity.actor.moveByVelocity",
            [runtime_id, 2, speed, direction]
        )

    @_utils.check_type
    @staticmethod
    def get_motion_vector(runtime_id: int):
        runtime_id = max(0, runtime_id)
        return _interface.call_api(
            "unity", 
            "unity.character.getMoveDirection", 
            [runtime_id]
        )

    # 旋转运动方向向量
    @_utils.check_type
    @staticmethod
    def rotate_to_direction(
        runtime_id: int, 
        angle: _Union[int, float]=0, 
        direction: _List[_Union[int, float]]=[0, 0, 1]
    ):
        runtime_id = max(0, runtime_id)
        _utils.check_three_dimensions("rotate_to_direction", "direction", 
            direction)
        _interface.call_api(
            "unity",
            "unity.character.rotateUpAxisByDirection",
            [runtime_id, angle, direction, 0]
        )

    # 停止运动
    @_utils.check_type
    @staticmethod
    def stop(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api_async(
            "unity",
            "unity.character.stop",
            [runtime_id]
        )

    # 设置别名
    @_utils.check_type
    @staticmethod
    def create_object(
        config_id: str,
        nickname: str,
        coordinate: _List[_Union[int, float]]=[0, 0, 1],
    ):
        _utils.check_three_dimensions("create_object", "coordinate", coordinate)
        _interface.call_api_async(
            "unity",
            "unity.alias.setAlias",
            [
                nickname,
                Motion.create_object_coordinate(config_id, coordinate)
            ]
        )

    # 销毁对象
    @_utils.check_type
    @staticmethod
    def destroy(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api_async(
            "unity",
            "unity.alias.destoryObject",
            [runtime_id]
        )

    # 上升
    @_utils.check_type
    @staticmethod
    def rise(
        runtime_id: int, 
        speed: int=3, 
        height: _Union[int, float]=10, 
        block: bool=False
    ):
        runtime_id = max(0, runtime_id)
        speed = max(1, min(speed, 5))
        _interface.call_api(
            "unity",
            "unity.character.moveUpByDistance",
            [runtime_id, height, abs(height/speed), block]
        )
    # 降落
    @_utils.check_type
    @staticmethod
    def landing(runtime_id: int):
        runtime_id = max(0, runtime_id)
        _interface.call_api(
            "unity",
            "unity.character.land",
            [runtime_id, 3]
        )

    # 获取离自身距离的坐标
    @_utils.check_type
    @staticmethod
    def get_object_local_position(
        runtime_id: int, 
        coordinate: _List[_Union[int, float]]=[0, 0, 1], 
        distance: _Union[int,float]=0
    ):
        runtime_id = max(0, runtime_id)
        _utils.check_three_dimensions("get_object_local_position", "coordinate", coordinate)
        return _interface.call_api(
            "unity",
            "unity.actor.getObjectLocalPosition",
            [runtime_id, coordinate, distance]
        )

    # 移动到指定坐标
    @_utils.check_type
    @staticmethod
    def move_by_point(
        runtime_id: int, 
        time: _Union[int,float]=1, 
        coordinate: _List[_Union[int, float]]=[0, 0, 1], 
        block: bool=False
    ):
        runtime_id = max(runtime_id, 0)
        time = max(time, 0)
        _utils.check_three_dimensions("move_by_point", "coordinate", coordinate)
        _interface.call_api(
            "unity",
            "unity.actor.moveByPoint",
            [runtime_id, time, coordinate, block]
        )

    # 绕坐标轴旋转
    @_utils.check_type
    @staticmethod
    def rotate_by_origin_and_axis(
        runtime_id: int,
        time: _Union[int,float]=2,
        point_1: int=_constants.AxisType.LOCAL,
        coordinate_1: _List[_Union[int, float]]=[0, 0, 0],
        point_2: int=_constants.AxisType.LOCAL,
        coordinate_2: _List[_Union[int, float]]=[0, 0, 1],
        angle: _Union[int,float]=90,
        block: bool=False
    ):
        runtime_id = max(runtime_id, 0)
        time = max(time, 0)
        _utils.check_out_of_range("rotate_by_origin_and_axis", "point_1", 
            point_1, _constants.AxisType)
        _utils.check_three_dimensions("rotate_by_origin_and_axis", "coordinate_1", 
            coordinate_1)
        _utils.check_out_of_range("rotate_by_origin_and_axis", "point_2", 
            point_2, _constants.AxisType)
        _utils.check_three_dimensions("rotate_by_origin_and_axis", "coordinate_2", 
            coordinate_2)
        _interface.call_api(
            "unity",
            "unity.actor.rotateByOringinAndAxis",
            [
                runtime_id,
                coordinate_1,
                point_1,
                coordinate_2,
                point_2,
                angle,
                time,
                block 
            ]
        )


class Property:
    # 新增自定义属性
    @_utils.check_type
    @staticmethod
    def add_attr(runtime_id: int, attr_name: str, attr_value: str):
        runtime_id = max(runtime_id, 0)
        _interface.call_api(
            "unity",
            "unity.actor.addCustomProp",
            [runtime_id, attr_name, attr_value]
        )

    # 新增自定义属性 --crealand-1.13.2新增
    @_utils.check_type
    @staticmethod
    def add_prop(runtime_id: int, prop_name: str, prop_value: str):
        runtime_id = max(runtime_id, 0)
        _interface.call_api(
            "unity",
            "unity.actor.addCustomProp",
            [runtime_id, prop_name, prop_value]
        )

    # 删除自定义属性
    @_utils.check_type
    @staticmethod
    def del_attr(runtime_id: int, attr_name: str):
        runtime_id = max(runtime_id, 0)
        _interface.call_api(
            "unity",
            "unity.actor.delCustomProp",
            [runtime_id, attr_name]
        )
    # 删除自定义属性--crealand-1.13.2新增
    @_utils.check_type
    @staticmethod
    def del_prop(runtime_id: int, prop_name: str):
        runtime_id = max(runtime_id, 0)
        _interface.call_api(
            "unity",
            "unity.actor.delCustomProp",
            [runtime_id, prop_name]
        )
    # 修改自定义属性
    @_utils.check_type
    @staticmethod
    def set_attr(runtime_id: int, attr_name: str, attr_value: str):
        runtime_id = max(runtime_id, 0)
        _interface.call_api(
            "unity",
            "unity.actor.setCustomProp",
            [runtime_id, attr_name, attr_value]
        )
    # 修改自定义属性--crealand-1.13.2新增
    @_utils.check_type
    @staticmethod
    def set_prop(runtime_id: int, prop_name: str, prop_value: str):
        runtime_id = max(runtime_id, 0)
        _interface.call_api(
            "unity",
            "unity.actor.setCustomProp",
            [runtime_id, prop_name, prop_value]
        )

    # 获取自定义属性的值
    @_utils.check_type
    @staticmethod
    def get_value(runtime_id: int, prop_name: str):
        runtime_id = max(runtime_id, 0)
        return _interface.call_api(
            "unity",
            "unity.actor.getCustomProp",
            [runtime_id, prop_name]
        )

    # 获取自定义属性组中某一项的值
    @_utils.check_type
    @staticmethod
    def get_value_by_idx(runtime_id: int, index: int=1):
        runtime_id = max(runtime_id, 0)
        return _interface.call_api(
            "unity",
            "unity.actor.getCustomPropValueByIdx",
            [runtime_id, index]
        )

    # 获取自定义属性组中某一项的名称
    @_utils.check_type
    @staticmethod
    def get_key_by_idx(runtime_id: int, index: int=1):
        runtime_id = max(runtime_id, 0)
        return _interface.call_api(
            "unity",
            "unity.actor.getCustomPropKeyByIdx",
            [runtime_id, index]
        )


class Show:
    # 3d文本-RGB
    @_utils.check_type
    @staticmethod
    def set_3D_text_status_rgb(
        runtime_id: int, 
        rgb: _List[int] = [255, 255, 255], 
        size: int = 30, 
        text: str = "文本"
    ):
        runtime_id = max(runtime_id, 0)
        _utils.check_three_dimensions("set_3D_text_status_rgb", "rgb", rgb)
        for i in range(3):
            rgb[i] = max(0, min(255, rgb[i]))

        size = max(0, min(30, size))
        _interface.call_api(
            "unity",
            "unity.building.set3DTextStatus",
            [runtime_id, rgb, size, text]
        )
