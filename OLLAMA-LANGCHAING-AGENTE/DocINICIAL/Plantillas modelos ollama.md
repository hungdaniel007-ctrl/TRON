[qwen2.5](https://ollama.com/library/qwen2.5 "qwen2.5"):7b

20.7M DownloadsUpdated 1 year ago

## Qwen2.5 models are pretrained on Alibaba's latest large-scale dataset, encompassing up to 18 trillion tokens. The model supports up to 128K tokens and has multilingual support.

tools0.5b1.5b3b7b14b32b72b

[qwen2.5:7b](https://ollama.com/library/qwen2.5:7b)/

template

eb4402837c78 · 1.5kB

{{- if .Messages }}

{{- if or .System .Tools }}<|im_start|>system

{{- if .System }}

{{ .System }}

{{- end }}

{{- if .Tools }}

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:

<tools>

{{- range .Tools }}

{"type": "function", "function": {{ .Function }}}

{{- end }}

</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:

<tool_call>

{"name": <function-name>, "arguments": <args-json-object>}

</tool_call>

{{- end }}<|im_end|>

{{ end }}

{{- range $i, $_ := .Messages }}

{{- $last := eq (len (slice $.Messages $i)) 1 -}}

{{- if eq .Role "user" }}<|im_start|>user

{{ .Content }}<|im_end|>

{{ else if eq .Role "assistant" }}<|im_start|>assistant

{{ if .Content }}{{ .Content }}

{{- else if .ToolCalls }}<tool_call>

{{ range .ToolCalls }}{"name": "{{ .Function.Name }}", "arguments": {{ .Function.Arguments }}}

{{ end }}</tool_call>

{{- end }}{{ if not $last }}<|im_end|>

{{ end }}

{{- else if eq .Role "tool" }}<|im_start|>user

<tool_response>

{{ .Content }}

</tool_response><|im_end|>

{{ end }}

{{- if and (ne .Role "assistant") $last }}<|im_start|>assistant

{{ end }}

{{- end }}

{{- else }}

{{- if .System }}<|im_start|>system

{{ .System }}<|im_end|>

{{ end }}{{ if .Prompt }}<|im_start|>user

{{ .Prompt }}<|im_end|>

{{ end }}<|im_start|>assistant

{{ end }}{{ .Response }}{{ if .Response }}<|im_end|>{{ end }}


phi4-mini:latest
849.9K
 Downloads
Updated 
11 months ago

Phi-4-mini brings significant enhancements in multilingual support, reasoning, and mathematics, and now, the long-awaited function calling feature is finally supported.
tools
3.8b
phi4-mini:latest
/
template
813f53fdc6e5 · 655B
{{- if or .System .Tools }}<|system|>{{ if .System }}{{ .System }}{{ end }}
{{- if .Tools }}{{ if not .System }}You are a helpful assistant with some tools.{{ end }}<|tool|>{{ .Tools }}<|/tool|><|end|>
{{- end }}
{{- end }}
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 -}}
{{- if ne .Role "system" }}<|{{ .Role }}|>{{ .Content }}
{{- if .ToolCalls }}<|tool_call|>[{{ range .ToolCalls }}{"name":"{{ .Function.Name }}","arguments":{{ .Function.Arguments }}{{ end }}]<|/tool_call|>
{{- end }}
{{- if not $last }}<|end|>
{{- end }}
{{- if and (ne .Role "assistant") $last }}<|end|><|assistant|>{{ end }}
{{- end }}
{{- end }}

gemma3:4b
31.5M
 Downloads
Updated 
2 months ago

The current, most capable model that runs on a single GPU.
vision
cloud
270m
1b
4b
12b
27b
gemma3:4b
/
template
e0a42594d802 · 358B
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if or (eq .Role "user") (eq .Role "system") }}<start_of_turn>user
{{ .Content }}<end_of_turn>
{{ if $last }}<start_of_turn>model
{{ end }}
{{- else if eq .Role "assistant" }}<start_of_turn>model
{{ .Content }}{{ if not $last }}<end_of_turn>
{{ end }}
{{- end }}
{{- end }}


llama3.2:3b
56.3M
 Downloads
Updated 
1 year ago

Meta's Llama 3.2 goes small with 1B and 3B models.
tools
1b
3b
llama3.2:3b
/
template
966de95ca8a6 · 1.4kB
<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023

{{ if .System }}{{ .System }}
{{- end }}
{{- if .Tools }}When you receive a tool call response, use the output to format an answer to the orginal user question.

You are a helpful assistant with tool calling capabilities.
{{- end }}<|eot_id|>
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if eq .Role "user" }}<|start_header_id|>user<|end_header_id|>
{{- if and $.Tools $last }}

Given the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.

Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.

{{ range $.Tools }}
{{- . }}
{{ end }}
{{ .Content }}<|eot_id|>
{{- else }}

{{ .Content }}<|eot_id|>
{{- end }}{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>
{{- if .ToolCalls }}
{{ range .ToolCalls }}
{"name": "{{ .Function.Name }}", "parameters": {{ .Function.Arguments }}}{{ end }}
{{- else }}

{{ .Content }}
{{- end }}{{ if not $last }}<|eot_id|>{{ end }}
{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>

{{ .Content }}<|eot_id|>{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- end }}
{{- end }}


