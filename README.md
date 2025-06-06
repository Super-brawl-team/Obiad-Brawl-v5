# Obiad Brawl  
🎉 My first open-source project! 🎉  
This server support v5
---

## ⚠️ PLEASE READ THIS BEFORE USING! ⚠️  
### 🚨 This is an open-source server for self-hosting or simple hosting.  
### 📌 Installing the IPA without following the tutorial **will not work!**  

---

## 🔥 Features  
Enjoy tons of cool features, including:  
- The ability to **add brawlers, skins, ranks, and power levels**  
- Customization options for cryptography methods  
- Debug menu toggle  

---

## 🚀 Coming Soon  
- Online battle logic

---

## 🔄 Frequent Updates  
The server will be updated regularly! Feel free to use it, but **please don't forget to credit**. 😊  

---

## 🛠️ Requirements  
- **Python 3**  
- **A brain** 😭  

---

## 📥 Clients  
(Thanks to **risporce** for the method!)  

- **Client Download:** [Click Here](https://www.mediafire.com/file/yo6uuc9r5jn26yk/ObiadV5.ipa/file)  

---

## 🌍 How to Change IP and Port  
(Thanks to **risporce** for this amazing script!)  

### Steps:  
1. Download the client and extract it.  

2. Open your file manager and navigate to:  
   **`Payload/Brawl Stars.app/`**  

3. Open a terminal and navigate to the same directory.  

4. Locate **`ipPatcher.py`** in your file manager and open it in a text editor.  

5. Find the first line containing `patched_ip` and `patched_port`, then update the values:  
   - **Set `patched_ip`** to your device's **IPv4 address** (the one running the server).  
   - **Set `patched_port`** if needed (default: `9339`).  

6. Save the file and execute the following command in the terminal:  
   ```sh
   python ipPatcher.py
   ```  

7. Save your changes and **convert the file back to `.ipa`** format.  

8. Install the client using your favorite app installer. Enjoy! 🎉  

---

## 🎁 Bonus Features  

### 💪 Starting Tutorial state
- You can change `"startingTutorialState"` to the state you want
- **Note:** Id 0 is the tutorial with shelly, Id 1 is the first tutorial game, Id 2 is last tutorial state (main menu) , Id 3 and more will just act like Id 2

### 🎫 Ticket Price!
- You can change `"ticketPrice"` to the price you want
- **Note:** changing the price of the weekend event will also be the multiplier for the gained coins! I had to do that bc i cant read the ticket event selected price sorry about that

### 💪 Season reset bonus
- You can change `"seasonEndBonus"` to a certain integer value
- **Note:** If you set it to 0 or a negative number you will see nothing

### ⚡ UDP Server  
- You can enable `"UseUDPServer"` for battles if you have another free port.  
- **Note:** It's currently broken, so it may not work properly.  

### ⚡ Game Assets Server  
- You can enable `"gameAssetsServer"` to get an assets server and update every clients without sending a new one if you have another free port.  
- **Note:** You must run Updater.py to generate a new update.  

### 🔧 Debug Menu  
- Toggle `"debugMenuEnabled"` to enable/disable the debug menu.  
- **Note:** I don’t use dev builds, so only a few buttons work.  

### 🔐 RC4 Key  
- You **can** (optional) edit the **RC4 key** to a random one for better security.  
- Set `"changeRC4Key": true` and copy the key provided.  
- Update **`settings.json`** with your new key.  

### 🔑 Different Cryptography Methods  
- You can use **NaCl cryptography** by setting `"NACL"` in `settings.json`.  
- **Note:** Only useful if you're using this server as a base for **v7 or higher**.  

---

### 📝 Notes  
- **Do not use the RC4 key change feature**—it is currently broken.  
- If you encounter issues, double-check the tutorial and ensure everything is configured properly.  

---

**Enjoy hosting your own Obiad Brawl server! 🎮🔥**  
