from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import gradio as gr

model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

def index(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)

    decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(decoded_outputs)

    return decoded_outputs

inputs_image_url = [
    gr.Textbox(type="text", label="Topic Name"),
]

outputs_result_dict = [
    gr.Textbox(type="text", label="Result"),
]

interface_image_url = gr.Interface(
    fn=index,
    inputs=inputs_image_url,
    outputs=outputs_result_dict,
    title="Text Generation",
    cache_examples=False,
)

gr.TabbedInterface(
    [interface_image_url],
    tab_names=['Some inference']
).launch()
