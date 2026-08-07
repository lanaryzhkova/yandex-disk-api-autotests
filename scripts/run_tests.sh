cd "$(dirname "$0")/.."

THREADS=${1:-3}

echo "Запуск тестов, количество потоков (воркеров) $THREADS..."
pytest -n "$THREADS" --reruns=3 --alluredir=allure-results --clean-alluredir
allure serve