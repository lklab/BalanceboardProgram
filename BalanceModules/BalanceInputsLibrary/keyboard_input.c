#include <stdio.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>

int open_keyboard_event();
int flush_keyboard_event();
int get_keyboard_event();
int close_keyboard_event();

static int fd = -1;

int open_keyboard_event()
{
	fd = open("/dev/input/event0", O_RDONLY | O_NONBLOCK);

	if(fd >= 0)
		return 0;
	else
	{
		fd = -1;
		return -1;
	}
}

int flush_keyboard_event()
{
	if(fd < 0)
		return -1;

	while(get_keyboard_event() != -1);
	return 0;
}

int get_keyboard_event()
{
	int ret;
	struct input_event event;
	int key, value;

	if(fd < 0)
		return -1;

	value = -1;
	while(1)
	{
		ret = read(fd, &event, sizeof(struct input_event));
		if(ret < 0)
			return value;

		if(event.code == 4)
		{
			key = event.value;
			ret = read(fd, &event, sizeof(struct input_event));
			if(ret < 0)
				return value;

			if(event.value == 1)
				value = key - 0x6FFA3;
		}
	}
}

int close_keyboard_event()
{
	close(fd);
	fd = -1;
	return 0;
}
