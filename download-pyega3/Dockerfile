FROM biocontainers/pyega3:4.0.1--pyhdfd78af_0

LABEL org.opencontainers.image.source https://github.com/edsu7/argo-data-submission

ENV PATH="/tools:${PATH}"

COPY *.py /tools/

ENTRYPOINT ["/usr/bin/env"]

CMD ["/bin/bash"]
