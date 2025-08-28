FROM python:3

RUN pip install jupyter_kernel_gateway jupyter_client ipykernel \
    && pip install smolagents 'smolagents[toolkit]' \
    && python -m ipykernel install

EXPOSE 8888
CMD ["jupyter", "kernelgateway", "--KernelGatewayApp.ip='0.0.0.0'", "--KernelGatewayApp.port=8888", "--KernelGatewayApp.allow_origin='*'"]