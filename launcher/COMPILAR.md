# Compilar el lanzador

Requiere Go 1.22 o posterior (se probó con 1.24.7). Sólo usa la biblioteca estándar.

```sh
cd launcher
mkdir -p web
cp ../web/Kenti-Libre-0.3.html web/index.html      # la interfaz que se embebe

# Linux / macOS (para pruebas)
go build -o kenti .

# Windows
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -trimpath \
  -ldflags "-H windowsgui -s -w \
    -X 'main.appID=kenti-libre' \
    -X 'main.appName=Kenti Libre' \
    -X 'main.folderName=Kenti Libre' \
    -X 'main.dataName=datos-kenti-libre.json' \
    -X 'main.portText=47840'" \
  -o "Kenti Libre.exe" .
```

Los valores de `appID`, `appName`, `folderName`, `dataName` y `portText` se fijan al compilar;
así un mismo lanzador sirve a cada módulo, con su propia carpeta de datos y su puerto.
Los ejecutables distribuidos en kenti.com.ar se compilan con el mismo código.
