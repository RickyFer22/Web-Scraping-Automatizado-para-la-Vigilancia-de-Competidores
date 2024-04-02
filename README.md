# **Trabajo Final Bootcamp de Ingeniería de Datos** 


##  Título: Web Scraping Automatizado para la Vigilancia de Competidores

El **web scraping** es crucial en la ingeniería de datos para monitorear a la competencia en línea. ¿Por qué es necesario?

### Problema:

Las empresas necesitan estar al tanto de las estrategias de precios, productos y promociones de sus competidores para mantenerse competitivas. Sin embargo, recopilar esta información manualmente es tedioso y poco práctico, además sumado a su constantes cambios de precios por la alta inflación en argentina.

### Solución:

El **web scraping** automatiza la recopilación de datos relevantes de los sitios web de la competencia. Esto permite:

- Obtener datos actualizados sobre precios, productos y promociones.
- Analizar tendencias del mercado y comportamiento de la competencia.
- Ajustar estrategias empresariales de manera ágil y eficiente.

### Descripción:

El proyecto ha consistido en el desarrollo de un sistema automatizado que incluye las siguientes etapas:

1. **Web Scraping**:
   - Se ha utilizado las bibliotecas de  **Beautiful Soup** y **Selenium** para extraer datos de múltiples sitios web.
   - Se han definido los sitios web de interés y se han creado scripts para extraer la información relevante de manera eficiente.

2. **Almacenamiento en una base de datos relacional (SQLite)**:
   - Se ha creado una base de datos SQLite para almacenar los datos extraídos de forma organizada.
   - Se han diseñado tablas que reflejan la estructura de los datos y se han utilizado consultas SQL para la inserción y recuperación de información.

3. **Generación de informes en Excel**:
   - Se ha empleado la biblioteca **openpyxl** para generar archivos Excel que contienen los resultados del análisis.
   - Se han creado hojas de cálculo con los datos procesados.

4. **Orquestación y automatización con GitHub Actions**:
   - Se han configurado flujos de trabajo en **GitHub Actions** para automatizar tareas relacionadas con el proyecto.
   - Se han definido acciones que se ejecutan automáticamente cuando se realizan cambios en el repositorio, garantizando una gestión eficiente del proyecto.

5. **Comunicación efectiva de resultados por correo electrónico Google**:
   - Se ha utilizado la API de **Gmail** para enviar correos electrónicos que contienen los informes generados a una lista de destinatarios.
   - Se han adjuntado los archivos Excel con los informes o se han compartido enlaces para acceder a ellos directamente desde el correo electrónico.

Este proyecto ha permitido desarrollar un sistema completo que automatiza el proceso de obtención, almacenamiento, análisis y comunicación de datos, contribuyendo así a una toma de decisiones más informada y eficiente.

![webscraping](https://github.com/RickyFer22/Web-Scraping-Automatizado-para-la-Vigilancia-de-Competidores/assets/111261185/c3df0774-e71f-405f-a36a-5c42ed81c0b8)


