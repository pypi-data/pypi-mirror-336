FROM ghcr.io/diracgrid/diracx/services:dev

#Extension
ENV DIRACX_EXTENSIONS="lhcbdiracx,diracx"
ENV LHCBDIRACX_IMAGE_PACKAGES=db,logic,routers,client


ARG EXTRA_PACKAGES_TO_INSTALL

# Kaniko does not support bind mount
# https://github.com/GoogleContainerTools/kaniko/issues/1568
COPY --chown=$MAMBA_USER:$MAMBA_USER . /bindmount
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp

RUN micromamba install --freeze-installed --yes --file /tmp/environment.yml  --name=base && \
    micromamba clean --all --yes --force-pkgs-dirs && \
    rm -rf /tmp/environment.yml

RUN LHCBDIRACX_CUSTOM_SOURCE_PREFIXES=/bindmount /entrypoint.sh bash -exc "ls /bindmount && echo 'Running pip check' && pip check"
RUN rm -rf /bindmount/*
# # In many clusters the container is ran as a random uid for security reasons.
# # If we mark the conda directory as group 0 and give it group write permissions
# # then we're still able to manage the environment from inside the container.
USER 0
RUN chown -R $MAMBA_USER:0 /opt/conda && chmod -R g=u /opt/conda
USER $MAMBA_USER
