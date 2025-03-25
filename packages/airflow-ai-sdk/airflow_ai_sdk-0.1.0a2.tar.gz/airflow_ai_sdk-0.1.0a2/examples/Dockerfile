FROM quay.io/astronomer/astro-runtime:12.7.1-base

USER root

RUN pip install -U uv

COPY ./airflow-ai-sdk-slim  ${AIRFLOW_HOME}/airflow-ai-sdk-slim
COPY ./examples/requirements.txt ${AIRFLOW_HOME}/requirements.txt

# install the package in editable mode
RUN uv pip install --system -e "${AIRFLOW_HOME}/airflow-ai-sdk-slim"[openai,duckduckgo]

# install the requirements
RUN uv pip install --system -r requirements.txt

# make sure astro user owns the package
RUN chown -R astro:astro ${AIRFLOW_HOME}/airflow-ai-sdk-slim

USER astro