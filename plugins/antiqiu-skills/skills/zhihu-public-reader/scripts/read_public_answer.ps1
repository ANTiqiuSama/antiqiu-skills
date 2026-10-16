[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Url,

    [string]$CliPath = "C:\Users\Administrator\AppData\Local\Programs\zhihu-cli\Scripts\zhihu-cli.exe",

    [switch]$MetadataOnly,

    [switch]$AllowAnonymousProbe
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Result {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Value,
        [Parameter(Mandatory = $true)]
        [int]$ExitCode
    )

    $Value | ConvertTo-Json -Depth 8
    exit $ExitCode
}

if (-not (Test-Path -LiteralPath $CliPath -PathType Leaf)) {
    Write-Result -Value @{
        status = "cli_error"
        reason = "zhihu-cli executable was not found"
        http_status = $null
    } -ExitCode 2
}

$arguments = @("answer", $Url, "--api", "--json")
if ($MetadataOnly) {
    $arguments += "--metadata-only"
}
if ($AllowAnonymousProbe) {
    $arguments += "--allow-anonymous"
}

& $CliPath @arguments
$cliExitCode = $LASTEXITCODE
if ($null -eq $cliExitCode) {
    Write-Result -Value @{
        status = "cli_error"
        reason = "zhihu-cli did not report an exit code"
        http_status = $null
    } -ExitCode 2
}
exit $cliExitCode
