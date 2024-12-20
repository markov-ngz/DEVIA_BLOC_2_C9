from fastapi import  Depends, APIRouter , Request, Response
from prometheus_client import Gauge, Counter, Summary , Histogram , CollectorRegistry, generate_latest
import os , sys, time, base64
from transformers import AutoTokenizer
from transformers import TFAutoModelForSeq2SeqLM
from .. import schemas , oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TranslationFeedback

router = APIRouter(
    prefix="/translation",
    tags=['Translation']
)



env = os.getenv("ENVIRONNEMENT")
if env == "dev":
    model=TFAutoModelForSeq2SeqLM.from_pretrained(os.getenv("MODEL_PATH"),local_files_only=True)
    tokenizer=AutoTokenizer.from_pretrained(os.getenv("TOKEN_PATH"),local_files_only=True)
elif env == "test":
    model=TFAutoModelForSeq2SeqLM.from_pretrained(os.getenv("TEST_MODEL_PATH"))
    tokenizer=AutoTokenizer.from_pretrained(os.getenv("TEST_TOKEN_PATH"))
elif env== "prod":
    model=TFAutoModelForSeq2SeqLM.from_pretrained(os.getenv("MODEL_PATH"),local_files_only=True)
    tokenizer=AutoTokenizer.from_pretrained(os.getenv("TOKEN_PATH"),local_files_only=True)

#-------METRICS ----------------------------------------------------------------------------------------------------

registry = CollectorRegistry()
NAMESPACE = "model" 

# track the flux of inprogress translation 
g = Gauge('translations_inprogress', 'Inprogress Translations',namespace=NAMESPACE, registry=registry)
g.set_to_current_time()

# number of translation
c = Counter('translation_requests_total', 'Count request',namespace=NAMESPACE, registry=registry)

# number of translation succeeded
translation_counts_processed = Counter('translation_counts','Number of text translated',namespace=NAMESPACE, registry=registry) 

# average time of processing the request
REQUEST_TIME =  Histogram('translation_processing_seconds_bis', 'Time spent processing request',namespace=NAMESPACE, registry=registry)

# average size of the payload 
SIZE_BYTES_IN = Histogram('translation_size_bytes_in','In Request size (bytes)',namespace=NAMESPACE, registry=registry)
SIZE_BYTES_OUT = Histogram('translation_size_bytes_out',' Out Request size (bytes)',namespace=NAMESPACE, registry=registry)
SIZE_BYTES_GEN= Histogram('translation_size_bytes_gen','Generated Request size (bytes)',namespace=NAMESPACE, registry=registry)
#----------------------------------------------------------------------------------------------------------------



def translate(sample_text:str)->str: 

    batch = tokenizer([sample_text], return_tensors="tf")
    gen = model.generate(**batch)
    preds = tokenizer.batch_decode(gen, skip_special_tokens=True)

    return preds[0]

@g.track_inprogress()
@router.post("/",status_code=200, response_description="Translation procesed",response_model=schemas.TranslationOut)
def get_translation(payload:schemas.TranslationIn,current_user: int = Depends(oauth2.get_current_user)): 

    # 1. Get text from payload  ( + metrics )
    c.inc()
    size_payload = sys.getsizeof(payload.text)
    SIZE_BYTES_IN.observe(size_payload)
    text = payload.text
    
    # 2. Proceed the request  (+ metrics )
    start = time.time()
    translation = translate(text)
    REQUEST_TIME.observe(time.time()- start )
    size_gen = sys.getsizeof(translation)
    SIZE_BYTES_GEN.observe(size_gen)
    SIZE_BYTES_OUT.observe(sys.getsizeof(size_gen + size_payload))
    translation_counts_processed.inc()

    
    return {"text": text, "translation":translation}


@router.post("/feedback",status_code=201, response_description="API UP & Running", response_model=schemas.FeedbackOut)
def get_translation(payload:schemas.FeedbackIn, db :Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    new_fb = TranslationFeedback(**payload.model_dump())
    db.add(new_fb)
    db.commit()
    return {"message":"Feedback Saved"}


PROMETHEUS_PASSWORD = os.getenv("PROMETHEUS_PASSWORD")
PROMETHEUS_USERNAME = os.getenv("PROMETHEUS_USERNAME")

@router.get("/metrics/",status_code=200)
def metrics(request:Request):

   
    if 'Authorization' in request.headers:
        basic_auth = request.headers['Authorization'][6:]
        str_basic_auth = base64.b64decode(basic_auth).decode("utf-8")
        username, password = str_basic_auth.split(":")
        if username == PROMETHEUS_USERNAME and password == PROMETHEUS_PASSWORD:
            # response = Response(headers={'content_type':'text/plain'},status_code=200)
            # response.write(generate_latest(registry))
            return  generate_latest(registry)
    response = Response(status_code = 404 )
    return response


