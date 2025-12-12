# 🚀 Demos Funcionales - Sistema Multi-Agente

Esta carpeta contiene demos completamente funcionales del sistema multi-agente CrewAI.

## ✅ Estado: FUNCIONANDO

Todos los demos están **probados y funcionando** con Google Gemini 2.5 Flash (gratuito).

## 📋 Demos Disponibles

### 1. `demo_simple.py` (⭐ Recomendado - Marketing)
**Descripción:** Demo simplificado con 2 agentes coordinados  
**Agentes:** Market Research Analyst + Business Strategist  
**Tiempo:** ~3 minutos  
**Resultado:** Análisis completo de mercado + estrategia empresarial  

```bash
python demo_simple.py
```

### 2. `demo_sst.py` (⭐ Nuevo - Seguridad y Salud Laboral)
**Descripción:** Análisis integral de riesgos laborales con 3 especialistas SST  
**Agentes:** Risk Analyst + Compliance Officer + Prevention Planner  
**Tiempo:** ~6-8 minutos  
**Resultado:** Plan completo de prevención de riesgos (28,929 caracteres)  

```bash
python demo_sst.py
```

### 3. `demo_gemini.py` (Completo - Marketing)  
**Descripción:** Sistema multi-agente completo con 3 agentes especializados  
**Agentes:** Research + Strategy + Content  
**Tiempo:** ~5-7 minutos  
**Resultado:** Análisis integral de SaaS B2B España  

```bash
python demo_gemini.py
```

### 4. `demo_direct_gemini.py` (Diagnóstico)
**Descripción:** Prueba directa de conectividad con Google Gemini API  
**Propósito:** Verificar configuración de API y modelos disponibles  
**Tiempo:** ~30 segundos  

```bash
python demo_direct_gemini.py
```

## 🔧 Configuración Requerida

### Archivo `.env` (en la raíz del proyecto)
```bash
GOOGLE_API_KEY=tu_api_key_aqui
```

### Obtener API Key
1. Visita: https://aistudio.google.com/
2. Crea una API key gratuita
3. Cópiala al archivo `.env`

## 🎯 Casos de Uso Demostrados

### 📊 Marketing Digital
- ✅ **Análisis de Mercado**: Competidores, segmentos, oportunidades
- ✅ **Estrategia Empresarial**: Pricing, canales, plan marketing  
- ✅ **Research Sectorial**: Específico para mercado español
- ✅ **Métricas y KPIs**: Timeline detallado 6 meses

### 🦺 Seguridad y Salud en el Trabajo (SST)
- ✅ **Evaluación de Riesgos**: Matriz completa por nivel de criticidad
- ✅ **Cumplimiento Normativo**: Gap analysis detallado (Ley 31/1995, RDs)
- ✅ **Plan Integral de Prevención**: Presupuesto €75K/12 meses
- ✅ **Cronograma Implementación**: Planificación mensual con KPIs

## 📊 Ejemplo de Output

Los demos generan análisis profesionales de **15,000-29,000+ caracteres** incluyendo:

### Marketing Digital
- Análisis competitivo detallado (Microsoft, Google, Atlassian, Salesforce)
- Segmentación de clientes (consultorías, tech, manufactura)  
- Estrategia de precios por niveles (€9.99-€15.99/usuario/mes)
- Plan marketing €50K/6 meses con KPIs específicos

### Seguridad y Salud Laboral
- Evaluación integral de riesgos (físicos, químicos, ergonómicos, psicosociales)
- Análisis de cumplimiento normativo (7 normativas españolas)
- Plan preventivo €75K/12 meses con 91 actividades específicas
- Matriz de responsabilidades y cronograma de implementación mensual

## 💰 Costo

**€0.00** - Completamente gratuito usando Google Gemini 2.5 Flash

## 🆘 Resolución de Problemas

Si un demo falla:

1. **Verificar .env**: Confirma que `GOOGLE_API_KEY` esté configurada
2. **Conectividad**: Ejecuta `demo_direct_gemini.py` para diagnosticar
3. **Modelo actualizado**: Los demos usan `gemini-2.5-flash` (actualizado enero 2025)

## 📄 Documentación Adicional

- [Documentación SST Multi-Agent](../docs/sst_multiagent.md) - Arquitectura y flujos del dominio SST
- [API Setup Guide](../docs/api-setup-guide.md) - Guía completa de configuración de APIs