# Code Mapper 🗺️

**Generate a complete text map of your codebase for AI context windows.**  
Perfect for feeding your **entire project** to ChatGPT, Claude, Gemini, Grok, or any LLM in one shot!

```
--app/UserController.php          (full source code)
--public/logo.png                 (binary – name only)
--SUMMARY
Text: 142  Binary: 38  Skipped: 2,847
```

One file → full project context. No more "upload 4 files at a time"!

---

### 🚀 Quick Start (Zero Setup)

**Option 1 – Easiest (Double-click)**
```
1. Drop codemapper.exe into your project folder
2. Double-click it
3. Done → codemapper/output/code_map.txt
```

**Option 2 – Terminal**
```bash
# In your project folder
codemapper.exe
```

---

### 📋 What It Does

- Includes **full content** of 70+ text file types (.py, .js, .php, .html, .md, .json, .sql, etc.)
- Lists binary files (images, PDFs, videos) by path only
- Skips junk automatically: `node_modules`, `.git`, `vendor`, `dist`, `build`, `__pycache__`, **codemapper folder itself**
- Outputs **one clean, copy-paste-ready** `.txt` file
- Optional timestamp: `code_map_110825-1430.txt`

---

### 💾 Save Your Settings (Configs)

#### Create Default Config (Run Once)
```bash
codemapper.exe --folders app,database,config --except-folders tests,storage --savetoconfig
```
→ Now just **double-click** `codemapper.exe` forever – it remembers!

#### Create Named Configs
```bash
codemapper.exe --folders app,src,public --savetoconfig frontend
codemapper.exe --folders api,database --savetoconfig backend
```

#### Use Them
```bash
codemapper.exe --config frontend
codemapper.exe --config backend
```

Configs live in: `codemapper/config/*.json`

---

### 🎯 Common Commands

| Goal                              | Command                                                                 |
|-----------------------------------|-------------------------------------------------------------------------|
| Scan entire project               | `codemapper.exe`                                                        |
| Specific folders only             | `codemapper.exe --folders app,src,config`                               |
| Specific files only               | `codemapper.exe --files config.php,.env.example,README.md`              |
| Exclude folders                   | `codemapper.exe --except-folders tests,logs,storage`                    |
| Exclude files                     | `codemapper.exe --except-files .env,package-lock.json`                  |
| Multiple source roots             | `codemapper.exe --src ./frontend --src ./backend`                       |
| Custom output path                | `codemapper.exe --output D:\maps\myproject.txt`                         |
| Only PHP files                    | `codemapper.exe --extensions *.php`                                      |
| Load saved config                 | `codemapper.exe --config myapp`                                         |
| Save current flags as config      | `codemapper.exe --folders app --savetoconfig myapp`                     |

---

### 🤖 Paste into Any AI (Example Prompts)

1. Generate map → open `codemapper/output/code_map.txt` → **Ctrl+A, Ctrl+C**
2. Paste into chat:

```text
Here's my entire codebase:

[PASTE MAP HERE]

Refactor the authentication system to use Laravel Sanctum.
```

Other great prompts:
- "Find security vulnerabilities"
- "Add file upload with progress bar"
- "Explain how User → Order → Payment models are related"
- "Convert this to TypeScript + React"

---

### 📁 Folder Structure After Running

```
your-project/
├── codemapper.exe
├── codemapper/
│   ├── config/
│   │   ├── default.json
│   │   └── frontend.json
│   └── output/
│       ├── code_map.txt
│       └── code_map_110825-1430.txt
├── src/
├── app/
└── public/
```

---

### 💡 Pro Tips

1. **Timestamp maps** → press `y` when asked → never overwrite old versions
2. **Open folder instantly** → choose `folder` at the end
3. **Large files?** Edit any `.json` in `codemapper/config/`:
   ```json
   { "max_file_size_mb": 50 }
   ```
4. **Multiple projects?** One exe → unlimited named configs!

---

### 🔧 Advanced Examples

```bash
# Only app folder, PHP files, 50MB limit
codemapper.exe --folders app --extensions .php --savetoconfig php-only

# Everything except tests + logs
codemapper.exe --except-folders tests,logs,storage/logs

# Full scan of two separate repos
codemapper.exe --src ../frontend --src ../api
```

---

### 🐍 Developers (Python Version)

```bash
python codemapper.py --folders app,src
```

Build your own exe:
```bash
pip install pyinstaller
pyinstaller --onefile --name codemapper codemapper.py
```

---

### ❓ FAQ

| Question                                   | Answer                                                                 |
|--------------------------------------------|------------------------------------------------------------------------|
| Where is the output?                       | `codemapper/output/code_map.txt` (or timestamped)                      |
| Can I use on 10 projects?                  | Yes – create 10 named configs                                          |
| What’s skipped by default?                 | `node_modules`, `.git`, `vendor`, `dist`, `build`, `codemapper` folder |
| How to reset defaults?                     | Delete `codemapper/config/default.json`                                |
| Works on Mac/Linux?                        | Yes with Python version (`codemapper.py`)                              |
| Can I exclude .env?                        | `codemapper.exe --except-files .env`                                   |

---

### 📄 Example Config (`codemapper/config/default.json`)

```json
{
  "src": ["."],
  "folders": ["app", "database", "config"],
  "except_folders": ["tests", "storage/logs"],
  "except_files": [".env", "package-lock.json"],
  "text_extensions": [".php", ".js", ".py", ".html", ".json", ".md"],
  "max_file_size_mb": 20
}
```

---

### 📄 License

**Free for personal and commercial use.**  
Made with ❤️ by an AI power user – enjoy unlimited context!

**Download `codemapper.exe` → drop → double-click → paste into AI → profit!** 🚀

--- 

*Last updated: November 08, 2025*