FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app ${LAMBDA_TASK_ROOT}/app
COPY .env ${LAMBDA_TASK_ROOT}/.env

CMD ["handlers.main_handler.lambda_handler"]
