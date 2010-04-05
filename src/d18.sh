#!/bin/sh
# sets up ssh configuration for development server(s)
# example
# $ sh d18.sh username@192.168.0.200

[ $# = 0 ] && exit 1

ssh_dir=$HOME/.ssh
tmpfile=/tmp/`basename $0`.tmp
rm -f $tmpfile

for server in $*
do
    (echo $server |grep "@" >/dev/null) ||
      (echo "[ERROR] server name must be 'user@host', '$server'" 1>&2; exit 1) ||
      continue
    user=`echo $server | cut -d"@" -f1`
    host=`echo $server | cut -d"@" -f2`
    [ -z "$user" ] && echo "user is empty, '$server'" && continue
    [ -z "$host" ] && echo "host is empty, '$server'" && continue
    echo "[INFO] host: $host, user: $user"
    key=$host.key
    [ -f $ssh_dir/$key ] && echo "key is exists at $ssh_dir/$key." && continue
    ssh -l $user $host "ssh-keygen -t rsa && cd .ssh && \
            cat id_rsa.pub >>authorized_keys && chmod 600 authorized_keys"
    # connection failure returns 255
    [ $? = 255 ] && continue
    echo "generated ssh key file and pull it to local machine."
    scp $user@$host:.ssh/id_rsa $ssh_dir/$key
    cat <<EOT >>$tmpfile
HOST $host
    HostName $host
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

