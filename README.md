# SDN_VideoStreaming

Pre-requisites:

	Floodlight (v1.2+ or Master)
	Mininet (2.2.0b+ or Master)
	FFMpeg (2.0+ or Master) (must build from Source!)
	Python (2.X)
	Wireshark	
	
Installation:

	1. Install Floodlight (w/ all Submodules)
	2. Install Mininet (w/ all Submodules + Full Install)
	3. Install FFmpeg (w/ all Submodules as instructed at https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu)
	4. FFMpeg: Add PATH for binaries to ~/.buildrc for pathless execution (Important!)
	5. Install Wireshark
	6. (Optional) Install nLoad for B/w Monitoring
	
Run:

	1. Go to Base Directory (contains 'SDN_mininet.py', 'Noise_UDP.py', 'SDN_config.py')
	2. Exec: '$python SDN_mininet.py'
	3. Enter configuration parameters (Skip for default)
	4. Exec: 'mininet> stream <path_to_video>'
	5. View Results at 'output/RESULTS.csv'

Noise Calculation Theory:

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
