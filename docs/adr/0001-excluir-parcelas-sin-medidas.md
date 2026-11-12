# Excluir las parcelas sin medidas y responder `none` por regla

Las 46 parcelas sin medidas (sitios Mor y Wen) son todas de clase `none`. Si se dejan, el modelo aprende que "no hay medidas = none" y las métricas salen infladas. Por eso las quitamos del modelado en train, validación y test con la misma regla, y la app responde `none` por regla fija cuando la entrada no trae medidas, sin llamar al modelo.

## Consecuencias
- El modelo solo vale para parcelas con medidas, y las métricas del informe se refieren solo a ellas.
- La clase `none` pasa de ~24,5 % a ~17 % de train.
