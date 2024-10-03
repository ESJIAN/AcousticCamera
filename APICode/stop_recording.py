def stop_recording():
    global stream, is_recording
    if is_recording:
        stream.stop_stream()
        stream.close()
        is_recording = False