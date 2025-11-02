# Modular Frontend Framework

## Overview

This directory contains a modular frontend architecture that allows running multiple frontend variants simultaneously on different ports. This enables A/B testing, feature experimentation, and deployment flexibility.

## Architecture

```
frontends/
├── port-5555/     # Main React Frontend (Production)
├── port-6666/     # Pure HTML/CSS/JS Frontend (Zero Dependencies)
├── port-7777/     # React Variant A (Testing/Staging)
├── port-8888/     # React Variant B (Testing/Feature Branch)
└── port-9999/     # React Variant C (Development/Experimental)
```

## Port Assignments

| Port | Frontend Type | Description | Use Case |
|------|--------------|-------------|----------|
| 5555 | React + TypeScript | Primary production frontend | Main user-facing application |
| 6666 | Pure HTML/CSS/JS | Zero-dependency version | Mobile-optimized, security-focused |
| 7777 | React Variant A | Alternative React implementation | A/B testing, staging |
| 8888 | React Variant B | Alternative React implementation | Feature branches, experiments |
| 9999 | React Variant C | Alternative React implementation | Development, beta features |

## Running Frontends

### Individual Ports

```bash
# Start port 5555 (Main React)
npm run frontend:5555

# Start port 6666 (Pure HTML)
npm run frontend:6666

# Start port 7777 (Variant A)
npm run frontend:7777

# Start port 8888 (Variant B)
npm run frontend:8888

# Start port 9999 (Variant C)
npm run frontend:9999
```

### All Frontends Simultaneously

```bash
# Start all frontends in parallel
npm run frontends:all
```

## Access URLs

Once running, access the frontends at:

- **Port 5555**: http://localhost:5555
- **Port 6666**: http://localhost:6666
- **Port 7777**: http://localhost:7777
- **Port 8888**: http://localhost:8888
- **Port 9999**: http://localhost:9999

## Frontend Details

### Port 5555 - Main React Frontend
- **Technology**: React 18, TypeScript, Vite 7, Tailwind CSS v4
- **Features**: Full-featured Pokemon TCG search with grid/list views
- **Build**: Production-ready with optimizations
- **Target**: End users, production deployment

### Port 6666 - Pure HTML/CSS/JS
- **Technology**: Vanilla HTML5, CSS3, JavaScript ES6+
- **Features**: Security-focused (CSP, XSS protection), WCAG 2.1 compliant
- **Build**: No build process required
- **Target**: Mobile browsers, lightweight deployments

### Port 7777 - React Variant A
- **Technology**: React 18, TypeScript, Vite 7, Tailwind CSS v4
- **Features**: Same as main frontend, customizable for testing
- **Build**: Development/staging builds
- **Target**: A/B testing, UI experiments

### Port 8888 - React Variant B
- **Technology**: React 18, TypeScript, Vite 7, Tailwind CSS v4
- **Features**: Same as main frontend, customizable for testing
- **Build**: Development/staging builds
- **Target**: Feature branches, alternative implementations

### Port 9999 - React Variant C
- **Technology**: React 18, TypeScript, Vite 7, Tailwind CSS v4
- **Features**: Same as main frontend, customizable for testing
- **Build**: Development/staging builds
- **Target**: Experimental features, beta testing

## Configuration Files

Each React-based frontend has its own Vite configuration:

- `vite.config.5555.ts` - Port 5555 configuration
- `vite.config.7777.ts` - Port 7777 configuration
- `vite.config.8888.ts` - Port 8888 configuration
- `vite.config.9999.ts` - Port 9999 configuration

Port 6666 uses http-server (no build configuration needed).

## Integration with Agents Framework

This modular frontend framework integrates seamlessly with the Python agents framework located in `/agents`:

```
pokemon-dev/
├── agents/              # Modular Python agents framework
│   ├── python/         # Agent implementations
│   ├── skills/         # Agent skills
│   └── workflows/      # Agent workflows
├── frontends/          # Modular frontend framework
│   ├── port-5555/     # Production frontend
│   ├── port-6666/     # Lightweight frontend
│   └── port-XXXX/     # Additional variants
└── package.json       # Frontend scripts
```

The agents can interact with any frontend variant for testing, monitoring, or automation purposes.

## Development Workflow

### Creating a New Variant

1. **Copy an existing frontend**:
   ```bash
   cp -r frontends/port-5555 frontends/port-XXXX
   ```

2. **Create a Vite config** (for React variants):
   ```typescript
   // vite.config.XXXX.ts
   export default defineConfig({
     plugins: [react()],
     root: resolve(__dirname, 'frontends/port-XXXX'),
     server: { port: XXXX, strictPort: true }
   })
   ```

3. **Add npm script**:
   ```json
   "frontend:XXXX": "vite --config vite.config.XXXX.ts"
   ```

4. **Test**:
   ```bash
   npm run frontend:XXXX
   ```

### Testing Changes

1. Make changes in the specific port directory
2. The dev server will hot-reload automatically
3. Test at http://localhost:XXXX
4. Compare with other variants if needed

### Deployment

Each frontend can be built and deployed independently:

```bash
# Build specific frontend
vite build --config vite.config.5555.ts

# Outputs to dist/port-5555/
```

## Use Cases

### A/B Testing
- Run port 5555 (control) and port 7777 (variant A) simultaneously
- Compare user metrics between versions
- Route traffic based on test groups

### Feature Development
- Develop new features on port 9999
- Test with users before merging to main
- Compare side-by-side with production

### Environment Separation
- **Production**: Port 5555
- **Staging**: Port 7777
- **Development**: Port 9999
- **Testing**: Port 8888

### Mobile-Specific Version
- Port 6666 serves a lightweight, zero-dependency version
- Optimized for mobile browsers
- Enhanced security features

## Performance

All frontends are independently optimized:

- **React frontends** (5555, 7777, 8888, 9999): Fast with Vite HMR
- **HTML frontend** (6666): ~30KB total size, no build step

## Security

- Port 6666 includes CSP headers and XSS protection
- React ports use secure dependencies and Vite's security features
- All frontends sanitize user input
- HTTPS recommended for production

## Troubleshooting

### Port Already in Use

If a port is already in use, the server will fail to start. Check running processes:

```bash
lsof -i :5555
```

Kill the process or use a different port.

### Module Not Found

If you get module errors:

```bash
npm install
```

### Vite Config Issues

Ensure the vite config points to the correct frontend directory:

```typescript
root: resolve(__dirname, 'frontends/port-XXXX')
```

## Testing Status

✅ All frontends tested and verified (2025-11-02):

- Port 5555: HTTP 200 OK
- Port 6666: HTTP 200 OK
- Port 7777: HTTP 200 OK
- Port 8888: HTTP 200 OK
- Port 9999: HTTP 200 OK

## Contributing

When adding new frontends:

1. Follow the existing port structure
2. Document the purpose in a README.md within the port directory
3. Add appropriate npm scripts
4. Test thoroughly before committing
5. Update this main README with the new port information

## Version History

- **v1.0** (2025-11-02): Initial modular frontend framework with 5 ports
- Integrated with existing Pokemon TCG Search application
- All ports tested and verified functional

---

**Last Updated**: 2025-11-02
**Maintained By**: Development Team
**Questions**: See main project README.md
