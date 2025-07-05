#!/bin/bash

# 🚨 USO: sudo ./firewall-ctf.sh <IP del target VPN>
# Ejemplo: sudo ./firewall-ctf.sh 10.10.10.10

TARGET="$1"

if [ -z "$TARGET" ]; then
  echo "Uso: $0 <IP del target VPN>"
  exit 1
fi

# 🚩 Limpiar reglas previas
iptables -F
iptables -X

# 🚩 Política predeterminada: Drop todo
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# 🚩 Permitir conexiones establecidas/relacionadas
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 🚩 Permitir loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 🚩 Permitir salida básica
# DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT
# HTTP y HTTPS
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT

# 🚩 Permitir tráfico tun0 hacia el target VPN
# Entrada desde el target
iptables -A INPUT -i tun0 -s "$TARGET" -j ACCEPT
# Salida hacia el target
iptables -A OUTPUT -o tun0 -d "$TARGET" -j ACCEPT

# 🚩 Permitir ICMP en tun0 con el target (ping)
iptables -A INPUT -i tun0 -s "$TARGET" -p icmp -j ACCEPT
iptables -A OUTPUT -o tun0 -d "$TARGET" -p icmp -j ACCEPT

# 🚩 Docker: Permitir tráfico interno de Docker
# Ojo: Si quieres aislar más, aquí puedes ser restrictivo
iptables -A INPUT -i docker0 -j ACCEPT
iptables -A OUTPUT -o docker0 -j ACCEPT

# 🚩 (Opcional) Registrar y dropear lo que no se permite
iptables -A INPUT -j LOG --log-prefix "INPUT DROP: "
iptables -A OUTPUT -j LOG --log-prefix "OUTPUT DROP: "

echo "Firewall configurado para CTF con target $TARGET"
