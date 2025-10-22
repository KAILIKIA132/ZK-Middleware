# Makefile for ZK Middleware

.PHONY: install test run docker-build docker-run clean

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python test_middleware.py

# Run the application
run:
	python app.py

# Build Docker image
docker-build:
	docker build -t zk-middleware:latest .

# Run Docker container
docker-run:
	docker run -v $(PWD)/config.yml:/app/config.example.yml -p 5000:5000 zk-middleware:latest

# Clean Python cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Install in development mode
dev-install:
	pip install -e .

# Run with gunicorn
gunicorn:
	gunicorn -b 0.0.0.0:5000 app:app --workers 3

# Show help
help:
	@echo "Available targets:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  run          - Run the application"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo "  clean        - Clean Python cache files"
	@echo "  dev-install  - Install in development mode"
	@echo "  gunicorn     - Run with gunicorn"
	@echo "  help         - Show this help"