# LOG表示関連をまとめたヘッダーファイル
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    ' %(module)s -  %(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)