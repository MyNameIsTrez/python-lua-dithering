brightness = 0.5
prev_frame = 0.5
diff = brightness - prev_frame

print(brightness if diff else -1)