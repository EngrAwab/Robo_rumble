import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,True)
for x in range(100000000):
	pass
GPIO.output(11,False)
GPIO.cleanup()

