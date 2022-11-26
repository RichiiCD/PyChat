import sys
from sockets.server import ServerSocket
from application import ChatApplication
from application import configure_application


if __name__ == "__main__":

   args = sys.argv
   
   if (args[1] == 'runserver'):
      server = ServerSocket(64)
      if (server.setup()):
         server.run()

   if (args[1] == 'chat'):
      app = ChatApplication()

   if (args[1] == 'settings'):
      configure_application()
      