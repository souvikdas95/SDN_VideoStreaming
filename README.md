# SDN_VideoStreaming

Pre-requisites:

	Floodlight (v1.2+ or Master)
	Mininet (2.2.0+ or Master)

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
