# pyqeq 🐍 Python Quién es Quién - PyCamp 2026

PoC de un juego social por turnos donde los jugadores intentan descubrir quién dice la verdad y quién miente, compitiendo contra humanos.

## 🚀 Cómo empezar

1. **Instalar dependencias:**
   Asegurate de tener `uv` instalado.
   ```bash
   uv sync
   ```

2. **Configurar el entorno:**
   Crea un archivo `.env` (ya hay uno base) con tu `OPENAI_API_KEY` si querés usar bots reales.
   ```env
   DEBUG=True
   SECRET_KEY=clave-secreta-pycamp
   OPENAI_API_KEY=tu-key-aqui
   ```

3. **Migrar la base de datos:**
   ```bash
   uv run python manage.py migrate
   ```

4. **Correr para la red local:**
   Primero, descubrí tu IP local (ej: `192.168.1.XX`). Luego corre:
   ```bash
   uv run python manage.py runserver 0.0.0.0:8000
   ```
   ¡Tus amigos ya pueden entrar navegando a `http://tu-ip:8000`!

## 🎮 Mecánica del Juego
- **Lobby:** Creá una sala y compartí el código. Podés sumar bots.
- **Submitting:** Escribí 1 verdad y 2 mentiras sobre vos.
- **Guessing:** Adiviná cuál es la verdad de cada uno y quién escribió ese grupo de frases.
- **Results:** Mirá quién fue el mejor engañador y quién adivinó más.

## 🛠️ Tecnologías
- **Django 5.1** (Backend)
- **HTMX** (Interactividad sin recargar)
- **Tailwind CSS** (Estilos rápidos)
- **OpenAI API** (IA Player)
- **uv** (Gestión de paquetes)
