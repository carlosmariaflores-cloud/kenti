# Kenti (código abierto de los módulos base)

**EN:** Kenti is a local desktop tool for ecological community data (diversity indices, similarity, clustering, PCA). This repository holds the source of Kenti Libre 0.3 (single-file HTML app), the Go launcher for Windows, the scripts that verify the calculations against NumPy/SciPy, and the scripts that generate the manuscript figures. MIT licensed. Reference databases and paid modules are not included.

Kenti es un sistema para manejo de datos ecológicos que corre en la computadora del usuario. Los datos no salen del equipo.

## Qué contiene

| Carpeta | Contenido |
|---|---|
| `web/` | Código fuente de Kenti Libre 0.3 (un solo archivo HTML con interfaz y cálculos). Se abre directamente en el navegador. |
| `launcher/` | Lanzador en Go (solo biblioteca estándar) que sirve la interfaz en 127.0.0.1, guarda los datos en Documentos y abre una ventana de aplicación. Ver `COMPILAR.md`. |
| `verificacion/` | Scripts que extraen las funciones reales de Kenti, las ejecutan sobre 1.000 conjuntos simulados por procedimiento y las comparan con NumPy/SciPy. `verificar.sh` reproduce la tabla del manuscrito. |
| `figuras/` | Scripts que generan las Figuras 1 y 2 del manuscrito. `reproducir.sh` las regenera. |

## Qué no contiene

Las bases de referencia (por ejemplo códigos y perfiles de diatomeas, tolerancias de índices bióticos regionales), los módulos pagos (fitoplancton/fitobentos, macroinvertebrados, ictiológico, caudal ecológico, etc.), sus configuraciones y las configuraciones de proyectos de clientes. Esos componentes no forman parte de este repositorio ni están cubiertos por su licencia.

## Verificar los cálculos

```
cd verificacion
bash verificar.sh
```

Requiere Node.js y Python con NumPy y SciPy.

## Licencia y marca

Código bajo licencia MIT (ver `LICENSE`). El nombre y logotipo "Kenti" son marca de sus autores y no se otorgan con la licencia; ver excepciones en `LICENSE`.

## Cómo citar

Ver `CITATION.cff`.

## Autores

Carlos María Flores (Atoj S.A.S.) y Mariana Urueña (Foconoa). La Esperanza, Tucumán, Argentina. Contacto: contacto@kenti.com.ar
