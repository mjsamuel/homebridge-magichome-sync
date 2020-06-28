import logging, json
from bottle import route, request, run
from workers import StoppableThread, sync_screen

sync_worker = StoppableThread(target=sync_screen,  args=("light", 1))


@route('/api/state', method='GET')
def get_state():
    status = "enabled" if sync_worker.is_alive() else "disabled"
    response = { "status": status}

    return json.dumps(response)


@route('/api/state', method='POST')
def set_state():
    global sync_worker
    data = json.loads(request.body.read())

    if data['status']:
        if sync_worker.is_alive() is False:
            light_ip = data['light_ip']
            light_type = data['light_type']
            polling_interval = data['polling_interval']

            logging.info("Starting sync worker thread")
            sync_worker = StoppableThread(
                target=sync_screen, 
                args=(light_ip, light_type, polling_interval))
            sync_worker.start()
    else:
        if sync_worker.is_alive():
            logging.info("Stopping sync worker thread")
            sync_worker.stop()
            sync_worker.join()

    status = "enabled" if sync_worker.is_alive() else "disabled"
    response = { "status": status }

    return json.dumps(response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        run(host='localhost', port=6006)
    finally:
        if sync_worker.is_alive():
            sync_worker.stop()
            sync_worker.join()
