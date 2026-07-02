# Start all servers: Django (8000), Admin CMS (8080), Portfolio (5174)

Write-Host "Starting all servers..." -ForegroundColor Green

# Start Django server on port 8000
Write-Host "Starting Django API on port 8000..." -ForegroundColor Yellow
$django = Start-Process python -ArgumentList "manage.py", "runserver" -NoNewWindow -PassThru

# Start Admin CMS on port 8080
Write-Host "Starting Admin CMS on port 8080..." -ForegroundColor Yellow
Set-Location admin
$admin = Start-Process npm -ArgumentList "run", "dev" -NoNewWindow -PassThru
Set-Location ..

# Start Portfolio site on port 5174
Write-Host "Starting Portfolio site on port 5174..." -ForegroundColor Yellow
Set-Location portfolio
$portfolio = Start-Process npm -ArgumentList "run", "dev" -NoNewWindow -PassThru
Set-Location ..

Write-Host ""
Write-Host "All servers started!" -ForegroundColor Green
Write-Host "Django API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Admin CMS: http://localhost:8080" -ForegroundColor Cyan
Write-Host "Portfolio: http://localhost:5174" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow

# Wait for any key to stop all servers
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "Stopping all servers..." -ForegroundColor Red
    Stop-Process -Id $django.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $admin.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $portfolio.Id -ErrorAction SilentlyContinue
    Write-Host "All servers stopped." -ForegroundColor Green
}
