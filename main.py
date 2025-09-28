from fastapi import FastAPI
from pydantic import BaseModel
import re, sys, io

app = FastAPI()

class RequestData(BaseModel):
    instruction: str

class CodeRequest(BaseModel):
    code: str

def translate_to_python(instruction: str) -> str:
    instruction = instruction.lower()

    if "buat list angka" in instruction:
        match = re.search(r"(\d+)\s*sampai\s*(\d+)", instruction)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return f"angka = list(range({start}, {end+1}))\nprint(angka)"

    if "hitung jumlah" in instruction:
        return "data = [1,2,3,4,5]\nprint(sum(data))"

    if "cetak hello world" in instruction:
        return 'print("Hello, World!")'

    return "# Belum bisa menerjemahkan instruksi ini"

@app.post("/translate")
def translate(data: RequestData):
    code = translate_to_python(data.instruction)
    return {"code": code}

@app.post("/run")
def run_code(req: CodeRequest):
    code = req.code
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(code, {})
        output = redirected_output.getvalue()
    except Exception as e:
        output = f"Error: {e}"
    finally:
        sys.stdout = old_stdout
    return {"output": output}