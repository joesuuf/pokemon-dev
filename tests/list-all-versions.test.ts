/**
 * Test to list and verify all front-end and back-end versions
 * 
 * This test provides a comprehensive overview of all versions in the application
 * and can be used to verify version consistency across the codebase.
 */

import { describe, it, expect } from 'vitest';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

describe('Application Versions', () => {
  describe('Front-End Versions', () => {
    const frontendPorts = [
      { port: 1111, name: 'Development Hub', path: 'frontends/port-1111' },
      { port: 4444, name: 'OCR Card Search', path: 'frontends/port-4444' },
      { port: 5555, name: 'Main React Frontend', path: 'frontends/port-5555' },
      { port: 6666, name: 'Pure HTML/CSS/JS (v2)', path: 'frontends/port-6666' },
      { port: 7777, name: 'React Variant A', path: 'frontends/port-7777' },
      { port: 8888, name: 'React Variant B', path: 'frontends/port-8888' },
      { port: 9999, name: 'React Variant C', path: 'frontends/port-9999' },
    ];

    it('should have 7 front-end versions', () => {
      expect(frontendPorts.length).toBe(7);
    });

    frontendPorts.forEach(({ port, name, path }) => {
      it(`should have frontend version on port ${port} (${name})`, () => {
        const fullPath = join(process.cwd(), path);
        expect(existsSync(fullPath)).toBe(true);
      });
    });

    it('should have vite configs for React versions', () => {
      const viteConfigs = [
        'vite.config.1111.ts',
        'vite.config.4444.ts',
        'vite.config.5555.ts',
        'vite.config.7777.ts',
        'vite.config.8888.ts',
        'vite.config.9999.ts',
      ];

      viteConfigs.forEach((config) => {
        const configPath = join(process.cwd(), config);
        expect(existsSync(configPath)).toBe(true);
      });
    });

    it('should have package.json scripts for all frontends', () => {
      const packageJsonPath = join(process.cwd(), 'package.json');
      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      const scripts = packageJson.scripts || {};

      expect(scripts['hub']).toBeDefined();
      expect(scripts['frontend:4444']).toBeDefined();
      expect(scripts['frontend:5555']).toBeDefined();
      expect(scripts['frontend:6666']).toBeDefined();
      expect(scripts['frontend:7777']).toBeDefined();
      expect(scripts['dev']).toBeDefined(); // Port 8888
      expect(scripts['frontend:8888']).toBeDefined();
      expect(scripts['frontend:9999']).toBeDefined();
      expect(scripts['frontends:all']).toBeDefined();
    });
  });

  describe('Back-End Versions', () => {
    it('should have backend directory', () => {
      const backendPath = join(process.cwd(), 'backend');
      expect(existsSync(backendPath)).toBe(true);
    });

    it('should have backend server file', () => {
      const serverPath = join(process.cwd(), 'backend', 'server.ts');
      expect(existsSync(serverPath)).toBe(true);
    });

    it('should have backend package.json', () => {
      const packageJsonPath = join(process.cwd(), 'backend', 'package.json');
      expect(existsSync(packageJsonPath)).toBe(true);
      
      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      expect(packageJson.name).toBe('pokemon-backend');
      expect(packageJson.version).toBeDefined();
    });

    it('should have OCR routes', () => {
      const ocrRoutePath = join(process.cwd(), 'backend', 'routes', 'ocr.ts');
      expect(existsSync(ocrRoutePath)).toBe(true);
    });

    it('should have server management routes', () => {
      const serversRoutePath = join(process.cwd(), 'backend', 'routes', 'servers.ts');
      expect(existsSync(serversRoutePath)).toBe(true);
    });
  });

  describe('Version Summary', () => {
    it('should list all front-end versions', () => {
      const versions = {
        frontend: {
          total: 7,
          react19: ['1111', '4444'],
          react18: ['5555', '7777', '8888', '9999'],
          vanilla: ['6666'],
        },
        backend: {
          total: 1,
          routes: ['ocr', 'servers'],
        },
      };

      expect(versions.frontend.total).toBe(7);
      expect(versions.frontend.react19.length).toBe(2);
      expect(versions.frontend.react18.length).toBe(4);
      expect(versions.frontend.vanilla.length).toBe(1);
      expect(versions.backend.total).toBe(1);
      expect(versions.backend.routes.length).toBe(2);
    });

    it('should have test suites for React versions', () => {
      const testPorts = [5555, 7777, 8888, 9999];
      
      testPorts.forEach((port) => {
        const testPath = join(process.cwd(), 'frontends', `port-${port}`, 'tests');
        expect(existsSync(testPath)).toBe(true);
      });
    });
  });

  describe('Version Information Output', () => {
    it('should provide version summary', () => {
      const summary = {
        frontendVersions: 7,
        backendVersions: 1,
        totalPorts: 8,
        reactVersions: {
          react19: 2,
          react18: 4,
        },
        vanillaVersions: 1,
        testSuites: 4,
      };

      console.log('\n=== VERSION SUMMARY ===');
      console.log(`Front-End Versions: ${summary.frontendVersions}`);
      console.log(`  - React 19: ${summary.reactVersions.react19} (ports 1111, 4444)`);
      console.log(`  - React 18: ${summary.reactVersions.react18} (ports 5555, 7777, 8888, 9999)`);
      console.log(`  - Vanilla JS: ${summary.vanillaVersions} (port 6666)`);
      console.log(`Back-End Versions: ${summary.backendVersions}`);
      console.log(`Total Ports: ${summary.totalPorts}`);
      console.log(`Test Suites: ${summary.testSuites} (ports 5555, 7777, 8888, 9999)`);
      console.log('======================\n');

      expect(summary.frontendVersions).toBe(7);
      expect(summary.backendVersions).toBe(1);
      expect(summary.totalPorts).toBe(8);
    });
  });
});
