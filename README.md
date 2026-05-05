# LibFind

**LibFind** es una skill interna para evaluar si conviene reutilizar una librería open source de GitHub o implementar una solución propia dentro del proyecto.

Su objetivo no es encontrar "la librería más popular", sino ayudar a tomar una decisión técnica conservadora, razonada y basada en evidencia.

---

## Propósito

LibFind ayuda a los agentes a investigar librerías reutilizables antes de implementar features, módulos, fixes o porciones de código no triviales.

La skill existe para evitar dos problemas opuestos:

- reinventar soluciones complejas que ya existen y están bien mantenidas;
- agregar dependencias innecesarias que aumentan riesgo, peso, mantenimiento o lock-in.

---

## Cuándo usarla

Usá LibFind cuando:

- una feature o módulo podría resolverse con una librería existente;
- el problema es técnico, repetido o difícil de implementar correctamente;
- hay decisiones de `build vs in-house`;
- necesitás comparar varias librerías open source;
- querés validar licencia, seguridad, mantenimiento o compatibilidad antes de depender de un paquete;
- el código a construir podría introducir complejidad que ya fue resuelta por proyectos maduros.

No hace falta usar LibFind cuando:

- la implementación propia sería corta, clara y segura;
- el problema es trivial;
- ya existe una utilidad interna equivalente;
- sólo se necesita una pequeña función que no justifica una dependencia;
- el requerimiento exige modificar código inmediatamente sin evaluar dependencias;
- se necesita una auditoría legal o de seguridad formal.

---

## Filosofía

LibFind es conservadora por defecto. Una librería no se recomienda por ser popular o conocida. Se recomienda sólo si pasa gates críticos y supera claramente a una implementación propia.

Si una dependencia agrega más superficie de riesgo que valor, la recomendación debe ser `build-it-in-house`.

---

## Contrato de salida

LibFind ahora usa un contrato único:

- `Outcome code` siempre va en inglés y en `kebab-case`
- la explicación humana va en el idioma del usuario
- `Reason code` es opcional y también va en inglés

Outcome codes canónicos:

- `recommended-library`
- `acceptable-alternative`
- `use-only-if-constraint-applies`
- `do-not-use`
- `build-it-in-house`
- `insufficient-evidence`

Esto evita mezclar un contrato semántico en inglés con frases exactas en español.

Los templates oficiales viven en [references/output-formats.md](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/references/output-formats.md>).

---

## Ejemplo de salida

```markdown
## Context detected
- Language: TypeScript
- Framework or runtime: Next.js
- Package manager: pnpm
- Dependency type: runtime dependency

## Problem to solve
Render and sanitize user-provided Markdown.

## Search scope
- Registry: npm
- Keywords: markdown parser, markdown sanitizer, commonmark
- Minimum required features: parsing, sanitization support, ESM compatibility

## Candidates evaluated
| Candidate | Category | Outcome code | Notes |
| --- | --- | --- | --- |
| example-lib-a | runtime dependency | do-not-use | Unresolved advisory |
| example-lib-b | runtime dependency | acceptable-alternative | Good fit, larger bundle |
| example-lib-c | runtime dependency | recommended-library | Passes gates and reduces complexity |

## Final recommendation
- Outcome code: recommended-library
- Recommended option: example-lib-c
- Reason code: standards-complexity

## Pending risks
- Verificar manualmente el impacto en bundle y cold start.

## Checklist before integration
- Revisar lockfile diff.
- Correr auditoría de seguridad.
- Agregar tests de integración.

## Sources or evidence reviewed
- GitHub repository
- Package registry page
- Advisory sources
- Documentation
```

---

## Referencias

- [SKILL.md](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/SKILL.md>): workflow operativo.
- [references/rubric.md](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/references/rubric.md>): gates, scoring y heurísticas por categoría.
- [references/output-formats.md](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/references/output-formats.md>): templates compactos y completos.
- [references/scenarios.md](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/references/scenarios.md>): escenarios manuales y checklist de comportamiento.
- [.plugin-eval/benchmark.json](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/.plugin-eval/benchmark.json>): escenarios espejados para benchmark.

---

## Estructura de archivos

```text
libfind/
├── .plugin-eval/
│   ├── .gitignore
│   └── benchmark.json
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── VERSION
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── run_validate.ps1
│   ├── run_validate.sh
│   └── validate_skill.py
└── references/
    ├── output-formats.md
    ├── rubric.md
    └── scenarios.md
```

---

## Validación local

El validador usa sólo la standard library de Python.

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_validate.ps1 .
```

Si tu execution policy permite scripts locales, también podés usar:

```powershell
.\scripts\run_validate.ps1 .
```

Alternativa directa sin wrapper:

```powershell
py -3 .\scripts\validate_skill.py .
```

### Linux

```bash
sh ./scripts/run_validate.sh .
```

Alternativa directa:

```bash
python3 ./scripts/validate_skill.py .
```

### macOS

```bash
sh ./scripts/run_validate.sh .
```

Alternativa directa:

```bash
python3 ./scripts/validate_skill.py .
```

Antes de mergear cambios a `main`, la validación debe pasar.

---

## Benchmark con plugin-eval

Si `plugin-eval` está disponible:

```bash
plugin-eval benchmark . --config ./.plugin-eval/benchmark.json
```

El benchmark usa un verifier POSIX (`sh ./scripts/run_validate.sh .`) porque el harness de `plugin-eval` ejecuta verifiers con `/bin/zsh`. En Windows conviene correr ese benchmark desde un entorno compatible como WSL o Git Bash, o usar [references/scenarios.md](</C:/Users/nicoc/OneDrive/Documentos/New project 2/LibFind/references/scenarios.md>) como checklist manual.

---

## Cómo contribuir

1. Crear una branch según el tipo de cambio.
2. Modificar sólo los archivos necesarios.
3. Actualizar `CHANGELOG.md` si cambia comportamiento, criterios, workflow o documentación relevante.
4. Actualizar `VERSION` cuando corresponda.
5. Ejecutar la validación local en tu sistema operativo.
6. Abrir un PR hacia la rama correspondiente.

---

## Versionado

LibFind usa Semantic Versioning:

- **MAJOR:** cambios incompatibles en el comportamiento de la skill o en invocaciones anteriores.
- **MINOR:** nuevas capacidades, nuevos criterios, nuevos formatos compatibles o cambios relevantes en el workflow operativo.
- **PATCH:** correcciones de redacción, aclaraciones, fixes menores y mejoras de documentación.
