# -*- coding: utf-8 -*-

def make_remote_shell(init_func=None, banner=None, use_ipython=True):
  if banner is None:
    banner = 'Interactive Kay Remote Shell'
  if init_func is None:
    init_func = dict
  def action(appid=('a', ''), host=('h', ''), ipython=use_ipython):
    """Start a new interactive python session."""
    import sys
    import getpass
    from google.appengine.ext.remote_api import remote_api_stub
    from kay.misc import get_appid
    namespace = init_func()
    def auth_func():
      return raw_input('Username:'), getpass.getpass('Password:')
    if not appid:
      appid = get_appid()
    if not host:
      host = "%s.appspot.com" % appid
    remote_api_stub.ConfigureRemoteDatastore(appid, '/remote_api', auth_func,
                                             host)
    if ipython:
      try:
        import IPython
      except ImportError:
        pass
      else:
        sh = IPython.Shell.IPShellEmbed(argv='', banner=banner)
        sh(global_ns={}, local_ns=namespace)
        return
    from code import interact
    interact(banner, local=namespace)
  return action
