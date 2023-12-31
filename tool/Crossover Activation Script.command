#!/bin/zsh

clear
cd ~/Library/Preferences/

echo -e "\e[36mGenerating Licence.....\e[0m"

openssl genrsa -out temp.pem 2048 >> /dev/null 2>&1
openssl rsa -in temp.pem -outform PEM -pubout -out public.pem >> /dev/null 2>&1
mv public.pem /Applications/CrossOver.app/Contents/SharedSupport/CrossOver/share/crossover/data/tie.pub
echo "[crossmac]\ncustomer=iAnon\nemail=iAnon@ianon.com\nexpires=2999/10/26\n[license]\nid=iAnonIsVeryNice" > com.codeweavers.CrossOver.license
openssl dgst -sha1 -sign temp.pem -out com.codeweavers.CrossOver.sig com.codeweavers.CrossOver.license 
rm temp.pem

echo -e "\e[32mSuccessfully activated, enjoy!\e[0m"

exit 0