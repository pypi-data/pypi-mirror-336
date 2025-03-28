import requests
from elasticsearch_dsl.query import Query
from km_sdk.api_provider import ApiProvider, UserDto, PermissionDto, FileDto
from km_sdk.utils.log_utils import LogUtils

sync_logger = LogUtils.get_logger()


class InterfaceApi(ApiProvider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_file_url = kwargs.get("list_file_url")
        self.get_file_url = kwargs.get('get_file_url')

        self.list_file_permission_url = kwargs.get('list_file_permission_url')
        self.list_user_file_permission_url = kwargs.get('list_user_file_permission_url')

        self.get_user_url = kwargs.get('get_user_url')
        self.download_url = kwargs.get('download_url')

        self.request_params = kwargs.get('request_params')

    def get_files(self, page_size=20, current=1) -> [FileDto]:
        res = requests.get(self.list_file_url.format(page_size, current), **self.request_params)
        return res.json()

    def get_file(self, file_id: str) -> FileDto:
        return requests.post(self.get_file_url.format(file_id), **self.request_params).json()

    def download(self, file_id: str) -> bytes:
        return requests.get(self.download_url.format(file_id), **self.request_params).content

    def list_file_permission(self, file_id: str) -> [PermissionDto]:
        return requests.get(self.list_file_permission_url.format(file_id), **self.request_params)

    def list_user_file_permission(self, user_id: str, file_ids: [str]) -> [str]:
        return requests.post(self.list_user_file_permission_url.format(user_id, '["' + ('","'.join(file_ids)) + '"]'),
                             **self.request_params).json()

    def get_user(self, user_id: str) -> UserDto:
        return requests.get(self.get_user_url.format(user_id), **self.request_params).json()

    def build_filter(self, user_id: str, related_sync_system: str, bqry: Query) -> Query:
        return bqry

    def system_init(self):
        pass


    @staticmethod
    def get_description() -> dict:
        return {
            "name": "通用api接口",
            "type": "INTERFACE",
            "params": [
                {
                    "name": "list_file_url",
                    "key": "list_file_url",
                    "remark": "获取文件列表的网址",
                    "required": True,
                    "type": "input",
                    "rules": [{"type": "url"}]
                },
                {
                    "name": "get_file_url",
                    "key": "get_file_url",
                    "remark": "获取单个文件的网址",
                    "required": True,
                    "type": "input",
                    "rules": [{"type": "url"}]
                },
                {
                    "name": "list_file_permission_url",
                    "key": "list_file_permission_url",
                    "remark": "获取文件权限的网址",
                    "required": True,
                    "type": "input",
                    "rules": [{"type": "url"}]
                },
                {
                    "name": "list_user_file_permission_url",
                    "key": "list_user_file_permission_url",
                    "remark": "获取用户文件权限的网址",
                    "required": True,
                    "type": "input",
                    "rules": [{"type": "url"}]
                },
                {
                    "name": "get_user_url",
                    "key": "get_user_url",
                    "remark": "获取用户信息的网址",
                    "required": True,
                    "type": "input",
                    "rules": [{"type": "url"}]
                },
                {
                    "name": "download_url",
                    "key": "download_url",
                    "remark": "下载文件的网址",
                    "required": True,
                    "type": "input",
                    "rules": [{"type": "url"}]
                },
                {
                    "name": "request_params",
                    "key": "request_params",
                    "remark": "请求参数,json格式",
                    "required": False,
                    "type": "input"
                }
            ]
        }