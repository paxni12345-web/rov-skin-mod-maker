#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
       RoV Skin Mod Generator (Auto Skin Swapper)
============================================================
เครื่องมือสำหรับสร้างไฟล์มอดสกิน RoV (Full Set) สลับเป็นร่างต้น
- รหัสฮีโร่ตรงตามไฟล์ระบบจริง 100%
- รองรับทั้งโฟลเดอร์ Resources และ Extra (ที่เก็บสกินจริงของ RoV 1.64)
- จัดโครงสร้าง Zip เริ่มต้นที่โฟลเดอร์ 'files' เพื่อให้ก๊อปปี้ไปวางใน com.garena.game.kgth ได้ง่ายและตรงเป๊ะ 100%
============================================================
"""

import os
import sys
import shutil
import zipfile
import re

PKG_NAME = "com.garena.game.kgth"

SEARCH_BASE_DIRS = [
    "/sdcard/Download",
    "/storage/emulated/0/Download",
    f"/sdcard/Android/data/{PKG_NAME}/files",
    f"/storage/emulated/0/Android/data/{PKG_NAME}/files",
    "./Download",
    ".",
]

ID_TO_HERO = {
    "150": "Nakroth (นาครอส)",
    "141": "Lauriel (ลอเรียล)",
    "521": "Florentino (ฟลอเรนติโน่)",
    "510": "Liliana (ลิเลียน่า)",
    "548": "Allain (อลัน / Sun Ce)",
    "501": "Tel'Annas (เทลอันนาส)",
    "132": "Hayate (ฮายาเตะ)",
    "196": "Elsu (เอลสุ)",
    "167": "Wukong (วูคอง / ลิง)",
    "131": "Murad (มูราด)",
    "130": "Airi (ไอริ)",
    "111": "Violet (ไวโอเล็ต)",
    "112": "Yorn (ยอร์น)",
    "116": "Butterfly (บัตเตอร์ฟลาย)",
    "106": "Valhein (แวน)",
    "107": "Zhao Yun (จูล่ง)",
    "108": "Krixi (คริกซี่)",
    "109": "Veera (วีร่า)",
    "113": "Chaugnar (ช้าง)",
    "114": "Omega (โอเมก้า)",
    "115": "Jinna (จินนา)",
    "117": "Ormarr (ออร์มาร์)",
    "118": "Alice (อลิซ)",
    "119": "Mganga (มังกังก้า)",
    "120": "Mina (มีน่า)",
    "121": "Marja (มาร์จา)",
    "123": "Lu Bu (ลิโป้)",
    "124": "Ignis (อิกนิส)",
    "126": "Arthur (อาร์เธอร์)",
    "127": "Diao Chan (เตียวเสี้ยน)",
    "128": "Maloch (มาลอค)",
    "129": "Zanis (ซานิส)",
    "135": "Thane (เธน)",
    "136": "Ilumia (อิลูเมีย)",
    "137": "Paine (เพน)",
    "139": "Omen (โอเมน)",
    "140": "Superman (ซูเปอร์แมน)",
    "142": "Helen (เฮเลน)",
    "144": "Taara (ทาร่า)",
    "146": "Astrid (แอสทริด)",
    "180": "Nezha (เนจา)",
    "190": "Tulen (ทูเลน)",
    "502": "Astrid (แอสทริด)",
    "503": "Zuka (ซูก้า)",
    "504": "Wonder Woman (วันเดอร์ วูแมน)",
    "505": "Baldum (บัลดัม)",
    "508": "Zata (ซาต้า)",
    "512": "Rourke (รูร์ก)",
    "514": "Roxie (ร็อกซี่)",
    "515": "Richter (ริกเตอร์)",
    "518": "Quillen (ควิลเลน)",
    "519": "Annette (แอนเน็ต)",
    "520": "Veres (เวเรส)",
    "522": "Errol (เออร์รอล)",
    "523": "D'Arcy (ดาร์ซี่)",
    "524": "Capheny (คาเฟนี่)",
    "527": "Sephera (เซฟิร่า)",
    "529": "Volkath (โวลคาท)",
    "530": "Dirak (ดิแรก)",
    "531": "Keera (คีร่า)",
    "538": "Iggy (อิกกี้)",
    "540": "Bright (ไบรท์)",
    "541": "Bonnie (บอนนี่)",
    "542": "Tachi (ทาชิ)",
    "544": "Yan (ยัน)",
    "547": "Charlotte (ชาร์ล็อตต์)",
    "550": "Dolia (โดเลีย)",
}

NAME_ALIAS = {
    "nakroth": "150", "นาครอส": "150", "นาคอส": "150",
    "lauriel": "141", "ลอเรียล": "141", "ลอเรล": "141",
    "florentino": "521", "ฟลอเรน": "521", "ฟลอเรนติโน่": "521",
    "liliana": "510", "ลิเลียน่า": "510", "ลิลี่": "510",
    "allain": "548", "อลัน": "548", "อาแล็ง": "548",
    "hayate": "132", "ฮายาเตะ": "132",
    "elsu": "196", "เอลสุ": "196",
    "wukong": "167", "วูคอง": "167", "ลิง": "167",
    "murad": "131", "มูราด": "131",
    "airi": "130", "ไอริ": "130",
    "violet": "111", "ไวโอเล็ต": "111", "ไวโอ": "111",
    "yorn": "112", "ยอร์น": "112",
    "butterfly": "116", "บัต": "116", "บัตเตอร์ฟลาย": "116",
    "valhein": "106", "แวน": "106",
    "tulen": "190", "ทูเลน": "190",
    "thane": "135", "เธน": "135",
}

def banner():
    print("=" * 60)
    print("       🔥 RoV Skin Mod Generator (Auto Skin Swapper) 🔥")
    print("       Full Set: 3D Model, VFX, Sound & 10v10 Mode")
    print("=" * 60)
    print()

def find_game_resource_dirs():
    found_dirs = []
    for base in SEARCH_BASE_DIRS:
        for folder_name in ["Extra", "extra", "Resources", "resources"]:
            target = os.path.join(base, folder_name)
            if os.path.exists(target):
                subdirs = [
                    os.path.join(target, d) for d in os.listdir(target)
                    if os.path.isdir(os.path.join(target, d)) and any(c.isdigit() for c in d)
                ]
                if subdirs:
                    subdirs.sort(key=lambda s: [int(u) for u in re.findall(r'\d+', s)] if re.findall(r'\d+', s) else [0])
                    found_dirs.append(subdirs[-1])
                else:
                    found_dirs.append(target)
    return list(set(found_dirs))

def scan_available_skins(source_dirs, hero_id):
    found_skins = set()
    pat_5d = re.compile(rf"(?:^|[_\-/])(?:Actor_|Hero_|Effect_|Ani_)?{hero_id}0(\d{{1,2}})(?:[_\.\-/]|$)")
    pat_4d = re.compile(rf"(?:^|[_\-/])(?:Actor_|Hero_|Effect_|Ani_)?{hero_id}(\d{{1,2}})(?:[_\.\-/]|$)")
    pat_skin = re.compile(rf"[Ss]kin[_\-]?(\d{{1,2}})")

    for sdir in source_dirs:
        for root, _, files in os.walk(sdir):
            for f in files:
                if f.endswith(".wem"):
                    continue
                for p in [pat_5d, pat_4d, pat_skin]:
                    m = p.search(f)
                    if m:
                        val = int(m.group(1))
                        if 1 <= val <= 35:
                            found_skins.add(val)
    return sorted(list(found_skins))

def is_10v10_file(filepath):
    name_lower = filepath.lower()
    return "10v10" in name_lower or "10_10" in name_lower or "mayhem" in name_lower

def is_sound_file(filepath):
    name_lower = filepath.lower()
    return "sound" in name_lower or "audio" in name_lower or name_lower.endswith(".bnk") or "vo_" in name_lower

def generate_mod(source_dirs, hero_id, target_skin_num, include_10v10=True, include_sound=True):
    hero_name = ID_TO_HERO.get(hero_id, f"Hero_{hero_id}")
    print(f"\n[*] กำลังสกัดไฟล์ของ {hero_name} (ID: {hero_id}) สกินลำดับที่ {target_skin_num}...")

    target_patterns = [
        (f"{hero_id}0{target_skin_num}", f"{hero_id}00"),
        (f"{hero_id}{target_skin_num}", f"{hero_id}0"),
        (f"Skin_{hero_id}0{target_skin_num}", f"Skin_{hero_id}00"),
        (f"Skin_{target_skin_num}", f"Skin_0"),
        (f"skin_{target_skin_num}", f"skin_0"),
        (f"_{hero_id}_{target_skin_num}", f"_{hero_id}_0"),
    ]

    staging_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "staging_mod")
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)

    matched_files = 0
    skipped_10v10 = 0
    skipped_sound = 0

    for sdir in source_dirs:
        is_extra = "extra" in sdir.lower()
        folder_category = "Extra" if is_extra else "Resources"
        version_name = os.path.basename(sdir)

        for root, _, files in os.walk(sdir):
            for f in files:
                file_path = os.path.join(root, f)

                if not include_10v10 and is_10v10_file(file_path):
                    skipped_10v10 += 1
                    continue

                if not include_sound and is_sound_file(file_path):
                    skipped_sound += 1
                    continue

                new_filename = None
                for pattern, default_pattern in target_patterns:
                    if pattern in f:
                        new_filename = f.replace(pattern, default_pattern)
                        break

                if new_filename:
                    rel_dir = os.path.relpath(root, sdir)
                    dest_dir = os.path.join(staging_dir, "files", folder_category, version_name, rel_dir)
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.copy2(file_path, os.path.join(dest_dir, new_filename))
                    matched_files += 1

    if matched_files == 0:
        print(f"\n❌ ไม่พบไฟล์ของสกินที่ {target_skin_num} สำหรับ {hero_name}")
        print("💡 สาเหตุหลัก:")
        print("   ไฟล์โมเดลสกินของ RoV อยู่ในโฟลเดอร์ 'Extra'")
        print("   กรุณาใช้ ZArchiver เข้าไปที่ Android/data/com.garena.game.kgth/files/ แล้วก๊อปปี้โฟลเดอร์ 'Extra' มาไว้ใน Download ด้วยนะครับ")
        return None

    print(f"\n[✓] รวมไฟล์มอดสำเร็จทั้งหมด: {matched_files} ไฟล์")

    zip_output_dir = "/storage/emulated/0/Download"
    if not os.path.exists(zip_output_dir):
        zip_output_dir = "/sdcard/Download"
    if not os.path.exists(zip_output_dir):
        zip_output_dir = os.path.dirname(os.path.abspath(__file__))

    mode_suffix = "Full_10v10" if include_10v10 else "Normal_No10v10"
    safe_name = hero_name.split()[0].replace('/', '_')
    zip_name = f"Mod_{safe_name}_Skin_{target_skin_num}_{mode_suffix}.zip"
    zip_full_path = os.path.join(zip_output_dir, zip_name)

    print(f"\n[*] กำลังบีบอัดเป็นไฟล์ .zip: {zip_name} ...")
    with zipfile.ZipFile(zip_full_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(staging_dir):
            for file in files:
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, staging_dir)
                zipf.write(abs_f, rel_f)

    shutil.rmtree(staging_dir)
    print("\n" + "=" * 60)
    print("🎉 สร้างไฟล์มอดสำเร็จเรียบร้อยแล้ว!")
    print(f"📁 บันทึกไฟล์ไว้ที่: {zip_full_path}")
    print("=" * 60)
    print("\n👉 วิธีลงในเกมด้วย ZArchiver (ง่ายและตรงเป๊ะ 100%):")
    print(f"1. เปิดแอป ZArchiver -> เข้าโฟลเดอร์ Download")
    print(f"2. แตะที่ไฟล์ {zip_name} -> เลือก 'ดูข้อมูล' (View)")
    print("3. ข้างในจะเจอโฟลเดอร์ชื่อ 'files' ให้กดค้างที่โฟลเดอร์ 'files' แล้วเลือก 'คัดลอก' (Copy)")
    print(f"4. กดแถบด้านบนสุด ย้อนกลับไปที่: Android -> data -> {PKG_NAME}")
    print("5. กดปุ่ม 'วาง' สีเขียว (มุมขวาล่าง)")
    print("6. ติ๊กถูก 'นำไปใช้กับทุกไฟล์' (Apply to all) -> กด 'แทนที่' (Replace)")
    print("7. เปิดเกม RoV เลือกร่างต้น สกินจะเปลี่ยนเป็นสกินที่เลือกทันที!")
    print("=" * 60)
    return zip_full_path

def main():
    banner()
    print("[*] กำลังค้นหาโฟลเดอร์เกม RoV (Resources & Extra)...")
    res_dirs = find_game_resource_dirs()

    if not res_dirs:
        print("\n⚠️ ไม่พบโฟลเดอร์เกมอัตโนมัติ")
        user_path = input("กรุณาใส่ Path โฟลเดอร์ Resources หรือ Extra ด้วยตัวเอง: ").strip()
        if user_path and os.path.exists(user_path):
            res_dirs = [user_path]
        else:
            print("❌ ไม่พบโฟลเดอร์ สิ้นสุดการทำงาน")
            sys.exit(1)

    print(f"[✓] ตรวจพบโฟลเดอร์ข้อมูลเกม {len(res_dirs)} โฟลเดอร์:")
    for d in res_dirs:
        print(f"    📁 {d}")

    print("\n--- เลือกฮีโร่ ---")
    hero_input = input("ใส่ชื่อฮีโร่ (เช่น lauriel, nakroth, florentino) หรือรหัส ID: ").strip().lower()

    selected_hero_id = None
    if hero_input in NAME_ALIAS:
        selected_hero_id = NAME_ALIAS[hero_input]
    elif hero_input in ID_TO_HERO:
        selected_hero_id = hero_input
    elif hero_input.isdigit():
        selected_hero_id = hero_input
    else:
        for hid, name in ID_TO_HERO.items():
            if hero_input in name.lower():
                selected_hero_id = hid
                break

    if not selected_hero_id:
        print(f"❌ ไม่พบฮีโร่ '{hero_input}'")
        sys.exit(1)

    hname = ID_TO_HERO.get(selected_hero_id, f"Hero_{selected_hero_id}")
    print(f"\n[✓] คุณเลือก: {hname} (Hero ID: {selected_hero_id})")

    print(f"[*] กำลังสแกนหาเลขสกินของ {hname} ในไฟล์ที่พบ...")
    available_skins = scan_available_skins(res_dirs, selected_hero_id)

    if available_skins:
        print(f"\n✨ ตรวจพบเลขสกินสำหรับตัวนี้: {available_skins}")
        print("   (0 = ร่างต้นปกติ, 1 = สกินแรก, 2, 3, 5... เรียงตามสกินที่ปล่อย)")
    else:
        print("\nℹ️ ไม่พบไฟล์สกินใน Resources (ไฟล์โมเดลสกินส่วนใหญ่อยู่ในโฟลเดอร์ Extra)")

    target_skin = input("\nใส่ลำดับสกินที่ต้องการ (เช่น 1, 2, 5, 9): ").strip()
    if not target_skin.isdigit():
        print("❌ ลำดับสกินต้องเป็นตัวเลขเท่านั้น!")
        sys.exit(1)

    opt_10v10 = input("1. ต้องการให้ติดเอฟเฟกต์โหมด 10v10 ด้วยหรือไม่? (y/n) [ค่าเริ่มต้น: y]: ").strip().lower()
    include_10v10 = opt_10v10 != 'n'

    opt_sound = input("2. ต้องการให้ติดเสียงพากย์และเสียงสกิลด้วยหรือไม่? (y/n) [ค่าเริ่มต้น: y]: ").strip().lower()
    include_sound = opt_sound != 'n'

    generate_mod(
        source_dirs=res_dirs,
        hero_id=selected_hero_id,
        target_skin_num=target_skin,
        include_10v10=include_10v10,
        include_sound=include_sound
    )

if __name__ == "__main__":
    main()
