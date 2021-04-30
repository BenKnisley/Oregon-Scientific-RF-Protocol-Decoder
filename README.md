Oregon Scientific RF Protocol Decoder
==

This project is a proof of concept for pulling data directly from a simple
household weather monitor directly to my computer using a RTL-SDR. The monitor 
in question is an Oregon Scientific THGR122NX, and it transmits data using the 
the Oregon Scientific RF protocol v2. I am using an RTL-SDR V3 to receive the 
transmitted radio pulse.

I built this project not with the goal of it being useful, but to explore the 
engineering behind the product and to learn. My most important take away is
manchester encoding; I have already taken what I learned about it to other 
projects.

## The Protocol
I learned about the basics of the Oregon Scientific RF Protocol V2 at this link
http://www.osengr.org/WxShield/Downloads/OregonScientific-RF-Protocols-II.pdf.
It also has specifications for several similar protocols, I might port software
to those as well if I can get my hands on those sensors.


## Files & Directories Explanations

`data/` contains a small set of wave files each containing a recording the 
target signal. 

`data/data_values.txt` contains the actual data values for each sample file.

`signal_functions.py` is a library containing functions pertaining to cleaning
and processing the signal.

`message_functions.py` is a library containing functions pertaining to 
processing and formatting the signal message.

`file_decode.py` is an executable for decoding the message from a wave file.

`realtime_decode.py` is an executable for decoding the message from a stdin 
stream.

`start_realtime.sh` is a script that pipes live RTL-SDR data into the 
realtime_decode.py executable.