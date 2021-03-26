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