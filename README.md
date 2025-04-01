 # **XploitDir** - Advanced Directory Enumeration Tool  

![XploitDir](https://img.shields.io/badge/XploitDir-v1.0-blue.svg?style=flat-square)  
*A fast and powerful directory enumeration tool for penetration testers and security researchers.*

---

## **📜 Description**  
XploitDir is a multithreaded directory brute-forcing tool designed to help security professionals discover hidden directories and files on a target web server. By using a customizable wordlist, it scans URLs for accessible directories, aiding in security assessments and vulnerability testing.

---

## **🚀 Features**  
✅ **Multithreading Support** – Boosts speed with adjustable thread count  
✅ **Custom User-Agent** – Spoof User-Agent strings to avoid detection  
✅ **Timeout Control** – Define request timeouts for efficiency  
✅ **Live Progress Updates** – Track scan progress in real-time  
✅ **Formatted Logging** – Save results with timestamps for easy analysis

---

## **📌 Usage**  

### **🔹 Installation**  
Ensure you have **Python 3** installed and the required dependencies:  

```bash
git clone https://github.com/yourusername/XploitDir.git
cd XploitDir
pip install -r requirements.txt
```

---

### **🔹 Basic Usage**  
```bash
python xploitdir.py <target_url> <wordlist_file>
```

#### **🔹 Example:**  
```bash
python xploitdir.py http://example.com wordlist.txt
```

---

### **🔹 Advanced Usage**  
```bash
python xploitdir.py http://example.com wordlist.txt -t 20 -o results.txt --timeout 10 --user-agent "MyScanner/2.0"
```

#### **💡 Options:**  
| Option | Description | Default |
|--------|-------------|---------|
| `-t, --threads <num>` | Number of threads | `10` |
| `-o, --output <file>` | Save results to a file | `xploitdir_results.txt` |
| `--timeout <seconds>` | Set request timeout | `5.0` sec |
| `--user-agent <string>` | Custom User-Agent string | `"XploitDir/1.0"` |
| `-h, --help` | Show help menu | |

---

## **⚠️ Disclaimer**  
This tool is intended for educational and ethical security testing purposes only. **Do not use it on unauthorized systems.** The developer is not responsible for any misuse.

---

## **👨‍💻 Author**  
🛠 **Developed by [megoz]**  
📧 Contact: kareemmaged.official@gmail.com 
🚀 Follow me on GitHub: [kareemmaged](https://github.com/kareemmaged)  

---

## **⭐ Support**  
If you find XploitDir useful, consider **starring** the repository ⭐ and sharing it with fellow security enthusiasts!
