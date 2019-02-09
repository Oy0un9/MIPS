#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>
void do_system(int code,char *cmd)
{
    char buf[255];
    //sleep(1);
    system(cmd);
}

void main()
{
    char buf[256]={0};
    char ch;
    int count = 0;
    unsigned int fileLen = 0;
    struct stat fileData;
    FILE *fp;
   
    if(0 == stat("passwd",&fileData))
        fileLen = fileData.st_size;
    else
        return 1;

    if((fp = fopen("passwd","rb")) == NULL)
    {
        printf("Cannot open file passwd!n");
        exit(1);
    }    
    ch=fgetc(fp);
    
    while(count <= fileLen)
    {
        buf[count++] = ch;
        ch = fgetc(fp);
    }
    buf[--count] = '\x00';
    
    if(!strcmp(buf,"adminpwd\n"))
    {        
        do_system(count,"ls -l");
    }
    else
    {
        printf("you have an invalid password!\n");
    }
    fclose(fp);
}
