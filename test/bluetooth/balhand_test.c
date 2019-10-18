#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>

int main(int argc, char **argv)
{
	struct sockaddr_rc addr = {0};
	int s, status, bytes_read;
	char dest[18] = "98:D3:31:FD:63:8D";
	char buf[1024] = {0};

	/* allocate socket */
	s = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);

	/* set the connection parameters (who to connect to) */
	addr.rc_family = AF_BLUETOOTH;
	addr.rc_channel = (uint8_t)1;
	str2ba(dest, &addr.rc_bdaddr);

	/* connect to server */
	status = connect(s, (struct sockaddr*)&addr, sizeof(addr));
	if(status != 0)
	{
		printf("fail to connect!\n");
		return 0;
	}
	printf("connection success!!!, wait for data...\n");

	/* receive data */
	bytes_read = read(s, buf, sizeof(buf));
	if(bytes_read > 0)
	{
		buf[bytes_read] = '\0';
		printf("received [%s]\n", buf);
	}

	/* close connection */
	close(s);
	return 0;
}

