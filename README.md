Oregon Scientific RF Protocol Decoder
==

This project is a proof of concept for pulling data directly from a simple
household weather monitor directly to my computer using a RTL-SDR. The monitor 
in question is an Oregon Scientific THGR122NX, and it transmits data using the 
the Oregon Scientific RF protocol v2. I am using an RTLSDR to receive the 
transmitted radio pulse.

I built this project not with the goal of it being useful, but to explore the 
engineering behind the product and to learn. I learned about manchester 
encoding, signal processing, and building faster software.



## The Protocol
I learned about the basics of the Oregon Scientific RF Protocol V2 at this link
http://www.osengr.org/WxShield/Downloads/OregonScientific-RF-Protocols-II.pdf


## Files & Directories

`data/` Directory contains a small sample of wave files containing sample 
signals. 

`data/data_values.txt` contains the actual data values for each sample file.


`signal_functions.py` is a library containing functions pertaining to cleaning
and processing the signal.

`message_functions.py` is a library containing functions pertaining to 
processing and formatting the signal message.

`file_decode.py` is an executable for decoding the message from a wave file.

`realtime_decode.py` is an executable for decoding the message from a stdin 
stream.

`start_realtime.sh` is a script that pipes live RTL-SDR data into the realtime_decode.py executable.