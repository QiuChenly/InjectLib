cp '/Applications/Adobe Lightroom Classic/Adobe Lightroom Classic.app/Contents/MacOS/Adobe Lightroom Classic' /tmp/lrc
sudo codesign -fs - /tmp/lrc
cp /tmp/lrc '/Applications/Adobe Lightroom Classic/Adobe Lightroom Classic.app/Contents/MacOS/Adobe Lightroom Classic'
rm -rf /tmp/lrc