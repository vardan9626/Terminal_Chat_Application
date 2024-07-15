#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<signal.h> 
#include<pthread.h>
#include<iostream>
#include<bits/stdc++.h>

#define MAX_BUF 1024
#define SA struct sockaddr
#define SA_IN struct sockaddr_in
#define SA_UN struct sockaddr_un

#define SOCKET_PORT 18000
#define IP_ADDR "192.168.1.106" // Server's IP address


void error_handling(char *message) {
    printf("%s\n", message);
    // exit(1);
}

void close_client(int client_socket)
{
    close(client_socket);
    printf("Client disconnected\n");
}



