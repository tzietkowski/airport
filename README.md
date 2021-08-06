# airport

An application that manages automatic landing at the airport. The airport is the server and the planes are the clients connecting to the airport. 

Assumptions:
- the airport has two runways 
- the airfield space has dimensions of 10x10x5 km 
- a maximum of 100 planes can approach the landing, the rest will be refused 
- each plane has fuel for 3 hours 
- there are two landing air corridors 
- planes spawn in a random location between 2 and 5 km 
- if the planes are closer than 10m to each other, a collision occurs 

airport - the server works concurrently to communicate with airplanes on an ongoing basis 

