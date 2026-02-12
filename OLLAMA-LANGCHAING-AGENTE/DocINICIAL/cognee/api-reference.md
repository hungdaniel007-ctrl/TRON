# maestro.md - Contenido de: /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference

**Extensiones procesadas:** `.md`

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/introduction.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# API Reference

> Complete API documentation for Cognee's knowledge graph platform

# Cognee API Reference

Welcome to the Cognee API documentation. This comprehensive reference covers all endpoints for building, managing, and querying your memory using Cognee's powerful platform.

## Getting Started

Before using the API, you need to choose how to run Cognee. You have two main options:

<CardGroup cols={2}>
  <Card title="Cognee Cloud" href="/how-to-guides/cognee-cloud/index" icon="cloud">
    **Managed Cloud Platform**

    Production-ready, fully managed service with automatic scaling and enterprise features.
  </Card>

  <Card title="Local Docker Setup" icon="docker">
    **Self-Hosted Development**

    Run Cognee locally using Docker for development, testing, and custom deployments.
  </Card>
</CardGroup>

## Setup Options

<Tabs>
  <Tab title="Cognee Cloud">
    **Managed Service - Recommended for Production**

    1. **Sign up** at [platform.cognee.ai](https://platform.cognee.ai/)
    2. **Create API Key** in your dashboard
    3. **Start using** the API immediately

    ```bash  theme={null}
    # Base URL for Cognee Cloud
    BASE_URL="https://api.cognee.ai"

    # Authentication
    curl -H "X-Api-Key: YOUR-API-KEY" \
         -H "Content-Type: application/json" \
         $BASE_URL/api/health
    ```

    <Info>
      Cognee Cloud provides enterprise-grade infrastructure with automatic scaling, managed databases, and 24/7 monitoring.
    </Info>
  </Tab>

  <Tab title="Local Docker">
    **Self-Hosted - Perfect for Development**

    Quick start with Docker (single command):

    ```bash  theme={null}
    # Create environment file
    echo 'LLM_API_KEY="your_openai_api_key"' > .env

    # Run Cognee container
    docker run --env-file ./.env -p 8000:8000 --rm -it cognee/cognee:main
    ```

    Or use Docker Compose from the [Cognee repository](https://github.com/topoteretes/cognee):

    ```bash  theme={null}
    # Clone repository
    git clone https://github.com/topoteretes/cognee.git
    cd cognee

    # Set up environment
    cp .env.template .env
    # Edit .env with your API keys

    # Start with Docker Compose
    docker-compose up -d
    ```

    <Note>
      Local setup uses embedded databases by default (SQLite, LanceDB, NetworkX) for easy development.
    </Note>
  </Tab>
</Tabs>

## API Base URLs

<AccordionGroup>
  <Accordion title="Production (Cognee Cloud)" defaultOpen>
    ```
    https://api.cognee.ai
    ```

    **Authentication**: X-Api-Key header
    **Rate Limits**: Based on your subscription plan
    **Availability**: 99.9% uptime SLA
  </Accordion>

  <Accordion title="Local Development">
    ```
    http://localhost:8000
    ```

    **Authentication**: Optional (can be disabled for local development)
    **Rate Limits**: None
    **Availability**: Depends on your local setup
  </Accordion>
</AccordionGroup>

## Authentication

<Tabs>
  <Tab title="Cognee Cloud">
    **API Key Authentication**

    All requests require an API key in the header:

    ```http  theme={null}
    X-Api-Key: YOUR-API-KEY
    Content-Type: application/json
    ```

    Get your API key from the [Cognee Cloud dashboard](https://platform.cognee.ai/).
  </Tab>

  <Tab title="Local Docker">
    **Optional Authentication**

    Local development typically runs without authentication:

    ```http  theme={null}
    Content-Type: application/json
    ```

    To enable authentication locally, set `REQUIRE_AUTH=true` in your `.env` file.
  </Tab>
</Tabs>

## Core API Endpoints

The Cognee API provides endpoints for the complete knowledge graph lifecycle:

<CardGroup cols={2}>
  <Card title="Data Ingestion" icon="plus">
    **`POST /api/add`**

    Add text, documents, or structured data to your knowledge base.
  </Card>

  <Card title="Knowledge Processing" icon="brain">
    **`POST /api/cognify`**

    Transform raw data into structured knowledge graphs with entities and relationships.
  </Card>

  <Card title="Semantic Search" icon="search">
    **`POST /api/search`**

    Query your knowledge graph using natural language or structured queries.
  </Card>

  <Card title="Data Management" icon="trash">
    **`DELETE /api/delete`**

    Remove specific data items or entire datasets from your knowledge base.
  </Card>
</CardGroup>

## API Features

<AccordionGroup>
  <Accordion title="Multiple Search Types">
    Choose from different search modes based on your needs:

    * **`GRAPH_COMPLETION`**: LLM-powered responses with graph context
    * **`CHUNKS`**: Raw text segments matching your query
    * **`SUMMARIES`**: Pre-generated hierarchical summaries
    * **`INSIGHTS`**: Structured entity relationships
    * **`CODE`**: Code-specific search with syntax understanding
  </Accordion>

  <Accordion title="Flexible Data Formats">
    Support for various input formats locally and strings on Cognee Cloud:

    * **Text**: Raw text strings, documents, articles
    * **Structured**: JSON, CSV, XML data
    * **Code**: Source code files and repositories
    * **URLs**: Web pages and online content
  </Accordion>
</AccordionGroup>

## Quick Example

Here's a complete example using the API:

<CodeGroup>
  ```python Python theme={null}
  import requests

  # Configuration
  BASE_URL = "http://localhost:8000"  # or https://api.cognee.ai for Cognee Cloud
  API_KEY = "your-api-key"  # only for Cognee Cloud

  headers = {
      "Content-Type": "application/json",
      "X-Api-Key": API_KEY  # only for Cognee Cloud
  }

  # 1. Add data
  add_response = requests.post(
      f"{BASE_URL}/api/add",
      json={"data": "AI is transforming how we work and live."},
      headers=headers
  )

  # 2. Process into knowledge graph
  cognify_response = requests.post(
      f"{BASE_URL}/api/cognify",
      json={"datasets": ["main_dataset"]},
      headers=headers
  )

  # 3. Search the knowledge graph
  search_response = requests.post(
      f"{BASE_URL}/api/search",
      json={
          "query": "What is AI?",
          "search_type": "GRAPH_COMPLETION"
      },
      headers=headers
  )

  print(search_response.json())
  ```

  ```curl cURL theme={null}
  # 1. Add data
  curl -X POST "http://localhost:8000/api/add" \
    -H "Content-Type: application/json" \
    -d '{"data": "AI is transforming how we work and live."}'

  # 2. Process into knowledge graph
  curl -X POST "http://localhost:8000/api/cognify" \
    -H "Content-Type: application/json" \
    -d '{"datasets": ["main_dataset"]}'

  # 3. Search the knowledge graph
  curl -X POST "http://localhost:8000/api/search" \
    -H "Content-Type: application/json" \
    -d '{
      "query": "What is AI?",
      "search_type": "GRAPH_COMPLETION"
    }'
  ```
</CodeGroup>

## Interactive API Explorer

<Card title="OpenAPI Specification" icon="play">
  **Try the API interactively**

  All endpoints below are automatically generated from our OpenAPI specification, providing interactive examples and real-time testing capabilities.
</Card>

## Error Handling

All API endpoints return standard HTTP status codes:

* **200**: Success
* **400**: Bad Request - Invalid parameters
* **401**: Unauthorized - Invalid or missing API key
* **404**: Not Found - Resource doesn't exist
* **429**: Too Many Requests - Rate limit exceeded
* **500**: Internal Server Error - Server-side error

<Warning>
  Always implement proper error handling in your applications to gracefully handle API failures and rate limits.
</Warning>

## Next Steps

<CardGroup cols={2}>
  <Card title="Explore Endpoints" icon="list">
    **API Documentation**

    Browse all available endpoints with interactive examples below.
  </Card>

  <Card title="Community Support" href="https://discord.gg/m63hxKsp4p" icon="discord">
    **Get Help**

    Join our Discord community for support and discussions.
  </Card>
</CardGroup>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/settings/get-settings.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Settings

> Get the current system settings.

This endpoint retrieves the current configuration settings for the system,
including LLM (Large Language Model) configuration and vector database
configuration. These settings determine how the system processes and stores data.

## Response
Returns the current system settings containing:
- **llm**: LLM configuration (provider, model, API key)
- **vector_db**: Vector database configuration (provider, URL, API key)

## Error Codes
- **500 Internal Server Error**: Error retrieving settings



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/settings
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/settings:
    get:
      tags:
        - settings
      summary: Get Settings
      description: >-
        Get the current system settings.


        This endpoint retrieves the current configuration settings for the
        system,

        including LLM (Large Language Model) configuration and vector database

        configuration. These settings determine how the system processes and
        stores data.


        ## Response

        Returns the current system settings containing:

        - **llm**: LLM configuration (provider, model, API key)

        - **vector_db**: Vector database configuration (provider, URL, API key)


        ## Error Codes

        - **500 Internal Server Error**: Error retrieving settings
      operationId: get_settings_api_v1_settings_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SettingsDTO'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    SettingsDTO:
      properties:
        llm:
          $ref: '#/components/schemas/LLMConfigOutputDTO'
        vectorDb:
          $ref: '#/components/schemas/VectorDBConfigOutputDTO'
      type: object
      required:
        - llm
        - vectorDb
      title: SettingsDTO
    LLMConfigOutputDTO:
      properties:
        apiKey:
          type: string
          title: Apikey
        model:
          type: string
          title: Model
        provider:
          type: string
          title: Provider
        endpoint:
          anyOf:
            - type: string
            - type: 'null'
          title: Endpoint
        apiVersion:
          anyOf:
            - type: string
            - type: 'null'
          title: Apiversion
        models:
          additionalProperties:
            items:
              $ref: '#/components/schemas/ConfigChoice'
            type: array
          type: object
          title: Models
        providers:
          items:
            $ref: '#/components/schemas/ConfigChoice'
          type: array
          title: Providers
      type: object
      required:
        - apiKey
        - model
        - provider
        - endpoint
        - apiVersion
        - models
        - providers
      title: LLMConfigOutputDTO
    VectorDBConfigOutputDTO:
      properties:
        apiKey:
          type: string
          title: Apikey
        url:
          type: string
          title: Url
        provider:
          type: string
          title: Provider
        providers:
          items:
            $ref: '#/components/schemas/ConfigChoice'
          type: array
          title: Providers
      type: object
      required:
        - apiKey
        - url
        - provider
        - providers
      title: VectorDBConfigOutputDTO
    ConfigChoice:
      properties:
        value:
          type: string
          title: Value
        label:
          type: string
          title: Label
      type: object
      required:
        - value
        - label
      title: ConfigChoice
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/settings/save-settings.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Save Settings

> Save or update system settings.

This endpoint allows updating the system configuration settings. You can
update either the LLM configuration, vector database configuration, or both.
Only provided settings will be updated; others remain unchanged.

## Request Parameters
- **llm** (Optional[LLMConfigInputDTO]): LLM configuration (provider, model, API key)
- **vector_db** (Optional[VectorDBConfigInputDTO]): Vector database configuration (provider, URL, API key)

## Response
No content returned on successful save.

## Error Codes
- **400 Bad Request**: Invalid settings provided
- **500 Internal Server Error**: Error saving settings



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/settings
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/settings:
    post:
      tags:
        - settings
      summary: Save Settings
      description: >-
        Save or update system settings.


        This endpoint allows updating the system configuration settings. You can

        update either the LLM configuration, vector database configuration, or
        both.

        Only provided settings will be updated; others remain unchanged.


        ## Request Parameters

        - **llm** (Optional[LLMConfigInputDTO]): LLM configuration (provider,
        model, API key)

        - **vector_db** (Optional[VectorDBConfigInputDTO]): Vector database
        configuration (provider, URL, API key)


        ## Response

        No content returned on successful save.


        ## Error Codes

        - **400 Bad Request**: Invalid settings provided

        - **500 Internal Server Error**: Error saving settings
      operationId: save_settings_api_v1_settings_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SettingsPayloadDTO'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    SettingsPayloadDTO:
      properties:
        llm:
          anyOf:
            - $ref: '#/components/schemas/LLMConfigInputDTO'
            - type: 'null'
        vectorDb:
          anyOf:
            - $ref: '#/components/schemas/VectorDBConfigInputDTO'
            - type: 'null'
      type: object
      title: SettingsPayloadDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    LLMConfigInputDTO:
      properties:
        provider:
          anyOf:
            - type: string
              const: openai
            - type: string
              const: ollama
            - type: string
              const: anthropic
            - type: string
              const: gemini
          title: Provider
        model:
          type: string
          title: Model
        apiKey:
          type: string
          title: Apikey
      type: object
      required:
        - provider
        - model
        - apiKey
      title: LLMConfigInputDTO
    VectorDBConfigInputDTO:
      properties:
        provider:
          anyOf:
            - type: string
              const: lancedb
            - type: string
              const: chromadb
            - type: string
              const: pgvector
          title: Provider
        url:
          type: string
          title: Url
        apiKey:
          type: string
          title: Apikey
      type: object
      required:
        - provider
        - url
        - apiKey
      title: VectorDBConfigInputDTO
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/verify:request-token.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Verify:Request-Token



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/request-verify-token
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/request-verify-token:
    post:
      tags:
        - auth
      summary: Verify:Request-Token
      operationId: verify_request_token_api_v1_auth_request_verify_token_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_verify_request_token_api_v1_auth_request_verify_token_post
        required: true
      responses:
        '202':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_verify_request_token_api_v1_auth_request_verify_token_post:
      properties:
        email:
          type: string
          format: email
          title: Email
      type: object
      required:
        - email
      title: Body_verify_request_token_api_v1_auth_request_verify_token_post
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/auth:cookielogin.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Auth:Cookie.Login



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/login
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/login:
    post:
      tags:
        - auth
      summary: Auth:Cookie.Login
      operationId: auth_cookie_login_api_v1_auth_login_post
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema:
              $ref: >-
                #/components/schemas/Body_auth_cookie_login_api_v1_auth_login_post
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '204':
          description: No Content
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                LOGIN_BAD_CREDENTIALS:
                  summary: Bad credentials or the user is inactive.
                  value:
                    detail: LOGIN_BAD_CREDENTIALS
                LOGIN_USER_NOT_VERIFIED:
                  summary: The user is not verified.
                  value:
                    detail: LOGIN_USER_NOT_VERIFIED
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_auth_cookie_login_api_v1_auth_login_post:
      properties:
        grant_type:
          anyOf:
            - type: string
              pattern: ^password$
            - type: 'null'
          title: Grant Type
        username:
          type: string
          title: Username
        password:
          type: string
          format: password
          title: Password
        scope:
          type: string
          title: Scope
          default: ''
        client_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Client Id
        client_secret:
          anyOf:
            - type: string
            - type: 'null'
          format: password
          title: Client Secret
      type: object
      required:
        - username
        - password
      title: Body_auth_cookie_login_api_v1_auth_login_post
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/verify:verify.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Verify:Verify



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/verify
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/verify:
    post:
      tags:
        - auth
      summary: Verify:Verify
      operationId: verify_verify_api_v1_auth_verify_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Body_verify_verify_api_v1_auth_verify_post'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                VERIFY_USER_BAD_TOKEN:
                  summary: >-
                    Bad token, not existing user ornot the e-mail currently set
                    for the user.
                  value:
                    detail: VERIFY_USER_BAD_TOKEN
                VERIFY_USER_ALREADY_VERIFIED:
                  summary: The user is already verified.
                  value:
                    detail: VERIFY_USER_ALREADY_VERIFIED
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_verify_verify_api_v1_auth_verify_post:
      properties:
        token:
          type: string
          title: Token
      type: object
      required:
        - token
      title: Body_verify_verify_api_v1_auth_verify_post
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/reset:forgot-password.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Reset:Forgot Password



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/forgot-password
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/forgot-password:
    post:
      tags:
        - auth
      summary: Reset:Forgot Password
      operationId: reset_forgot_password_api_v1_auth_forgot_password_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_reset_forgot_password_api_v1_auth_forgot_password_post
        required: true
      responses:
        '202':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_reset_forgot_password_api_v1_auth_forgot_password_post:
      properties:
        email:
          type: string
          format: email
          title: Email
      type: object
      required:
        - email
      title: Body_reset_forgot_password_api_v1_auth_forgot_password_post
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/auth:cookielogout.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Auth:Cookie.Logout



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/logout
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/logout:
    post:
      tags:
        - auth
      summary: Auth:Cookie.Logout
      operationId: auth_cookie_logout_api_v1_auth_logout_post
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '204':
          description: No Content
        '401':
          description: Missing token or inactive user.
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/reset:reset-password.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Reset:Reset Password



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/reset-password
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/reset-password:
    post:
      tags:
        - auth
      summary: Reset:Reset Password
      operationId: reset_reset_password_api_v1_auth_reset_password_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_reset_reset_password_api_v1_auth_reset_password_post
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                RESET_PASSWORD_BAD_TOKEN:
                  summary: Bad or expired token.
                  value:
                    detail: RESET_PASSWORD_BAD_TOKEN
                RESET_PASSWORD_INVALID_PASSWORD:
                  summary: Password validation failed.
                  value:
                    detail:
                      code: RESET_PASSWORD_INVALID_PASSWORD
                      reason: Password should be at least 3 characters
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_reset_reset_password_api_v1_auth_reset_password_post:
      properties:
        token:
          type: string
          title: Token
        password:
          type: string
          title: Password
      type: object
      required:
        - token
        - password
      title: Body_reset_reset_password_api_v1_auth_reset_password_post
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/register:register.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Register:Register



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/register
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/register:
    post:
      tags:
        - auth
      summary: Register:Register
      operationId: register_register_api_v1_auth_register_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
        required: true
      responses:
        '201':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                REGISTER_USER_ALREADY_EXISTS:
                  summary: A user with this email already exists.
                  value:
                    detail: REGISTER_USER_ALREADY_EXISTS
                REGISTER_INVALID_PASSWORD:
                  summary: Password validation failed.
                  value:
                    detail:
                      code: REGISTER_INVALID_PASSWORD
                      reason: Password should beat least 3 characters
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    UserCreate:
      properties:
        email:
          type: string
          format: email
          title: Email
        password:
          type: string
          title: Password
        is_active:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Active
          default: true
        is_superuser:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: true
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - email
        - password
      title: UserCreate
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/maestro.md

```
# maestro.md - Contenido de: /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference

**Extensiones procesadas:** `.md`

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/introduction.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# API Reference

> Complete API documentation for Cognee's knowledge graph platform

# Cognee API Reference

Welcome to the Cognee API documentation. This comprehensive reference covers all endpoints for building, managing, and querying your memory using Cognee's powerful platform.

## Getting Started

Before using the API, you need to choose how to run Cognee. You have two main options:

<CardGroup cols={2}>
  <Card title="Cognee Cloud" href="/how-to-guides/cognee-cloud/index" icon="cloud">
    **Managed Cloud Platform**

    Production-ready, fully managed service with automatic scaling and enterprise features.
  </Card>

  <Card title="Local Docker Setup" icon="docker">
    **Self-Hosted Development**

    Run Cognee locally using Docker for development, testing, and custom deployments.
  </Card>
</CardGroup>

## Setup Options

<Tabs>
  <Tab title="Cognee Cloud">
    **Managed Service - Recommended for Production**

    1. **Sign up** at [platform.cognee.ai](https://platform.cognee.ai/)
    2. **Create API Key** in your dashboard
    3. **Start using** the API immediately

    ```bash  theme={null}
    # Base URL for Cognee Cloud
    BASE_URL="https://api.cognee.ai"

    # Authentication
    curl -H "X-Api-Key: YOUR-API-KEY" \
         -H "Content-Type: application/json" \
         $BASE_URL/api/health
    ```

    <Info>
      Cognee Cloud provides enterprise-grade infrastructure with automatic scaling, managed databases, and 24/7 monitoring.
    </Info>
  </Tab>

  <Tab title="Local Docker">
    **Self-Hosted - Perfect for Development**

    Quick start with Docker (single command):

    ```bash  theme={null}
    # Create environment file
    echo 'LLM_API_KEY="your_openai_api_key"' > .env

    # Run Cognee container
    docker run --env-file ./.env -p 8000:8000 --rm -it cognee/cognee:main
    ```

    Or use Docker Compose from the [Cognee repository](https://github.com/topoteretes/cognee):

    ```bash  theme={null}
    # Clone repository
    git clone https://github.com/topoteretes/cognee.git
    cd cognee

    # Set up environment
    cp .env.template .env
    # Edit .env with your API keys

    # Start with Docker Compose
    docker-compose up -d
    ```

    <Note>
      Local setup uses embedded databases by default (SQLite, LanceDB, NetworkX) for easy development.
    </Note>
  </Tab>
</Tabs>

## API Base URLs

<AccordionGroup>
  <Accordion title="Production (Cognee Cloud)" defaultOpen>
    ```
    https://api.cognee.ai
    ```

    **Authentication**: X-Api-Key header
    **Rate Limits**: Based on your subscription plan
    **Availability**: 99.9% uptime SLA
  </Accordion>

  <Accordion title="Local Development">
    ```
    http://localhost:8000
    ```

    **Authentication**: Optional (can be disabled for local development)
    **Rate Limits**: None
    **Availability**: Depends on your local setup
  </Accordion>
</AccordionGroup>

## Authentication

<Tabs>
  <Tab title="Cognee Cloud">
    **API Key Authentication**

    All requests require an API key in the header:

    ```http  theme={null}
    X-Api-Key: YOUR-API-KEY
    Content-Type: application/json
    ```

    Get your API key from the [Cognee Cloud dashboard](https://platform.cognee.ai/).
  </Tab>

  <Tab title="Local Docker">
    **Optional Authentication**

    Local development typically runs without authentication:

    ```http  theme={null}
    Content-Type: application/json
    ```

    To enable authentication locally, set `REQUIRE_AUTH=true` in your `.env` file.
  </Tab>
</Tabs>

## Core API Endpoints

The Cognee API provides endpoints for the complete knowledge graph lifecycle:

<CardGroup cols={2}>
  <Card title="Data Ingestion" icon="plus">
    **`POST /api/add`**

    Add text, documents, or structured data to your knowledge base.
  </Card>

  <Card title="Knowledge Processing" icon="brain">
    **`POST /api/cognify`**

    Transform raw data into structured knowledge graphs with entities and relationships.
  </Card>

  <Card title="Semantic Search" icon="search">
    **`POST /api/search`**

    Query your knowledge graph using natural language or structured queries.
  </Card>

  <Card title="Data Management" icon="trash">
    **`DELETE /api/delete`**

    Remove specific data items or entire datasets from your knowledge base.
  </Card>
</CardGroup>

## API Features

<AccordionGroup>
  <Accordion title="Multiple Search Types">
    Choose from different search modes based on your needs:

    * **`GRAPH_COMPLETION`**: LLM-powered responses with graph context
    * **`CHUNKS`**: Raw text segments matching your query
    * **`SUMMARIES`**: Pre-generated hierarchical summaries
    * **`INSIGHTS`**: Structured entity relationships
    * **`CODE`**: Code-specific search with syntax understanding
  </Accordion>

  <Accordion title="Flexible Data Formats">
    Support for various input formats locally and strings on Cognee Cloud:

    * **Text**: Raw text strings, documents, articles
    * **Structured**: JSON, CSV, XML data
    * **Code**: Source code files and repositories
    * **URLs**: Web pages and online content
  </Accordion>
</AccordionGroup>

## Quick Example

Here's a complete example using the API:

<CodeGroup>
  ```python Python theme={null}
  import requests

  # Configuration
  BASE_URL = "http://localhost:8000"  # or https://api.cognee.ai for Cognee Cloud
  API_KEY = "your-api-key"  # only for Cognee Cloud

  headers = {
      "Content-Type": "application/json",
      "X-Api-Key": API_KEY  # only for Cognee Cloud
  }

  # 1. Add data
  add_response = requests.post(
      f"{BASE_URL}/api/add",
      json={"data": "AI is transforming how we work and live."},
      headers=headers
  )

  # 2. Process into knowledge graph
  cognify_response = requests.post(
      f"{BASE_URL}/api/cognify",
      json={"datasets": ["main_dataset"]},
      headers=headers
  )

  # 3. Search the knowledge graph
  search_response = requests.post(
      f"{BASE_URL}/api/search",
      json={
          "query": "What is AI?",
          "search_type": "GRAPH_COMPLETION"
      },
      headers=headers
  )

  print(search_response.json())
  ```

  ```curl cURL theme={null}
  # 1. Add data
  curl -X POST "http://localhost:8000/api/add" \
    -H "Content-Type: application/json" \
    -d '{"data": "AI is transforming how we work and live."}'

  # 2. Process into knowledge graph
  curl -X POST "http://localhost:8000/api/cognify" \
    -H "Content-Type: application/json" \
    -d '{"datasets": ["main_dataset"]}'

  # 3. Search the knowledge graph
  curl -X POST "http://localhost:8000/api/search" \
    -H "Content-Type: application/json" \
    -d '{
      "query": "What is AI?",
      "search_type": "GRAPH_COMPLETION"
    }'
  ```
</CodeGroup>

## Interactive API Explorer

<Card title="OpenAPI Specification" icon="play">
  **Try the API interactively**

  All endpoints below are automatically generated from our OpenAPI specification, providing interactive examples and real-time testing capabilities.
</Card>

## Error Handling

All API endpoints return standard HTTP status codes:

* **200**: Success
* **400**: Bad Request - Invalid parameters
* **401**: Unauthorized - Invalid or missing API key
* **404**: Not Found - Resource doesn't exist
* **429**: Too Many Requests - Rate limit exceeded
* **500**: Internal Server Error - Server-side error

<Warning>
  Always implement proper error handling in your applications to gracefully handle API failures and rate limits.
</Warning>

## Next Steps

<CardGroup cols={2}>
  <Card title="Explore Endpoints" icon="list">
    **API Documentation**

    Browse all available endpoints with interactive examples below.
  </Card>

  <Card title="Community Support" href="https://discord.gg/m63hxKsp4p" icon="discord">
    **Get Help**

    Join our Discord community for support and discussions.
  </Card>
</CardGroup>

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/settings/get-settings.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Settings

> Get the current system settings.

This endpoint retrieves the current configuration settings for the system,
including LLM (Large Language Model) configuration and vector database
configuration. These settings determine how the system processes and stores data.

## Response
Returns the current system settings containing:
- **llm**: LLM configuration (provider, model, API key)
- **vector_db**: Vector database configuration (provider, URL, API key)

## Error Codes
- **500 Internal Server Error**: Error retrieving settings



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/settings
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/settings:
    get:
      tags:
        - settings
      summary: Get Settings
      description: >-
        Get the current system settings.


        This endpoint retrieves the current configuration settings for the
        system,

        including LLM (Large Language Model) configuration and vector database

        configuration. These settings determine how the system processes and
        stores data.


        ## Response

        Returns the current system settings containing:

        - **llm**: LLM configuration (provider, model, API key)

        - **vector_db**: Vector database configuration (provider, URL, API key)


        ## Error Codes

        - **500 Internal Server Error**: Error retrieving settings
      operationId: get_settings_api_v1_settings_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SettingsDTO'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    SettingsDTO:
      properties:
        llm:
          $ref: '#/components/schemas/LLMConfigOutputDTO'
        vectorDb:
          $ref: '#/components/schemas/VectorDBConfigOutputDTO'
      type: object
      required:
        - llm
        - vectorDb
      title: SettingsDTO
    LLMConfigOutputDTO:
      properties:
        apiKey:
          type: string
          title: Apikey
        model:
          type: string
          title: Model
        provider:
          type: string
          title: Provider
        endpoint:
          anyOf:
            - type: string
            - type: 'null'
          title: Endpoint
        apiVersion:
          anyOf:
            - type: string
            - type: 'null'
          title: Apiversion
        models:
          additionalProperties:
            items:
              $ref: '#/components/schemas/ConfigChoice'
            type: array
          type: object
          title: Models
        providers:
          items:
            $ref: '#/components/schemas/ConfigChoice'
          type: array
          title: Providers
      type: object
      required:
        - apiKey
        - model
        - provider
        - endpoint
        - apiVersion
        - models
        - providers
      title: LLMConfigOutputDTO
    VectorDBConfigOutputDTO:
      properties:
        apiKey:
          type: string
          title: Apikey
        url:
          type: string
          title: Url
        provider:
          type: string
          title: Provider
        providers:
          items:
            $ref: '#/components/schemas/ConfigChoice'
          type: array
          title: Providers
      type: object
      required:
        - apiKey
        - url
        - provider
        - providers
      title: VectorDBConfigOutputDTO
    ConfigChoice:
      properties:
        value:
          type: string
          title: Value
        label:
          type: string
          title: Label
      type: object
      required:
        - value
        - label
      title: ConfigChoice
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/settings/save-settings.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Save Settings

> Save or update system settings.

This endpoint allows updating the system configuration settings. You can
update either the LLM configuration, vector database configuration, or both.
Only provided settings will be updated; others remain unchanged.

## Request Parameters
- **llm** (Optional[LLMConfigInputDTO]): LLM configuration (provider, model, API key)
- **vector_db** (Optional[VectorDBConfigInputDTO]): Vector database configuration (provider, URL, API key)

## Response
No content returned on successful save.

## Error Codes
- **400 Bad Request**: Invalid settings provided
- **500 Internal Server Error**: Error saving settings



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/settings
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/settings:
    post:
      tags:
        - settings
      summary: Save Settings
      description: >-
        Save or update system settings.


        This endpoint allows updating the system configuration settings. You can

        update either the LLM configuration, vector database configuration, or
        both.

        Only provided settings will be updated; others remain unchanged.


        ## Request Parameters

        - **llm** (Optional[LLMConfigInputDTO]): LLM configuration (provider,
        model, API key)

        - **vector_db** (Optional[VectorDBConfigInputDTO]): Vector database
        configuration (provider, URL, API key)


        ## Response

        No content returned on successful save.


        ## Error Codes

        - **400 Bad Request**: Invalid settings provided

        - **500 Internal Server Error**: Error saving settings
      operationId: save_settings_api_v1_settings_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SettingsPayloadDTO'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    SettingsPayloadDTO:
      properties:
        llm:
          anyOf:
            - $ref: '#/components/schemas/LLMConfigInputDTO'
            - type: 'null'
        vectorDb:
          anyOf:
            - $ref: '#/components/schemas/VectorDBConfigInputDTO'
            - type: 'null'
      type: object
      title: SettingsPayloadDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    LLMConfigInputDTO:
      properties:
        provider:
          anyOf:
            - type: string
              const: openai
            - type: string
              const: ollama
            - type: string
              const: anthropic
            - type: string
              const: gemini
          title: Provider
        model:
          type: string
          title: Model
        apiKey:
          type: string
          title: Apikey
      type: object
      required:
        - provider
        - model
        - apiKey
      title: LLMConfigInputDTO
    VectorDBConfigInputDTO:
      properties:
        provider:
          anyOf:
            - type: string
              const: lancedb
            - type: string
              const: chromadb
            - type: string
              const: pgvector
          title: Provider
        url:
          type: string
          title: Url
        apiKey:
          type: string
          title: Apikey
      type: object
      required:
        - provider
        - url
        - apiKey
      title: VectorDBConfigInputDTO
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/verify:request-token.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Verify:Request-Token



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/request-verify-token
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/request-verify-token:
    post:
      tags:
        - auth
      summary: Verify:Request-Token
      operationId: verify_request_token_api_v1_auth_request_verify_token_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_verify_request_token_api_v1_auth_request_verify_token_post
        required: true
      responses:
        '202':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_verify_request_token_api_v1_auth_request_verify_token_post:
      properties:
        email:
          type: string
          format: email
          title: Email
      type: object
      required:
        - email
      title: Body_verify_request_token_api_v1_auth_request_verify_token_post
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/auth:cookielogin.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Auth:Cookie.Login



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/login
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/login:
    post:
      tags:
        - auth
      summary: Auth:Cookie.Login
      operationId: auth_cookie_login_api_v1_auth_login_post
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema:
              $ref: >-
                #/components/schemas/Body_auth_cookie_login_api_v1_auth_login_post
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '204':
          description: No Content
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                LOGIN_BAD_CREDENTIALS:
                  summary: Bad credentials or the user is inactive.
                  value:
                    detail: LOGIN_BAD_CREDENTIALS
                LOGIN_USER_NOT_VERIFIED:
                  summary: The user is not verified.
                  value:
                    detail: LOGIN_USER_NOT_VERIFIED
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_auth_cookie_login_api_v1_auth_login_post:
      properties:
        grant_type:
          anyOf:
            - type: string
              pattern: ^password$
            - type: 'null'
          title: Grant Type
        username:
          type: string
          title: Username
        password:
          type: string
          format: password
          title: Password
        scope:
          type: string
          title: Scope
          default: ''
        client_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Client Id
        client_secret:
          anyOf:
            - type: string
            - type: 'null'
          format: password
          title: Client Secret
      type: object
      required:
        - username
        - password
      title: Body_auth_cookie_login_api_v1_auth_login_post
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/verify:verify.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Verify:Verify



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/verify
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/verify:
    post:
      tags:
        - auth
      summary: Verify:Verify
      operationId: verify_verify_api_v1_auth_verify_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Body_verify_verify_api_v1_auth_verify_post'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                VERIFY_USER_BAD_TOKEN:
                  summary: >-
                    Bad token, not existing user ornot the e-mail currently set
                    for the user.
                  value:
                    detail: VERIFY_USER_BAD_TOKEN
                VERIFY_USER_ALREADY_VERIFIED:
                  summary: The user is already verified.
                  value:
                    detail: VERIFY_USER_ALREADY_VERIFIED
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_verify_verify_api_v1_auth_verify_post:
      properties:
        token:
          type: string
          title: Token
      type: object
      required:
        - token
      title: Body_verify_verify_api_v1_auth_verify_post
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/reset:forgot-password.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Reset:Forgot Password



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/forgot-password
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/forgot-password:
    post:
      tags:
        - auth
      summary: Reset:Forgot Password
      operationId: reset_forgot_password_api_v1_auth_forgot_password_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_reset_forgot_password_api_v1_auth_forgot_password_post
        required: true
      responses:
        '202':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_reset_forgot_password_api_v1_auth_forgot_password_post:
      properties:
        email:
          type: string
          format: email
          title: Email
      type: object
      required:
        - email
      title: Body_reset_forgot_password_api_v1_auth_forgot_password_post
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/auth:cookielogout.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Auth:Cookie.Logout



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/logout
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/logout:
    post:
      tags:
        - auth
      summary: Auth:Cookie.Logout
      operationId: auth_cookie_logout_api_v1_auth_logout_post
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '204':
          description: No Content
        '401':
          description: Missing token or inactive user.
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/reset:reset-password.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Reset:Reset Password



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/auth/reset-password
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/auth/reset-password:
    post:
      tags:
        - auth
      summary: Reset:Reset Password
      operationId: reset_reset_password_api_v1_auth_reset_password_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_reset_reset_password_api_v1_auth_reset_password_post
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                RESET_PASSWORD_BAD_TOKEN:
                  summary: Bad or expired token.
                  value:
                    detail: RESET_PASSWORD_BAD_TOKEN
                RESET_PASSWORD_INVALID_PASSWORD:
                  summary: Password validation failed.
                  value:
                    detail:
                      code: RESET_PASSWORD_INVALID_PASSWORD
                      reason: Password should be at least 3 characters
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    Body_reset_reset_password_api_v1_auth_reset_password_post:
      properties:
        token:
          type: string
          title: Token
        password:
          type: string
          title: Password
      type: object
      required:
        - token
        - password
      title: Body_reset_reset_password_api_v1_auth_reset_password_post
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/auth/register:register.md

```

```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/health-check.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Health Check

> Health check endpoint for liveness/readiness probes.



## OpenAPI

````yaml cognee_openapi_spec.json get /health
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /health:
    get:
      summary: Health Check
      description: Health check endpoint for liveness/readiness probes.
      operationId: health_check_health_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/search/get-search-history.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Search History

> Get search history for the authenticated user.

This endpoint retrieves the search history for the authenticated user,
returning a list of previously executed searches with their timestamps.

## Response
Returns a list of search history items containing:
- **id**: Unique identifier for the search
- **text**: The search query text
- **user**: User who performed the search
- **created_at**: When the search was performed

## Error Codes
- **500 Internal Server Error**: Error retrieving search history



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/search
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/search:
    get:
      tags:
        - search
      summary: Get Search History
      description: |-
        Get search history for the authenticated user.

        This endpoint retrieves the search history for the authenticated user,
        returning a list of previously executed searches with their timestamps.

        ## Response
        Returns a list of search history items containing:
        - **id**: Unique identifier for the search
        - **text**: The search query text
        - **user**: User who performed the search
        - **created_at**: When the search was performed

        ## Error Codes
        - **500 Internal Server Error**: Error retrieving search history
      operationId: get_search_history_api_v1_search_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/SearchHistoryItem'
                type: array
                title: Response Get Search History Api V1 Search Get
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    SearchHistoryItem:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        text:
          type: string
          title: Text
        user:
          type: string
          title: User
        createdAt:
          type: string
          format: date-time
          title: Createdat
      type: object
      required:
        - id
        - text
        - user
        - createdAt
      title: SearchHistoryItem
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/search/search.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Search

> Search for nodes in the graph database.

This endpoint performs semantic search across the knowledge graph to find
relevant nodes based on the provided query. It supports different search
types and can be scoped to specific datasets.

## Request Parameters
- **search_type** (SearchType): Type of search to perform
- **datasets** (Optional[List[str]]): List of dataset names to search within
- **dataset_ids** (Optional[List[UUID]]): List of dataset UUIDs to search within
- **query** (str): The search query string
- **top_k** (Optional[int]): Maximum number of results to return (default: 10)

## Response
Returns a list of search results containing relevant nodes from the graph.

## Error Codes
- **409 Conflict**: Error during search operation
- **403 Forbidden**: User doesn't have permission to search datasets (returns empty list)

## Notes
- Datasets sent by name will only map to datasets owned by the request sender
- To search datasets not owned by the request sender, dataset UUID is needed
- If permission is denied, returns empty list instead of error



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/search
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/search:
    post:
      tags:
        - search
      summary: Search
      description: >-
        Search for nodes in the graph database.


        This endpoint performs semantic search across the knowledge graph to
        find

        relevant nodes based on the provided query. It supports different search

        types and can be scoped to specific datasets.


        ## Request Parameters

        - **search_type** (SearchType): Type of search to perform

        - **datasets** (Optional[List[str]]): List of dataset names to search
        within

        - **dataset_ids** (Optional[List[UUID]]): List of dataset UUIDs to
        search within

        - **query** (str): The search query string

        - **top_k** (Optional[int]): Maximum number of results to return
        (default: 10)


        ## Response

        Returns a list of search results containing relevant nodes from the
        graph.


        ## Error Codes

        - **409 Conflict**: Error during search operation

        - **403 Forbidden**: User doesn't have permission to search datasets
        (returns empty list)


        ## Notes

        - Datasets sent by name will only map to datasets owned by the request
        sender

        - To search datasets not owned by the request sender, dataset UUID is
        needed

        - If permission is denied, returns empty list instead of error
      operationId: search_api_v1_search_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SearchPayloadDTO'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items: {}
                type: array
                title: Response Search Api V1 Search Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    SearchPayloadDTO:
      properties:
        searchType:
          $ref: '#/components/schemas/SearchType'
          default: GRAPH_COMPLETION
        datasets:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Datasets
        datasetIds:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Datasetids
          examples:
            - []
        query:
          type: string
          title: Query
          default: What is in the document?
        topK:
          anyOf:
            - type: integer
            - type: 'null'
          title: Topk
          default: 10
      type: object
      title: SearchPayloadDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    SearchType:
      type: string
      enum:
        - SUMMARIES
        - INSIGHTS
        - CHUNKS
        - RAG_COMPLETION
        - GRAPH_COMPLETION
        - GRAPH_SUMMARY_COMPLETION
        - CODE
        - CYPHER
        - NATURAL_LANGUAGE
        - GRAPH_COMPLETION_COT
        - GRAPH_COMPLETION_CONTEXT_EXTENSION
        - FEELING_LUCKY
      title: SearchType
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/detailed-health-check.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Detailed Health Check

> Comprehensive health status with component details.



## OpenAPI

````yaml cognee_openapi_spec.json get /health/detailed
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /health/detailed:
    get:
      summary: Detailed Health Check
      description: Comprehensive health status with component details.
      operationId: detailed_health_check_health_detailed_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/code-pipeline/code-pipeline-retrieve.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Pipeline Retrieve

> Retrieve context from the code knowledge graph.

This endpoint searches the indexed code repository to find relevant
context based on the provided query.

## Request Parameters
- **query** (str): Search query for code context
- **full_input** (str): Full input text for processing

## Response
Returns a list of relevant code files and context as JSON.

## Error Codes
- **409 Conflict**: Error during retrieval process



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/code-pipeline/retrieve
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/code-pipeline/retrieve:
    post:
      tags:
        - code-pipeline
      summary: Code Pipeline Retrieve
      description: |-
        Retrieve context from the code knowledge graph.

        This endpoint searches the indexed code repository to find relevant
        context based on the provided query.

        ## Request Parameters
        - **query** (str): Search query for code context
        - **full_input** (str): Full input text for processing

        ## Response
        Returns a list of relevant code files and context as JSON.

        ## Error Codes
        - **409 Conflict**: Error during retrieval process
      operationId: code_pipeline_retrieve_api_v1_code_pipeline_retrieve_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CodePipelineRetrievePayloadDTO'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  additionalProperties: true
                  type: object
                type: array
                title: >-
                  Response Code Pipeline Retrieve Api V1 Code Pipeline Retrieve
                  Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    CodePipelineRetrievePayloadDTO:
      properties:
        query:
          type: string
          title: Query
        fullInput:
          type: string
          title: Fullinput
      type: object
      required:
        - query
        - fullInput
      title: CodePipelineRetrievePayloadDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/code-pipeline/code-pipeline-index.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Pipeline Index

> Run indexation on a code repository.

This endpoint processes a code repository to create a knowledge graph
of the codebase structure, dependencies, and relationships.

## Request Parameters
- **repo_path** (str): Path to the code repository
- **include_docs** (bool): Whether to include documentation files (default: false)

## Response
No content returned. Processing results are logged.

## Error Codes
- **409 Conflict**: Error during indexation process



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/code-pipeline/index
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/code-pipeline/index:
    post:
      tags:
        - code-pipeline
      summary: Code Pipeline Index
      description: >-
        Run indexation on a code repository.


        This endpoint processes a code repository to create a knowledge graph

        of the codebase structure, dependencies, and relationships.


        ## Request Parameters

        - **repo_path** (str): Path to the code repository

        - **include_docs** (bool): Whether to include documentation files
        (default: false)


        ## Response

        No content returned. Processing results are logged.


        ## Error Codes

        - **409 Conflict**: Error during indexation process
      operationId: code_pipeline_index_api_v1_code_pipeline_index_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CodePipelineIndexPayloadDTO'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    CodePipelineIndexPayloadDTO:
      properties:
        repoPath:
          type: string
          title: Repopath
        includeDocs:
          type: boolean
          title: Includedocs
          default: false
      type: object
      required:
        - repoPath
      title: CodePipelineIndexPayloadDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/create-new-dataset.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create New Dataset

> Create a new dataset or return existing dataset with the same name.

This endpoint creates a new dataset with the specified name. If a dataset
with the same name already exists for the user, it returns the existing
dataset instead of creating a duplicate. The user is automatically granted
all permissions (read, write, share, delete) on the created dataset.

## Request Parameters
- **dataset_data** (DatasetCreationPayload): Dataset creation parameters containing:
  - **name**: The name for the new dataset

## Response
Returns the created or existing dataset object containing:
- **id**: Unique dataset identifier
- **name**: Dataset name
- **created_at**: When the dataset was created
- **updated_at**: When the dataset was last updated
- **owner_id**: ID of the dataset owner

## Error Codes
- **418 I'm a teapot**: Error creating dataset



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/datasets
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets:
    post:
      tags:
        - datasets
      summary: Create New Dataset
      description: >-
        Create a new dataset or return existing dataset with the same name.


        This endpoint creates a new dataset with the specified name. If a
        dataset

        with the same name already exists for the user, it returns the existing

        dataset instead of creating a duplicate. The user is automatically
        granted

        all permissions (read, write, share, delete) on the created dataset.


        ## Request Parameters

        - **dataset_data** (DatasetCreationPayload): Dataset creation parameters
        containing:
          - **name**: The name for the new dataset

        ## Response

        Returns the created or existing dataset object containing:

        - **id**: Unique dataset identifier

        - **name**: Dataset name

        - **created_at**: When the dataset was created

        - **updated_at**: When the dataset was last updated

        - **owner_id**: ID of the dataset owner


        ## Error Codes

        - **418 I'm a teapot**: Error creating dataset
      operationId: create_new_dataset_api_v1_datasets_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DatasetCreationPayload'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DatasetDTO'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    DatasetCreationPayload:
      properties:
        name:
          type: string
          title: Name
      type: object
      required:
        - name
      title: DatasetCreationPayload
    DatasetDTO:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        name:
          type: string
          title: Name
        createdAt:
          type: string
          format: date-time
          title: Createdat
        updatedAt:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Updatedat
        ownerId:
          type: string
          format: uuid
          title: Ownerid
      type: object
      required:
        - id
        - name
        - createdAt
        - ownerId
      title: DatasetDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/get-dataset-data.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Dataset Data

> Get all data items in a dataset.

This endpoint retrieves all data items (documents, files, etc.) that belong
to a specific dataset. Each data item includes metadata such as name, type,
creation time, and storage location.

## Path Parameters
- **dataset_id** (UUID): The unique identifier of the dataset

## Response
Returns a list of data objects containing:
- **id**: Unique data item identifier
- **name**: Data item name
- **created_at**: When the data was added
- **updated_at**: When the data was last updated
- **extension**: File extension
- **mime_type**: MIME type of the data
- **raw_data_location**: Storage location of the raw data

## Error Codes
- **404 Not Found**: Dataset doesn't exist or user doesn't have access
- **500 Internal Server Error**: Error retrieving data



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/datasets/{dataset_id}/data
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets/{dataset_id}/data:
    get:
      tags:
        - datasets
      summary: Get Dataset Data
      description: >-
        Get all data items in a dataset.


        This endpoint retrieves all data items (documents, files, etc.) that
        belong

        to a specific dataset. Each data item includes metadata such as name,
        type,

        creation time, and storage location.


        ## Path Parameters

        - **dataset_id** (UUID): The unique identifier of the dataset


        ## Response

        Returns a list of data objects containing:

        - **id**: Unique data item identifier

        - **name**: Data item name

        - **created_at**: When the data was added

        - **updated_at**: When the data was last updated

        - **extension**: File extension

        - **mime_type**: MIME type of the data

        - **raw_data_location**: Storage location of the raw data


        ## Error Codes

        - **404 Not Found**: Dataset doesn't exist or user doesn't have access

        - **500 Internal Server Error**: Error retrieving data
      operationId: get_dataset_data_api_v1_datasets__dataset_id__data_get
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/DataDTO'
                title: >-
                  Response Get Dataset Data Api V1 Datasets  Dataset Id  Data
                  Get
        '404':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponseDTO'
          description: Not Found
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    DataDTO:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        name:
          type: string
          title: Name
        createdAt:
          type: string
          format: date-time
          title: Createdat
        updatedAt:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Updatedat
        extension:
          type: string
          title: Extension
        mimeType:
          type: string
          title: Mimetype
        rawDataLocation:
          type: string
          title: Rawdatalocation
      type: object
      required:
        - id
        - name
        - createdAt
        - extension
        - mimeType
        - rawDataLocation
      title: DataDTO
    ErrorResponseDTO:
      properties:
        message:
          type: string
          title: Message
      type: object
      required:
        - message
      title: ErrorResponseDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/get-raw-data.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Raw Data

> Download the raw data file for a specific data item.

This endpoint allows users to download the original, unprocessed data file
for a specific data item within a dataset. The file is returned as a direct
download with appropriate headers.

## Path Parameters
- **dataset_id** (UUID): The unique identifier of the dataset containing the data
- **data_id** (UUID): The unique identifier of the data item to download

## Response
Returns the raw data file as a downloadable response.

## Error Codes
- **404 Not Found**: Dataset or data item doesn't exist, or user doesn't have access
- **500 Internal Server Error**: Error accessing the raw data file



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/datasets/{dataset_id}/data/{data_id}/raw
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets/{dataset_id}/data/{data_id}/raw:
    get:
      tags:
        - datasets
      summary: Get Raw Data
      description: >-
        Download the raw data file for a specific data item.


        This endpoint allows users to download the original, unprocessed data
        file

        for a specific data item within a dataset. The file is returned as a
        direct

        download with appropriate headers.


        ## Path Parameters

        - **dataset_id** (UUID): The unique identifier of the dataset containing
        the data

        - **data_id** (UUID): The unique identifier of the data item to download


        ## Response

        Returns the raw data file as a downloadable response.


        ## Error Codes

        - **404 Not Found**: Dataset or data item doesn't exist, or user doesn't
        have access

        - **500 Internal Server Error**: Error accessing the raw data file
      operationId: get_raw_data_api_v1_datasets__dataset_id__data__data_id__raw_get
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
        - name: data_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Data Id
      responses:
        '200':
          description: Successful Response
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/delete-dataset.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete Dataset

> Delete a dataset by its ID.

This endpoint permanently deletes a dataset and all its associated data.
The user must have delete permissions on the dataset to perform this operation.

## Path Parameters
- **dataset_id** (UUID): The unique identifier of the dataset to delete

## Response
No content returned on successful deletion.

## Error Codes
- **404 Not Found**: Dataset doesn't exist or user doesn't have access
- **500 Internal Server Error**: Error during deletion



## OpenAPI

````yaml cognee_openapi_spec.json delete /api/v1/datasets/{dataset_id}
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets/{dataset_id}:
    delete:
      tags:
        - datasets
      summary: Delete Dataset
      description: >-
        Delete a dataset by its ID.


        This endpoint permanently deletes a dataset and all its associated data.

        The user must have delete permissions on the dataset to perform this
        operation.


        ## Path Parameters

        - **dataset_id** (UUID): The unique identifier of the dataset to delete


        ## Response

        No content returned on successful deletion.


        ## Error Codes

        - **404 Not Found**: Dataset doesn't exist or user doesn't have access

        - **500 Internal Server Error**: Error during deletion
      operationId: delete_dataset_api_v1_datasets__dataset_id__delete
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '404':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponseDTO'
          description: Not Found
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    ErrorResponseDTO:
      properties:
        message:
          type: string
          title: Message
      type: object
      required:
        - message
      title: ErrorResponseDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/get-datasets.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Datasets

> Get all datasets accessible to the authenticated user.

This endpoint retrieves all datasets that the authenticated user has
read permissions for. The datasets are returned with their metadata
including ID, name, creation time, and owner information.

## Response
Returns a list of dataset objects containing:
- **id**: Unique dataset identifier
- **name**: Dataset name
- **created_at**: When the dataset was created
- **updated_at**: When the dataset was last updated
- **owner_id**: ID of the dataset owner

## Error Codes
- **418 I'm a teapot**: Error retrieving datasets



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/datasets
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets:
    get:
      tags:
        - datasets
      summary: Get Datasets
      description: |-
        Get all datasets accessible to the authenticated user.

        This endpoint retrieves all datasets that the authenticated user has
        read permissions for. The datasets are returned with their metadata
        including ID, name, creation time, and owner information.

        ## Response
        Returns a list of dataset objects containing:
        - **id**: Unique dataset identifier
        - **name**: Dataset name
        - **created_at**: When the dataset was created
        - **updated_at**: When the dataset was last updated
        - **owner_id**: ID of the dataset owner

        ## Error Codes
        - **418 I'm a teapot**: Error retrieving datasets
      operationId: get_datasets_api_v1_datasets_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/DatasetDTO'
                type: array
                title: Response Get Datasets Api V1 Datasets Get
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    DatasetDTO:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        name:
          type: string
          title: Name
        createdAt:
          type: string
          format: date-time
          title: Createdat
        updatedAt:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Updatedat
        ownerId:
          type: string
          format: uuid
          title: Ownerid
      type: object
      required:
        - id
        - name
        - createdAt
        - ownerId
      title: DatasetDTO
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/get-dataset-status.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Dataset Status

> Get the processing status of datasets.

This endpoint retrieves the current processing status of one or more datasets,
indicating whether they are being processed, have completed processing, or
encountered errors during pipeline execution.

## Query Parameters
- **dataset** (List[UUID]): List of dataset UUIDs to check status for

## Response
Returns a dictionary mapping dataset IDs to their processing status:
- **pending**: Dataset is queued for processing
- **running**: Dataset is currently being processed
- **completed**: Dataset processing completed successfully
- **failed**: Dataset processing encountered an error

## Error Codes
- **500 Internal Server Error**: Error retrieving status information



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/datasets/status
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets/status:
    get:
      tags:
        - datasets
      summary: Get Dataset Status
      description: >-
        Get the processing status of datasets.


        This endpoint retrieves the current processing status of one or more
        datasets,

        indicating whether they are being processed, have completed processing,
        or

        encountered errors during pipeline execution.


        ## Query Parameters

        - **dataset** (List[UUID]): List of dataset UUIDs to check status for


        ## Response

        Returns a dictionary mapping dataset IDs to their processing status:

        - **pending**: Dataset is queued for processing

        - **running**: Dataset is currently being processed

        - **completed**: Dataset processing completed successfully

        - **failed**: Dataset processing encountered an error


        ## Error Codes

        - **500 Internal Server Error**: Error retrieving status information
      operationId: get_dataset_status_api_v1_datasets_status_get
      parameters:
        - name: dataset
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
              format: uuid
            default: []
            title: Dataset
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  $ref: '#/components/schemas/PipelineRunStatus'
                title: Response Get Dataset Status Api V1 Datasets Status Get
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    PipelineRunStatus:
      type: string
      enum:
        - DATASET_PROCESSING_INITIATED
        - DATASET_PROCESSING_STARTED
        - DATASET_PROCESSING_COMPLETED
        - DATASET_PROCESSING_ERRORED
      title: PipelineRunStatus
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/get-dataset-graph.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Dataset Graph

> Get the knowledge graph visualization for a dataset.

This endpoint retrieves the knowledge graph data for a specific dataset,
including nodes and edges that represent the relationships between entities
in the dataset. The graph data is formatted for visualization purposes.

## Path Parameters
- **dataset_id** (UUID): The unique identifier of the dataset

## Response
Returns the graph data containing:
- **nodes**: List of graph nodes with id, label, and properties
- **edges**: List of graph edges with source, target, and label

## Error Codes
- **404 Not Found**: Dataset doesn't exist or user doesn't have access
- **500 Internal Server Error**: Error retrieving graph data



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/datasets/{dataset_id}/graph
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets/{dataset_id}/graph:
    get:
      tags:
        - datasets
      summary: Get Dataset Graph
      description: >-
        Get the knowledge graph visualization for a dataset.


        This endpoint retrieves the knowledge graph data for a specific dataset,

        including nodes and edges that represent the relationships between
        entities

        in the dataset. The graph data is formatted for visualization purposes.


        ## Path Parameters

        - **dataset_id** (UUID): The unique identifier of the dataset


        ## Response

        Returns the graph data containing:

        - **nodes**: List of graph nodes with id, label, and properties

        - **edges**: List of graph edges with source, target, and label


        ## Error Codes

        - **404 Not Found**: Dataset doesn't exist or user doesn't have access

        - **500 Internal Server Error**: Error retrieving graph data
      operationId: get_dataset_graph_api_v1_datasets__dataset_id__graph_get
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GraphDTO'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    GraphDTO:
      properties:
        nodes:
          items:
            $ref: '#/components/schemas/GraphNodeDTO'
          type: array
          title: Nodes
        edges:
          items:
            $ref: '#/components/schemas/GraphEdgeDTO'
          type: array
          title: Edges
      type: object
      required:
        - nodes
        - edges
      title: GraphDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    GraphNodeDTO:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        label:
          type: string
          title: Label
        properties:
          additionalProperties: true
          type: object
          title: Properties
      type: object
      required:
        - id
        - label
        - properties
      title: GraphNodeDTO
    GraphEdgeDTO:
      properties:
        source:
          type: string
          format: uuid
          title: Source
        target:
          type: string
          format: uuid
          title: Target
        label:
          type: string
          title: Label
      type: object
      required:
        - source
        - target
        - label
      title: GraphEdgeDTO
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/datasets/delete-data.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete Data

> Delete a specific data item from a dataset.

This endpoint removes a specific data item from a dataset while keeping
the dataset itself intact. The user must have delete permissions on the
dataset to perform this operation.

## Path Parameters
- **dataset_id** (UUID): The unique identifier of the dataset containing the data
- **data_id** (UUID): The unique identifier of the data item to delete

## Response
No content returned on successful deletion.

## Error Codes
- **404 Not Found**: Dataset or data item doesn't exist, or user doesn't have access
- **500 Internal Server Error**: Error during deletion



## OpenAPI

````yaml cognee_openapi_spec.json delete /api/v1/datasets/{dataset_id}/data/{data_id}
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/datasets/{dataset_id}/data/{data_id}:
    delete:
      tags:
        - datasets
      summary: Delete Data
      description: >-
        Delete a specific data item from a dataset.


        This endpoint removes a specific data item from a dataset while keeping

        the dataset itself intact. The user must have delete permissions on the

        dataset to perform this operation.


        ## Path Parameters

        - **dataset_id** (UUID): The unique identifier of the dataset containing
        the data

        - **data_id** (UUID): The unique identifier of the data item to delete


        ## Response

        No content returned on successful deletion.


        ## Error Codes

        - **404 Not Found**: Dataset or data item doesn't exist, or user doesn't
        have access

        - **500 Internal Server Error**: Error during deletion
      operationId: delete_data_api_v1_datasets__dataset_id__data__data_id__delete
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
        - name: data_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Data Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '404':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponseDTO'
          description: Not Found
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    ErrorResponseDTO:
      properties:
        message:
          type: string
          title: Message
      type: object
      required:
        - message
      title: ErrorResponseDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/cognify/cognify.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Cognify

> Transform datasets into structured knowledge graphs through cognitive processing.

This endpoint is the core of Cognee's intelligence layer, responsible for converting
raw text, documents, and data added through the add endpoint into semantic knowledge graphs.
It performs deep analysis to extract entities, relationships, and insights from ingested content.

## Processing Pipeline
1. Document classification and permission validation
2. Text chunking and semantic segmentation
3. Entity extraction using LLM-powered analysis
4. Relationship detection and graph construction
5. Vector embeddings generation for semantic search
6. Content summarization and indexing

## Request Parameters
- **datasets** (Optional[List[str]]): List of dataset names to process. Dataset names are resolved to datasets owned by the authenticated user.
- **dataset_ids** (Optional[List[UUID]]): List of existing dataset UUIDs to process. UUIDs allow processing of datasets not owned by the user (if permitted).
- **run_in_background** (Optional[bool]): Whether to execute processing asynchronously. Defaults to False (blocking).

## Response
- **Blocking execution**: Complete pipeline run information with entity counts, processing duration, and success/failure status
- **Background execution**: Pipeline run metadata including pipeline_run_id for status monitoring via WebSocket subscription

## Error Codes
- **400 Bad Request**: When neither datasets nor dataset_ids are provided, or when specified datasets don't exist
- **409 Conflict**: When processing fails due to system errors, missing LLM API keys, database connection failures, or corrupted content

## Example Request
```json
{
    "datasets": ["research_papers", "documentation"],
    "run_in_background": false
}
```

## Notes
To cognify data in datasets not owned by the user and for which the current user has write permission,
the dataset_id must be used (when ENABLE_BACKEND_ACCESS_CONTROL is set to True).

## Next Steps
After successful processing, use the search endpoints to query the generated knowledge graph for insights, relationships, and semantic search.



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/cognify
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/cognify:
    post:
      tags:
        - cognify
      summary: Cognify
      description: >-
        Transform datasets into structured knowledge graphs through cognitive
        processing.


        This endpoint is the core of Cognee's intelligence layer, responsible
        for converting

        raw text, documents, and data added through the add endpoint into
        semantic knowledge graphs.

        It performs deep analysis to extract entities, relationships, and
        insights from ingested content.


        ## Processing Pipeline

        1. Document classification and permission validation

        2. Text chunking and semantic segmentation

        3. Entity extraction using LLM-powered analysis

        4. Relationship detection and graph construction

        5. Vector embeddings generation for semantic search

        6. Content summarization and indexing


        ## Request Parameters

        - **datasets** (Optional[List[str]]): List of dataset names to process.
        Dataset names are resolved to datasets owned by the authenticated user.

        - **dataset_ids** (Optional[List[UUID]]): List of existing dataset UUIDs
        to process. UUIDs allow processing of datasets not owned by the user (if
        permitted).

        - **run_in_background** (Optional[bool]): Whether to execute processing
        asynchronously. Defaults to False (blocking).


        ## Response

        - **Blocking execution**: Complete pipeline run information with entity
        counts, processing duration, and success/failure status

        - **Background execution**: Pipeline run metadata including
        pipeline_run_id for status monitoring via WebSocket subscription


        ## Error Codes

        - **400 Bad Request**: When neither datasets nor dataset_ids are
        provided, or when specified datasets don't exist

        - **409 Conflict**: When processing fails due to system errors, missing
        LLM API keys, database connection failures, or corrupted content


        ## Example Request

        ```json

        {
            "datasets": ["research_papers", "documentation"],
            "run_in_background": false
        }

        ```


        ## Notes

        To cognify data in datasets not owned by the user and for which the
        current user has write permission,

        the dataset_id must be used (when ENABLE_BACKEND_ACCESS_CONTROL is set
        to True).


        ## Next Steps

        After successful processing, use the search endpoints to query the
        generated knowledge graph for insights, relationships, and semantic
        search.
      operationId: cognify_api_v1_cognify_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CognifyPayloadDTO'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                additionalProperties: true
                type: object
                title: Response Cognify Api V1 Cognify Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    CognifyPayloadDTO:
      properties:
        datasets:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Datasets
        datasetIds:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Datasetids
          examples:
            - []
        runInBackground:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Runinbackground
          default: false
      type: object
      title: CognifyPayloadDTO
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/responses/create-response.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Response

> OpenAI-compatible responses endpoint with function calling support.

This endpoint provides OpenAI-compatible API responses with integrated
function calling capabilities for Cognee operations.

## Request Parameters
- **input** (str): The input text to process
- **model** (str): The model to use for processing
- **tools** (Optional[List[Dict]]): Available tools for function calling
- **tool_choice** (Any): Tool selection strategy (default: "auto")
- **temperature** (float): Response randomness (default: 1.0)

## Response
Returns an OpenAI-compatible response body with function call results.

## Error Codes
- **400 Bad Request**: Invalid request parameters
- **500 Internal Server Error**: Error processing request

## Notes
- Compatible with OpenAI API format
- Supports function calling with Cognee tools
- Uses default tools if none provided



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/responses/
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/responses/:
    post:
      tags:
        - responses
      summary: Create Response
      description: |-
        OpenAI-compatible responses endpoint with function calling support.

        This endpoint provides OpenAI-compatible API responses with integrated
        function calling capabilities for Cognee operations.

        ## Request Parameters
        - **input** (str): The input text to process
        - **model** (str): The model to use for processing
        - **tools** (Optional[List[Dict]]): Available tools for function calling
        - **tool_choice** (Any): Tool selection strategy (default: "auto")
        - **temperature** (float): Response randomness (default: 1.0)

        ## Response
        Returns an OpenAI-compatible response body with function call results.

        ## Error Codes
        - **400 Bad Request**: Invalid request parameters
        - **500 Internal Server Error**: Error processing request

        ## Notes
        - Compatible with OpenAI API format
        - Supports function calling with Cognee tools
        - Uses default tools if none provided
      operationId: create_response_api_v1_responses__post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResponseRequest'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseBody'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    ResponseRequest:
      properties:
        model:
          $ref: '#/components/schemas/CogneeModel'
          default: cognee-v1
        input:
          type: string
          title: Input
        tools:
          anyOf:
            - items:
                $ref: '#/components/schemas/ToolFunction'
              type: array
            - type: 'null'
          title: Tools
        toolChoice:
          anyOf:
            - type: string
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Toolchoice
          default: auto
        user:
          anyOf:
            - type: string
            - type: 'null'
          title: User
        temperature:
          anyOf:
            - type: number
            - type: 'null'
          title: Temperature
          default: 1
        maxTokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Maxtokens
      type: object
      required:
        - input
      title: ResponseRequest
      description: >-
        Request body for the new responses endpoint (OpenAI Responses API
        format)
    ResponseBody:
      properties:
        id:
          type: string
          title: Id
        created:
          type: integer
          title: Created
        model:
          type: string
          title: Model
        object:
          type: string
          title: Object
          default: response
        status:
          type: string
          title: Status
          default: completed
        toolCalls:
          items:
            $ref: '#/components/schemas/ResponseToolCall'
          type: array
          title: Toolcalls
        usage:
          anyOf:
            - $ref: '#/components/schemas/ChatUsage'
            - type: 'null'
        metadata:
          additionalProperties: true
          type: object
          title: Metadata
      type: object
      required:
        - model
        - toolCalls
      title: ResponseBody
      description: Response body for the new responses endpoint
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    CogneeModel:
      type: string
      enum:
        - cognee-v1
      title: CogneeModel
      description: Enum for supported model types
    ToolFunction:
      properties:
        type:
          type: string
          title: Type
          default: function
        function:
          $ref: '#/components/schemas/Function'
      type: object
      required:
        - function
      title: ToolFunction
      description: Tool function wrapper (for OpenAI compatibility)
    ResponseToolCall:
      properties:
        id:
          type: string
          title: Id
        type:
          type: string
          title: Type
          default: function
        function:
          $ref: '#/components/schemas/FunctionCall'
        output:
          anyOf:
            - $ref: '#/components/schemas/ToolCallOutput'
            - type: 'null'
      type: object
      required:
        - function
      title: ResponseToolCall
      description: Tool call in a response
    ChatUsage:
      properties:
        prompt_tokens:
          type: integer
          title: Prompt Tokens
          default: 0
        completion_tokens:
          type: integer
          title: Completion Tokens
          default: 0
        total_tokens:
          type: integer
          title: Total Tokens
          default: 0
      type: object
      title: ChatUsage
      description: Token usage information
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
    Function:
      properties:
        name:
          type: string
          title: Name
        description:
          type: string
          title: Description
        parameters:
          $ref: '#/components/schemas/FunctionParameters'
      type: object
      required:
        - name
        - description
        - parameters
      title: Function
      description: Function definition compatible with OpenAI's format
    FunctionCall:
      properties:
        name:
          type: string
          title: Name
        arguments:
          type: string
          title: Arguments
      type: object
      required:
        - name
        - arguments
      title: FunctionCall
      description: Function call made by the assistant
    ToolCallOutput:
      properties:
        status:
          type: string
          title: Status
          default: success
        data:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Data
      type: object
      title: ToolCallOutput
      description: Output of a tool call in the responses API
    FunctionParameters:
      properties:
        type:
          type: string
          title: Type
          default: object
        properties:
          additionalProperties:
            additionalProperties: true
            type: object
          type: object
          title: Properties
        required:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Required
      type: object
      required:
        - properties
      title: FunctionParameters
      description: JSON Schema for function parameters
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/add/add.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Add

> Add data to a dataset for processing and knowledge graph construction.

This endpoint accepts various types of data (files, URLs, GitHub repositories)
and adds them to a specified dataset for processing. The data is ingested,
analyzed, and integrated into the knowledge graph.

## Request Parameters
- **data** (List[UploadFile]): List of files to upload. Can also include:
  - HTTP URLs (if ALLOW_HTTP_REQUESTS is enabled)
  - GitHub repository URLs (will be cloned and processed)
  - Regular file uploads
- **datasetName** (Optional[str]): Name of the dataset to add data to
- **datasetId** (Optional[UUID]): UUID of an already existing dataset

Either datasetName or datasetId must be provided.

## Response
Returns information about the add operation containing:
- Status of the operation
- Details about the processed data
- Any relevant metadata from the ingestion process

## Error Codes
- **400 Bad Request**: Neither datasetId nor datasetName provided
- **409 Conflict**: Error during add operation
- **403 Forbidden**: User doesn't have permission to add to dataset

## Notes
- To add data to datasets not owned by the user, use dataset_id (when ENABLE_BACKEND_ACCESS_CONTROL is set to True)
- GitHub repositories are cloned and all files are processed
- HTTP URLs are fetched and their content is processed
- The ALLOW_HTTP_REQUESTS environment variable controls URL processing
- datasetId value can only be the UUID of an already existing dataset



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/add
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/add:
    post:
      tags:
        - add
      summary: Add
      description: >-
        Add data to a dataset for processing and knowledge graph construction.


        This endpoint accepts various types of data (files, URLs, GitHub
        repositories)

        and adds them to a specified dataset for processing. The data is
        ingested,

        analyzed, and integrated into the knowledge graph.


        ## Request Parameters

        - **data** (List[UploadFile]): List of files to upload. Can also
        include:
          - HTTP URLs (if ALLOW_HTTP_REQUESTS is enabled)
          - GitHub repository URLs (will be cloned and processed)
          - Regular file uploads
        - **datasetName** (Optional[str]): Name of the dataset to add data to

        - **datasetId** (Optional[UUID]): UUID of an already existing dataset


        Either datasetName or datasetId must be provided.


        ## Response

        Returns information about the add operation containing:

        - Status of the operation

        - Details about the processed data

        - Any relevant metadata from the ingestion process


        ## Error Codes

        - **400 Bad Request**: Neither datasetId nor datasetName provided

        - **409 Conflict**: Error during add operation

        - **403 Forbidden**: User doesn't have permission to add to dataset


        ## Notes

        - To add data to datasets not owned by the user, use dataset_id (when
        ENABLE_BACKEND_ACCESS_CONTROL is set to True)

        - GitHub repositories are cloned and all files are processed

        - HTTP URLs are fetched and their content is processed

        - The ALLOW_HTTP_REQUESTS environment variable controls URL processing

        - datasetId value can only be the UUID of an already existing dataset
      operationId: add_api_v1_add_post
      requestBody:
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Body_add_api_v1_add_post'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                additionalProperties: true
                type: object
                title: Response Add Api V1 Add Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    Body_add_api_v1_add_post:
      properties:
        data:
          items:
            type: string
            format: binary
            maxLength: 10485760
          type: array
          title: Data
          maxItems: 10
          description: List of files to upload (max 10MB per file, max 10 files)
        datasetName:
          anyOf:
            - type: string
            - type: 'null'
          title: Datasetname
        datasetId:
          anyOf:
            - type: string
              format: uuid
            - type: string
              const: ''
            - type: 'null'
          title: Datasetid
          examples:
            - ''
      type: object
      title: Body_add_api_v1_add_post
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/visualize/visualize.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Visualize

> Generate an HTML visualization of the dataset's knowledge graph.

This endpoint creates an interactive HTML visualization of the knowledge graph
for a specific dataset. The visualization displays nodes and edges representing
entities and their relationships, allowing users to explore the graph structure
visually.

## Query Parameters
- **dataset_id** (UUID): The unique identifier of the dataset to visualize

## Response
Returns an HTML page containing the interactive graph visualization.

## Error Codes
- **404 Not Found**: Dataset doesn't exist
- **403 Forbidden**: User doesn't have permission to read the dataset
- **500 Internal Server Error**: Error generating visualization

## Notes
- User must have read permissions on the dataset
- Visualization is interactive and allows graph exploration



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/visualize
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/visualize:
    get:
      tags:
        - visualize
      summary: Visualize
      description: >-
        Generate an HTML visualization of the dataset's knowledge graph.


        This endpoint creates an interactive HTML visualization of the knowledge
        graph

        for a specific dataset. The visualization displays nodes and edges
        representing

        entities and their relationships, allowing users to explore the graph
        structure

        visually.


        ## Query Parameters

        - **dataset_id** (UUID): The unique identifier of the dataset to
        visualize


        ## Response

        Returns an HTML page containing the interactive graph visualization.


        ## Error Codes

        - **404 Not Found**: Dataset doesn't exist

        - **403 Forbidden**: User doesn't have permission to read the dataset

        - **500 Internal Server Error**: Error generating visualization


        ## Notes

        - User must have read permissions on the dataset

        - Visualization is interactive and allows graph exploration
      operationId: visualize_api_v1_visualize_get
      parameters:
        - name: dataset_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/root.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Root

> Root endpoint that returns a welcome message.



## OpenAPI

````yaml cognee_openapi_spec.json get /
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /:
    get:
      summary: Root
      description: Root endpoint that returns a welcome message.
      operationId: root__get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/delete/delete.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete

> Delete data by its ID from the specified dataset.

Args:
    data_id: The UUID of the data to delete
    dataset_id: The UUID of the dataset containing the data
    mode: "soft" (default) or "hard" - hard mode also deletes degree-one entity nodes
    user: Authenticated user

Returns:
    JSON response indicating success or failure



## OpenAPI

````yaml cognee_openapi_spec.json delete /api/v1/delete
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/delete:
    delete:
      tags:
        - delete
      summary: Delete
      description: |-
        Delete data by its ID from the specified dataset.

        Args:
            data_id: The UUID of the data to delete
            dataset_id: The UUID of the dataset containing the data
            mode: "soft" (default) or "hard" - hard mode also deletes degree-one entity nodes
            user: Authenticated user

        Returns:
            JSON response indicating success or failure
      operationId: delete_api_v1_delete_delete
      parameters:
        - name: data_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
            title: Data Id
        - name: dataset_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
        - name: mode
          in: query
          required: false
          schema:
            type: string
            default: soft
            title: Mode
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/users/users:current-user.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Users:Current User



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/users/me
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/users/me:
    get:
      tags:
        - users
      summary: Users:Current User
      operationId: users_current_user_api_v1_users_me_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '401':
          description: Missing token or inactive user.
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/users/users:patch-current-user.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Users:Patch Current User



## OpenAPI

````yaml cognee_openapi_spec.json patch /api/v1/users/me
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/users/me:
    patch:
      tags:
        - users
      summary: Users:Patch Current User
      operationId: users_patch_current_user_api_v1_users_me_patch
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '400':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                UPDATE_USER_EMAIL_ALREADY_EXISTS:
                  summary: A user with this email already exists.
                  value:
                    detail: UPDATE_USER_EMAIL_ALREADY_EXISTS
                UPDATE_USER_INVALID_PASSWORD:
                  summary: Password validation failed.
                  value:
                    detail:
                      code: UPDATE_USER_INVALID_PASSWORD
                      reason: Password should beat least 3 characters
          description: Bad Request
        '401':
          description: Missing token or inactive user.
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    UserUpdate:
      properties:
        password:
          anyOf:
            - type: string
            - type: 'null'
          title: Password
        email:
          anyOf:
            - type: string
              format: email
            - type: 'null'
          title: Email
        is_active:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Active
        is_superuser:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Superuser
        is_verified:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Verified
      type: object
      title: UserUpdate
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/users/users:delete-user.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Users:Delete User



## OpenAPI

````yaml cognee_openapi_spec.json delete /api/v1/users/{id}
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/users/{id}:
    delete:
      tags:
        - users
      summary: Users:Delete User
      operationId: users_delete_user_api_v1_users__id__delete
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            title: Id
      responses:
        '204':
          description: Successful Response
        '401':
          description: Missing token or inactive user.
        '403':
          description: Not a superuser.
        '404':
          description: The user does not exist.
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/users/users:patch-user.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Users:Patch User



## OpenAPI

````yaml cognee_openapi_spec.json patch /api/v1/users/{id}
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/users/{id}:
    patch:
      tags:
        - users
      summary: Users:Patch User
      operationId: users_patch_user_api_v1_users__id__patch
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            title: Id
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '400':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorModel'
              examples:
                UPDATE_USER_EMAIL_ALREADY_EXISTS:
                  summary: A user with this email already exists.
                  value:
                    detail: UPDATE_USER_EMAIL_ALREADY_EXISTS
                UPDATE_USER_INVALID_PASSWORD:
                  summary: Password validation failed.
                  value:
                    detail:
                      code: UPDATE_USER_INVALID_PASSWORD
                      reason: Password should beat least 3 characters
          description: Bad Request
        '401':
          description: Missing token or inactive user.
        '403':
          description: Not a superuser.
        '404':
          description: The user does not exist.
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    UserUpdate:
      properties:
        password:
          anyOf:
            - type: string
            - type: 'null'
          title: Password
        email:
          anyOf:
            - type: string
              format: email
            - type: 'null'
          title: Email
        is_active:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Active
        is_superuser:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Superuser
        is_verified:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Verified
      type: object
      title: UserUpdate
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
    ErrorModel:
      properties:
        detail:
          anyOf:
            - type: string
            - additionalProperties:
                type: string
              type: object
          title: Detail
      type: object
      required:
        - detail
      title: ErrorModel
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/users/users:user.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Users:User



## OpenAPI

````yaml cognee_openapi_spec.json get /api/v1/users/{id}
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/users/{id}:
    get:
      tags:
        - users
      summary: Users:User
      operationId: users_user_api_v1_users__id__get
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            title: Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRead'
        '401':
          description: Missing token or inactive user.
        '403':
          description: Not a superuser.
        '404':
          description: The user does not exist.
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    UserRead:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        email:
          type: string
          format: email
          title: Email
        is_active:
          type: boolean
          title: Is Active
          default: true
        is_superuser:
          type: boolean
          title: Is Superuser
          default: false
        is_verified:
          type: boolean
          title: Is Verified
          default: false
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
      type: object
      required:
        - id
        - email
      title: UserRead
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/permissions/create-tenant.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Tenant

> Create a new tenant.

This endpoint creates a new tenant with the specified name. Tenants are used
to organize users and resources in multi-tenant environments, providing
isolation and access control between different groups or organizations.

## Request Parameters
- **tenant_name** (str): The name of the tenant to create

## Response
Returns a success message indicating the tenant was created.

## Error Codes
- **400 Bad Request**: Invalid tenant name or tenant already exists
- **500 Internal Server Error**: Error creating the tenant



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/permissions/tenants
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/permissions/tenants:
    post:
      tags:
        - permissions
      summary: Create Tenant
      description: >-
        Create a new tenant.


        This endpoint creates a new tenant with the specified name. Tenants are
        used

        to organize users and resources in multi-tenant environments, providing

        isolation and access control between different groups or organizations.


        ## Request Parameters

        - **tenant_name** (str): The name of the tenant to create


        ## Response

        Returns a success message indicating the tenant was created.


        ## Error Codes

        - **400 Bad Request**: Invalid tenant name or tenant already exists

        - **500 Internal Server Error**: Error creating the tenant
      operationId: create_tenant_api_v1_permissions_tenants_post
      parameters:
        - name: tenant_name
          in: query
          required: true
          schema:
            type: string
            title: Tenant Name
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/permissions/add-user-to-role.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Add User To Role

> Add a user to a role.

This endpoint assigns a user to a specific role, granting them all the
permissions associated with that role. The authenticated user must be
the owner of the role or have appropriate administrative permissions.

## Path Parameters
- **user_id** (UUID): The UUID of the user to add to the role

## Request Parameters
- **role_id** (UUID): The UUID of the role to assign the user to

## Response
Returns a success message indicating the user was added to the role.

## Error Codes
- **400 Bad Request**: Invalid user or role ID
- **403 Forbidden**: User doesn't have permission to assign roles
- **404 Not Found**: User or role doesn't exist
- **500 Internal Server Error**: Error adding user to role



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/permissions/users/{user_id}/roles
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/permissions/users/{user_id}/roles:
    post:
      tags:
        - permissions
      summary: Add User To Role
      description: |-
        Add a user to a role.

        This endpoint assigns a user to a specific role, granting them all the
        permissions associated with that role. The authenticated user must be
        the owner of the role or have appropriate administrative permissions.

        ## Path Parameters
        - **user_id** (UUID): The UUID of the user to add to the role

        ## Request Parameters
        - **role_id** (UUID): The UUID of the role to assign the user to

        ## Response
        Returns a success message indicating the user was added to the role.

        ## Error Codes
        - **400 Bad Request**: Invalid user or role ID
        - **403 Forbidden**: User doesn't have permission to assign roles
        - **404 Not Found**: User or role doesn't exist
        - **500 Internal Server Error**: Error adding user to role
      operationId: add_user_to_role_api_v1_permissions_users__user_id__roles_post
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: User Id
        - name: role_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
            title: Role Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/permissions/create-role.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Role

> Create a new role.

This endpoint creates a new role with the specified name. Roles are used
to group permissions and can be assigned to users to manage access control
more efficiently. The authenticated user becomes the owner of the created role.

## Request Parameters
- **role_name** (str): The name of the role to create

## Response
Returns a success message indicating the role was created.

## Error Codes
- **400 Bad Request**: Invalid role name or role already exists
- **500 Internal Server Error**: Error creating the role



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/permissions/roles
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/permissions/roles:
    post:
      tags:
        - permissions
      summary: Create Role
      description: >-
        Create a new role.


        This endpoint creates a new role with the specified name. Roles are used

        to group permissions and can be assigned to users to manage access
        control

        more efficiently. The authenticated user becomes the owner of the
        created role.


        ## Request Parameters

        - **role_name** (str): The name of the role to create


        ## Response

        Returns a success message indicating the role was created.


        ## Error Codes

        - **400 Bad Request**: Invalid role name or role already exists

        - **500 Internal Server Error**: Error creating the role
      operationId: create_role_api_v1_permissions_roles_post
      parameters:
        - name: role_name
          in: query
          required: true
          schema:
            type: string
            title: Role Name
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/permissions/add-user-to-tenant.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Add User To Tenant

> Add a user to a tenant.

This endpoint assigns a user to a specific tenant, allowing them to access
resources and data associated with that tenant. The authenticated user must
be the owner of the tenant or have appropriate administrative permissions.

## Path Parameters
- **user_id** (UUID): The UUID of the user to add to the tenant

## Request Parameters
- **tenant_id** (UUID): The UUID of the tenant to assign the user to

## Response
Returns a success message indicating the user was added to the tenant.

## Error Codes
- **400 Bad Request**: Invalid user or tenant ID
- **403 Forbidden**: User doesn't have permission to assign tenants
- **404 Not Found**: User or tenant doesn't exist
- **500 Internal Server Error**: Error adding user to tenant



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/permissions/users/{user_id}/tenants
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/permissions/users/{user_id}/tenants:
    post:
      tags:
        - permissions
      summary: Add User To Tenant
      description: >-
        Add a user to a tenant.


        This endpoint assigns a user to a specific tenant, allowing them to
        access

        resources and data associated with that tenant. The authenticated user
        must

        be the owner of the tenant or have appropriate administrative
        permissions.


        ## Path Parameters

        - **user_id** (UUID): The UUID of the user to add to the tenant


        ## Request Parameters

        - **tenant_id** (UUID): The UUID of the tenant to assign the user to


        ## Response

        Returns a success message indicating the user was added to the tenant.


        ## Error Codes

        - **400 Bad Request**: Invalid user or tenant ID

        - **403 Forbidden**: User doesn't have permission to assign tenants

        - **404 Not Found**: User or tenant doesn't exist

        - **500 Internal Server Error**: Error adding user to tenant
      operationId: add_user_to_tenant_api_v1_permissions_users__user_id__tenants_post
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: User Id
        - name: tenant_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
            title: Tenant Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

## /home/daniel/tron/programas/ProyectoPizza/BD/cognee/Documentacion/definitiva/api-reference/permissions/give-datasets-permission-to-principal.md

```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Give Datasets Permission To Principal

> Grant permission on datasets to a principal (user or role).

This endpoint allows granting specific permissions on one or more datasets
to a principal (which can be a user or role). The authenticated user must
have appropriate permissions to grant access to the specified datasets.

## Path Parameters
- **principal_id** (UUID): The UUID of the principal (user or role) to grant permission to

## Request Parameters
- **permission_name** (str): The name of the permission to grant (e.g., "read", "write", "delete")
- **dataset_ids** (List[UUID]): List of dataset UUIDs to grant permission on

## Response
Returns a success message indicating permission was assigned.

## Error Codes
- **400 Bad Request**: Invalid request parameters
- **403 Forbidden**: User doesn't have permission to grant access
- **500 Internal Server Error**: Error granting permission



## OpenAPI

````yaml cognee_openapi_spec.json post /api/v1/permissions/datasets/{principal_id}
openapi: 3.1.0
info:
  title: Cognee API
  description: Cognee API with Bearer token and Cookie auth
  version: 1.0.0
servers:
  - url: https://api.cognee.ai
    description: Production server (full functionality)
  - url: http://localhost:8000
    description: Local development server (requires local setup)
security:
  - BearerAuth: []
  - CookieAuth: []
paths:
  /api/v1/permissions/datasets/{principal_id}:
    post:
      tags:
        - permissions
      summary: Give Datasets Permission To Principal
      description: >-
        Grant permission on datasets to a principal (user or role).


        This endpoint allows granting specific permissions on one or more
        datasets

        to a principal (which can be a user or role). The authenticated user
        must

        have appropriate permissions to grant access to the specified datasets.


        ## Path Parameters

        - **principal_id** (UUID): The UUID of the principal (user or role) to
        grant permission to


        ## Request Parameters

        - **permission_name** (str): The name of the permission to grant (e.g.,
        "read", "write", "delete")

        - **dataset_ids** (List[UUID]): List of dataset UUIDs to grant
        permission on


        ## Response

        Returns a success message indicating permission was assigned.


        ## Error Codes

        - **400 Bad Request**: Invalid request parameters

        - **403 Forbidden**: User doesn't have permission to grant access

        - **500 Internal Server Error**: Error granting permission
      operationId: >-
        give_datasets_permission_to_principal_api_v1_permissions_datasets__principal_id__post
      parameters:
        - name: principal_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Principal Id
        - name: permission_name
          in: query
          required: true
          schema:
            type: string
            title: Permission Name
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                type: string
                format: uuid
              title: Dataset Ids
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - OAuth2PasswordBearer: []
        - APIKeyCookie: []
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    CookieAuth:
      type: apiKey
      in: cookie
      name: auth_token

````
```

