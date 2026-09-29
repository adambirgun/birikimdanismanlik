# Birikim Danışmanlık — birikimedu.com

Alanya merkezli yurtdışı eğitim danışmanlığı sitesi (v2).

Statik HTML/CSS/JS. **GitHub Pages** + **Cloudflare** ile yayınlanır.

## Klasör yapısı

```
v2/                          ← Bu klasörün içeriğini repo köküne yükleyin
├── index.html
├── hakkimizda.html
├── hizmetlerimiz.html
├── iletisim.html
├── assets/
│   ├── css/style.css
│   ├── js/script.js
│   ├── images/
│   │   ├── brand/logo.png   ← logo
│   │   ├── og/              ← og-image.png (1200×630) buraya
│   │   ├── content/         ← sayfa / hizmet görselleri
│   │   └── team/            ← ekip fotoğrafları
│   ├── videos/              ← tanıtım / öğrenci videoları
│   ├── icons/               ← ek SVG / favicon dosyaları
│   ├── fonts/               ← self-host font (opsiyonel)
│   └── documents/           ← PDF broşür, form şablonları
├── docs/
│   └── DESIGN.md            ← tasarım referansı
├── _headers
├── robots.txt
├── sitemap.xml
├── CNAME
├── .gitignore
└── README.md
```

## Medya nereye konur?

| İçerik | Klasör | Örnek dosya adı |
|--------|--------|-----------------|
| Logo | `assets/images/brand/` | `logo.png`, `logo-white.png` |
| Sosyal önizleme | `assets/images/og/` | `og-image.png` (1200×630) |
| Sayfa görselleri | `assets/images/content/` | `ispanya.jpg`, `dil-okulu.webp` |
| Ekip | `assets/images/team/` | `birikim-buyukgebiz.jpg` |
| Video | `assets/videos/` | `tanitim.mp4`, `poster.jpg` |
| İkon / favicon | `assets/icons/` | `favicon.ico`, `whatsapp.svg` |
| Font dosyası | `assets/fonts/` | `Nunito-SemiBold.woff2` |
| PDF | `assets/documents/` | `basvuru-checklist.pdf` |

HTML’de örnek kullanım:

```html
<img src="assets/images/content/ispanya.jpg" alt="İspanya’da eğitim" width="800" height="500">
<video controls poster="assets/videos/poster.jpg">
  <source src="assets/videos/tanitim.mp4" type="video/mp4">
</video>
```

## GitHub Pages

1. Bu klasörün **içeriğini** repo köküne push edin (`index.html` kökte olsun).
2. Settings → Pages → branch `main` / `/ (root)`.
3. Custom domain: `birikimedu.com` (`CNAME` hazır).
4. Enforce HTTPS.

İletişim formu → kullanıcının e-posta uygulaması (`mailto:info@birikimedu.com`). Üçüncü taraf form servisi yok.

## Yerel önizleme

```bash
npx --yes serve .
```

## Cloudflare (üç alan adı)

Detaylı adımlar: [`docs/CLOUDFLARE.md`](docs/CLOUDFLARE.md)

| Domain | Rol |
|--------|-----|
| `birikimedu.com` | Ana site |
| `birikimedu.info` | → `.com` yönlendirme |
| `birikiedu.online` | → `.com` yönlendirme |

**Özet:** Cloudflare Pages ← GitHub repo → custom domain’ler → `.info` / `.online` 301 → `.com` → Email Routing `info@birikimedu.com`.

## GitHub Pages

1. Bu klasörün **içeriğini** repo köküne push edin (`index.html` kökte olsun).  
   Dosyalar `v2` altındaysa Cloudflare Pages **Root directory** = `v2` yapın.
2. Settings → Pages → branch `main` / `/ (root)` *(veya doğrudan Cloudflare Pages kullanın)*.
3. Custom domain: `birikimedu.com` (`CNAME` hazır).
4. Enforce HTTPS.