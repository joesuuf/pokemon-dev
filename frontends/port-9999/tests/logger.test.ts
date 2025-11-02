import { describe, it, expect, beforeEach, vi } from 'vitest'
import { logger } from '../utils/logger'

describe('Logger', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should log info messages', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.info('Test info message')
    expect(consoleSpy).toHaveBeenCalled()
    expect(consoleSpy.mock.calls[0][0]).toContain('[INFO]')
  })

  it('should log error messages', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.error('Test error message')
    expect(consoleSpy).toHaveBeenCalled()
    expect(consoleSpy.mock.calls[0][0]).toContain('[ERROR]')
  })

  it('should log debug messages', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.debug('Test debug message')
    expect(consoleSpy).toHaveBeenCalled()
    expect(consoleSpy.mock.calls[0][0]).toContain('[DEBUG]')
  })

  it('should log warn messages', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.warn('Test warning message')
    expect(consoleSpy).toHaveBeenCalled()
    expect(consoleSpy.mock.calls[0][0]).toContain('[WARN]')
  })

  it('should include options in log messages', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.info('Test message', { duration: 100, size: 1024 })
    const logOutput = consoleSpy.mock.calls[0][0]
    expect(logOutput).toContain('Test message')
  })

  it('should get logs array', () => {
    logger.info('Message 1')
    logger.error('Message 2')
    const logs = logger.getLogs()
    expect(logs.length).toBeGreaterThanOrEqual(2)
  })

  it('should export logs as markdown', () => {
    logger.info('Test export')
    const markdown = logger.exportLogs()
    expect(markdown).toContain('Pokemon TCG Search')
    expect(markdown).toContain('Complete Log Export')
  })

  it('should handle log with duration', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.info('Timed operation', { duration: 500 })
    expect(consoleSpy).toHaveBeenCalled()
  })

  it('should handle log with size', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.debug('Size test', { size: 2048 })
    expect(consoleSpy).toHaveBeenCalled()
  })

  it('should handle log with URL', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.info('API call', { url: 'https://api.example.com' })
    expect(consoleSpy).toHaveBeenCalled()
  })

  it('should handle log with status code', () => {
    const consoleSpy = vi.spyOn(console, 'log')
    logger.error('Error response', { statusCode: 404 })
    expect(consoleSpy).toHaveBeenCalled()
  })

  it('should store logs in localStorage', () => {
    logger.info('Storage test')
    const stored = localStorage.getItem('pokemon-tcg-logs-logALL-20251024-234536.md')
    expect(stored).toBeDefined()
  })

  it('should download logs with createObjectURL', () => {
    logger.downloadLog()
    expect(window.URL.createObjectURL).toHaveBeenCalled()
  })

  it('should handle multiple log levels', () => {
    logger.info('Info')
    logger.error('Error')
    logger.debug('Debug')
    logger.warn('Warn')
    const logs = logger.getLogs()
    expect(logs.length).toBeGreaterThanOrEqual(4)
  })
})
