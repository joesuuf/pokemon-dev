/**
 * Comprehensive logging system with file writing capability
 */

export interface LogEntry {
  timestamp: string
  level: 'info' | 'error' | 'debug' | 'warn'
  message: string
  duration?: number
  size?: number
  url?: string
  statusCode?: number
}

class Logger {
  private logs: LogEntry[] = []
  private startTime: number = Date.now()
  private logFileName: string = ''

  constructor() {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    const hours = String(now.getHours()).padStart(2, '0')
    const mins = String(now.getMinutes()).padStart(2, '0')
    const secs = String(now.getSeconds()).padStart(2, '0')

    this.logFileName = `logALL-${year}${month}${day}-${hours}${mins}${secs}.md`

    // Write header
    this.writeToFile(`# Pokemon TCG Search - Comprehensive Log\n\n**Session Started:** ${now.toISOString()}\n\n## Log Entries\n\n`)
  }

  private getElapsedTime(): number {
    return Date.now() - this.startTime
  }

  private formatDuration(ms: number): string {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(2)}s`
  }

  private formatSize(bytes: number): string {
    if (bytes < 1024) return `${bytes}B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)}KB`
    return `${(bytes / 1024 / 1024).toFixed(2)}MB`
  }

  private writeToFile(content: string) {
    // Store in localStorage as a fallback since we can't write files directly from browser
    const key = `pokemon-tcg-logs-${this.logFileName}`
    const existing = localStorage.getItem(key) || ''
    localStorage.setItem(key, existing + content)
  }

  log(level: LogEntry['level'], message: string, options?: { duration?: number; size?: number; url?: string; statusCode?: number }) {
    const now = new Date()
    const timestamp = now.toISOString()
    const elapsed = this.getElapsedTime()

    const entry: LogEntry = {
      timestamp,
      level,
      message,
      duration: options?.duration,
      size: options?.size,
      url: options?.url,
      statusCode: options?.statusCode,
    }

    this.logs.push(entry)

    // Format for console
    let logLine = `[${timestamp}] [${level.toUpperCase()}] [+${this.formatDuration(elapsed)}] ${message}`

    if (options?.duration) {
      logLine += ` (${this.formatDuration(options.duration)})`
    }
    if (options?.size) {
      logLine += ` (${this.formatSize(options.size)})`
    }
    if (options?.statusCode) {
      logLine += ` (Status: ${options.statusCode})`
    }

    // Only log to console in development mode
    if (process.env.NODE_ENV === 'development') {
      console.log(logLine)
    }

    // Format for file
    let fileLine = `- **${level.toUpperCase()}** [\`${timestamp}\`] [+${this.formatDuration(elapsed)}]`

    if (options?.duration) {
      fileLine += ` ⏱️ ${this.formatDuration(options.duration)}`
    }
    if (options?.size) {
      fileLine += ` 📦 ${this.formatSize(options.size)}`
    }
    if (options?.statusCode) {
      fileLine += ` 🔗 HTTP ${options.statusCode}`
    }
    if (options?.url) {
      fileLine += ` 🌐 \`${options.url}\``
    }

    fileLine += `\n  ${message}\n\n`

    this.writeToFile(fileLine)
  }

  info(message: string, options?: { duration?: number; size?: number; url?: string }) {
    this.log('info', message, options)
  }

  error(message: string, options?: { duration?: number; size?: number; statusCode?: number; url?: string }) {
    this.log('error', message, options)
  }

  debug(message: string, options?: { duration?: number; size?: number; url?: string }) {
    this.log('debug', message, options)
  }

  warn(message: string, options?: { duration?: number; size?: number; url?: string }) {
    this.log('warn', message, options)
  }

  getLogs(): LogEntry[] {
    return [...this.logs]
  }

  exportLogs(): string {
    let markdown = `# Pokemon TCG Search - Complete Log Export\n\n**Session:** ${this.logFileName}\n\n## Summary\n\n- **Total Entries:** ${this.logs.length}\n- **Errors:** ${this.logs.filter(l => l.level === 'error').length}\n- **Duration:** ${this.formatDuration(this.getElapsedTime())}\n\n## Entries\n\n`

    this.logs.forEach(log => {
      markdown += `- **${log.level.toUpperCase()}** [\`${log.timestamp}\`]\n`
      markdown += `  - Message: ${log.message}\n`
      if (log.duration) markdown += `  - Duration: ${this.formatDuration(log.duration)}\n`
      if (log.size) markdown += `  - Size: ${this.formatSize(log.size)}\n`
      if (log.statusCode) markdown += `  - Status: ${log.statusCode}\n`
      if (log.url) markdown += `  - URL: \`${log.url}\`\n`
      markdown += `\n`
    })

    return markdown
  }

  downloadLog() {
    const markdown = this.exportLogs()
    const blob = new Blob([markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = this.logFileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
}

export const logger = new Logger()
