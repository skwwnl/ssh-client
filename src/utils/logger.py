import logging
import colorlog

# 이전 Code
# class Logger:
#     @staticmethod
#     def get_logger(name):
#         logger = logging.getLogger(name)
#         if not logger.handlers:
#             logger.setLevel(logging.DEBUG)
#             formatter = logging.Formatter(
#                 "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#             )

#             # Console handler
#             ch = logging.StreamHandler()
#             ch.setLevel(logging.INFO)
#             ch.setFormatter(formatter)
#             logger.addHandler(ch)

#             # File handler
#             fh = logging.FileHandler("ssh_client.log")
#             fh.setLevel(logging.DEBUG)
#             fh.setFormatter(formatter)
#             logger.addHandler(fh)

#         return logger


class Logger:
    @staticmethod
    def get_logger(name):
        logger = colorlog.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            # Console handler
            console_handler = colorlog.StreamHandler()
            console_handler.setLevel(logging.INFO)
            color_formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
                secondary_log_colors={},
                style="%",
            )
            console_handler.setFormatter(color_formatter)
            logger.addHandler(console_handler)

            # 파일 핸들러 (색상 없음)
            file_handler = logging.FileHandler("ssh_client.log")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger
