ARG CODENAME=trixie
FROM debian:${CODENAME}-slim AS builder
ARG USERNAME=vscode
ARG GROUPNAME=vscode
ARG UID=1000
ARG GID=1000
ARG USERHOME=/home/${USERNAME}
ENV PYTHONUNBUFFERED=True
ENV UV_LINK_MODE=copy
ENV DPRINT_INSTALL=/home/${USERNAME}/.local
WORKDIR /workdir
ADD https://dprint.dev/install.sh dprint-installer.sh
ADD https://mise.run mise-installer.sh
ADD https://astral.sh/uv/install.sh uv-installer.sh
SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]
RUN : \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates=* curl=* unzip=* xz-utils=* \
    && groupadd -g $GID $GROUPNAME \
    && useradd -l -m -s /bin/bash -u $UID -g $GID $USERNAME \
    && touch mise-completions node-completions npm-completions uv-completions \
    && chown $USERNAME:$GROUPNAME ./*-completions \
    && chmod +r ./*-installer.sh
USER $USERNAME
RUN : \
    && bash dprint-installer.sh \
    && bash mise-installer.sh \
    && bash uv-installer.sh \
    && export PATH="${USERHOME}/.local/share/mise/shims:${USERHOME}/.local/bin:${PATH}" \
    && mise settings set node.compile false \
    && mise install node@lts \
    && mise use --global node@lts \
    && npm install -g @biomejs/biome@latest vite@latest markuplint@latest @google/clasp@latest @types/google-apps-script@latest @google/gemini-cli@latest \
    && uv tool install ruff@latest \
    && uv tool install ty@latest \
    && uv tool install shellcheck-py@latest \
    && uv tool install shfmt-py@latest \
    && uv tool install pre-commit@latest \
    && mise completion bash --include-bash-completion-lib > mise-completions \
    && uv generate-shell-completion bash > uv-completions \
    && node --completion-bash > node-completions \
    && npm completion > npm-completions \
    && echo 'alias ll="ls -lha --color=auto"' >> ${USERHOME}/.bash_aliases \
    && echo 'alias ..="cd .."' >> ${USERHOME}/.bash_aliases

ARG CODENAME=trixie
FROM mcr.microsoft.com/vscode/devcontainers/base:${CODENAME}
ARG USERNAME=vscode
ARG GROUPNAME=vscode
ARG USERHOME=/home/${USERNAME}
ENV PYTHONUNBUFFERED=True
ENV UV_LINK_MODE=copy
COPY --from=builder /workdir/*-completions /etc/bash_completion.d/
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${USERHOME}/.bash_aliases ${USERHOME}/
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${USERHOME}/.local ${USERHOME}/.local
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${USERHOME}/.config ${USERHOME}/.config
USER $USERNAME
# hadolint ignore=SC2016
RUN echo '[ -d "$HOME/.local/share/mise/shims" ] && export PATH="$HOME/.local/share/mise/shims:$PATH"' >> /${USERHOME}/.profile
