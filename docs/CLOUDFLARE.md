# Cloudflare + GitHub — üç alan adı

Canlı repo örneği: `https://github.com/adambirgun/birikimdanismanlik`  
Pages önizleme: `https://adambirgun.github.io/birikimdanismanlik/`

## Alan adları

| Alan adı | Rol |
|----------|-----|
| **birikimedu.com** | Ana (canonical) site |
| **birikimedu.info** | Aynı site / `.com`’a yönlendirme |
| **birikiedu.online** | Aynı site / `.com`’a yönlendirme |

> Yazım: mesajda `birikiedu.online` geçiyor (`m` yok). Domain gerçekten böyle alındıysa aşağıdaki tabloda olduğu gibi kullanın. `birikimedu.online` ise tüm adımlarda onu yazın.

Önerilen mimari: **Cloudflare Pages ← GitHub repo**, üç custom domain; `.info` ve `.online` → `.com` 301 redirect.

---

## A) Cloudflare Pages (önerilen)

`_headers` dosyası burada çalışır (güvenlik başlıkları).

### 1) Projeyi bağla

1. [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. GitHub: `adambirgun/birikimdanismanlik` (veya repo adınız)
3. Ayarlar (dashboard — bu hatalı ayar deploy’u kırar):

| Alan | Doğru değer | Yanlış (kaçın) |
|------|-------------|----------------|
| Production branch | `main` | — |
| Framework preset | **None** | Next/Nuxt vb. |
| Build command | *(boş)* | `npm run build` |
| **Build output directory** | `/` veya `.` | `index.html` ← **bu hata log’daki sebep** |
| **Root directory** | *(boş)* | `v2` ← repo kökünde zaten site var; `v2/` klasörü yok |

> Log’da `Output directory "index.html" not found` görürseniz: Pages → **Settings → Builds & deployments → Build configuration** → Output directory = `/` yapıp **Retry deployment**.

Repoda `wrangler.toml` ile `pages_build_output_dir = "."` tanımlıdır; dashboard yine `/` olmalı.

4. **Save and Deploy** — ilk deploy bitsin.

### 2) Custom domain’ler

Pages proje → **Custom domains** → **Set up a domain**:

1. `birikimedu.com`
2. `www.birikimedu.com` (isteğe bağlı)
3. `birikimedu.info`
4. `www.birikimedu.info` (isteğe bağlı)
5. `birikiedu.online`
6. `www.birikiedu.online` (isteğe bağlı)

Cloudflare her domain için DNS kayıtlarını kendisi ekler (domain aynı hesaptaysa).

### 3) DNS (her domain Cloudflare’de olmalı)

Her alan adı için:

1. Cloudflare → **Add a site** → domain’i ekle  
2. Registrar’da nameserver’ları Cloudflare’inkilerle değiştir  
3. SSL/TLS → **Full** (Pages ile genelde **Full (strict)**)

Pages custom domain eklenince tipik kayıtlar (otomatik):

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | `@` veya `www` | `<proje>.pages.dev` | Proxied (turuncu) |

Apex (`@`) için Cloudflare CNAME flattening kullanır — normaldir.

### 4) Yönlendirme: .info ve .online → .com

**Bulk Redirects** (önerilir):

1. **Account** → **Bulk Redirects** → List oluştur  
2. Kurallar:

| Source | Target | Status | Preserve query |
|--------|--------|--------|----------------|
| `https://birikimedu.info/*` | `https://birikimedu.com/${1}` | 301 | Evet |
| `https://www.birikimedu.info/*` | `https://birikimedu.com/${1}` | 301 | Evet |
| `https://birikiedu.online/*` | `https://birikimedu.com/${1}` | 301 | Evet |
| `https://www.birikiedu.online/*` | `https://birikimedu.com/${1}` | 301 | Evet |

**veya** her domain zone’unda **Rules → Redirect Rules**:

- If: Hostname equals `birikimedu.info`  
- Then: Dynamic redirect → `concat("https://birikimedu.com", http.request.uri.path)`  
- Status: 301  

Aynı kuralı `.online` için tekrarlayın.

### 5) www → apex (.com)

Redirect Rule:

- If: `www.birikimedu.com`  
- Then: `https://birikimedu.com` + path  
- 301  

### 6) SSL / güvenlik

Her zone (veya Pages):

| Ayar | Değer |
|------|--------|
| SSL/TLS mode | Full (strict) |
| Always Use HTTPS | On |
| Automatic HTTPS Rewrites | On |
| Minimum TLS | 1.2 |

Pages, repodaki `_headers` dosyasını uygular (CSP, X-Frame-Options vb.).

**GitHub Pages kullanıyorsanız** `_headers` uygulanmaz. Cloudflare DNS (turuncu bulut) açıksa şu Transform Rule’ları ekleyin (birikimedu.com zone):

1. **Rules → Transform Rules → Modify Response Header → Create rule**
2. Rule name: `Security headers`
3. When: `All incoming requests` (veya hostname = `birikimedu.com` / `www.birikimedu.com`)
4. Then set:

| Header | Value |
|--------|--------|
| `X-Frame-Options` | `DENY` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy` | `default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self' mailto:; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https: blob:; media-src 'self' blob:; connect-src 'self'; upgrade-insecure-requests` |

Ayrıca: **Scrape Shield / Email Address Obfuscation** açık olabilir (CF). **Bot Fight Mode** (ücretsiz) önerilir. Admin paneli / API anahtarı bu sitede yok — statik site.

### 7) E-posta (Cloudflare Email Routing)

Sadece **birikimedu.com** üzerinde yeterli (diğerleri yönleniyorsa):

1. Domain → **Email** → **Email Routing** → Enable  
2. Destination (Gmail vb.) doğrula  
3. Custom address: `info@birikimedu.com` → destination  

Form: `mailto:info@birikimedu.com` — tarayıcı e-posta uygulamasını açar; FormSubmit yok.

---

## B) Alternatif: GitHub Pages + Cloudflare DNS (üç domain)

Pages zaten açıksa: `https://adambirgun.github.io/birikimdanismanlik/`

### GitHub ayarı

1. Repo → **Settings → Pages**  
2. Custom domain: **birikimedu.com**  
3. Enforce HTTPS  

Repo kökünde `CNAME` dosyası içeriği:

```
birikimedu.com
```

> GitHub Pages **tek** custom domain kabul eder. `.info` / `.online` için Cloudflare redirect veya ikinci bir hosting gerekir. Bu yüzden **Pages (A)** daha uygun.

### DNS — sadece .com → GitHub

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | `@` | `185.199.108.153` | DNS only (gri) *veya* Proxied |
| A | `@` | `185.199.109.153` | aynı |
| A | `@` | `185.199.110.153` | aynı |
| A | `@` | `185.199.111.153` | aynı |
| CNAME | `www` | `adambirgun.github.io` | Proxied |

SSL Cloudflare: **Full**.

`.info` / `.online` zone’larında Redirect Rule → `https://birikimedu.com`.

**Not:** Proxied + GitHub’da bazen SSL doğrulama zorlanır; ilk kurulumda A kayıtlarını **DNS only** yapıp GitHub HTTPS yeşillensin, sonra turuncu bulut açın.

---

## Yayın kontrol listesi

- [ ] Üç domain Cloudflare’de (Active)
- [ ] GitHub repo Cloudflare Pages’e bağlı, deploy yeşil
- [ ] `https://birikimedu.com` açılıyor
- [ ] `https://birikimedu.info` → 301 → `.com`
- [ ] `https://birikiedu.online` → 301 → `.com`
- [ ] `www` → apex
- [ ] `info@birikimedu.com` mail geliyor
- [ ] Form test mesajı geldi
- [ ] Canonical / sitemap `https://birikimedu.com` (zaten böyle)

---

## Sık sorunlar

| Sorun | Çözüm |
|-------|--------|
| Domain pending | Nameserver değişimini bekleyin (birkaç saat) |
| SSL error | Full strict; sertifika provision bitene kadar bekleyin |
| Eski GH Pages path görünüyor | Pages custom domain + redirect; tarayıcı cache temizleyin |
| `_headers` yok | Cloudflare Pages kullanın; düz GH Pages bu dosyayı okumaz |
| Form gitmiyor | Cihazda varsayılan e-posta uygulaması tanımlı mı kontrol edin; veya doğrudan `info@birikimedu.com` yazın |

---

## Kısa özet

1. Üç domain’i Cloudflare’e ekle  
2. Repo’yu **Cloudflare Pages**’e bağla (`v2` kök ise Root directory = `v2`)  
3. Custom domains: `.com`, `.info`, `.online` (+ www)  
4. `.info` ve `.online` → `.com` 301  
5. Email Routing: `info@birikimedu.com`  
6. Form + SSL test
