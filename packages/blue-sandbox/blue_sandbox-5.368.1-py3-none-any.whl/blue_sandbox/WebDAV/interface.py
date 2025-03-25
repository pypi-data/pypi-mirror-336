from webdav3.client import Client

from blueness import module

from blue_sandbox import NAME
from blue_sandbox import env
from blue_sandbox.logger import logger

NAME = module.name(__file__, NAME)


# https://chatgpt.com/c/67e06812-4af0-8005-b2ab-5f9a1eabbbe3
class WebDAVInterface:
    def __init__(self):
        config = {
            "webdav_hostname": env.WEBDAV_HOSTNAME,
            "webdav_login": env.WEBDAV_LOGIN,
            "webdav_password": env.WEBDAV_PASSWORD,
        }

        self.client = Client(config)

    def ensure_remote_directory(
        self,
        path: str,
        log: bool = True,
    ) -> bool:
        try:
            if self.client.check(path):
                return True

            self.client.mkdir(path)
        except Exception as e:
            logger.error(e)
            return False

        if log:
            logger.info(
                "{}.ensure_remote_directory: created {}".format(
                    NAME,
                    path,
                )
            )

        return True

    def upload(
        self,
        local_path: str,
        remote_path: str,
        log: bool = True,
    ) -> bool:
        remote_dir = "/".join(remote_path.split("/")[:-1])
        if not self.ensure_remote_directory(
            path=remote_dir,
            log=log,
        ):
            return False

        try:
            self.client.upload_sync(
                remote_path=remote_path,
                local_path=local_path,
            )
        except Exception as e:
            logger.error(e)
            return False

        if log:
            logger.info(
                "{}.upload: {} -> {}".format(
                    NAME,
                    local_path,
                    remote_path,
                )
            )

        return True

    def download(
        self,
        remote_path: str,
        local_path: str,
        log: bool = True,
    ) -> bool:
        try:
            self.client.download_sync(
                remote_path=remote_path,
                local_path=local_path,
            )
        except Exception as e:
            logger.error(e)
            return False

        if log:
            logger.info(
                "{}.download {} -> {}".format(
                    NAME,
                    remote_path,
                    local_path,
                )
            )

        return True
