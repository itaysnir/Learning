#include <stdio.h>

int main ()
{

	setvbuf (stdout, 0, 1, 0);
	setvbuf (stdin, 0, 1, 0);
	int c;
	int i = 0;
	int num;
	char g_buf[256];
	printf ("Please enter a CAPTCHA\n");
	scanf ("%d", &num);
	printf ("The CAPTCHA is %d\n", num);
	while (1){
		c = getchar();
		printf ("The cnum is %d, and char %c\n", c, c);
		if (c == '\n'){
			break;
		}
	}

	fgets (g_buf, 1024, stdin);
	printf ("The loaded buffer is %s\n", g_buf);
	

	return 0;
}