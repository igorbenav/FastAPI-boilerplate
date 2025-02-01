from prometheus_client import multiprocess


def worker_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)
