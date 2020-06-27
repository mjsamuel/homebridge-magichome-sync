import logging, json
from bottle import route, request, run
from workers import StoppableThread, sync_screen

sync_worker = StoppableThread(target=sync_screen)

@route('/api/state', method='GET')
def get_state():
    response = { "is_syncing": sync_worker.is_alive() }

    return json.dumps(response)


@route('/api/state', method='POST')
def set_state():
    response = { "message": None }
    data = json.loads(request.body.read())

    if data['sync']:
        response['message'] ="started syncing"
        sync_worker.start()
    else:
        response['message'] ="stopped syncing"
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
