import { useRef, useEffect } from 'react'

interface LogEntry {
  timestamp: string
  level: 'info' | 'error' | 'debug'
  message: string
}

interface DebugLogsProps {
  logs: LogEntry[]
  onDownloadLogs?: () => void
}

export default function DebugLogs({ logs, onDownloadLogs }: DebugLogsProps) {
  const logsEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Auto-scroll to bottom when new logs appear
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'text-red-400'
      case 'info':
        return 'text-blue-400'
      case 'debug':
        return 'text-gray-400'
      default:
        return 'text-white'
    }
  }

  const getLevelBg = (level: string) => {
    switch (level) {
      case 'error':
        return 'bg-red-900'
      case 'info':
        return 'bg-blue-900'
      case 'debug':
        return 'bg-gray-900'
      default:
        return 'bg-gray-800'
    }
  }

  if (logs.length === 0) {
    return (
      <div className="mt-8 bg-gray-900 rounded-lg shadow-lg p-4 font-mono text-sm border border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-gray-400 font-bold">🔍 Debug Console (Ready)</h3>
          <span className="text-gray-500 text-xs">Waiting for search...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="mt-8 bg-gray-900 rounded-lg shadow-lg p-4 font-mono text-sm border-2 border-yellow-500">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-white font-bold text-lg">🔍 Debug Console</h3>
          <p className="text-gray-400 text-xs mt-1">📋 Comprehensive logging with timestamps & request details</p>
        </div>
        <div className="flex gap-2">
          {onDownloadLogs && (
            <button
              onClick={onDownloadLogs}
              className="px-3 py-2 bg-green-600 hover:bg-green-700 text-white text-xs font-bold rounded transition-colors"
            >
              📥 Download Log
            </button>
          )}
          <span className="text-yellow-400 text-xs font-bold px-3 py-2 bg-gray-800 rounded">
            {logs.length} LOGS
          </span>
        </div>
      </div>

      <div className="bg-black rounded p-3 max-h-96 overflow-y-auto border border-gray-700">
        {logs.map((log, idx) => (
          <div key={idx} className={`${getLevelBg(log.level)} p-2 mb-1 rounded flex items-start gap-2 text-xs`}>
            <span className="text-gray-500 flex-shrink-0 w-24 font-bold">{log.timestamp}</span>
            <span className={`font-bold flex-shrink-0 w-14 ${getLevelColor(log.level)}`}>
              [{log.level.toUpperCase()}]
            </span>
            <span className="text-gray-100 flex-1 break-words">
              {log.message}
            </span>
          </div>
        ))}
        <div ref={logsEndRef} />
      </div>

      <p className="text-gray-500 text-xs mt-3">
        💡 Logs show API requests, responses, and errors for debugging
      </p>
    </div>
  )
}
