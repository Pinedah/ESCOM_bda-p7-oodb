# Sistema Médico

Sistema de gestión para consultas médicas desarrollado con Django.

## Requisitos previos

Para ejecutar esta aplicación, necesitas:

- [Docker](https://www.docker.com/products/docker-desktop) instalado y en ejecución
- [Git](https://git-scm.com/downloads) para clonar el repositorio

## Instrucciones de instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Pinedah/bda-p7-oodb.git
   cd bda-p7-oodb/sistema_medico
   ```

2. Crea un archivo `.env` en la carpeta `sistema_medico` con el siguiente contenido:
   ```
   # Django settings
   DJANGO_SECRET_KEY=django-insecure-x5*fam1pjjj%zr(yt@e(gx(pe+32ep^pk(gr*!!9gg*%s5vxr)
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   ```

3. Inicia la aplicación con Docker:
   ```bash
   docker-compose up --build
   ```

4. Accede a la aplicación en tu navegador:
   ```
   http://localhost:8000
   ```

## Cuentas de prueba

La aplicación incluye las siguientes cuentas predefinidas:

- **Admin**: 
  - Email: admin@admin.com
  - Contraseña: admin

- **Médico**: 
  - Email: medico@example.com
  - Contraseña: medico123

- **Pacientes**:
  - Email: paciente1@example.com
  - Contraseña: paciente123
  
  - Email: paciente2@example.com
  - Contraseña: paciente123

## Detener la aplicación

Para detener la aplicación, presiona `Ctrl+C` en la terminal donde está corriendo Docker Compose, o ejecuta:

```bash
docker-compose down
```

## Desarrollo

Si quieres contribuir al desarrollo:

1. Clona el repositorio
2. Crea un entorno virtual de Python
3. Instala las dependencias con `pip install -r requirements.txt`
4. Realiza tus cambios
5. Envía un Pull Request

## Licencia

Este proyecto está licenciado bajo MIT Licence
