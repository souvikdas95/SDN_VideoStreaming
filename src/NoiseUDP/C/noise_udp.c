#include <stdio.h>
#include <stdarg.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <strings.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <time.h>
#include <math.h>

double max(double a, double b)
{
	return a > b ? a : b;
}

int main(int argc, char** argv)
{
	int servSocket;
	struct sockaddr_in remoteAddr;
	struct sockaddr_in localAddr;
	socklen_t addrlen, len, iOpt;
	
	servSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	
	bzero(&localAddr, sizeof(localAddr));
	localAddr.sin_family = AF_INET;
	localAddr.sin_port = htons(max(1024, argc > 1 ? atoi(argv[1]) : 65535));
	localAddr.sin_addr.s_addr = INADDR_ANY;

	bind(servSocket, (const struct sockaddr *) &localAddr, sizeof(localAddr));
	
	iOpt = 1;
	setsockopt(servSocket, SOL_SOCKET, SO_BROADCAST, &iOpt, sizeof(int));
	
	bzero(&remoteAddr, sizeof(remoteAddr));
	remoteAddr.sin_family = AF_INET;
	remoteAddr.sin_port = htons(max(1024, argc > 1 ? atoi(argv[1]) : 65535));
	remoteAddr.sin_addr.s_addr = htonl(-1);	// Broadcast
	addrlen = sizeof(remoteAddr);
	
	unsigned long plen = max(0, argc > 2 ? atoi(argv[2]) : 1024);	// Overhead: 18 (Ethernet) + 20 (IP) + 12 (IP-PseudoHeader) + 8 (UDP-Header) + 6 (Ethernet-Padding) = 52 Bytes
	printf("payload length = %lu\n", plen);
	char* payload = (char*) malloc(sizeof(char) * plen);
	memset(payload, (char)~0, plen);	// Set all bits to 1
	struct timespec tim, tim2;
	tim.tv_sec  = max(0, argc > 3 ? floor(atof(argv[3])) / 1000 : 0);
	printf("tim.tv_sec = %lu\n", tim.tv_sec);
	tim.tv_nsec = (unsigned long)((double)max(tim.tv_sec > 0 ? 0 : 1, argc > 3 ? fmod(atof(argv[3]), 1000) : 1) * (double)1000000L);	// 1 ms = 10^6 ns
	printf("tim.tv_nsec = %lu\n", tim.tv_nsec);
	printf("data rate (calculated): %0.2f KBit/s\n", ((double)(plen + 52) * (double)8 / (double)1024) / ((double)tim.tv_sec + (double)tim.tv_nsec / (double)1000000000L));
	while(1)
	{
		len = sendto(servSocket, payload, plen, 0, (const struct sockaddr*) &remoteAddr, (socklen_t) addrlen);
		nanosleep(&tim, &tim2);	// Delay
	}
	
	shutdown(servSocket, 2);
	close(servSocket);
	return 0;
}
