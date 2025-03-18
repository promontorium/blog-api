# Python builder stage
FROM python:3.13-alpine AS python-builder
COPY . /app
WORKDIR /app
# Disable __pycache__ creation since it will not be skipped by .dockerignore x_x
ENV PYTHONDONTWRITEBYTECODE=1
# Install globally
ENV UV_PROJECT_ENVIRONMENT=/usr/local
# Get uv from image
COPY --from=ghcr.io/astral-sh/uv:0.6.7-alpine /usr/local/bin/uv /bin/
RUN uv sync --no-dev --frozen && \
    rm uv.lock pyproject.toml

# Final image stage
FROM python:3.13-alpine
# Create non-root user
RUN adduser -D appuser
# Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# Python dependencies from the builder stage
COPY --from=python-builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=python-builder /usr/local/bin/ /usr/local/bin/
# Project files
COPY --from=python-builder --chown=appuser /app /app
# Make entry point executable
RUN chmod +x /app/entrypoint.sh
# Run as non-root user
USER appuser
WORKDIR /app/blog
EXPOSE 8000
CMD ["/app/entrypoint.sh"]