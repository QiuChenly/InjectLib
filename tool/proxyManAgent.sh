
echo "准备自动计算Helper偏移参数..."

cp ./tool/proxyman_o.sh ./tool/proxyman.sh

chmod +x ./tool/QAQ_GenshineImpactStarter

./tool/QAQ_GenshineImpactStarter proxyman

sh ./tool/proxyman.sh

rm ./tool/proxyman.sh