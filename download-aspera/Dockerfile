FROM ibmcom/aspera-cli:3.9.1.1401.be67d47

LABEL org.opencontainers.image.source https://github.com/edsu7/argo-data-submission

ENV PATH="/tools:${PATH}"

COPY *.py /tools/

ENTRYPOINT ["/usr/bin/env"]

CMD ["/bin/bash"]
