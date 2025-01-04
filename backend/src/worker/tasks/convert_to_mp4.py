from main import app, redis_client
import subprocess
import os
from pathlib import Path
from config import settings
from util import get_result
from datetime import datetime, timezone
import shutil
import ffmpeg
import shlex

CONVERT_TO_MP4_DIR = "convert_to_mp4"
REDIS_KEY_PREFIX = "convert_to_mp4:"

@app.task(name="convert_to_mp4.convert", bind=True)
def convert(self, video_url: str, file_name: str):
    task_id = self.request.id
    output_dir = os.path.join(settings.shared_files_path, CONVERT_TO_MP4_DIR, task_id)
    output_path = os.path.join(output_dir, file_name)

    # task_data = {
    #     "date_start": datetime.now(timezone.utc)
    # }
    # redis_client.hset(REDIS_KEY_PREFIX + task_id, mapping=task_data)

    os.makedirs(output_dir, exist_ok=True)

    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-nostdin", "-i", shlex.quote(video_url), "-c", "copy", "-bsf:a", "aac_adtstoasc", shlex.quote(output_path)],
        check=True,
        timeout=60
    )

    # num_tries = 3

    # for i in range(num_tries):
    #     try:
    #         (
    #             ffmpeg
    #             .input(video_url, timeout=30)
    #             .output(output_path, format='mp4', codec='copy')
    #             .global_args(
    #                 '-reconnect', '1',
    #                 '-reconnect_streamed', '1',
    #                 '-reconnect_delay_max', '5',
    #                 '-rw_timeout', '30000000',
    #                 '-timeout', '300'
    #             )
    #             .run_async(pipe_stdout=True, pipe_stderr=False)
    #         )

    #         break
    #     except ffmpeg.Error as e:
    #         if i + 1 == num_tries:
    #             print("FFmpeg encountered an error!")
    #             print("Stderr Output:")
    #             print(e.stderr.decode())
    #             raise

    # try:
    #     os.makedirs(output_dir, exist_ok=True)

    #     subprocess.run(
    #         ["ffmpeg", "-i", "{}".format(video_url), "-c", "copy", "-bsf:a", "aac_adtstoasc", "{}".format(output_path)],
    #         check=True
    #     )
    # except:
    #     delete_dir(output_dir)

    #     raise

    return output_path

def delete_dir(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


@app.task(name="convert_to_mp4.clean_up_files")
def clean_up_files():
    parent_dir = os.path.join(settings.shared_files_path, CONVERT_TO_MP4_DIR)
    for task_id in os.listdir(parent_dir):
        if os.path.isdir(os.path.join(parent_dir, task_id)):
            result = get_result(task_id)

            if result.failed():
                delete_dir(os.path.join(parent_dir, task_id))

            if result.date_done != None:
                diff_seconds = (datetime.now(timezone.utc) - result.date_done).seconds
                if diff_seconds > 30: # TODO: Make configurable
                    delete_dir(os.path.join(parent_dir, task_id))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, clean_up_files.s()) # TODO: Make seconds configurable