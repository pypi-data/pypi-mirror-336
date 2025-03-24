#!/usr/bin/env python
#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import os
import time
import json
import argparse

from sciveo.tools.logger import *
from sciveo.tools.configuration import GlobalConfiguration


def main():
  config = GlobalConfiguration.get()

  parser = argparse.ArgumentParser(description='sciveo CLI')
  parser.add_argument(
    'command',
    choices=[
      'init', 'monitor', 'scan', 'nvr', 'predictors-server',
      'media-server', 'media-run',
      'watchdog'
    ],
    help='Command to execute')

  parser.add_argument('--period', type=int, default=120, help='Period in seconds')
  parser.add_argument('--block', type=bool, default=True, help='Block flag')
  parser.add_argument('--auth', type=str, default=config['secret_access_key'], help='Auth secret access key')
  parser.add_argument('--timeout', type=float, default=1.0, help='Timeout')
  parser.add_argument('--net', type=str, default=None, help='Network like 192.168.10.0/24')
  parser.add_argument('--host', type=str, default=None, help='Host ip or name')
  parser.add_argument('--port', type=int, default=22, help='Host port number, used for network ops')
  parser.add_argument('--ports', type=str, default="[]", help='Host ports list')
  parser.add_argument('--localhost', type=bool, default=False, help='Add localhost to list of hosts')
  parser.add_argument('--input-path', type=str, help='Input Path')
  parser.add_argument('--output-path', type=str, default=None, help='Output Path')
  parser.add_argument('--width', type=str, default=None, help='width')
  parser.add_argument('--height', type=str, default=None, help='height')
  parser.add_argument('--rate', type=int, help='Rate number')
  parser.add_argument('--processor', type=str, help='Processor name')
  parser.add_argument('--src', type=str, default=None, help='Source')
  parser.add_argument('--dst', type=str, default=None, help='Destination')
  parser.add_argument('--value', type=float, help='Value')
  parser.add_argument('--threshold', type=float, help='Threshold')
  parser.add_argument('--execute', type=str, default=None, help='Execute command')

  args = parser.parse_args()

  if args.command == 'monitor':
    from sciveo.monitoring.start import MonitorStart
    MonitorStart(period=args.period, block=args.block, output_path=args.output_path)()
  elif args.command == 'scan':
    from sciveo.network.tools import NetworkTools
    host=args.host
    if host is None:
      NetworkTools(timeout=args.timeout, localhost=args.localhost).scan_port(port=args.port, network=args.net)
    else:
      NetworkTools(timeout=args.timeout, ports=json.loads(args.ports)).scan_host(host)
  elif args.command == 'init':
    home = os.path.expanduser('~')
    base_path = os.path.join(home, '.sciveo')
    if not os.path.exists(base_path):
      os.makedirs(base_path)
      default_lines = [
        "secret_access_key=<your secret access key>",
        "api_base_url=https://sciveo.com",
        "sci_log_level=DEBUG"
      ]
      with open(os.path.join(base_path, "default"), 'w') as fp:
        for line in default_lines:
          fp.write(line + '\n')
    else:
      info(f"init, [{base_path}] already there")
  elif args.command == 'nvr':
    from sciveo.media.tools.nvr import VideoRecorder
    VideoRecorder(args.input_path).start()
  elif args.command == 'media-server':
    from sciveo.media.pipelines.server import __START_SCIVEO_MEDIA_SERVER__
    __START_SCIVEO_MEDIA_SERVER__()
  elif args.command == 'media-run':
    if args.processor == "audio-plot":
      from sciveo.media.pipelines.processors.audio.audio_extractor_process import plot_audio
      plot_audio(args.width, args.height, args.rate, args.input_path, args.output_path)
  elif args.command == 'watchdog':
    from sciveo.monitoring.watchdog.memory import MemoryWatchDogDaemon
    daemons = []
    if args.execute is not None:
      daemons.append(MemoryWatchDogDaemon(threshold_percent=args.threshold, period=args.period, command=args.execute))
    for daemon in daemons:
      daemon.start()
    while(True):
      time.sleep(3600)
  elif args.command == 'predictors-server':
    GlobalConfiguration.set("API_PREDICTORS", None)
    from sciveo.api.server import WebServerDaemon
    daemons = [
      WebServerDaemon(port=args.port)
    ]
    for daemon in daemons:
      debug("starting", type(daemon).__name__)
      daemon.start()
    while(True):
      time.sleep(3600)
  else:
    warning(args.command, "not implemented")

if __name__ == '__main__':
    main()