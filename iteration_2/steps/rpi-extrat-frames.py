import time
import picamera

with picamera.PiCamera(resolution=(1280, 720), framerate=30) as camera:
    camera.iso = 800
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    camera.start_preview()
    start = time.time()
    camera.capture_sequence((
        'frames/image%03d.jpg' % i
        for i in range(120)
        ), use_video_port=True)
    print('Captured 120 images at %.2ffps' % (120 / (time.time() - start)))
    camera.stop_preview()