import socketio

EVENT_MANAGER_HOST = 'gts-event-manager'
EVENT_MANAGER_PORT = '8083'

sio = socketio.AsyncClient()


@sio.event
def connect():
    print("Connected to gts-event-manager")

@sio.event
def connect_error(data):
    print("Failed to connect to gts-event-manager")

@sio.event
def disconnect():
    print("Disconnected from gts-event-manager")


async def connect_to_event_manager():
    await sio.connect(f"http://{EVENT_MANAGER_HOST}:{EVENT_MANAGER_PORT}", namespaces=['/gts-service'])