# 🔥 DNS & ARP Spoofing Tool - MITM Attack GUI

Una herramienta de ataque Man-in-the-Middle (MITM) con interfaz gráfica, desarrollada en Python y basada en Scapy y Tkinter. Permite realizar ataques de ARP Spoofing, DNS Spoofing y bloqueo de red a una víctima específica dentro de una red local.

![MITM Tool Banner](https://img.shields.io/badge/status-Development-orange)  
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)  
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

![image](https://github.com/user-attachments/assets/56a59e57-a875-42b6-b096-b6943a363d2d)

---

## ✨ Funcionalidades

- 🎯 **ARP Spoofing** para interceptar tráfico entre la víctima y el gateway.
- 🧠 **DNS Spoofing** configurable: define dominios personalizados para redirigir.
- 🔇 **Bloqueo de Internet**: desactiva la conectividad de la víctima con un clic.
- 🔍 **Escaneo de red** para encontrar hosts disponibles.
- 🔐 **Intercepción de credenciales** en tráfico HTTP y FTP.
- 🌐 **Reenvío de paquetes** y NAT para mantener la conexión a Internet de la víctima.
- 🖥️ Interfaz gráfica fácil de usar con `Tkinter`.

---

## 🧪 Requisitos

- Python 3.8+
- Sistema operativo **Linux** (con permisos de root)
- Bibliotecas:
  - `scapy`
  - `netifaces`
  - `tkinter` (generalmente preinstalada en sistemas con entorno gráfico)

Instálalos con:

```bash
sudo apt update
sudo apt install -y python3-scapy python3-tkinter python3-netifaces
sudo python3 spoofy.py
```

