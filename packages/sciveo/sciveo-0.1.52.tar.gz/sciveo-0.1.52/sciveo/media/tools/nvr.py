#
# Stanislav Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact s.georgiev@softel.bg.
#
# 2025
#

import os
import shutil
import subprocess as sp
import time
import re
import json
import cv2
import datetime

from sciveo.tools.logger import *
from sciveo.tools.daemon import DaemonBase
from sciveo.tools.queue import TouchedFilePathQueue
from sciveo.tools.simple_counter import RunCounter


class VideoCameraCaptureDaemon(DaemonBase):
  def __init__(self, cam_id, url, dst_path, max_video_len=60, transport="tcp"):
    super().__init__()
    self.cam_id = cam_id
    self.url = url
    self.dst_path = dst_path
    self.max_video_len = max_video_len
    self.transport = transport
    self.cmd = [
      "ffmpeg",
      "-rtsp_transport", self.transport,
      "-i", self.url,
      "-c", "copy",
      "-acodec", "aac",
      "-f", "segment",
      "-segment_time", f"{self.max_video_len}",
      "-reset_timestamps", "1",
      "-strftime", "1",
      "-reconnect", "1",
      "-reconnect_at_eof", "1",
      "-reconnect_streamed", "1",
      "-reconnect_delay_max", "5",
      f"{self.dst_path}/{self.cam_id}___%Y-%m-%d___%H-%M-%S.mp4"
    ]

  def clear(self):
    os.system(f"pgrep -f \"{self.url}\" |xargs kill -9")

    files = [f for f in os.listdir(self.dst_path) if os.path.isfile(os.path.join(self.dst_path, f))]
    for file_name in files:
      if file_name.startswith(f"{self.cam_id}___"):
        file_path = os.path.join(self.dst_path, file_name)
        info("RM", file_path)
        os.remove(file_path)

  def loop(self):
    info("start", self.cam_id)
    while(True):
      self.clear()

      p = sp.Popen(self.cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      p.wait()

      self.clear()
      warning(self.cam_id, "streaming interrupted, wait to retry...")
      time.sleep(5)


class VideoRecorder:
  def __init__(self, path_configuration):
    with open(path_configuration, 'r') as fp:
      self.configuration = json.load(fp)
    self.cams = []

    for cam_id, cam_config in self.configuration["cam"].items():
      cam = VideoCameraCaptureDaemon(
        cam_id, cam_config["url"],
        self.configuration["path"]["tmp"],
        self.configuration.get("max_video_len", 60),
        self.configuration.get("transport", "tcp")
      )
      self.cams.append(cam)

    self.queue = TouchedFilePathQueue(self.configuration["path"]["tmp"], period=5, touched_timeout=5)
    self.cleaner_timer = RunCounter(1000, self.clean_old_videos)

  def start(self):
    for cam in self.cams:
      cam.start()

    time.sleep(10)

    while(True):
      try:
        file_name, file_path = self.queue.pop()
        debug("pop", file_name, file_path)
        self.process_file(file_name, file_path)
        self.cleaner_timer.run()
      except Exception as e:
        exception(e)
        time.sleep(1)

  def process_file(self, file_name, file_path):
    split = file_name.split("___")
    if len(split) == 3:
      cam_id = split[0]
      video_date = split[1]
      video_file_name = split[2]
    else:
      warning("wrong file format, removing", file_name, file_path)
      os.remove(file_path)

    match = re.match(r"(\d{2})\-(\d{2})\-(\d{2})\.mp4", video_file_name)
    if not match:
      warning("Invalid filename format")
      video_file_name_split = video_file_name.split(".")
      video_file_name = f"{video_file_name_split[0]}-{video_file_name_split[0]}.{video_file_name_split[1]}"
    else:
      hh, mm, ss = map(int, match.groups())
      start_time = datetime.datetime(2000, 1, 1, hh, mm, ss)
      end_time = start_time + datetime.timedelta(seconds=self.configuration["max_video_len"])
      video_file_name = f"{start_time.strftime('%H.%M.%S')}-{end_time.strftime('%H.%M.%S')}.mp4"

    video_base_path = os.path.join(self.configuration["path"]["video"], cam_id, video_date)
    video_file_path = os.path.join(video_base_path, video_file_name)

    debug("MV", file_path, "=>", video_file_path)
    os.makedirs(video_base_path, exist_ok=True)
    shutil.move(file_path, video_file_path)

  def clean_old_videos(self):
    try:
      days = self.configuration.get("video_retention_period", 7)
      cmd = "find {} -mtime +{} -type f -delete".format(self.configuration["path"]["video"], days)
      debug("cmd", cmd)
      os.system(cmd)
    except Exception as e:
      excprint([self], e, cmd)


if __name__ == '__main__':
  VideoRecorder("./cams.json").start()