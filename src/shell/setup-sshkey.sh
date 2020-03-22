#!/bin/sh
# Sets up ssh configuration for development server(s)

if [ $# = 0 ]
then
    echo Usage: $0 username@host
    exit 1
fi

ssh_dir=$HOME/.ssh
tmpfile=/tmp/`basename $0`.tmp
rm -f $tmpfile

for server in $*
do
    (echo $server |grep "@" >/dev/null) ||
      (echo "[ERROR] server name must be 'user@host', '$server'" 1>&2; exit 1) ||
      continue
    user=`echo $server |cut -d"@" -f1`
    hostport=`echo $server |cut -d"@" -f2`
    port=`echo $hostport |cut -d":" -s -f2`
    if [ -z $port ]
    then
        host=$hostport
        port=22
        key=$host.key
    else
        host=`echo $hostport |cut -d":" -f1`
        key=$host.$port.key
    fi
    [ -z "$user" ] && echo "user is empty, '$server'" && continue
    [ -z "$host" ] && echo "host is empty, '$server'" && continue
    echo "[INFO] host: $host, port: $port, user: $user, key: $key"
    [ -f $ssh_dir/$key ] && echo "key is exists at $ssh_dir/$key." && continue
    ssh -l $user -p $port $host "ssh-keygen -t rsa && cd .ssh && \
            cat id_rsa.pub >>authorized_keys && \
            chmod 600 authorized_keys && \
            cat id_rsa" >$ssh_dir/$key
    chmod 600 $ssh_dir/$key
    # connection failure returns 255
    [ $? = 255 ] && continue
    cat <<EOT >>$tmpfile
HOST $host
    HostName $host
    Port $port
    User $user
    IdentityFile $ssh_dir/$key
EOT
done

cat <<EOT
*****************************************************************
Use 'ssh-agent' and 'ssh-add' to register your ssh key(s).
Check \$SSH_AUTH_SOCK and \$SSH_AGENT_PID to avoid multiple agents.
*****************************************************************
EOT
if [ -e $tmpfile ]
then
    echo "Append this block on your config file: $ssh_dir/config"
    echo "Edit 'Host' name on your own to use with ssh command."
    cat $tmpfile && rm -f $tmpfile
fi

