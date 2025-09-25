Series 2.0.3 Vi and Linux Exam Commands.md
******************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

# Useful Exam Cmds

    # Aliases
    alias k=kubectl

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage
    cat pod.yaml                                                                # output file

# Commonly Used in CKA Exam

      # Vi Exam Essentials (Learn by Heart)
      Ctrl+R: Recall the last command matching the characters you provide. Press Enter to execute cmd!
      Ctrl+R (again): Navigate through the matching commands
      Ctrl+D to leave current search history with no execute
      
      Use / to search forward in a file for text string
      Use ? to search backwards in a file for text string
      Type n to go to the next occurrence of the string
      Type N to go to the previous occurrence
      
      Toggle Line numbers On/Off :set number!
      Find line by number :<LINE_NUMBER>
      Move to beginning of file: gg
      Move to line 3: 3G
      Move to last line: G
      Move to the end of the file: $ (also Shift+G could work)
      Copy (yank,cut) current line: yy
      Copy (yank,cut) next N lines: Nyy
      Paste line: p
      Delete current line: dd
      Delete next N lines: Ndd
      Remove all lines after: dG
      To Undo: u

      # Useful Linux Shortcuts for Exam
      cd                                        # go back to previous folder
      ls                                        # list files
      pwd                                       # print working dir
      mkdir <folder>                            # make folder
      cd <folder>                               # change to there
      cd /                                      # to root file system
      cd ..                                     # return to previous
      cd -                                      # go back to previous folder
      cd                                        # return to home folder
      cd ~                                      # return to users home folder
      touch                                     # create file
      vi or nano                                # modify file
      cat <file name>                           # view file contents
      cp <file>                                 # copy file (leaves original)
      mv <file>                                 # move file
      rm <file>                                 # remove file
      rmdir <folder>                            # if folder empty
      rm -r <folder>                            # if folder has contents
      clear                                     # clear terminal (also Ctrl+L works)
      Ctrl+U                                    # remove all characters from current terminal quickly
      Ctrl+A                                    # Move to start of terminal line
      Ctrl+E                                    # Move to end of terminal line
      Ctrl+D                                    # Log current user out of session
 
      ls -1                                     # list file names only
      ls -R                                     # list all files in the sub-directories as well
      ls -a                                     # show hidden files
      ls -al                                    # list files and directories with detailed information

      sudo !!                                   # re-run the last command as root
      sudo -i                                   # log in as root
 
      wc -l core.txt                            # count lines in file. Alternatives: -w (words) or -c (characters)s

      head <file>                               # see start of file
      head -n 5 filename.ext                    # if you only want to show the first five lines (10 is default)
      tail <file>                               # see end of file
      tail filename.txt                         # default tails the last 10 lines
      tail -n 20 filename.txt                   # show the last 20 lines

      man ls                                    # show man page for ls command
      man cat                                   # show man page for cat command

      history                                   # show history
      ! nan                                     # re-run nano command from history
      ! 134                                     # line number also works!

      cat > filename creates a new file
      cat filename1 filename2>filename3         # joins two files (1 and 2) and stores the output of them in a new file 
      cat filename | tr a-z A-Z >output.txt     # to convert a file to upper or lower case use
      
      uptime                                    # show uptime of system
      df -h                                     # show disk usage in readable format
      du -sh /var/log/*                         # show how much space is being used for files

      # Background and Foreground Processes
      Hit CTRL + Z shortcut to put it to the background and carry on working
      Show Background Processes: jobs -l
      Send Background Processes to the Foreground: fg %2 (sends Job ID 2 for the Foreground)
      
      # Make curly brackets on MAC: Alt Gr + Shift + [ OR ]
      Inside Vim Tip: Use e in vim to switch between files!
      Inside Vim Tip: Use :!kubectl to apply a kubectl command quicker!

# More Advanced Linux Commands
## (Not Required for Exam but When Working on Solutions)

      whoami
      useradd tom
      sudo useradd tom
      su tom
      exit
      sudo apt update
      sudo apt install <finger>
      >whatis finger
      whereis finger
      cmp <file1> <file2>                             # compare 2 files
      diff <file1> <file2>                            # compare 2 files to see real differences
      cat <file1> | sort                              # cat and sort

      wall hello                                      # broadcast message to all logged in users
      who                                             # show loggedin users
      free                                            # show all systems resources
      sort sort.txt                                   # sort by ascending order
      sort -r sort.txt                                # sort by descending order
      shutdown -h +10                                 # shutdown machine in 10mins
      shutdown -r now                                 # shutdown machine now
      man "name of the command"                       # show the manual of the command
      whatis  ls                                      # one line description of the command ls (works with others)

      password/shadow files                           # for storing users and passwords
      echo "not going to be in the history"           # add a leading space to not enter in the history
      journelctl -fu nginx                            # get logging of nginx process
      cron job                                        # automate the execution of a daily script

      ## Files Management
      find / -name "thebible"
      find . -type f -name ".*"
      find . -type f -empty
      find . -perm /a=x 							                       # all executable files

      find /testfolder -type f -printf '%TY-%Tm-%Td %TT %pn' | sort -r
      find /testfolder -newermt "2 day ago" -ls       # find 2 days ago
      find /testfolder -mtime 0                       # find in last 24 hours
      find /testfolder/*.sh -newermt "1 day ago" -ls  # find last modified of .sh file

      NOTE: An inode is a data structure on a traditional Unix-style file system such as ext3 or ext4. storing the properties of a file and directories.       Linux extended filesystems such as ext3 or ext4 maintain an array of these inodes called the inode table.
      Can be an weird issues if plenty of disk space but not enough inodes to create a new file!

      mkdir ram                                       # Create super fast ram disk example (for performance!)
      cd ram/
      dd if=/dev/zero of=test.iso bs=1M count=8000    # took 44 seconds at 189MB/s
      rm test.iso
      cd ..
      mount -t tmpfs tmpfs /testfolder/ram -o size=8192M     # create super fast ram disk!
      cd ram/
      dd if=/dev/zero of=test.iso bs=1M count=8000    # took 2.5 seconds at 3.2 GB/s

      cat > file.txt                                  # write out to file
      cat << EOF > file.txt (ENTER)                   # write lines to the file (type EOF to end)
      tar -zcvf archive-name.tar.gz directory-name    # compress a whole directory
      ls -lht | head -5 					# list top 5 last modified files in the folder
      sed -e "/^#/d" /etc/squid/squid.conf | awk NF   # dont show lines that start with # char

      locate 							# just like the search command in Windows (-i argument along with this command will make it case-insensitive)
      locate -i school*note 					# search for any file that contains the word “school” and “note”, whether it is uppercase or lowercase

      find . -name core.txt 					# find files in the current directory use
      find . -type f -name "core.txt"			# find the file
      find . -type f -name "core.txt" -exec ls {} \;	# find the file AND run some execution on it e.g. -exec rm -f {} \;
      find . -type f -name "core.txt" -exec rm -i {} \; # interactive mode to prompt IF file should be deleted

      find /var/log -type f -maxdepth 1			# find all log files from 1 level down
      find /var/log -type f -maxdepth 2 | grep syslog # find all log files from 2 levels down, and then find syslog only
      find . -type d -name salt -exec ls {} \;		# find folder called salt
      find . -type f -name ~/.bashrc			# find the bachrc file
      find . -type f -newermt "2020-06-16 11:55:00" ! -newermt "2020-06-16 14:20:00" -exec grep "Read timed out" {} \; | wc -l

      find /logs/mylogs -name "*-LOG" -type f -mtime +1 -exec gzip {} \;      # Zip logs which are older than days
      find /logs/mylogs -name "*-LOG.gz" -type f -mtime +30 -delete;          # Delete zipped logs which are older than days
      find /logs/mylogs -type d -empty -delete                                # After deleting old zip files, there might be empty directories. So Find and delete empty directories recursively
 
# System Management

      cd /sys (the sysfs)                             # all the knobs and switches for Linux
      cd /proc                                        # find information about processes in there (virtual file systems)
      cat /proc/meminfo                               # example: get information about memory

      /proc/cmdline – Kernel command line information.
      /proc/console – Information about current consoles including tty.
      /proc/devices – Device drivers currently configured for the running kernel.
      /proc/dma – Info about current DMA channels.
      /proc/fb – Framebuffer devices.
      /proc/filesystems – Current filesystems supported by the kernel.
      /proc/iomem – Current system memory map for devices.
      /proc/ioports – Registered port regions for input output communication with device.
      /proc/loadavg – System load average.
      /proc/locks – Files currently locked by kernel.
      /proc/meminfo – Info about system memory (see above example).
      /proc/misc – Miscellaneous drivers registered for miscellaneous major device.
      /proc/modules – Currently loaded kernel modules.
      /proc/mounts – List of all mounts in use by system.
      /proc/partitions – Detailed info about partitions available to the system.
      /proc/pci – Information about every PCI device.
      /proc/stat – Record or various statistics kept from last reboot.
      /proc/swap – Information about swap space.
      /proc/uptime – Uptime information (in seconds).
      /proc/version – Kernel version, gcc version, and Linux distribution installed.
      NOTE: Above taken from: https://www.tecmint.com/exploring-proc-file-system-in-linux/

      netstat -tn 2>/dev/null | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head	# SHOWS FOREIGN IPs connected to the system
      sudo dd if=/dev/zero of=/backup/myfile bs=1M count=5    # create a dummy 5MB file for testing
      
      yum install httpd                                     # install tomcat
      systemctl start httpd
      systemctl enable httpd
      system status httpd
      
      sudo apt install zip                                  # install zip
      
      sudo chattr +i testfile.txt 					# set the immutable flag so cant delete file!
      sudo lsattr testfile.txt				
      chmod +t /graphics_folder    					# only allow the owners group to delete
      SGID									# new files get group associates
      px -xl                                                # list processes on the system (including nice priority)

      nice -n 15 pico myfile                                # modify the process BEFORE process starts
      renice +1 -p 5554                                     # modify the RUNNING process to be +1 (or use renice 10 -p 5554)
      NOTE: Niceness values range from -20 (most favorable to the process) to 19 (least favorable to the process)

      sudo ln -s /Packages /var/www/html/packages           # create a symbolic link to the apache website location
      sudo shread -v --iterations=1 /dev/backup             # shread and destroy the backup location

      ls -l /dev/mapper | grep databk                       # grep for the databk

      rpm -qi ksh                                           # query the information
      rpm -ql ksh                                           # list the files of the package
      rpm -qa ksh                                           # verify the new package is installed

      sudo shred -v --iterations=1 /dev/backup              # shred to destroy the data on a location

      base64 /dev/urandom | head -c 10000000 - printfile.txt  # create a base64 test file for printing
  
# Troubleshooting & Investigation

      man pages, stackoverflow, google                # for troubleshooting issues
      top or htop command                             # see resource usage
      lsof                                            # explore which sockets are open

      netstat -tulnp | grep 80                        # get processes running on port 80
      ss -tunapl | egrep "(ESTAB|LISTEN)"             # see what the process is binding too (ss is newer version!)
      e.g. tcp    LISTEN     0      1      127.0.0.1:8005                  *:*                   users:(("java",pid=654,fd=71))

      ps aux | grep -i 654                            # get running process by pid (process id)
      ls -alh myfile.txt                              # listen ownership and permissions of file

      # File Upload & Download
      scp test.txt myuser@my-host.com:/tmp            # upload file to the box
  
# Linux Folder and Files Permissions (Absolute mode)

      e.g. chmod 775 testfile.txt
      --------------------------------------------------------------------------
      Each number has meaning in permission. Do not give full permission of 777.
      N   Description                      		ls   		binary    
      0   No permissions at all            		---  		000
      1   Only execute                     		--x  		001
      2   Only write                       		-w-  		010
      3   Write and execute                		-wx  		011
      4   Only read                        		r--  		100
      5   Read and execute                 		r-x  		101
      6   Read and write                   		rw-  		110
      7   Read, write, and execute         		rwx  		111

# Linux Folder and Files Permissions (Symbolic Mode)

      e.g. chmod g=rwx file (assigns read, write, and execute permissions to group)
      -----------------------------------------------------------------------------
      u Who User (owner) 
      g Who Group 
      o Who Others 
      a Who All 
      = Operation Assign 
      + Operation Add 
      - Operation Remove 
      r Permission Read 
      w Permission Write 
      x Permission Execute 
      l Permission Mandatory locking, setgid bit is on, group execution bit is off
      s Permission setuid or setgid bit is on
      S Permission suid bit is on, user execution bit is off
      t Permission Sticky bit is on, execution bit for others is on 
      T Permission Sticky bit is on, execution bit for others is off 
      
      chmod +x <file>                                 # make file executable
      chown austin <file>                             # change owner to be austin
      chown ubuntu:ubuntu myfile.txt                  # change group and owner of the file
      chmod 600 myfile.txt                        

      chroot                                          # create a test environment or jailed (isolated) enviornment

# Linux & Networking

      curl <server or IP>                             # check curl is working
      
      wget                                            # download file
      curl                                            # hit a URL
      zip                                             # zip a large
      unzip <file>                                    # unzip a file
      
      ip config                                       # install with sudo apt install net-tools
      ip address
      ip address | grep eth0
      ip address | grep eth0 | grep inet | awk '{print $2}'

      wget -qO- --timeout=2 10.68.1.24:8080       # <webpod IP> should work!
      wget -qO- --timeout=2 10.68.1.25:8080       # <storagepod IP> should work!
      wget -qO- --timeout=2 10.68.1.26:8080       # <shouldnotworkpod IP> should work!

      Could also try netcat just for testing!
      nc -z -v 10.68.1.14 8080                    # netcat to <webpod IP> should show open!
      nc -z -v -w 1 10.68.1.14 8080               # netcat with timeout

      ip addr show dev eth0                       # show the primary network inferface
      ip route show                               # show default route/gateway
      init.d                                      # first process that linux starts
                                                  # starts all of the services, units and parenting orphan processes

      ssh tunnel using port forwarding -L or proxy socks -D               # access web service running on server B

      ssh -L 3337:127.0.0.1:6379 root@emkc.org -N     # tunnel with ssh (local port 3337 -> remote IP on port 6379)

      NOTE:
      An Layer 4 load balancer works at the transport layer, using the TCP and UDP protocols to manage transaction traffic based on a simple load balancing algorithm and basic information such as server connections and response times. 
      An Layer 7 load balancer works at the application layer—the highest layer in the OSI model—and makes its routing decisions based on more detailed information such as the characteristics of the HTTP/HTTPS header, message content, URL type, and cookie data. An L4-7 load balancer manages traffic based on a set of network services across ISO layers 4 through 7 that provide data storage, manipulation, and communication services.

# Security

      vi /etc/ssh/sshd_config                      # disable root login for entire operating system
      PermitRootLogin no
      
# Vi Editor Commands
## (Most Say Not Required Now But Still Good for Working Solutions Practice)

      # We will use visual line mode
      Step 1: Move your cursor to the top line of the block of text/code to remove.
      Step 2: Press V (Shift + v) to enter the Visual mode in Vim/Vi.
      Step 3: Now move your cursor down to the bottom of the block of text/code to remove
      Step 4: Press 3d to delete the block selected.
      You can also use the gv command to rehighlight the same block again.

      # Vi How to Indent/Detent Spec Files
      :set shiftwidth=2
      Place cursor to start of line
      Press Shift V to go to Visual Line mode
      Press Up or Down to select the lines
      Press Shift . to Indent to the right
      Press Shift , to Indent to the Left

      # Vi Configure for tabstop and expandtab
      vi ~/.vimrc
      then add these two lines to the file
      set tabstop=2
      set expandtab # use spaces for tabs

      # Vi Configure for :retab
      In situations where an errant tab makes its way into your yaml file, use :retab, which replaces all tab sequences with new strings of white-space using the tabstop value.

      # Vi Configure for :set paste
      Use to keep the formatting in yaml after paste

      # Worth watching by jedi.ascode() - Please subscribe to him too!
      https://www.youtube.com/watch?v=8VK9NJ3pObU
