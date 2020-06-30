import logging, json
from bottle import route, response, request, run
from mh_device import MagicHomeDevice
from workers import StoppableThread, sync_screen

sync_worker = StoppableThread(target=sync_screen,  args=("light", 1))


@route('/api/state', method='GET')
def get_state():
    status = "enabled" if sync_worker.is_alive() else "disabled"
    message = { "status": status}

    return json.dumps(message)


@route('/api/state', method='POST')
def set_state():
    global sync_worker
    data = json.loads(request.body.read())

    message = { "status": "disabled" }

    if data['status'] and sync_worker.is_alive() is False:
        light_ip = data['light_ip']
        light_type = data['light_type']
        polling_interval = data['polling_interval']

        try:
            logging.info("Attempting to connect to Magic Home device")
            light = MagicHomeDevice(ipaddr=light_ip, setup=light_type)

            logging.info("Starting sync worker thread")
            sync_worker = StoppableThread(
                target=sync_screen, 
                args=(light, polling_interval))
            sync_worker.start()
            message["status"] = "enabled"
        except:
            logging.warning("Failed to connect to Magic Home device")
            response.status = 400
            message["error"] = "Failed to connect to Magic Home device"
    elif data['status'] is False and sync_worker.is_alive():
        logging.info("Stopping sync worker thread")
        sync_worker.stop()
        sync_worker.join()

    return json.dumps(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        run(host='0.0.0.0', port=6006)
    finally:
        if sync_worker.is_alive():
            sync_worker.stop()
            sync_worker.join()
