import re
from src.utils.logger import Logger
from typing import Tuple


class VersionExchanger:
    def __init__(self, client_version: str):
        self.logger = Logger.get_logger(__name__)
        self.client_version = client_version
        self.server_version = None
        self.supported_versions = ["^2.0"]  # 지원하는 SSH 버전 목록

    def get_client_version_string(self) -> str:
        """클라이언트 버전 문자열을 반환합니다."""
        return f"{self.client_version}\r\n"

    def parse_server_version(self, version_string: str) -> Tuple[bool, str]:
        """
        서버 버전 문자열을 파싱하고 유효성을 검사합니다.

        :param version_string: 서버로부터 받은 버전 문자열
        :return: (유효성 여부, 파싱된 버전 또는 에러 메시지)
        """
        # 개행 문자 제거
        version_string = version_string.strip()

        # 정규표현식을 사용하여 버전 문자열 파싱
        match = re.match(r"SSH-(\d+\.\d+)-.*", version_string)
        if not match:
            return False, "Invalid version string format"

        version = match.group(1)
        if version not in self.supported_versions:
            return False, f"Unsupported SSH version: {version}"

        self.server_version = version_string
        return True, version

    def exchange_versions(self, socket_handler) -> bool:
        """
        서버와 버전을 교환합니다.

        :param socket_handler: 소켓 통신을 위한 핸들러 객체
        :return: 버전 교환 성공 여부
        """
        try:
            # 클라이언트 버전 전송
            socket_handler.send(self.get_client_version_string().encode())

            # 서버 버전 수신
            server_version_string = socket_handler.receive().decode()

            # 서버 버전 파싱 및 검증
            is_valid, result = self.parse_server_version(server_version_string)
            if not is_valid:
                print(f"Version exchange failed: {result}")
                return False

            print(f"Version exchange successful. Server version: {self.server_version}")
            return True

        except Exception as e:
            print(f"Error during version exchange: {str(e)}")
            return False

    def get_negotiated_version(self) -> str:
        """협상된 SSH 버전을 반환합니다."""
        if self.server_version:
            return self.supported_versions[0]  # 현재는 항상 2.0을 반환
        return None
