# robot_car
robot car SW based on Adeept PiCar-B

This repository contains the modified code from the Adeept PiCar-B repository.  I intentionaly did not fork their repository
because the code was so poorly written that a major rewrite was needed.  

So far I have removed lots of extraneous code, and repaired lots of eroneous stuff.  The Adeept SW was clearly written in a 
clasical lazy hacking process that left many cut and pasted comment errors (some of which I haven't gotten around to cleaning up)
and lots of sledge hammer fixes to coding errrors that reflect an obviously poor understanding of the imported modules. An example 
of this is the laughably pointless 'loop' method in the client.py module with the comical sledge hammer conditional at it's end 
to ensure the TK mainloop only runs once.  

I have also ported the client GUI to work on the Raspberry Pi to facilitate debugging using just the single Raspbian desktop.  I 
added some shell scripts to start and kill the server SW and to log the output to files to help in debugging.

There is more to be done for sure, but this is a good start. 
