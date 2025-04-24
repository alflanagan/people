# Add to your existing INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    "rest_framework",
    "django_filters",
]

# Add REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}
