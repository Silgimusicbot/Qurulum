Userator+="\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝"
MESAJ+="\n "
MESAJ+="\n✅Kanal: @SilgiUbPlugin"
MESAJ+="\n✅Qrup: @silgiuserbot"
MESAJ+="\n "
KOMEK+="\n "
BOSLUQ="\n "
clear
echo -e $BOSLUQ
echo -e $BOSLUQ
pkg update -y && pkg upgrade
clear
echo -e $BOSLUQ
apt upgrade -y
echo -e $BOSLUQ
echo -e $MESAJ
echo -e $BOSLUQ
echo "Python ✅"
echo -e $BOSLUK
pkg install python3
pip3 install --upgrade pip
clear
echo -e $MESAJ
echo -e $BOSLUQ
echo "Git ✅"
echo -e $BOSLUQ
pkg install git -y
clear
echo -e $MESAJ
echo -e $BOSLUQ
echo "Telethon ✅"
echo -e $BOSLUQ
pip install telethon
clear
echo -e $MESAJ
echo -e $BOSLUQ
echo "Repo ✅"
echo -e $BOSLUQ
rm -rf Qurulum
git clone https://github.com/Silgimusicbot/Qurulum
clear
echo -e $BOSLUQ
echo -e $MESAJ
echo -e $BOSLUQ
echo -e $BOSLUQ
cd Qurulum
pip install -r requirements.txt
python3 -m up_qurulum
