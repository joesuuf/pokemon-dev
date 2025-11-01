# Start Both Servers Script (Windows PowerShell)
# Starts React front-end and HTML v2 front-end
# Works locally and in GitHub Codespaces

$ErrorActionPreference = "Stop"

# Configuration
$REACT_PORT = 8888
$HTML_PORT = 9999
$CAROUSEL_PORT = 7777

# Detect if we're in GitHub Codespaces
function Test-IsCodespace {
    $env:CODESPACE_NAME -or $env:GITHUB_CODESPACE
}

# Check if port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue
        return $connection.TcpTestSucceeded
    } catch {
        return $false
    }
}

# Check if dependencies are installed
function Test-Dependencies {
    if (-not (Test-Path "node_modules")) {
        Write-Host "⚠️  node_modules not found. Installing dependencies..." -ForegroundColor Yellow
        
        if (Get-Command npm -ErrorAction SilentlyContinue) {
            npm install
            Write-Host "✅ Dependencies installed!" -ForegroundColor Green
        } else {
            Write-Host "❌ npm not found. Please install Node.js." -ForegroundColor Red
            exit 1
        }
    }
}

# Start React dev server
function Start-ReactServer {
    Write-Host "🚀 Starting React dev server on port $REACT_PORT..." -ForegroundColor Blue
    
    if (Test-Port -Port $REACT_PORT) {
        Write-Host "⚠️  Port $REACT_PORT is already in use. Skipping React server." -ForegroundColor Yellow
        return
    }
    
    $reactJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        npm run dev 2>&1
    }
    
    Start-Sleep -Seconds 3
    
    Write-Host "✅ React server started (Job ID: $($reactJob.Id))" -ForegroundColor Green
    
    if (Test-IsCodespace) {
        $codespaceName = if ($env:CODESPACE_NAME) { $env:CODESPACE_NAME } else { $env:COMPUTERNAME.ToLower() }
        Write-Host "   Local: http://localhost:$REACT_PORT" -ForegroundColor Cyan
        Write-Host "   Codespace: https://$codespaceName-$REACT_PORT.app.github.dev" -ForegroundColor Cyan
    } else {
        Write-Host "   Access: http://localhost:$REACT_PORT" -ForegroundColor Cyan
    }
    
    return $reactJob
}

# Start HTML v2 server
function Start-HtmlServer {
    Write-Host "🚀 Starting HTML v2 server on port $HTML_PORT..." -ForegroundColor Blue
    
    if (Test-Port -Port $HTML_PORT) {
        Write-Host "⚠️  Port $HTML_PORT is already in use. Skipping HTML server." -ForegroundColor Yellow
        return
    }
    
    $htmlJob = $null
    
    # Try Python first, fallback to http-server (bind to 0.0.0.0 for Codespaces)
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $htmlJob = Start-Job -ScriptBlock {
            Set-Location (Join-Path $using:PWD "v2")
            # Python 3.8+ supports --bind flag
            python -m http.server $using:HTML_PORT --bind 0.0.0.0 2>&1
        }
    } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        $htmlJob = Start-Job -ScriptBlock {
            Set-Location (Join-Path $using:PWD "v2")
            python3 -m http.server $using:HTML_PORT --bind 0.0.0.0 2>&1
        }
    } elseif (Get-Command npx -ErrorAction SilentlyContinue) {
        $htmlJob = Start-Job -ScriptBlock {
            Set-Location $using:PWD
            npx http-server v2 -p $using:HTML_PORT -a 0.0.0.0 2>&1
        }
    } else {
        Write-Host "❌ No suitable server found. Install Python 3 or Node.js." -ForegroundColor Red
        exit 1
    }
    
    Start-Sleep -Seconds 2
    
    Write-Host "✅ HTML v2 server started (Job ID: $($htmlJob.Id))" -ForegroundColor Green
    
    if (Test-IsCodespace) {
        $codespaceName = if ($env:CODESPACE_NAME) { $env:CODESPACE_NAME } else { $env:COMPUTERNAME.ToLower() }
        Write-Host "   Local: http://localhost:$HTML_PORT" -ForegroundColor Cyan
        Write-Host "   Codespace: https://$codespaceName-$HTML_PORT.app.github.dev" -ForegroundColor Cyan
    } else {
        Write-Host "   Access: http://localhost:$HTML_PORT" -ForegroundColor Cyan
    }
    
    return $htmlJob
}

# Cleanup function
function Stop-Servers {
    param($ReactJob, $HtmlJob)
    
    Write-Host "`n🛑 Shutting down servers..." -ForegroundColor Yellow
    
    if ($ReactJob) {
        Stop-Job -Job $ReactJob -ErrorAction SilentlyContinue
        Remove-Job -Job $ReactJob -ErrorAction SilentlyContinue
        Write-Host "✅ React server stopped" -ForegroundColor Green
    }
    
    if ($HtmlJob) {
        Stop-Job -Job $HtmlJob -ErrorAction SilentlyContinue
        Remove-Job -Job $HtmlJob -ErrorAction SilentlyContinue
        Write-Host "✅ HTML server stopped" -ForegroundColor Green
    }
    
    # Kill processes on ports
    Get-NetTCPConnection -LocalPort $REACT_PORT -ErrorAction SilentlyContinue | 
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    Get-NetTCPConnection -LocalPort $HTML_PORT -ErrorAction SilentlyContinue | 
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}

# Main execution
$reactJob = $null
$htmlJob = $null

try {
    Write-Host "════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  Pokémon TCG Dev Servers" -ForegroundColor Green
    if (Test-IsCodespace) {
        Write-Host "  🚀 GitHub Codespaces Mode" -ForegroundColor Cyan
    } else {
        Write-Host "  💻 Windows PowerShell Mode" -ForegroundColor Cyan
    }
    Write-Host "════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    
    Test-Dependencies
    Write-Host ""
    
    $reactJob = Start-ReactServer
    Write-Host ""
    $htmlJob = Start-HtmlServer
    
    Write-Host ""
    Write-Host "✅ All servers started!" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow
    Write-Host ""
    
    # Wait for user interrupt
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    } catch {
        # User pressed Ctrl+C
    }
} finally {
    Stop-Servers -ReactJob $reactJob -HtmlJob $htmlJob
}

