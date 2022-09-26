#include <unistd.h>
#include <pwd.h>
#include <string.h>
#include <stdio.h>
#include <shadow.h>

int main()
{
	FILE *fpfd;
	FILE *fdata;
	FILE *fshadow;
	FILE *fshadowC;
	FILE *fdoc;
	struct passwd *p;
	struct spwd *up;
	char user[100];
	char oldpasswd[100];
	char newpasswd[100];
	char savepasswd[100];
	int ktra = 0;
	printf("nhap user: ");
	scanf("%s", user);
	printf("nhap pass cu: ");
	scanf("%s", oldpasswd);
	fdata = fopen("/etc/data.txt", "w");
	fclose(fdata);
	fpfd = fopen("/etc/data.txt", "a");
	while ((p = getpwent()) != NULL)
	{
		up = getspnam(p->pw_name);
		if (strcmp(p->pw_name, user) == 0)
		{
			up = getspnam(user);
			if (up)
				p->pw_passwd = up->sp_pwdp;
			if (strcmp(p->pw_passwd, crypt(oldpasswd, p->pw_passwd)) == 0)
			{
				ktra = 1;
				printf("dang nhap thanh cong\n");
				printf("nhap pass moi: ");
				scanf("%s", newpasswd);
				strcpy(savepasswd, crypt(newpasswd, p->pw_passwd));
				up->sp_pwdp = savepasswd;
				printf("doi mat khau thanh cong\n");
			}
			else
				printf("khong tim thay user hoac mat khau sai\n");
		}
		putspent(up, fpfd);
	}
	fclose(fpfd);
	if (ktra = 1)
	{
		char data[1000];
		fshadowC = fopen("/etc/shadow", "w");
		fclose(fshadowC);
		fshadow = fopen("/etc/shadow", "a");
		fdata = fopen("/etc/data.txt", "r");
		while (fgets(data, 1000, fdata) != NULL)
		{
			fputs(data, fshadow);
		}
		fclose(fshadow);
		fclose(fdata);
	}
	else
		printf("khong tim thay user hoac mat khau sai\n");
	fdata = fopen("/etc/data.txt", "w");
	fclose(fdata);
	return 0;
}