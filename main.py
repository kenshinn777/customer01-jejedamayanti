import asyncio
import random
import json
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from isipesan import text_message

# ========== DAFTAR AKUN ==========
accounts = [
    {
        'api_id': 24174295,
        'api_hash': '796dfc5ac61ac4da26aec83b24e9fa41',
        'phone': '+6285352582288',
        'is_active': True
    }
]

# ========== LOAD GRUP ==========
def load_groups_from_file():
    try:
        with open("groups.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Gagal membaca groups.json: {e}")
        return {}

# ========== CEK KEANGGOTAAN ==========
async def is_member_of_group(client, group_username):
    try:
        entity = await client.get_entity(group_username)
        await client.get_participants(entity)
        return True
    except:
        return False

# ========== KIRIM PESAN ==========
async def send_text_message(account):
    if not account['is_active']:
        print(f"❌ Akun {account['phone']} nonaktif. Skip.\n")
        return

    client = TelegramClient('session_' + account['phone'], account['api_id'], account['api_hash'])
    await client.start(account['phone'])
    await asyncio.sleep(random.randint(3, 7))

    try:
        group_data = load_groups_from_file()
        group_links = group_data.get(account['phone'], [])

        while True:
            available_groups = group_links.copy()
            random.shuffle(available_groups)

            for group_link in available_groups:
                group_username = group_link.split("/")[-1]
                try:
                    if not await is_member_of_group(client, group_username):
                        await client(JoinChannelRequest(group_username))
                        print(f"✅ ({account['phone']}) Berhasil join {group_username}")
                        await asyncio.sleep(3)
                    
                    entity = await client.get_entity(group_username)
                    await client.send_message(entity, text_message)
                    print(f"✅ ({account['phone']}) Kirim pesan ke {group_link}")
                except Exception as e:
                    print(f"⚠️ ({account['phone']}) Gagal kirim ke {group_link}: {e}")
                    continue

            print(f"⏳ Cooldown 180 detik sebelum kirim ulang untuk {account['phone']}")
            await asyncio.sleep(180)

    except Exception as e:
        print(f"❌ ERROR umum akun {account['phone']}: {e}")

# ========== MAIN ==========
async def main():
    print("=== 🚀 Multi-Akun Telegram Message Sender Dimulai ===\n")

    tasks = []
    for acc in accounts:
        if acc['is_active']:
            tasks.append(asyncio.create_task(send_text_message(acc)))

    await asyncio.gather(*tasks)

# ========== EKSEKUSI ==========
if __name__ == '__main__':
    asyncio.run(main())
