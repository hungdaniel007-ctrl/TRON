# Su primera llamada a la API

La API de DeepSeek utiliza un formato de API compatible con OpenAI. Modificando la configuración, puede usar el SDK de OpenAI o software compatible con la API de OpenAI para acceder a la API de DeepSeek.

| PARÁMETRO  | VALOR                                                             |
| ---------- | ----------------------------------------------------------------- |
| URL base * | `https://api.deepseek.com`                                        |
| clave api  | solicitar una [clave API](https://platform.deepseek.com/api_keys) |

* Para ser compatible con OpenAI, también puedes usar `https://api.deepseek.com/v1`como `base_url`. Sin embargo, ten en cuenta que `v1`aquí NO tiene relación con la versión del modelo.

* **Y corresponden a la versión del modelo DeepSeek-V3.2 (límite de contexto de 128K), que difiere de la versión APP/WEB.`deepseek-chat``deepseek-reasoner`** `deepseek-chat` es el **modo sin pensamiento** de DeepSeek-V3.2 y `deepseek-reasoner`es el **modo de pensamiento** **de** DeepSeek-V3.2.

## Invocar la

Una vez obtenida la clave API, puede acceder a la API de DeepSeek mediante los siguientes scripts de ejemplo. Este es un ejemplo sin transmisión; puede configurar el `stream`parámetro para `true`obtener la respuesta de la transmisión.

- 
- node.js

```
// Please install OpenAI SDK first: `npm install openai`

import OpenAI from "openai";

const openai = new OpenAI({
        baseURL: 'https://api.deepseek.com',
        apiKey: process.env.DEEPSEEK_API_KEY,
});

async function main() {
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "You are a helpful assistant." }],
    model: "deepseek-chat",
  });

  console.log(completion.choices[0].message.content);
}

main();
```

# Almacenamiento en caché de contexto

La [tecnología de almacenamiento en caché de contexto de API de DeepSeek en disco](https://api-docs.deepseek.com/news/news0802) está habilitada de forma predeterminada para todos los usuarios, lo que les permite beneficiarse sin necesidad de modificar su código.

Cada solicitud de usuario activará la construcción de una caché en el disco duro. Si las solicitudes posteriores tienen prefijos que se superponen con las solicitudes anteriores, la parte superpuesta solo se recuperará de la caché, lo que se considera un "acceso de caché".

Nota: Entre dos solicitudes, solo la parte repetida **del prefijo** puede generar un acierto de caché. Consulte el ejemplo a continuación para obtener más detalles.

---

## Ejemplo 1: Preguntas y

**Primera solicitud**

```
messages: [
    {"role": "system", "content": "You are an experienced financial report analyst..."}
    {"role": "user", "content": "<financial report content>\n\nPlease summarize the key information of this financial report."}
]**Segunda solicitud**
```

```
messages: [
    {"role": "system", "content": "You are an experienced financial report analyst..."}
    {"role": "user", "content": "<financial report content>\n\nPlease analyze the profitability of this financial report."}
]En el ejemplo anterior, ambas solicitudes tienen el mismo **prefijo** , que es el `system`mensaje + `<financial report content>`en el `user`mensaje. Durante la segunda solicitud, este prefijo se considerará un "acceso de caché".
```

---

## Ejemplo 2:

**Primera solicitud**

```
messages: [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is the capital of China?"}
]**Segunda solicitud**
```

```
messages: [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is the capital of China?"},
    {"role": "assistant", "content": "The capital of China is Beijing."},
    {"role": "user", "content": "What is the capital of the United States?"}
]En este ejemplo, la segunda solicitud puede reutilizar el mensaje **inicial** `system` y `user`el mensaje de la primera solicitud, lo que contará como un "acceso de caché".
```

---

## Ejemplo 3: Uso

En aplicaciones prácticas, los usuarios pueden mejorar el rendimiento de salida del modelo mediante el aprendizaje de pocos ejemplos. Este aprendizaje implica proporcionar algunos ejemplos en la solicitud para que el modelo aprenda un patrón específico. Dado que el aprendizaje de pocos ejemplos generalmente proporciona el mismo prefijo de contexto, su costo se reduce significativamente gracias al almacenamiento en caché de contexto.

**Primera solicitud**

```
messages: [    
    {"role": "system", "content": "You are a history expert. The user will provide a series of questions, and your answers should be concise and start with `Answer:`"},
    {"role": "user", "content": "In what year did Qin Shi Huang unify the six states?"},
    {"role": "assistant", "content": "Answer: 221 BC"},
    {"role": "user", "content": "Who was the founder of the Han Dynasty?"},
    {"role": "assistant", "content": "Answer: Liu Bang"},
    {"role": "user", "content": "Who was the last emperor of the Tang Dynasty?"},
    {"role": "assistant", "content": "Answer: Li Zhu"},
    {"role": "user", "content": "Who was the founding emperor of the Ming Dynasty?"},
    {"role": "assistant", "content": "Answer: Zhu Yuanzhang"},
    {"role": "user", "content": "Who was the founding emperor of the Qing Dynasty?"}
]**Segunda solicitud**
```

```
messages: [    
    {"role": "system", "content": "You are a history expert. The user will provide a series of questions, and your answers should be concise and start with `Answer:`"},
    {"role": "user", "content": "In what year did Qin Shi Huang unify the six states?"},
    {"role": "assistant", "content": "Answer: 221 BC"},
    {"role": "user", "content": "Who was the founder of the Han Dynasty?"},
    {"role": "assistant", "content": "Answer: Liu Bang"},
    {"role": "user", "content": "Who was the last emperor of the Tang Dynasty?"},
    {"role": "assistant", "content": "Answer: Li Zhu"},
    {"role": "user", "content": "Who was the founding emperor of the Ming Dynasty?"},
    {"role": "assistant", "content": "Answer: Zhu Yuanzhang"},
    {"role": "user", "content": "When did the Shang Dynasty fall?"},        
]En este ejemplo, se utilizan 4 rondas. La única diferencia entre las dos solicitudes es la última pregunta. La segunda solicitud puede reutilizar el contenido de las primeras 4 rondas de diálogo de la primera, lo que se considerará un "acceso a la caché".
```

---

## Comprobación

En la respuesta de la API de DeepSeek, hemos agregado dos campos en la `usage`sección para reflejar el estado de acierto de caché de la solicitud:

1. prompt_cache_hit_tokens: la cantidad de tokens en la entrada de esta solicitud que resultaron en un acierto de caché (0,1 yuanes por millón de tokens).

2. prompt_cache_miss_tokens: La cantidad de tokens en la entrada de esta solicitud que no resultaron en un acierto de caché (1 yuan por millón de tokens).

## Caché del disco duro y

La caché del disco duro solo coincide con la parte del prefijo de la entrada del usuario. La salida se genera mediante cálculo e inferencia, y se ve influenciada por parámetros como la temperatura, lo que introduce aleatoriedad.

## adicionales

1. El sistema de caché utiliza 64 tokens como unidad de almacenamiento; el contenido con menos de 64 tokens no se almacenará en caché.

2. El sistema de caché funciona según el principio de "máximo esfuerzo" y no garantiza una tasa de acierto del caché del 100 %.

3. La creación de la caché tarda segundos. Una vez que la caché ya no se utiliza, se borra automáticamente, generalmente en cuestión de horas o días.

# Llamadas de herramientas

Llamadas de herramientas permite que el modelo llame a herramientas externas para mejorar sus capacidades.

---

## no pensante

### de muestra

A continuación se muestra un ejemplo del uso de llamadas a herramientas para obtener la información meteorológica actual de la ubicación del usuario, demostrado con código Python completo.

Para conocer el formato API específico de las llamadas de herramientas, consulte la documentación [de Finalización de chat](https://api-docs.deepseek.com/api/create-chat-completion/) .

```
from openai import OpenAI

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply a location first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [{"role": "user", "content": "How's the weather in Hangzhou, Zhejiang?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
print(f"Model>\t {message.content}")El flujo de ejecución de este ejemplo es el siguiente:
```

1. Usuario: Pregunta sobre el clima actual en Hangzhou
2. Modelo: Devuelve la función`get_weather({location: 'Hangzhou'})`
3. Usuario: llama a la función `get_weather({location: 'Hangzhou'})`y proporciona el resultado al modelo
4. Modelo: Devuelve en lenguaje natural: "La temperatura actual en Hangzhou es de 24 °C".

Nota: En el código anterior, la funcionalidad de la `get_weather`función debe ser proporcionada por el usuario. El modelo en sí no ejecuta funciones específicas.

---

## de pensamiento

A partir de DeepSeek-V3.2, la API admite el uso de herramientas en modo de pensamiento. Para más detalles, consulte [Modo de pensamiento.](https://api-docs.deepseek.com/guides/thinking_mode)

---

## `strict`Modo (Beta

En `strict`modo, el modelo cumple estrictamente los requisitos de formato del esquema JSON de la función al generar una llamada a una herramienta, lo que garantiza que la salida del modelo cumpla con la definición del usuario. Es compatible con los modos de pensamiento y no pensamiento.

Para utilizar `strict`el modo, necesitas:

1. Úselo `base_url="https://api.deepseek.com/beta"`para habilitar funciones Beta
2. En el `tools`parámetro, todos `function`deben establecer la `strict`propiedad en`true`
3. El servidor validará el esquema JSON de la función proporcionada por el usuario. Si el esquema no cumple con las especificaciones o contiene tipos de esquema JSON no compatibles con el servidor, se mostrará un mensaje de error.

El siguiente es un ejemplo de una definición de herramienta en el `strict`modo:

```
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "strict": true,
        "description": "Get weather of a location, the user should supply a location first.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
            "additionalProperties": false
        }
    }
}---
```

### Admite tipos de esquemas JSON en `strict`

- objeto
- cadena
- número
- entero
- booleano
- formación
- enumeración
- cualquiera de

---

Define `object`una estructura anidada que contiene pares clave-valor, donde `properties`especifica el esquema para cada clave (o propiedad) dentro del objeto. **Todas las propiedades de cada `object`deben establecerse como `required`, y el `additionalProperties`atributo de `object`debe establecerse como `false`.**

Ejemplo:

```
{
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" }
    },
    "required": ["name", "age"],
    "additionalProperties": false
}---
```

- Parámetros admitidos:
  
  - `pattern`:Utiliza expresiones regulares para restringir el formato de la cadena
  - `format`Valida la cadena con formatos comunes predefinidos. Formatos compatibles actualmente:
    - `email`: Dirección de correo electrónico
    - `hostname`: Nombre de host
    - `ipv4`:Dirección IPv4
    - `ipv6`:Dirección IPv6
    - `uuid`: UUID

- Parámetros no admitidos:
  
  - `minLength`
  - `maxLength`

Ejemplo:

```
{
    "type": "object",
    "properties": {
        "user_email": {
            "type": "string",
            "description": "The user's email address",
            "format": "email" 
        },
        "zip_code": {
            "type": "string",
            "description": "Six digit postal code",
            "pattern": "^\\d{6}$"
        }
    }
}---
```

#### número/

- Parámetros admitidos:
  - `const`: Especifica un valor numérico constante
  - `default`: Define el valor predeterminado del número
  - `minimum`: Especifica el valor mínimo
  - `maximum`: Especifica el valor máximo
  - `exclusiveMinimum`: Define un valor que el número debe ser mayor que
  - `exclusiveMaximum`: Define un valor que el número debe ser menor que
  - `multipleOf`:Asegura que el número sea un múltiplo del valor especificado

Ejemplo:

```
{
    "type": "object",
    "properties": {
        "score": {
            "type": "integer",
            "description": "A number from 1-5, which represents your rating, the higher, the better",
            "minimum": 1,
            "maximum": 5
        }
    },
    "required": ["score"],
    "additionalProperties": false
}---
```

- Parámetros no admitidos:
  - minItems
  - máximo de artículos

Ejemplo:

```
{
    "type": "object",
    "properties": {
        "keywords": {
            "type": "array",
            "description": "Five keywords of the article, sorted by importance",
            "items": {
                "type": "string",
                "description": "A concise and accurate keyword or phrase."
            }
        }
    },
    "required": ["keywords"],
    "additionalProperties": false
}---
```

Esto `enum`garantiza que la salida sea una de las opciones predefinidas. Por ejemplo, en el caso del estado del pedido, solo puede ser uno de un conjunto limitado de estados especificados.

Ejemplo:

```
{
    "type": "object",
    "properties": {
        "order_status": {
            "type": "string",
            "description": "Ordering status",
            "enum": ["pending", "processing", "shipped", "cancelled"]
        }
    }
}---
```

Coincide con cualquiera de los esquemas proporcionados, lo que permite que los campos admitan múltiples formatos válidos. Por ejemplo, la cuenta de un usuario podría ser una dirección de correo electrónico o un número de teléfono:

```
{
    "type": "object",
    "properties": {
    "account": {
        "anyOf": [
            { "type": "string", "format": "email", "description": "可以是电子邮件地址" },
            { "type": "string", "pattern": "^\\d{11}$", "description": "或11位手机号码" }
        ]
    }
  }
}---
```

#### $ref y $

Puede usarla `$def`para definir módulos reutilizables y luego `$ref`referenciarlos, lo que reduce la repetición de esquemas y permite la modularización. Además, `$ref`puede usarse de forma independiente para definir estructuras recursivas.

```
{
    "type": "object",
    "properties": {
        "report_date": {
            "type": "string",
            "description": "The date when the report was published"
        },
        "authors": {
            "type": "array",
            "description": "The authors of the report",
            "items": {
                "$ref": "#/$def/author"
            }
        }
    },
    "required": ["report_date", "authors"],
    "additionalProperties": false,
    "$def": {
        "authors": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "author's name"
                },
                "institution": {
                    "type": "string",
                    "description": "author's institution"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "author's email"
                }
            },
            "additionalProperties": false,
            "required": ["name", "institution", "email"]
        }
    }
}[
```

# Salida JSON

En muchos escenarios, los usuarios necesitan que el modelo genere en formato JSON estricto para lograr una salida estructurada, lo que facilita el análisis posterior.

DeepSeek proporciona salida JSON para garantizar que el modelo genere cadenas JSON válidas.

Para habilitar la salida JSON, los usuarios deben:

1. Establezca el `response_format`parámetro en `{'type': 'json_object'}`.
2. Incluya la palabra "json" en el sistema o en el mensaje de usuario y proporcione un ejemplo del formato JSON deseado para guiar al modelo en la salida de JSON válido.
3. Establezca el `max_tokens`parámetro de manera razonable para evitar que la cadena JSON se trunque a mitad de camino.
4. **Al usar la función de salida JSON, la API puede ocasionalmente devolver contenido vacío. Estamos trabajando activamente para solucionar este problema. Puede intentar modificar el mensaje de solicitud para mitigar estos problemas.**

## Aquí está el código Python completo que demuestra el uso de la salida JSON:

```
import json
from openai import OpenAI

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
        'type': 'json_object'
    }
)

print(json.loads(response.choices[0].message.content))El modelo generará:
```

```
{
    "question": "Which is the longest river in the world?",
    "answer": "The Nile River"
}[
```

# Almacenamiento en caché de contexto

La [tecnología de almacenamiento en caché de contexto de API de DeepSeek en disco](https://api-docs.deepseek.com/news/news0802) está habilitada de forma predeterminada para todos los usuarios, lo que les permite beneficiarse sin necesidad de modificar su código.

Cada solicitud de usuario activará la construcción de una caché en el disco duro. Si las solicitudes posteriores tienen prefijos que se superponen con las solicitudes anteriores, la parte superpuesta solo se recuperará de la caché, lo que se considera un "acceso de caché".

Nota: Entre dos solicitudes, solo la parte repetida **del prefijo** puede generar un acierto de caché. Consulte el ejemplo a continuación para obtener más detalles.

---

## Ejemplo 1: Preguntas y

**Primera solicitud**

```
messages: [
    {"role": "system", "content": "You are an experienced financial report analyst..."}
    {"role": "user", "content": "<financial report content>\n\nPlease summarize the key information of this financial report."}
]
```

**Segunda solicitud**

```
messages: [
    {"role": "system", "content": "You are an experienced financial report analyst..."}
    {"role": "user", "content": "<financial report content>\n\nPlease analyze the profitability of this financial report."}
]---
```

---

## Ejemplo 2:

**Primera solicitud**

```
messages: [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is the capital of China?"}
]
```

**Segunda solicitud**

```
messages: [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is the capital of China?"},
    {"role": "assistant", "content": "The capital of China is Beijing."},
    {"role": "user", "content": "What is the capital of the United States?"}
]
```

En este ejemplo, la segunda solicitud puede reutilizar el mensaje **inicial** `system` y `user`el mensaje de la primera solicitud, lo que contará como un "acceso de caché".

---

## Ejemplo 3: Uso

En aplicaciones prácticas, los usuarios pueden mejorar el rendimiento de salida del modelo mediante el aprendizaje de pocos ejemplos. Este aprendizaje implica proporcionar algunos ejemplos en la solicitud para que el modelo aprenda un patrón específico. Dado que el aprendizaje de pocos ejemplos generalmente proporciona el mismo prefijo de contexto, su costo se reduce significativamente gracias al almacenamiento en caché de contexto.

**Primera solicitud**

```
messages: [    
    {"role": "system", "content": "You are a history expert. The user will provide a series of questions, and your answers should be concise and start with `Answer:`"},
    {"role": "user", "content": "In what year did Qin Shi Huang unify the six states?"},
    {"role": "assistant", "content": "Answer: 221 BC"},
    {"role": "user", "content": "Who was the founder of the Han Dynasty?"},
    {"role": "assistant", "content": "Answer: Liu Bang"},
    {"role": "user", "content": "Who was the last emperor of the Tang Dynasty?"},
    {"role": "assistant", "content": "Answer: Li Zhu"},
    {"role": "user", "content": "Who was the founding emperor of the Ming Dynasty?"},
    {"role": "assistant", "content": "Answer: Zhu Yuanzhang"},
    {"role": "user", "content": "Who was the founding emperor of the Qing Dynasty?"}
]**Segunda solicitud**
```

```
messages: [    
    {"role": "system", "content": "You are a history expert. The user will provide a series of questions, and your answers should be concise and start with `Answer:`"},
    {"role": "user", "content": "In what year did Qin Shi Huang unify the six states?"},
    {"role": "assistant", "content": "Answer: 221 BC"},
    {"role": "user", "content": "Who was the founder of the Han Dynasty?"},
    {"role": "assistant", "content": "Answer: Liu Bang"},
    {"role": "user", "content": "Who was the last emperor of the Tang Dynasty?"},
    {"role": "assistant", "content": "Answer: Li Zhu"},
    {"role": "user", "content": "Who was the founding emperor of the Ming Dynasty?"},
    {"role": "assistant", "content": "Answer: Zhu Yuanzhang"},
    {"role": "user", "content": "When did the Shang Dynasty fall?"},        
]En este ejemplo, se utilizan 4 rondas. La única diferencia entre las dos solicitudes es la última pregunta. La segunda solicitud puede reutilizar el contenido de las primeras 4 rondas de diálogo de la primera, lo que se considerará un "acceso a la caché".
```

---

## Comprobación

En la respuesta de la API de DeepSeek, hemos agregado dos campos en la `usage`sección para reflejar el estado de acierto de caché de la solicitud:

1. prompt_cache_hit_tokens: la cantidad de tokens en la entrada de esta solicitud que resultaron en un acierto de caché (0,1 yuanes por millón de tokens).

2. prompt_cache_miss_tokens: La cantidad de tokens en la entrada de esta solicitud que no resultaron en un acierto de caché (1 yuan por millón de tokens).

## Caché del disco duro y

La caché del disco duro solo coincide con la parte del prefijo de la entrada del usuario. La salida se genera mediante cálculo e inferencia, y se ve influenciada por parámetros como la temperatura, lo que introduce aleatoriedad.

## adicionales

1. El sistema de caché utiliza 64 tokens como unidad de almacenamiento; el contenido con menos de 64 tokens no se almacenará en caché.

2. El sistema de caché funciona según el principio de "máximo esfuerzo" y no garantiza una tasa de acierto del caché del 100 %.

3. La creación de la caché tarda segundos. Una vez que la caché ya no se utiliza, se borra automáticamente, generalmente en cuestión de horas o días.

# Conversación de varias rondas

Esta guía presentará cómo utilizar la `/chat/completions`API de DeepSeek para conversaciones de múltiples turnos.

La `/chat/completions`API de DeepSeek es una API sin estado, lo que significa que el servidor no registra el contexto de las solicitudes del usuario. Por lo tanto, el usuario debe **concatenar todo el historial de conversaciones previas** y pasarlo a la API de chat con cada solicitud.

El siguiente código en Python demuestra cómo concatenar el contexto para lograr conversaciones de múltiples turnos.

```
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 1: {messages}")

# Round 2
messages.append({"role": "user", "content": "What is the second?"})
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 2: {messages}")---
```

En la **primera ronda** de la solicitud, los datos `messages`que se pasan a la API son:

```
[
    {"role": "user", "content": "What's the highest mountain in the world?"}
]En la **segunda ronda** de la solicitud:
```

1. Añade la salida del modelo de la primera ronda al final de `messages`.
2. Añade la nueva pregunta al final del `messages`.

Los datos `messages`que finalmente se pasan a la API son:

```
[
    {"role": "user", "content": "What's the highest mountain in the world?"},
    {"role": "assistant", "content": "The highest mountain in the world is Mount Everest."},
    {"role": "user", "content": "What is the second?"}
][
```

# Modo de pensamiento

El modelo DeepSeek admite el modo de pensamiento: antes de generar la respuesta final, el modelo generará un razonamiento en cadena para mejorar la precisión de la respuesta final. Puede activar el modo de pensamiento mediante cualquiera de los siguientes métodos:

1. Establezca el `model`parámetro:`"model": "deepseek-reasoner"`

2. Establezca el `thinking`parámetro:`"thinking": {"type": "enabled"}`

Si está utilizando el SDK de OpenAI, al configurar `thinking`el parámetro, debe pasar el `thinking`parámetro dentro de `extra_body`:

```
response = client.chat.completions.create(
  model="deepseek-chat",
  # ...
  extra_body={"thinking": {"type": "enabled"}}
)## de API
```

- **Aporte** :
  
  - `max_tokens`Longitud máxima de salida (incluida la parte COT). Predeterminado: 32 Kbps, máximo: 64 Kbps.

- **Producción** :
  
  - `reasoning_content`El contenido del CoT, que se encuentra al mismo nivel que `content`la estructura de salida. Consulte [el ejemplo de API](https://api-docs.deepseek.com/guides/thinking_mode#api-example) para obtener más información.
  - `content`:El contenido de la respuesta final.
  - `tool_calls`:La herramienta llama.

- **Funciones compatibles** : [Salida JSON](https://api-docs.deepseek.com/guides/json_mode) , [Llamadas a herramientas](https://api-docs.deepseek.com/guides/tool_calls) , [Finalización de chat](https://api-docs.deepseek.com/api/create-chat-completion) , [Finalización de prefijo de chat (Beta)](https://api-docs.deepseek.com/guides/chat_prefix_completion)

- **Funciones no compatibles** : FIM (Beta)

- **Parámetros no compatibles** : `temperature`、`top_p`、`presence_penalty`、`frequency_penalty`、`logprobs`、`top_logprobs`. Tenga en cuenta que, para garantizar la compatibilidad con el software existente, configurar `temperature`、`top_p`、`presence_penalty`、`frequency_penalty`no generará un error, pero tampoco tendrá ningún efecto. Configurar `logprobs`、`top_logprobs`generará un error.

## de varios turnos

En cada turno de la conversación, el modelo genera el CoT ( `reasoning_content`) y la respuesta final ( `content`). En el siguiente turno, el CoT de los turnos anteriores no se concatena en el contexto, como se ilustra en el siguiente diagrama:

![](https://api-docs.deepseek.com/img/deepseek_r1_multiround_example_en.jpeg)

## de API

El siguiente código, usando Python como ejemplo, demuestra cómo acceder al CoT y a la respuesta final, así como cómo mantener conversaciones multiturno. Tenga en cuenta que en el código del nuevo turno de conversación, solo `content`se pasa el de la salida del turno anterior, mientras que el `reasoning_content`se ignora.

- Sin transmisión
- 

```
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Turn 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

# Turn 2
messages.append({'role': 'assistant', 'content': content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)
# ...## de herramientas
```

* Transmisión

```
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Turn 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=True
)

reasoning_content = ""
content = ""

for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
    else:
        content += chunk.choices[0].delta.content

# Turn 2
messages.append({"role": "assistant", "content": content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=True
)
# ...
```

El modo de razonamiento del modelo DeepSeek ahora admite llamadas a herramientas. Antes de generar la respuesta final, el modelo puede realizar múltiples rondas de razonamiento y llamadas a herramientas para mejorar la calidad de la respuesta. El patrón de llamada se ilustra a continuación:

![](https://api-docs.deepseek.com/img/v3.2_thinking_with_tools_en.jpeg)

- Durante el proceso de respuesta a la pregunta 1 (Turnos 1.1 - 1.3), el modelo realizó varios turnos de razonamiento y llamadas a herramientas antes de proporcionar la respuesta. Durante este proceso, el usuario debe enviar el contenido del razonamiento ( `reasoning_content`) a la API para que el modelo pueda continuar el razonamiento.

- Al iniciar la siguiente pregunta del usuario (Turno 2.1), `reasoning_content`se debe eliminar la anterior, conservando los demás elementos para enviarlos a la API. Si `reasoning_content`se conserva y se envía a la API, esta lo ignorará.

### de compatibilidad

Dado que el proceso de invocación de la herramienta en modo de pensamiento requiere que los usuarios pasen la información `reasoning_content`a la API, si su código no la pasa correctamente `reasoning_content`, la API devolverá un error 400. Consulte el código de ejemplo a continuación para conocer la manera correcta.

### de muestra

A continuación se muestra un código de muestra simple para llamadas de herramientas en modo de pensamiento:

```
import os
import json
from openai import OpenAI

# The definition of the tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Get the current date",
            "parameters": { "type": "object", "properties": {} },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply the location and date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": { "type": "string", "description": "The city name" },
                    "date": { "type": "string", "description": "The date in format YYYY-mm-dd" },
                },
                "required": ["location", "date"]
            },
        }
    },
]

# The mocked version of the tool calls
def get_date_mock():
    return "2025-12-01"

def get_weather_mock(location, date):
    return "Cloudy 7~13°C"

TOOL_CALL_MAP = {
    "get_date": get_date_mock,
    "get_weather": get_weather_mock
}

def clear_reasoning_content(messages):
    for message in messages:
        if hasattr(message, 'reasoning_content'):
            message.reasoning_content = None

def run_turn(turn, messages):
    sub_turn = 1
    while True:
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=messages,
            tools=tools,
            extra_body={ "thinking": { "type": "enabled" } }
        )
        messages.append(response.choices[0].message)
        reasoning_content = response.choices[0].message.reasoning_content
        content = response.choices[0].message.content
        tool_calls = response.choices[0].message.tool_calls
        print(f"Turn {turn}.{sub_turn}\n{reasoning_content=}\n{content=}\n{tool_calls=}")
        # If there is no tool calls, then the model should get a final answer and we need to stop the loop
        if tool_calls is None:
            break
        for tool in tool_calls:
            tool_function = TOOL_CALL_MAP[tool.function.name]
            tool_result = tool_function(**json.loads(tool.function.arguments))
            print(f"tool result for {tool.function.name}: {tool_result}\n")
            messages.append({
                "role": "tool",
                "tool_call_id": tool.id,
                "content": tool_result,
            })
        sub_turn += 1

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('DEEPSEEK_BASE_URL'),
)

# The user starts a question
turn = 1
messages = [{
    "role": "user",
    "content": "How's the weather in Hangzhou Tomorrow"
}]
run_turn(turn, messages)

# The user starts a new question
turn = 2
messages.append({
    "role": "user",
    "content": "How's the weather in Hangzhou Tomorrow"
})
# We recommended to clear the reasoning_content in history messages so as to save network bandwidth
clear_reasoning_content(messages)
run_turn(turn, messages)
```

En cada subsolicitud del Turno 1, el `reasoning_content`generado durante ese turno se envía a la API, lo que permite que el modelo continúe con su razonamiento anterior. `response.choices[0].message`Contiene todos los campos necesarios para el `assistant`mensaje, incluyendo `content`, `reasoning_content`y `tool_calls`. Para simplificar, puede añadir el mensaje directamente al final de la lista de mensajes con el siguiente código:

```
messages.append(response.choices[0].message)
```

Esta línea de código es equivalente a:

```
messages.append({
    'role': 'assistant',
    'content': response.choices[0].message.content,
    'reasoning_content': response.choices[0].message.reasoning_content,
    'tool_calls': response.choices[0].message.tool_calls,
})
```

Al comienzo del Turno 2, recomendamos descartar los `reasoning_content`de turnos anteriores para ahorrar ancho de banda de red:

> clear_reasoning_content(messages)

El ejemplo de salida de este código es el siguiente:

```
Turn 1.1
reasoning_content="The user is asking about the weather in Hangzhou tomorrow. I need to get the current date first, then calculate tomorrow's date, and then call the weather API. Let me start by getting the current date."
content=''
tool_calls=[ChatCompletionMessageToolCall(id='call_00_Tcek83ZQ4fFb1RfPQnsPEE5w', function=Function(arguments='{}', name='get_date'), type='function', index=0)]
tool_result(get_date): 2025-12-01

Turn 1.2
reasoning_content='Today is December 1, 2025. Tomorrow is December 2, 2025. I need to format the date as YYYY-mm-dd: "2025-12-02". Now I can call get_weather with location Hangzhou and date 2025-12-02.'
content=''
tool_calls=[ChatCompletionMessageToolCall(id='call_00_V0Uwt4i63m5QnWRS1q1AO1tP', function=Function(arguments='{"location": "Hangzhou", "date": "2025-12-02"}', name='get_weather'), type='function', index=0)]
tool_result(get_weather): Cloudy 7~13°C

Turn 1.3
reasoning_content="I have the weather information: Cloudy with temperatures between 7 and 13°C. I should respond in a friendly, helpful manner. I'll mention that it's for tomorrow (December 2, 2025) and give the details. I can also ask if they need any other information. Let's craft the response."
content="Tomorrow (Tuesday, December 2, 2025) in Hangzhou will be **cloudy** with temperatures ranging from **7°C to 13°C**.  \n\nIt might be a good idea to bring a light jacket if you're heading out. Is there anything else you'd like to know about the weather?"
tool_calls=None

Turn 2.1
reasoning_content="The user wants clothing advice for tomorrow based on the weather in Hangzhou. I know tomorrow's weather: cloudy, 7-13°C. That's cool but not freezing. I should suggest layered clothing, maybe a jacket, long pants, etc. I can also mention that since it's cloudy, an umbrella might not be needed unless there's rain chance, but the forecast didn't mention rain. I should be helpful and give specific suggestions. I can also ask if they have any specific activities planned to tailor the advice. Let me respond."
content="Based on tomorrow's forecast of **cloudy weather with temperatures between 7°C and 13°C** in Hangzhou, here are some clothing suggestions:\n\n**Recommended outfit:**\n- **Upper body:** A long-sleeve shirt or sweater, plus a light to medium jacket (like a fleece, windbreaker, or light coat)\n- **Lower body:** Long pants or jeans\n- **Footwear:** Closed-toe shoes or sneakers\n- **Optional:** A scarf or light hat for extra warmth, especially in the morning and evening\n\n**Why this works:**\n- The temperature range is cool but not freezing, so layering is key\n- Since it's cloudy but no rain mentioned, you likely won't need an umbrella\n- The jacket will help with the morning chill (7°C) and can be removed if you warm up during the day\n\n**If you have specific plans:**\n- For outdoor activities: Consider adding an extra layer\n- For indoor/office settings: The layered approach allows you to adjust comfortably\n\nWould you like more specific advice based on your planned activities?"
tool_calls=None
```

# # Lists Models

GET

## https://api.deepseek.com/models

Lists the currently available models, and provides basic information about each one such as the owner and availability. Check [Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing) for our currently supported models.

## Responses

- 200

OK, returns A list of models

- application/json

- Schema

- Example (from schema)

- Example

```
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-chat",
      "object": "model",
      "owned_by": "deepseek"
    },
    {
      "id": "deepseek-reasoner",
      "object": "model",
      "owned_by": "deepseek"
    }
  ]
}## https://api.deepseek.com/models
```

const axios = require('axios');  

let config = {  
method: 'get',  
maxBodyLength: Infinity,  
url: 'https://api.deepseek.com/models',  
headers: {  
'Accept': 'application/json',  
'Authorization': 'Bearer <TOKEN>'  
}  
};  

axios(config)  
.then((response) => {  
console.log(JSON.stringify(response.data));  
})  
.catch((error) => {  
console.log(error);  
});

- OpenAI SDK

```
import OpenAI from "openai";

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `baseURL`.
const openai = new OpenAI({
        baseURL: 'https://api.deepseek.com',
        apiKey: '<your API key>'
});

async function main() {
  const models = await openai.models.list()
  for await (const model of models) {
    console.log(model);
  }
}

main();AXIOS
```

- NATIVE

```
const axios = require('axios');

let config = {
  method: 'get',
maxBodyLength: Infinity,
  url: 'https://api.deepseek.com/models',
  headers: { 
    'Accept': 'application/json', 
    'Authorization': 'Bearer <TOKEN>'
  }
};

axios(config)
.then((response) => {
  console.log(JSON.stringify(response.data));
})
.catch((error) => {
  console.log(error);
});
```

# Obtener saldo de usuario




```
const axios = require('axios');

let config = {
  method: 'get',
maxBodyLength: Infinity,
  url: 'https://api.deepseek.com/user/balance',
  headers: { 
    'Accept': 'application/json', 
    'Authorization': 'Bearer <TOKEN>'
  }
};

axios(config)
.then((response) => {
  console.log(JSON.stringify(response.data));
})
.catch((error) => {
  console.log(error);
});
```

