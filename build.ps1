Param(
    [switch]$Clean,
    [switch]$View
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Ensure-ToolExists {
    param(
        [Parameter(Mandatory = $true)][string]$ToolName
    )
    $cmd = Get-Command $ToolName -ErrorAction SilentlyContinue
    if (-not $cmd) {
        throw "No se encontró '$ToolName' en el PATH. Instala MiKTeX o TeX Live y asegúrate de que '$ToolName' esté disponible."
    }
    return $cmd.Source
}

function Remove-AuxFiles {
    $auxFiles = @(
        'main.log', 'main.aux', 'main.blg', 'main.out', 'main.bbl',
        'missfont.log', 'main.lof', 'main.lot', 'main.toc',
        'main.synctex.gz', 'main.fls', 'main.fdb_latexmk', 'main.run.xml', 'main.bcf', 'main.xdv'
    )
    foreach ($f in $auxFiles) {
        Remove-Item -LiteralPath $f -ErrorAction SilentlyContinue
    }
}

function Ensure-OutDir {
    param([string]$OutDir)
    if (-not (Test-Path -LiteralPath $OutDir)) {
        New-Item -ItemType Directory -Path $OutDir | Out-Null
    }
}

function Run-XeLaTeX {
    param([string]$OutDir)
    Write-Host "Compilando con XeLaTeX (outdir=$OutDir)..." -ForegroundColor Cyan
    & xelatex -interaction=nonstopmode -halt-on-error -output-directory=$OutDir main.tex | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "XeLaTeX falló. Revisa 'out/main.log' para detalles. Si 'out/main.pdf' está abierto en un visor, ciérralo e inténtalo de nuevo."
    }
}

function Run-BibTeXIfNeeded {
    param([string]$OutDir)
    $auxPath = Join-Path $OutDir 'main.aux'
    if (Test-Path -LiteralPath $auxPath) {
        $needsBib = Select-String -Path $auxPath -Pattern '\\citation|\\bibdata|\\bibstyle' -Quiet
        if ($needsBib) {
            Write-Host "Ejecutando BibTeX..." -ForegroundColor Cyan
            Push-Location $OutDir
            & bibtex main | Out-Host
            $code = $LASTEXITCODE
            Pop-Location
            if ($code -ne 0) {
                throw "BibTeX falló. Revisa 'main.blg' para detalles."
            }
        }
        else {
            Write-Host "No se detectaron citas; se omite BibTeX." -ForegroundColor DarkYellow
        }
    }
}

try {
    if ($Clean) {
        Remove-AuxFiles
        if (Test-Path -LiteralPath 'out') {
            Write-Host "Eliminando carpeta 'out/'..." -ForegroundColor DarkYellow
            Remove-Item -Recurse -Force -LiteralPath 'out' -ErrorAction SilentlyContinue
        }
    }

    Ensure-ToolExists -ToolName 'xelatex' | Out-Null
    $bibtexPresent = $true
    try { Ensure-ToolExists -ToolName 'bibtex' | Out-Null } catch { $bibtexPresent = $false }
    if (-not $bibtexPresent) { Write-Host "Advertencia: 'bibtex' no está en PATH. Intentaré compilar sin bibliografía." -ForegroundColor DarkYellow }

    $outDir = 'out'
    Ensure-OutDir -OutDir $outDir

    Run-XeLaTeX -OutDir $outDir
    if ($bibtexPresent) { Run-BibTeXIfNeeded -OutDir $outDir }
    Run-XeLaTeX -OutDir $outDir
    Run-XeLaTeX -OutDir $outDir

    $pdfCandidate = Join-Path $outDir 'main.pdf'
    if (Test-Path -LiteralPath $pdfCandidate) {
        $pdfPath = Resolve-Path -LiteralPath $pdfCandidate
        Write-Host ("PDF generado: {0}" -f $pdfPath) -ForegroundColor Green
        if ($View) { Start-Process $pdfPath }
        exit 0
    }
    else {
        throw "La compilación terminó sin errores pero no se encontró 'out\\main.pdf'. Revisa 'out\\main.log'."
    }
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}


