# DeviceUAgen

DeviceUAgen adalah pustaka Python untuk menghasilkan User-Agent yang realistis untuk berbagai merek dan model perangkat Android.

## Instalasi

Gunakan pip untuk menginstal paket ini:
```sh
pip install DeviceUAgen
```

## Penggunaan

```python
from DeviceUAgen import GenerateUseragent

# Inisialisasi objek GenerateUseragent
os = GenerateUseragent()

# Menghasilkan User-Agent dari sistem
ua = os.useragent(system=True)
print(ua)

# Menghasilkan User-Agent secara acak
ua = os.useragent()
print(ua)

# Menghasilkan User-Agent berbasis Dalvik dari sistem
ua = os.useragent(system=True, dalvik=True)
print(ua)

# Menghasilkan User-Agent berbasis Dalvik secara acak
ua = os.useragent(dalvik=True)
print(ua)
```

## Fitur
- Menghasilkan User-Agent berbasis Chrome
- Menghasilkan User-Agent berbasis Dalvik
- Mendukung berbagai merek dan model perangkat
- Dapat mengambil informasi perangkat dari sistem

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).