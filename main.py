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
t = sensorDeltaTimes = matrix( [ sensorTime - cTime for sensorTime in sensorTimes ] )

ijs = range(nSensors)
del ijs[c]

A = zeros([nSensors-1,numOfDimensions])
b = zeros([nSensors-1,1])
iRow = 0
rankA = 0
for i in ijs:
	for j in ijs:
		#original 2*(v*(t(j)-t(c))*(p(:,i)-p(:,c)).T-v*(t(i)-t(c))*(p(:,j)-p(:,c)).T)
		#I swapped the column accessors to row accessors, because it seemed the wrong way round 
		A[iRow,:] = 2*( v*(t[j]-t[c])*(p(:,i)-p(:,c)).T - v*(t[i]-t[c])*(p[:,j]-p[:,c]).T )
		b[iRow,1] = 0.0 #Something something, too tired heading to bed
		rankA = matrix_rank(A)
		if rankA >= nDim :
			break

		iRow += 1

	if rankA >= nDim:
		break

calculatedLocation = solve(A,b)

print "Emitter location: %s " % emitterLocation
print "Calculated position of emitter: %s " % calculatedLocation
