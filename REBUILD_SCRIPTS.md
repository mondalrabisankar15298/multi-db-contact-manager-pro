# 🚀 Quick Rebuild Scripts

These scripts help you quickly rebuild and run your Contact Manager app without restarting all services every time.

## 📋 Available Scripts

### 1. `./run-app.sh` - **Simple & Fast** ⚡
**Best for**: Quick testing after code changes
```bash
./run-app.sh
```
- ✅ Rebuilds app container silently
- ✅ Ensures databases are running
- ✅ Starts app interactively
- ⚡ Minimal output, fastest option

### 2. `./quick-rebuild.sh` - **Interactive Menu** 🎛️
**Best for**: When you need different rebuild options
```bash
./quick-rebuild.sh
```
**Options:**
1. 🔄 Rebuild app only (keeps databases running)
2. 🏗️ Rebuild app + restart databases  
3. 🧹 Clean rebuild (remove old images)
4. 📋 Just run existing app (no rebuild)
5. 🛑 Stop all services

## 🆚 When to Use Each Script

| Scenario | Recommended Script | Why |
|----------|-------------------|-----|
| Made small code changes | `./run-app.sh` | Fastest, silent rebuild |
| Want rebuild options | `./quick-rebuild.sh` | Interactive menu |
| Database issues | `./quick-rebuild.sh` → Option 2 | Restarts databases |
| App won't start properly | `./quick-rebuild.sh` → Option 3 | Clean rebuild |
| Just want to run app | `./quick-rebuild.sh` → Option 4 | No rebuild needed |

## 🔄 Typical Workflow

1. **Make code changes** in your editor
2. **Run rebuild script**: `./run-app.sh`
3. **Test your changes** in the interactive app
4. **Press Ctrl+C** to stop when done
5. **Repeat** as needed

## 💡 Tips

- **Databases stay running** between rebuilds (much faster!)
- **Use Ctrl+C** to exit the app cleanly
- **Scripts are safe** - they won't break your setup
- **All scripts work** from the project root directory

## 🚨 Troubleshooting

**App won't start?**
```bash
./quick-rebuild.sh
# Choose option 3 (Clean rebuild)
```

**Database connection issues?**
```bash
./quick-rebuild.sh  
# Choose option 2 (Rebuild + restart databases)
```

**Docker not running?**
```bash
# Start Docker Desktop first, then run any script
```

## 🔧 Original Commands (for reference)

These scripts replace the need to run:
```bash
# Old way (slow)
./start-docker-app.sh  # Rebuilds everything

# New way (fast)
./run-app.sh          # Rebuilds only app
```

---

## 📚 See Also

- **[README.md](README.md)** - Main project documentation
- **[DOCS.md](docs/DOCS.md)** - Complete documentation with all deployment options
- **[DOCKER_SETUP_GUIDE.md](docs/DOCKER_SETUP_GUIDE.md)** - Comprehensive Docker guide

---

**Happy coding! 🎉**
