<p align="center">
  <img src="https://img.shields.io/github/languages/top/Rdimo/Anti-Debug?style=flat-square" </a>
  <img src="https://img.shields.io/github/last-commit/Rdimo/Anti-Debug?style=flat-square" </a>
  <img src="https://img.shields.io/github/stars/Rdimo/Anti-Debug?color=%2300ff99&label=Stars&style=flat-square" </a>
  <img src="https://img.shields.io/github/forks/Rdimo/Anti-Debug?color=%2300ff99&label=Forks&style=flat-square" </a>
</p>

#### Anti-Debug was made by
Love ❌ code ✅

---

### 🎉・What it checks for
**・** Kills tools that can be used to **debug your file**

**・** Exits if ran in vm (supports different vms like **oracle, sandbox, windows sandbox etc...**)

**・** Checks if the **Username, Pc name, hwid (uuid), ip and gpu** are any known vm's like virustotal

**・** Checks the **registery**

**・** Checks for **vm dll's and known vm folders**

**・** Checks the specs **(ram, hardrive space and cpu count)** to see if they are suspicious which could give away the vm

---

### 🎈・Code example
Example of how you can use [Anti-Debug](https://github.com/Rdimo/Anti-Debug#code-example)
```py
import os
from anti_debug import AntiDebug

if AntiVm().inVM:
    os._exit(0)
else:
    #we are not in a vm, run your malicious code or whatever
```
