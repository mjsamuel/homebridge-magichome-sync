import logging, json
from bottle import route, request, run
from workers import StoppableThread, sync_screen

sync_worker = StoppableThread(target=sync_screen)


@route('/api/state', method='GET')
def get_state():
    status = "enabled" if sync_worker.is_alive() else "disabled"
    response = { "status": status}

    return json.dumps(response)


@route('/api/state', method='POST')
def set_state():
    data = json.loads(request.body.read())
    response = { "status": None }

    if data['status']:
        response['status'] = "enabled"
        sync_worker.start()
    else:
        response['status'] = "disabled"
        if sync_worker is not None and sync_worker.is_alive():
            sync_worker.stop()
            sync_worker.join()

    return json.dumps(response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        run(host='localhost', port=6006)
    finally:
        if sync_worker is not None and sync_worker.is_alive():
            sync_worker.stop()
            sync_worker.join()
