import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import ffmpeg

logger = logging.getLogger(__name__)
# discord.pyのログ出力フォーマットを再現
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 時間フォーマット
TIME_FORMAT: str = "%H:%M:%S"

# エラーログフォーマット
LOG_FORMAT: str = "エラーが発生しました。"


@dataclass
class InputArgs:
    """入力パラメータ"""

    file_path: str
    video_time: str
    leave_time_from: str
    leave_time_to: str


def m2ts_to_mp4(input_args: InputArgs) -> None:
    """時間を指定して録画ファイルから動画をmp4に変換して切り抜く

    Parameters
    ----------
    input_args : InputArgs
        file_path: str
            ファイルパス
        video_time: str
            動画の尺
        leave_time_from: str
            切り抜き開始時間
        leave_time_to: str
            切り抜き終了時間
    """
    msg = f"[処理開始] {m2ts_to_mp4.__name__}"
    logger.info(msg)
    # 切り抜き開始時間と切り抜き所要時間を作成
    try:
        # 切り抜き開始時間
        start_time = datetime.strptime(  # noqa: DTZ007
            input_args.video_time, TIME_FORMAT
        ) - datetime.strptime(input_args.leave_time_from, TIME_FORMAT)  # noqa: DTZ007

        # 切り抜き所要時間
        delta_time = datetime.strptime(  # noqa: DTZ007
            input_args.leave_time_from, TIME_FORMAT
        ) - datetime.strptime(input_args.leave_time_to, TIME_FORMAT)  # noqa: DTZ007
    except ValueError as e:
        msg = f"{LOG_FORMAT} {e}"
        logger.info(msg)
        return

    input_path = Path(input_args.file_path)
    output_path = Path("output", input_path.stem + ".mp4")

    input_options = {
        "ss": start_time,
    }
    output_options = {
        "t": delta_time,
        "vf": "yadif",
        "vcodec": "h264_videotoolbox",
        "video_bitrate": "12M",
        "acodec": "aac",
    }

    stream = ffmpeg.input(str(input_path), **input_options)
    stream = ffmpeg.output(stream, str(output_path), **output_options)

    try:
        ffmpeg.run(stream)

    except ffmpeg._run.Error as e:  # noqa: SLF001
        msg = f"{LOG_FORMAT} {e}"
        logger.info(msg)

    finally:
        msg = f"[処理終了] {m2ts_to_mp4.__name__}"
        logger.info(msg)


if __name__ == "__main__":
    args = sys.argv

    input_args = InputArgs(args[1], args[2], args[3], args[4])
    m2ts_to_mp4(input_args)
