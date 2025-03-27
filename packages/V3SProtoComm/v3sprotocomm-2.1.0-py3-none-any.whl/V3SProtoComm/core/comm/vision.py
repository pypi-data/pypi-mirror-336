import logging
import socket
import struct

import json
import numpy as np

from V3SProtoComm.core.comm.receiver import Receiver
from V3SProtoComm.core.comm.protocols import packet_pb2, wrapper_pb2
from V3SProtoComm.core.data import FieldData, EntityData
from V3SProtoComm.core.comm.thread_job import Job
from google.protobuf.json_format import MessageToDict


class ProtoVision(Receiver):
    def __init__(self, team_color_yellow: bool,
                 field_data: FieldData = None,
                 vision_ip='224.5.23.2', vision_port=10015):
        super(ProtoVision, self).__init__(vision_ip, vision_port)

        self.team_color_yellow = team_color_yellow
        self.field_data = field_data

    def receive(self):
        data = super().receive()
        return data

    def receive_dict(self):

        data = self.receive()

        if self.receiver_ip == '224.0.0.1':
            try:
                env_msg = packet_pb2.Environment().FromString(data)
                env_dict = MessageToDict(env_msg.frame)
                logging.debug("Pacote decodificado como SIMULADOR (Environment)")
                return {"type": "simulator", "data": env_dict}
            except Exception as e:
                logging.warning(f"Falha ao decodificar como Environment: {e}")
                return None

        elif self.receiver_ip == '224.5.23.2':
            try:
                ssl_msg = wrapper_pb2.SSL_WrapperPacket().FromString(data)
                ssl_dict = MessageToDict(ssl_msg)
                logging.debug("Pacote decodificado como VISÃO (SSL_WrapperPacket)")
                return {"type": "vision", "data": ssl_dict}
            except Exception as e:
                logging.warning(f"Falha ao decodificar como SSL_WrapperPacket: {e}")
                return None

        else:
            logging.warning(f"IP não reconhecido: {self.receiver_ip}")
            return None

    def receive_field_data(self) -> FieldData:
        """
        Caso queira um FieldData 'novo' a cada chamada, sem sobrescrever o self.field_data.
        """
        data_dict = self.receive_dict()

        rcv_field_data = FieldData()
        if data_dict is None:
            return rcv_field_data  

        if data_dict["type"] == "simulator":
            self._field_data_from_dict(rcv_field_data, data_dict["data"])
        elif data_dict["type"] == "vision":
            self._field_data_from_vision_dict(rcv_field_data, data_dict["data"])

        return rcv_field_data

    def update(self):
        """
        Atualiza self.field_data usando o que chegar (simulador OU visão).
        """
        if self.field_data is None:
            logging.error('FieldData not instantiated', exc_info=True)
            return

        data_dict = self.receive_dict()
        if data_dict is None:
            return

        if data_dict["type"] == "simulator":
            self._field_data_from_dict(self.field_data, data_dict["data"])
        elif data_dict["type"] == "vision":
            self._field_data_from_vision_dict(self.field_data, data_dict["data"])


    def _field_data_from_dict(self, field_data: FieldData, raw_data_dict):

        if self.team_color_yellow:
            team_list_of_dicts = raw_data_dict.get('robotsYellow', [])
            foes_list_of_dicts = raw_data_dict.get('robotsBlue', [])
            rotate_field = True
        else:
            team_list_of_dicts = raw_data_dict.get('robotsBlue', [])
            foes_list_of_dicts = raw_data_dict.get('robotsYellow', [])
            rotate_field = False

        if 'ball' in raw_data_dict:
            self._entity_from_dict(field_data.ball, raw_data_dict['ball'], rotate_field)

        for i in range(len(team_list_of_dicts)):
            self._entity_from_dict(field_data.robots[i], team_list_of_dicts[i], rotate_field)

        for i in range(len(foes_list_of_dicts)):
            self._entity_from_dict(field_data.foes[i], foes_list_of_dicts[i], rotate_field)


    def _field_data_from_vision_dict(self, field_data: FieldData, raw_data_dict):
        """
        Recebe um dicionário que vem do SSL_WrapperPacket (convertido para JSON).
        Ajusta para puxar 'balls', 'robotsYellow', 'robotsBlue', etc.
        """

        if self.team_color_yellow:
            robot_key = "robotsYellow"
            foe_key = "robotsBlue"
            rotate_field = True
        else:
            robot_key = "robotsBlue"
            foe_key = "robotsYellow"
            rotate_field = False

        if "balls" in raw_data_dict and len(raw_data_dict["balls"]) > 0:
            ball_info = raw_data_dict["balls"][0]
            self._entity_from_dict(field_data.ball, ball_info, rotate_field)

        if robot_key in raw_data_dict:
            for i, robot_data in enumerate(raw_data_dict[robot_key]):
                self._entity_from_dict(field_data.robots[i], robot_data, rotate_field)

        if foe_key in raw_data_dict:
            for i, foe_data in enumerate(raw_data_dict[foe_key]):
                self._entity_from_dict(field_data.foes[i], foe_data, rotate_field)


    def _entity_from_dict(self, entity_data: EntityData, data_dict, rotate_field=False):
        multiplier = 1 if not rotate_field else -1
        sum_to_angle = 0 if not rotate_field else np.pi

        x = data_dict.get('x', 0)
        y = data_dict.get('y', 0)
        orientation = data_dict.get('orientation', 0)
        vx = data_dict.get('vx', 0)
        vy = data_dict.get('vy', 0)
        vorientation = data_dict.get('vorientation', 0)

        entity_data.position.x = x * multiplier
        entity_data.position.y = y * multiplier
        entity_data.position.theta = self._assert_angle(orientation + sum_to_angle)
        entity_data.velocity.x = vx * multiplier
        entity_data.velocity.y = vy * multiplier
        entity_data.velocity.theta = vorientation

    def _assert_angle(self, angle):
        angle = angle % (2 * np.pi)
        if angle > np.pi:
            angle -= 2 * np.pi
        return angle


class ProtoVisionThread(Job):
    def __init__(self, team_color_yellow: bool,
                 field_data: FieldData = None,
                 vision_ip='224.0.0.1', vision_port=10015):
        self.vision = ProtoVision(team_color_yellow, field_data, vision_ip, vision_port)
        super(ProtoVisionThread, self).__init__(self.vision.update)


