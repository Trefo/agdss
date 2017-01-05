c = get_config()
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always
c.NotebookApp.ip = 'airborne.ddns.net'
c.NotebookApp.port = 8001
c.NotebookApp.open_browser = False
c.NotebookApp.tornado_settings = { 'headers': { 'Content-Security-Policy': "frame-src 'self' http://airborne.ddns.net:8001/" } }

