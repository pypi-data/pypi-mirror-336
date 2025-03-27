# dig_ass_critic_protos

## Ответственный разработчик

@bakulin

## Зависимости

`python3.13 -m pip install -r requirements.txt`

## Тесты

- `sudo docker compose up --build`

### Линтеры

Работают частично, не удалось исключить [DigitalAssistantCritic_pb2_grpc.py](src/dig_ass_critic_protos/DigitalAssistantCritic_pb2_grpc.py) из проверки

```shell
pip install black flake8-pyproject mypy
black .
flake8
mypy .
```
