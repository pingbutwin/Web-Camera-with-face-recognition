import cv2
import asyncio
import websockets
import time

log_label = '[CLIENT]:'
async def stream_camera():
    url = input('Enter public url given by server: ')

    cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print(f'{log_label} establishing connection with {url}')

    try:
        async with websockets.connect(url) as websocket:
            print(f'{log_label} connected, starting streaming')
            while cap.isOpened():

                ret, frame = cap.read()
                if not ret:
                    print(f'{log_label} no frame, breaking')
                    break
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                try:
                    await websocket.send(buffer.tobytes())
                except websockets.exceptions.ConnectionClosedError:
                    print(f'{log_label} ERROR: connection closed')
                    break
                except Exception as e:
                    print(f'{log_label} ERROR: {e}')
                await asyncio.sleep(0.01)
    except Exception as e:
        print(f'{log_label} ERROR (while connecting): {e}')
    finally:
        if cap.isOpened():
            cap.release()
        print(f'{log_label} Releasing all resources')

if __name__ == '__main__':
    try:
        asyncio.run(stream_camera())
    except KeyboardInterrupt:
        print(f'{log_label} Shutting down the client')

