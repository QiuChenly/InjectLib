echo "准备自动计算Helper偏移参数..."
cp ./tool/aldente_x.sh ./tool/aldente.sh
chmod +x ./tool/QAQ_GenshineImpactStarter
./tool/QAQ_GenshineImpactStarter aldente
sh ./tool/aldente.sh
rm ./tool/aldente.sh