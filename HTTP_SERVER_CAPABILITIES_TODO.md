# HTTP-Server Capabilities Implementation TODO

**Created:** 2025-11-02
**Package:** http-server v14.1.1
**Status:** Using basic features, many advanced capabilities available

---

## Current Implementation

We're currently using `npx http-server` with basic flags:
```bash
npx http-server [directory] -p [port] -a 0.0.0.0 -o
```

**Flags in use:**
- `-p [port]` - Port specification ✅
- `-a 0.0.0.0` - Bind to all addresses ✅
- `-o` - Open browser on start ✅

---

## Available Capabilities Not Yet Implemented

### 🔒 Security Features

#### 1. CORS Configuration
**Flag:** `--cors[=headers]`

**Use Case:**
- Enable cross-origin requests for API testing
- Configure specific CORS headers for different environments

**Implementation TODO:**
```bash
# Basic CORS
npx http-server v2 -p 9999 -a 0.0.0.0 --cors

# Custom CORS headers
npx http-server v2 -p 9999 -a 0.0.0.0 --cors="Content-Type,Authorization"
```

**Priority:** 🔴 HIGH - Important for API development

---

#### 2. Basic Authentication
**Flags:** `--username`, `--password`

**Use Case:**
- Protect staging/demo environments
- Secure internal development servers
- Can use environment variables for credentials

**Implementation TODO:**
```bash
# Via flags
npx http-server v2 -p 9999 -a 0.0.0.0 --username dev --password secret

# Via environment variables
export NODE_HTTP_SERVER_USERNAME=dev
export NODE_HTTP_SERVER_PASSWORD=secret
npx http-server v2 -p 9999 -a 0.0.0.0
```

**Priority:** 🟡 MEDIUM - Useful for shared development

---

#### 3. HTTPS/TLS Support
**Flags:** `-S`, `-C [cert]`, `-K [key]`

**Use Case:**
- Test service workers (require HTTPS)
- Test secure cookies and headers
- Simulate production HTTPS environment

**Implementation TODO:**
```bash
# Generate self-signed cert (one-time setup)
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

# Serve with HTTPS
npx http-server v2 -p 9999 -a 0.0.0.0 -S -C cert.pem -K key.pem
```

**Priority:** 🟡 MEDIUM - Important for PWA/service worker testing

---

### ⚡ Performance Features

#### 4. Gzip Compression
**Flag:** `-g` or `--gzip`

**Use Case:**
- Test compressed asset delivery
- Simulate production compression
- Improve local dev performance

**Implementation TODO:**
```bash
npx http-server v2 -p 9999 -a 0.0.0.0 -g -o
```

**Priority:** 🟢 LOW - Nice to have for performance testing

---

#### 5. Brotli Compression
**Flag:** `-b` or `--brotli`

**Use Case:**
- Modern compression (better than gzip)
- Test next-gen asset delivery
- Brotli takes precedence over gzip when both enabled

**Implementation TODO:**
```bash
# Brotli only
npx http-server v2 -p 9999 -a 0.0.0.0 -b -o

# Both (brotli preferred)
npx http-server v2 -p 9999 -a 0.0.0.0 -g -b -o
```

**Priority:** 🟢 LOW - Modern feature for optimization

---

#### 6. Cache Control
**Flag:** `-c [seconds]`

**Use Case:**
- Test caching strategies
- Disable caching for development
- Configure max-age headers

**Implementation TODO:**
```bash
# No caching (good for dev)
npx http-server v2 -p 9999 -a 0.0.0.0 -c-1 -o

# 10 second cache
npx http-server v2 -p 9999 -a 0.0.0.0 -c10 -o

# 1 hour cache (default is 3600)
npx http-server v2 -p 9999 -a 0.0.0.0 -c3600 -o
```

**Priority:** 🔴 HIGH - Very useful for development

---

### 🛠️ Development Features

#### 7. Proxy Fallback
**Flags:** `-P [url]`, `--proxy-options`

**Use Case:**
- Proxy API requests to backend
- Test with production APIs
- Single-domain development

**Implementation TODO:**
```bash
# Basic proxy
npx http-server v2 -p 9999 -a 0.0.0.0 -P http://localhost:3000

# With options
npx http-server v2 -p 9999 -a 0.0.0.0 -P http://api.example.com --proxy-options.secure false
```

**Priority:** 🟡 MEDIUM - Useful for full-stack dev

---

#### 8. Default File Extension
**Flag:** `-e [extension]`

**Use Case:**
- Serve files without extensions
- Clean URLs without .html
- Simulate production routing

**Implementation TODO:**
```bash
# Serve about as about.html
npx http-server v2 -p 9999 -a 0.0.0.0 -e html -o
```

**Priority:** 🟢 LOW - Nice for clean URLs

---

#### 9. Silent Mode
**Flag:** `-s` or `--silent`

**Use Case:**
- Reduce console noise
- Cleaner CI/CD logs
- Focus on application logs

**Implementation TODO:**
```bash
npx http-server v2 -p 9999 -a 0.0.0.0 -s -o
```

**Priority:** 🟢 LOW - Cleanliness preference

---

#### 10. Directory Listings Control
**Flag:** `-d [true|false]`

**Use Case:**
- Hide directory structure
- Secure file browsing
- Production-like behavior

**Implementation TODO:**
```bash
# Disable directory listings
npx http-server v2 -p 9999 -a 0.0.0.0 -d false -o
```

**Priority:** 🟡 MEDIUM - Security consideration

---

#### 11. Robots.txt Configuration
**Flag:** `-r` or `--robots`

**Use Case:**
- Test SEO configurations
- Control crawler behavior
- Default: disallow all

**Implementation TODO:**
```bash
npx http-server v2 -p 9999 -a 0.0.0.0 -r -o
```

**Priority:** 🟢 LOW - SEO testing

---

#### 12. Custom MIME Types
**Flag:** `--mimetypes [path]`

**Use Case:**
- Serve custom file types
- Override default MIME mappings
- Support new file formats

**Implementation TODO:**
```bash
# Create .types file with custom mappings
npx http-server v2 -p 9999 -a 0.0.0.0 --mimetypes custom.types -o
```

**Priority:** 🟢 LOW - Edge case support

---

#### 13. Hide Dotfiles
**Flag:** `--no-dotfiles`

**Use Case:**
- Security - hide .env, .git, etc.
- Production-like behavior
- Prevent sensitive file exposure

**Implementation TODO:**
```bash
npx http-server v2 -p 9999 -a 0.0.0.0 --no-dotfiles -o
```

**Priority:** 🔴 HIGH - Security best practice

---

#### 14. Connection Timeout
**Flag:** `-t [seconds]`

**Use Case:**
- Test timeout handling
- Configure long-polling scenarios
- Default: 120 seconds

**Implementation TODO:**
```bash
# 60 second timeout
npx http-server v2 -p 9999 -a 0.0.0.0 -t60 -o

# No timeout
npx http-server v2 -p 9999 -a 0.0.0.0 -t0 -o
```

**Priority:** 🟢 LOW - Specific use cases

---

#### 15. UTC Logging
**Flag:** `-U` or `--utc`

**Use Case:**
- Consistent timestamps
- Multi-timezone development
- Production log format

**Implementation TODO:**
```bash
npx http-server v2 -p 9999 -a 0.0.0.0 -U -o
```

**Priority:** 🟢 LOW - Logging preference

---

#### 16. IP Logging
**Flag:** `--log-ip`

**Use Case:**
- Track client connections
- Debug network issues
- Security monitoring

**Implementation TODO:**
```bash
npx http-server v2 -p 9999 -a 0.0.0.0 --log-ip -o
```

**Priority:** 🟢 LOW - Debugging aid

---

## Recommended Implementation Phases

### Phase 1: Security & Development Essentials (HIGH Priority)
1. ✅ Basic setup (current)
2. 🔲 Add CORS support (`--cors`)
3. 🔲 Disable caching for dev (`-c-1`)
4. 🔲 Hide dotfiles (`--no-dotfiles`)

**Suggested scripts:**
```json
{
  "v2": "npx http-server v2 -p 9999 -a 0.0.0.0 --cors -c-1 --no-dotfiles -o",
  "carousel": "npx http-server carousel -p 7777 -a 0.0.0.0 --cors -c-1 --no-dotfiles -o",
  "hub": "npx http-server hub -p 1111 -a 0.0.0.0 --cors -c-1 --no-dotfiles -o"
}
```

---

### Phase 2: Authentication & Proxying (MEDIUM Priority)
4. 🔲 Add basic auth for staging
5. 🔲 Configure proxy fallback
6. 🔲 HTTPS/TLS setup for PWA testing

**Suggested additional scripts:**
```json
{
  "v2:secure": "npx http-server v2 -p 9999 -a 0.0.0.0 -S --username dev --password secret",
  "v2:proxy": "npx http-server v2 -p 9999 -a 0.0.0.0 -P http://localhost:3000"
}
```

---

### Phase 3: Performance & Optimization (LOW Priority)
7. 🔲 Enable compression (gzip/brotli)
8. 🔲 Custom cache strategies
9. 🔲 Production-like configurations

**Suggested scripts:**
```json
{
  "v2:prod-like": "npx http-server v2 -p 9999 -a 0.0.0.0 -g -b -c3600 --no-dotfiles -d false"
}
```

---

## Environment Variables for Configuration

Create `.env.development`:
```bash
# HTTP Server Authentication
NODE_HTTP_SERVER_USERNAME=dev
NODE_HTTP_SERVER_PASSWORD=devpass123

# Server Ports
VITE_PORT=5173
V2_PORT=9999
CAROUSEL_PORT=7777
HUB_PORT=1111
```

---

## Documentation References

- http-server docs: https://github.com/http-party/http-server
- Current version: v14.1.1
- All features tested and available

---

**Next Steps:**
1. Implement Phase 1 (security essentials)
2. Update package.json with enhanced scripts
3. Document configuration in README
4. Create environment variable template
5. Test all configurations

---

**Last Updated:** 2025-11-02
