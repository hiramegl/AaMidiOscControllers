#!/usr/bin/ruby

puts('> Looking for local address')
loop do
  puts('  polling ...')
  sIfConfig = `ifconfig`
  break if sIfConfig =~ /inet (169\.254.\d+\.\d+?) /
  sleep(1) # sleep 1 sec and poll again
end
sMacAddr = $1

puts("\n> Looking for raspberry-pi address")
loop do
  puts('  polling ...')
  sTraceRt = `traceroute raspberrypi.local 2>&1`
  break if sTraceRt =~ /(169.254.\d+\.\d+)/
  sleep(1) # sleep 1 sec and poll again
end
sPiAddr = $1

puts("\n> Done looking for addresses:")
puts("  MacAddr: '#{sMacAddr}'")
puts("  Pi Addr: '#{sPiAddr}'")

sMacFile = 'mac_addr.txt'
sPiFile  = 'pi_addr.txt'
sMacPath = "/Users/hiram/AaConfig/#{sMacFile}"
sPiPath  = "/Users/hiram/AaConfig/#{sPiFile}"
puts("\n> Writing address-files in macbook ...")
File.open(sMacPath, 'wt') { |oFile| oFile.print(sMacAddr) }
File.open(sPiPath,  'wt') { |oFile| oFile.print(sPiAddr) }

sSsh = 'ssh hiram@raspberrypi.local'
puts("\n> Removing address-files in raspberry pi ...")
`#{sSsh} 'rm -f #{sMacFile}'`
`#{sSsh} 'rm -f #{sPiFile}'`

puts("\n> Writing address-files in raspberry pi ...")
`cat #{sMacPath} | #{sSsh} 'cat >> #{sMacFile}'`
`cat #{sPiPath } | #{sSsh} 'cat >> #{sPiFile}'`

puts("\n> Starting bridge scripts ...")
spawn("#{sSsh} './bcf.sh &' &")
spawn("#{sSsh} './bcr.sh &' &")
spawn("#{sSsh} './wfd.sh &' &")
spawn("#{sSsh} 'pwd' &")

puts("\n> Done")

=begin
**************************
   SSH WITHOUT PASSWORD
**************************

1) GENERATING A KEY IN THE LOCAL COMPUTER.
   IN THE DEVICE FROM WHERE YOU WANT TO REACH THE SERVER (THE MACBOOK/LAPTOP) --------------------------------

NOTE: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Do not enter a passphrase when asked to !!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

a@A:~> ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/a/.ssh/id_rsa): 
Created directory '/home/a/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/a/.ssh/id_rsa.
Your public key has been saved in /home/a/.ssh/id_rsa.pub.
The key fingerprint is:

2) (OPTIONAL STEP IN CASE ~/.ssh FOLDER DOES NOT EXIST IN THE SERVER) ----------------------------------------
Now use ssh to create a directory ~/.ssh as user b on B. (The directory may already exist, which is fine):

a@A:~> ssh b@B mkdir -p .ssh
b@B's password: 

3) ADDING THE KEY IN THE SERVER (WHERE WE WANT TO CONNECT WITHOUT PASSWORD)
   APPEND PUBLIC KEY (COULD BE DONE BY SENDING THE TEXT FROM THE DEVICE YOU WANT TO CONNECT ------------------
   TO A DEVICE THAT ALREADY HAS ACCESS AND COPY PASTE THE PUBLIC KEY -----------------------------------------
Finally append a's new public key to b@B:.ssh/authorized_keys and enter b's password one last time:

a@A:~> cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
b@B's password: 

--------------------------------------------------------------------------------------------------------------
From now on you can log into B as b from A as a without password:

a@A:~> ssh b@B

=end

