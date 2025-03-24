import json
import os
import pdb

from stoobly_agent.config.data_dir import DataDir

class MitmproxyConfig():
  MITMPROXY_DIR_NAME = '.mitmproxy'

  __instance = None
  __master = None

  def __init__(self, master):
    if self.__instance:
        raise RuntimeError('Call instance() instead')
    else:
        self.__master = master 

        self.__mitmproxy_dir_path = DataDir.instance().mitmproxy_conf_dir_path

        if not os.path.exists(self.__mitmproxy_dir_path):
            os.mkdir(self.__mitmproxy_dir_path)

  @classmethod
  def instance(cls, master = None):
      if cls.__instance is None:
        cls.__instance = cls(master)

      return cls.__instance

  @property
  def ca_cert_pem_path(self):
      path = os.path.join(self.__mitmproxy_dir_path, 'mitmproxy-ca-cert.pem')

      if not os.path.exists(path):
          return ''

      return path

  def with_master(self, master):
    from mitmproxy.tools.dump import DumpMaster
    self.__master: DumpMaster = master

  def get(self, key: str):
    if not self.__master:
      try:
        fp = open(DataDir.instance().mitmproxy_options_json_path, 'r')
        contents = fp.read()
        fp.close()
        options = json.loads(contents)
        return options.get(key)
      except Exception as e:
        pass
    else:
      from mitmproxy.options import Options
      options: Options = self.__master.options

      if key in options:
        for k, val in options.items():
          if key == k:
            return val.current()

  def set(self, option: tuple):
    if self.__master:
      self.__master.options.set(*option)

  def dump(self):
    if not self.__master:
      return

    options = {}
    for k, v in self.__master.options.items():
      options[k] = v.current()

    fp = open(DataDir.instance().mitmproxy_options_json_path, 'w')
    fp.write(json.dumps(options, indent=2, sort_keys=True))
    fp.close()