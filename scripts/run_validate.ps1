$ErrorActionPreference = "Stop"

$target = if ($args.Count -gt 0) { $args[0] } else { "." }
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$validatorPath = Join-Path $scriptDir "validate_skill.py"

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $validatorPath $target
    exit $LASTEXITCODE
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $validatorPath $target
    exit $LASTEXITCODE
}

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 $validatorPath $target
    exit $LASTEXITCODE
}

Write-Error "Python 3 was not found in PATH."
exit 1
