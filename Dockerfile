FROM devlifeag2003/python-package:1.0

# Copy app code
COPY . /app
WORKDIR /app

# Start server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
