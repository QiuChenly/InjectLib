echo "准备自动计算Helper偏移参数..."

cp ./tool/cmm_o.sh ./tool/cmm.sh

chmod +x ./tool/GenShineImpactStarter

./tool/GenShineImpactStarter cmmx

sh ./tool/cmm.sh
