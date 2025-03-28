#!/bin/bash

# Уровень обновления версии (1 - patch, 2 - minor, 3 - major)
VERSION_BUMP=${1:-1}

# Проверяем наличие необходимых утилит
if ! command -v python &> /dev/null; then
    echo "Ошибка: Python не установлен"
    exit 1
fi

# Проверяем корректность аргумента версии
if [[ ! "$VERSION_BUMP" =~ ^[1-3]$ ]]; then
    echo "Ошибка: Аргумент должен быть 1, 2 или 3 (по умолчанию 1)"
    echo "1 - patch (0.0.1 → 0.0.2)"
    echo "2 - minor (0.0.1 → 0.1.0)"
    echo "3 - major (0.0.1 → 1.0.0)"
    exit 1
fi

# Загружаем переменные из .env файла
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Файл .env не найден"
    exit 1
fi

# Проверяем наличие переменной PYPI_API_KEY
if [ -z "$PYPI_API_KEY" ]; then
    echo "Ошибка: PYPI_API_KEY не установлен в .env файле"
    exit 1
fi

# Функция для обновления версии
update_version() {
    local current_version=$(grep -E '^version = "[0-9]+\.[0-9]+\.[0-9]+"' pyproject.toml | cut -d'"' -f2)
    IFS='.' read -ra version_parts <<< "$current_version"

    case $VERSION_BUMP in
        1) # Patch
            version_parts[2]=$((version_parts[2]+1))
            ;;
        2) # Minor
            version_parts[1]=$((version_parts[1]+1))
            version_parts[2]=0
            ;;
        3) # Major
            version_parts[0]=$((version_parts[0]+1))
            version_parts[1]=0
            version_parts[2]=0
            ;;
    esac

    new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"

    # Обновляем версию в pyproject.toml (версия для macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' -E "s/^version = \".+\"/version = \"$new_version\"/" pyproject.toml
        # Удаляем временный файл, если он создался
        [ -f "pyproject.toml-E" ] && rm "pyproject.toml-E"
    else
        sed -i -E "s/^version = \".+\"/version = \"$new_version\"/" pyproject.toml
    fi

    echo "Обновление версии: $current_version → $new_version"
}

# Обновляем версию
update_version

# Устанавливаем необходимые пакеты
pip install -q --upgrade build twine

# Очищаем предыдущие сборки
echo "Очистка предыдущих сборок..."
rm -rf dist/* build/*

# Собираем пакет
echo "Сборка пакета..."
python -m build

# Проверяем успешность сборки
if [ $? -ne 0 ]; then
    echo "Ошибка при сборке пакета"
    exit 1
fi

# Публикуем пакет
echo "Загрузка в PyPI..."
TWINE_USERNAME="__token__" \
TWINE_PASSWORD="$PYPI_API_KEY" \
twine upload --skip-existing dist/*

# Проверяем успешность загрузки
if [ $? -ne 0 ]; then
    echo "Ошибка при загрузке пакета"
    exit 1
fi

echo "Пакет успешно опубликован!"