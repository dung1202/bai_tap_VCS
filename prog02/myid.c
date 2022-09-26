#include <stdio.h>
#include <pwd.h>
#include <grp.h>
#include <string.h>

int main(){
	char n[100];
	printf("Nhap user: ");
	scanf("%s", n);
	struct passwd *pw;
	struct group *up;
	pw = getpwnam(n);
	if(pw != NULL){
		printf("User ID = %u\n", pw->pw_uid);
		printf("User Name = %s\n", pw->pw_name);
		printf("Home = %s\n", pw->pw_dir);
		printf("Group =");
		printf(" %s", pw->pw_name);
		int i = 0;
		setgrent();
		while((up=getgrent())!=NULL){
			i=0;
			while(*(up->gr_mem+i)){
				if (strcmp(n,*(up->gr_mem+i))==0){
					printf(" %s", up->gr_name);
				}	
				i++;
			}
		}
		endgrent();
		printf("\n");
	} 
	else printf("Khong tim thay user\n");	
	return 0;
}