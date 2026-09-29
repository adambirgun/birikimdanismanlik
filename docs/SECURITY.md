# Site güvenlik notları

Statik site: sunucu tarafı form işleyici, oturum veya veritabanı yok.

## Zaten uygulananlar
- Form yalnızca `mailto:` (üçüncü taraf formşaj aktarımı yok)
- CSP / güvenlik başlıkları: `_headers` (Cloudflare Pages) + Cloudflare Transform Rules (GH Pages + proxy) — **GH Pages tek başına `_headers` okumaz; CF kuralı zorunlu**
- `Referrer-Policy` meta
- `robots.txt`: `/tools/`, `/docs/`, `/README.md` yasak
- `.well-known/security.txt`
- HSTS (proxy / Pages üzerinden)
- Clickjacking: `X-Frame-Options: DENY`, `frame-ancestors 'none'`
- `/tools` derleme betikleri canlı repoda yok (yalnızca lokal)

## Cloudflare’de hemen açın (GH Pages kullanıyorsanız)
`docs/CLOUDFLARE.md` içindeki **Transform Rules** tablosunu uygulayın. Aksi halde CSP / XFO / HSTS yanıt başlığında görünmez.

## Site sahibi kontrol listesi
- [ ] Cloudflare SSL: Full (strict), Always HTTPS
- [ ] Transform Rules güvenlik başlıkları (GH Pages ise)
- [ ] Email Routing: yalnızca ihtiyaç duyulan adresler
- [ ] GitHub repo’da sır / `.env` / hesap notları yok
- [ ] FormSubmit veya benzeri webhook kullanılmıyor
- [ ] Custom domain HTTPS yeşil (GitHub Pages Enforce HTTPS)

## Kullanıcı / yayıncı
- Site çerezleri yalnızca temel işlev (tercih anahtarları); izleme pixeli yok
- Harici script yalnızca Google Fonts (CSP’te sınırlı)
- Dil linkleri düz `<a href>` — JS zorunlu değil
