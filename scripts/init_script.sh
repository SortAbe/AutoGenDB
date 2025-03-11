#!/bin/bash

cd /root || exit 1
wget https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb && echo "wget done" >> /root/event_log
add-apt-repository ppa:deadsnakes/ppa -y && echo "repo add done" >> /root/event_log
apt update && echo "update done" >> /root/event_log
apt install python3.11 -y && echo "3.11 done" >> /root/event_log
apt install python3.11-distutils -y && echo "utils done" >> /root/event_log
apt install python3-pip -y && echo "pip done" >> /root/event_log
apt upgrade -y && echo "upgrade done" >> /root/event_log
python3.11 -m pip install mysql-connector-python && echo "connector done" >> /root/event_log
git clone https://github.com/sortabe/autogendb && echo "git done" >> /root/event_log

cat << EOF > /root/finish.sh
#!/bin/bash
dpkg -i /root/mysql-apt-config_0.8.33-1_all.deb
apt install mysql-server -y
cd /root/autogendb || exit 1
mysql -e "CREATE USER 'py'@'localhost' IDENTIFIED BY 'xKHOxyThyC7u8f';"
mysql -e "CREATE DATABASE IF NOT EXISTS university;"
mysql -e "GRANT ALL PRIVILEGES ON university.* TO 'py'@'localhost';"
{
    cat /root/autogendb/sql/schema.sql
    cat /root/autogendb/sql/department.sql
    cat /root/autogendb/sql/course.sql
    cat /root/autogendb/sql/addr.sql
    cat /root/autogendb/sql/female.sql
    cat /root/autogendb/sql/male.sql
    cat /root/autogendb/sql/last.sql
    echo 'COMMIT'
} >> /root/autogendb/sql/complete.sql
mysql -u py -h localhost -pxKHOxyThyC7u8f < /root/autogendb/sql/complete.sql
rm -f /root/autogendb/sql/complete.sql
EOF
chmod +x /root/finish.sh

cat << EOF > /root/.vimrc
set number relativenumber
set showcmd
set spell
syntax on

set ignorecase
set smartcase
set incsearch
set hlsearch

set autoindent
set smartindent
set virtualedit=onemore
set noexpandtab
set tabstop=4
set shiftwidth=4

set backspace=indent,eol,start
set foldmethod=manual
set paste

set undofile
set undodir=~/.vim/undo/

hi VertSplit cterm=NONE
hi Search ctermfg=black ctermbg=33
hi StatusLine ctermfg=black ctermbg=green
hi StatusLineNC ctermfg=black ctermbg=red
hi Visual ctermfg=NONE ctermbg=8
hi clear SpellBad
hi SpellBad cterm=underline gui=underline
EOF
