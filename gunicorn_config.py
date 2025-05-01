import multiprocessing

# Configurações do servidor
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
timeout = 120
worker_class = "sync"

# Configurações de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configurações de reload e debug
reload = False
capture_output = True
enable_stdio_inheritance = True 