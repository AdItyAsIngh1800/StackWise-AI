from __future__ import annotations


LANGUAGE_TO_BACKEND_FRAMEWORKS = {
    "python": ["fastapi", "django", "flask"],
    "javascript": ["express", "nestjs"],
    "typescript": ["nestjs", "express"],
    "java": ["spring-boot"],
    "go": ["gin", "fiber"],
    "c#": ["aspnet-core"],
    "php": ["laravel"],
    "ruby": ["rails"],
    "rust": ["actix-web", "axum"],
}


LANGUAGE_TO_DATABASES = {
    "python": ["postgresql", "mysql", "mongodb", "redis", "sqlite"],
    "javascript": ["postgresql", "mongodb", "redis", "mysql"],
    "typescript": ["postgresql", "mongodb", "redis", "mysql"],
    "java": ["postgresql", "mysql", "redis"],
    "go": ["postgresql", "mysql", "redis"],
    "c#": ["postgresql", "sql-server", "redis"],
    "php": ["mysql", "postgresql", "redis"],
    "ruby": ["postgresql", "mysql", "redis"],
    "rust": ["postgresql", "redis", "sqlite"],
}


LANGUAGE_TO_DEPLOYMENT = {
    "python": ["render", "railway", "docker-vm", "ecs"],
    "javascript": ["vercel", "render", "railway", "docker-vm"],
    "typescript": ["vercel", "render", "railway", "docker-vm"],
    "java": ["docker-vm", "ecs", "kubernetes"],
    "go": ["docker-vm", "ecs", "kubernetes", "fly-io"],
    "c#": ["azure-app-service", "docker-vm", "ecs"],
    "php": ["shared-hosting", "render", "docker-vm"],
    "ruby": ["render", "fly-io", "docker-vm"],
    "rust": ["docker-vm", "fly-io", "kubernetes"],
}


FRAMEWORK_TO_LANGUAGE = {
    "fastapi": "python",
    "django": "python",
    "flask": "python",
    "express": "javascript",
    "nestjs": "typescript",
    "spring-boot": "java",
    "gin": "go",
    "fiber": "go",
    "aspnet-core": "c#",
    "laravel": "php",
    "rails": "ruby",
    "actix-web": "rust",
    "axum": "rust",
}


DATABASE_COMPATIBILITY_TAGS = {
    "postgresql": ["general-purpose", "relational", "scalable", "production-ready"],
    "mysql": ["relational", "common", "easy-hosting"],
    "mongodb": ["document", "flexible-schema", "rapid-iteration"],
    "redis": ["cache", "queue", "session-store"],
    "sqlite": ["embedded", "prototype", "single-node"],
    "sql-server": ["enterprise", "microsoft-stack", "relational"],
}


DEPLOYMENT_COMPATIBILITY_TAGS = {
    "vercel": ["frontend-first", "low-ops", "typescript-friendly"],
    "render": ["general-purpose", "low-ops", "full-stack-friendly"],
    "railway": ["rapid-prototyping", "low-ops", "startup-friendly"],
    "docker-vm": ["portable", "flexible", "self-managed"],
    "ecs": ["aws", "containerized", "scalable"],
    "kubernetes": ["high-scale", "high-complexity", "portable"],
    "fly-io": ["developer-friendly", "global", "container-based"],
    "azure-app-service": ["managed", "microsoft-stack"],
    "shared-hosting": ["cheap", "simple", "legacy-friendly"],
}