###########################
#
#   WORK IN PROGRESS
#   attempt to rewrite [this example](http://blog.andersen.im/2012/07/signal-emitter-positioning-using-multilateration) in python.
#
############################

from numpy import *
from numpy.linalg import *

#speed of sound in medium
v = 3450
numOfDimensions = 3
nSensors = 5
region = 3
sensorRegion = 2

#choose a random sensor location
emitterLocation = region * ( random.random_sample(numOfDimensions) - 0.5 )
sensorLocations = [ sensorRegion * ( random.random_sample(numOfDimensions)-0.5 ) for n in range(nSensors) ]
p = matrix( sensorLocations ).T

#Time from emitter to each sensor
sensorTimes = [ sqrt( dot(location-emitterLocation,location-emitterLocation) ) / v for location in sensorLocations ]

c = argmin(sensorTimes)
cTime = sensorTimes[c]

#sensors delta time relative to sensor c
t = sensorDeltaTimes = [ sensorTime - cTime for sensorTime in sensorTimes ]

ijs = range(nSensors)
del ijs[c]

A = zeros([nSensors-1,numOfDimensions])
b = zeros([nSensors-1,1])
iRow = 0
rankA = 0
for i in ijs:
	for j in ijs:
		A[iRow,:] = 2*( v*(t[j]-t[c])*(p[:,i]-p[:,c]).T - v*(t[i]-t[c])*(p[:,j]-p[:,c]).T )
		b[iRow,0] = v*(t[i]-t[c])*(v*v*(t[j]-t[c])**2-p[:,j].T*p[:,j]) + \
		(v*(t[i]-t[c])-v*(t[j]-t[c]))*p[:,c].T*p[:,c] + \
		v*(t[j]-t[c])*(p[:,i].T*p[:,i]-v*v*(t[i]-t[c])**2)
		rankA = matrix_rank(A)
		if rankA >= numOfDimensions :
			break
		iRow += 1
	if rankA >= numOfDimensions:
		break

calculatedLocation = asarray( lstsq(A,b)[0] )[:,0]

print "Emitter location: %s " % emitterLocation
print "Calculated position of emitter: %s " % calculatedLocation
