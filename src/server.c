#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdlib.h>

typedef int SOCKET;

#define FIRST 1
#define SECOND 0

struct Move {
    uint16_t row;
    uint16_t column;
    uint16_t winner;
};

struct Move receive_move_from_player(SOCKET player_socket) {
    struct Move move;
    
    if(recv(player_socket, (char*) &move.row, sizeof(move.row), 0) < 0) {
        printf("Error receiving the data\n");
    }
    if(recv(player_socket, (char*) &move.column, sizeof(move.column), 0) < 0) {
        printf("Error receiving the data\n");
    }
    if(recv(player_socket, (char*) &move.winner, sizeof(move.winner), 0) < 0) {
        printf("Error receiving the data\n");
    }
    
    move.row = ntohs(move.row);
    move.column = ntohs(move.column);
    move.winner = ntohs(move.winner);
    return move;
}

void send_move_to_player(SOCKET player_socket, struct Move move) {
    move.row = htons(move.row);
    move.column = htons(move.column);
    move.winner = htons(move.winner);

    if(send(player_socket, (char*) &move.row, sizeof(move.row), 0) < 0) {
        printf("Error sending the data\n");
    }
    if(send(player_socket, (char*) &move.column, sizeof(move.column), 0) < 0) {
        printf("Error sending the data\n");
    }
    if(send(player_socket, (char*) &move.winner, sizeof(move.winner), 0) < 0) {
        printf("Error sending the data\n");
    }
}

void handle_game(SOCKET first_player_socket, SOCKET second_player_socket) {
    int16_t turn = FIRST;
    turn = htons(turn);
    send(first_player_socket, (char*) &turn, sizeof(turn), 0);
    turn = SECOND;
    turn = htons(turn);
    send(second_player_socket, (char*) &turn, sizeof(turn), 0);


    while(1) {
        struct Move move = receive_move_from_player(first_player_socket);
        send_move_to_player(second_player_socket, move);
        struct Move move2 = receive_move_from_player(second_player_socket);
        send_move_to_player(first_player_socket, move2);
    }
}

int main(int argc, char *argv[]) {
    SOCKET server_socket;
    struct sockaddr_in server, first_player, second_player;

    if((server_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("Error creating the socket\n");
        return 1;
    }

    memset(&server, 0, sizeof(server));
    server.sin_port = htons(5270);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;

    if(bind(server_socket, (struct sockaddr* ) &server, sizeof(server)) < 0) {
        printf("Error binding the socket\n");
        return 1;
    }

    listen(server_socket, 1);

    socklen_t size = sizeof(first_player);
    SOCKET first_player_socket = accept(server_socket, (struct sockaddr *) &first_player, &size);
    
    if(first_player_socket < 0) {
        printf("Error accepting\n");
        return 1;
    }
    printf("First player connected with IP %s and PORT %d\n", inet_ntoa(first_player.sin_addr), ntohs(first_player.sin_port));

    size = sizeof(second_player);
    SOCKET second_player_socket = accept(server_socket, (struct sockaddr *) &second_player, &size);

    if(second_player_socket < 0) {
        printf("Error accepting\n");
        return 1;
    }
    printf("Second player connected with IP %s and PORT %d\n", inet_ntoa(second_player.sin_addr), ntohs(second_player.sin_port));

    handle_game(first_player_socket, second_player_socket);
    close(first_player_socket);
    close(second_player_socket);
    close(server_socket);
}
