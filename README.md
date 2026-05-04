# LibFind

**LibFind** es una skill interna para evaluar si conviene reutilizar una librería open source de GitHub o implementar una solución propia dentro del proyecto.

Su objetivo no es buscar "la librería más popular", sino ayudar a tomar una decisión técnica conservadora, razonada y basada en evidencia.

---

## Propósito

LibFind ayuda a los agentes a investigar librerías reutilizables antes de implementar features, módulos, fixes o porciones de código no triviales.

La skill existe para evitar dos problemas opuestos:

- reinventar soluciones complejas que ya existen y están bien mantenidas;
- agregar dependencias innecesarias que aumentan riesgo, peso, mantenimiento o lock-in.

---

## Cuándo Usarla

Usá LibFind cuando:

- una feature o módulo podría resolverse con una librería existente;
- el problema es técnico, repetido o difícil de implementar correctamente;
- hay decisiones de `build vs in-house`;
- necesitás comparar varias librerías open source;
- querés validar licencia, seguridad, mantenimiento o compatibilidad antes de depender de un paquete;
- el código a construir podría introducir complejidad que ya fue resuelta por proyectos maduros.

## Cuándo NO Usarla

No hace falta usar LibFind cuando:

- la implementación propia sería corta, clara y segura;
- el problema es trivial;
- ya existe una utilidad interna equivalente;
- sólo se necesita una pequeña función que no justifica una dependencia;
- el requerimiento exige modificar código inmediatamente sin evaluar dependencias;
- se necesita una auditoría legal o de seguridad formal.

---

## Qué Problema Resuelve

LibFind reduce decisiones impulsivas sobre dependencias. Obliga a revisar contexto del repo, scope de búsqueda, licencia, seguridad, mantenimiento, compatibilidad, costo de integración y riesgo de supply chain antes de recomendar una librería.

También protege contra dependency creep: agregar paquetes grandes, riesgosos o mal mantenidos para resolver problemas simples.

---

## Filosofía

### Conservative by default

LibFind es conservadora por defecto. Una librería no se recomienda por ser popular, conocida o tener muchas estrellas. Se recomienda sólo si pasa los gates críticos y supera claramente a una implementación propia.

### Anti dependency creep

Si una dependencia agrega más superficie de riesgo que valor, la recomendación debe ser:

`build it in-house`

Esto aplica especialmente cuando:

- el problema es simple;
- la implementación propia es corta;
- la librería requiere mucha configuración;
- el paquete es demasiado grande;
- sólo se necesita una parte mínima;
- hay dudas de licencia, seguridad o mantenimiento.

---

## Cómo Invocarla

Prompt recomendado:

```text
Use $libfind to find and evaluate reusable open-source libraries before implementing this feature.
```

También puede invocarse cuando se quiera evaluar una librería específica o comparar alternativas.

---

## Ejemplos de Uso

```text
Use $libfind to evaluate whether we should add a markdown parser library or implement a small parser in-house.
```

```text
Use $libfind before building this CSV import feature. Check GitHub libraries compatible with our stack and recommend only if the dependency is worth it.
```

```text
Use $libfind to compare date/time libraries for this module and decide whether we should use one or build the required formatting helper ourselves.
```

---

## Ejemplo de Salida Esperada

```markdown
## Context detected
- Language: TypeScript
- Framework: Next.js
- Package manager: pnpm
- Dependency type: runtime dependency

## Problem to solve
Parse and sanitize user-provided markdown.

## Search scope
- Registry: npm
- Keywords: markdown parser, markdown sanitizer, commonmark
- Minimum features: parsing, sanitization support, ESM compatibility

## Candidates evaluated
| Candidate | Outcome | Notes |
| --- | --- | --- |
| example-lib-a | do not use | Unresolved advisory |
| example-lib-b | acceptable alternative | Good fit, larger bundle |
| example-lib-c | recommended library | Passes gates and reduces complexity |

## Final recommendation
recommended library: example-lib-c

## Pending risks
- Verify production bundle impact manually.

## Checklist before integration
- Review lockfile diff.
- Run security audit.
- Add integration tests.
```

---

## Criterios Evaluados

LibFind evalúa:

- **Licencia:** claridad, compatibilidad y obligaciones.
- **Seguridad:** advisories, CVEs, issues de seguridad y señales de riesgo.
- **Mantenimiento:** releases, actividad, respuesta a issues y madurez.
- **Compatibilidad:** lenguaje, framework, runtime, package manager y deploy.
- **Costo de integración:** configuración, cambios de arquitectura y testing.
- **Supply chain:** provenance, maintainer risk, install scripts y package/repo match.
- **Fit funcional:** si resuelve el problema real sin forzar abstracciones.
- **Build vs in-house:** si la dependencia reduce o aumenta complejidad neta.

---

## Outcomes Posibles

- `recommended library`
- `acceptable alternative`
- `use only if constraint X applies`
- `do not use`
- `build it in-house`
- `insufficient evidence`

Cuando falte evidencia crítica, la skill debe usar:

```text
Evidencia insuficiente para recomendar esta librería de forma segura.
```

---

## Limitaciones

LibFind v0.1.0 es advisory-only:

- no es auditoría legal formal;
- no es auditoría de seguridad formal;
- no instala paquetes;
- no modifica manifests;
- no modifica código;
- no crea wrappers ni adapters;
- no hace commits.

La decisión final de producción debe validarse manualmente con los procesos internos del equipo.

---

## Estructura de Archivos

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
│   └── validate_skill.py
└── references/
    ├── rubric.md
    └── scenarios.md
```

---

## Cómo Validar

Desde la raíz de la skill, ejecutar el validador local:

```powershell
python .\scripts\validate_skill.py .
```

El script usa sólo la standard library de Python, por lo que no requiere `PyYAML` ni paquetes externos. Si `python` no está en el PATH, usá cualquier ejecutable de Python 3 disponible y mantené los argumentos relativos.

Antes de mergear cambios a `main`, la validación debe pasar.

---

## Cómo Probar Escenarios

Los escenarios de prueba viven en `references/scenarios.md` y están espejados en `.plugin-eval/benchmark.json`.

Si `plugin-eval` está disponible:

```powershell
plugin-eval benchmark . --config .\.plugin-eval\benchmark.json
```

Si no está disponible, usar `references/scenarios.md` como checklist manual para revisar respuestas de la skill.

---

## Cómo Contribuir

1. Crear una branch según el tipo de cambio.
2. Modificar sólo los archivos necesarios.
3. Actualizar `CHANGELOG.md` si cambia comportamiento, criterios, workflow o documentación relevante.
4. Actualizar `VERSION` cuando corresponda.
5. Ejecutar `quick_validate.py`.
6. Abrir un PR hacia la rama correspondiente.

---

## Flujo de Branches

### Branches principales

- `main`
  - rama estable;
  - sólo versiones validadas;
  - cambios entran por PR;
  - debe pasar `quick_validate.py`.

- `develop`
  - rama de integración;
  - recibe features y mejoras documentales antes de release.

### Branches de trabajo

- `feat/nombre-del-cambio`
  - nuevas capacidades de la skill;
  - nuevos criterios;
  - nuevos documentos.

- `fix/nombre-del-fix`
  - correcciones de errores;
  - fixes de validación;
  - correcciones de comportamiento.

- `docs/nombre-del-cambio`
  - mejoras de README, changelog o documentación.

- `chore/nombre`
  - tareas menores de mantenimiento.

- `refactor/nombre`
  - reorganización interna sin cambiar comportamiento.

- `hotfix/nombre`
  - corrección urgente desde `main`;
  - debe volver a `main` y `develop`.

### Reglas

- No commitear directo a `main`.
- Todo cambio a `main` debe pasar por PR.
- Antes de mergear a `main`, ejecutar `quick_validate.py`.
- Todo cambio de comportamiento debe actualizar `CHANGELOG.md`.
- Todo release debe actualizar `VERSION`.
- Si cambia el workflow operativo de `SKILL.md`, subir al menos MINOR.
- Si sólo cambia `README.md` o aclaraciones menores, usar PATCH.
- Si rompe compatibilidad con invocaciones anteriores, usar MAJOR.

---

## Changelog

Los cambios se registran en `CHANGELOG.md` con formato simple inspirado en Keep a Changelog.

Cada versión debe indicar:

- fecha;
- cambios agregados;
- cambios modificados;
- fixes;
- cambios incompatibles, si existen.

---

## Semantic Versioning

LibFind usa Semantic Versioning:

- **MAJOR:** cambios incompatibles en el comportamiento de la skill o en invocaciones anteriores.
- **MINOR:** nuevas capacidades, nuevos criterios, nuevos formatos compatibles o cambios relevantes en el workflow operativo.
- **PATCH:** correcciones de redacción, aclaraciones, fixes menores y mejoras de documentación.

Versión inicial:

```text
0.1.0
```
