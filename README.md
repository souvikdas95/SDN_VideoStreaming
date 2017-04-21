# SDN_VideoStreaming

Pre-requisites:

	Floodlight (v1.2+ or Master)
	Mininet (2.2.0b+ or Master)
	FFMpeg (2.0+ or Master)
	Apache Ant (1.6.0+)
	JDK (1.8+)
	Python (2.3.7)
	GCC (C13/C99) (Temporary)
	Apache Maven (3.3.9+)
	
Installation:

	1. Install Floodlight (w/ all Submodules)
	2. Install Mininet (w/ all Submodules + Full Install)
	3. Install FFmpeg (w/ all Submodules + default Compilation configuration given on Site)
	4. Install Dependencies - JDK, GCC, Python, Apache Ant, Apache Maven
	5. Run "$ant" in the base directory (Proxy is not supported)
	6. Run "$python SDN_mininet.py" in the base directory

Noise Calculation:

	Annotations:
		t = Delay b/w Packets (Milliseconds)
		P = Payload Size (Bytes)
		h = Header Size (Bytes) (Always Fixed)
		b = Data Rate (bps) (Given)
		MTU = Maximum Transmission Unit (Always Fixed)
	
	Objective:
		Minimize Z = (1000 / t) aka. Number of Packets transmitted per Second.
	
	Case 1: (Default)
		P is fixed,
			t = 8000 * (h + P) / b
		Optimal Solution: Use max(P) = MTU - h
		Note: This is only feasible if t <= 1000
	
	Case 2:
		t is fixed,
			P = (t * b / 8000) - h
		Optimal Solution: Use max(t) = 1000
		Note: This is only feasible if p <= MTU - h
