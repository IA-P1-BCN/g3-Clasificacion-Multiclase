# Quitar las parcelas sin medidas del entrenamiento y responder `none` por regla

Las 46 parcelas sin medidas (sitios Mor y Wen, en train) son todas de clase `none`. Si se dejan en el entrenamiento, el modelo aprende que "no hay medidas = none" y las métricas salen infladas. Por eso las quitamos **solo de train**, después del split. Validación y test las conservan, y una parcela sin medidas no pasa por el modelo: se responde `none` por regla fija, también en la app.

Sustituye a la primera versión de este ADR, que las quitaba también de validación y test.

## Consecuencias
- El modelo se entrena y se ajusta solo con parcelas con medidas; la clase `none` pasa de ~24,5 % a ~17 % de train.
- Validación y test incluyen parcelas sin medidas, así que se parecen a lo que verá la app. Las métricas se informan sobre todo el conjunto y también solo sobre las parcelas con medidas, porque la regla fija acierta las primeras por construcción.
- Hay que aplicar la regla a validación y test antes de calcular las métricas, en todos los notebooks de algoritmo.
