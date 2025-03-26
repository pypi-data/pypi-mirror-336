import os

from dotenv import load_dotenv

load_dotenv()

CONNEXITY_URL = os.environ.get('CONNEXITY_URL', default="https://connexity-gateway-owzhcfagkq-uc.a.run.app/process/sdk")
CONNEXITY_METRICS_URL = os.environ.get('CONNEXITY_METRICS_URL', default="https://connexity-gateway-owzhcfagkq-uc.a.run.app/process/sdk/llm_latency")