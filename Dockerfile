# Python builder stage
FROM python:3.13.2-alpine3.21 AS python-builder
WORKDIR /app
# Disable __pycache__ \ install packages globally
ENV PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local
RUN apk add --no-cache uv
COPY . .
RUN uv sync --no-dev --frozen && \
    rm -rf uv.lock pyproject.toml

# Final image stage
FROM python:3.13.2-alpine3.21
# Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# Create non-root user
RUN adduser -D appuser
# Dependencies and Project files
COPY --from=python-builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=python-builder /usr/local/bin/ /usr/local/bin/
COPY --from=python-builder --chown=appuser /app /app
# Make entry point executable and switch to non-root user
RUN chmod +x /app/entrypoint.sh
USER appuser
WORKDIR /app/blog
EXPOSE 8000
CMD ["/app/entrypoint.sh"]