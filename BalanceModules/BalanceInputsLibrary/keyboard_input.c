#include <stdio.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>

static int fd = -1;

int open_keyboard_event()
{
	fd = open("/dev/input/event0", O_RDONLY);

	if(fd >= 0)
		return 0;
	else
	{
		fd = -1;
		return 1;
	}
}

int get_keyboard_event()
{
	int ret;
	struct input_event event;
	int key;

	if(fd < 0)
		return -1;

	while(1)
	{
		ret = read(fd, &event, sizeof(struct input_event));
		if(ret < 0)
			return -1;

		if(event.code == 4)
		{
			key = event.value;
			ret = read(fd, &event, sizeof(struct input_event));
			if(ret < 0)
				return -1;

			if(event.value == 1)
				return key - 0x6FFA3;
		}
	}
}

int close_keyboard_event()
{
	close(fd);
	fd = -1;
	return 0;
}
