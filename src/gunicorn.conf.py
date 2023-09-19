import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "core.wsgi:application"
threads = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
accesslog = "-"
