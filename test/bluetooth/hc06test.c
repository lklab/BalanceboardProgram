#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(void)
{
	int rfcomm0;
	int read_bytes;
	char buff[255];
	int count = 10;

	rfcomm0 = open("/dev/rfcomm0", O_RDWR | O_NOCTTY);
	if(rfcomm0 == -1)
	{
		printf("ERROR: unable to open rfcomm0\n");
		return 0;
	}
	printf("rfcomm successfully opened\n");

	while(count > 0)
	{
		read_bytes = read(rfcomm0, buff, sizeof(buff));
		buff[read_bytes] = '\0';
		if(read_bytes > 0)
			printf("received: [%s]\n");
		else
			printf("ERROR: read fail\n");

		count--;
	}

	close(rfcomm0);

	return 0;
}
