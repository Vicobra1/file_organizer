Add-Type -AssemblyName System.Drawing

$outPath = Join-Path $PSScriptRoot 'organiseur_icone.ico'
$bitmap = New-Object System.Drawing.Bitmap(256, 256, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$graphics.Clear([System.Drawing.Color]::Transparent)

function Fill-RoundedRect($graphics, $brush, [float]$x, [float]$y, [float]$width, [float]$height, [float]$radius) {
    $diameter = $radius * 2
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddArc($x, $y, $diameter, $diameter, 180, 90)
    $path.AddArc(($x + $width - $diameter), $y, $diameter, $diameter, 270, 90)
    $path.AddArc(($x + $width - $diameter), ($y + $height - $diameter), $diameter, $diameter, 0, 90)
    $path.AddArc($x, ($y + $height - $diameter), $diameter, $diameter, 90, 90)
    $path.CloseFigure()
    $graphics.FillPath($brush, $path)
    $path.Dispose()
}

$navy = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 23, 50, 77))
$teal = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 91, 205, 185))
$gold = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 195, 77))
$goldLight = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 215, 119))
$paper = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$blue = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 93, 157, 231))
$pink = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 220, 117, 151))
$green = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 70, 172, 126))

Fill-RoundedRect $graphics $navy 8 8 240 240 54

# Un dossier ouvert avec trois fiches colorées bien rangées.
Fill-RoundedRect $graphics $gold 42 57 104 49 13
Fill-RoundedRect $graphics $gold 35 81 186 116 16
Fill-RoundedRect $graphics $paper 59 95 43 79 8
Fill-RoundedRect $graphics $paper 106 88 43 86 8
Fill-RoundedRect $graphics $paper 153 98 43 76 8
Fill-RoundedRect $graphics $blue 68 105 25 7 3
Fill-RoundedRect $graphics $pink 115 98 25 7 3
Fill-RoundedRect $graphics $green 162 108 25 7 3

$linePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 206, 218, 230), 4)
$graphics.DrawLine($linePen, 68, 124, 91, 124)
$graphics.DrawLine($linePen, 68, 137, 88, 137)
$graphics.DrawLine($linePen, 115, 117, 138, 117)
$graphics.DrawLine($linePen, 115, 130, 135, 130)
$graphics.DrawLine($linePen, 162, 127, 185, 127)
$graphics.DrawLine($linePen, 162, 140, 182, 140)

# Rabat avant du dossier et petite étincelle.
$folderPath = New-Object System.Drawing.Drawing2D.GraphicsPath
$folderPath.AddLine(35, 128, 221, 128)
$folderPath.AddLine(221, 128, 207, 188)
$folderPath.AddArc(193, 178, 28, 25, 0, 90)
$folderPath.AddLine(207, 203, 49, 203)
$folderPath.AddArc(34, 188, 30, 30, 90, 90)
$folderPath.AddLine(34, 203, 35, 128)
$folderPath.CloseFigure()
$graphics.FillPath($goldLight, $folderPath)
$folderPath.Dispose()

$graphics.FillEllipse($teal, 195, 35, 12, 12)
$graphics.FillEllipse($teal, 218, 57, 8, 8)
$graphics.DrawLine((New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 91, 205, 185), 5)), 215, 34, 215, 49)
$graphics.DrawLine((New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 91, 205, 185), 5)), 208, 41, 223, 41)

$memory = New-Object System.IO.MemoryStream
$bitmap.Save($memory, [System.Drawing.Imaging.ImageFormat]::Png)
$png = $memory.ToArray()
$stream = [System.IO.File]::Create($outPath)
$writer = New-Object System.IO.BinaryWriter($stream)
$writer.Write([UInt16]0)
$writer.Write([UInt16]1)
$writer.Write([UInt16]1)
$writer.Write([Byte]0)
$writer.Write([Byte]0)
$writer.Write([Byte]0)
$writer.Write([Byte]0)
$writer.Write([UInt16]1)
$writer.Write([UInt16]32)
$writer.Write([UInt32]$png.Length)
$writer.Write([UInt32]22)
$writer.Write($png)
$writer.Close()
$memory.Dispose()
$graphics.Dispose()
$bitmap.Dispose()
$navy.Dispose(); $teal.Dispose(); $gold.Dispose(); $goldLight.Dispose(); $paper.Dispose()
$blue.Dispose(); $pink.Dispose(); $green.Dispose(); $linePen.Dispose()
Write-Output $outPath
