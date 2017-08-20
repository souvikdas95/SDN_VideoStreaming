# SDN_VideoStreaming

## Testing Environment

	1. Server: Dell PowerEdge T630 Tower Server
	2. Processor: Intel(R) Xeon(R) E5-2630 v3 (20M Cache, 2.40 Ghz, 8 GT/s Intel QPI)
	3. Memory: 16 GB (NUMA #1) out of 32 GB Total (DDR4 2100 MHz)
	4. Storage: 16 GB (NUMA #0) Volatile RAM Disk Drive Volume (NTFS) enclosing VMDK
	5. OS: Ubuntu Desktop 16.04.2 64-bit

## Software Packages Used:

	1. Floodlight (v1.2)
	2. Mininet/Containernet (v2.2.0b2)
	3. FFMpeg (v3.3)
	4. Python (v2.7)
	5. Wireshark (v2.2.6)

## Project Setup:

	1. Install Floodlight from Scratch (Git Master)
		1. `sudo apt-get -y install build-essential ant maven python-dev`
		2. `sudo apt-get -y install openjdk-8-jre openjdk-8-jdk`
		3. `git clone git://github.com/floodlight/floodlight.git`
		4. `cd floodlight`
		5. `git submodule init`
		6. `git submodule update`
		7. `sudo mkdir /var/lib/floodlight`
		8. `sudo chmod 777 /var/lib/floodlight`
	2. Install Mininet from Scratch (Git Master – Install Everything)
		1. `git clone git://github.com/mininet/mininet`
		2. `cd mininet/util`
		3. `sudo bash install.sh -a`
	2. (Alternative) Install Containernet (For Docker Support)
		1. `sudo apt-get -y install ansible git aptitude`
		2. `sudo echo 'localhost ansible_connection=local' >> /etc/ansible/hosts`
		3. `git clone https://github.com/containernet/containernet.git`
		4. `cd containernet/ansible`
		5. `sudo ansible-playbook install.yml`
	3. Install FFmpeg (Git Master)
		1. `sudo apt-get -y install autoconf automake build-essential \
		   libass-dev libfreetype6-dev libsdl2-dev libtheora-dev \
		   libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev \
		   libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo wget \
		   zlib1g-dev yasm nasm libx264-dev libx265-dev libfdk-aac-dev \
		   libmp3lame-dev libopus-dev libvpx-dev`
		2. `cd FFmpeg`
		3. `mkdir build`
		4. `cd build`
		5. `sudo ../configure \
		   --enable-gpl \
		   --enable-libass \
		   --enable-libfdk-aac \
		   --enable-libfreetype \
		   --enable-libmp3lame \
		   --enable-libopus \
		   --enable-libtheora \
		   --enable-libvorbis \
		   --enable-libvpx \
		   --enable-libx264 \
		   --enable-libx265 \
		   --enable-nonfree \
		   --enable-libfontconfig`
		6. `sudo make -j`
		7. `sudo make install`
		8. `hash -r`
	4. Install Wireshark (Package)
		* For GUI users:
		`sudo apt-get -y install wireshark`
		* (Alternative) For CLI users:
		`sudo apt-get -y install tshark`
	5. (Optional) Install nLoad (Package) for Bandwidth Monitoring
		`sudo apt-get -y install nload`

## Project Execution Instruction:

	1. Go to Base Directory (contains 'SDN_mininet.py')
	2. Exec: '$python SDN_mininet.py'
	3. Enter configuration parameters (Skip for default)
	4. Exec: 'mininet> stream <path_to_video>'
	5. View Results at 'output/RESULTS.csv'

## Mininet Script Configuration Parameters:

#### Base Config Parameters:
  
	# Type of Topology
	# 1. Bus
	# 2. Ring
	# 3. Mesh
	# 4. Star
	# 5. Random
	# Note: Random doesn't have fixed no. of Hosts in the Network
	TOPOLOGY_TYPE = 1

	# No. of Switches in the entire Topology
	SWITCH_COUNT = 4

	# No. of Hosts per Switch in the Topology
	# Note: For Random, this is the Max. Hosts per Switch (0 - Minimum)
	HOST_COUNT_PER_SWITCH = 2

	# Max. Switch-Switch Links in the Topology globally
	# Note: Only valid for Random (Value Range depends on SWITCH_COUNT)
	SWITCH_GLOBAL_MAX_LINKS = ?

	# Enable STP at Switch
	# Note: May be required in case of sophisticated topology
	# Note: Helps prevent broadcast storms
	USE_STP = False (F)

	# Link/Interface Speed Requirement for each Host Node (QoS)
	# Range: 1 - 1000 (Mbps)
	HOST_LINK_SPEED = 1

	# Link/Interface Speed Requirement for each Switch Node (QoS)
	# Range: 1 - 1000 (Mbps)
	SWITCH_LINK_SPEED = 1

#### Docker Config Parameters:

	# Enable Docker Hosts
	# Docker Containers will be used as
	# Host nodes in the Topology
	DOCKER_ENABLE = True (T)
	
	# Docker Image to use for building Containers
	# Note: The image must support the requirements.
	#       Please check the image configuration 
	DOCKER_IMAGE = "ubuntu:build_sdn"
	
	# Docker Host Resource Configuration Arguments
	# Check: https://docs.docker.com/engine/reference/run/
	# Note: In CLI, use '-' for an arg to use default.
	DOCKER_CPU_QUOTA = -1;
	DOCKER_CPU_PERIOD = None;
	DOCKER_CPU_SHARES = None;
	DOCKER_CPUSET_CPUS = None;
	DOCKER_MEM_LIMIT = None;
	DOCKER_MEMSWAP_LIMIT = None;

#### Mininet Packet Config Parameters:

	# Maximum Transmission Unit (Bytes)
	# for a Packet transmitted in Mininet
	# Note: This can't be altered from CLI
	MTU = 1492

	# Protocol Overhead in Mininet
	# 18 (Ethernet) +
	# 20 (IP) +
	# 12 (IP-PseudoHeader) +
	# 8 (UDP-Header) +
	# 6 (Ethernet-Padding)
	# = 52 Bytes
	# Note: This can't be altered from CLI
	OVERHEAD = 52
	
	# Size of Payload to be used
	# when transmitting packets in Mininet
	# Note: This can't be altered from CLI
	NOISE_PACKET_PAYLOAD_SIZE = MTU - OVERHEAD;
	
	# Note:
	# These will later be referenced from within
	# Mininet instead of explicit hardcoding.

#### Stream Config Parameters:

	# No. of Stream Recorders/Destinations in the Topology
	# Note: In case of Random, if it exceeds allocated hosts, all 
	# other than source host becomes Stream Recorder/Destination
	DESTINATION_COUNT = 1

	# IP Address (Must be Multicast) for Streaming by Host
	STREAM_IP = 234.0.0.1

	# Port (Must be Ephimeral) for Streaming by Host
	STREAM_PORT = 5555

	# Noise Type
	# 1. Broadcast (Simplex Flood Each to All)
	# 2. Unicast (Duplex Flood in Unique Pairs)
	NOISE_TYPE = 1
	
	# Port (Must be Ephimeral) for Noise Generated in the Network
	# Noise is generated by all hosts which are niether Source nor
	# Destination in Streaming
	NOISE_DESTINATION_PORT = 65535

	# Noise Data Rate (in bps) per Host
	NOISE_DATA_RATE = 32768
	
	# Delay between consecutive Noise Packets
	# Note: This is a derived parameter
	NOISE_PACKET_DELAY = 8000 * MTU / NOISE_DATA_RATE
	
	# Port (Must be Ephimeral) for SAP (Session Announcement)
	# and exchange of SDPs b/w Streamer & Recorder
	SAP_PORT = 49160

## Docker Image Configuration ('ubuntu:build_sdn')

	1. `sudo docker run -dt --name="_build_sdn" ubuntu:xenial bash`
	2. `sudo docker -it _build_sdn bash`
	3. Run these inside the container:
	   `apt-get update
	   apt-get upgrade
	   apt-get -y install net-tools iputils-ping tshark nload python \
	   python-pip autoconf automake build-essential libass-dev \
	   libfreetype6-dev libtheora-dev libtool libvorbis-dev pkg-config \
	   texinfo wget zlib1g-dev yasm nasm libx264-dev libx265-dev \
	   libfdk-aac-dev libmp3lame-dev libopus-dev libvpx-dev
	   cd FFmpeg
	   mkdir build
	   cd build
	   ../configure \
	     --enable-gpl \
	     --enable-libass \
	     --enable-libfdk-aac \
	     --enable-libfreetype \
	     --enable-libmp3lame \
	     --enable-libopus \
	     --enable-libtheora \
	     --enable-libvorbis \
	     --enable-libvpx \
	     --enable-libx264 \
	     --enable-libx265 \
	     --enable-nonfree \
	     --enable-libfontconfig
	   make -j
	   make install
	   hash -r
	   exit`
	4. `sudo docker commit _build_sdn ubuntu:build_sdn`
	5. `sudo docker kill _build_sdn`
	6. `sudo docker rm _build_sdn`

## Project Description:

	Floodlight is an Open Source SDN Controller, compatible to be used by 
	Mininet, an Open Source Virtual Network Emulator. OVSSwitch provides the 
	necessary toolset for Switching functionality in SDN to Mininet. Since 
	the emergence of Netoworking as a functionality for connecting People 
	across the world, we have only observed patented standards for configuration 
	of networks by some of the most prestigious companies in the networking 
	industry, namely Cisco & Juniper. For instance, Cisco uses IOS as the underlying 
	OS for almost all of the hardwares that it's built so far. It has pre-defined 
	RFC Standards for R&S which means, we can't alter the algorithms they use, 
	or make out-of-the-box changes to adapt to our envisioned network requirements. 
	For ages, we have seen network administrators going on sacrificing and compromising 
	optimalitity in their networks with sub-optimal and fixed solutions of these 
	companies. However, with the emergence of SDN, we have near to Full Control over our 
	network's working, using the same backbone architectures that we've been 
	using but with added functionality of customizability. In our case, OVSSwitch 
	& Floodlight together do that job for R&D Purpose. 
	With a simple Multicast Routing Algorithm implemented over fundamental SDN 
	implementation, we are trying to test the feasability of the network by using 
	Video Streaming as the sole application. Why Video Streaming? It involves 
	Realtime sampling & packeting, QoS specifications, Realtime Media Controlling 
	functionality and most importantly, can't afford large packet losses. All of these
	can be provided by RTP (W/ RTCP) which is an application layer protocol using 
	UDP as the underlying payload container, made solely for Realtime Communications 
	(Audio/Visual). It supports Multi-party Communications & Conferences as well. 
	Applications made over this protocol, also have the provisioning for Error 
	Prevention 	& Concealment, alongside Timestamping and Sequencing, which together 
	helps in smooth playback irrespective of adverse network conditions like 
	Broadcast Noise. In our case, we are using FFmpeg's inbuild functionality for 
	RTP (PT96) Streaming & Recording over Multicast Network. In the background, we have 
	initiated a simple 'Broadcast Noise' contributed by the hosts in the network, to 
	deploy scalable traffic in the network. QoS implementation by Mininet on the other 
	hand, helps in balancing out this traffic. By analyzing the frames & the packets, 
	we are able to produce mapping of sent and receive quality in SDN. By applying that 
	over Multicast Networks, we are able to test the susceptibility of the network in 
	Multicasting Environments.

## Previously Used/Tested Software Packages/Scripts (See: old/):

	1. LibVLC (from VideoLAN – Native VLC Player Library)
		This library has no video processing/post-processing logging and control. 
		Also, the binary is produced as a single package without any customizability 
		or addon feature.
	2. Vlcj Java API
		This API is not VideoLAN proprietary and so, isn’t suitable for R&D purpose.
	3. Apache Ant, Maven with Maven Ant Tasks
		Use of Maven Ant Tasks is depricated. This was one of the reasons, why we planned 
		to remove Java as dependency from Mininet’s script. Note: Floodlight still requires 
		JDK with Apache Ant.
	4. NoiseUDP (C/Java), StreamVLC (Java), RecordVLC (Java), PlayVLC (Java)

## Noise Calculation Theory:

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
