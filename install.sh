#!/bin/bash
# ============================================================
#   RoV Skin Mod Maker - One-Click Installer for Termux
# ============================================================

echo "============================================================"
echo "    🚀 กำลังติดตั้งตัวย่อคำสั่ง 'rov' ใน Termux..."
echo "============================================================"

# อัปเดตแพ็กเกจที่จำเป็น
pkg update -y && pkg install python git curl -y 2>/dev/null || apt-get update -y && apt-get install python3 curl -y 2>/dev/null

# ขอสิทธิ์เข้าถึงพื้นที่จัดเก็บข้อมูลของ Android (ถ้ายังไม่เคยขอ)
if command -v termux-setup-storage >/dev/null 2>&1; then
    termux-setup-storage
fi

# โฟลเดอร์เก็บสคริปต์
INSTALL_DIR="$HOME/.rov-mod"
mkdir -p "$INSTALL_DIR"
curl -sL https://raw.githubusercontent.com/paxni12345-web/rov-skin-mod-maker/main/rov_skin_mod_maker.py -o "$INSTALL_DIR/rov_skin_mod_maker.py"

# ค้นหาตำแหน่ง bin เพื่อสร้างคำสั่ง 'rov'
BIN_PATH=""
if [ -d "$PREFIX/bin" ]; then
    BIN_PATH="$PREFIX/bin/rov"
elif [ -d "/data/data/com.termux/files/usr/bin" ]; then
    BIN_PATH="/data/data/com.termux/files/usr/bin/rov"
else
    BIN_PATH="/usr/local/bin/rov"
fi

cat << 'EOF' > "$BIN_PATH"
#!/bin/bash
python "$HOME/.rov-mod/rov_skin_mod_maker.py" 2>/dev/null || python3 "$HOME/.rov-mod/rov_skin_mod_maker.py"
EOF

chmod +x "$BIN_PATH"

echo ""
echo "============================================================"
echo "🎉 ติดตั้งสำเร็จเรียบร้อยแล้ว!"
echo "👉 ต่อไปนี้เวลาจะใช้ แค่พิมพ์คำสั้นๆ ว่า:"
echo ""
echo "           rov"
echo ""
echo "   แล้วกด Enter ได้ทันทีเลยครับ ไม่ต้องพิมพ์คำสั่งยาวๆ อีกแล้ว!"
echo "============================================================"
